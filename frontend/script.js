const enhSlider = document.getElementById("enhSlider");
const sharpSlider = document.getElementById("sharpSlider");
const claritySlider = document.getElementById("claritySlider");

const enhValue = document.getElementById("enhValue");
const sharpValue = document.getElementById("sharpValue");
const clarityValue = document.getElementById("clarityValue");

const enhanceBtn = document.getElementById("enhanceBtn"); // optional
const imageInput = document.getElementById("imageInput");
const resultImage = document.getElementById("resultImage");
const spinner = document.getElementById("spinner");
const downloadBtn = document.getElementById("downloadBtn");

let currentFile = null;
let debounceTimer;

// Store selected image
imageInput.addEventListener("change", () => {
  currentFile = imageInput.files[0];
  if (!currentFile) return;
  resultImage.style.display = "block";
  downloadBtn.style.display = "none";
});

// Function to send image to backend
async function updateImage() {
  if (!currentFile) return;

  spinner.style.display = "block";        // show spinner
  downloadBtn.style.display = "none";     // hide download button

  const formData = new FormData();
  formData.append("file", currentFile);

  const url = `http://127.0.0.1:8000/api/enhance/?enh=${enhSlider.value}&sharp=${sharpSlider.value}&clarity=${claritySlider.value}`;

  try {
    const response = await fetch(url, { method: "POST", body: formData });
    if (!response.ok) throw new Error("Enhancement failed!");

    const data = await response.json();
    resultImage.src = "data:image/png;base64," + data.image;
    resultImage.style.display = "block";

    spinner.style.display = "none";        // hide spinner
    downloadBtn.style.display = "inline";  // show download button

  } catch (err) {
    console.error(err);
    spinner.style.display = "none";
    alert("Error connecting to backend!");
  }
}

// Debounce function
function debounceUpdate() {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(updateImage, 300); // wait 300ms
}

// Update displayed values and call debounced update
enhSlider.addEventListener("input", () => {
  enhValue.textContent = enhSlider.value;
  debounceUpdate();
});
sharpSlider.addEventListener("input", () => {
  sharpValue.textContent = sharpSlider.value;
  debounceUpdate();
});
claritySlider.addEventListener("input", () => {
  clarityValue.textContent = claritySlider.value;
  debounceUpdate();
});

// Optional Enhance button
enhanceBtn.addEventListener("click", updateImage);

// Download button
downloadBtn.addEventListener("click", () => {
  const link = document.createElement("a");
  link.href = resultImage.src;
  link.download = "enhanced_image.png";
  link.click();
});
