import matplotlib
matplotlib.use('Agg')

import numpy as np
from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from calculos import simular_triangulo, simular_triangulo_especifico, generarAleatorios, generar_aproximacion, analizar_normalidad
import os

app = FastAPI()

# Ruta para las plantillas HTML
templates = Jinja2Templates(directory="templates")

# (Opcional) Si tienes archivos estáticos como CSS/JS/imagenes
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/simular")
def simular(levels: int = 10):
    aleatorios = generarAleatorios(n_balls=100, n_levels=levels)
    message = []
    for x in range(0, 5):
        result = simular_triangulo(n_balls=100, n_levels=levels, aleatorios=aleatorios) if x > 3 else simular_triangulo_especifico(n_balls=100, n_levels=levels, triangulo=x, aleatorios=aleatorios)
        valores = np.repeat(np.arange(len(result)), result.astype(int))
        generar_aproximacion(valores, x)
        cv, es_cv, shapiro_value, es_shapiro = analizar_normalidad(valores)
        message.append({
            "cv": cv,
            "es_cv": str(es_cv),
            "shapiro": shapiro_value,
            "es_shapiro": str(es_shapiro)
        })
    
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        "message": message
    })

@app.get("/imagen")
def imagen(imagen: int):
    image_path = os.path.join("img", "aproximacion" + str(imagen) + ".png")
    return FileResponse(image_path, media_type="image/png")

#if __name__ == "__main__":
#    import uvicorn
#    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)