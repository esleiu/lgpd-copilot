from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.pipeline.rag import LgpdRagPipeline
from src.pipeline.routing import ModelRouter


st.set_page_config(page_title="LGPD Copilot", page_icon="⚖️", layout="wide")


@st.cache_resource
def load_pipeline() -> LgpdRagPipeline:
    return LgpdRagPipeline()


pipeline = load_pipeline()

st.title("LGPD Copilot")
st.caption("Assistente RAG para duvidas de compliance em produtos digitais.")

with st.sidebar:
    st.header("Metricas da sessao")
    stats = st.session_state.setdefault("stats", {"strong": 0, "cheap": 0, "cache": 0})
    reduction = ModelRouter.estimate_cost_reduction(stats["strong"], stats["cheap"], stats["cache"])
    st.metric("Reducao estimada de custo", f"{reduction}%")
    st.write(f"Chamadas cheap: {stats['cheap']}")
    st.write(f"Chamadas strong: {stats['strong']}")
    st.write(f"Cache hits: {stats['cache']}")
    st.divider()
    st.write("Perguntas de teste")
    examples = [
        "Posso armazenar CPF para emitir nota fiscal e prevenir fraude?",
        "Quais direitos o usuario tem se pedir exclusao dos dados?",
        "Cite o Art. 46 e explique medidas tecnicas para um app.",
        "Quando posso manter dados apos o fim do contrato?",
        "O que fazer se ocorrer vazamento de dados pessoais?",
    ]
    for example in examples:
        if st.button(example, use_container_width=True):
            st.session_state["pending_question"] = example

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Pergunte sobre LGPD, bases legais, direitos do titular, retencao, incidentes ou medidas de seguranca.",
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ex.: Posso guardar CPF em logs de auditoria?")
if st.session_state.get("pending_question"):
    question = st.session_state.pop("pending_question")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Consultando corpus, cache e ferramenta LGPD..."):
            result = pipeline.ask(question)
            answer = result["answer"]
            st.markdown(answer)

            route = result.get("route")
            if route == "cache":
                st.session_state.stats["cache"] += 1
            elif route in {"cheap", "strong"}:
                st.session_state.stats[route] += 1

            with st.expander("Fontes recuperadas e telemetria"):
                st.write(
                    {
                        "route": result.get("route"),
                        "model": result.get("model"),
                        "cache_hit": result.get("cache_hit"),
                        "route_reason": result.get("route_reason"),
                    }
                )
                for source in result.get("sources", []):
                    st.markdown(
                        f"**{source['source']}** · {source['page_hint']} · score `{source['score']}`\n\n"
                        f"{source['preview']}..."
                    )

    st.session_state.messages.append({"role": "assistant", "content": answer})
