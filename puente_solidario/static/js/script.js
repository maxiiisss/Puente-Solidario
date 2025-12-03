document.addEventListener('DOMContentLoaded', function () {

    // Funcionalidad de los botones de pregunta
    const questionBtns = document.querySelectorAll('.question-btn');
    const questionContents = document.querySelectorAll('.question-content');

    questionBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            const targetQuestion = this.getAttribute('data-question');

            // Remueve las clases activas de todos los botones
            questionBtns.forEach(b => b.classList.remove('active'));
            questionContents.forEach(c => c.classList.remove('active'));

            // Agrega clases activas al clickear el boton para el contenido que corresponde
            this.classList.add('active');
            document.getElementById(targetQuestion).classList.add('active');
        });
    });

    // Funcionalidad de la seccion preguntas frecuentes
    const faqQuestions = document.querySelectorAll('.faq-question');

    faqQuestions.forEach(question => {
        question.addEventListener('click', function () {
            const answer = this.nextElementSibling;
            const isActive = answer.classList.contains('active');

            // Cierra todas las preguntas frecuentes
            document.querySelectorAll('.faq-answer').forEach(ans => {
                ans.classList.remove('active');
            });

            // Activa las respuestas
            if (!isActive) {
                answer.classList.add('active');
            }
        });
    });

    // Funcionalidad de los cards de navegacion
    const navCards = document.querySelectorAll('.nav-card');

    navCards.forEach(card => {
        card.addEventListener('click', function () {
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'translateY(-5px)';
            }, 150);
            
        });
    });

    // Scroll suave para enlaces internos (si se agregan más tarde)
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Anima los datos de dinero de la parte inferior al momento de bajar hasta la seccion
    const observerOptions = {
        threshold: 0.5,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateNumbers(entry.target);
            }
        });
    }, observerOptions);

    // Observa los datos financieros
    const statNumbers = document.querySelectorAll('.stat-number');
    statNumbers.forEach(stat => {
        observer.observe(stat);
    });

    // Agrega animación de carga a los cards de navegación
    navCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';

        setTimeout(() => {
            card.style.transition = 'all 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
});



function animateNumbers(element) {
    const finalNumber = parseInt(element.textContent.replace(/[^0-9]/g, ''));
    const duration = 2000;
    const increment = finalNumber / (duration / 16);
    let current = 0;

    const timer = setInterval(() => {
        current += increment;
        if (current >= finalNumber) {
            current = finalNumber;
            clearInterval(timer);
        }

        element.textContent = '$' + Math.floor(current).toLocaleString();
    }, 16);
}

// Agrega algunas funciones interactivas
function addInteractiveFeatures() {
    // Agrega contador de clics para seguimiento de interacciones
    let clickCount = 0;

    document.addEventListener('click', function (e) {
        clickCount++;

        // Agrega efecto de onda a los botones
        if (e.target.tagName === 'BUTTON' || e.target.classList.contains('nav-card')) {
            createRipple(e);
        }
    });

    // Soporte de navegación por teclado
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Tab') {
            document.body.classList.add('keyboard-navigation');
        }
    });

    document.addEventListener('mousedown', function () {
        document.body.classList.remove('keyboard-navigation');
    });
}

function createRipple(event) {
    const button = event.currentTarget;
    const ripple = document.createElement('span');
    const rect = button.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;

    ripple.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        left: ${x}px;
        top: ${y}px;
        background: rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        transform: scale(0);
        animation: ripple 0.6s ease-out;
        pointer-events: none;
    `;

    // Agrega CSS de animación de onda si no existe
    if (!document.querySelector('#ripple-style')) {
        const style = document.createElement('style');
        style.id = 'ripple-style';
        style.textContent = `
            @keyframes ripple {
                to {
                    transform: scale(2);
                    opacity: 0;
                }
            }
            .nav-card, button {
                position: relative;
                overflow: hidden;
            }
        `;
        document.head.appendChild(style);
    }

    button.appendChild(ripple);

    setTimeout(() => {
        ripple.remove();
    }, 600);
}

// Inicializa las funciones interactivas
addInteractiveFeatures();