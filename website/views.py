from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

# Homepage route to add new note or update existing one
@views.route('/', methods=["GET", "POST"])
@login_required
def homepage():
    if request.method == 'POST':
        title = request.form.get("title")
        description = request.form.get("description")
        
        if len(title) < 1:
            flash("Add title to note", category="error")
        elif len(description) < 1:
            flash("Add description to note", category="error")
        else:
            new_note = Note(title=title, description=description, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()  # Commit the new note to the database
            flash("Note added successfully!", category="success")

    return render_template("index.html", user=current_user)

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
    
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            note.title = new_title
            note.description = new_description
            db.session.commit()  # Commit the updated note to the database
            flash("Note updated successfully!", category="success")
    
    return jsonify({})