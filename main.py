from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from typing import List

app = FastAPI()

FATOR_ENERGIA = 0.09 # kg CO2e por kWh 
FATOR_AGUA = 0.40 # kg CO2e por m³

class RegistroConsumo(BaseModel):
    empresa: str = Field(..., description="Nome da empresa")
    kwh: float = Field(..., gt=0, description="Consumo de energia em kWh")
    m3: float = Field(..., gt=0, description="Consumo de água em m³")

@app.post("/calcular")
def calcular_impacto(lista_dados: List[RegistroConsumo]):
    resultados_individuais = []
    total_co2_acumulado = 0.0 

    for registro in lista_dados:
        emissao_k = registro.kwh * FATOR_ENERGIA
        emissao_m = registro.m3 * FATOR_AGUA
        impacto_item = round(emissao_k + emissao_m, 2)
        
        total_co2_acumulado += impacto_item
        
        resultados_individuais.append({
            "empresa": registro.empresa,
            "impacto_kg_co2": impacto_item
        })
    
    return {
        "resumo_por_empresa": resultados_individuais,
        "impacto_total_do_lote": f"{round(total_co2_acumulado, 2)} kg CO2",
        "total_de_empresas_processadas": len(lista_dados),
        "status": "Processamento em lote concluído."
    }

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):  
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "mensagem_de_erro": "Dados de entrada inválidos. Verifique os campos e tente novamente.",
            "ajuda": "Certifique-se de que 'empresa' é uma string, 'kwh' e 'm3' são números positivos.",
            "detalhes": exc.errors()
            },
    )