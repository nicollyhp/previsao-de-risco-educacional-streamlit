# 📘 Previsão de Risco Educacional – Associação Passos Mágicos

Aplicação desenvolvida em **Python** com interface em **Streamlit**, voltada à **identificação precoce de alunos em risco de defasagem educacional**, utilizando técnicas de **Machine Learning** aliadas a **regras pedagógicas preventivas**.

---

## 🔗 Aplicação online

https://previsao-de-risco-educacional.streamlit.app/

---

## 1. Introdução

A defasagem educacional é um fenômeno multifatorial, influenciado por aspectos acadêmicos, comportamentais e psicossociais. A identificação tardia desses fatores dificulta intervenções pedagógicas eficazes e aumenta o risco de evasão e baixo desempenho escolar.

Este projeto foi desenvolvido com o objetivo de **antecipar situações de risco**, oferecendo suporte analítico à tomada de decisão pedagógica, sem substituir o olhar humano do educador.

---

## 2. Objetivo do Projeto

O objetivo principal é **estimar o risco educacional de alunos** a partir de indicadores pedagógicos e psicossociais, permitindo:

- identificação precoce de perfis em risco;
- compreensão dos fatores associados à defasagem;
- apoio a intervenções pedagógicas preventivas;
- maior transparência e explicabilidade do modelo.

O foco do projeto está na **prevenção**, e não apenas na classificação de situações já consolidadas.

---

## 3. Indicadores Utilizados

O modelo foi treinado exclusivamente com indicadores considerados **básicos, acionáveis e anteriores à defasagem**, a saber:

- **IAN** – Adequação de nível  
- **IDA** – Desempenho acadêmico  
- **IEG** – Engajamento  
- **IAA** – Autoavaliação  
- **IPS** – Aspectos psicossociais  
- **IPV** – Ponto de virada  

Esses indicadores representam o **perfil do aluno antes da ocorrência da defasagem**, o que possibilita análises mais justas e intervenções antecipadas.

---

## 4. Construção da Variável de Risco

A variável **risco educacional** (baixo, moderado ou alto) foi construída a partir da **defasagem histórica (Defas)**, utilizada exclusivamente para **rotulagem dos dados durante o treinamento**.

A defasagem **não é utilizada como variável de entrada no modelo**.

Essa decisão foi tomada para evitar vazamento de informação e garantir maior validade ao aprendizado do modelo.

---

## 5. Variáveis Removidas do Treinamento

Algumas variáveis foram **removidas intencionalmente** do conjunto de treino para evitar que o modelo aprendesse padrões artificiais ou redundantes.

### Variáveis excluídas:

- **Defas**  
  Base para a criação do rótulo de risco. Sua inclusão caracterizaria uso da resposta no treino.

- **risco**  
  Variável-alvo, portanto não pode ser utilizada como preditora.

- **IPP** e **INDE**  
  Índices finais e agregados, que sintetizam outros indicadores e já representam, de forma indireta, o próprio risco.

A inclusão desses índices resultaria em um modelo que “antecipa” o risco utilizando informações que já o resumem, comprometendo a qualidade do aprendizado.

---

## 6. Estratégia de Modelagem

O projeto adota uma **abordagem híbrida**, composta por dois níveis complementares:

### 6.1 Risco Estatístico (Machine Learning)

- O modelo estima a **probabilidade estatística** de o aluno estar em risco.
- A classificação é baseada na soma das probabilidades de **risco moderado** e **alto risco**.
- Esse componente é responsável por capturar padrões históricos presentes nos dados.

### 6.2 Risco Moderado Preventivo (Regra Pedagógica)

Em situações nas quais a probabilidade estatística é baixa, mas há **concentração de indicadores em zona de atenção**, aplica-se uma regra pedagógica preventiva:

- Dois ou mais indicadores abaixo de 5; ou  
- Três ou mais indicadores muito baixos (abaixo de 4,5).

Nesses casos, o aluno é classificado como **Risco Moderado Preventivo**, mesmo sem evidência estatística significativa.

Essa estratégia reflete a prática pedagógica real, na qual múltiplos sinais de fragilidade demandam acompanhamento, ainda que o risco não esteja plenamente configurado.

---

## 7. Interpretação do Risco Moderado

O **risco moderado** não deve ser interpretado como um diagnóstico definitivo, mas como um **estado intermediário de atenção**, que pode surgir por dois motivos distintos:

- **Estatístico**: probabilidade intermediária estimada pelo modelo;  
- **Preventivo**: acúmulo de indicadores em zona de atenção, identificado por regra pedagógica.

Essa separação melhora a **explicabilidade**, evita contradições e fortalece o uso responsável do modelo.

---

## 8. Interface e Visualização

A aplicação, desenvolvida em **Streamlit**, permite:

- simulação interativa dos indicadores do aluno;
- visualização das probabilidades estimadas;
- identificação clara dos indicadores críticos;
- distinção explícita entre risco estatístico e risco preventivo.

O foco da interface é **clareza e apoio à decisão**, e não automação da decisão pedagógica.

---

## 9. Tecnologias Utilizadas

- Python  
- Pandas  
- Scikit-learn  
- Joblib  
- Streamlit  

---

## 10. Considerações Finais

Este projeto demonstra a aplicação de **Machine Learning de forma responsável no contexto educacional**, priorizando:

- prevenção em vez de reação;
- transparência nos critérios de decisão;
- separação entre análise estatística e julgamento pedagógico;
- apoio ao educador, e não substituição de sua atuação.

A abordagem adotada busca equilibrar **rigor técnico**, **interpretabilidade** e **aplicabilidade prática**.
