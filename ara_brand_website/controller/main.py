# -*- coding: utf-8 -*-
from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request
from odoo.osv import expression
import logging

_logger = logging.getLogger(__name__)


class WebsiteSaleBrand(WebsiteSale):

    def _get_search_options(
        self, category=None, attrib_values=None, tags=None,
        min_price=0.0, max_price=0.0, conversion_rate=1, **post
    ):
        """Override default search options untuk tambahkan filter brand."""
        options = super()._get_search_options(
            category=category,
            attrib_values=attrib_values,
            tags=tags,
            min_price=min_price,
            max_price=max_price,
            conversion_rate=conversion_rate,
            **post
        )

        # domain default Odoo
        base_domain = request.website.sale_product_domain()

        # ambil brand_id dari URL
        brand_id = request.httprequest.args.get("brand_id")
        if brand_id and brand_id.isdigit():
            # ✅ perbaikan di sini: gunakan 'product_brand_id' bukan 'product.brand'
            brand_domain = [('product_brand_id', '=', int(brand_id))]
            final_domain = expression.AND([base_domain, brand_domain])
            options["domain"] = final_domain
            _logger.info(
                "💡 Filtering with brand_id=%s | Final domain=%s", brand_id, final_domain
            )
        else:
            options["domain"] = base_domain
            _logger.info(
                "💡 No brand filter, using base_domain=%s", base_domain
            )

        return options

    def _shop_lookup_products(self, attrib_set, options, post, search, website):
        """Custom pencarian produk saat ada filter brand."""
        brand_id = request.httprequest.args.get("brand_id")
        domain = options.get("domain", [])

        if brand_id and brand_id.isdigit():
            # Kalau ada filter brand -> manual search (tanpa fuzzy)
            products = request.env["product.template"].with_context(
                bin_size=True
            ).search(domain)
            _logger.info(
                "📊 Brand search -> brand_id=%s | domain=%s | found=%s",
                brand_id, domain, len(products)
            )
            return False, len(products), products
        else:
            # Kalau All Brands -> pakai fuzzy bawaan Odoo
            _logger.info(
                "🔎 _shop_lookup_products domain=%s | search='%s'", domain, search
            )
            product_count, details, fuzzy_search_term = website._search_with_fuzzy(
                "product.template", search,
                limit=None,
                order=self._get_search_order(post),
                options={"domain": domain}
            )
            _logger.info(
                "📊 All brands fuzzy -> count=%s | fuzzy_term=%s | details_len=%s",
                product_count, fuzzy_search_term, len(details)
            )

            if details and details[0].get("results"):
                search_result = details[0]["results"].with_context(bin_size=True)
            else:
                _logger.warning(
                    "⚠️ No details returned from fuzzy search, fallback to full domain search"
                )
                search_result = request.env["product.template"].with_context(
                    bin_size=True
                ).search(domain)

            return fuzzy_search_term, product_count, search_result

    def _get_shop_domain(self, search, category, attrib_values, search_in_description=True):
        """Tambahkan domain filter brand ke domain utama shop."""
        domain = super()._get_shop_domain(
            search, category, attrib_values, search_in_description
        )

        brand_id = request.httprequest.args.get('brand_id')
        if brand_id and brand_id.isdigit():
            domain = expression.AND(
                [domain, [('product_brand_id', '=', int(brand_id))]]
            )
            _logger.info(
                "🔧 _get_shop_domain final domain with brand_id=%s -> %s", brand_id, domain
            )
        else:
            _logger.info(
                "🔧 _get_shop_domain final domain (no brand) -> %s", domain
            )

        return domain

    def _get_additional_extra_shop_values(self, values, **post):
        """Tambahkan daftar brand & brand terpilih ke template context."""
        values = super()._get_additional_extra_shop_values(values, **post)

        Brand = request.env['product.brand'].sudo()
        values['brands'] = Brand.search([])
        values['selected_brand'] = request.httprequest.args.get('brand_id')

        return values
