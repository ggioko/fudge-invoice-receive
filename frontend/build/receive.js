import { TOKEN } from "./auth.js";

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

    let url = 'http://127.0.0.1:8080/search_id?' + query;

    fetch(url, {
        method: 'GET',
        headers: {
        'content-Type': 'application/json',
        'authorization': TOKEN
        }
    })
    .then(response => response.json())
    .then((data) => {
        console.log('Success:', data);
        const commReport = document.createElement('div');
        commReport.id = "comm-report";
        createReport(data.comm_rep_id, data.invoice_name, data.invoice_id, data.comm_msg, data.comm_time, commReport);
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

    let url = 'http://127.0.0.1:8080/search_name?' + query;

    fetch(url, {
        method: 'GET',
        headers: {
        'content-Type': 'application/json',
        'authorization': TOKEN,
        }
    })
    .then(response => response.json())
    .then((data) => {
        console.log('Success:', data);
        const commReport = document.createElement('div');
        commReport.id = "comm-report";
        for (var key in data) {
            createReport(data[key].comm_rep_id, data[key].invoice_name, data[key].invoice_id, data[key].comm_msg, data[key].comm_time, commReport);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}


/*
* Method for sending invoice id and token to API. Get communication report as a repsonse.
*/
export function recvApiInvoiceContent() {
    let params = {
        "invoice_id": document.getElementById('invoiceId2').value
    };

    // Combining query with url
    let query = Object.keys(params)
                    .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(params[k]))
                    .join('&');

    let url = 'http://127.0.0.1:8080/invoice_content?' + query;

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
    fetch('http://127.0.0.1:8080/invoice_receive/', {
        method: 'POST',
        headers: {
        'content-Type': 'application/json',
        'authorization': TOKEN
        },
        body: JSON.stringify(invoice)
    })
    .then(response =>{     
        // if (response.ok) {
        //     sendRenderApiInvoice(invoice.invoice_content);
        // }
        return response.json()
        
    })
    .then(data => {
        console.log(data);
        const commReport = document.createElement('div');
        commReport.id = "comm-report";
        createReport(data.comm_rep_id, data.invoice_name, data.invoice_id, data.comm_msg, data.comm_time, commReport);

    })
    // any errors
    .catch(error => console.log('ERROR', error))

}

/*
* Method for sending invoice to API
*/
function sendRenderApiInvoice(invoiceContent) {
    // fetch API no supported by older browsers like internet explorer
    // just trying a get request
    console.log(invoiceContent);
    fetch('http://127.0.0.1:8080/invoice_render/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'authorization': TOKEN
        },
        body: JSON.stringify({
            'xml': invoiceContent
        })
    })
    .then(response => response.blob())
    .then(blob => {
        console.log(blob);
        var url = window.URL.createObjectURL(blob);
        const pdfPreview = document.createElement('embed');
        pdfPreview.id = "pdf-preview"
        pdfPreview.src = url;
        document.getElementById("display-report").append(pdfPreview);
        // var a = document.createElement('a');
        // a.href = url;
        // a.download = "invoice.pdf";
        // document.body.appendChild(a); // we need to append the element to the dom -> otherwise it will not work in firefox
        // document.getElementById("invoices-download-button").addEventListener("click", (event) => {
        //     a.click();    
        //     a.remove();  //afterwards we remove the element again
        // }) 
        document.getElementById("invoices-download-button").style.display = "flex";      
    })
    .catch((error) => {
        console.log('DOWNLOAD ERROR', error);
    });

}

function createReport(comm_rep_id, invoice_name, invoice_id, comm_msg, comm_time, commReport) {
    const commReportSection = document.getElementById("display-report");

    const commReportId = document.createElement('p');
    commReportId.textContent = "Communcation Report ID: " + comm_rep_id;
    commReport.appendChild(commReportId);

    const commReportInvoiceName = document.createElement('h2');
    commReportInvoiceName.textContent = invoice_name;
    commReport.appendChild(commReportInvoiceName);

    const commReportInvoiceId = document.createElement('p');
    commReportInvoiceId.textContent = "Invoice ID: " + invoice_id;
    commReport.appendChild(commReportInvoiceId);

    const commReportMsg = document.createElement('p');
    commReportMsg.textContent = comm_msg;
    commReport.appendChild(commReportMsg);

    const commReportTime = document.createElement('p');
    commReportTime.textContent = "Received at: " + comm_time;
    commReport.appendChild(commReportTime);
    commReportTime.style.fontWeight = 'bold';
    commReportSection.appendChild(commReport);

    commReportSection.style.fontWeight ='bold';
    commReportSection.style.display = "flex";

    const note = document.createElement('p');
    note.textContent = "(Invoice Id can used to reaccess and download your invoice)";
    note.style.fontWeight = '200';
    note.appendChild(commReportTime);
    commReport.appendChild(note);
}

function createInv() {
    const invSection = document.getElementById("display-report");

    const invContent = document.createElement('h2');
    invContent.textContent = "Invoice Preview";
    invContent.id = "invoice-content"

    invSection.appendChild(invContent);
    invSection.style.display = "flex";
}