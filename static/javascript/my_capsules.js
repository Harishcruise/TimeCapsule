document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.form-input').forEach(input => {
        const blockId = input.parentElement.id;
        const label = input.previousElementSibling;

        input.addEventListener('focus', () => {
            document.getElementById(blockId).classList.add('active');
            label.classList.add('active');
        });

        input.addEventListener('blur', () => {
            if (!input.value) {
                document.getElementById(blockId).classList.remove('active');
                label.classList.remove('active');
            }
        });
    });

    let today = new Date();
    let dd = String(today.getDate()).padStart(2, '0');
    let mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    let yyyy = today.getFullYear();

    const minDate = `${yyyy}-${mm}-${dd}T00:00`; // Template literal for clarity
    const dateInput = document.getElementById('id_unsealing_date');

    if (dateInput) {
        dateInput.setAttribute("min", minDate);
    }

    let modal = document.getElementById("capsuleFormModal"); // Get the modal
    let btn = document.querySelector("button[data-target='#capsuleFormModal']");  // Get the button that opens the modal
    let span = document.getElementsByClassName("close")[0];  // Get the <span> element that closes the modal
    function resetFormFields() {
        document.getElementById('id_name').value = '';
        document.getElementById('nameBlock').classList.remove('active');
        document.getElementById('nameLabel').classList.remove('active');

        document.getElementById('id_description').value = '';
        document.getElementById('descriptionBlock').classList.remove('active');
        document.getElementById('descriptionLabel').classList.remove('active');

        document.getElementById('id_unsealing_date').value = ''; // Set to today's date or leave blank
        document.getElementById('unsealing_dateBlock').classList.remove('active');
        document.getElementById('unsealing_dateLabel').classList.remove('active');

        document.getElementById('id_is_public').value = 'False';

        document.getElementById('id_status').value = 'False';

        // Change the button text to "Update"
        document.getElementById('form-button').textContent = 'Submit'; //
    }
    // When the user clicks the button, open the modal
    if(btn != null) { // Check if the button was found
        btn.onclick = function() {
            resetFormFields();
            modal.style.display = "flex";
        }
    }
    // When the user clicks on <span> (x), close the modal
    if(span != null) { // Check if the span was found
        span.onclick = function() {
            modal.style.display = "none";
        }
    }

    // Drag and Drop functionality
    const form = document.getElementById('capsuleForm');
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('capsule_contents');
    const fileListContainer = document.querySelector('.uploaded-capsule-content-section');
    let selectedFiles = []; // To keep track of the selected files

    // Function to update the displayed file list
    function updateFileListDisplay() {
        fileListContainer.innerHTML = ''; // Clear current list
        if (selectedFiles.length < 0) {
            // Reset styles if no files are selected
            fileListContainer.style.background = 'none';
            fileListContainer.style.padding = '0';
        }
        selectedFiles.forEach((file, index) => {
            const fileElement = document.createElement('div');
            fileElement.className = 'file-item';

            const fileName = document.createElement('span');
            fileName.textContent = file.name;
            fileName.className = 'file-item'; // Add a class for styling

            const deleteIcon = document.createElement('span');
            deleteIcon.textContent = 'X';
            deleteIcon.className = 'delete-icon';
            deleteIcon.addEventListener('click', () => {
                selectedFiles = selectedFiles.filter((_, i) => i !== index); // Remove the file from the array
                updateFileListDisplay(); // Refresh the displayed file list
                // fileInput.value = ''; // Reset the file input to ensure change event can trigger again for the same file
             });

            fileElement.appendChild(fileName);
            fileElement.appendChild(deleteIcon);
            fileListContainer.appendChild(fileElement);
        });
    }

    // Handle files after selection or drop
    function handleFiles(files) {
        const dropZoneText = document.getElementById('dropZone').querySelector('p'); // Assuming your dropzone has a <p> tag for text
        const originalText = dropZoneText.textContent; // Save the original text
        dropZoneText.innerHTML = '<div class="spinner"></div>'; // Add your spinner HTML here
        selectedFiles = selectedFiles.concat(Array.from(files)); // Add new files to the array
        setTimeout(() => {
            updateFileListDisplay(); // Update the list display
            dropZoneText.textContent = originalText;
            fileInput.value = '';
        }, 1000); // Adjust the delay as necessary
    }

    // Open file dialog when dropZone is clicked
    dropZone.addEventListener('click', () => fileInput.click());

    // Update selected files when user selects files
    fileInput.addEventListener('change', function() {
        handleFiles(this.files);
        // fileInput.value = ''; // Clear the file input to allow re-uploading the same file
    });

    // Handle file drop
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        const files = e.dataTransfer.files;
        handleFiles(files);
    });

    // Prevent default behavior for dragover
    dropZone.addEventListener('dragover', (e) => e.preventDefault());

    form.addEventListener('submit', function(e) {
        e.preventDefault(); // Prevent normal form submission

        const formData = new FormData(this);
        selectedFiles.forEach((file) => {
            formData.append('capsule_contents', file);
        });

        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: { 'X-CSRFToken': csrftoken },
            credentials: 'include',
        })
        .then(response => response.text())
        .then(data => {
            console.log(data); // For debugging
            const [status, message] = data.split('|');
                window.location.href = message;  // Redirect to the given URL
        })
        .catch(error => console.error('Error:', error));
    });

    // Function to open and populate the modal for editing
    document.querySelectorAll('.edit-icon').forEach(button => {
        button.addEventListener('click', function() {
            const capsuleId = this.getAttribute('data-capsule-id');
            fetch(`/edit/${capsuleId}/`, { method: 'GET', credentials: 'include' })
                .then(response => response.json())
                .then(data => {
                    console.log(data)
                    document.getElementById('form-button').textContent = 'Update';
                    // Populate the form fields with the capsule data
                    document.getElementById('nameBlock').classList.add('active');
                    document.getElementById('nameLabel').classList.add('active');
                    document.getElementById('id_name').value = data.name;

                    document.getElementById('descriptionBlock').classList.add('active');
                    document.getElementById('descriptionLabel').classList.add('active');
                    document.getElementById('id_description').value = data.description;

                    document.getElementById('unsealing_dateBlock').classList.add('active');
                    document.getElementById('unsealing_dateLabel').classList.add('active');
                    document.getElementById('id_unsealing_date').value = data.unsealing_date;

                    let is_public = data.is_public ? 'True' : 'False';
                    document.getElementById('id_is_public').value = is_public;

                    let status = data.status ? 'True' : 'False';
                    document.getElementById('id_status').value = status;

                    // Change the form action to update the capsule
                    document.querySelector('#capsuleForm').action = `/edit/${capsuleId}/`;
                    modal.style.display = "flex";  // Open the modal
                })
                .catch(error => console.error('Error:', error));
        });
    });
});
