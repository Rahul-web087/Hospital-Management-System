document.addEventListener("DOMContentLoaded", () => {

    document.addEventListener("DOMContentLoaded", function () {

    const sidebar = document.getElementById("sidebar");

    const toggle = document.getElementById("sidebarToggle");

    const content = document.querySelector(".main-content");

    if (toggle && sidebar) {

        toggle.addEventListener("click", function () {

            if (window.innerWidth <= 992) {

                sidebar.classList.toggle("active");

            } else {

                sidebar.classList.toggle("hide");

                if(content){
                    content.classList.toggle("expand");
                }

            }

        });

    }

});

    // Password Toggle
    const togglePassword = document.getElementById("togglePassword");
    const password = document.getElementById("password");

    if (togglePassword && password) {

        togglePassword.addEventListener("click", () => {

            const icon = togglePassword.querySelector("i");

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