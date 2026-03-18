import os
import sys
import pandas as pd
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

MODEL_PATH = os.path.join(BASE_DIR, "modelo_treinado.pkl")
bundle = joblib.load(MODEL_PATH)

# Se for bundle
if isinstance(bundle, dict) and "model" in bundle:
    modelo = bundle["model"]
    FEATURES_MODELO = bundle.get("features", ["IAN","IDA","IEG","IAA","IPS","IPV"])
else:
    # Se for modelo simples
    modelo = bundle
    FEATURES_MODELO = ["IAN","IDA","IEG","IAA","IPS","IPV"]

def prever_risco(df):
    df = pd.DataFrame(df)

    for col in FEATURES_MODELO:
        if col not in df.columns:
            df[col] = 0

    df = df[FEATURES_MODELO].fillna(0).astype(float)

    # Probabilidades do modelo
    prob = modelo.predict_proba(df)[0]
    classes = list(modelo.classes_)
    prob_por_classe = {int(c): float(p) for c, p in zip(classes, prob)}

    # Assumindo classes 0/1/2 como baixo/moderado/alto (coerente com o bundle atual)
    prob_baixo = prob_por_classe.get(0, 0.0)
    prob_moderado = prob_por_classe.get(1, 0.0)
    prob_alto = prob_por_classe.get(2, 0.0)

    # Probabilidade estatística de risco
    prob_risco = prob_moderado + prob_alto

    # Regras pedagógicas (preventivo)
    indicadores_baixos = (df.iloc[0] < 5.0).sum()
    indicadores_muito_baixos = (df.iloc[0] < 4.5).sum()

    # Decisão final (híbrida)
    if prob_risco >= 0.40:
        classe_final = "Alto risco de defasagem educacional"
        tipo_risco = "estatistico"

    elif prob_risco >= 0.01:
        classe_final = "Risco moderado de defasagem"
        tipo_risco = "estatistico"

    elif indicadores_muito_baixos >= 3 or indicadores_baixos >= 2:
        classe_final = "Risco moderado de defasagem"
        tipo_risco = "preventivo"

    else:
        classe_final = "Baixo risco educacional"
        tipo_risco = "estatistico"

    return {
        "classe": classe_final,
        "tipo_risco": tipo_risco,          
        "prob_baixo": prob_baixo,
        "prob_moderado": prob_moderado,
        "prob_alto": prob_alto,
        "prob_risco": prob_risco,
        "prob_nao_risco": prob_baixo       
    }