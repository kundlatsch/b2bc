from protocol.message import B2BCMessage
from protocol.state import MentalState


class B2BCProtocol:
    def __init__(self, state: MentalState, entity_name: str = "entity"):
        self.state = state
        self.entity_name = entity_name
        self.emit_listeners = []

    # -------------------------
    # Public API
    # -------------------------
    def on_emit(self, callback):
        self.emit_listeners.append(callback)

    def handle(self, msg: B2BCMessage):
        if msg.opkey == "DELTA":
            return self._handle_delta(msg)

        if msg.opkey == "ASSERT":
            self.state.set(msg.key, msg.value)
            return self._ack(msg, "ok")

        if msg.opkey == "QUERY":
            return self._query(msg)

        if msg.opkey == "EMIT":
            return self._emit(msg)

        if msg.opkey in ("ACK", "DATA", "ERR"):
            # Protocol-level responses are terminal
            return None

        return self._err(msg, "unknown_operation")

    # -------------------------
    # Operations
    # -------------------------
    def _handle_delta(self, msg: B2BCMessage):
        if msg.key is None:
            return self._err(msg, "missing_key")

        value = msg.value

        if msg.optype == "set":
            self.state.set(msg.key, value)

        elif msg.optype in ("add", "slide"):
            current = self.state.get(msg.key) or 0
            if not isinstance(current, (int, float)) \
               or not isinstance(value, (int, float)):
                return self._err(msg, "numeric_required")
            self.state.set(msg.key, current + value)

        else:
            return self._err(msg, "unknown_delta_type")

        return self._ack(msg, "ok")

    def _query(self, msg: B2BCMessage):
        responses = []

        if msg.optype == "overall":
            responses.append(
                self._data(
                    msg,
                    "overall",
                    round(self.state.overall(), 4)
                )
            )
            for k, v in self.state.data.items():
                responses.append(
                    self._data(msg, k, v)
                )
            return responses

        if msg.optype == "get" and msg.key:
            value = self.state.get(msg.key)
            return self._data(msg, msg.key, value)

        return self._err(msg, "invalid_query")

    def _emit(self, msg: B2BCMessage):
        for listener in self.emit_listeners:
            listener(msg)

        return self._ack(msg, "ok")

    # -------------------------
    # Responses
    # -------------------------
    def _ack(self, msg: B2BCMessage, status: str):
        return B2BCMessage.create(
            opkey="ACK",
            optype="of",
            key=msg.opkey,
            value=status,
            in_reply_to=msg.msg_id
        )

    def _data(self, msg: B2BCMessage, key, value):
        return B2BCMessage.create(
            opkey="DATA",
            optype="value",
            key=key,
            value=value,
            in_reply_to=msg.msg_id
        )

    def _err(self, msg: B2BCMessage, error: str):
        return B2BCMessage.create(
            opkey="ERR",
            optype="protocol",
            key=error,
            value="error",
            in_reply_to=msg.msg_id
        )
