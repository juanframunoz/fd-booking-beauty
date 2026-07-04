# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request

from odoo.addons.fd_booking_beauty.services.beauty_public_api import BeautyPublicAPI


class BeautyPublicController(http.Controller):


    @http.route("/beauty/api/services", type="json", auth="public", website=True)
    def beauty_api_services(self):
        services = request.env["fd.beauty.service"].sudo().search(
            [],
            order="name"
        )

        return [
            {
                "id": service.id,
                "name": service.name,
                "duration": service.duration,
                "price": service.list_price,
            }
            for service in services
        ]

    @http.route(
        "/beauty",
        type="http",
        auth="public",
        website=True,
    )
    def beauty_home(self, **kw):

        services = request.env["fd.beauty.service"].sudo().search([
            ("active", "=", True),
        ])

        return request.render(
            "fd_booking_beauty.beauty_homepage",
            {
                "services": services,
            },
        )




    @http.route(
        "/beauty/api/service/<int:service_id>/times",
        type="json",
        auth="public",
        website=True,
    )
    def beauty_api_service_times(self, service_id, target_date, employee_id=False):

        from datetime import datetime

        api = BeautyPublicAPI(request.env)

        return api.get_available_times(
            service_id,
            datetime.strptime(target_date, "%Y-%m-%d").date(),
            employee_id=employee_id,
        )


    @http.route(
        "/beauty/api/service/<int:service_id>/days",
        type="json",
        auth="public",
        website=True,
    )
    def beauty_api_service_days(self, service_id, date_from, date_to):

        from datetime import datetime

        api = BeautyPublicAPI(request.env)

        return api.get_available_days(
            service_id,
            datetime.strptime(date_from, "%Y-%m-%d").date(),
            datetime.strptime(date_to, "%Y-%m-%d").date(),
        )

    @http.route(
        "/beauty/api/service/<int:service_id>",
        type="json",
        auth="public",
    )
    def beauty_service(self, service_id):

        api = BeautyPublicAPI(request.env)

        return api.get_service(service_id)
