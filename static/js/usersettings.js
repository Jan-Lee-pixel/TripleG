document.addEventListener('DOMContentLoaded', function() {
  // Mobile menu functionality
  const mobileMenuBtn = document.getElementById('mobileMenuBtn');
  const navLinks = document.getElementById('navLinks');

  if (mobileMenuBtn && navLinks) {
    mobileMenuBtn.addEventListener('click', function() {
      navLinks.classList.toggle('active');
    });
  }

  // Settings menu navigation
  const menuItems = document.querySelectorAll('.settings-menu-item');
  const settingsSections = document.querySelectorAll('.settings-section');

  menuItems.forEach(item => {
    item.addEventListener('click', function() {
      // Remove active class from all menu items
      menuItems.forEach(i => i.classList.remove('active'));
      
      // Add active class to clicked item
      this.classList.add('active');
      
      // Hide all sections
      settingsSections.forEach(section => {
        section.classList.remove('active');
      });
      
      // Show selected section
      const sectionId = this.getAttribute('data-section');
      document.getElementById(sectionId).classList.add('active');
    });
  });

  // Load saved user data from localStorage
  loadUserData();

  // Profile Form handling
  const profileForm = document.getElementById('profileForm');
  const emailInput = document.getElementById('email');
  const emailError = document.getElementById('emailError');
  const phoneInput = document.getElementById('phone');
  const phoneError = document.getElementById('phoneError');
  const profileSuccess = document.getElementById('profileSuccess');

  if (profileForm) {
    // Email validation
    if (emailInput && emailError) {
      emailInput.addEventListener('input', function() {
        validateEmail(this);
      });
      
      emailInput.addEventListener('blur', function() {
        validateEmail(this);
      });
    }

    // Phone validation
    if (phoneInput && phoneError) {
      phoneInput.addEventListener('input', function() {
        validatePhone(this);
      });
      
      phoneInput.addEventListener('blur', function() {
        validatePhone(this);
      });
    }

    // Form submission
    profileForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      // Validate all fields
      let isValid = true;
      
      if (emailInput && !validateEmail(emailInput)) {
        isValid = false;
      }
      
      if (phoneInput && !validatePhone(phoneInput)) {
        isValid = false;
      }
      
      if (isValid) {
        // Save profile data
        saveProfileData();
        
        // Show success message
        if (profileSuccess) {
          profileSuccess.style.display = 'flex';
          setTimeout(() => {
            profileSuccess.style.display = 'none';
          }, 3000);
        }
      }
    });
  }

  // Notifications Form handling
  const notificationsForm = document.getElementById('notificationsForm');
  const notificationsSuccess = document.getElementById('notificationsSuccess');

  if (notificationsForm) {
    notificationsForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      // Save notification preferences
      saveNotificationPreferences();
      
      // Show success message
      if (notificationsSuccess) {
        notificationsSuccess.style.display = 'flex';
        setTimeout(() => {
          notificationsSuccess.style.display = 'none';
        }, 3000);
      }
    });
  }

  // Security Form handling
  const securityForm = document.getElementById('securityForm');
  const currentPasswordInput = document.getElementById('currentPassword');
  const newPasswordInput = document.getElementById('newPassword');
  const confirmPasswordInput = document.getElementById('confirmPassword');
  const passwordMatchError = document.getElementById('passwordMatchError');
  const strengthBar = document.getElementById('passwordStrength');
  const securitySuccess = document.getElementById('securitySuccess');

  if (securityForm) {
    // Password strength meter
    if (newPasswordInput && strengthBar) {
      newPasswordInput.addEventListener('input', function() {
        const password = this.value;
        updatePasswordStrength(password);
        
        // Check password match if confirm password has value
        if (confirmPasswordInput && confirmPasswordInput.value) {
          checkPasswordMatch();
        }
      });
    }

    // Password match validation
    if (confirmPasswordInput && passwordMatchError && newPasswordInput) {
      confirmPasswordInput.addEventListener('input', checkPasswordMatch);
      confirmPasswordInput.addEventListener('blur', checkPasswordMatch);
    }

    // Form submission
    securityForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      // Simple validation (in a real app you'd verify current password with backend)
      let isValid = true;
      
      if (!currentPasswordInput.value) {
        currentPasswordInput.setCustomValidity('Please enter your current password');
        isValid = false;
      } else {
        currentPasswordInput.setCustomValidity('');
      }
      
      if (newPasswordInput.value && !checkPasswordMatch()) {
        isValid = false;
      }
      
      if (isValid) {
        // In a real app, you would send data to server
        // For now, just show success message
        if (securitySuccess) {
          securitySuccess.style.display = 'flex';
          setTimeout(() => {
            securitySuccess.style.display = 'none';
          }, 3000);
          
          // Reset form
          securityForm.reset();
          strengthBar.style.width = '0';
        }
      }
    });
  }

  // Delete account modal
  const deleteAccountBtn = document.getElementById('deleteAccountBtn');
  const deleteModal = document.getElementById('deleteModal');
  const cancelDelete = document.getElementById('cancelDelete');
  const confirmDelete = document.getElementById('confirmDelete');
  const closeModal = document.querySelector('.close-modal');

  if (deleteAccountBtn && deleteModal) {
    deleteAccountBtn.addEventListener('click', function() {
      deleteModal.classList.add('active');
    });

    // Close modal functions
    const closeDeleteModal = function() {
      deleteModal.classList.remove('active');
    };

    if (cancelDelete) {
      cancelDelete.addEventListener('click', closeDeleteModal);
    }

    if (closeModal) {
      closeModal.addEventListener('click', closeDeleteModal);
    }

    // Outside click to close
    window.addEventListener('click', function(e) {
      if (e.target === deleteModal) {
        closeDeleteModal();
      }
    });

    // Confirm delete
    if (confirmDelete) {
      confirmDelete.addEventListener('click', function() {
        // In a real app, you would send delete request to server
        // For demo, just show alert and redirect
        alert('Account deletion request submitted. You will be logged out.');
        window.location.href = 'index.html';
      });
    }
  }

  // Logout button
  const logoutBtn = document.getElementById('logoutBtn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', function() {
      // In a real app, you would clear session data
      window.location.href = 'index.html';
    });
  }

  // Profile image upload
  const avatarUpload = document.getElementById('avatar-upload');
  const profileImage = document.getElementById('profileImage');
  const avatarOverlay = document.querySelector('.avatar-upload-overlay');

  if (avatarUpload && profileImage) {
    // Click on avatar or overlay opens file dialog
    if (avatarOverlay) {
      avatarOverlay.addEventListener('click', function() {
        avatarUpload.click();
      });
    }

    avatarUpload.addEventListener('change', function(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
          profileImage.src = e.target.result;
          
          // Save to localStorage
          localStorage.setItem('userProfileImage', e.target.result);
          
          // Update display name image as well
          const displayNameEl = document.getElementById('displayName');
          if (displayNameEl) {
            displayNameEl.textContent = document.getElementById('firstName').value + ' ' + 
                                       document.getElementById('lastName').value;
          }
        };
        reader.readAsDataURL(file);
      }
    });
  }

  // Validation functions
  function validateEmail(input) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const isValid = emailRegex.test(input.value);
    
    if (!isValid) {
      input.setCustomValidity('Please enter a valid email address');
      emailError.style.display = 'block';
      return false;
    } else {
      input.setCustomValidity('');
      emailError.style.display = 'none';
      return true;
    }
  }

  function validatePhone(input) {
    const phoneRegex = /^[\+]?[(]?[0-9]{1,3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/;
    const isValid = phoneRegex.test(input.value);
    
    if (!isValid) {
      input.setCustomValidity('Please enter a valid phone number');
      phoneError.style.display = 'block';
      return false;
    } else {
      input.setCustomValidity('');
      phoneError.style.display = 'none';
      return true;
    }
  }

  function checkPasswordMatch() {
    const newPassword = newPasswordInput.value;
    const confirmPassword = confirmPasswordInput.value;
    
    if (newPassword !== confirmPassword) {
      confirmPasswordInput.setCustomValidity('Passwords do not match');
      passwordMatchError.style.display = 'block';
      return false;
    } else {
      confirmPasswordInput.setCustomValidity('');
      passwordMatchError.style.display = 'none';
      return true;
    }
  }

  function updatePasswordStrength(password) {
    let strength = 0;
    
    if (password.length >= 8) strength += 20;
    if (password.match(/[a-z]+/)) strength += 20;
    if (password.match(/[A-Z]+/)) strength += 20;
    if (password.match(/[0-9]+/)) strength += 20;
    if (password.match(/[^a-zA-Z0-9]+/)) strength += 20;
    
    strengthBar.style.width = strength + '%';
    
    if (strength < 40) {
      strengthBar.style.backgroundColor = '#F44336'; // Danger
    } else if (strength < 70) {
      strengthBar.style.backgroundColor = '#FF9800'; // Warning
    } else {
      strengthBar.style.backgroundColor = '#4CAF50'; // Success
    }
  }

  // Save data functions
  function saveProfileData() {
    const userData = {
      firstName: document.getElementById('firstName').value,
      lastName: document.getElementById('lastName').value,
      email: document.getElementById('email').value,
      phone: document.getElementById('phone').value,
    };
    
    localStorage.setItem('userData', JSON.stringify(userData));
    
    // Update display elements
    updateDisplayElements(userData);
  }

  function saveNotificationPreferences() {
    const notificationPrefs = {
      emailNotifications: document.getElementById('emailNotifications').checked,
      smsNotifications: document.getElementById('smsNotifications').checked,
      milestoneNotifications: document.getElementById('milestoneNotifications').checked,
      newsletterNotifications: document.getElementById('newsletterNotifications').checked,
      frequency: document.getElementById('notificationFrequency').value
    };
    
    localStorage.setItem('notificationPrefs', JSON.stringify(notificationPrefs));
  }

  // Load saved data from localStorage
  function loadUserData() {
    // Load profile data
    const savedUserData = localStorage.getItem('userData');
    if (savedUserData) {
      const userData = JSON.parse(savedUserData);
      
      if (document.getElementById('firstName')) document.getElementById('firstName').value = userData.firstName || '';
      if (document.getElementById('lastName')) document.getElementById('lastName').value = userData.lastName || '';
      if (document.getElementById('email')) document.getElementById('email').value = userData.email || '';
      if (document.getElementById('phone')) document.getElementById('phone').value = userData.phone || '';
      
      // Update display elements
      updateDisplayElements(userData);
    }
    
    // Load profile image
    const savedProfileImage = localStorage.getItem('userProfileImage');
    if (savedProfileImage && document.getElementById('profileImage')) {
      document.getElementById('profileImage').src = savedProfileImage;
    }
    
    // Load notification preferences
    const savedNotificationPrefs = localStorage.getItem('notificationPrefs');
    if (savedNotificationPrefs) {
      const prefs = JSON.parse(savedNotificationPrefs);
      
      if (document.getElementById('emailNotifications')) 
        document.getElementById('emailNotifications').checked = prefs.emailNotifications;
      if (document.getElementById('smsNotifications')) 
        document.getElementById('smsNotifications').checked = prefs.smsNotifications;
      if (document.getElementById('milestoneNotifications')) 
        document.getElementById('milestoneNotifications').checked = prefs.milestoneNotifications;
      if (document.getElementById('newsletterNotifications')) 
        document.getElementById('newsletterNotifications').checked = prefs.newsletterNotifications;
      if (document.getElementById('notificationFrequency')) 
        document.getElementById('notificationFrequency').value = prefs.frequency;
    }
  }

  function updateDisplayElements(userData) {
    // Update display name and email
    const displayName = document.getElementById('displayName');
    const displayEmail = document.getElementById('displayEmail');
    
    if (displayName && userData.firstName && userData.lastName) {
      displayName.textContent = userData.firstName + ' ' + userData.lastName;
    }
    
    if (displayEmail && userData.email) {
      displayEmail.textContent = userData.email;
    }
  }
});
