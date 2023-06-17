// Execute code when the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function() {
    // Add event listener to the "Shop Now" button
    var ctaButton = document.querySelector(".cta-button");
    ctaButton.addEventListener("click", function(event) {
      event.preventDefault();
      // Replace with the appropriate URL to the shop page
      window.location.href = "shop.html";
    });
  });

  // Execute code when the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function() {
    // Get all the store sections
    var storeSections = document.querySelectorAll(".store");
  
    // Iterate over each store section
    storeSections.forEach(function(section) {
      // Get the store info and image elements within the section
      var storeInfo = section.querySelector(".store-info");
      var storeImage = section.querySelector(".store-image");
  
      // Add event listener to each store section
      section.addEventListener("click", function() {
        // Replace with the appropriate URL to the store page
        window.location.href = "store.html";
      });
  
      // Add hover effect to each store section
      section.addEventListener("mouseover", function() {
        storeInfo.classList.add("active");
        storeImage.classList.add("active");
      });
  
      section.addEventListener("mouseout", function() {
        storeInfo.classList.remove("active");
        storeImage.classList.remove("active");
      });
    });
  });

  // Execute code when the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function() {
  // Get the remove buttons for each cart item
  var removeButtons = document.querySelectorAll(".remove-item");

  // Add event listener to each remove button
  removeButtons.forEach(function(button) {
    button.addEventListener("click", function(event) {
      event.preventDefault();
      // Remove the entire cart item when the remove button is clicked
      var cartItem = button.closest(".cart-item");
      cartItem.remove();
    });
  });

  // Get the checkout button
  var checkoutButton = document.querySelector(".checkout-button");

  // Add event listener to the checkout button
  checkoutButton.addEventListener("click", function(event) {
    event.preventDefault();
    // Perform the necessary actions to complete the checkout process
    // Replace with your own logic for the checkout process
    alert("Checkout process initiated!");
  });
});

// Execute code when the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function() {
  // Get the checkout button
  var checkoutButton = document.querySelector(".checkout-button");

  // Add event listener to the checkout button
  checkoutButton.addEventListener("click", function(event) {
    event.preventDefault();
    // Perform the necessary actions to complete the checkout process
    // Replace with your own logic for the checkout process
    var nameInput = document.getElementById("name").value;
    var addressInput = document.getElementById("address").value;

    // Perform validation on the input fields
    if (nameInput.trim() === "" || addressInput.trim() === "") {
      alert("Please provide your name and address.");
      return;
    }

    // Continue with the checkout process
    alert("Order placed successfully! Thank you for shopping with us.");
  });
});

// Execute code when the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function() {
  // Get the login and register forms
  var loginForm = document.querySelector(".login-form");
  var registerForm = document.querySelector(".register-form");

  // Add event listener to the login form
  loginForm.addEventListener("submit", function(event) {
    event.preventDefault();
    // Perform the necessary actions to process the login
    // Replace with your own logic for user authentication
    var emailInput = document.getElementById("login-email").value;
    var passwordInput = document.getElementById("login-password").value;

    // Perform validation on the input fields
    if (emailInput.trim() === "" || passwordInput.trim() === "") {
      alert("Please provide your email and password.");
      return;
    }

    // Continue with the login process
    alert("Login successful!");
    // Redirect to the desired page after login
    window.location.href = "dashboard.html";
  });

  // Add event listener to the register form
  registerForm.addEventListener("submit", function(event) {
    event.preventDefault();
    // Perform the necessary actions to process the registration
    // Replace with your own logic for user registration
    var nameInput = document.getElementById("register-name").value;
    var emailInput = document.getElementById("register-email").value;
    var passwordInput = document.getElementById("register-password").value;

    // Perform validation on the input fields
    if (nameInput.trim() === "" || emailInput.trim() === "" || passwordInput.trim() === "") {
      alert("Please provide your name, email, and password.");
      return;
    }

    // Continue with the registration process
    alert("Registration successful!");
    // Redirect to the desired page after registration
    window.location.href = "dashboard.html";
  });
});


// Execute code when the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function() {
  // Get the add-to-cart buttons
  var addToCartButtons = document.querySelectorAll(".add-to-cart");

  // Add event listener to each add-to-cart button
  addToCartButtons.forEach(function(button) {
    button.addEventListener("click", function(event) {
      event.preventDefault();
      // Perform the necessary actions to add the item to the cart
      // Replace with your own logic for adding items to the cart

      // Get the product details
      var storeItem = button.closest(".store-item");
      var productName = storeItem.querySelector("h3").innerText;
      var productPrice = storeItem.querySelector("p").innerText;

      // Create an object representing the item to add to the cart
      var item = {
        name: productName,
        price: productPrice
      };

      // Add the item to the cart
      addToCart(item);
    });
  });

  // Function to add an item to the cart
  function addToCart(item) {
    // Replace with your own logic for adding the item to the cart
    // You can store the item in local storage, make an API request, etc.

    // Display a success message to the user
    alert("Item added to cart!");
  }
});

  