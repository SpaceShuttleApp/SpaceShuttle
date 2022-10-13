let imginfo = document.getElementById("imginfo");
let imgId = imginfo.innerHTML.split(".")[0];
// lazy to take image id from window.location.pathname
let delButton = document.getElementById("delete");
delButton.addEventListener("click", function () {
    fetch(`/delete?id=${imgId}`, { method: "DELETE" })
});
