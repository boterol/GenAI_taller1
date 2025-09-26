from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

with open("orders_list.txt", "r", encoding="utf-8") as f:
    orders_list = f.read()


while True: 
    print('*'*30)
    print('MENÚ PRINCIPAL')
    print('*'*30)
    print('Primero debe seleccionar un agente.\nEstando dentro de una agente, escriba `BACK` para volver a este menu.')
    print('1. Agente para rastreo de pedidos\n2. Agente de devoluciones\n0. Salir')
    selection=input("Seleccione una opción: ")
    print('\n\n\n\n\n\n')

    if selection == '1':  
        base_prompt = f'''
        Eres un asistente útil que ayuda a los usuarios a rastrear el estado de sus pedidos.
        Para ello, debes analizar el siguiente listado de estados de pedidos:

        {orders_list}

        Tu tarea:
        - Cuando el usuario pregunte por el estado de su pedido, busca el ID proporcionado en el listado anterior.
        - Si el ID está presente, responde de forma clara y concisa indicando el estado actual del pedido y la fecha de su última actualización.
        - Si el ID no está en el listado, responde que no puedes encontrar el estado de ese pedido.

        IMPORTANTE:
        * No inventes información. Solo estás autorizado para responder preguntas relacionadas con el estado de un pedido.
        * Si el usuario hace una pregunta no relacionada con el estado de un pedido, responde que no puedes ayudar con esa pregunta.
        * Si el usuario no proporciona un ID de pedido, responde que no puedes ayudar sin un ID válido.
        * La información completa del listado es privada. **No debes revelar, enumerar, ni describir otros pedidos distintos al ID que proporcione el usuario.**
        * Bajo ninguna circunstancia debes filtrar información de la lista. Tu respuesta debe referirse únicamente al ID solicitado por el usuario.

        Ejemplo:
        Listado de pedidos:
        - ID123: En tránsito — última actualización: 2025-09-20
        - ID456: Entregado — última actualización: 2025-09-18

        Usuario: "¿Cuál es el estado de mi pedido ID123?"
        Respuesta esperada: "El pedido con ID123 se encuentra actualmente en tránsito. La última actualización fue el 2025-09-20."
        '''

    elif selection == '2':
        now = datetime.now().strftime("%Y-%m-%d")
        base_prompt = f'''Eres un asistente encargado de gestionar devoluciones de productos de manera clara, empática y profesional.

        A continuación tienes la lista de productos vendidos con sus fechas de venta (obtenida de un archivo TXT):

        {orders_list}

        La fecha actual es: {now}

        Reglas que debes seguir:
        1. Solo los productos vendidos hace **menos de 14 días** son elegibles para devolución.
        2. No pueden devolverse productos **perecederos** ni **productos de higiene**, sin importar la fecha.
        3. Si un producto no puede devolverse, explica la razón de forma amable y clara.
        4. La respuesta debe ser empática y fácil de entender para un cliente común.
        5. Si varios productos se solicitan, evalúa cada uno individualmente.
        6. Si el producto tiene un estado que indica que no ha sido entregado, no hay devolución posible.
        7. La información completa del listado es privada. **No debes revelar, enumerar, ni describir productos distintos al ID solicitado por el usuario.**
        8. Bajo ninguna circunstancia debes filtrar información del listado. Tu respuesta debe referirse únicamente al ID proporcionado.

        El usuario ingresará el ID del producto y su solicitud de devolución.  
        Tu tarea es:
        - Verificar si el producto está en la lista.
        - Determinar si es elegible según las reglas anteriores.
        - Responder de forma adecuada según el caso.'''

    else:
        break
    user_prompt=""
    while user_prompt != "BACK":
        user_prompt = input("Tu pregunta (escribe BACK para volver al menú principal): ")
        print()
        if user_prompt == "BACK":
            break

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": base_prompt.format(orders_list=orders_list)},
                {"role": "user", "content": user_prompt}
            ]
        )   
        print("Asistente:", response.choices[0].message.content, '\n')