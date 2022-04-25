import { uploadInvoice, recvApiCommReportId, recvApiCommReportName, recvApiInvoiceContent } from "./receive.js";
import { login, register } from "./auth.js";

function isNumeric(val) {
  return /^-?\d+$/.test(val);
}

// EVENT LISTENERS
document.getElementById("login-button").addEventListener("click", (event) => { login(); })

document.getElementById("login-register-button").addEventListener("click", (event) => {
  document.getElementById("login-form").style.display = "none";
  document.getElementById("register-form").style.display = "block";
})

document.getElementById("register-button").addEventListener("click", (event) => { register(); })

document.getElementById("register-login-button").addEventListener("click", (event) => {
  document.getElementById("login-form").style.display = "block";
  document.getElementById("register-form").style.display = "none";
})

document.getElementById("login-popup-close").addEventListener("click", (event) => {
  document.getElementById("login-popup").style.display = "none";
})

document.getElementById("nav-bar-upload").addEventListener("click", (event) => {
  document.getElementById("upload").style.display = "flex";
  document.getElementById("reports").style.display = "none";
  document.getElementById("invoices").style.display = "none";
  document.getElementById("display-report").style.display = "none";
  if (document.getElementById("comm-report") != null) { document.getElementById("comm-report").remove(); }
  if (document.getElementById("invoice-content") != null) { document.getElementById("invoice-content").remove(); }
  if (document.getElementById("pdf-preview") != null) { document.getElementById("pdf-preview").remove(); }
})
document.getElementById("nav-bar-invoices").addEventListener("click", (event) => {
  document.getElementById("upload").style.display = "none";
  document.getElementById("reports").style.display = "none";
  document.getElementById("invoices").style.display = "flex";
  document.getElementById("display-report").style.display = "none";
  if (document.getElementById("comm-report") != null) { document.getElementById("comm-report").remove(); }
  if (document.getElementById("invoice-content") != null) { document.getElementById("invoice-content").remove(); }
  if (document.getElementById("pdf-preview") != null) { document.getElementById("pdf-preview").remove(); }
})
document.getElementById("nav-bar-reports").addEventListener("click", (event) => {
  document.getElementById("upload").style.display = "none";
  document.getElementById("reports").style.display = "flex";
  document.getElementById("invoices").style.display = "none";
  document.getElementById("display-report").style.display = "none";
  if (document.getElementById("comm-report") != null) { document.getElementById("comm-report").remove(); }
  if (document.getElementById("invoice-content") != null) { document.getElementById("invoice-content").remove(); }
  if (document.getElementById("pdf-preview") != null) { document.getElementById("pdf-preview").remove(); }
})

document.getElementById("upload-button").addEventListener("click", (event) => { 
  if (document.getElementById("comm-report") != null) { document.getElementById("comm-report").remove(); }
  if (document.getElementById("invoice-content") != null) { document.getElementById("invoice-content").remove(); }
  if (document.getElementById("pdf-preview") != null) { document.getElementById("pdf-preview").remove(); }
  uploadInvoice(); 
})
document.getElementById("invoices-button").addEventListener("click", (event) => { 
  if (document.getElementById("comm-report") != null) { document.getElementById("comm-report").remove(); }
  if (document.getElementById("invoice-content") != null) { document.getElementById("invoice-content").remove(); }
  if (document.getElementById("pdf-preview") != null) { document.getElementById("pdf-preview").remove(); }
  document.getElementById('display-report').style.display = "flex";
  recvApiInvoiceContent(); 
})
document.getElementById("reports-button").addEventListener("click", (event) => { 
  if (document.getElementById("comm-report") != null) { document.getElementById("comm-report").remove(); }
  if (document.getElementById("invoice-content") != null) { document.getElementById("invoice-content").remove(); }
  if (document.getElementById("pdf-preview") != null) { document.getElementById("pdf-preview").remove(); }
  if (isNumeric(document.getElementById("invoiceIdName").value) === true) {
    recvApiCommReportId(); 
  }
  else {
    recvApiCommReportName();
  }
})