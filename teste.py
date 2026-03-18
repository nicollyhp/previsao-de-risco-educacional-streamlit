import pandas as pd
from predictor import prever_risco

# -------------------------------------------------
# Função utilitária para gerar cenários rapidamente
# -------------------------------------------------
def testar_caso(nome, **kwargs):
    """
    Exemplo:
    testar_caso(
        "IEG baixo",
        IAN=6.0, IDA=6.5, IEG=3.0, IAA=7.0, IPS=6.0, IPV=6.5
    )
    """
    df = pd.DataFrame([kwargs])
    resultado = prever_risco(df)

    print("\n" + "=" * 70)
    print(nome)
    print("Entrada:", kwargs)
    print(
        "Saída:",
        f"Classe = {resultado['classe']} | "
        f"Prob. risco = {resultado['prob_risco']*100:.1f}% | "
        f"(baixo={resultado['prob_baixo']*100:.1f}%, "
        f"mod={resultado['prob_moderado']*100:.1f}%, "
        f"alto={resultado['prob_alto']*100:.1f}%)"
    )


# -------------------------------------------------
# Cenários de teste
# -------------------------------------------------

# Caso base (baixo risco)
testar_caso(
    "Perfil saudável (baseline)",
    IAN=6.0, IDA=6.5, IEG=6.5, IAA=7.0, IPS=6.0, IPV=6.5
)

# MODERADO — dois indicadores na zona de atenção
testar_caso(
    "MODERADO — IEG e IPS baixos",
    IAN=6.0,
    IDA=6.5,
    IEG=4.2,
    IAA=6.8,
    IPS=4.5,
    IPV=6.2
)

# MODERADO — desempenho e engajamento no limite
testar_caso(
    "MODERADO — IDA e IEG no limite",
    IAN=6.0,
    IDA=4.9,
    IEG=4.8,
    IAA=6.5,
    IPS=6.0,
    IPV=6.5
)

# MODERADO — perfil instável (vários ~5)
testar_caso(
    "MODERADO — perfil instável",
    IAN=5.0,
    IDA=5.1,
    IEG=5.0,
    IAA=5.2,
    IPS=5.3,
    IPV=5.1
)

# Alto risco — vários indicadores baixos
testar_caso(
    "Perfil de alto risco",
    IAN=3.0,
    IDA=3.5,
    IEG=4.0,
    IAA=4.5,
    IPS=3.8,
    IPV=4.0
)

# Caso extremo
testar_caso(
    "Crítico extremo",
    IAN=2.0,
    IDA=2.5,
    IEG=2.8,
    IAA=3.0,
    IPS=2.2,
    IPV=2.7
)