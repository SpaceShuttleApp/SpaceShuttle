let shareButton = document.getElementById("share");

shareButton.addEventListener("click", () => {
  let imginfo = document.getElementById("imginfo");
  navigator.clipboard.writeText(`${window.location.origin}/cdn/${imginfo.innerHTML}`);
  alert("Link copied to clipboard.");
});
