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
    "data": [
        "security/ir.model.access.csv",
        "data/beauty_demo_data.xml",
        "views/beauty_service_views.xml",   # <-- AÑADIR ESTA LÍNEA
        "views/beauty_employee_views.xml",
        "views/beauty_employee_service_views.xml",
        "views/beauty_menu_views.xml",
    ],
    "installable": True,
    "application": True,
}
