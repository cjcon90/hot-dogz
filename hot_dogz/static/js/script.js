let dogCards = document.getElementById('gallery-container').children;
console.log(dogCards)
for(let card of dogCards){
  card.style.visibility = 'hidden'
  card.style.opacity = 0
}

for (let i = 0; i < dogCards.length; i++){
  moveLeft(i, dogCards[i])
}

// Source on adding a delay within a loop: https://www.geeksforgeeks.org/how-to-add-a-delay-in-a-javascript-loop/
function moveLeft(i, card){
  setTimeout(function() {
    card.style.visibility = 'visible'
    card.style.opacity = 1
  }, 750 + (250 * i));
}