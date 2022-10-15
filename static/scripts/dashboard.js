let shareButtons = document.getElementsByClassName("share-button");

for (let button of shareButtons) {
  button.addEventListener("click", () => {
    let imginfo = document.getElementById("imginfo");
    navigator.clipboard.writeText(`${window.location.origin}/cdn/${imginfo.innerHTML}`);
    alert("Link copied to clipboard.");
    // Fix copy to clipboard only working once issue and add error alert when the image returns an error (404) saying that the image isn't visable (Public)
  });
}
