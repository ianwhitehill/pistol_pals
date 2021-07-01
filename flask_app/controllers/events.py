from types import resolve_bases
from flask.helpers import flash
from flask_app import app
from flask import render_template, redirect, session, request

from flask_app.models.event import Event

@app.route('/events')
def show_events():
    if not 'user_id' in session:
        flash('you most be loged in to view events')
        return redirect('/')
    else:
        events = Event.select_all()
        return render_template('events.html', events = events, user_name=session['user_name'])

@app.route('/create_event')
def create_event_form():
    if not 'user_id' in session:
        flash('you most be loged in to create events')
        return redirect('/')
    else:
        return render_template('create_event.html', user_name=session['user_name'])

@app.route('/insert_event', methods=['POST'])
def insert_event():
    if Event.validation(request.form):
        data = {
            'name' : request.form['name'],
            'description' : request.form['description'],
            'start_time' : request.form['start_time']
        }
        Event.insert(data)
        return redirect('/events')
    else:
        return redirect('/create_event')

@app.route('/edit/<int:event_id>')
def edit_form(event_id):
    data = {
        'id' : event_id
    }
    event = Event.select_by_id(data)
    if event == False:
        return redirect('/events')

    return render_template("edit_event.html", event = event)

@app.route('/update_event/<int:event_id>', methods=['POST'])
def update_event(event_id):
    if Event.validation(request.form):
        data = {
            'name' : request.form['name'],
            'description' : request.form['description'],
            'start_time' : request.form['start_time'],
            'id' : event_id
        }
        Event.update(data)
        return redirect('/events')
    else:
        return redirect(f'/edit/{event_id}')

@app.route('/delete/<int:event_id>')
def remove(event_id):
    data = {
        'id' : event_id
    }
    Event.delete(data)
    return redirect('/events')