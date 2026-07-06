# -*- coding: utf-8 -*-

from odoo.addons.fd_booking.services.plugin import BookingPlugin
from odoo.addons.fd_booking.services.plugin_registry import PluginRegistry


class BeautyPlugin(BookingPlugin):
    code = "beauty"
    name = "Beauty"

    def _state(self, condition):
        return "done" if condition else "pending"

    def get_onboarding_steps(self, env):
        return [
            {
                "code": "services",
                "name": "Create your services",
                "sequence": 10,
            },
            {
                "code": "employees",
                "name": "Create your professionals",
                "sequence": 20,
            },
            {
                "code": "cabins",
                "name": "Create your cabins",
                "sequence": 30,
                "optional": True,
            },
            {
                "code": "availability",
                "name": "Configure availability",
                "sequence": 40,
            },
            {
                "code": "public_page",
                "name": "Review your booking page",
                "sequence": 50,
            },
            {
                "code": "first_booking",
                "name": "Create your first booking",
                "sequence": 60,
                "optional": True,
            },
        ]

    def get_onboarding_step_state(self, env, step):
        code = step.get("code")

        if code == "services":
            return self._state(env["fd.beauty.service"].sudo().search_count([]))

        if code == "employees":
            return self._state(env["fd.beauty.employee"].sudo().search_count([]))

        if code == "cabins":
            return self._state(env["fd.beauty.cabin"].sudo().search_count([]))

        if code == "availability":
            return self._state(env["fd.booking.availability"].sudo().search_count([]))

        if code == "public_page":
            return "done"

        if code == "first_booking":
            return self._state(env["fd.booking"].sudo().search_count([]))

        return "pending"


PluginRegistry.register(BeautyPlugin())
