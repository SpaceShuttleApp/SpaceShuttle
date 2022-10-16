let imginfo = document.getElementById("imginfo");
let imgId = imginfo.innerHTML.split(".")[0];
// lazy to take image id from window.location.pathname
let deleteButton = document.getElementById("delete");

deleteButton.addEventListener("click", () => {
  fetch(`/delete/${imgId}`, { method: "DELETE" }).then(() => {
    window.location.href = "/";
  });
});
