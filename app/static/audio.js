alert("audio.js loaded");

const params = new URLSearchParams(window.location.search);
const audioId = params.get("id");
const token = localStorage.getItem("token");

console.log("Audio ID:", audioId);
console.log("Token exists:", !!token);

if (!audioId || !token) {
  window.location.href = "/";
  throw new Error("Not authorized or missing audioId");
}

// ===== ХАРАКТЕРИСТИКИ =====
fetch(`/api/audio/${audioId}/analysis`, {
  headers: {
    Authorization: "Bearer " + token,
  },
})
  .then((res) => {
    console.log("Analysis HTTP status:", res.status);
    return res.json();
  })
  .then((data) => {
    console.log("Analysis data:", data);

    if (data.message) {
      document.getElementById("info").innerHTML = `<p>${data.message}</p>`;
      return;
    }

    document.getElementById("info").innerHTML = `
        <p><b>Duration:</b> ${data.duration.toFixed(2)} sec</p>
        <p><b>Sample rate:</b> ${data.sample_rate}</p>
        <p><b>RMS mean:</b> ${data.rms_mean.toFixed(6)}</p>
        <p><b>Spectral centroid mean:</b> ${data.spectral_centroid_mean.toFixed(
          2
        )}</p>
    `;
  });

// ===== ВИЗУАЛИЗАЦИЯ =====
fetch(`/api/audio/${audioId}/visualization`, {
  headers: {
    Authorization: "Bearer " + token,
  },
})
  .then((res) => {
    console.log("Visualization HTTP status:", res.status);
    return res.json();
  })
  .then((data) => {
    console.log("Visualization data:", data);

    if (!data.waveform || !data.fft) {
      console.error("Visualization data missing");
      return;
    }

    new Chart(document.getElementById("waveform"), {
      type: "line",
      data: {
        labels: data.waveform.map((_, i) => i),
        datasets: [
          {
            data: data.waveform,
            borderWidth: 1,
            pointRadius: 0,
          },
        ],
      },
    });

    new Chart(document.getElementById("fft"), {
      type: "line",
      data: {
        labels: data.fft.map((_, i) => i),
        datasets: [
          {
            data: data.fft,
            borderWidth: 1,
            pointRadius: 0,
          },
        ],
      },
    });
  });
