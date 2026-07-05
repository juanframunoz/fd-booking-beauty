/** @odoo-module **/

export class FDCalendar {
    constructor(options = {}) {
        this.el = options.el;
        this.tr = options.tr || ((text) => text);
        this.availableDays = options.availableDays || [];
        this.selectedDate = options.selectedDate || null;
        this.onSelect = options.onSelect || (() => {});
        this.currentDate = this.selectedDate
            ? new Date(this.selectedDate)
            : new Date();
    }

    setAvailableDays(days) {
        this.availableDays = days || [];
    }

    setSelectedDate(date) {
        this.selectedDate = date;
        if (date) {
            this.currentDate = new Date(date);
        }
    }

    getAvailableMap() {
        const map = {};
        for (const day of this.availableDays) {
            map[day.date] = day;
        }
        return map;
    }

    formatMonthTitle(date) {
        return date.toLocaleDateString(undefined, {
            month: "long",
            year: "numeric",
        });
    }

    isoDate(year, month, day) {
        return `${year}-${String(month + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
    }

    render() {
        if (!this.el) {
            return;
        }

        const availableMap = this.getAvailableMap();
        const year = this.currentDate.getFullYear();
        const month = this.currentDate.getMonth();
        const firstDay = new Date(year, month, 1);
        const lastDay = new Date(year, month + 1, 0);
        const startOffset = (firstDay.getDay() + 6) % 7;
        const todayIso = new Date().toISOString().slice(0, 10);

        const weekdays = [
            this.tr("Mon"),
            this.tr("Tue"),
            this.tr("Wed"),
            this.tr("Thu"),
            this.tr("Fri"),
            this.tr("Sat"),
            this.tr("Sun"),
        ];

        let cells = "";

        for (let i = 0; i < startOffset; i++) {
            cells += `<div class="fd-calendar-day fd-calendar-day-empty"></div>`;
        }

        for (let day = 1; day <= lastDay.getDate(); day++) {
            const iso = this.isoDate(year, month, day);
            const available = availableMap[iso];
            const isSelected = this.selectedDate === iso;
            const isToday = todayIso === iso;

            const classes = [
                "fd-calendar-day",
                available ? "fd-calendar-day-available" : "fd-calendar-day-disabled",
                isSelected ? "fd-calendar-day-selected" : "",
                isToday ? "fd-calendar-day-today" : "",
            ].filter(Boolean).join(" ");

            cells += `
                <button type="button"
                        class="${classes}"
                        data-date="${iso}"
                        ${available ? "" : "disabled"}>
                    <span>${day}</span>
                    ${available ? `<small>${available.slot_count || 0}</small>` : ""}
                </button>`;
        }

        this.el.innerHTML = `
            <div class="fd-calendar">
                <div class="fd-calendar-header">
                    <button type="button" class="fd-calendar-nav" data-action="prev">‹</button>
                    <strong>${this.formatMonthTitle(this.currentDate)}</strong>
                    <button type="button" class="fd-calendar-nav" data-action="next">›</button>
                </div>
                <div class="fd-calendar-weekdays">
                    ${weekdays.map((day) => `<span>${day}</span>`).join("")}
                </div>
                <div class="fd-calendar-grid">
                    ${cells}
                </div>
            </div>
        `;

        this.el.querySelectorAll(".fd-calendar-nav").forEach((button) => {
            button.addEventListener("click", () => {
                const action = button.dataset.action;
                this.currentDate = new Date(
                    year,
                    month + (action === "next" ? 1 : -1),
                    1
                );
                this.render();
            });
        });

        this.el.querySelectorAll(".fd-calendar-day-available").forEach((button) => {
            button.addEventListener("click", () => {
                this.selectedDate = button.dataset.date;
                this.onSelect(this.selectedDate);
                this.render();
            });
        });
    }
}
