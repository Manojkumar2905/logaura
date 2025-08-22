from threading import Thread


class CustomThread(Thread):
    def __init__(self, target, args=(), **kwargs):
        super().__init__(target=target, args=args, kwargs=kwargs)
        self.result = None

    def run(self):
        self.result = self._target(*self._args, **self._kwargs)

    def join(self, *args, **kwargs):
        super().join(*args, **kwargs)
        return self.result
