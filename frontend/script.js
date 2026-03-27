const backendURL = "http://127.0.0.1:8000/process";

let pdfDoc = null;
let scale = 1.5;

async function renderPDF(file) {
  const reader = new FileReader();

  reader.onload = async function () {
    const typedarray = new Uint8Array(this.result);

    pdfDoc = await pdfjsLib.getDocument(typedarray).promise;
    const page = await pdfDoc.getPage(1);

    const viewport = page.getViewport({ scale });

    const canvas = document.getElementById("pdfCanvas");
    const context = canvas.getContext("2d");

    canvas.height = viewport.height;
    canvas.width = viewport.width;

    await page.render({
      canvasContext: context,
      viewport: viewport
    }).promise;

    // Resize overlay
    const overlay = document.getElementById("overlay");
    overlay.style.width = canvas.width + "px";
    overlay.style.height = canvas.height + "px";
  };

  reader.readAsArrayBuffer(file);
}

async function uploadPDF() {
  const fileInput = document.getElementById("fileInput");
  const file = fileInput.files[0];

  if (!file) return alert("Select file");

  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(backendURL, {
    method: "POST",
    body: formData
  });

  const data = await response.json();

  await renderPDF(file);   // render PDF
  drawBoxes(data.results); // draw boxes
}


function drawBoxes(results) {
  const overlay = document.getElementById("overlay");
  overlay.innerHTML = "";

  results.forEach(item => {
    const [x0, y0, x1, y1] = item.bbox;

    const box = document.createElement("div");
    box.className = "box";

    // scale coordinates
    box.style.left = x0 * scale + "px";
    box.style.top = y0 * scale + "px";
    box.style.width = (x1 - x0) * scale + "px";
    box.style.height = (y1 - y0) * scale + "px";

    // color coding
    if (item.type === "NAME") box.style.borderColor = "red";
    else if (item.type === "PHONE") box.style.borderColor = "blue";
    else if (item.type === "EMAIL") box.style.borderColor = "green";

    overlay.appendChild(box);
  });
}