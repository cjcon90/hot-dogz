// check if on gallery page by searching for main gallery container
let galleryContainer = document.querySelector('.gallery-animate')

if(galleryContainer) {
  // if true, perform opacity animation on each child element
  let dogCards = galleryContainer.children
  
  for (let i = 0; i < dogCards.length; i++){
    fadeIn(i, dogCards[i])
  }
  
  // Source on adding a delay within a loop: https://www.geeksforgeeks.org/how-to-add-a-delay-in-a-javascript-loop/
  function fadeIn(i, card){
    setTimeout(function() {
      card.classList.remove('opacity-0')
    }, 500 + (250 * i));
  }
}




