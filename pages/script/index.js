const rule_button = document.getElementById("rule-button");
const rule_modal = document.getElementById("rule-modal");
const close_button = document.getElementById("close-button");
const play_button = document.getElementById("play-button");

rule_button.addEventListener("click", ()=> {
  rule_modal.showModal();
});

close_button.addEventListener("click", ()=> {
  rule_modal.close();
});

play_button.addEventListener("click", () => {
	window.location.href="./character_select.html";
});
