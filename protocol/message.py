from dataclasses import dataclass
from typing import Union, Optional
import uuid

B2BValue = Union[int, float, str]

def short_id(uid: str, size=8):
    return uid[:size] if uid else "-"

@dataclass
class B2BCMessage:
    msg_id: str
    in_reply_to: Optional[str]
    opkey: str
    optype: str
    key: str
    value: B2BValue

    @staticmethod
    def parse(raw: str) -> "B2BCMessage":
        """
        Format:
        msg_id|in_reply_to|opkey>optype>key>value

        in_reply_to may be empty.
        """
        try:
            envelope, payload = raw.split("|", 1)
            msg_id, in_reply_to = envelope.split(",", 1)
            in_reply_to = in_reply_to or None
        except ValueError:
            raise ValueError("Invalid B2B/c envelope")

        parts = payload.split(">", 3)
        if len(parts) != 4:
            raise ValueError("Invalid B2B/c message format")

        opkey, optype, key, raw_value = parts

        # Type coercion
        if raw_value.isdigit():
            value = int(raw_value)
        else:
            try:
                value = float(raw_value)
            except ValueError:
                value = raw_value

        return B2BCMessage(
            msg_id=msg_id,
            in_reply_to=in_reply_to,
            opkey=opkey.upper(),
            optype=optype,
            key=key,
            value=value,
        )

    @staticmethod
    def create(opkey, optype, key, value, in_reply_to=None):
        return B2BCMessage(
            msg_id=str(uuid.uuid4()),
            in_reply_to=in_reply_to,
            opkey=opkey.upper(),
            optype=optype,
            key=key,
            value=value,
        )

    @staticmethod
    def create_from_payload(payload: str):
        return B2BCMessage.create(
            *payload.split(">", 3)
        )


    def serialize(self) -> str:
        reply = self.in_reply_to or ""
        return f"{self.msg_id},{reply}|{self.opkey}>{self.optype}>{self.key}>{self.value}"

    def pretty(self) -> str:
        lines = []

        header = f"{self.opkey}"
        if self.optype:
            header += f"::{self.optype}"

        lines.append(header)

        lines.append(f"  id: {short_id(self.msg_id)}")
        if self.in_reply_to:
            lines.append(f"  ↳ reply_to: {short_id(self.in_reply_to)}")

        if self.key:
            lines.append(f"  key: {self.key}")
        if self.value is not None:
            lines.append(f"  value: {self.value}")

        return "\n".join(lines)