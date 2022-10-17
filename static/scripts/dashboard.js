let shareButtons = document.getElementsByClassName("share-button");

for (let button of shareButtons) {
    button.addEventListener("click", () => {
        let url = `${window.location.origin}/cdn/${button.id}`
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