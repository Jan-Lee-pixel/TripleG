document.addEventListener('DOMContentLoaded', function() {
    // ===== DOM Elements =====
    const form = document.getElementById('projectForm');
    const coverInput = document.getElementById('cover');
    const galleryInput = document.getElementById('gallery');
    const coverPreview = document.getElementById('coverPreview');
    const galleryPreview = document.getElementById('galleryPreview');
    const milestoneList = document.getElementById('milestoneList');

    // ===== INIT =====
    init();

    function init() {
        setupEventListeners();
    }

    function setupEventListeners() {
        // Cover preview
        if (coverInput) {
            coverInput.addEventListener('change', () => handleImagePreview(coverInput.files, coverPreview, false));
        }

        // Gallery preview
        if (galleryInput) {
            galleryInput.addEventListener('change', () => handleImagePreview(galleryInput.files, galleryPreview, true));
        }

        // Form submit
        if (form) {
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                openModal("Publish Project", "<p>Your project was published (demo only, no backend).</p>", [
                    { text: "Close", action: closeModal }
                ]);
                form.reset();
                coverPreview.innerHTML = "";
                galleryPreview.innerHTML = "";
                milestoneList.innerHTML = "";
            });
        }
    }

    // ===== IMAGE PREVIEWS =====
    function handleImagePreview(files, previewContainer, multiple = true) {
        previewContainer.innerHTML = "";
        Array.from(files).forEach(file => {
            if (!file.type.startsWith("image/")) return;
            const reader = new FileReader();
            reader.onload = e => {
                const img = document.createElement("img");
                img.src = e.target.result;
                img.classList.add("preview-img");
                previewContainer.appendChild(img);
            };
            reader.readAsDataURL(file);
        });
    }

    // ===== MILESTONES =====
    window.addMilestone = function() {
        const id = Date.now();
        const item = document.createElement("div");
        item.className = "milestone-item";
        item.innerHTML = `
            <div class="milestone-header">
                <input type="text" placeholder="Milestone Title" class="milestone-title">
                <input type="date" class="milestone-date">
                <button type="button" class="btn btn-danger remove-milestone"><i class="fas fa-trash"></i></button>
            </div>
            <textarea class="milestone-desc" placeholder="Milestone description..."></textarea>
        `;
        milestoneList.appendChild(item);

        // Remove event
        item.querySelector(".remove-milestone").addEventListener("click", () => item.remove());
    };

    // ===== SAVE AS DRAFT =====
    window.saveAsDraft = function() {
        openModal("Save Draft", "<p>Your project draft was saved locally (demo only).</p>", [
            { text: "Close", action: closeModal }
        ]);
    };

    // ===== MODALS =====
    function openModal(title, body, actions) {
        const modal = document.getElementById("actionModal");
        const modalTitle = document.getElementById("modalTitle");
        const modalBody = document.getElementById("modalBody");
        const modalFooter = document.getElementById("modalFooter");

        modalTitle.textContent = title;
        modalBody.innerHTML = body;
        modalFooter.innerHTML = "";

        actions.forEach(btn => {
            const button = document.createElement("button");
            button.textContent = btn.text;
            button.className = "btn btn-primary";
            button.addEventListener("click", btn.action);
            modalFooter.appendChild(button);
        });

        modal.style.display = "block";
    }

    window.closeModal = function() {
        const modal = document.getElementById("actionModal");
        modal.style.display = "none";
    };

    // Close modal on outside click
    window.onclick = function(event) {
        const modal = document.getElementById("actionModal");
        if (event.target === modal) modal.style.display = "none";
    };
});
