document.addEventListener('DOMContentLoaded', function() {
    const diagnosticForm = document.getElementById('diagnosticForm');
    if (diagnosticForm) {
        diagnosticForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const problemType = document.getElementById('problemType').value;
            const problemTime = document.getElementById('problemTime').value;
            const symptoms = Array.from(document.querySelectorAll('input[name="symptoms"]:checked'))
                .map(cb => cb.value);
            const additionalInfo = document.getElementById('additionalInfo').value;

            const resultDiv = document.getElementById('diagnosticResult');
            const resultContent = document.getElementById('resultContent');
            
            let diagnosis = `На основе ваших ответов, возможные проблемы:\n`;
            
            switch(problemType) {
                case 'engine':
                    diagnosis += '- Рекомендуется комплексная диагностика двигателя\n';
                    break;
                case 'transmission':
                    diagnosis += '- Необходима проверка трансмиссии\n';
                    break;
                    case 'brakes':
                        diagnosis += '- Требуется диагностика тормозной системы\n';
                        break;
                    case 'suspension':
                        diagnosis += '- Рекомендуется проверка подвески\n';
                        break;
                    case 'electrical':
                        diagnosis += '- Необходима диагностика электрооборудования\n';
                        break;
                }
    
                if (symptoms.includes('noise')) {
                    diagnosis += '- Необходима проверка на наличие механических повреждений\n';
                }
                if (symptoms.includes('vibration')) {
                    diagnosis += '- Рекомендуется проверка балансировки и креплений\n';
                }
                if (symptoms.includes('smoke')) {
                    diagnosis += '- Срочная диагностика двигателя\n';
                }
                if (symptoms.includes('performance')) {
                    diagnosis += '- Комплексная диагностика двигателя и топливной системы\n';
                }
                if (symptoms.includes('warning')) {
                    diagnosis += '- Компьютерная диагностика\n';
                }
    
                resultContent.innerHTML = diagnosis.replace(/\n/g, '<br>');
                resultDiv.style.display = 'block';
                resultDiv.scrollIntoView({ behavior: 'smooth' });
            });
        }
    
        // Валидация формы записи
        const appointmentForm = document.querySelector('.appointment-form form');
        if (appointmentForm) {
            appointmentForm.addEventListener('submit', function(e) {
                const phone = document.querySelector('input[name="phone"]').value;
                const phoneRegex = /^\+?[0-9]{10,12}$/;
                
                if (!phoneRegex.test(phone)) {
                    e.preventDefault();
                    alert('Пожалуйста, введите корректный номер телефона');
                }
            });
        }
    
        // Анимация появления элементов при скролле
        const animateOnScroll = () => {
            const elements = document.querySelectorAll('.service-card, .master-card, .advantage-item');
            
            elements.forEach(element => {
                const elementTop = element.getBoundingClientRect().top;
                const elementBottom = element.getBoundingClientRect().bottom;
                
                if (elementTop < window.innerHeight && elementBottom > 0) {
                    element.classList.add('visible');
                }
            });
        };
    
        window.addEventListener('scroll', animateOnScroll);
        animateOnScroll();
    
        // Плавная прокрутка для навигации
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
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
    
        // Обработка сообщений
        const messages = document.querySelector('.messages');
        if (messages) {
            setTimeout(() => {
                messages.style.opacity = '0';
                setTimeout(() => {
                    messages.style.display = 'none';
                }, 600);
            }, 3000);
        }
    });