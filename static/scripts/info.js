let imginfo = document.getElementById("imginfo");
let imgId = imginfo.innerHTML.split(".")[0];
let deleteButton = document.getElementById("delete");
let visibilityToggle = document.getElementById("visibility");
let eshareButton = document.getElementsByClassName("eshare-button")[0];
let esaveButton = document.getElementsByClassName("esave-button")[0];

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

eshareButton.addEventListener("click", () => {
    let url = `${window.location.origin}/embed/${eshareButton.id}`
    fetch(`/data/${eshareButton.id.split(".")[0]}`)
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

let intialColor = "#ff0000"
let colourInput = document.getElementById("ecolour")
colourInput.addEventListener("change", () => {
    intialColor = colourInput.value
})

esaveButton.addEventListener("click", () => {
    let title = document.getElementById("einput")
    fetch(`/update/${imgId}?embed_title=${title.value}&embed_colour_hex=${intialColor}`, {
        method: "PATCH"
    }).then(() => {
        alert("Embed saved")
    })
});