/** @odoo-module **/

class BeautySPA {

    constructor() {

        this.state = {
            service: null,
            professional: null,
            day: null,
            slot: null,
            customer: {},
        };

        this.step = "service";

        console.log("Beauty SPA ready");
    }

    next(step) {
        this.step = step;
        this.render();
    }

    render() {

        const el = document.getElementById("beauty_app");

        if (!el) {
            return;
        }

        el.innerHTML = `
            <div class="alert alert-info">
                Current step:
                <strong>${this.step}</strong>
            </div>
        `;
    }
}

window.addEventListener("load", () => {

    window.BeautySPA = new BeautySPA();

    BeautySPA.render();

});
