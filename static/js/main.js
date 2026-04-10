// ── Navbar scroll effect ──
window.addEventListener("scroll", function () {
  var navbar = document.getElementById("navbar");
  if (navbar) {
    if (window.scrollY > 40) {
      navbar.style.background = "rgba(6,10,18,0.98)";
    } else {
      navbar.style.background = "rgba(6,10,18,0.88)";
    }
  }
});

// ── Mobile hamburger menu ──
var hamburger = document.getElementById("hamburger");
if (hamburger) {
  hamburger.addEventListener("click", function () {
    var links = document.querySelector(".nav-links");
    if (links) links.classList.toggle("open");
  });
}

// ── Scroll reveal: fade-in sections as you scroll ──
function revealOnScroll() {
  var sections = document.querySelectorAll(".section, .page-hero");
  sections.forEach(function (el) {
    var rect = el.getBoundingClientRect();
    if (rect.top < window.innerHeight - 80) {
      el.classList.add("revealed");
    }
  });
}

// Add base style for reveal animation
var style = document.createElement("style");
style.textContent = [
  ".section, .page-hero { opacity: 0; transform: translateY(24px); transition: opacity 0.7s ease, transform 0.7s ease; }",
  ".section.revealed, .page-hero.revealed { opacity: 1; transform: none; }"
].join("");
document.head.appendChild(style);

window.addEventListener("scroll", revealOnScroll);
window.addEventListener("load", revealOnScroll);