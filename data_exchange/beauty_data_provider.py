# -*- coding: utf-8 -*-

from odoo.addons.fd_booking.services.data_provider import DataProvider
from odoo.addons.fd_booking.services.data_provider_registry import DataProviderRegistry


class BeautyDataProvider(DataProvider):
    code = "beauty"
    name = "Beauty"

    def templates(self, env):
        return [
            {
                "code": "services",
                "name": "Beauty services",
                "description": "Import beauty services, durations and prices.",
                "formats": ["xlsx", "csv"],
            },
            {
                "code": "professionals",
                "name": "Beauty professionals",
                "description": "Import beauty professionals.",
                "formats": ["xlsx", "csv"],
            },
            {
                "code": "cabins",
                "name": "Beauty cabins",
                "description": "Import beauty cabins.",
                "formats": ["xlsx", "csv"],
            },
            {
                "code": "assignments",
                "name": "Beauty assignments",
                "description": "Import professional-service assignments.",
                "formats": ["xlsx", "csv"],
            },
        ]


DataProviderRegistry.register(BeautyDataProvider())
