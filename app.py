import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora de Fotografias", layout="centered")

# Estilo e cabeçalho
st.title("📸 Calculadora de Combinações de Fotografias")
st.markdown("Feito com 💜 por **Guilherme Santos**")
st.markdown("---")

# Sessão de histórico
if "historico" not in st.session_state:
    st.session_state["historico"] = []

# Limpar dados
f st.button("🧹 Limpar dados"):
    # Limpar todos os dados armazenados na sessão
    st.session_state.clear()  # Isso apaga todos os dados do estado da sessão

    # Adicionar uma mensagem para o utilizador
    st.write("Dados limpos com sucesso!")

    # A maneira mais simples de garantir que a interface é atualizada: parar o script
    st.stop()  # Isso faz com que a execução do script pare, o que ajuda a "refrescar" a página

# Layout de inputs em colunas
col1, col2 = st.columns(2)
with col1:
    total_preco = st.number_input("💰 Faturação total (€)", min_value=0, step=1)
with col2:
    total_fotografias = st.number_input("📷 Total de fotografias", min_value=0, step=1)

st.subheader("🎞️ Pacotes de Reportagens")
col3, col4 = st.columns(2)
with col3:
    pacote_5 = st.number_input("5 fotos (25€)", min_value=0, step=1)
    pacote_15 = st.number_input("15 fotos (45€)", min_value=0, step=1)
with col4:
    pacote_10 = st.number_input("10 fotos (35€)", min_value=0, step=1)
    pacote_20 = st.number_input("20 fotos (55€)", min_value=0, step=1)

st.subheader("🏫 Fotografias de Escolas")
fotos_escola = st.number_input("Nº de fotografias de escola (5€/cada)", min_value=0, step=1)

# Função principal
def encontrar_combinacoes(total_preco, total_fotografias, pacotes_reportagens, pacotes_escolas):
    combinacoes = []
    valor_escolas = pacotes_escolas[0] * 5
    total_preco -= valor_escolas
    total_fotografias -= pacotes_escolas[0]

    valor_reportagens = (
        pacotes_reportagens[0] * 25 +
        pacotes_reportagens[1] * 35 +
        pacotes_reportagens[2] * 45 +
        pacotes_reportagens[3] * 55
    )
    total_preco -= valor_reportagens

    for x in range(total_fotografias + 1):
        for y in range(total_fotografias // 2 + 1):
            fotos_usadas = x + 2 * y
            z = total_fotografias - fotos_usadas
            if z >= 0:
                preco_total = 10 * x + 15 * y + 5 * z
                if preco_total == total_preco:
                    combinacoes.append((x, y, z))
    return combinacoes

# Botão para calcular
if st.button("🔍 Calcular combinações"):
    pacotes_reportagens = [pacote_5, pacote_10, pacote_15, pacote_20]
    pacotes_escolas = [fotos_escola]

    combinacoes = encontrar_combinacoes(total_preco, total_fotografias, pacotes_reportagens, pacotes_escolas)

    if combinacoes:
        st.success(f"✅ {len(combinacoes)} combinação(ões) encontrada(s):")
        resultado_df = pd.DataFrame(combinacoes, columns=["10€", "15€", "Extras (5€)"])
        st.dataframe(resultado_df)

        # Guardar no histórico
        st.session_state["historico"].append({
            "faturacao": total_preco,
            "fotos": total_fotografias,
            "escolas": fotos_escola,
            "combinacoes": combinacoes
        })

        # Botão para descarregar CSV
        csv = resultado_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Descarregar resultados (.csv)",
            data=csv,
            file_name="combinacoes_fotografias.csv",
            mime="text/csv",
        )
    else:
        st.warning("⚠️ Nenhuma combinação encontrada.")

# Histórico
with st.expander("📜 Ver histórico da sessão"):
    if st.session_state["historico"]:
        for i, h in enumerate(st.session_state["historico"], 1):
            st.markdown(f"**#{i}** - Fotos: `{h['fotos']}` | Faturação: `{h['faturacao']}€` | Escolas: `{h['escolas']}`")
            for comb in h["combinacoes"]:
                st.write(f"• 10€: {comb[0]}, 15€: {comb[1]}, Extras: {comb[2]}")
    else:
        st.write("Ainda sem histórico.")
# Simulação de histórico de combinações
historico = pd.DataFrame({
    'Data': ['2025-04-01', '2025-04-02', '2025-04-03'],
    'Combinação': ['A+B', 'C+D', 'A+B']
})

# Atalhos para ações frequentes - Adicionar combinação igual a ontem
ultimo_dia = historico.iloc[-1]
if st.button("Adicionar combinação igual a ontem"):
    st.text_input("Combinação", ultimo_dia['Combinação'])

# Campo de pesquisa nas combinações já guardadas
search_term = st.text_input('Procurar por combinação')

if search_term:
    resultados = historico[historico['Combinação'].str.contains(search_term, case=False)]
    st.write(resultados)







