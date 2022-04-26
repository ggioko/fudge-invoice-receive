import { TOKEN, USERNAME } from "./auth.js";
import { addErrorMessage } from "./receive.js";
/*
* Method for extracting upload invoice data and token to give to API
*/
export function updateEmail() {

    const email = document.getElementById("reset-email").value;
    const password = document.getElementById("password1").value;

    fetch('http://invoicerecv.us-east-1.elasticbeanstalk.com/reset_email/', {
        method: 'POST',
        headers: {
            'content-Type': 'application/json',
            'authorization': TOKEN
        },
        body: JSON.stringify({
            'email': email,
            'password': password
        })
    })
    .then(response => {
        if (response.status === 200) {
            response.json()
            .then((data) => {
                console.log('Success:', data);
                addErrorMessage("success")

            })
        }
        else if (response.status === 400 || response.status === 403 || response.status === 500) {
            addErrorMessage("account")
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}


export function updateuserName() {

    const username = document.getElementById("updateUsername").value;
    const password = document.getElementById("password2").value;

    fetch('http://invoicerecv.us-east-1.elasticbeanstalk.com/update_username/', {
        method: 'POST',
        headers: {
            'content-Type': 'application/json',
            'authorization': TOKEN
        },
        body: JSON.stringify({
            'username': username,
            'password': password
        })
    })
    .then(response => {
        if (response.status === 200) {
            response.json()
            .then((data) => {
                console.log('Success:', data);
                addErrorMessage("success")

            })
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
                    data.username
                })
            })
        }
        else if (response.status === 400 || response.status === 403 || response.status === 500) {
            addErrorMessage("account")
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}


export function deleteAccount() {
    const password = document.getElementById("password3").value
    const confirm_password = document.getElementById("password4").value
    if (password != confirm_password) {
        document.getElementById("login-popup-message").textContent = "Passwords do not match";
        document.getElementById("login-popup").style.display = "block";    
        addErrorMessage("account")
    }
    else {
        let params = {
            "password": document.getElementById('password3').value
        };
    
        // Combining query with url
        let query = Object.keys(params)
                        .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(params[k]))
                        .join('&');
        let url ='http://invoicerecv.us-east-1.elasticbeanstalk.com/delete_account?' + query;

        fetch(url, {
            method: 'DELETE',
            headers: {
            'authorization': TOKEN
            }
        })
        .then(response => {
            if (response.status === 200) {
                document.getElementById("logged-in").style.display = "none"
                document.getElementById("not-logged-in").style.display = "flex"
                console.log("Success")
            }
            else if (response.status === 400 || response.status === 403 || response.status === 500) {
                addErrorMessage("account")
            }
        })   
        .catch((error) => {
            console.error('Error:', error);
        });
    }
}