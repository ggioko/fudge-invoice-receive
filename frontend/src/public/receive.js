import { TOKEN, USERNAME} from "./auth.js";

/*
* Method for extracting upload invoice data and token to give to API
*/
export function uploadInvoice() {
    let invoice = {};
    var readXml=null;
    var selectedFile = document.getElementById('invoice').files[0];
    console.log(selectedFile);
    var reader = new FileReader();
    reader.onload = function(e) {
        readXml=e.target.result;
        const { name } = selectedFile;
        
        invoice = {
          'invoice_name': name,
          'invoice_content': readXml
        }
        sendApiInvoice(invoice);
    }
    reader.readAsText(selectedFile);
}
  
/*
* Method for sending invoice id and token to API. Get communication report as a repsonse.
*/
export function recvApiCommReportId() {
    let params = {
        "invoice_id": document.getElementById('invoiceIdName').value
    };

    // Combining query with url
    let query = Object.keys(params)
                    .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(params[k]))
                    .join('&');

    let url = 'http://invoicerecv.us-east-1.elasticbeanstalk.com/search_id?' + query;

    fetch(url, {
        method: 'GET',
        headers: {
        'content-Type': 'application/json',
        'authorization': TOKEN
        }
    })
    .then(response => {
        if (response.status === 200) {
            response.json()
            .then((data) => {
                console.log('Success:', data);
                const commReport = document.createElement('div');
                commReport.id = "comm-report";
                createReport(data.comm_rep_id, data.invoice_name, data.invoice_id, data.comm_msg, data.comm_time, commReport);
            })
        }
        else if (response.status === 400 || response.status === 403 || response.status === 500) {
            addErrorMessage("invoice")
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
  
  
export function recvApiCommReportName() {
    let params = {
        "invoice_n": document.getElementById('invoiceIdName').value
    };

    // Combining query with url
    let query = Object.keys(params)
                    .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(params[k]))
                    .join('&');

    let url = 'http://invoicerecv.us-east-1.elasticbeanstalk.com/search_name?' + query;

    fetch(url, {
        method: 'GET',
        headers: {
        'content-Type': 'application/json',
        'authorization': TOKEN,
        }
    })
    .then(response => {
        if (response.status === 200) {
            response.json()
            .then((data) => {
                console.log('Success:', data);
                const commReport = document.createElement('div');
                commReport.id = "comm-report";
                for (var key in data) {
                    createReport(data[key].comm_rep_id, data[key].invoice_name, data[key].invoice_id, data[key].comm_msg, data[key].comm_time, commReport);
                }
            })
        }
        else if (response.status === 400 || response.status === 403 || response.status === 500) {
            addErrorMessage("report")
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}


/*
* Method for sending invoice id and token to API. Get pdf invoice as a repsonse.
*/
export function recvApiInvoiceContent() {
    let params = {
        "invoice_id": document.getElementById('invoiceId2').value
    };

    // Combining query with url
    let query = Object.keys(params)
                    .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(params[k]))
                    .join('&');

    let url = 'http://invoicerecv.us-east-1.elasticbeanstalk.com/invoice_content?' + query;

    fetch(url, {
        method: 'GET',
        headers: {
        'authorization': TOKEN
        }
    })
    .then(response => response.json())
    .then(data => {
        sendRenderApiInvoice(data);
        createInv(data);

    })
    .catch((error) => {
        console.error('Error:', error);
    });
}


/*
* Method for sending invoice to API
*/
function sendApiInvoice(invoice) {
    // fetch API no supported by older browsers like internet explorer
    // just trying a get request
    console.log(invoice);
    fetch('http://invoicerecv.us-east-1.elasticbeanstalk.com/invoice_receive/', {
        method: 'POST',
        headers: {
        'content-Type': 'application/json',
        'authorization': TOKEN
        },
        body: JSON.stringify(invoice)
    })
    .then(response => {
        if (response.status === 200) {
            response.json()
            .then(data => {
                console.log(data);
                const commReport = document.createElement('div');
                commReport.id = "comm-report";
                createReport(data.comm_rep_id, data.invoice_name, data.invoice_id, data.comm_msg, data.comm_time, commReport);
            })
        }
        else if (response.status === 400 || response.status === 403 || response.status === 500) {
            addErrorMessage("invoiceUpload")
        }
    })
    // any errors
    .catch(error => console.log('ERROR', error))

}

/*
* Method for getting rendered invoice from API
*/
function sendRenderApiInvoice(invoiceContent) {
    // fetch API no supported by older browsers like internet explorer
    // just trying a get request
    console.log(invoiceContent);
    fetch('http://invoicerecv.us-east-1.elasticbeanstalk.com/invoice_render/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'authorization': TOKEN
        },
        body: JSON.stringify({
            'xml': invoiceContent
        })
    })
    .then(response => {
        if (response.status === 200) {
            response.blob()
            .then(blob => {
                console.log(blob);
                var url = window.URL.createObjectURL(blob);
                const pdfPreview = document.createElement('embed');
                pdfPreview.id = "pdf-preview"
                pdfPreview.src = url;
                document.getElementById("display-invoice").append(pdfPreview);
                pdfPreview.height = "100%"
            })
        }
        else if (response.status === 400 || response.status === 403 || response.status === 500) {
            addErrorMessage("invoice")
        }
    })
    .catch((error) => {
        console.log('DOWNLOAD ERROR', error);
    });

}

/*
* Method for sending invoice id and token to API. Deletes invoice form database
*/
export function deleteApiInvoiceContent() {
    let params = {
        "invoice_id": document.getElementById('invoiceId2').value
    };

    // Combining query with url
    let query = Object.keys(params)
                    .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(params[k]))
                    .join('&');

    let url = 'http://invoicerecv.us-east-1.elasticbeanstalk.com/invoice_delete?' + query;

    fetch(url, {
        method: 'DELETE',
        headers: {
        'authorization': TOKEN
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log("Success:", data)
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

export function createReport(comm_rep_id, invoice_name, invoice_id, comm_msg, comm_time, commReport) {
    const commReportSection = document.getElementById("display-report");

    const commReportId = document.createElement('p');
    commReportId.textContent = "Communcation Report ID: " + comm_rep_id;
    commReport.appendChild(commReportId);

    const newline1 = document.createElement('br');
    commReport.appendChild(newline1);

    const commReportInvoiceName = document.createElement('h2');
    commReportInvoiceName.textContent = invoice_name;
    commReport.appendChild(commReportInvoiceName);

    const newline2 = document.createElement('br');
    commReport.appendChild(newline2);

    const commReportInvoiceId = document.createElement('p');
    commReportInvoiceId.textContent = "Invoice ID: " + invoice_id;
    commReport.appendChild(commReportInvoiceId);

    const newline3 = document.createElement('br');
    commReport.appendChild(newline3);

    const commReportMsg = document.createElement('p');
    commReportMsg.textContent = comm_msg;
    commReport.appendChild(commReportMsg);

    const newline4 = document.createElement('br');
    commReport.appendChild(newline4);

    const commReportTime = document.createElement('p');
    commReportTime.textContent = "Received at: " + comm_time;
    commReport.appendChild(commReportTime);
    commReportTime.style.fontWeight = 'bold';
    commReportSection.appendChild(commReport);

    commReportSection.style.fontWeight ='bold';
    commReportSection.style.display = "flex";

    const newline5 = document.createElement('br');
    commReport.appendChild(newline5);

    const note = document.createElement('p');
    note.textContent = "(Invoice Id can used to reaccess and download your invoice)";
    note.style.fontWeight = '200';
    commReport.appendChild(note);

    const newline6 = document.createElement('br');
    commReport.appendChild(newline6);

    const breakline = document.createElement('hr');
    breakline.style.width = '100%'
    commReport.appendChild(breakline);
}

function createInv() {
    const invSection = document.getElementById("display-invoice");

    // const invContent = document.createElement('h2');
    // invContent.textContent = "Invoice Preview";
    // invContent.id = "invoice-content"

    const invDelete = document.createElement('input');
    invDelete.value = "DELETE INVOICE";
    invDelete.type = "button";
    invDelete.style.background = "#323940"
    invDelete.style.color = "white"
    invDelete.id = "inv-delete";
    
    invSection.appendChild(invDelete);

    invDelete.addEventListener("click", (event) => {
        deleteApiInvoiceContent();
    })

    invSection.style.display = "flex";
}

export function addErrorMessage(type) {
    if (type === "invoice") {
        alert("Invoice does not exist with given id or name");
    }
    else if (type === "invoiceUpload") {
        alert("Invoice could not be uploaded at this time");
    }
    else if (type === "report") {
        alert("Communication report does not exist with given id or name");
    }
    else if (type === "account") {
        alert("Account information could not be updated at this time");
    }
    else if (type === "success") {
        alert("success!");
    }
}
