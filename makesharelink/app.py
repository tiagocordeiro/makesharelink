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
        description = r.html.find('#tab-description', first=True)
        options = r.html.find('.options', first=True)
        if options:
            pricevalue = 'a partir de ' + price.text
        else:
            pricevalue = price.text

        print(product.text)
        print(image.attrs['src'])
        print(price.text)
        print(description.text[:896] + '...')
        print('saiba mais ' + url)
        return render_template('index.html', url=url, product=product.text,
                               image=image.attrs['src'], price=pricevalue,
                               description=description.text[:896] + '...')

    return application
