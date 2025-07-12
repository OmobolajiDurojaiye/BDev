"use strict";

class InteractivePortfolio {
  constructor() {
    this.canvas = document.getElementById("constellation-canvas");
    this.ctx = this.canvas.getContext("2d");
    this.nodes = [];
    this.mouse = { x: undefined, y: undefined };
    this.config = {
      nodeCount: 80,
      nodeColor: "rgba(0, 229, 255, 0.8)", // --cyber-teal
      lineColor: "rgba(0, 229, 255, 0.1)",
      nodeRadius: 2,
      maxDistance: 120,
    };
    this.codeBlock = document.querySelector(".code-block");

    // NEW: Elements for mobile navigation
    this.hamburgerButton = document.getElementById("hamburger-button");
    this.mobileNav = document.getElementById("mobile-nav");

    this.init();
  }

  init() {
    this.setupCanvas();
    this.createNodes();
    this.bindEvents();
    this.animate();
    this.initTypingAnimation();
    this.initConsoleMessage();
    this.initMobileMenu(); // NEW: Initialize mobile menu logic
  }

  setupCanvas() {
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
  }

  createNodes() {
    for (let i = 0; i < this.config.nodeCount; i++) {
      this.nodes.push({
        x: Math.random() * this.canvas.width,
        y: Math.random() * this.canvas.height,
        vx: Math.random() * 0.4 - 0.2,
        vy: Math.random() * 0.4 - 0.2,
        radius: Math.random() * 1.5 + 1,
      });
    }
  }

  drawNodes() {
    this.nodes.forEach((node) => {
      this.ctx.beginPath();
      this.ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
      this.ctx.fillStyle = this.config.nodeColor;

      // Add glow near mouse
      const distToMouse = Math.hypot(
        this.mouse.x - node.x,
        this.mouse.y - node.y
      );
      if (distToMouse < 150) {
        this.ctx.fillStyle = "rgba(255, 255, 255, 0.9)";
        node.radius = 3;
      } else {
        node.radius = Math.max(1, node.radius - 0.05);
      }

      this.ctx.fill();
    });
  }

  drawLines() {
    for (let i = 0; i < this.nodes.length; i++) {
      for (let j = i + 1; j < this.nodes.length; j++) {
        const dist = Math.hypot(
          this.nodes[i].x - this.nodes[j].x,
          this.nodes[i].y - this.nodes[j].y
        );
        if (dist < this.config.maxDistance) {
          this.ctx.beginPath();
          this.ctx.moveTo(this.nodes[i].x, this.nodes[i].y);
          this.ctx.lineTo(this.nodes[j].x, this.nodes[j].y);
          this.ctx.strokeStyle = `rgba(0, 229, 255, ${
            1 - dist / this.config.maxDistance
          })`;
          this.ctx.lineWidth = 0.5;
          this.ctx.stroke();
        }
      }
    }
  }

  updateNodes() {
    this.nodes.forEach((node) => {
      node.x += node.vx;
      node.y += node.vy;

      if (node.x < 0 || node.x > this.canvas.width) node.vx *= -1;
      if (node.y < 0 || node.y > this.canvas.height) node.vy *= -1;
    });
  }

  animate() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    this.updateNodes();
    this.drawLines();
    this.drawNodes();
    requestAnimationFrame(this.animate.bind(this));
  }

  handleMouseMove(e) {
    this.mouse.x = e.clientX;
    this.mouse.y = e.clientY;

    // 3D tilt effect on code block
    if (this.codeBlock) {
      const rect = this.codeBlock.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const rotateY = -1 * ((x - rect.width / 2) / (rect.width / 2)) * 8; // Max 8 deg rotation
      const rotateX = ((y - rect.height / 2) / (rect.height / 2)) * 8;

      this.codeBlock.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.03)`;
      this.codeBlock.style.boxShadow = `0 40px 60px -20px rgba(0,0,0,0.4)`;
    }
  }

  handleMouseLeave() {
    if (this.codeBlock) {
      this.codeBlock.style.transform = "rotateX(0deg) rotateY(0deg) scale(1)";
      this.codeBlock.style.boxShadow = `0 25px 50px rgba(0, 0, 0, 0.3)`;
    }
  }

  bindEvents() {
    window.addEventListener("resize", () => this.setupCanvas());
    document.addEventListener("mousemove", (e) => this.handleMouseMove(e));
    if (this.codeBlock) {
      const container = document.querySelector(".code-block-container");
      container.addEventListener("mouseleave", () => this.handleMouseLeave());
    }
  }

  // NEW: Method to handle mobile menu functionality
  initMobileMenu() {
    if (!this.hamburgerButton || !this.mobileNav) return;

    // Toggle menu on hamburger click
    this.hamburgerButton.addEventListener("click", () => {
      this.hamburgerButton.classList.toggle("is-active");
      this.mobileNav.classList.toggle("is-active");
      document.body.classList.toggle("no-scroll");
    });

    // Close menu when a link inside it is clicked
    const mobileLinks = this.mobileNav.querySelectorAll("a");
    mobileLinks.forEach((link) => {
      link.addEventListener("click", () => {
        if (this.mobileNav.classList.contains("is-active")) {
          this.hamburgerButton.classList.remove("is-active");
          this.mobileNav.classList.remove("is-active");
          document.body.classList.remove("no-scroll");
        }
      });
    });
  }

  initTypingAnimation() {
    const typingLine = document.querySelector(".typing-line");
    if (!typingLine) return;

    const fullText = typingLine.textContent.replace("|", "").trim();
    const lineContent = typingLine.querySelector(".string");
    const cursor = typingLine.querySelector(".cursor");
    if (!lineContent || !cursor) return;

    lineContent.textContent = '""';
    let i = 0;

    setTimeout(() => {
      const typeInterval = setInterval(() => {
        if (i < fullText.length) {
          lineContent.textContent = `"${fullText.substring(0, i + 1)}"`;
          i++;
        } else {
          clearInterval(typeInterval);
        }
      }, 100);
    }, 2000); // Start typing after 2 seconds
  }

  initConsoleMessage() {
    console.log(
      `%cBolaji | Developer, Dreamer, Builder\n%cWelcome to my universe. Feel free to explore the source.`,
      "font-family: monospace; font-size: 20px; color: #00e5ff;",
      "font-family: sans-serif; font-size: 14px; color: #e0e0e0;"
    );
  }
}

document.addEventListener("DOMContentLoaded", () => {
  new InteractivePortfolio();
});
