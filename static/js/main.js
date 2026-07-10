document.addEventListener("DOMContentLoaded", function () {

    const togglePassword = document.getElementById("togglePassword");

    if (togglePassword) {

        togglePassword.addEventListener("click", function () {

            const password = document.getElementById("password");

            const icon = this.querySelector("i");

            if (password.type === "password") {

                password.type = "text";
                icon.classList.remove("fa-eye");
                icon.classList.add("fa-eye-slash");

            } else {

                password.type = "password";
                icon.classList.remove("fa-eye-slash");
                icon.classList.add("fa-eye");

            }

        });

    }

});




document.addEventListener("DOMContentLoaded", function () {

    const sidebar = document.getElementById("sidebar");
    const toggle = document.getElementById("sidebarToggle");

    if (toggle) {

        toggle.addEventListener("click", function () {

            sidebar.classList.toggle("active");

        });

    }

    const togglePassword = document.getElementById("togglePassword");

    if (togglePassword) {

        togglePassword.addEventListener("click", function () {

            const password = document.getElementById("password");
            const icon = this.querySelector("i");

            if (password.type === "password") {

                password.type = "text";
                icon.classList.replace("fa-eye", "fa-eye-slash");

            } else {

                password.type = "password";
                icon.classList.replace("fa-eye-slash", "fa-eye");

            }

        });

    }

});