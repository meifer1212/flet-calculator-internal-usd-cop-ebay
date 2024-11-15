import flet as ft
import locale
import math
import requests  # Import requests to get the exchange rate

locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')


# Function to fetch the current exchange rate
def fetch_dollar_rate(page):
    dollar_rate = 4300
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = response.json()
        # Fetch the exchange rate for COP (Colombian Peso)
        dollar_rate = data["rates"]["COP"]
    except Exception as e:
        print(f"Error fetching exchange rate: {e}")
        page.add(ft.Toast(f"Error al obtener el precio del dólar. Usando valor predeterminado."))
    return dollar_rate


def nomain(page: ft.Page):
    # Set the page title and layout
    page.title = "Calculadora de Producto con Impuestos"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Fetch the current dollar rate from the API
    default_dollar_rate = fetch_dollar_rate(page)
    page.update()

    # Function to calculate the total price (COP)
    def calcular_total(e):
        try:
            precio_dolar = float(dolar_input.value)
            costo_producto = float(costo_input.value)
            porcentaje_impuesto = float(impuesto_input.value) / 100

            # Calculate total with tax
            impuestos = costo_producto * porcentaje_impuesto
            total = (costo_producto + impuestos) * precio_dolar
            total_rounded = math.ceil(total)

            total_input.value = total_rounded

            # Display information text
            information.value = (
                f"Impuesto: {locale.format_string('%d', math.ceil(impuestos), grouping=True)} | "
                f"Costo: {locale.format_string('%d', math.ceil(costo_producto), grouping=True)} | "
                f"Precio Dolar: {locale.format_string('%d', math.ceil(precio_dolar), grouping=True)} | "
                f"Total: {locale.format_string('%d', total_rounded, grouping=True)} COP"
            )

        except ValueError:
            total_input.value = "0"
            information.value = "Impuesto: 0 | Costo: 0 | Precio Dolar: 0 | Total: 0 COP"
        page.update()

    # Function to calculate the product cost from the total price (inversely)
    def calcular_costo(e):
        try:
            precio_dolar = float(dolar_input.value)
            total_value = float(total_input.value)
            porcentaje_impuesto = float(impuesto_input.value) / 100

            # Reverse calculation for the cost
            costo_producto_inverso = total_value / (precio_dolar * (1 + porcentaje_impuesto))
            costo_producto_inverso_rounded = math.ceil(costo_producto_inverso)

            costo_input.value = costo_producto_inverso_rounded

            # Display the updated information
            dolares_value_inverso = costo_producto_inverso_rounded * (1 + porcentaje_impuesto)
            dolares_rounded_inverso = math.ceil(dolares_value_inverso)

            information.value = (
                f"Impuesto: {locale.format_string('%d', math.ceil(costo_producto_inverso_rounded * porcentaje_impuesto), grouping=True)} | "
                f"Costo: {locale.format_string('%d', costo_producto_inverso_rounded, grouping=True)} | "
                f"Precio Dolar: {locale.format_string('%d', math.ceil(precio_dolar), grouping=True)} | "
                f"Total: {locale.format_string('%d', dolares_rounded_inverso * precio_dolar, grouping=True)} COP"
            )

        except ValueError:
            costo_input.value = "0"
            information.value = "Impuesto: 0 | Costo: 0 | Precio Dolar: 0 | Total: 0 COP"
        page.update()

    # Create the input fields for dolar, cost, total, and tax percentage
    dolar_input = ft.TextField(label="Precio del dólar hoy", width=250, keyboard_type="number",
                               on_change=calcular_total, prefix_text="COP$ ")

    # Set initial values for the inputs
    dolar_input.value = str(default_dollar_rate)  # Set the default dollar rate dynamically

    costo_input = ft.TextField(label="Costo del producto", width=250, keyboard_type="number", on_change=calcular_total,
                               prefix_text="USD$ ")

    total_input = ft.TextField(label="Total", width=250, keyboard_type="number", on_change=calcular_costo,
                               prefix_text="COP$ ")

    impuesto_input = ft.TextField(label="TAX %", value="7", width=250, keyboard_type="number", on_change=calcular_total,
                                  prefix_text="% ")

    # Information text to show details like tax, cost, dollar rate, and total
    information = ft.Text(value="Impuesto: 0 | Costo: 0 | Precio Dolar: 0 | Total: 0 COP", size=14, color="gray")

    # Add the elements to the page layout
    page.add(
        ft.Column(
            [
                ft.Row([ft.Text("Calculadora de Producto con Impuestos", size=20, color="blue")], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                ft.Row([costo_input], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                ft.Row([dolar_input, impuesto_input], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                ft.Row([total_input], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                ft.Row([information], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )
    )


# Run the Flet app
ft.app(target=nomain)
