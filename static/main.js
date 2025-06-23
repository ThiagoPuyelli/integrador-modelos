
const renglones = document.querySelector("#renglones")
const button = document.querySelector("#enviarSimulacion")
const cargando =  document.querySelector("#cargando")

button.addEventListener("click", () => {
    const levels = renglones.value
    //const tole = tolerancia.value
    generarSimulacion(levels)
})
const generarSimulacion = async (levels = 10) => {
    try {
        cargando.style.display = "block"
        mensajes = []
        const simular = await fetch(`/simular?levels=${levels}`)
        if (simular.ok) {
            const content = await simular.json()
            mensajes = content.message
            cargando.style.display = "none"
            for (let i = 0;i <= 4;i++) {
                if (i < 4 && levels < 4) {
                    continue
                }
                fetch('/imagen?imagen=' + i)
                    .then(response => response.blob())
                    .then(blob => {
                        const img = document.createElement('img');
                        const p = document.createElement('p');
                        const div = document.querySelector(".i" + i)
                        p.innerHTML = i === 4 ? "Sin triangulo modificado<br>" : "Triangulo en posicion " + (i + 1) + "<br>"
                        p.innerHTML += "CV: " + mensajes[i].cv + "<br>Shapiro: " + mensajes[i].shapiro + "<br>"
                        console.log(mensajes[i])
                        p.innerHTML += mensajes[i].es_cv === 'True' ? "Si se puede aproximar a normal por variacion<br>" : "No se puede aproximar a la normal por variacion<br>" 
                        p.innerHTML += mensajes[i].es_shapiro === 'True' ? "Si se puede aproximar a normal por Shapiro-Wilk<br>" : "No se puede aproximar a la normal por Shapiro-Wilk<br>" 

                        img.src = URL.createObjectURL(blob);
                        img.alt = "Imagen cargada dinámicamente";
                        img.style.maxWidth = "400px";
                        div.innerHTML = ""
                        //const grafico = document.querySelector('#grafico')
                        div.appendChild(img);
                        div.appendChild(p);
                        //grafico.appendChild(div);
                    })
                    .catch(error => {
                        console.error('Error al cargar la imagen:', error);
                });
            }
        }
    } catch (err) {
        console.log(err)
    }
    
    
}

