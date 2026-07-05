/** @odoo-module **/

import { FDCalendar } from "./fd_calendar";

class BeautySPA {
    constructor() {
        this.app = document.getElementById("beauty_app");
        this.translations = {};
        const node = document.getElementById("fd_beauty_i18n");
        if (node) {
            try {
                this.translations = JSON.parse(node.textContent || "{}");
            } catch (error) {
                this.translations = {};
            }
        }

        this.state = {
            serviceId: null,
            serviceName: null,
            serviceData: null,
            selectedServices: [],
            combinationWarning: null,
            professionalId: null,
            professionalName: this.tr("Any professional"),
            day: null,
            slot: null,
            customer: {},
            services: [],
            serviceDetail: null,
            recommendedProfessional: null,
            availableDays: [],
            availableTimes: [],
            loading: false,
            bookingResult: null,
            servicesSummary: null,
        };

        this.step = "service";
    }

    tr(text) {
        return this.translations[text] || text;
    }

    async start() {
        if (!this.app) {
            return;
        }

        await this.loadServices();
        this.render();
    }

    async rpc(route, params = {}) {
        const response = await fetch(route, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                jsonrpc: "2.0",
                method: "call",
                params: params,
            }),
        });

        const payload = await response.json();

        if (payload.error) {
            throw payload.error;
        }

        return payload.result;
    }

    async loadServices() {
        this.state.loading = true;
        this.render();

        this.state.services = await this.rpc("/beauty/api/services");

        this.state.loading = false;
    }

    async loadServiceDetail(serviceId) {
        this.state.loading = true;
        this.render();

        const result = await this.rpc(`/beauty/api/service/${serviceId}`);

        this.state.serviceDetail = result.service || null;
        this.state.recommendedProfessional = result.recommended_professional || null;

        this.state.loading = false;
    }

    async loadAvailableDays() {
        this.state.loading = true;
        this.render();

        try {
            const today = new Date();
            const dateFrom = today.toISOString().slice(0, 10);

            const dateToObj = new Date(today);
            dateToObj.setDate(dateToObj.getDate() + 30);
            const dateTo = dateToObj.toISOString().slice(0, 10);

            const result = await this.rpc(
                `/beauty/api/service/${this.state.serviceId}/days`,
                {
                    date_from: dateFrom,
                    date_to: dateTo,
                    service_ids: this.getSelectedServiceIds(),
                }
            );

            this.state.availableDays = (result.days || []).filter((day) => day.available);
        } catch (error) {
            console.error(error);
            this.state.availableDays = [];
        }

        this.state.loading = false;
    }

    async loadAvailableTimes() {
        this.state.loading = true;
        this.render();

        try {
            const result = await this.rpc(
                `/beauty/api/service/${this.state.serviceId}/times`,
                {
                    target_date: this.state.day,
                    employee_id: this.state.professionalId || false,
                    service_ids: this.getSelectedServiceIds(),
                }
            );

            this.state.availableTimes = result.times || [];
        } catch (error) {
            console.error(error);
            this.state.availableTimes = [];
        }

        this.state.loading = false;
    }

    next(step) {
        this.step = step;
        this.render();
    }

    back(step) {
        this.step = step;
        this.render();
    }

    renderHeader(title, subtitle) {
        const steps = ["service", "professional", "calendar", "time", "customer", "confirm"];
        const labels = {
            service: this.tr("Service"),
            professional: this.tr("Professional"),
            calendar: this.tr("Date"),
            time: this.tr("Time"),
            customer: this.tr("Details"),
            confirm: this.tr("Confirm"),
        };
        const index = Math.max(steps.indexOf(this.step), 0);
        const progress = ((index + 1) / steps.length) * 100;

        return `
            <div class="fd-beauty-header text-center">
                <h1>${title}</h1>
                <p class="text-muted mb-0">${subtitle || ""}</p>
            </div>
            <div class="fd-beauty-progress">
                <div class="fd-beauty-progress-bar" style="width:${progress}%"></div>
            </div>
            <div class="fd-beauty-step-label">
                ${this.tr("Step")} ${index + 1} ${this.tr("of")} ${steps.length} · ${labels[this.step]}
            </div>
        `;
    }

    render() {
        if (!this.app) {
            return;
        }

        if (this.step === "service") {
            this.renderService();
        } else if (this.step === "professional") {
            this.renderProfessional();
        } else if (this.step === "calendar") {
            this.renderCalendar();
        } else if (this.step === "time") {
            this.renderTime();
        } else if (this.step === "customer") {
            this.renderCustomer();
        } else if (this.step === "confirm") {
            this.renderConfirm();
        }
    }

    getSelectedServiceIds() {
        return this.state.selectedServices.map((service) => service.id);
    }

    async loadServicesSummary() {
        if (!this.state.selectedServices.length) {
            this.state.servicesSummary = null;
            return;
        }
        const result = await this.rpc("/beauty/api/services/summary", {
            service_ids: this.getSelectedServiceIds(),
        });
        this.state.servicesSummary = result.summary || null;
    }

    getSelectedServicesTotalDuration() {
        if (this.state.servicesSummary) {
            return this.state.servicesSummary.effective_duration || 0;
        }
        return this.state.selectedServices.reduce((total, service) => total + (service.duration || 0), 0);
    }

    getSelectedServicesTotalPrice() {
        return this.state.selectedServices.reduce((total, service) => total + (service.price || 0), 0);
    }

    isServiceSelected(serviceId) {
        return this.state.selectedServices.some((service) => service.id === serviceId);
    }

    getDefaultCombinationMessage(service) {
        return service.combination_message || this.tr("This service cannot be combined with other services. Please make a separate booking.");
    }

    toggleService(service) {
        const selected = this.isServiceSelected(service.id);
        if (selected) {
            this.state.selectedServices = this.state.selectedServices.filter((item) => item.id !== service.id);
            this.state.combinationWarning = null;
            this.loadServicesSummary().then(() => this.renderService());
            return;
        }

        const isExclusive = service.combination_policy === "exclusive";
        const exclusiveSelected = this.state.selectedServices.find((item) => item.combination_policy === "exclusive");

        if (isExclusive && this.state.selectedServices.length) {
            this.state.combinationWarning = this.getDefaultCombinationMessage(service);
            this.renderService();
            return;
        }

        if (exclusiveSelected) {
            this.state.combinationWarning = this.getDefaultCombinationMessage(exclusiveSelected);
            this.renderService();
            return;
        }

        this.state.selectedServices.push(service);
        this.state.combinationWarning = null;
        this.loadServicesSummary().then(() => this.renderService());
    }

    async continueWithSelectedServices() {
        if (!this.state.selectedServices.length) {
            return;
        }

        const firstService = this.state.selectedServices[0];

        this.state.serviceId = firstService.id;
        this.state.serviceName = this.state.selectedServices.map((service) => service.name).join(" + ");

        await this.loadServiceDetail(this.state.serviceId);
        this.next("professional");
    }

    renderService() {
        if (this.state.loading) {
            this.app.innerHTML = `<div class="fd-beauty-shell fd-beauty-view">
                ${this.renderHeader(this.tr("Book your appointment"), this.tr("Loading services..."))}
                <div class="alert alert-light border">${this.tr("Loading...")}</div>
            </div>`;
            return;
        }

        const selectedCount = this.state.selectedServices.length;
        const totalDuration = this.getSelectedServicesTotalDuration();
        const totalPrice = this.getSelectedServicesTotalPrice();

        this.app.innerHTML = `<div class="fd-beauty-shell fd-beauty-view">
            ${this.renderHeader(this.tr("Book your appointment"), this.tr("Choose a service below"))}
            <div class="fd-beauty-service-list">
                ${this.state.services.map((service) => {
                    const selected = this.isServiceSelected(service.id);
                    return `
                        <button class="fd-card beauty-service-card ${selected ? "beauty-service-card-selected" : ""} w-100 text-start p-3 mb-3"
                                data-service-id="${service.id}">
                            <div class="d-flex justify-content-between align-items-start gap-3">
                                <div>
                                    <strong>${service.name}</strong>
                                    <div class="text-muted small">${service.duration || 0} min</div>
                                    ${service.combination_policy === "exclusive" ? `<div class="fd-service-exclusive-badge">${this.tr("Exclusive service")}</div>` : ""}
                                </div>
                                <div class="text-end">
                                    <strong>${service.price || 0} €</strong>
                                    <div class="beauty-service-check">${selected ? "✓" : "+"}</div>
                                </div>
                            </div>
                        </button>
                    `;
                }).join("")}
            </div>

            ${this.state.combinationWarning ? `
                <div class="alert alert-warning fd-combination-warning">
                    ${this.state.combinationWarning}
                </div>
            ` : ""}

            ${selectedCount ? `
                <div class="fd-service-basket">
                    <div class="fd-service-basket-content">
                        <div class="fd-service-basket-title">
                            <strong>${this.tr("Your booking")}</strong>
                            <span>${selectedCount} ${selectedCount === 1 ? this.tr("service selected") : this.tr("services selected")}</span>
                        </div>

                        <div class="fd-service-basket-lines">
                            ${this.state.selectedServices.map((service) => `
                                <div class="fd-service-basket-line">
                                    <span>✓ ${service.name}</span>
                                    <button type="button"
                                            class="fd-service-basket-remove"
                                            data-service-id="${service.id}"
                                            aria-label="${this.tr("Remove service")}">
                                        ×
                                    </button>
                                </div>
                            `).join("")}
                        </div>

                        <div class="fd-service-basket-total">
                            <span>${totalDuration} min</span>
                            <strong>${totalPrice} €</strong>
                        </div>
                    </div>

                    <button class="btn btn-primary" id="beauty_continue_services">
                        ${this.tr("Continue")}
                    </button>
                </div>
            ` : ""}
        </div>`;

        this.app.querySelectorAll(".beauty-service-card").forEach((item) => {
            item.addEventListener("click", () => {
                const serviceId = parseInt(item.dataset.serviceId);
                const service = this.state.services.find((item) => item.id === serviceId);
                if (service) {
                    this.toggleService(service);
                }
            });
        });

        this.app.querySelectorAll(".fd-service-basket-remove").forEach((button) => {
            button.addEventListener("click", (event) => {
                event.stopPropagation();
                const serviceId = parseInt(button.dataset.serviceId);
                this.state.selectedServices = this.state.selectedServices.filter((service) => service.id !== serviceId);
                this.loadServicesSummary().then(() => this.renderService());
            });
        });

        const continueButton = this.app.querySelector("#beauty_continue_services");
        if (continueButton) {
            continueButton.addEventListener("click", async () => {
                await this.continueWithSelectedServices();
            });
        }
    }

    renderProfessional() {
        if (this.state.loading) {
            this.app.innerHTML = `<div class="fd-beauty-shell fd-beauty-view">
                ${this.renderHeader(this.tr("Choose professional"), this.tr("Loading professionals..."))}
                <div class="alert alert-light border">${this.tr("Loading...")}</div>
            </div>`;
            return;
        }

        const professionals = this.state.serviceDetail?.professionals || [];

        this.app.innerHTML = `<div class="fd-beauty-shell fd-beauty-view">
            ${this.renderHeader(this.tr("Choose professional"), this.state.serviceName)}
            <div class="d-grid gap-2">
                <button class="fd-card w-100 text-start p-3 beauty-professional-card"
                        data-professional-id=""
                        data-professional-name="${this.tr("Any professional")}">
                    <strong>${this.tr("Any professional")}</strong>
                    <div class="text-muted small">${this.tr("Recommended if you want the first available option")}</div>
                </button>

                ${professionals.map((professional) => `
                    <button class="fd-card w-100 text-start p-3 beauty-professional-card"
                            data-professional-id="${professional.id}"
                            data-professional-name="${professional.name}">
                        <div class="d-flex justify-content-between">
                            <div>
                                <strong>${professional.name}</strong>
                                <div class="text-muted small">${professional.duration || 0} min</div>
                            </div>
                            <strong>${professional.price || 0} €</strong>
                        </div>
                    </button>
                `).join("")}
            </div>
            <button class="btn btn-link mt-3" id="beauty_back_service">${this.tr("Back")}</button>
        </div>`;

        this.app.querySelectorAll(".beauty-professional-card").forEach((item) => {
            item.addEventListener("click", async () => {
                this.state.professionalId = item.dataset.professionalId
                    ? parseInt(item.dataset.professionalId)
                    : null;
                this.state.professionalName = item.dataset.professionalName;
                await this.loadAvailableDays();
                this.next("calendar");
            });
        });

        this.app.querySelector("#beauty_back_service").addEventListener("click", () => {
            this.back("service");
        });
    }

    renderCalendar() {
        if (this.state.loading) {
            this.app.innerHTML = `<div class="fd-beauty-shell fd-beauty-view">
                ${this.renderHeader(this.tr("Choose date"), this.tr("Loading available days..."))}
                <div class="alert alert-light border">${this.tr("Loading...")}</div>
            </div>`;
            return;
        }

        this.app.innerHTML = `<div class="fd-beauty-shell fd-beauty-view">
            ${this.renderHeader(this.tr("Choose date"), this.state.serviceName)}
            <div id="beauty_calendar"></div>
            <button class="btn btn-link mt-3" id="beauty_back_professional">${this.tr("Back")}</button>
        </div>`;

        const calendar = new FDCalendar({
            el: this.app.querySelector("#beauty_calendar"),
            tr: (text) => this.tr(text),
            availableDays: this.state.availableDays,
            selectedDate: this.state.day,
            onSelect: async (date) => {
                this.state.day = date;
                await this.loadAvailableTimes();
                this.next("time");
            },
        });
        calendar.render();

        this.app.querySelector("#beauty_back_professional").addEventListener("click", () => {
            this.back("professional");
        });
    }

    renderTime() {
        if (this.state.loading) {
            this.app.innerHTML = `<div class="fd-beauty-shell fd-beauty-view">
                ${this.renderHeader(this.tr("Choose time"), this.tr("Loading available times..."))}
                <div class="alert alert-light border">${this.tr("Loading...")}</div>
            </div>`;
            return;
        }

        const formatTime = (isoValue) => {
            const date = new Date(isoValue);
            return date.toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit",
            });
        };

        this.app.innerHTML = `<div class="fd-beauty-shell fd-beauty-view">
            ${this.renderHeader(this.tr("Choose time"), this.state.day)}
            <div class="fd-time-grid">
                ${this.state.availableTimes.length ? this.state.availableTimes.map((slot) => `
                    <button class="fd-time-chip beauty-slot"
                            data-start="${slot.start}"
                            data-end="${slot.end}">
                        ${formatTime(slot.start)}
                    </button>
                `).join("") : `<div class="alert alert-warning">${this.tr("There is not enough available time for the selected services. Please choose fewer services or another date.")}</div>`}
            </div>
            <button class="btn btn-link mt-3" id="beauty_back_calendar">${this.tr("Back")}</button>
        </div>`;

        this.app.querySelectorAll(".beauty-slot").forEach((button) => {
            button.addEventListener("click", () => {
                this.state.slot = {
                    start: button.dataset.start,
                    end: button.dataset.end,
                };
                this.next("customer");
            });
        });

        this.app.querySelector("#beauty_back_calendar").addEventListener("click", () => {
            this.back("calendar");
        });
    }

    renderCustomer() {
        this.app.innerHTML = `<div class="fd-beauty-shell fd-beauty-view">
            ${this.renderHeader(this.tr("Your details"), this.tr("Almost done"))}
            <div class="mb-3">
                <input class="form-control" id="beauty_customer_name" placeholder="${this.tr("Name")}"/>
            </div>
            <div class="mb-3">
                <input class="form-control" id="beauty_customer_email" placeholder="${this.tr("Email")}"/>
            </div>
            <div class="mb-3">
                <input class="form-control" id="beauty_customer_phone" placeholder="${this.tr("Phone")}"/>
            </div>
            <button class="btn btn-primary" id="beauty_customer_continue">${this.tr("Continue")}</button>
            <button class="btn btn-link" id="beauty_back_time">${this.tr("Back")}</button>
        </div>`;

        this.app.querySelector("#beauty_customer_continue").addEventListener("click", () => {
            this.state.customer = {
                name: this.app.querySelector("#beauty_customer_name").value,
                email: this.app.querySelector("#beauty_customer_email").value,
                phone: this.app.querySelector("#beauty_customer_phone").value,
            };
            this.next("confirm");
        });

        this.app.querySelector("#beauty_back_time").addEventListener("click", () => {
            this.back("time");
        });
    }

    async createBooking() {
        if (!this.state.slot || !this.state.slot.start || !this.state.slot.end) {
            this.state.bookingResult = {
                success: false,
                errors: [this.tr("Please select an available time before confirming.")],
            };
            this.render();
            return;
        }

        this.state.loading = true;
        this.render();

        const result = await this.rpc("/beauty/api/booking", {
            service_id: this.state.serviceId,
            service_ids: this.getSelectedServiceIds(),
            start: this.state.slot.start,
            end: this.state.slot.end,
            employee_id: this.state.professionalId || false,
            customer: this.state.customer,
        });

        this.state.bookingResult = result;
        this.state.loading = false;

        this.render();
    }

    renderConfirm() {
        if (this.state.loading) {
            this.app.innerHTML = `<div class="fd-beauty-shell fd-beauty-view">
                ${this.renderHeader(this.tr("Confirm booking"), this.tr("Creating booking..."))}
                <div class="alert alert-light border">${this.tr("Creating booking...")}</div>
            </div>`;
            return;
        }

        if (this.state.bookingResult?.success) {
            this.app.innerHTML = `<div class="fd-beauty-shell fd-beauty-view">
                ${this.renderHeader(this.tr("Booking confirmed"), this.tr("Your appointment has been created"))}
                <div class="alert alert-success">
                    ${this.tr("Booking confirmed")}: <strong>${this.state.bookingResult.booking_name}</strong>
                </div>
            </div>`;
            return;
        }

        if (this.state.bookingResult && !this.state.bookingResult.success) {
            this.app.innerHTML = `<div class="fd-beauty-shell fd-beauty-view">
                ${this.renderHeader(this.tr("Booking error"), this.tr("Please review your booking"))}
                <div class="alert alert-danger">
                    ${(this.state.bookingResult.errors || []).join("<br/>")}
                </div>
                <button class="btn btn-link mt-3" id="beauty_back_customer">${this.tr("Back")}</button>
            </div>`;
            this.app.querySelector("#beauty_back_customer").addEventListener("click", () => {
                this.back("customer");
            });
            return;
        }

        this.app.innerHTML = `<div class="fd-beauty-shell fd-beauty-view">
            ${this.renderHeader(this.tr("Confirm booking"), this.tr("Review your appointment"))}
            <div class="card">
                <div class="card-body">
                    <p><strong>${this.tr("Service")}:</strong> ${this.state.serviceName}</p>
                    <p><strong>${this.tr("Professional")}:</strong> ${this.state.professionalName}</p>
                    <p><strong>${this.tr("Date")}:</strong> ${this.state.day}</p>
                    <p><strong>${this.tr("Time")}:</strong> ${this.state.slot?.start || ""}</p>
                    <p><strong>${this.tr("Customer")}:</strong> ${this.state.customer.name || ""}</p>
                </div>
            </div>
            <button class="btn btn-success mt-3" id="beauty_create_booking">${this.tr("Confirm booking")}</button>
            <button class="btn btn-link mt-3" id="beauty_back_customer">${this.tr("Back")}</button>
        </div>`;

        this.app.querySelector("#beauty_create_booking").addEventListener("click", () => {
            this.createBooking();
        });

        this.app.querySelector("#beauty_back_customer").addEventListener("click", () => {
            this.back("customer");
        });
    }
}

function startBeautySPA() {
    if (!window.BeautySPA) {
        window.BeautySPA = new BeautySPA();
        window.BeautySPA.start();
    }
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", startBeautySPA);
} else {
    startBeautySPA();
}
