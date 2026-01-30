from protocol.engine import B2BCProtocol
from protocol.message import B2BCMessage
from protocol.state import MentalState


class Peer:
    def __init__(self, name):
        self.name = name
        self.state = MentalState()
        self.engine = B2BCProtocol(self.state, entity_name=name)

    def send(self, target, message: B2BCMessage):
        raw = message.serialize()
        print(f"\n[{self.name} SENDS]")
        print("  " + message.pretty().replace("\n", "\n  "))
        print(f"  (wire) {raw}")

        return target.receive(raw)


    def receive(self, raw: str):
        print(f"\n[{self.name} RECEIVES]")
        print(f"  (wire) {raw}")

        msg = B2BCMessage.parse(raw)
        result = self.engine.handle(msg)

        def show(m):
            print("  ↳ " + m.pretty().replace("\n", "\n    "))

        if result is None:
            return None

        if isinstance(result, list):
            for r in result:
                show(r)
        else:
            show(result)

        return result

