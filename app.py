from flask import Flask, render_template, redirect, url_for, session
import mercadopago
import os

app = Flask(__name__)
app.secret_key = '202501'

sdk = mercadopago.SDK("APP_USR-1050632944109688-061818-c3aaa6a92666a7d8d93c06e828a85646-2507084684")

productos = [
    {'id': 1, 'nombre': 'Camiseta Barça', 'precio': 50, 'imagen': 'https://static.wixstatic.com/media/ca2cbe_7e46cba9ddef4919b2f8de9f81f2da27~mv2.jpg/v1/fill/w_516,h_689,al_c,q_80,enc_avif,quality_auto/ca2cbe_7e46cba9ddef4919b2f8de9f81f2da27~mv2.jpg', 'descripcion': 'Camiseta oficial del FC Barcelona. Con los colores tradicionales del club, esta camiseta es ideal para mostrar tu apoyo al equipo.', 'tallas': ['S', 'M', 'L', 'XL']},
    {'id': 2, 'nombre': 'Camiseta Real Madrid', 'precio': 55, 'imagen': 'https://static.wixstatic.com/media/ca2cbe_0b9e9cb66b404de685b3a07ac71b8c45~mv2.jpg/v1/fill/w_516,h_689,al_c,q_80,enc_avif,quality_auto/ca2cbe_0b9e9cb66b404de685b3a07ac71b8c45~mv2.jpg', 'descripcion': 'Camiseta oficial del Real Madrid. Elegante y cómoda, perfecta para los fanáticos más apasionados del equipo.', 'tallas': ['M', 'L', 'XL']},
    {'id': 3, 'nombre': 'Camiseta Juventus', 'precio': 60, 'imagen': 'https://static.wixstatic.com/media/ca2cbe_dd086ec0ac92496397ead762aaca56e9~mv2.jpg/v1/fill/w_516,h_689,al_c,q_80,enc_avif,quality_auto/ca2cbe_dd086ec0ac92496397ead762aaca56e9~mv2.jpg', 'descripcion': 'Camiseta oficial de la Juventus, de color blanco y negro con un diseño moderno que representa el poder y la historia de este club icónico.', 'tallas': ['S', 'M', 'L']},
    {'id': 4, 'nombre': 'Camiseta Manchester United', 'precio': 65, 'imagen': 'https://static.wixstatic.com/media/ca2cbe_19bb0892c9da4ebd8882a8af7d6d2ee3~mv2.jpg/v1/fill/w_516,h_689,al_c,q_80,enc_avif,quality_auto/ca2cbe_19bb0892c9da4ebd8882a8af7d6d2ee3~mv2.jpg', 'descripcion': 'Camiseta oficial del Manchester United, con el diseño clásico rojo que representa la pasión y la energía del club.', 'tallas': ['S', 'M', 'L', 'XL']},
    {'id': 5, 'nombre': 'Camiseta Bayern Múnich', 'precio': 70, 'imagen': 'https://static.wixstatic.com/media/ca2cbe_44a534ecc09743b7adb516cb76d1b314~mv2.jpg/v1/fill/w_509,h_679,al_c,lg_1,q_80,enc_avif,quality_auto/ca2cbe_44a534ecc09743b7adb516cb76d1b314~mv2.jpg', 'descripcion': 'Camiseta oficial del Bayern Múnich, con el diseño tradicional en rojo que caracteriza a los campeones alemanes.', 'tallas': ['M', 'L', 'XL']},
    {'id': 6, 'nombre': 'Camiseta PSG', 'precio': 75, 'imagen': 'https://static.wixstatic.com/media/ca2cbe_1d6bb8f6587b4a09af3295c10bdc15d9~mv2.jpg/v1/fill/w_487,h_650,al_c,lg_1,q_80,enc_avif,quality_auto/ca2cbe_1d6bb8f6587b4a09af3295c10bdc15d9~mv2.jpg', 'descripcion': 'Camiseta oficial del PSG, con un diseño moderno y elegante que resalta el estilo del club de la capital francesa.', 'tallas': ['S', 'M', 'L', 'XL']},
    {'id': 7, 'nombre': 'Camiseta Liverpool', 'precio': 80, 'imagen': 'https://static.wixstatic.com/media/ca2cbe_a8b751e9d1b246388e339668fefa5409~mv2.jpg/v1/fill/w_516,h_689,al_c,q_80,enc_avif,quality_auto/ca2cbe_a8b751e9d1b246388e339668fefa5409~mv2.jpg', 'descripcion': 'Camiseta oficial del Liverpool FC, con el característico color rojo que representa la historia y la pasión de este club.', 'tallas': ['M', 'L', 'XL']},
    {'id': 8, 'nombre': 'Camiseta Chelsea', 'precio': 85, 'imagen': 'https://static.wixstatic.com/media/ca2cbe_4c1ac6de102e4fd187a81e4a81cbb9ed~mv2.jpg/v1/fill/w_516,h_689,al_c,q_80,enc_avif,quality_auto/ca2cbe_4c1ac6de102e4fd187a81e4a81cbb9ed~mv2.jpg', 'descripcion': 'Camiseta oficial del Chelsea FC, ideal para mostrar tu apoyo a uno de los clubes más grandes de la Premier League.', 'tallas': ['S', 'M', 'L', 'XL']},
    {'id': 9, 'nombre': 'Camiseta Arsenal', 'precio': 90, 'imagen': 'https://static.wixstatic.com/media/ca2cbe_efb22497d19140819f94ee6c8a2ff61d~mv2.jpg/v1/fill/w_516,h_689,al_c,q_80,enc_avif,quality_auto/ca2cbe_efb22497d19140819f94ee6c8a2ff61d~mv2.jpg', 'descripcion': 'Camiseta oficial del Arsenal FC, con un diseño rojo y blanco que resalta la historia de uno de los clubes más grandes de Londres.', 'tallas': ['S', 'M', 'L']},
    {'id': 10, 'nombre': 'Camiseta AC Milan', 'precio': 95, 'imagen': 'https://static.wixstatic.com/media/ca2cbe_c356f4a3a15140609a567ff0fe0606ff~mv2.jpg/v1/fill/w_625,h_625,al_c,lg_1,q_85,enc_avif,quality_auto/ca2cbe_c356f4a3a15140609a567ff0fe0606ff~mv2.jpg', 'descripcion': 'Camiseta oficial del AC Milan, un homenaje al club italiano con un diseño en rojo y negro que destaca su historia y éxito.', 'tallas': ['S', 'M', 'L', 'XL']}
]

@app.route('/')
def index():
    return render_template('index.html', productos=productos)

@app.route('/add_to_cart/<int:producto_id>')
def add_to_cart(producto_id):
    producto = next((p for p in productos if p['id'] == producto_id), None)
    
    if not producto:
        return redirect(url_for('index'))
    
    if 'cart' not in session:
        session['cart'] = []
    
    product_in_cart = next((item for item in session['cart'] if item['id'] == producto_id), None)
    
    if product_in_cart:
        product_in_cart['cantidad'] += 1
    else:
        producto['cantidad'] = 1
        session['cart'].append(producto)
    
    session.modified = True
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total = sum(item['precio'] * item['cantidad'] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/remove_from_cart/<int:producto_id>')
def remove_from_cart(producto_id):
    cart_items = session.get('cart', [])
    session['cart'] = [item for item in cart_items if item['id'] != producto_id]
    session.modified = True
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['POST'])
def checkout():
    cart_items = session.get('cart', [])
    
    if not cart_items:
        return redirect(url_for('cart'))
    
    items = []
    for item in cart_items:
        items.append({
            "title": item['nombre'],
            "quantity": item['cantidad'],
            "unit_price": float(item['precio']),
            "currency_id": "ARS"
        })
    
    # Configuración de ngrok
    ngrok_url = "https://1d58-2803-a3e0-1732-41a0-38eb-8fd2-aa43-53e6.ngrok-free.app"
    
    preference_data = {
        "items": items,
        "back_urls": {
            "success": f"{ngrok_url}/payment_success",
            "failure": f"{ngrok_url}/payment_failure",
            "pending": f"{ngrok_url}/payment_pending"
        },
        "auto_return": "approved"
    }
    
    preference_response = sdk.preference().create(preference_data)
    
    if "response" not in preference_response:
        return redirect(url_for('payment_failure'))
    
    init_point = preference_response["response"].get("init_point")
    if not init_point:
        return redirect(url_for('payment_failure'))
    
    return redirect(init_point)

@app.route('/payment_success')
def payment_success():
    session.pop('cart', None)
    return render_template('payment_success.html')

@app.route('/payment_failure')
def payment_failure():
    return render_template('payment_failure.html')

@app.route('/payment_pending')
def payment_pending():
    return render_template('payment_pending.html')

@app.route('/payment_status/<payment_id>')
def payment_status(payment_id):
    payment = sdk.payment().get(payment_id)
    payment_info = payment["response"]
    return render_template('payment_status.html', payment_info=payment_info)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
