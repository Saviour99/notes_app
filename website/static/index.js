const addBox = document.querySelector(".add-note"),
      popupBox = document.querySelector(".popup-box"),
      closeBox = popupBox.querySelector("header i"),
      titleTag = popupBox.querySelector("input"),
      descTag = popupBox.querySelector("textarea"),
      addBtn = popupBox.querySelector("button"),
      mainTag = popupBox.querySelector("header p");

addBox.addEventListener("click", () => {
    titleTag.focus();
    popupBox.classList.add("show");
});

closeBox.addEventListener("click", () => {
    titleTag.value = "";
    descTag.value = "";
    mainTag.innerText = "Add New Note";  // Reset form text
    addBtn.innerText = "Add Note";  // Reset button text
    popupBox.classList.remove("show");
});

function showMenu(elem) {
    elem.parentElement.classList.add("show");
    document.addEventListener("click", e => {
        if (e.target.tagName != "I" || e.target != elem){
            elem.parentElement.classList.remove("show");
        }
    });
}

function updateNoteFromData(element) {
    const noteId = element.getAttribute('data-param1');
    const title = element.getAttribute('data-param2');
    const description = element.getAttribute('data-param3');
    
    // Set the form fields with current note data
    titleTag.value = title;
    descTag.value = description;
    mainTag.innerText = "Update Note"; // Change header text to Update
    addBtn.innerText = "Update Note"; // Change button text to Update

    // Open the popup box
    popupBox.classList.add("show");
    
    // Update the note when the form is submitted
    addBtn.addEventListener("click", () => {
        updateNote(noteId, titleTag.value, descTag.value);
    });
}

function updateNote(noteId, newTitle, newDescription){
    fetch('/update-note', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ noteId: noteId, title: newTitle, description: newDescription }),
    }).then((_res) => {
        // Update the note on the page without reloading
        document.getElementById(`note-title-${noteId}`).innerText = newTitle;
        document.getElementById(`note-description-${noteId}`).innerText = newDescription;
        
        // Close the popup and clear inputs
        popupBox.classList.remove("show");
        titleTag.value = "";
        descTag.value = "";
    });
}

function deleteNote(noteId) {
    if (confirm('Are you sure you want to delete this note?')) {
        fetch('/delete-note', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ noteId: noteId }),
        }).then((_res) => {
            window.location.href = '/';
        });
    }
}