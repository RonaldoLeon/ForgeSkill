document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registerForm');
    const inputs = document.querySelectorAll('input[required]');
    const passwordToggle = document.getElementById('passwordToggle');
    const passwordInput = document.getElementById('password');
    const submitBtn = form.querySelector('.submit-btn');
    
    // Animación de entrada para los elementos del formulario
    const formElements = document.querySelectorAll('.form-group, .checkbox-group, .submit-btn, .social-buttons');
    formElements.forEach((element, index) => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.animation = `slideUp 0.6s ease forwards ${index * 0.1}s`;
    });
    
    // Crear animación keyframes dinámicamente
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideUp {
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    `;
    document.head.appendChild(style);
    
    // Toggle de contraseña
    let passwordVisible = false;
    passwordToggle.addEventListener('click', function() {
        passwordVisible = !passwordVisible;
        passwordInput.type = passwordVisible ? 'text' : 'password';
        this.querySelector('.eye-icon').textContent = passwordVisible ? '🙈' : '👁️';
        
        // Animación del botón
        this.style.transform = 'scale(0.9)';
        setTimeout(() => {
            this.style.transform = 'scale(1)';
        }, 150);
    });
    
    // Validación en tiempo real
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            validateField(this);
            updateSubmitButton();
        });
        
        input.addEventListener('blur', function() {
            validateField(this);
        });
    });
    
    // Validación del formulario
    function validateField(field) {
        const container = field.closest('.input-container');
        let isValid = true;
        let errorMessage = '';
        
        // Remover errores previos
        removeError(container);
        
        if (field.type === 'email') {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(field.value)) {
                isValid = false;
                errorMessage = 'Ingresa un correo electrónico válido';
            }
        }
        
        if (field.name === 'password') {
            if (field.value.length < 6) {
                isValid = false;
                errorMessage = 'La contraseña debe tener al menos 6 caracteres';
            }
        }
        
        if (field.name === 'confirmPassword') {
            const passwordValue = document.getElementById('password').value;
            if (field.value !== passwordValue) {
                isValid = false;
                errorMessage = 'Las contraseñas no coinciden';
            }
        }
        
        if (field.hasAttribute('required') && !field.value.trim()) {
            isValid = false;
            errorMessage = 'Este campo es obligatorio';
        }
        
        if (!isValid && field.value) {
            showError(container, errorMessage);
        }
        
        return isValid;
    }
    
    function showError(container, message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        errorDiv.style.color = '#ff4444';
        errorDiv.style.fontSize = '12px';
        errorDiv.style.marginTop = '5px';
        errorDiv.style.opacity = '0';
        errorDiv.style.transform = 'translateY(-10px)';
        
        container.appendChild(errorDiv);
        
        // Animación de entrada del error
        setTimeout(() => {
            errorDiv.style.opacity = '1';
            errorDiv.style.transform = 'translateY(0)';
            errorDiv.style.transition = 'all 0.3s ease';
        }, 10);
        
        // Cambiar color del borde
        const input = container.querySelector('input');
        input.style.borderBottomColor = '#ff4444';
    }
    
    function removeError(container) {
        const errorMessage = container.querySelector('.error-message');
        if (errorMessage) {
            errorMessage.style.opacity = '0';
            setTimeout(() => {
                errorMessage.remove();
            }, 300);
        }
        
        const input = container.querySelector('input');
        input.style.borderBottomColor = '';
    }
    
    function updateSubmitButton() {
        const allValid = Array.from(inputs).every(input => {
            return input.value.trim() && validateField(input);
        });
        
        const termsChecked = document.getElementById('terms').checked;
        
        if (allValid && termsChecked) {
            submitBtn.style.background = 'linear-gradient(135deg, #00BCD4, #17293f)';
            submitBtn.disabled = false;
        } else {
            submitBtn.style.background = 'linear-gradient(135deg, #ccc, #999)';
            submitBtn.disabled = true;
        }
    }
    
    // Manejar envío del formulario
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Validar todos los campos
        let allValid = true;
        inputs.forEach(input => {
            if (!validateField(input)) {
                allValid = false;
            }
        });
        
        if (!document.getElementById('terms').checked) {
            alert('Debes aceptar los términos y condiciones');
            return;
        }
        
        if (allValid) {
            // Mostrar loading
            submitBtn.classList.add('loading');
            submitBtn.disabled = true;
            
            // Simular envío del formulario
            setTimeout(() => {
                submitBtn.classList.remove('loading');
                submitBtn.disabled = false;
                
                // Animación de éxito
                showSuccessMessage();
            }, 2000);
        }
    });
    
    function showSuccessMessage() {
        const successDiv = document.createElement('div');
        successDiv.innerHTML = `
            <div style="
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: linear-gradient(135deg, #00BCD4, #17293f);
                color: white;
                padding: 20px 30px;
                border-radius: 12px;
                box-shadow: 0 20px 40px rgba(0, 188, 212, 0.3);
                z-index: 1000;
                animation: successPop 0.5s ease;
            ">
                <h3 style="margin: 0 0 10px 0;">¡Registro exitoso! 🎉</h3>
                <p style="margin: 0; opacity: 0.9;">Tu cuenta ha sido creada correctamente</p>
            </div>
        `;
        
        const successStyle = document.createElement('style');
        successStyle.textContent = `
            @keyframes successPop {
                0% { transform: translate(-50%, -50%) scale(0.5); opacity: 0; }
                100% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
            }
        `;
        document.head.appendChild(successStyle);
        document.body.appendChild(successDiv);
        
        setTimeout(() => {
            successDiv.style.opacity = '0';
            setTimeout(() => {
                successDiv.remove();
                successStyle.remove();
            }, 300);
        }, 3000);
    }
    
    // Efectos de hover para botones sociales
    const socialBtns = document.querySelectorAll('.social-btn');
    socialBtns.forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px) scale(1.02)';
        });
        
        btn.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
        
        btn.addEventListener('click', function() {
            // Efecto de ripple
            const ripple = document.createElement('div');
            ripple.style.position = 'absolute';
            ripple.style.borderRadius = '50%';
            ripple.style.background = 'rgba(0, 188, 212, 0.3)';
            ripple.style.transform = 'scale(0)';
            ripple.style.animation = 'ripple 0.6s linear';
            ripple.style.left = '50%';
            ripple.style.top = '50%';
            ripple.style.width = '100px';
            ripple.style.height = '100px';
            ripple.style.marginLeft = '-50px';
            ripple.style.marginTop = '-50px';
            
            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
    
    // Añadir animación de ripple
    const rippleStyle = document.createElement('style');
    rippleStyle.textContent = `
        @keyframes ripple {
            to {
                transform: scale(2);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(rippleStyle);
    
    // Efecto parallax sutil en las formas de fondo
    document.addEventListener('mousemove', function(e) {
        const shapes = document.querySelectorAll('.shape');
        const mouseX = e.clientX / window.innerWidth;
        const mouseY = e.clientY / window.innerHeight;
        
        shapes.forEach((shape, index) => {
            const speed = 0.5 + (index * 0.2);
            const x = (mouseX - 0.5) * speed * 20;
            const y = (mouseY - 0.5) * speed * 20;
            
            shape.style.transform = `translate(${x}px, ${y}px)`;
        });
    });
});