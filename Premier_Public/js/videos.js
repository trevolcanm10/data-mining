const container = document.getElementById("videos-container");

fetch("videos.json")
  .then(res => res.json())
  .then(data => {

    data.forEach(video => {
      const div = document.createElement("div");
      div.className = "video-item";

      div.innerHTML = `
        <h3>${video.title}</h3>

        <iframe width="560" height="315"
          src="${video.url}"
          frameborder="0"
          allowfullscreen>
        </iframe>
      `;

      container.appendChild(div);
    });

  })
  .catch(err => {
    container.innerHTML = "<p>No se pudieron cargar los videos.</p>";
    console.error(err);
  });
