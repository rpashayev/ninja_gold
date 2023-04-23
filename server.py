from flask import Flask, render_template, redirect, request, session
from random import randint
from datetime import datetime

app = Flask(__name__)
app.secret_key = '123456'

@app.route('/')
def start():
    if 'total_gold' not in session:
        session['total_gold'] = 0
        session['ninja_movements'] = 0
        session['log'] = f'Welcome to the Game! {datetime.now()}'
    return render_template('game.html')

@app.route('/process', methods=['POST'])
def process_gold():
    activity = randomize()
    session['total_gold'] += activity['value']
    session['ninja_movements'] += 1
    session['log'] = activity['log'] + session['log']
    session['color'] = activity['color']
    return redirect('/')

@app.route('/reset', methods=['POST'])
def reset():
    session.clear()
    return redirect('/')

def randomize():
    gain = 'earned'
    color = 'text-success'
    min = -50
    max = 50
    if request.form['property'] == 'farm':
        min = 10
        max = 20
    elif request.form['property'] == 'cave':
        min = 5
        max = 10
    elif request.form['property'] == 'house':
        min = 2
        max = 5
        
    value = randint(min, max)
    if value < 0:
        gain = 'lost'
        color = 'text-danger'
    log_text = f'<p class="mb-0 {color}">Dojo entered {request.form["property"].title()} and {gain} {value} golds @ {datetime.now()} </p>'
    activity = {
        'value': value,
        'log': log_text,
        'color': color
    }
    return activity

if __name__ == '__main__':
    app.run(debug = True)
    