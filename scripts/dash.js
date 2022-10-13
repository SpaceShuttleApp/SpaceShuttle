let shareButton = document.getElementById("share");
shareButton.addEventListener("click", function () {
    let imginfo = document.getElementById("imginfo");
    console.long(window.location.href);
    navigator.clipboard.writeText(`/cdn/${imginfo.innerHTML}`);
});