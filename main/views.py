from django.http import HttpResponse
from django.shortcuts import render, redirect

from main.models import Home, Product
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import pandas as pd


def home(request):
    homepage = Home.objects.first()
    return render(request, "main/home.html", {'home': homepage})


def women(request):
    womenProducts = Product.objects.filter(gender='women')
    return render(request, 'main/women.html', {'products': womenProducts})


def men(request):
    menProducts = Product.objects.filter(gender='men')
    return render(request, 'main/men.html', {'products': menProducts})


def unisex(request):
    return render(request, 'main/unisex.html')


def item(request, pk):
    item = Product.objects.select_related('info').get(pk=pk)
    return render(request, 'main/item.html', {"item": item})


def bag(request):
    cart = request.session.get('cart')
    product_ids = list(cart.keys())
    products = Product.objects.filter(id__in=product_ids)

    cart_items = []
    for product in products:
        quantity = cart[str(product.id)]
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': product.price * quantity
        })

    total_sum = sum(item['total_price'] for item in cart_items)

    return render(request, 'main/bag.html', {'cart_items': cart_items, 'total_sum': total_sum})


def add_to_bag(request, pk):
    cart = request.session.get('cart', {})
    pk_str = str(pk)

    cart[pk_str] = cart.get(pk_str, 0) + 1
    request.session['cart'] = cart
    return redirect(request.META.get('HTTP_REFERER', '/'))


def remove_from_bag(request, pk):
    cart = request.session.get('cart', {})
    pk_str = str(pk)
    if pk_str in cart:
        del cart[pk_str]
        request.session['cart'] = cart
        request.session.modified = True
    return redirect(bag)


def statistics(request):
    qs = Product.objects.select_related('statistics').all()


    data = []
    for product in qs:
        if hasattr(product, 'statistics'):
            data.append({
                'name': product.name,
                'gender': product.gender,
                'salesPerMonth': product.statistics.salesPerMonth,
                'price': product.price
            })

    df = pd.DataFrame(data)
    top_products = df.sort_values(by='salesPerMonth', ascending=False).head(5)


    plt.figure(figsize=(7, 4))
    plt.bar(top_products['name'], top_products['salesPerMonth'], color='skyblue')
    plt.title('Топ проданих товарів')
    plt.xlabel('Товар')
    plt.ylabel('Продаж за місяц')
    plt.xticks(rotation=15)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    chart = f'data:image/png;base64,{chart_base64}'


    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)
    excel_base64 = base64.b64encode(excel_buffer.read()).decode('utf-8')
    excel_file_url = f"data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{excel_base64}"


    table_html = df.sort_values(by='salesPerMonth', ascending=False).to_html(
        classes='table table-striped table-bordered',
        index=False,
        border=0
    )

    return render(request, 'main/statistics.html', {
        'chart': chart,
        'table': table_html,
        'excel_file_url': excel_file_url
    })
