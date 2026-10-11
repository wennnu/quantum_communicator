const cards = document.querySelectorAll(".character-card");
const start_button = document.getElementById("start-button");

cards.forEach(card => {
	card.addEventListener("click", () => {
		cards.forEach(c => c.classList.remove("selected"));
		card.classList.add("selected");
		selectedCharacter = card.getAttribute("data-hero");
		start_button.disabled = false;
	});
});


start_button.addEventListener("click", () => {
	if (selectedCharacter) {
		alert("You selected ${selectedCharacter}$!");
	}
});
