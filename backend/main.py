from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging
import db_helper
import generic_helper

app = FastAPI()

inprogress_orders = {}
# Setup logging
logging.basicConfig(level=logging.INFO)

@app.get("/")
def home():
    return {"status": "Server is running!"}

@app.post("/")
async def handle_request(request: Request):
    try:
        logging.info("Webhook request received.")

        # Read raw body
        raw_body = await request.body()
        if not raw_body:
            raise ValueError("Empty request body received.")

        # Attempt to parse JSON
        payload = await request.json()
        # logging.info(f"Payload received: {payload}")

        query_result = payload.get('queryResult', {})
        intent = query_result.get('intent', {}).get('displayName', '')
        parameters = query_result.get('parameters', {})
        output_contexts = query_result.get('outputContexts', [])
        session_id = generic_helper.extract_session_id(output_contexts[0]['name'])

        intent_handler_dict = {
            'order.add': add_to_order,
            'order.remove': remove_from_order,
            'order.complete': complete_order,
            'track.order-ongoing': track_order
        }

        return intent_handler_dict[intent](parameters, session_id)


    except Exception as e:
        logging.error(f"Exception occurred: {e}")
        return JSONResponse(
            content={"fulfillmentText": f"Webhook error: {str(e)}"},
            status_code=500
        )

def complete_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        return "I am having trouble finding your order. Sorry! Can you please place a new order."

    order = inprogress_orders[session_id]
    order_id = save_to_db(order)

    if order_id == -1:
        fulfillment_text = (
            "Sorry, I couldn't process your order due to a backend error. "
            "Please place a new order again."
        )
    else:
        order_total = db_helper.get_total_order_price(order_id)
        fulfillment_text = (
            f"Awesome. We have placed your order. "
            f"Here is your order id #{order_id}. "
            f"Your order total is {order_total} which you can pay at the time of delivery!"
        )

    # Remove the order from in-progress regardless of success/failure
    del inprogress_orders[session_id]

    return JSONResponse(content={"fulfillmentText": fulfillment_text})

def save_to_db(order: dict):
    next_order_id = db_helper.get_next_order_id()
    for food_items, quantity in order.items():
        rcode = db_helper.insert_order_items(
            food_items,
            quantity,
            next_order_id
        )
        if rcode == -1:
            return -1

    db_helper.insert_order_tracking(next_order_id, "in progress")

    return next_order_id

def add_to_order(parameters: dict, session_id: str):

    food_items = parameters.get('food-item')
    quantities = parameters.get('number')

    if len(food_items) != len(quantities):
        fulfillment_text = "Sorry I didn't understand. Can you please specify food items and quantities clearly?"
    else:
        new_food_dict = dict(zip(food_items, quantities))

        if session_id in inprogress_orders:
            current_order_dict = inprogress_orders[session_id]

            # Merge dictionaries by updating quantities
            for item, qty in new_food_dict.items():
                if item in current_order_dict:
                    current_order_dict[item] += qty
                else:
                    current_order_dict[item] = qty

            inprogress_orders[session_id] = current_order_dict
        else:
            inprogress_orders[session_id] = new_food_dict

        # print("*****************")
        # print(inprogress_orders)

        order_str = generic_helper.get_str_from_food_dict(inprogress_orders[session_id])
        fulfillment_text = f"So far you have: {order_str}. Do you need anything else?"

    return JSONResponse(content={"fulfillmentText": fulfillment_text})


def track_order(parameters: dict, session_id: str):
    order_id = int(parameters.get('number'))

    if not order_id:
        return JSONResponse(content={"fulfillmentText": "No order ID provided."})

    # Fetch from DB
    try:
        order_status = db_helper.get_order_status(order_id)
    except Exception as db_err:
        logging.error(f"Database error: {db_err}")
        return JSONResponse(content={"fulfillmentText": "Database error occurred."})

    if order_status:
        fulfillment_text = f"The order status for order ID {order_id} is: {order_status}"
    else:
        fulfillment_text = f"No order found with order ID {order_id}."

    return JSONResponse(content={"fulfillmentText": fulfillment_text})


def remove_from_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        return JSONResponse(content={
            "fulfillmentText": "I'm having a trouble finding your order. Sorry! Can you place a new order please?"
        })

    food_items = parameters["food-item"]
    current_order = inprogress_orders[session_id]

    removed_items = []
    no_such_items = []

    for item in food_items:
        if item not in current_order:
            no_such_items.append(item)
        else:
            removed_items.append(item)
            del current_order[item]

    if len(removed_items) > 0:
        fulfillment_text = f'Removed {",".join(removed_items)} from your order!'

    if len(no_such_items) > 0:
        fulfillment_text = f' Your current order does not have {",".join(no_such_items)}'

    if len(current_order.keys()) == 0:
        fulfillment_text += " Your order is empty!"
    else:
        order_str = generic_helper.get_str_from_food_dict(current_order)
        fulfillment_text += f" Here is what is left in your order: {order_str}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })