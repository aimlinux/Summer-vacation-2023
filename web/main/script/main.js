const gameText = document.querySelector(".game-text");
const userInput = document.getElementById("user-input");
const resetButton = document.getElementById("reset-button");
const message = document.getElementById("message");

let currentWordIndex = 0;
const words = ["お", "は", "よ", "う"];
let userInputValue = "";

function updateGameText() {
  gameText.textContent = words[currentWordIndex];
}

updateGameText();

userInput.addEventListener("input", (e) => {
  userInputValue = e.target.value;
  if (userInputValue === words[currentWordIndex]) {
    currentWordIndex++;
    userInput.value = "";
    if (currentWordIndex === words.length) {
      message.textContent = "クリア！おめでとうございます！";
    } else {
      updateGameText();
    }
  }
});

resetButton.addEventListener("click", () => {
  currentWordIndex = 0;
  userInput.value = "";
  message.textContent = "";
  updateGameText();
});