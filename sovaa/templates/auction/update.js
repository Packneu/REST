        document.addEventListener('DOMContentLoaded', function() {
            // Get the announcement data from the server
            fetch('/{{ announcement.id }}/data')
                .then(response => response.json())
                .then(data => {
                    // Pre-fill the form with the announcement data
                    document.getElementById('title').value = data.title;
                    document.getElementById('body').value = data.body;
                    document.getElementById('price').value = data.price;
                });

            // Handle the form submission
            document.getElementById('update-form').addEventListener('submit', function(event) {
                event.preventDefault();

                var form = event.target;
                var formData = new FormData(form);

                // Send the form data to the server
                fetch('/{{ announcement.id }}/update', {
                    method: 'POST',
                    body: formData
                })
                .then(response => {
                    if (response.ok) {
                        // Redirect to the index page on successful update
                        window.location.href = '/';
                    } else {
                        // Display an error message on update failure
                        alert('Failed to update the announcement.');
                    }
                });
            });
        });