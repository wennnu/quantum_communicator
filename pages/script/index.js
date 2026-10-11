console.log("Script loaded");
const rule_button = document.getElementById("rule-button");
const rule_modal = document.getElementById("rule-modal");
const close_button = document.getElementById("close-button");

rule_button.addEventListener("click", ()=> {
  console.log("Click!");
  rule_modal.showModal();
});

close_button.addEventListener("click", ()=> {
  rule_modal.close();
});
