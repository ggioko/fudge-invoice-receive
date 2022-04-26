import { uploadInvoice, recvApiCommReportId, recvApiCommReportName, recvApiInvoiceContent } from "./receive.js";
import { login, logout, register, req_reset, reset_password, USERNAME} from "./auth.js";
import { sendInvoice } from "./send.js";
import { deleteAccount, updateEmail, updateuserName } from "./account.js";

function isNumeric(val) {
  return /^-?\d+$/.test(val);
}

function clearForms() {
  document.getElementById("email").value = "";
  document.getElementById("password").value = "";
  document.getElementById("register-email").value = "";
  document.getElementById("register-confirm-password").value = "";
  document.getElementById("register-password").value = "";

  // display section clear
  if (document.getElementById("comm-report") != null) { document.getElementById("comm-report").remove(); }
  if (document.getElementById("invoice-content") != null) { document.getElementById("invoice-content").remove(); }
  if (document.getElementById("pdf-preview") != null) { document.getElementById("pdf-preview").remove(); }
  if (document.getElementById("inv-delete") != null) { document.getElementById("inv-delete").remove(); }
  if (document.getElementById("err-message") != null) { document.getElementById("err-message").remove(); }
}

// EVENT LISTENERS
document.getElementById("login-button").addEventListener("click", (event) => { login(); })

document.getElementById("login-register-button").addEventListener("click", (event) => {
  document.getElementById("login-form").style.display = "none";
  document.getElementById("reset-req-form").style.display = "none";
  document.getElementById("reset-form").style.display = "none";
  document.getElementById("register-form").style.display = "flex";
  document.getElementById("contact-form").style.display = "none";
})

document.getElementById("register-button").addEventListener("click", (event) => { register(); })

document.getElementById("register-login-button").addEventListener("click", (event) => {
  document.getElementById("login-form").style.display = "flex";
  document.getElementById("reset-req-form").style.display = "none";
  document.getElementById("reset-form").style.display = "none";
  document.getElementById("register-form").style.display = "none";
  document.getElementById("contact-form").style.display = "none";
})

document.getElementById("login-forgot-password").addEventListener("click", (event) => {
  document.getElementById("login-form").style.display = "none";
  document.getElementById("reset-req-form").style.display = "flex";
  document.getElementById("reset-form").style.display = "none";
  document.getElementById("register-form").style.display = "none"; 
  document.getElementById("contact-form").style.display = "none";
})

document.getElementById("forgot-password-button").addEventListener("click", (event) => {
  req_reset()
  document.getElementById("login-form").style.display = "none";
  document.getElementById("reset-req-form").style.display = "none";
  document.getElementById("reset-form").style.display = "flex";
  document.getElementById("register-form").style.display = "none";
  document.getElementById("contact-form").style.display = "none";
})

document.getElementById("contact").addEventListener("click", (event) => {
  req_reset()
  document.getElementById("login-form").style.display = "none";
  document.getElementById("reset-req-form").style.display = "none";
  document.getElementById("reset-form").style.display = "none";
  document.getElementById("register-form").style.display = "none";
  document.getElementById("contact-form").style.display = "flex";
})

document.getElementById("reset-password").addEventListener("click", (event) => {
  document.getElementById("reset-form").style.display = "none";
  document.getElementById("new-password-form").style.display = "flex";
  reset_password()
})

document.getElementById("nav-bar-faq1").addEventListener("click", (event) => {
  document.getElementById("login-form").style.display = "none";
  document.getElementById("reset-req-form").style.display = "none";
  document.getElementById("reset-form").style.display = "none";
  document.getElementById("register-form").style.display = "none";
  document.getElementById("contact-form").style.display = "none";
  document.getElementById("homepage-logo").style.display = "none";
  document.getElementById("faq1").style.display = "flex";
})

document.getElementById("login-popup-close").addEventListener("click", (event) => {
  document.getElementById("login-popup").style.display = "none";
})

document.getElementById("nav-bar-upload").addEventListener("click", (event) => {
  document.getElementById("upload").style.display = "flex";
  document.getElementById("reports").style.display = "none";
  document.getElementById("invoices").style.display = "none";
  document.getElementById("display-report").style.display = "none";
  document.getElementById("display-invoice").style.display = "none";
  document.getElementById("account").style.display = "none";
  document.getElementById("faq").style.display = "none";
  clearForms()
})
document.getElementById("nav-bar-invoices").addEventListener("click", (event) => {
  document.getElementById("upload").style.display = "none";
  document.getElementById("reports").style.display = "none";
  document.getElementById("invoices").style.display = "flex";
  document.getElementById("display-report").style.display = "none";
  document.getElementById("display-invoice").style.display = "none";
  document.getElementById("account").style.display = "none";
  document.getElementById("faq").style.display = "none";
  clearForms()
})
document.getElementById("nav-bar-account").addEventListener("click", (event) => {
  document.getElementById("upload").style.display = "none";
  document.getElementById("reports").style.display = "none";
  document.getElementById("invoices").style.display = "none";
  document.getElementById("display-report").style.display = "none";
  document.getElementById("display-invoice").style.display = "none";
  document.getElementById("account").style.display = "flex";
  document.getElementById("faq").style.display = "none";
  clearForms()
})
document.getElementById("nav-bar-reports").addEventListener("click", (event) => {
  document.getElementById("upload").style.display = "none";
  document.getElementById("reports").style.display = "flex";
  document.getElementById("invoices").style.display = "none";
  document.getElementById("display-report").style.display = "none";
  document.getElementById("display-invoice").style.display = "none";
  document.getElementById("account").style.display = "none";
  document.getElementById("faq").style.display = "none";
  clearForms()
})

document.getElementById("nav-bar-faq").addEventListener("click", (event) => {
  document.getElementById("upload").style.display = "none";
  document.getElementById("reports").style.display = "none";
  document.getElementById("invoices").style.display = "none";
  document.getElementById("display-report").style.display = "none";
  document.getElementById("display-invoice").style.display = "none";
  document.getElementById("account").style.display = "none";
  document.getElementById("faq").style.display = "flex";
  clearForms()
})

document.getElementById("nav-bar-logout").addEventListener("click", (event) => {
  document.getElementById("upload").style.display = "flex";
  document.getElementById("reports").style.display = "none";
  document.getElementById("invoices").style.display = "none";
  document.getElementById("display-report").style.display = "none";
  document.getElementById("display-invoice").style.display = "none";
  document.getElementById("account").style.display = "none";
  document.getElementById("faq").style.display = "none";
  //document.getElementById("account").style.display = "none";
  clearForms()

  document.getElementById("logged-in").style.display = "none"
  document.getElementById("not-logged-in").style.display = "flex"
  logout()
})

document.getElementById("upload-button").addEventListener("click", (event) => { 
  clearForms()
  uploadInvoice(); 
})
document.getElementById("upload-button1").addEventListener("click", (event) => { 
  clearForms()
  sendInvoice(); 
})
document.getElementById("account").addEventListener("click", (event) => { 
  clearForms()
  // function to send account info to backend
})
document.getElementById("invoices-button").addEventListener("click", (event) => { 
  clearForms()
  document.getElementById('display-invoice').style.display = "flex";
  recvApiInvoiceContent(); 
})
document.getElementById("reports-button").addEventListener("click", (event) => { 
  clearForms()
  if (isNumeric(document.getElementById("invoiceIdName").value) === true) {
    recvApiCommReportId(); 
  }
  else {
    recvApiCommReportName();
  }
})
document.getElementById("email-button").addEventListener("click", (event) => { 
  updateEmail();
  clearForms()
})
document.getElementById("username-button").addEventListener("click", (event) => { 
  updateuserName();
  clearForms()
})
document.getElementById("delete-account-button").addEventListener("click", (event) => { 
  deleteAccount();
})