const container = document.querySelector("body");

function createFallingObject() {
  const fallingObject = document.createElement("div");
  fallingObject.classList.add("falling-object");
  container.appendChild(fallingObject);
  
  setTimeout(() => {
    container.removeChild(fallingObject);
  }, 1000);
}

setInterval(createFallingObject, 10000000);