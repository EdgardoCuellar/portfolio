import React, { useEffect, useRef } from 'react';

const StarsBackground = () => {
  const canvasRef = useRef(null);
  
  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const width = canvas.width = canvas.offsetWidth;
    const height = canvas.height = canvas.offsetHeight;
    
    // Créer des étoiles
    const stars = [];
    const starCount = 150;
    
    for (let i = 0; i < starCount; i++) {
      stars.push({
        x: Math.random() * width,
        y: Math.random() * height,
        radius: Math.random() * 1.2,
        speedX: Math.random() * 0.6 - 0.2, // Vitesse aléatoire pour un mouvement horizontal
        speedY: Math.random() * 0.6 - 0.2, // Vitesse aléatoire pour un mouvement vertical
        opacity: Math.random() * 0.8 + 0.2
      });
    }
    
    let animationFrameId;
    
    const render = () => {
      ctx.clearRect(0, 0, width, height);
      
      stars.forEach(star => {
        // Déplacer légèrement les étoiles
        star.x += star.speedX;
        star.y += star.speedY;
        if (star.x > width) star.x = 0;
        if (star.x < 0) star.x = width;
        if (star.y > height) star.y = 0;
        if (star.y < 0) star.y = height;
        
        // Calculer l'opacité en fonction de la position y
        const opacity = Math.max(0, star.opacity * (1 - (star.y / height) * 1));
        
        ctx.beginPath();
        ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255, 255, 255, ${opacity})`;
        ctx.fill();
      });
      
      animationFrameId = requestAnimationFrame(render);
    };
    
    render();
    
    return () => {
      cancelAnimationFrame(animationFrameId);
    };
  }, []);
  
  return (
    <canvas 
      ref={canvasRef} 
      className="absolute inset-0 top-0 left-0 w-full h-full z-0 pointer-events-none"
    />
  );
};

export default StarsBackground;