# -*- coding: utf-8 -*-

import json
from markupsafe import Markup

from odoo import http
from odoo.http import request

from odoo.addons.fd_booking_beauty.services.beauty_public_api import BeautyPublicAPI


class BeautyPublicController(http.Controller):

    def _lang(self):
        return request.env.context.get("lang") or "en_US"

    def _frontend_i18n(self):
        base = {
            "Any professional": "Any professional",
            "Service": "Service",
            "Professional": "Professional",
            "Date": "Date",
            "Time": "Time",
            "Details": "Details",
            "Confirm": "Confirm",
            "Step": "Step",
            "of": "of",
            "Book your appointment": "Book your appointment",
            "Loading services...": "Loading services...",
            "Choose a service below": "Choose a service below",
            "Loading...": "Loading...",
            "Choose professional": "Choose professional",
            "Loading professionals...": "Loading professionals...",
            "Recommended if you want the first available option": "Recommended if you want the first available option",
            "Back": "Back",
            "Choose date": "Choose date",
            "Loading available days...": "Loading available days...",
            "available slots": "available slots",
            "No available days found.": "No available days found.",
            "Choose time": "Choose time",
            "Loading available times...": "Loading available times...",
            "No available times found.": "No available times found.",
            "There is not enough available time for the selected services. Please choose fewer services or another professional.": "There is not enough available time for the selected services. Please choose fewer services or another professional.",
            "There is not enough available time for the selected services. Please choose fewer services or another date.": "There is not enough available time for the selected services. Please choose fewer services or another date.",
            "Your details": "Your details",
            "Almost done": "Almost done",
            "Name": "Name",
            "Email": "Email",
            "Phone": "Phone",
            "Continue": "Continue",
            "Confirm booking": "Confirm booking",
            "Creating booking...": "Creating booking...",
            "Booking confirmed": "Booking confirmed",
            "Your appointment has been created": "Your appointment has been created",
            "Booking error": "Booking error",
            "Please review your booking": "Please review your booking",
            "Please select an available time before confirming.": "Please select an available time before confirming.",
            "Review your appointment": "Review your appointment",
            "Customer": "Customer",
            "Beauty appointments": "Beauty appointments",
        }

        es = {
            "Any professional": "Sin preferencia",
            "Service": "Servicio",
            "Professional": "Profesional",
            "Date": "Fecha",
            "Time": "Hora",
            "Details": "Datos",
            "Confirm": "Confirmar",
            "Step": "Paso",
            "of": "de",
            "Book your appointment": "Reserva tu cita",
            "Loading services...": "Cargando servicios...",
            "Choose a service below": "Elige un servicio",
            "Loading...": "Cargando...",
            "Choose professional": "Elige profesional",
            "Loading professionals...": "Cargando profesionales...",
            "Recommended if you want the first available option": "Te asignaremos la primera opción disponible",
            "Back": "Volver",
            "Choose date": "Elige fecha",
            "Loading available days...": "Cargando días disponibles...",
            "available slots": "huecos disponibles",
            "No available days found.": "No hay días disponibles.",
            "Choose time": "Elige hora",
            "Loading available times...": "Cargando horas disponibles...",
            "No available times found.": "No hay horas disponibles.",
            "There is not enough available time for the selected services. Please choose fewer services or another professional.": "No hay tiempo disponible suficiente para los servicios seleccionados. Elige menos servicios u otro profesional.",
            "There is not enough available time for the selected services. Please choose fewer services or another date.": "No hay tiempo disponible suficiente para los servicios seleccionados. Elige menos servicios u otra fecha.",
            "Your details": "Tus datos",
            "Almost done": "Ya casi está",
            "Name": "Nombre",
            "Email": "Correo electrónico",
            "Phone": "Teléfono",
            "Continue": "Continuar",
            "Confirm booking": "Confirmar reserva",
            "Creating booking...": "Creando reserva...",
            "Booking confirmed": "Reserva confirmada",
            "Your appointment has been created": "Tu cita se ha creado correctamente",
            "Booking error": "Error en la reserva",
            "Please review your booking": "Revisa los datos de la reserva",
            "Please select an available time before confirming.": "Selecciona una hora disponible antes de confirmar.",
            "Review your appointment": "Revisa tu cita",
            "Customer": "Cliente",
            "Beauty appointments": "Reservas de belleza",
        }

        fr = {
            "Any professional": "Sans préférence",
            "Service": "Service",
            "Professional": "Professionnel",
            "Date": "Date",
            "Time": "Heure",
            "Details": "Coordonnées",
            "Confirm": "Confirmer",
            "Step": "Étape",
            "of": "sur",
            "Book your appointment": "Réservez votre rendez-vous",
            "Loading services...": "Chargement des services...",
            "Choose a service below": "Choisissez un service",
            "Loading...": "Chargement...",
            "Choose professional": "Choisissez un professionnel",
            "Loading professionals...": "Chargement des professionnels...",
            "Recommended if you want the first available option": "Nous vous attribuerons la première option disponible",
            "Back": "Retour",
            "Choose date": "Choisissez une date",
            "Loading available days...": "Chargement des jours disponibles...",
            "available slots": "créneaux disponibles",
            "No available days found.": "Aucun jour disponible.",
            "Choose time": "Choisissez une heure",
            "Loading available times...": "Chargement des heures disponibles...",
            "No available times found.": "Aucune heure disponible.",
            "Your details": "Vos coordonnées",
            "Almost done": "C'est presque terminé",
            "Name": "Nom",
            "Email": "E-mail",
            "Phone": "Téléphone",
            "Continue": "Continuer",
            "Confirm booking": "Confirmer la réservation",
            "Creating booking...": "Création de la réservation...",
            "Booking confirmed": "Réservation confirmée",
            "Your appointment has been created": "Votre rendez-vous a bien été créé",
            "Booking error": "Erreur de réservation",
            "Please review your booking": "Veuillez vérifier votre réservation",
            "Review your appointment": "Vérifiez votre rendez-vous",
            "Customer": "Client",
            "Beauty appointments": "Réservations beauté",
        }

        de = {
            "Any professional": "Keine Präferenz",
            "Service": "Service",
            "Professional": "Fachkraft",
            "Date": "Datum",
            "Time": "Uhrzeit",
            "Details": "Daten",
            "Confirm": "Bestätigen",
            "Step": "Schritt",
            "of": "von",
            "Book your appointment": "Termin buchen",
            "Loading services...": "Services werden geladen...",
            "Choose a service below": "Wählen Sie einen Service",
            "Loading...": "Wird geladen...",
            "Choose professional": "Fachkraft auswählen",
            "Loading professionals...": "Fachkräfte werden geladen...",
            "Recommended if you want the first available option": "Wir weisen Ihnen die erste verfügbare Option zu",
            "Back": "Zurück",
            "Choose date": "Datum auswählen",
            "Loading available days...": "Verfügbare Tage werden geladen...",
            "available slots": "freie Termine",
            "No available days found.": "Keine verfügbaren Tage gefunden.",
            "Choose time": "Uhrzeit auswählen",
            "Loading available times...": "Verfügbare Zeiten werden geladen...",
            "No available times found.": "Keine verfügbaren Zeiten gefunden.",
            "Your details": "Ihre Daten",
            "Almost done": "Fast fertig",
            "Name": "Name",
            "Email": "E-Mail",
            "Phone": "Telefon",
            "Continue": "Weiter",
            "Confirm booking": "Buchung bestätigen",
            "Creating booking...": "Buchung wird erstellt...",
            "Booking confirmed": "Buchung bestätigt",
            "Your appointment has been created": "Ihr Termin wurde erstellt",
            "Booking error": "Buchungsfehler",
            "Please review your booking": "Bitte prüfen Sie Ihre Buchung",
            "Review your appointment": "Termin überprüfen",
            "Customer": "Kunde",
            "Beauty appointments": "Beauty-Termine",
        }

        it = {
            "Any professional": "Nessuna preferenza",
            "Service": "Servizio",
            "Professional": "Professionista",
            "Date": "Data",
            "Time": "Ora",
            "Details": "Dati",
            "Confirm": "Conferma",
            "Step": "Passo",
            "of": "di",
            "Book your appointment": "Prenota il tuo appuntamento",
            "Loading services...": "Caricamento servizi...",
            "Choose a service below": "Scegli un servizio",
            "Loading...": "Caricamento...",
            "Choose professional": "Scegli professionista",
            "Loading professionals...": "Caricamento professionisti...",
            "Recommended if you want the first available option": "Ti assegneremo la prima opzione disponibile",
            "Back": "Indietro",
            "Choose date": "Scegli data",
            "Loading available days...": "Caricamento giorni disponibili...",
            "available slots": "slot disponibili",
            "No available days found.": "Nessun giorno disponibile.",
            "Choose time": "Scegli ora",
            "Loading available times...": "Caricamento orari disponibili...",
            "No available times found.": "Nessun orario disponibile.",
            "Your details": "I tuoi dati",
            "Almost done": "Ci siamo quasi",
            "Name": "Nome",
            "Email": "Email",
            "Phone": "Telefono",
            "Continue": "Continua",
            "Confirm booking": "Conferma prenotazione",
            "Creating booking...": "Creazione prenotazione...",
            "Booking confirmed": "Prenotazione confermata",
            "Your appointment has been created": "Il tuo appuntamento è stato creato",
            "Booking error": "Errore di prenotazione",
            "Please review your booking": "Controlla i dati della prenotazione",
            "Review your appointment": "Rivedi il tuo appuntamento",
            "Customer": "Cliente",
            "Beauty appointments": "Prenotazioni bellezza",
        }

        pt = {
            "Any professional": "Sem preferência",
            "Service": "Serviço",
            "Professional": "Profissional",
            "Date": "Data",
            "Time": "Hora",
            "Details": "Dados",
            "Confirm": "Confirmar",
            "Step": "Passo",
            "of": "de",
            "Book your appointment": "Reserve a sua marcação",
            "Loading services...": "A carregar serviços...",
            "Choose a service below": "Escolha um serviço",
            "Loading...": "A carregar...",
            "Choose professional": "Escolha profissional",
            "Loading professionals...": "A carregar profissionais...",
            "Recommended if you want the first available option": "Atribuiremos a primeira opção disponível",
            "Back": "Voltar",
            "Choose date": "Escolha a data",
            "Loading available days...": "A carregar dias disponíveis...",
            "available slots": "horários disponíveis",
            "No available days found.": "Não há dias disponíveis.",
            "Choose time": "Escolha a hora",
            "Loading available times...": "A carregar horas disponíveis...",
            "No available times found.": "Não há horas disponíveis.",
            "Your details": "Os seus dados",
            "Almost done": "Está quase",
            "Name": "Nome",
            "Email": "Email",
            "Phone": "Telefone",
            "Continue": "Continuar",
            "Confirm booking": "Confirmar reserva",
            "Creating booking...": "A criar reserva...",
            "Booking confirmed": "Reserva confirmada",
            "Your appointment has been created": "A sua marcação foi criada corretamente",
            "Booking error": "Erro na reserva",
            "Please review your booking": "Reveja os dados da reserva",
            "Review your appointment": "Reveja a sua marcação",
            "Customer": "Cliente",
            "Beauty appointments": "Reservas de beleza",
        }

        lang = self._lang()
        if lang.startswith("es"):
            return {**base, **es}
        if lang.startswith("fr"):
            return {**base, **fr}
        if lang.startswith("de"):
            return {**base, **de}
        if lang.startswith("it"):
            return {**base, **it}
        if lang.startswith("pt"):
            return {**base, **pt}
        return base

    @http.route("/beauty/api/services/summary", type="json", auth="public", website=True)
    def beauty_api_services_summary(self, service_ids=None):
        api = BeautyPublicAPI(request.env)
        return api.get_services_summary(service_ids or [])


    @http.route("/beauty/api/services", type="json", auth="public", website=True)
    def beauty_api_services(self):
        services = request.env["fd.beauty.service"].sudo().search([], order="name")
        result = []
        for service in services:
            template = service.booking_template_id
            result.append({
                "id": service.id,
                "name": service.name,
                "duration": service.duration,
                "price": service.list_price,
                "combination_policy": template.combination_policy if template and "combination_policy" in template._fields else "combine_freely",
                "combination_message": template.combination_message if template and "combination_message" in template._fields else "",
                "time_optimization_percent": template.time_optimization_percent if template and "time_optimization_percent" in template._fields else 0.0,
            })
        return result

    @http.route(["/beauty", "/belleza"], type="http", auth="public", website=True)
    def beauty_home(self, **kw):
        translations = self._frontend_i18n()
        services = request.env["fd.beauty.service"].sudo().search([("active", "=", True)])
        return request.render("fd_booking_beauty.beauty_homepage", {
            "services": services,
            "page_title": translations.get("Beauty appointments", "Beauty appointments"),
            "translations_json": Markup(json.dumps(translations, ensure_ascii=False)),
        })

    @http.route("/beauty/api/booking", type="json", auth="public", website=True)
    def beauty_api_booking(self, service_id, start, end, customer, employee_id=False, service_ids=None):
        api = BeautyPublicAPI(request.env)
        return api.create_booking(
            service_id=service_id,
            start=start,
            end=end,
            customer=customer,
            employee_id=employee_id,
            service_ids=service_ids,
        )

    @http.route("/beauty/api/service/<int:service_id>/times", type="json", auth="public", website=True)
    def beauty_api_service_times(self, service_id, target_date, employee_id=False, service_ids=None):
        from datetime import datetime
        api = BeautyPublicAPI(request.env)
        return api.get_available_times(
            service_id,
            datetime.strptime(target_date, "%Y-%m-%d").date(),
            employee_id=employee_id,
            service_ids=service_ids,
        )

    @http.route("/beauty/api/service/<int:service_id>/days", type="json", auth="public", website=True)
    def beauty_api_service_days(self, service_id, date_from, date_to, service_ids=None):
        from datetime import datetime
        api = BeautyPublicAPI(request.env)
        return api.get_available_days(
            service_id,
            datetime.strptime(date_from, "%Y-%m-%d").date(),
            datetime.strptime(date_to, "%Y-%m-%d").date(),
            service_ids=service_ids,
        )

    @http.route("/beauty/api/service/<int:service_id>", type="json", auth="public")
    def beauty_service(self, service_id):
        api = BeautyPublicAPI(request.env)
        return api.get_service(service_id)
