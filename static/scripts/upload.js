let uploadButton = document.getElementById("upload");
let hiddenInput = document.getElementById("files");
let image = document.getElementById("placeholder");
let viewButtom = document.getElementById("view_img");
let matrix = document.getElementById("matrix");
let contextImageId = null;

function handleFile(file) {
  let reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onloadend = () => {
    uploadButton.disabled = true;
    image.src = reader.result;
    let data = { content: reader.result, filename: file.name };
    fetch(`/upload`, {
      method: "POST",
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((resp) => {
        contextImageId = resp.id;
        matrix.style.display = "flex";
      });
  };
}

uploadButton.addEventListener("click", () => {
  hiddenInput.click();
});

hiddenInput.addEventListener("change", () => {
  let file = hiddenInput.files[0];
  if (file) {
    handleFile(file);
  }
});

viewButtom.addEventListener("click", () => {
  window.location.href = `/info/${contextImageId}`;
});

// detect file paste
document.addEventListener("paste", (event) => {
  let file = event.clipboardData.files[0];
  if (file && file.type.startsWith("image/")) {
    handleFile(file);
  }
});

// file drop callback
function dropHandler(event) {
  event.preventDefault();
  if (event.dataTransfer.items) {
    let file = event.dataTransfer.items[0].getAsFile();
    if (file.type.startsWith("image/")) {
      handleFile(file);
    }
  }
}

// overrided default file drop event
function dragOverHandler(event) {
  event.preventDefault();
}
