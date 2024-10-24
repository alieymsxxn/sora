function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie string begins with the name we want
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function isValidUrl(string) {
    let url;
    try {
        url = new URL(string);
    } catch (_) {
        return false;
    }
    return url.protocol === "http:" || url.protocol === "https:";
}

function isEmpty(field) {
    if (field.value == '') {
        return true
    } else {
        return false
    }
}
// Function to validate fields
function validate_fields() {
    var valid = true
    const url = document.getElementById('url')
    const services = document.getElementById('services')
    if (isEmpty(url)) {
        document.getElementById('url_label').classList.replace("text-gray-900", "text-red-600")
        url.classList.add('input-red')
        document.getElementById('url_error_msg').innerText = 'It looks like you’ve missed providing the URL.'
        valid = false
    } else if (isValidUrl(url)) {
        document.getElementById('services_label').classList.replace("text-gray-900", "text-red-600")
        services.classList.add('input-red')
        document.getElementById('url_error_msg').innerText = 'The URL you entered doesn’t seem right. Please check and try again'
        valid = false
    }
    if (isEmpty(services)) {
        document.getElementById('services_label').classList.replace("text-gray-900", "text-red-600")
        services.classList.add('input-red')
        document.getElementById('services_error_msg').innerText = 'It seems like you haven’t provided any services description.'
        valid = false
    }
    return valid
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('copy-email-btn').addEventListener('click', function (event) {
        button = event.target
        let textNode = button.childNodes[2];  // Get the text node
        textNode.textContent = "Copied";
        var email = document.getElementById("email-view");
        navigator.clipboard.writeText(email.textContent);
    });
    document.getElementById('reset-form-btn').addEventListener('click', function () {
        document.getElementById('email-label').classList.add("hidden")
        document.getElementById('email-loader').classList.add("hidden")
        document.getElementById('content-container').classList.add("hidden")
        document.getElementById('email-view').classList.add('hidden');
        document.getElementById('content-btn-group').classList.add("hidden");
        document.getElementById('form-container').classList.remove("hidden")
        document.getElementById('url').value = '';
        document.getElementById('services').value = '';
    });
    document.getElementById('gen-email-btn').addEventListener('click', function (event) {
        event.preventDefault();
        valid = validate_fields()
        if (valid == false) {
            return
        }

        document.getElementById('form-container').classList.add("hidden")
        document.getElementById('email-label').classList.remove("hidden")
        document.getElementById('email-loader').classList.remove("hidden")
        document.getElementById('content-container').classList.remove("hidden")


        var xhr = new XMLHttpRequest();
        xhr.open('POST', 'generate/demo-email/', true);
        xhr.setRequestHeader('Content-Type', 'application/json');

        const url = document.getElementById('url').value;
        const services = document.getElementById('services').value;

        var csrftoken = getCookie('csrftoken');
        xhr.setRequestHeader('X-CSRFToken', csrftoken);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        var data = JSON.stringify({ job_url: url, services: services });

        xhr.onload = function () {
            if (xhr.status >= 200 && xhr.status < 300) {
                const obj = JSON.parse(xhr.responseText)
                var email = obj.email
                console.log(email)
                document.getElementById('email-view').innerHTML = email;
                document.getElementById('email-view').classList.remove('hidden');
                document.getElementById('email-loader').classList.add("hidden");
                document.getElementById('content-btn-group').classList.remove("hidden");
            } else {
                alert('Request failed. Status: ' + xhr.status);
            }
        }
        xhr.send(data);
    });
});