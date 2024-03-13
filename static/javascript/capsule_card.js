// carousel.js
let carouselState = {};

function showSlide(carouselId, slideIndex) {
  const carousel = document.getElementById(carouselId);
  if (!carousel) return; // Abort if the carousel element does not exist
  const slides = carousel.querySelectorAll('.carousel-item');
  if (!carouselState[carouselId]) {
    carouselState[carouselId] = 0;
  }
  carouselState[carouselId] = slideIndex;
  if (carouselState[carouselId] >= slides.length) {
    carouselState[carouselId] = 0;
  }
  if (carouselState[carouselId] < 0) {
    carouselState[carouselId] = slides.length - 1;
  }
  for (let i = 0; i < slides.length; i++) {
    slides[i].style.display = 'none';
  }
  slides[carouselState[carouselId]].style.display = 'block';
}

function nextSlide(carouselId) {
  showSlide(carouselId, carouselState[carouselId] + 1);
}

function prevSlide(carouselId) {
  showSlide(carouselId, carouselState[carouselId] - 1);
}