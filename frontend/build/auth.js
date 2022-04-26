export let TOKEN = null;
const storeTOKEN = (token) => {
	TOKEN = token;
}
export let USERNAME = null;
const storeUSERNAME = (username) => {
    USERNAME = username;
}

export function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    fetch('http://invoicerecv.us-east-1.elasticbeanstalk.com/auth_login/', {
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
                document.getElementById("login-popup-message").textContent = "Wrong email or password";
                document.getElementById("login-popup").style.display = "block";    
            })
        } else if (response.status === 200) {
            response.json()
            .then(data => {
                storeTOKEN(data.token)
                document.getElementById("logged-in").style.display = "flex"
                document.getElementById("not-logged-in").style.display = "none"

                    // Combining query with url
                let url = 'http://invoicerecv.us-east-1.elasticbeanstalk.com/username?';

                fetch(url, {
                    method: 'GET',
                    headers: {
                    'content-Type': 'application/json',
                    'authorization': TOKEN
                    }
                }).then(response => {
                    response.json()
                    .then(data => {
                        storeUSERNAME(data.username)
                        document.getElementById('page-title').innerHTML = 
                        USERNAME
                    })
                })
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
    else if (password.length < 8) {
        document.getElementById("login-popup-message").textContent = "Password is less than 8 characters";
        document.getElementById("login-popup").style.display = "block";  
    }
    else {
        fetch('http://invoicerecv.us-east-1.elasticbeanstalk.com/auth_register/', {
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
                    document.getElementById("login-popup-message").textContent = "Error";
                    document.getElementById("login-popup").style.display = "block";    
                })
            } else if (response.status === 200) {
                document.getElementById("login-form").style.display = "flex"
                document.getElementById("register-form").style.display = "none"
                document.getElementById("login-popup-message").textContent = "Successfully Registered";
                document.getElementById("login-popup").style.display = "block";  
            }
        })
        // any errors
        .catch(error => console.log('ERROR'))
    }
}

export function logout() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    fetch('http://invoicerecv.us-east-1.elasticbeanstalk.com/auth_logout/', {
        method: 'POST',
        headers: {
            'content-Type': 'application/json',
            'token': TOKEN
        }
    })
    // any errors
    .catch(error => console.log('ERROR'))
}

export function req_reset(){
    const email = document.getElementById("account-email").value
    fetch('http://invoicerecv.us-east-1.elasticbeanstalk.com/auth_reset_password_req/', {
        method: 'POST',
        headers: {
            'content-Type': 'application/json'
        },
        body: JSON.stringify({
            'email': email,
        })
    })
    // any errors
    .catch(error => console.log('ERROR'))
}

export function reset_password(){
    const reset_code = document.getElementById("reset-code").value
    const new_password = document.getElementById("new-password").value
    const confirm_password = document.getElementById("confirm-password").value
    if (new_password != confirm_password) {
        document.getElementById("login-popup-message").textContent = "Passwords do not match";
        document.getElementById("login-popup").style.display = "block";    
    }
    else {
        fetch('http://invoicerecv.us-east-1.elasticbeanstalk.com/auth_reset_password/', {
            method: 'POST',
            headers: {
                'content-Type': 'application/json'
            },
            body: JSON.stringify({
                'reset_code': reset_code,
                'new_password': new_password
            })
        })
        .catch(error => console.log('ERROR'))
    }   
    // any errors
}