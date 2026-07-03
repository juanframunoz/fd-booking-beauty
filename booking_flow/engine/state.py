# -*- coding: utf-8 -*-

from dataclasses import dataclass, field


@dataclass
class FlowState:
    step: str = "select_service"
    finished: bool = False
    cancelled: bool = False
    context: dict = field(default_factory=dict)
    errors: list = field(default_factory=list)

    def next(self, step):
        self.step = step

    def finish(self):
        self.finished = True

    def cancel(self):
        self.cancelled = True

    def add_error(self, message):
        self.errors.append(message)
