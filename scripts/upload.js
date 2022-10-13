let button = document.getElementById("upload");
let hiddenInput = document.getElementById("files");
let image = document.getElementById("placeholder");
let viewButtom = document.getElementById("view_img");
let matrix = document.getElementById("matrix");
let context_image_id = null;

function handleFile(file) {
    let reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = function () {
        button.disabled = true;
        image.src = reader.result;
        let data = { content: reader.result, filename: file.name };
        fetch(`/upload`, { method: "POST", body: JSON.stringify(data) })
            .then(response => response.json())
            .then(resp => {
                context_image_id = resp.id;
                matrix.style.display = "flex";
            })
    }
}
button.addEventListener("click", function () {
    hiddenInput.click();
});

hiddenInput.addEventListener("change", function () {
    let file = hiddenInput.files[0]
    if (file) {
        handleFile(file);
    }
});

viewButtom.addEventListener("click", function () {
    window.location.href = `/info/${context_image_id}`;
});

// file drop callback
function dropHandler(ev) {
    ev.preventDefault();
    if (ev.dataTransfer.items) {
        let file = ev.dataTransfer.items[0].getAsFile();
        if (file.type.startsWith("image/")) {
            handleFile(file);
        }
    }
}

// overrided default file drop event
function dragOverHandler(ev) {
    ev.preventDefault();
}

// detect file paste
document.addEventListener("paste", function (e) {
    let file = e.clipboardData.files[0];
    if (file && file.type.startsWith("image/")) {
        handleFile(file);
    }
});