document.getElementById("player-form").onsubmit = async function (event) {
  event.preventDefault();
  const formData = new FormData(this);
  const response = await fetch("/submit_answers", {
      method: "POST",
      body: formData,
  });

  if (response.ok) {
      alert("Answers submitted!");
      window.location.href = "/results";
  } else {
      alert("Error submitting answers.");
  }
};

function resetGame() {
  fetch("/reset_game").then(() => {
      alert("Game reset!");
      window.location.reload();
  });
}
