import asyncio
from abc import ABC, abstractmethod

from discord import SyncWebhook


class AsynchronousNotifier(ABC):
    async def notify_async(self, msg: str):
        self._notify_(msg)

    @abstractmethod
    def _notify_(self, msg: str):
        pass


class StandardOutputNotifier(AsynchronousNotifier):
    def _notify_(self, msg: str):
        print(msg)


class DiscordNotifier(AsynchronousNotifier):
    def __init__(self, channel_webhook_url: str):
        self.webhook = SyncWebhook.from_url(channel_webhook_url)

    def _notify_(self, msg: str):
        self.webhook.send(msg)


class Broadcaster:
    _notifiers: list[AsynchronousNotifier] = []

    def attach(self, notifier: AsynchronousNotifier):
        self._notifiers.append(notifier)

    def attach_all(self, notifiers: list[AsynchronousNotifier]):
        self._notifiers.extend(notifiers)

    async def broadcast(self, msg):
        tasks = [asyncio.create_task(notifier.notify_async(msg)) for notifier in self._notifiers]
        await asyncio.wait(tasks)
