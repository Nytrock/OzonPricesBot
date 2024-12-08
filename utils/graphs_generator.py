import datetime
import io
from typing import Any

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from database.methods import get_product_prices


async def get_price_graph(product_id: int, product_title: str, have_card: bool, i18n: dict[str, Any]) -> bytes:
    prices = await get_product_prices(product_id)
    plt.clf()

    plt.style.use('dark_background')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=2))

    plt.title(product_title, fontsize=7, y=1.04)

    all_y = []
    for i in range(len(prices) - 1):
        x = [prices[i].datetime, prices[i + 1].datetime]

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

    if len(prices) == 1:
        price = prices[0]
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))

        x = [price.datetime - datetime.timedelta(days=1), price.datetime]

        if have_card:
            y = [price.card_price, price.card_price]
        else:
            y = [price.regular_price, price.regular_price]

        if not price.in_stock:
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
