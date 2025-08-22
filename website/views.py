from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint("views", __name__)

# Homepage route to add new note or update existing one
@views.route("/", methods=["GET", "POST"])
@login_required
def homepage():
    if request.method == 'POST':
        note_id = request.form.get('note_id')
        title = request.form.get('title')
        description = request.form.get('description')

        if not title:
            flash('Add title to note', category='error')
        elif not description:
            flash('Add description to note', category='error')
        else:
            if note_id:
                # Update existing note
                note = Note.query.get(note_id)
                if note and note.user_id == current_user.id:
                    note.title = title
                    note.description = description
                    flash('Note updated successfully!', category='success')
            else:
                # Create new note
                new_note = Note(title=title, description=description, user_id=current_user.id)
                db.session.add(new_note)
                flash('Note added successfully!', category='success')

            db.session.commit()
            return redirect(url_for('views.homepage'))

    return render_template('index.html', user=current_user)

# Route to delete a note
@views.route("/delete-note", methods=["POST"])
def delete_note():
    note = json.loads(request.data)
    note_id = note["noteId"]
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()  # Commit the deletion
            flash("Deleted Note", category="success")
    return jsonify({})

# Route to update a note
@views.route('/update-note', methods=['PUT'])
def update_note():
    note_data = json.loads(request.data)
    note_id = note_data['noteId']
    new_title = note_data['title']
    new_description = note_data['description']
    
    if note_id:
        note = Note.query.get(note_id)
        if note and note.user_id == current_user.id:
            note.title = new_title
            note.description = new_description
            db.session.commit()  # Commit the updated note to the database
            flash("Note updated successfully!", category="success")
    
    return jsonify({})