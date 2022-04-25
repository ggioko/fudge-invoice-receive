export let TOKEN = null;
const storeTOKEN = (token) => {
	TOKEN = token;
}

export function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    fetch('http://127.0.0.1:8080/auth_login/', {
        method: 'POST',
        headers: {
            'content-Type': 'application/json'
        },
        body: JSON.stringify({
            'email': email,
            'password': password
        })
    })
    .then(response => {
        if (response.status === 400 || response.status === 403) {
            response.json()
            .then(errorMsg => {
                console.log(errorMsg)
                document.getElementById("login-popup-message").textContent = errorMsg.message;
                document.getElementById("login-popup").style.display = "block";    
            })
        } else if (response.status === 200) {
            response.json()
            .then(data => {
                storeTOKEN(data.token)
                document.getElementById("logged-in").style.display = "flex"
                document.getElementById("not-logged-in").style.display = "none"
            })
        }
    })
    // any errors
    .catch(error => console.log('ERROR'))
}

export function register() {
    const email = document.getElementById("register-email").value;
    const password = document.getElementById("register-password").value;
    const confirmPassword = document.getElementById("register-confirm-password").value;

    if (password != confirmPassword) {
        document.getElementById("login-popup-message").textContent = "Passwords do not match";
        document.getElementById("login-popup").style.display = "block";    
    }
    else if (email === "") {
        document.getElementById("login-popup-message").textContent = "Email is missing";
        document.getElementById("login-popup").style.display = "block";  
    }
    else if (password === "") {
        document.getElementById("login-popup-message").textContent = "Password is missing";
        document.getElementById("login-popup").style.display = "block";  
    }
    else if (confirmPassword === "") {
        document.getElementById("login-popup-message").textContent = "Confirm passord is missing";
        document.getElementById("login-popup").style.display = "block";  
    }
    else {
        fetch('http://127.0.0.1:8080/auth_register/', {
            method: 'POST',
            headers: {
                'content-Type': 'application/json'
            },
            body: JSON.stringify({
                'email': email,
                'password': password
            })
        })
        .then(response => {
            console.log(response.status)
            if (response.status === 400 || response.status === 403) {
                response.json()
                .then(errorMsg => {
                    console.log(errorMsg)
                    document.getElementById("login-popup-message").textContent = errorMsg.message;
                    document.getElementById("login-popup").style.display = "block";    
                })
            } else if (response.status === 200) {
                document.getElementById("login-form").style.display = "block"
                document.getElementById("register-form").style.display = "none"
            }
        })
        // any errors
        .catch(error => console.log('ERROR'))
    }
}