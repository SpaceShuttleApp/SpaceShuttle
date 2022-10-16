let imginfo = document.getElementById("imginfo");
let imgId = imginfo.innerHTML.split(".")[0];
// lazy to take image id from window.location.pathname
let deleteButton = document.getElementById("delete");

deleteButton.addEventListener("click", () => {
  fetch(`/delete/${imgId}`, { method: "DELETE" }).then(() => {
    window.location.href = "/";
  });
});

let visibilityToggle = document.getElementById("visibility");
visibilityToggle.addEventListener("click", () => {
    fetch(`/data/${imgId}`)
    .then((res) => res.json())
    .then((data) => {
        if (data.visibility == false) {
            fetch(`/update/${imgId}?visibility=${true}`, { method: "PATCH" })
            .then(() => {
                visibilityToggle.innerHTML = `<i class="fa fa-eye"></i> Public`;
            });
        } else {
            fetch(`/update/${imgId}?visibility=${false}`, { method: "PATCH" })
            .then(() => {
                visibilityToggle.innerHTML = `<i class="fa fa-eye"></i> Private`;
            });
        }
    })
});