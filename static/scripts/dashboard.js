let shareButtons = document.getElementsByClassName("share-button");

for (let button of shareButtons) {
  button.addEventListener("click", () => {
    let imginfo = document.getElementById("imginfo");
    navigator.clipboard.writeText(`${window.location.origin}/cdn/${imginfo.innerHTML}`);
    alert("Link copied to clipboard.");
  });
}
