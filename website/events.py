from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login.utils import login_required, current_user
from werkzeug.utils import secure_filename
from . import db
from datetime import date, datetime
import os
from werkzeug.utils import secure_filename
from .forms import CommentForm, EventForm, BookingForm, EventEditForm
from .models import Event, Comment, Booking


bp = Blueprint('event', __name__, url_prefix='/events')


EVENT_GENRES = ["Country", "Electronic", "Funk",
                "Hip Hop", "Jazz", "House", "Pop", "Rap", "Rock"]


@bp.route('/<int:id>')
def show(id):
    event = Event.query.filter_by(id=id).first()
    # create the comment form
    comment_form = CommentForm()
    booking_form = BookingForm()
    # # error handling
    if event is None:
        flash(f"Cound not find a event!", "warning")
        return redirect(url_for("main.index"))

    # return render_template('events/show.html', event=event, form=comment_form, id=id)
    return render_template('events/show.html', comment_form=comment_form, booking_form=booking_form, 
        event=event, id=id, display_edit_button = login_user_is_creator(current_user, event.created_by))


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    event_form = EventForm()
    if event_form.validate_on_submit():
        event = Event(
            event_name=event_form.event_name.data,
            artist_name=event_form.artist_name.data,
            status=event_form.status.data,
            genre=event_form.genre.data,
            date=event_form.date.data,
            time=event_form.time.data,
            location=event_form.location.data,
            description=event_form.description.data,
            image=check_event_img_file(event_form),
            price=event_form.price.data,
            num_tickets=event_form.num_tickers.data,
            created_by=current_user.id
        )
        if event.num_tickets == 0:
            event.status = "Booked"
        # add the object to the db session
        db.session.add(event)
        # commit to the database
        db.session.commit()

        flash(f'Successfully created new event', 'success')

        return redirect(url_for('event.show', id=event.id))
    return render_template('events/create.html', form=event_form)


@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    event = Event.query.filter_by(id=id).first()
    if login_user_is_creator(current_user, event.created_by) == False:
        flash(f'You must be the creator of the event to edit the details!', 'warning')
        return redirect(url_for('event.show', id=event.id))
    
    event_edit_form = EventEditForm()
    if event_edit_form.validate_on_submit():
        if event_edit_form.event_name.data != "":
            event.event_name = event_edit_form.event_name.data
        if event_edit_form.artist_name.data != "":
            event.artist_name = event_edit_form.artist_name.data
        if event_edit_form.status.data != "":
            event.status = event_edit_form.status.data
        if event_edit_form.genre.data != "":
            event.genre = event_edit_form.genre.data
        if event_edit_form.date.data != "":
            event.date = event_edit_form.date.data
        if event_edit_form.time.data != "":
            event.time = event_edit_form.time.data
        if event_edit_form.location.data != "":
            event.location = event_edit_form.location.data
        if event_edit_form.description.data != "":
            event.description = event_edit_form.description.data
        if event_edit_form.image.data is not None:
            event.image = check_event_img_file(event_edit_form)
        if event_edit_form.price.data is not None:
            event.price = event_edit_form.price.data
        if event_edit_form.num_tickers.data is not None :
            event.num_tickets = event_edit_form.num_tickers.data
            if event.num_tickets == 0:
                event.status = "Booked"
            else:
                event.status = "Active"

        db.session.commit()

        flash(f'Successfully updated event details', 'success')

        return redirect(url_for('event.show', id=event.id))
    return render_template('events/edit.html', form=event_edit_form)


@bp.route("/<int:id>/delete")
@login_required
def delete(id):
    event = Event.query.filter_by(id=id).first()
    if login_user_is_creator(current_user, event.created_by) == False:
        flash(f'You must be the creator of the event to delete the event!', 'warning')
        return redirect(url_for('event.show', id=event.id))
    Event.query.filter_by(id=id).delete()
    db.session.commit()
    flash(f'Successfully deleted event', 'success')
    return redirect(url_for('main.index'))
  

@bp.route('/<int:id>/comment', methods=['GET', 'POST'])
@login_required
def comment(id):
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = Comment(text = comment_form.text.data,
                          # change user id after login function is implemented - Marco
                          user_id = current_user.id,
                          event_id = id,
                          posted_at = datetime.now())

        db.session.add(comment)
        db.session.commit()

        flash(f"Comments successfully posted", "success")
    return redirect(url_for("event.show", id=id))


@bp.route('/<int:id>/booking', methods=['GET', 'POST'])
@login_required
def booking(id):
    event = Event.query.filter_by(id=id).first()
    booking_form = BookingForm()
    if (booking_form.validate_on_submit() == True):
        ticket_order = booking_form.num_tickets.data

        if (ticket_order > event.num_tickets):
            flash(f"Too many tickets booked", "error")
            return redirect(url_for('event.show', id=id))
            
        new_num_tickets = event.num_tickets - ticket_order
        event.num_tickets = new_num_tickets
        
        if new_num_tickets == 0:
            event.status = "Booked"

        booking = Booking(
            num_tickets = ticket_order,
            user_id = current_user.id,
            event_id = id)

        db.session.add(booking)
        db.session.commit()

        flash(f'{booking.num_tickets} tickets has been booked! Booking ID: {booking.id}', 'success')
        
    if (booking_form.validate_on_submit() == False):
        flash(f"Invalid amount of tickets", "error")
        return redirect(url_for('event.show', id=id))

    return redirect(url_for('event.show', id=id))


def check_event_img_file(form):
    fp = form.image.data
    filename = fp.filename
    BASE_PATH = os.path.dirname(__file__)
    EVENT_IMG_PATH = "static/img/events/"
    upload_path = os.path.join(
        BASE_PATH, EVENT_IMG_PATH, secure_filename(filename))
    db_upload_path = EVENT_IMG_PATH + secure_filename(filename)
    fp.save(upload_path)
    return db_upload_path


def login_user_is_creator(login_user, creator_id):
    try:
        return login_user.id == creator_id
    except:
        return False
    
