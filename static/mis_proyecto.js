  // FILTRAR PROYECTOS POR ESTADO
    const filtro = document.getElementById("filtroEstado");

    filtro.addEventListener("change", function () {
        const estadoSeleccionado = filtro.value;
        const tarjetas = document.querySelectorAll(".proyecto-card");

        tarjetas.forEach(card => {
            const estado = card.getAttribute("data-estado");

            if (estadoSeleccionado === "todos" || estado === estadoSeleccionado) {
                card.style.display = "block";
                card.style.opacity = 1;
            } else {
                card.style.opacity = 0;
                setTimeout(() => {
                    card.style.display = "none";
                }, 200);
            }
        });
    });