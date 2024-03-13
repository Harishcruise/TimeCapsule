// carousel.js
let carouselState = {};

function showSlide(carouselId, slideIndex) {
  const carousel = document.getElementById(carouselId);
  if (!carousel) return; // Abort if the carousel element does not exist
  const slides = carousel.querySelectorAll('.carousel-item');
  if (!carouselState[carouselId]) {
    carouselState[carouselId] = 0;
  }
}