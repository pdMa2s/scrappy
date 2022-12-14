import asyncio
from abc import ABC, abstractmethod

from discord import SyncWebhook


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
        await asyncio.sleep(randint(3, 10))
        self.notify(msg)


class StandardOutputNotifier(AsynchronousNotifier):
    def notify(self, msg: str):
        print(msg)


class DiscordNotifier(AsynchronousNotifier):
    def __init__(self, channel_webhook_url: str):
        self.webhook = SyncWebhook.from_url(channel_webhook_url)

    def notify(self, msg: str):
        self.webhook.send(msg)


class Broadcaster:
    _notifiers: list[Notifier] = []

    def attach(self, notifier: Notifier):
        self._notifiers.append(notifier)

    def attach_all(self, notifiers: list[Notifier]):
        self._notifiers.extend(notifiers)

    def broadcast(self, msg):
        for notifier in self._notifiers:
            notifier.notify(msg)
