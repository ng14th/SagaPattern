# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from threading import Lock


class Singleton:
    _singleton_lock = Lock()

    def __new__(cls, *args, **kwargs) -> object:
        """Control singleton instance creation."""
        with cls._singleton_lock:
            if not hasattr(cls, '_singleton_instance') or not cls._singleton_instance:
                cls._singleton_instance = super().__new__(cls)
            return cls._singleton_instance

    def __init__(self, **kwargs):
        """Singleton initialization."""
        if not hasattr(self, '_singleton_init_done'):
            self._singleton_init(**kwargs)
            self._singleton_init_done = True  # Ensure init runs only once

    @abstractmethod
    def _singleton_init(self, **kwargs):
        """You must override this method."""
        raise NotImplementedError

    def __repr__(self):
        return f"<{self.__class__.__name__} Singleton instance>"
