// check if on gallery page by searching for main gallery container
let galleryContainer = document.querySelector('.gallery-animate');

if(galleryContainer) {
  // if true, perform opacity animation on each child element
  let dogCards = galleryContainer.children;
  
  for (let i = 0; i < dogCards.length; i++){
    fadeIn(i, dogCards[i]);
  }
}

// Function for adding a delay within a loop
// Souce: https://www.geeksforgeeks.org/how-to-add-a-delay-in-a-javascript-loop/
function fadeIn(idx, e){
  setTimeout(function() {
    e.classList.remove('opacity-0');
  }, 500 + (250 * idx));
}

// 'vh' unit fix for mobile browsers to prevent backgroung image resizing on browser bar appear/disappear
// Source: https://css-tricks.com/the-trick-to-viewport-units-on-mobile/
let vh = window.innerHeight * 0.01;

document.documentElement.style.setProperty('--vh', `${vh}px`);

window.addEventListener('resize', () => {
  let vh = window.innerHeight * 0.01;
  document.documentElement.style.setProperty('--vh', `${vh}px`);
});




