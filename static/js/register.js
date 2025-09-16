const registerButton = document.getElementById('register');
const loginButton = document.getElementById('login');       
const container = document.getElementById('container');

// Hardcoded user credentials for demonstration
const localUser = {
  email: 'rideouts199@gmail.com',
  username: 'demesis221',
  password: 'ernesto123'
};

// Handle login form submission
const loginForm = document.querySelector('.login-container form');
if (loginForm) {
  loginForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const emailOrUsername = document.querySelector('.login-container input[type="text"]').value.trim();
    const password = document.querySelector('.login-container input[type="password"]').value.trim();
    
    // Validate input
    if (!emailOrUsername || !password) {
      alert('Please enter both email/username and password');
      return;
    }
    
    // Check if login is with email (contains @)
    const isEmail = emailOrUsername.includes('@');
    
    // If user is trying to login with email, validate email format
    if (isEmail && !isValidEmail(emailOrUsername)) {
      alert('Please enter a valid email address');
      return;
    }
    
    // Check if credentials match our local user
    if ((isEmail && emailOrUsername === localUser.email) || 
        (!isEmail && emailOrUsername === localUser.username)) {
      
      // Now check password
      if (password === localUser.password) {
        // Successful login
        localStorage.setItem('loggedIn', 'true');
        localStorage.setItem('username', localUser.username);
        
        // Show success message
        alert('Login successful! Welcome back, ' + localUser.username);
        
        // Redirect to main page or dashboard
        window.location.href = 'home.html';
        return;
      }
    }
    
    // If we get here, login failed
    alert('Invalid email/username or password. Please try again.');
  });
}

// Function to validate email format
function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

// Handle registration form submission
const registerForm = document.querySelector('.register-container form');
if (registerForm) {
  registerForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    // For demo purposes, just show a message
    alert('Registration functionality is not available in the demo. Please use the provided demo account to log in.');
    
    // Switch to login form
    container.classList.remove("right-panel-active");
  });
}

registerButton.addEventListener('click', () => {
container.classList.add("right-panel-active");
});

loginButton.addEventListener('click', () => {
container.classList.remove("right-panel-active");
 });

 // Mobile navigation support
 const loginToRegisterBtn = document.getElementById('loginToRegisterBtn');
 const registerToLoginBtn = document.getElementById('registerToLoginBtn');
 
 if (loginToRegisterBtn) {
   loginToRegisterBtn.addEventListener('click', () => {
     container.classList.add("right-panel-active");
   });
 }
 
 if (registerToLoginBtn) {
   registerToLoginBtn.addEventListener('click', () => {
     container.classList.remove("right-panel-active");
   });
 }
 
 // Show/hide the appropriate mobile toggle button based on current state
 function updateMobileToggleVisibility() {
   const loginToggle = document.querySelector('.login-toggle');
   const registerToggle = document.querySelector('.register-toggle');
   
   if (container.classList.contains('right-panel-active')) {
     if (loginToggle) loginToggle.style.display = 'none';
     if (registerToggle) registerToggle.style.display = 'flex';
   } else {
     if (loginToggle) loginToggle.style.display = 'flex';
     if (registerToggle) registerToggle.style.display = 'none';
   }
 }
 
 // Initial call to set visibility
 document.addEventListener('DOMContentLoaded', updateMobileToggleVisibility);
 
 // Update visibility when switching forms
 registerButton.addEventListener('click', updateMobileToggleVisibility);
 loginButton.addEventListener('click', updateMobileToggleVisibility);
 if (loginToRegisterBtn) {
   loginToRegisterBtn.addEventListener('click', updateMobileToggleVisibility);
 }
 if (registerToLoginBtn) {
   registerToLoginBtn.addEventListener('click', updateMobileToggleVisibility);
 }