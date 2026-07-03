# -*- coding: utf-8 -*-

from .assignment import (
    FirstAvailableStrategy,
    PriorityStrategy,
)


class BeautyAssignmentEngine:

    STRATEGIES = {
        "first_available": FirstAvailableStrategy,
        "priority": PriorityStrategy,
    }

    def __init__(self, env):
        self.env = env

    def select_professional(
        self,
        beauty_service,
        strategy="first_available",
    ):

        assignments = self.env["fd.beauty.employee.service"].search(
            [
                ("service_id", "=", beauty_service.id),
                ("active", "=", True),
                ("allow_online", "=", True),
                ("employee_id.active", "=", True),
            ],
            order="priority,sequence,id",
        )

        strategy_cls = self.STRATEGIES.get(
            strategy,
            FirstAvailableStrategy,
        )

        return strategy_cls(self.env).execute(assignments)
