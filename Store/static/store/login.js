// Execute code when the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function() {
    // Get the login and register forms
    var loginForm = document.getElementById("login-form");
    var registerForm = document.getElementById("register-form");
  
    // Get the login and register links
    var loginLink = document.getElementById("login-link");
    var registerLink = document.getElementById("register-link");
  
    // Add event listener to the login link
    loginLink.addEventListener("click", function(event) {
      event.preventDefault();
      toggleForms();
    });
  
    // Add event listener to the register link
    registerLink.addEventListener("click", function(event) {
      event.preventDefault();
      toggleForms();
    });
  
    // Function to toggle between login and register forms
    function toggleForms() {
      loginForm.classList.toggle("active");
      registerForm.classList.toggle("active");
    }
  });
  