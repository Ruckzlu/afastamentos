document.getElementById('travel-form').addEventListener('submit', function(event) {
    event.preventDefault();

    var formData = new FormData(this);
    fetch('/submit_form', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(result => {
        alert(result);
        document.getElementById('travel-form').reset();
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
