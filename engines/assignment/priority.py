# -*- coding: utf-8 -*-

from .base import BaseAssignmentStrategy


class PriorityStrategy(BaseAssignmentStrategy):

    code = "priority"

    def execute(self, assignments):
        if not assignments:
            return self.env["fd.beauty.employee"]

        assignments = assignments.sorted(
            key=lambda a: (
                a.priority,
                a.sequence,
                a.id,
            )
        )

        return assignments[0].employee_id
