/** @odoo-module **/

class BeautySPA {
    constructor() {
        this.app = document.getElementById("beauty_app");

        this.state = {
            serviceId: null,
            serviceName: null,
            serviceData: null,
            professionalId: null,
            professionalName: "Any professional",
            day: null,
            slot: null,
            customer: {},
            services: [],
            serviceDetail: null,
            recommendedProfessional: null,
            availableDays: [],
            availableTimes: [],
            loading: false,
        };

        this.step = "service";
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
            }
        );

        this.state.availableDays = (result.days || []).filter((day) => day.available);

        this.state.loading = false;
    }

    async loadAvailableTimes() {
        this.state.loading = true;
        this.render();

        const result = await this.rpc(
            `/beauty/api/service/${this.state.serviceId}/times`,
            {
                target_date: this.state.day,
                employee_id: this.state.professionalId || false,
            }
        );

        this.state.availableTimes = result.times || [];

        this.state.loading = false;
    }

    bindInitialServices() {
        document.querySelectorAll(".beauty-service").forEach((item) => {
            item.addEventListener("click", (event) => {
                event.preventDefault();

                this.state.serviceId = parseInt(item.dataset.id);
                this.state.serviceName = item.querySelector("strong")?.innerText || "Service";

                this.step = "professional";
                this.render();
            });
        });
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
        return `
            <div class="fd-beauty-header text-center mb-4">
                <h1>${title}</h1>
                <p class="text-muted">${subtitle || ""}</p>
            </div>
            <div class="fd-beauty-stepper mb-4">
                <span class="${this.step === "service" ? "fw-bold" : ""}">Service</span>
                <span> → </span>
                <span class="${this.step === "professional" ? "fw-bold" : ""}">Professional</span>
                <span> → </span>
                <span class="${this.step === "calendar" ? "fw-bold" : ""}">Date</span>
                <span> → </span>
                <span class="${this.step === "time" ? "fw-bold" : ""}">Time</span>
                <span> → </span>
                <span class="${this.step === "customer" ? "fw-bold" : ""}">Customer</span>
                <span> → </span>
                <span class="${this.step === "confirm" ? "fw-bold" : ""}">Confirm</span>
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

    renderService() {
        if (this.state.loading) {
            this.app.innerHTML = `
                ${this.renderHeader("Book your appointment", "Loading services...")}
                <div class="alert alert-light border">Loading...</div>
            `;
            return;
        }

        this.app.innerHTML = `
            ${this.renderHeader("Book your appointment", "Choose a service below")}
            <div class="fd-beauty-service-list">
                ${this.state.services.map((service) => `
                    <button class="fd-card beauty-service-card w-100 text-start p-3 mb-3"
                            data-service-id="${service.id}"
                            data-service-name="${service.name}">
                        <div class="d-flex justify-content-between align-items-start">
                            <div>
                                <strong>${service.name}</strong>
                                <div class="text-muted small">${service.duration || 0} min</div>
                            </div>
                            <strong>${service.price || 0} €</strong>
                        </div>
                    </button>
                `).join("")}
            </div>
        `;

        this.app.querySelectorAll(".beauty-service-card").forEach((item) => {
            item.addEventListener("click", () => {
                this.state.serviceId = parseInt(item.dataset.serviceId);
                this.state.serviceName = item.dataset.serviceName;
                await this.loadServiceDetail(this.state.serviceId);
                this.next("professional");
            });
        });
    }

    renderProfessional() {
        if (this.state.loading) {
            this.app.innerHTML = `
                ${this.renderHeader("Choose professional", "Loading professionals...")}
                <div class="alert alert-light border">Loading...</div>
            `;
            return;
        }

        const professionals = this.state.serviceDetail?.professionals || [];

        this.app.innerHTML = `
            ${this.renderHeader("Choose professional", this.state.serviceName)}
            <div class="d-grid gap-2">
                <button class="fd-card w-100 text-start p-3 beauty-professional-card"
                        data-professional-id=""
                        data-professional-name="Any professional">
                    <strong>Any professional</strong>
                    <div class="text-muted small">Recommended if you want the first available option</div>
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
            <button class="btn btn-link mt-3" id="beauty_back_service">Back</button>
        `;

        this.app.querySelectorAll(".beauty-professional-card").forEach((item) => {
            item.addEventListener("click", () => {
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
            this.app.innerHTML = `
                ${this.renderHeader("Choose date", "Loading available days...")}
                <div class="alert alert-light border">Loading...</div>
            `;
            return;
        }

        this.app.innerHTML = `
            ${this.renderHeader("Choose date", this.state.serviceName)}
            <div class="d-grid gap-2">
                ${this.state.availableDays.map((day) => `
                    <button class="fd-card w-100 text-start p-3 beauty-day-card"
                            data-day="${day.date}">
                        <strong>${day.date}</strong>
                        <div class="text-muted small">${day.slot_count || 0} available slots</div>
                    </button>
                `).join("") || '<div class="alert alert-warning">No available days found.</div>'}
            </div>
            <button class="btn btn-link mt-3" id="beauty_back_professional">Back</button>
        `;

        this.app.querySelectorAll(".beauty-day-card").forEach((button) => {
            button.addEventListener("click", () => {
                this.state.day = button.dataset.day;
                await this.loadAvailableTimes();
                this.next("time");
            });
        });

        this.app.querySelector("#beauty_back_professional").addEventListener("click", () => {
            this.back("professional");
        });
    }

    renderTime() {
        if (this.state.loading) {
            this.app.innerHTML = `
                ${this.renderHeader("Choose time", "Loading available times...")}
                <div class="alert alert-light border">Loading...</div>
            `;
            return;
        }

        const formatTime = (isoValue) => {
            const date = new Date(isoValue);
            return date.toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit",
            });
        };

        this.app.innerHTML = `
            ${this.renderHeader("Choose time", this.state.day)}
            <div class="d-grid gap-2">
                ${this.state.availableTimes.map((slot) => `
                    <button class="btn btn-outline-primary beauty-slot"
                            data-start="${slot.start}"
                            data-end="${slot.end}">
                        ${formatTime(slot.start)}
                    </button>
                `).join("") || '<div class="alert alert-warning">No available times found.</div>'}
            </div>
            <button class="btn btn-link mt-3" id="beauty_back_calendar">Back</button>
        `;

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
        this.app.innerHTML = `
            ${this.renderHeader("Your details", "Almost done")}
            <div class="mb-3">
                <input class="form-control" id="beauty_customer_name" placeholder="Name"/>
            </div>
            <div class="mb-3">
                <input class="form-control" id="beauty_customer_email" placeholder="Email"/>
            </div>
            <div class="mb-3">
                <input class="form-control" id="beauty_customer_phone" placeholder="Phone"/>
            </div>
            <button class="btn btn-primary" id="beauty_customer_continue">Continue</button>
            <button class="btn btn-link" id="beauty_back_time">Back</button>
        `;

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

    renderConfirm() {
        this.app.innerHTML = `
            ${this.renderHeader("Confirm booking", "Review your appointment")}
            <div class="card">
                <div class="card-body">
                    <p><strong>Service:</strong> ${this.state.serviceName}</p>
                    <p><strong>Professional:</strong> ${this.state.professionalName}</p>
                    <p><strong>Date:</strong> ${this.state.day}</p>
                    <p><strong>Time:</strong> ${this.state.slot?.start || ""}</p>
                    <p><strong>Customer:</strong> ${this.state.customer.name || ""}</p>
                </div>
            </div>
            <button class="btn btn-success mt-3" disabled>Create booking soon</button>
            <button class="btn btn-link mt-3" id="beauty_back_customer">Back</button>
        `;

        this.app.querySelector("#beauty_back_customer").addEventListener("click", () => {
            this.back("customer");
        });
    }
}

window.addEventListener("load", () => {
    window.BeautySPA = new BeautySPA();
    window.BeautySPA.start();
});
