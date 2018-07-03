from flask import Flask, request, render_template
from requests_html import HTMLSession


def create_app():
    application = Flask(__name__)

    @application.route('/')
    def index():
        return 'Hello'

    @application.route('/makelink/', methods=['PUT', 'GET'])
    def geturl():
        url = request.args.get('url')
        session = HTMLSession()
        r = session.get(url)
        product = r.html.find('.heading-title', first=True)
        image = r.html.find('#image', first=True)
        price = r.html.find('.product-price', first=True)
        price_old = r.html.find('#product > ul.list-unstyled.price > li.price-old', first=True)
        price_new = r.html.find('#product > ul.list-unstyled.price > li.price-new', first=True)
        description = r.html.find('#tab-description', first=True)
        options = r.html.find('.options', first=True)

        if price:
            if options:
                pricevalue = 'a partir de ' + price.text
            else:
                pricevalue = price.text

        if price_new and price_old:
            pricevalue = 'de ' + price_old.text + ' por ' + price_new.text
        
        return render_template('product.html', url=url, product=product.text,
                               image=image.attrs['src'], price=pricevalue,
                               description=description.text[:896] + '...')

    return application
