const newsContainer = document.getElementById("news-container");


fetch("news.json")
  .then(response => response.json())
  .then(data => {
    // Limitar a las 10 noticias más recientes
      data.slice(0, 10).forEach(item => { // muestra las 5 noticias más recientes
          const div = document.createElement("div");
          div.className = "news-item";
          div.innerHTML = `
            <h3><a href="${item.link}" target="_blank">${item.title}</a> (${item.source})</h3>
            <p>${item.summary}</p>
          `;
          newsContainer.appendChild(div);
      });
  })
  .catch(err => {
      newsContainer.innerHTML = "<p>No se pudieron cargar las noticias en este momento.</p>";
      console.error("Error cargando noticias:", err);
  });
