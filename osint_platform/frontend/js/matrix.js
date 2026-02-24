/**
 * Matrix Rain Effect - Background Animation
 */
const canvas = document.getElementById('matrixCanvas');
const ctx = canvas.getContext('2d');

// Resize canvas
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Characters for matrix effect
const chars = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン';
const charArray = chars.split('');

const fontSize = 14;
const columns = canvas.width / fontSize;
const drops = [];

// Initialize drops
for (let i = 0; i < columns; i++) {
    drops[i] = Math.random() * -100;
}

// Draw matrix rain
function drawMatrix() {
    // Fade effect
    ctx.fillStyle = 'rgba(10, 14, 21, 0.05)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Matrix characters
    ctx.fillStyle = '#00ff41';
    ctx.font = fontSize + 'px monospace';
    
    for (let i = 0; i < drops.length; i++) {
        const char = charArray[Math.floor(Math.random() * charArray.length)];
        ctx.fillText(char, i * fontSize, drops[i] * fontSize);
        
        // Reset drop to top randomly
        if (drops[i] * fontSize > canvas.height && Math.random() > 0.95) {
            drops[i] = 0;
        }
        
        drops[i]++;
    }
}

// Animation loop
setInterval(drawMatrix, 35);

// Resize handler
window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});
