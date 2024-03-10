document.addEventListener('DOMContentLoaded', function() {
    // Get the modal
    let modal = document.getElementById("capsuleFormModal");

    // Get the button that opens the modal
    let btn = document.querySelector("button[data-target='#capsuleFormModal']");

    // Get the <span> element that closes the modal
    let span = document.getElementsByClassName("close")[0];

    // When the user clicks the button, open the modal
    if(btn != null) { // Check if the button was found
        btn.onclick = function() {
            modal.style.display = "flex";
        }
    }

    // When the user clicks on <span> (x), close the modal
    if(span != null) { // Check if the span was found
        span.onclick = function() {
            modal.style.display = "none";
        }
    }
});
