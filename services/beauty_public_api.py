# -*- coding: utf-8 -*-

from odoo.addons.fd_booking_beauty.booking_flow.flow import BeautyBookingFlow


class BeautyPublicAPI:

    def __init__(self, env):
        self.env = env
        self.flow = BeautyBookingFlow(env)

    def get_service(self, service_id):

        result = self.flow.run({
            "service_id": service_id,
        })

        if not result.success:
            return {
                "success": False,
                "errors": result.errors,
            }

        data = result.data

        return {
            "success": True,
            "service": data["provider_data"],
            "recommended_professional":
                data["recommended_professional"].id
                if data.get("recommended_professional")
                else False,
        }
