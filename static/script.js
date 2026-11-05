
document.addEventListener("DOMContentLoaded", function () {

    // 1. MOBILE NAVIGATION MENU
    const menuButton = document.getElementById("menuButton");
    const navLinks = document.getElementById("navLinks");

    if (menuButton && navLinks) {
        menuButton.setAttribute("aria-expanded", "false");

        menuButton.addEventListener("click", function () {
            const isOpen = navLinks.classList.toggle("active");

            menuButton.setAttribute("aria-expanded", String(isOpen));
            menuButton.textContent = isOpen ? "✕" : "☰";
        });

        navLinks.querySelectorAll("a").forEach(function (link) {
            link.addEventListener("click", function () {
                navLinks.classList.remove("active");
                menuButton.setAttribute("aria-expanded", "false");
                menuButton.textContent = "☰";
            });
        });
    }


    // 2. SMOOTH SCROLLING FOR NAVIGATION LINKS
    document.querySelectorAll('a[href^="#"]').forEach(function (link) {
        link.addEventListener("click", function (event) {
            const targetId = link.getAttribute("href");

            if (!targetId || targetId === "#") return;

            const target = document.querySelector(targetId);

            if (target) {
                event.preventDefault();

                target.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });

                history.replaceState(null, "", targetId);

                if (navLinks && menuButton) {
                    navLinks.classList.remove("active");
                    menuButton.setAttribute("aria-expanded", "false");
                    menuButton.textContent = "☰";
                }
            }
        });
    });


    // 3. TYPING ANIMATION
    const typingText = document.getElementById("typingText");

    if (typingText) {
        const words = [
            "Python Developer",
            "Web Developer",
            "AI/ML Enthusiast",
            "Software Developer"
        ];

        let wordIndex = 0;
        let charIndex = 0;
        let deleting = false;

        function type() {
            const currentWord = words[wordIndex];

            if (deleting) {
                charIndex--;
            } else {
                charIndex++;
            }

            typingText.textContent = currentWord.substring(0, charIndex);

            let delay = deleting ? 55 : 100;

            if (!deleting && charIndex === currentWord.length) {
                deleting = true;
                delay = 1400;
            } else if (deleting && charIndex === 0) {
                deleting = false;
                wordIndex = (wordIndex + 1) % words.length;
                delay = 400;
            }

            setTimeout(type, delay);
        }

        type();
    }


    // 4. SCROLL REVEAL ANIMATION
    const revealElements = document.querySelectorAll(
        ".glass-card, .stat-card, .skill-card, .project-card, .ai-panel, .contact-banner"
    );

    if ("IntersectionObserver" in window) {
        const observer = new IntersectionObserver(
            function (entries, observer) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("visible");
                        observer.unobserve(entry.target);
                    }
                });
            },
            {
                threshold: 0.12
            }
        );

        revealElements.forEach(function (element) {
            element.classList.add("reveal");
            observer.observe(element);
        });
    } else {
        revealElements.forEach(function (element) {
            element.classList.add("visible");
        });
    }


    // 5. CLOSE MOBILE MENU WHEN CLICKING OUTSIDE
    document.addEventListener("click", function (event) {
        if (
            menuButton &&
            navLinks &&
            !menuButton.contains(event.target) &&
            !navLinks.contains(event.target)
        ) {
            navLinks.classList.remove("active");
            menuButton.setAttribute("aria-expanded", "false");
            menuButton.textContent = "☰";
        }
    });


    // 6. PREVENT EMPTY CONTACT FORM SUBMISSION
    const contactForm = document.querySelector(".contact-form");

    if (contactForm) {
        contactForm.addEventListener("submit", function (event) {
            const name = contactForm.querySelector('[name="name"]');
            const email = contactForm.querySelector('[name="email"]');
            const message = contactForm.querySelector('[name="message"]');

            if (
                !name || !email || !message ||
                !name.value.trim() ||
                !email.value.trim() ||
                !message.value.trim()
            ) {
                event.preventDefault();
                alert("Please fill in all contact form fields.");
            }
        });
    }

});
