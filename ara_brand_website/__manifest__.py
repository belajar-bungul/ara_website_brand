{
    'name': 'ARA Brand Website',
    'category': 'portal',
    'version': "18.0.0.0.0",
    'author': 'ARA Soft',
    'depends': [
        'website_sale', 'product_brand'
    ],
    "data": [
        "views/product_brand_views.xml",
        "views/templates.xml",
        "views/mega_menu_brands.xml",
        "views/snippet.xml",
    ],
    'assets': {
        'web.assets_frontend': [
            '/ara_brand_website/static/src/**/*',
        ],
    },
    'demo': [
    ],
    "price" : 56.10,
    "currency": "USD",
    "license": "AGPL-3",
    'application': False,
    'images': ['static/description/banner.gif'],
}
