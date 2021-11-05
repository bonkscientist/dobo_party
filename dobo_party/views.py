from django.http import HttpResponse
from django.shortcuts import render
from PIL import Image, ImageDraw, ImageFilter
import io
import os.path
import requests
from decouple import config


def home_page_view(request):
    return HttpResponse("<a href='https://www.dropbox.com/s/px5wb0crgdt6tfu/Why%20dogebonk%20can%20only%20rug%20upwards.pdf?dl=0'>Why dogebonk is decentralized (report)</a><br><br>"
                        "Call https://dobo.party/api/bonked-coin/?ticker=TICKER to get an image of the coin being bonked. <br>"
                        "For example, for SHIBA call <a href='https://dobo.party/api/bonked-coin/?ticker=SHIB'>https://dobo.party/api/bonked-coin/?ticker=SHIB</a> <br><br>"
                        "Contributions welcome: <a href='https://github.com/bonkscientist'>https://github.com/bonkscientist</a>")


def bonked_coin(request):
    try:
        ticker = request.GET['ticker']
    except:
        return HttpResponse("MISSING TICKER!! <br><br>" + "Call https://dobo.party/api/bonked-coin/?ticker=TICKER to get an image of the coin being bonked. <br>"
                        "For example, for SHIBA call <a href='https://dobo.party/api/bonked-coin/?ticker=SHIB'>https://dobo.party/api/bonked-coin/?ticker=SHIB</a> <br><br>")

    if  os.path.isfile('dobo_party/images/bonked_' + ticker + '.png'):
        return serve_image(ticker)

    COINMARKETCAP_API_KEY = config('CMC_API_KEY')
    h = {"X-CMC_PRO_API_KEY": COINMARKETCAP_API_KEY}
    r = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/info?symbol=' + ticker, headers=h)

    coin_id = r.json()['data'][ticker]['id']
    r = requests.get('https://s2.coinmarketcap.com/static/img/coins/200x200/' + str(coin_id) + '.png')
    file = open("dobo_party/images/logo.png", "wb")
    file.write(r.content)
    file.close()
    logo = Image.open('dobo_party/images/logo.png')

    # render image
    im1 = Image.open('dobo_party/images/background.png')
    im2 = Image.open('dobo_party/images/bonk.png')
    im1.paste(logo, (400, 200), logo.convert('RGBA'))
    im1.paste(im2, (0, 0), im2)
    im1.save('dobo_party/images/bonked_' + ticker + '.png', quality=95)

    return serve_image(ticker)


def serve_image(ticker):
    im = Image.open('dobo_party/images/bonked_' + ticker + '.png')
    img_byte_arr = io.BytesIO()
    im.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return HttpResponse(img_byte_arr, content_type='image/png')
