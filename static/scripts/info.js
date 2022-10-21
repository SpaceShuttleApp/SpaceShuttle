let imginfo = document.getElementById("imginfo");
let imgId = imginfo.innerHTML.split(".")[0];
let deleteButton = document.getElementById("delete");
let visibilityToggle = document.getElementById("visibility");
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

let intialColor = "000000"
let colourInput = document.getElementById("ecolour")
colourInput.addEventListener("change", () => {
    intialColor = colourInput.value
})

esaveButton.addEventListener("click", () => {
    let title = document.getElementById("einput")
    let url = `${window.location.origin}/embed/${esaveButton.id}`
    fetch(`/update/${imgId}?visibility=${true}&embed_title=${title.value}&embed_colour_hex=${intialColor.replace("#", " ")}`, {
        method: "PATCH"
    }).then(() => {
        navigator.clipboard.writeText(url)
        .then(() => {
            alert("Embed saved and link copied to clipboard.");
        });
    })
});