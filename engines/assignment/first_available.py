# -*- coding: utf-8 -*-

from .base import BaseAssignmentStrategy


class FirstAvailableStrategy(BaseAssignmentStrategy):

    code = "first_available"

    def execute(self, assignments):
        if not assignments:
            return self.env["fd.beauty.employee"]

        return assignments[0].employee_id
