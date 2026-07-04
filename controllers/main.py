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
        "/beauty/api/service/<int:service_id>",
        type="json",
        auth="public",
    )
    def beauty_service(self, service_id):

        api = BeautyPublicAPI(request.env)

        return api.get_service(service_id)
