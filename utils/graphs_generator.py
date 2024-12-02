import datetime
import io
from typing import Any

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from database.methods import get_product_prices
from database.models import Price


async def get_price_graph(product_id: int, product_title: str, have_card: bool, i18n: dict[str, Any]) -> bytes:
    prices = await get_product_prices(product_id)
    plt.clf()

    plt.style.use('dark_background')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=2))

    plt.title(product_title, fontsize=8, y=1.04)

    all_y = []
    for i in range(len(prices) - 1):
        x = [prices[i].date, prices[i + 1].date]

        if have_card:
            y = [prices[i].card_price, prices[i + 1].card_price]
        else:
            y = [prices[i].regular_price, prices[i + 1].regular_price]

        if not prices[i].in_stock:
            color = 'gray'
        else:
            color = 'green'

        if all_y:
            all_y.pop(-1)
        all_y.extend(y)

        plt.plot(x, y, color=color, label=i18n[f'graph_{color}'])

    external_prices = []
    if prices[-1].date != datetime.datetime.now():
        last_price = prices[-1]
        fake_price = Price(
            date=datetime.datetime.now(),
            regular_price=last_price.regular_price,
            card_price=last_price.card_price
        )
        external_prices = [last_price, fake_price]
    elif len(prices) == 1:
        external_prices = [prices[-1].date - datetime.timedelta(days=1), prices[-1].date]
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))

    if external_prices:
        x = [external_prices[0].date, external_prices[1].date]

        if have_card:
            y = [external_prices[0].card_price, external_prices[1].card_price]
        else:
            y = [external_prices[0].regular_price, external_prices[1].regular_price]

        if not external_prices[0].in_stock:
            color = 'gray'
        else:
            color = 'green'

        all_y.extend(y)
        plt.plot(x, y, color=color, label=i18n[f'graph_{color}'])

    all_y_labels = [f'{y} {i18n["rub"]}' for y in all_y]
    plt.yticks(all_y, all_y_labels)

    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())

    fig = plt.gcf()
    fig.autofmt_xdate()

    buf = io.BytesIO()
    plt.savefig(buf, dpi=300)
    buf.seek(0)

    return buf.read()
