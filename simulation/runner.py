from peer import Peer
from protocol.message import B2BCMessage


class SimulationRunner:
    def __init__(self):
        self.alice = Peer("Alice")
        self.bob = Peer("Bob")

        self.peers = {
            "alice": self.alice,
            "bob": self.bob,
        }

        # Optional: listen to EMITs
        self.alice.engine.on_emit(self._on_emit)
        self.bob.engine.on_emit(self._on_emit)

    def _on_emit(self, msg: B2BCMessage):
        print(f"  <TRIGGER> [EMIT RECEIVED] {msg.key}: {msg.value}")

    def run_file(self, path: str):
        print(f"\n=== Running BTB/C simulation: {path} ===")

        with open(path, "r", encoding="utf-8") as f:
            for lineno, line in enumerate(f, 1):
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                try:
                    self._execute_line(line)
                except Exception as e:
                    print(f"\n[ERROR line {lineno}] {e}")

    def _execute_line(self, line: str):
        """
        Syntax:
            sender -> receiver : OPKEY>optype>key>value
        """

        header, payload = line.split(":", 1)
        sender_name, receiver_name = map(str.strip, header.split("->"))

        sender = self.peers[sender_name.lower()]
        receiver = self.peers[receiver_name.lower()]

        msg = B2BCMessage.create_from_payload(payload.strip())

        sender.send(receiver, msg)
