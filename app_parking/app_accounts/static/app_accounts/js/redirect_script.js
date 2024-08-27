document.addEventListener("DOMContentLoaded", function () {
    if (shouldRedirect) {
        document.getElementById("signup-title").style.display = "none";
        document.getElementById("agreement-text").style.display = "none";
        document.getElementById("login-redirect").style.display = "none";
        document.getElementById("register-now").style.display = "none";
        document.getElementById("close-btn").style.display = "none";
        var inputGroups = document.querySelectorAll(".input-group");
        inputGroups.forEach(function (inputGroup) {
            inputGroup.style.display = "none";
        });

        var messages = document.getElementById("messages-django");
        messages.style.display = "block";

        setTimeout(function () {
            window.location.href = redirectUrl;
        }, 3000);
    }
});