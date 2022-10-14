function toggleColorMode() {
    setColorMode(document.documentElement.getAttribute("color-mode") === "dark" ? "light" : "dark");
  }

  function setColorMode(mode) {
    document.documentElement.setAttribute("color-mode", mode);
    colorToggleButton.innerText = mode === "dark" ? "🌙" : "☀️";
  }

  const colorToggleButton = document.getElementById("color-mode-toggle");
  colorToggleButton.addEventListener("click", toggleColorMode);
  // Initialize the color mode.
  const colorSchemeQueryList = window.matchMedia("(prefers-color-scheme: dark)");
  if (colorSchemeQueryList.matches) {
    setColorMode("dark");
}
