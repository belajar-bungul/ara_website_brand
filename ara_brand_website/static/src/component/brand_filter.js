/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget"
import { ensureJQuery } from "@web/core/ensure_jquery"

publicWidget.registry.BrandSelect = publicWidget.Widget.extend({
    selector: "#fal_brand_select",
    start: async function () {
        await ensureJQuery()
        this.$el.select2()
        this.$el.on("change", function () {
            let brandId = $(this).val()
            let url = new URL(window.location.href)
            if (brandId) {
                url.searchParams.set("brand_id", brandId) // ✅ samakan dengan Python
            } else {
                url.searchParams.delete("brand_id")
            }
            window.location.href = url.toString()
        })
    },
})
