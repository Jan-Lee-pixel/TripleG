const registerButton = document.getElementById('register');
const loginButton = document.getElementById('login');       
const container = document.getElementById('container');

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

// --- Modal Logic ---
document.addEventListener('DOMContentLoaded', function() {
    const modalOverlay = document.getElementById('messageModal');
    if (!modalOverlay) return;

    const modalContent = modalOverlay.querySelector('.modal-content');
    const closeButton = modalOverlay.querySelector('.modal-close');

    // Function to show the modal
    function showModal() {
        modalOverlay.style.display = 'flex';
        setTimeout(() => {
            modalOverlay.style.opacity = '1';
            modalContent.style.transform = 'translateY(0)';
        }, 10);
    }

    // Function to hide the modal
    function hideModal() {
        modalOverlay.style.opacity = '0';
        modalContent.style.transform = 'translateY(-50px)';
        setTimeout(() => {
            modalOverlay.style.display = 'none';
        }, 300);
    }

    // Show the modal immediately if it exists in the DOM
    showModal();

    // Event listeners to close the modal
    closeButton.addEventListener('click', hideModal);
    modalOverlay.addEventListener('click', function(event) {
        if (event.target === modalOverlay) {
            hideModal();
        }
    });
});