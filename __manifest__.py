# -*- coding: utf-8 -*-
{
    "name": "FD Booking Beauty",
    "summary": "Beauty and aesthetics vertical for FD Booking Engine",
    "version": "17.0.0.1.0",
    "category": "Services/Booking",
    "author": "Factor Digital",
    "website": "https://factordigital.es",
    "license": "LGPL-3",
    "depends": [
        "fd_booking",
    ],
    "assets": {
        "web.assets_frontend": [
            "fd_booking_beauty/static/src/js/fd_calendar.js",
            "fd_booking_beauty/static/src/js/beauty_spa.js",
            "fd_booking_beauty/static/src/scss/beauty.scss",
            "fd_booking_beauty/static/src/scss/fd_calendar.scss",
        ],
    },
    "data": [
        "security/ir.model.access.csv",
        "data/beauty_demo_data.xml",
        "views/beauty_service_views.xml",
        "views/beauty_employee_views.xml",
        "views/beauty_employee_service_views.xml",
        "views/beauty_cabin_views.xml",
        "wizard/beauty_booking_wizard_views.xml",
        "views/beauty_menu_views.xml",
        "views/beauty_homepage.xml",
    ],
    "installable": True,
    "application": True,
}
