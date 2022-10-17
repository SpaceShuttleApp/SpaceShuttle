let imginfo = document.getElementById("imginfo");
let imgId = imginfo.innerHTML.split(".")[0];
let deleteButton = document.getElementById("delete");
let visibilityToggle = document.getElementById("visibility");
let eshareButtons = document.getElementsByClassName("eshare-button");

deleteButton.addEventListener("click", () => {
  fetch(`/delete/${imgId}`, { method: "DELETE" }).then(() => {
    window.location.href = "/";
  });
});

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

for (let button of eshareButtons) {
  button.addEventListener("click", () => {
    let url = `${window.location.origin}/embed/${button.id}`
    fetch(`/data/${button.id.split(".")[0]}`)
    .then((res) => res.json())
    .then((data) => {
      if (data.visibility == false) {
        alert("Image is private. You can't share it.");
      } else {
        navigator.clipboard.writeText(url)
        .then(() => {
          alert("Link copied to clipboard.");
        });
      }
    })
  });
}