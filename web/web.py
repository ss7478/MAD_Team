import asyncio
from flask import Flask, render_template, request, jsonify
import json
import websockets
import time
import threading

from random import randint

app = Flask(__name__) 

colors = ["red", "green", "blue", "yellow"]

squares = []

flagz = [False, False, False, False]

@app.route("/") 
def index(): 
    return render_template('mainpage.html') 
 
@app.route('/buttons_handle', methods=['POST']) 
def buttons_handle(): 
    button_pressed = request.json['button'] 
    response_message = ''
    if button_pressed == 'start': 
        print('start') 
        flagz[0] = True

        response_message = 'start button pressed'
    elif button_pressed == 'stop': 
        print('stop') 
        flagz[1] = True
        response_message = 'stop button pressed'
    elif button_pressed == 'kill': 
        print('kill') 
        flagz[2] = True
        
        response_message = 'kill button pressed'
    elif button_pressed == 'pause': 
        print('pause') 
        flagz[3] = not flagz[3]
        response_message = 'pause button pressed'
    return jsonify({'message': response_message}) 
 

async def ws_handler(websocket):
    while True:
        await websocket.send(json.dumps(squares))
        await asyncio.sleep(1) 

async def start_websocket_server():
    server = await websockets.serve(ws_handler, "localhost", 8765)
    await server.wait_closed() 

def run_flask():
    app.run(port=5000) 
    
