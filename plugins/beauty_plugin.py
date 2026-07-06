# -*- coding: utf-8 -*-

from odoo.addons.fd_booking.services.plugin import BookingPlugin
from odoo.addons.fd_booking.services.plugin_registry import PluginRegistry


class BeautyPlugin(BookingPlugin):
    code = "beauty"
    name = "Beauty"

    def _has_services(self, env):
        return bool(env["fd.beauty.service"].sudo().search_count([]))

    def _has_employees(self, env):
        return bool(env["fd.beauty.employee"].sudo().search_count([]))

    def _has_cabins(self, env):
        return bool(env["fd.beauty.cabin"].sudo().search_count([]))

    def _has_availability(self, env):
        return bool(env["fd.booking.availability"].sudo().search_count([]))

    def _has_first_booking(self, env):
        return bool(env["fd.booking"].sudo().search_count([]))

    def _state(self, condition):
        return "done" if condition else "pending"

    def get_onboarding_steps(self, env):
        return [
            {
                "code": "services",
                "name": "Create your services",
                "sequence": 10,
                "state": self._state(self._has_services(env)),
            },
            {
                "code": "employees",
                "name": "Create your professionals",
                "sequence": 20,
                "state": self._state(self._has_employees(env)),
            },
            {
                "code": "cabins",
                "name": "Create your cabins",
                "sequence": 30,
                "state": self._state(self._has_cabins(env)),
                "optional": True,
            },
            {
                "code": "availability",
                "name": "Configure availability",
                "sequence": 40,
                "state": self._state(self._has_availability(env)),
            },
            {
                "code": "public_page",
                "name": "Review your booking page",
                "sequence": 50,
                "state": "done",
            },
            {
                "code": "first_booking",
                "name": "Create your first booking",
                "sequence": 60,
                "state": self._state(self._has_first_booking(env)),
                "optional": True,
            },
        ]


PluginRegistry.register(BeautyPlugin())
