from fastapi import FastAPI, Query

app = FastAPI()

FATOR_ENERGIA = 0.09 # kg CO2e por kWh 
FATOR_AGUA = 0.40 # kg CO2e por m³


@app.get("/")
def home():
    return {"status": "Monitor de Impacto Ambiental Ativo"}

@app.get("/calcular")
def calcular_impacto(
    kwh: float = Query(gt=0, description="Consumo de energia em kWh"),
    m3: float = Query(gt=0, description="Consumo de água em m³")
):
    co2_energia = kwh * FATOR_ENERGIA
    co2_agua = m3 * FATOR_AGUA
    co2_total = round(co2_energia + co2_agua, 2)
    
    return {
        "consumo_de_energia": kwh,
        "consumo_de_água": m3,
        "emissão_total_de_co2": co2_total, 
        "mensagem": "Calculado o impacto ambiental com base no consumo de energia e água."
    }