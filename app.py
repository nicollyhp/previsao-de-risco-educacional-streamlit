import streamlit as st
import pandas as pd
from predictor import prever_risco

# -------------------------------------------------
# Configuração da página
# -------------------------------------------------

st.set_page_config(
    page_title="Passos Mágicos • Previsão de Risco Educacional",
    page_icon="🎓",
    layout="wide"
)

# -------------------------------------------------
# Header
# -------------------------------------------------

st.title("🎓 Análise Preditiva de Risco Educacional")

st.caption(
    "Ferramenta de apoio para identificação precoce de alunos em risco de defasagem escolar."
)

st.markdown("---")

# -------------------------------------------------
# Sidebar
# -------------------------------------------------

with st.sidebar:

    st.header("📚 Sobre o Projeto")

    st.write(
        """
        Esta aplicação utiliza **Machine Learning** para identificar
        alunos com risco de **defasagem educacional**.

        O modelo analisa indicadores pedagógicos e psicossociais
        utilizados pela **Associação Passos Mágicos**.
        """
    )

    st.markdown("### Indicadores analisados")

    st.write(
        """
        **IAN** – Adequação de nível  
        **IDA** – Desempenho acadêmico  
        **IEG** – Engajamento  
        **IAA** – Autoavaliação  
        **IPS** – Aspectos psicossociais  
        **IPV** – Ponto de virada  
        """
    )

    st.markdown("---")

    st.info(
        "O objetivo é apoiar educadores na tomada de decisão e intervenção precoce."
    )

# -------------------------------------------------
# Entrada de dados
# -------------------------------------------------

st.header("📊 Simulador de Indicadores do Aluno")

col1, col2, col3 = st.columns(3)

dados_aluno = {}

with col1:

    dados_aluno["IAN"] = st.number_input(
        "IAN – Adequação de nível",
        0.0, 10.0, 6.0, 0.1
    )

    dados_aluno["IDA"] = st.number_input(
        "IDA – Desempenho acadêmico",
        0.0, 10.0, 6.5, 0.1
    )

with col2:

    dados_aluno["IEG"] = st.number_input(
        "IEG – Engajamento",
        0.0, 10.0, 6.5, 0.1
    )

    dados_aluno["IAA"] = st.number_input(
        "IAA – Autoavaliação",
        0.0, 10.0, 7.0, 0.1
    )

with col3:

    dados_aluno["IPS"] = st.number_input(
        "IPS – Aspectos psicossociais",
        0.0, 10.0, 6.0, 0.1
    )

    dados_aluno["IPV"] = st.number_input(
        "IPV – Ponto de virada",
        0.0, 10.0, 6.5, 0.1
    )

st.markdown("---")

# -------------------------------------------------
# Previsão
# -------------------------------------------------

st.header("🤖 Previsão de Risco Educacional")

if st.button("Analisar risco do aluno"):

    try:

        df = pd.DataFrame([dados_aluno])

        resultado = prever_risco(df)

        classe = resultado["classe"]
        tipo_risco = resultado.get("tipo_risco", "estatistico")  # ✅ novo (default)

        prob_baixo = resultado["prob_baixo"]
        prob_moderado = resultado["prob_moderado"]
        prob_alto = resultado["prob_alto"]

        prob_risco = resultado.get("prob_risco", prob_moderado + prob_alto)
        prob_nao_risco = resultado.get("prob_nao_risco", prob_baixo)

        st.success("Análise realizada com sucesso!")

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("📈 Probabilidade de Risco")

            st.caption(
                "Aqui, **risco** significa a chance estatística do aluno estar em **Risco moderado ou Alto**."
            )

            # ✅ Se for moderado preventivo, NÃO faz sentido exibir "risco 0.0%" como se fosse contraditório
            if ("moderado" in classe.lower()) and (tipo_risco == "preventivo"):
                st.warning("⚠️ Risco moderado **preventivo** (regra pedagógica)")
                st.markdown(
                    "A classificação moderada foi definida por **zona de atenção** (múltiplos indicadores abaixo de 5), "
                    "mesmo que a probabilidade estatística esteja baixa."
                )
                st.metric(
                    "Probabilidade estatística de risco (modelo)",
                    f"{prob_risco*100:.1f}%"
                )
                
                st.progress(prob_risco)

            else:
                st.metric(
                    "Probabilidade de risco (estatística)",
                    f"{prob_risco*100:.1f}%"
                )
                st.progress(prob_risco)

            st.info(
                f"✅ Probabilidade estatística de **não risco** (baixo risco): **{prob_nao_risco*100:.1f}%**"
            )

        with col2:

            st.subheader("🚨 Classificação")

            if "Baixo" in classe:
                st.success(classe)

            elif "moderado" in classe.lower():
                st.warning(classe)

            else:
                st.error(classe)

        st.markdown("---")

        # -------------------------------------------------
        # Distribuição real das probabilidades
        # -------------------------------------------------

        st.subheader("📊 Distribuição de Probabilidade (por categoria)")

        st.caption(
            "As três probabilidades abaixo somam 100%. O modelo escolhe a categoria com maior probabilidade."
        )

        df_risco = pd.DataFrame({
            "Categoria": [
                "Baixo risco",
                "Risco moderado",
                "Alto risco"
            ],
            "Probabilidade": [
                prob_baixo,
                prob_moderado,
                prob_alto
            ]
        })

        # gráfico mais legível (ordenado)
        df_risco["Probabilidade (%)"] = (df_risco["Probabilidade"] * 100).round(1)
        df_risco = df_risco.sort_values("Probabilidade", ascending=True)

        st.bar_chart(df_risco.set_index("Categoria")[["Probabilidade (%)"]])

        st.markdown("---")

        # -------------------------------------------------
        # Análise automática
        # -------------------------------------------------

        st.subheader("🔎 Análise dos Indicadores")

        st.caption("Regra rápida: indicadores **abaixo de 5** podem indicar necessidade de atenção.")

        indicadores_baixos = []

        for k, v in dados_aluno.items():
            if v < 5:
                indicadores_baixos.append(k)

        if indicadores_baixos:

            st.warning(
                f"""
                Indicadores que podem demandar atenção pedagógica:

                **{", ".join(indicadores_baixos)}**
                """
            )

        else:

            st.success(
                "Os indicadores estão dentro de níveis considerados adequados."
            )

        st.markdown("---")

        # -------------------------------------------------
        # Visualização
        # -------------------------------------------------

        st.subheader("📊 Indicadores Informados")

        st.caption(
            "Escala de 0 a 10. Quanto maior, melhor. A área **abaixo de 5** merece atenção."
        )

        df_ind = pd.DataFrame(
            list(dados_aluno.items()),
            columns=["Indicador", "Valor"]
        )

        # Ordenar do menor para o maior ajuda a identificar prioridades rapidamente
        df_ind = df_ind.sort_values("Valor", ascending=True)

        # Criar uma coluna de status para facilitar entendimento
        df_ind["Status"] = df_ind["Valor"].apply(
            lambda x: "Atenção (abaixo de 5)" if x < 5 else "Adequado (>= 5)"
        )

        # Mostrar tabela simples
        st.dataframe(
            df_ind,
            width="stretch",
            hide_index=True
        )

        # Gráfico de indicadores (✅ corrigido para mostrar os INDICADORES)
        df_plot = df_ind[["Indicador", "Valor"]].set_index("Indicador")
        st.bar_chart(df_plot)

        # Linha de referência textual
        st.markdown(
            "✅ **Dica de leitura:** valores **abaixo de 5** são considerados *zona de atenção* neste painel."
        )

    except Exception as e:

        st.error(f"Erro ao executar previsão: {e}")

# -------------------------------------------------
# Rodapé
# -------------------------------------------------

st.markdown("---")

st.caption(
    "Projeto desenvolvido para o Datathon da Associação Passos Mágicos • Machine Learning aplicado à educação"
)