from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

FATOR_ENERGIA = 0.09 # kg CO2e por kWh 
FATOR_AGUA = 0.40 # kg CO2e por m³


class RegistroConsumo(BaseModel):
    empresa: str = Field(..., description="Nome da empresa")
    kwh: float = Field(..., gt=0, description="Consumo de energia em kWh")
    m3: float = Field(..., gt=0, description="Consumo de água em m³")


@app.post("/calcular")
def calcular_impacto(
    dados: RegistroConsumo
):
    co2_energia = dados.kwh * FATOR_ENERGIA
    co2_agua = dados.m3 * FATOR_AGUA
    co2_total = round(co2_energia + co2_agua, 2)
    
    return {
        "empresa": dados.empresa,
        "detalhes": {
            "energia_kg_co2": round(co2_energia, 2),
            "agua_kg_co2": round(co2_agua, 2)
        },
        "impacto_total": f"{co2_total} kg CO2",
        "status": "Processamento concluído via Schema Pydantic"
    }