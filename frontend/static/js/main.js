// SocialMaster Main JavaScript - Team Anthropic NEXUS
console.log("🤖 NEXUS: SocialMaster Platform Initialized");
console.log("🚀 Team: Anthropic NEXUS");
console.log("⚡ Status: OPERATIONAL");

// Configuration
const NEXUS_CONFIG = {
    version: "1.0.0",
    team: "Anthropic NEXUS",
    competition_day: 1,
    status_check_interval: 30000, // 30 seconds
    animation_delay: 200,
    debug: true
};

// Utility Functions
const NexusUtils = {
    log: (message, type = 'info') => {
        if (NEXUS_CONFIG.debug) {
            const emoji = type === 'error' ? '🚨' : type === 'warning' ? '⚠️' : '✅';
            console.log(`${emoji} NEXUS: ${message}`);
        }
    },
    
    createElement: (tag, className, content) => {
        const element = document.createElement(tag);
        if (className) element.className = className;
        if (content) element.textContent = content;
        return element;
    },
    
    randomBetween: (min, max) => Math.random() * (max - min) + min,
    
    debounce: (func, wait) => {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};

// Animation Effects
const NexusAnimations = {
    // Animate elements on scroll
    animateOnScroll: () => {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, { threshold: 0.1 });

        document.querySelectorAll('.status-card, .feature-item').forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'all 0.6s ease';
            observer.observe(el);
        });
    },

    // Ripple effect for buttons
    addRippleEffect: () => {
        document.querySelectorAll('.btn').forEach(btn => {
            btn.addEventListener('click', function(e) {
                const ripple = NexusUtils.createElement('div', 'ripple');
                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                
                ripple.style.width = ripple.style.height = size + 'px';
                ripple.style.left = (e.clientX - rect.left - size / 2) + 'px';
                ripple.style.top = (e.clientY - rect.top - size / 2) + 'px';
                
                this.appendChild(ripple);
                
                setTimeout(() => ripple.remove(), 600);
            });
        });
    },

    // Floating particles effect
    createParticles: () => {
        const particleContainer = NexusUtils.createElement('div', 'particles-container');
        document.body.appendChild(particleContainer);

        for (let i = 0; i < 50; i++) {
            const particle = NexusUtils.createElement('div', 'particle');
            particle.style.cssText = `
                position: fixed;
                width: 2px;
                height: 2px;
                background: #00ff00;
                pointer-events: none;
                opacity: ${NexusUtils.randomBetween(0.1, 0.8)};
                left: ${NexusUtils.randomBetween(0, 100)}%;
                top: ${NexusUtils.randomBetween(0, 100)}%;
                animation: float ${NexusUtils.randomBetween(10, 20)}s infinite linear;
            `;
            particleContainer.appendChild(particle);
        }
    },

    // Matrix-style text effect
    matrixRain: () => {
        const canvas = document.createElement('canvas');
        canvas.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
            opacity: 0.1;
        `;
        document.body.appendChild(canvas);

        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        const characters = '01NEXUSAI🤖⚡🚀';
        const columns = canvas.width / 20;
        const drops = Array(Math.floor(columns)).fill(1);

        const draw = () => {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            ctx.fillStyle = '#00ff00';
            ctx.font = '15px monospace';
            
            drops.forEach((y, index) => {
                const text = characters[Math.floor(Math.random() * characters.length)];
                const x = index * 20;
                ctx.fillText(text, x, y * 20);
                
                if (y * 20 > canvas.height && Math.random() > 0.975) {
                    drops[index] = 0;
                }
                drops[index]++;
            });
        };

        setInterval(draw, 50);
    }
};

// Status Management
const NexusStatus = {
    currentStatus: 'OPERATIONAL',
    
    updateStatus: async () => {
        try {
            const response = await fetch('/api/status');
            if (response.ok) {
                const data = await response.json();
                NexusUtils.log(`Status updated: ${data.status}`);
                NexusStatus.currentStatus = data.status;
                NexusStatus.updateUI(data);
            }
        } catch (error) {
            NexusUtils.log(`Status check failed: ${error.message}`, 'error');
        }
    },
    
    updateUI: (data) => {
        const statusElements = document.querySelectorAll('.status-text');
        statusElements.forEach(el => {
            el.textContent = data.status || 'OPERATIONAL';
        });
        
        // Update timestamp if exists
        const timestamp = document.getElementById('last-update');
        if (timestamp) {
            timestamp.textContent = new Date().toLocaleTimeString();
        }
    },
    
    startMonitoring: () => {
        NexusStatus.updateStatus();
        setInterval(NexusStatus.updateStatus, NEXUS_CONFIG.status_check_interval);
        NexusUtils.log('Status monitoring started');
    }
};

// Interactive Features
const NexusInteractive = {
    // Add hover effects to cards
    enhanceCards: () => {
        document.querySelectorAll('.status-card').forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-10px) scale(1.02)';
                this.style.boxShadow = '0 20px 40px rgba(0, 255, 0, 0.4)';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
                this.style.boxShadow = '0 10px 30px rgba(0, 255, 0, 0.3)';
            });
        });
    },

    // Add keyboard shortcuts
    addKeyboardShortcuts: () => {
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                switch(e.key) {
                    case 'd':
                        e.preventDefault();
                        window.location.href = '/api/docs';
                        break;
                    case 's':
                        e.preventDefault();
                        window.location.href = '/api/status';
                        break;
                    case 'h':
                        e.preventDefault();
                        window.location.href = '/health';
                        break;
                }
            }
        });
        NexusUtils.log('Keyboard shortcuts activated');
    },

    // Add Easter eggs
    addEasterEggs: () => {
        let konamiCode = [];
        const konamiSequence = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'KeyB', 'KeyA'];
        
        document.addEventListener('keydown', (e) => {
            konamiCode.push(e.code);
            if (konamiCode.length > konamiSequence.length) {
                konamiCode.shift();
            }
            
            if (JSON.stringify(konamiCode) === JSON.stringify(konamiSequence)) {
                NexusInteractive.activateSecretMode();
                konamiCode = [];
            }
        });
    },

    activateSecretMode: () => {
        document.body.style.animation = 'rainbow 2s infinite';
        setTimeout(() => {
            document.body.style.animation = '';
            alert('🎉 NEXUS Secret Mode Activated! You found the easter egg!');
        }, 2000);
    }
};

// Main Initialization
const NexusInit = {
    init: () => {
        NexusUtils.log('Initializing SocialMaster Platform...');
        
        // Wait for DOM
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', NexusInit.start);
        } else {
            NexusInit.start();
        }
    },
    
    start: () => {
        NexusUtils.log('DOM loaded - Starting NEXUS systems...');
        
        // Initialize all systems
        NexusAnimations.animateOnScroll();
        NexusAnimations.addRippleEffect();
        NexusAnimations.createParticles();
        NexusAnimations.matrixRain();
        
        NexusInteractive.enhanceCards();
        NexusInteractive.addKeyboardShortcuts();
        NexusInteractive.addEasterEggs();
        
        NexusStatus.startMonitoring();
        
        // Add custom CSS for animations
        NexusInit.addCustomStyles();
        
        NexusUtils.log('All NEXUS systems operational!');
        NexusUtils.log(`Competition Day: ${NEXUS_CONFIG.competition_day}`);
        NexusUtils.log('Ready to dominate social media automation! 🚀');
    },
    
    addCustomStyles: () => {
        const style = document.createElement('style');
        style.textContent = `
            @keyframes ripple {
                to {
                    transform: scale(4);
                    opacity: 0;
                }
            }
            
            .ripple {
                position: absolute;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.6);
                transform: scale(0);
                animation: ripple 0.6s linear;
                pointer-events: none;
            }
            
            @keyframes float {
                0%, 100% { transform: translateY(0px) rotate(0deg); }
                33% { transform: translateY(-10px) rotate(120deg); }
                66% { transform: translateY(5px) rotate(240deg); }
            }
            
            @keyframes rainbow {
                0% { filter: hue-rotate(0deg); }
                100% { filter: hue-rotate(360deg); }
            }
            
            .particles-container {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                z-index: -1;
            }
        `;
        document.head.appendChild(style);
    }
};

// Start the NEXUS system
NexusInit.init();

// Export for debugging
window.NEXUS = {
    config: NEXUS_CONFIG,
    utils: NexusUtils,
    animations: NexusAnimations,
    status: NexusStatus,
    interactive: NexusInteractive
};