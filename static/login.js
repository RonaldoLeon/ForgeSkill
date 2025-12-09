const form = document.getElementById('loginForm');
const toggle = document.getElementById('togglePwd');
const pwd = document.getElementById('password');
const identifier = document.getElementById('identifier');
const btn = document.getElementById('btnSubmit');

// --- Mostrar / Ocultar contraseña ---
toggle.addEventListener('click', () => {
    const isPwd = pwd.type === 'password';
    pwd.type = isPwd ? 'text' : 'password';
    toggle.textContent = isPwd ? '🙈' : '👁️';
});

// --- Validación de formulario ---
form.addEventListener('submit', (e) => {
    const emailOrUsername = identifier.value.trim();
    const pass = pwd.value.trim();

    // Validar que sea email O username válido
    const isEmail = emailOrUsername.includes("@");
    const isUsername = emailOrUsername.length >= 3; // Aceptar cualquier cosa con 3+ caracteres

    if (!emailOrUsername || (!isEmail && !isUsername)) {
        e.preventDefault();
        alert("Introduce un correo o nombre de usuario válido.");
        return identifier.focus();
    }

    if (!pass || pass.length < 3) {
        e.preventDefault();
        alert("La contraseña es demasiado corta.");
        return pwd.focus();
    }

    // Si todo es válido, permitir que el formulario se envíe
    return true;
});