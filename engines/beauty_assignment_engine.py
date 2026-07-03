# -*- coding: utf-8 -*-

class BeautyAssignmentEngine:
    """
    Assignment engine for Beauty vertical.

    Responsible for selecting the professional that will
    perform a booking according to the configured strategy.
    """

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
            order="priority asc, sequence asc, id asc",
        )

        if not assignments:
            return self.env["fd.beauty.employee"]

        if strategy == "manual":
            return self.env["fd.beauty.employee"]

        if strategy == "first_available":
            return assignments[0].employee_id

        if strategy == "priority":
            return assignments[0].employee_id

        return assignments[0].employee_id
