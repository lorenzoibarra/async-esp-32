from microdot import Microdot, send_file
from machine import Pin

pins = {
    12: Pin(12, Pin.OUT)
}

boton = Pin(27, Pin.IN, Pin.PULL_UP)

for pin in pins.values():
    pin.value(0)

app = Microdot()

def estado_pin(gpio):
    return "checked" if pins[gpio].value() else ""

def armar_botones():
    botones = ""
    for gpio in pins:
        html = f"""
            <h4>Salida - GPIO {gpio}</h4>
            <label class="switch">
                <input type="checkbox" onchange="toggleCheckbox(this)" id="{gpio}" {estado_pin(gpio)}>
                <span class="slider"></span>
            </label>
        """
        botones += html
    return botones

def mainpage():
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>LED Asincrono</title>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
        <h1>ESP Web Server</h1>

        <!-- Declaracion de los LEDs -->
        {armar_botones()}
        <h4>Boton - GPIO 27</h4>
        <div id="indicador" class="indicador activo"></div>
        <script src="script.js"></script>
    </body>
    </html>
"""

@app.route("/")
async def index(request):
    print('Pagina principal')
    return mainpage(), 200, {"Content-Type": "text/html"}

@app.route("/style.css")
async def css(request):
    return send_file("style.css")

@app.route("/script.js")
async def js(request):
    return send_file("script.js")

@app.route("/update")
async def update(request):
    gpio_param = request.args.get("output")
    state_param = request.args.get("state")

    if gpio_param is not None and state_param is not None:
        gpio = int(gpio_param)
        state = int(state_param)
        if gpio in pins:
            pins[gpio].value(state)
        print (f"GPIO:{gpio} - Estado:{state}")
    else:
        print("No se encontraron los parametros")

    return "OK", 200, {"Content-Type": "text/plain"}

@app.route("/input")
async def input_state(request):
    estado = "1" if boton.value() == 0 else "0"
    return estado, 200, {"Content-Type": "text/plain", "Cache-Control": 'no-store'}

app.run(port=80)