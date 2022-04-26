import { TOKEN } from "./auth.js";
import { createReport, addErrorMessage} from "./receive.js";

/*
* Method for extracting upload invoice data and token to give to API
*/
export function sendInvoice() {
    let info= {};
    var readXml=null;
    var selectedFile = document.getElementById('invoice1').files[0];
    var username = document.getElementById('username').value
    console.log(selectedFile);
    var reader = new FileReader();
    reader.onload = function(e) {
        readXml=e.target.result;
        const { name } = selectedFile;
        
        info = {
          'invoice_name': name,
          'invoice_content': readXml,
          'username': username
        }
        sendUserInvoice(info);
    }
    reader.readAsText(selectedFile);
}
  

/*
* Method for sending invoice to API
*/
function sendUserInvoice(info) {
    // fetch API no supported by older browsers like internet explorer
    // just trying a get request
    console.log(info);
    fetch('http://invoicerecv.us-east-1.elasticbeanstalk.com/invoice_send/', {
        method: 'POST',
        headers: {
        'content-Type': 'application/json',
        'authorization': TOKEN
        },
        body: JSON.stringify(info)
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