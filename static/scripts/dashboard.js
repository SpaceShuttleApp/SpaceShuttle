let shareButton = document.getElementById("share");
shareButton.addEventListener("click", function () {
    let imginfo = document.getElementById("imginfo");
    navigator.clipboard.writeText(`${window.location.origin}/cdn/${imginfo.innerHTML}`);
});