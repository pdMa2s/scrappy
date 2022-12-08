import asyncio
from abc import ABC, abstractmethod


class Notifier(ABC):
    @abstractmethod
    def notify(self, msg: str):
        pass


class AsynchronousNotifier(Notifier, ABC):
    @abstractmethod
    def notify(self, msg: str):
        pass

    async def run(self, msg: str):
        from random import randint
        await asyncio.sleep(randint(1, 6))
        self.notify(msg)


class StandardOutputNotifier(AsynchronousNotifier):
    def notify(self, msg: str):
        print(msg)


class Subject:
    notifiers: list[Notifier]
