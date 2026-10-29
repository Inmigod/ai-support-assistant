
import json
from urllib import request, error

from atendimento import Atendimento
from diagnostic_engine import interpretar_resultado
from tools_registry import (
    FERRAMENTAS_PERMITIDAS,
    executar_ferramenta,
)

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "qwen3:1.7b"


def consultar_ia(mensagens):
    payload = {
        "model": MODEL,
        "stream": False,
        "think": False,
        "format": "json",
        "options": {
            "temperature": 0,
            "num_predict": 250,
        },
        "messages": mensagens,
    }

    requisicao = request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with request.urlopen(requisicao, timeout=90) as resposta:
        dados = json.load(resposta)

    resposta_ia = json.loads(dados["message"]["content"])

    if not isinstance(resposta_ia, dict):
        raise ValueError("A IA não retornou um objeto JSON.")

    return resposta_ia


def escolher_ferramenta(problema, atendimento):
    disponiveis = {
        nome: descricao
        for nome, descricao in FERRAMENTAS_PERMITIDAS.items()
        if not atendimento.ferramenta_ja_utilizada(nome)
    }

    if not disponiveis:
        return "nenhuma"

    mensagens = [
        {
            "role": "system",
            "content": (
                "Você seleciona ferramentas de diagnóstico de TI. "
                "Responda somente JSON: "
                '{"ferramenta": "nome"}. '
                "Escolha apenas uma ferramenta disponível. "
                "Se nenhuma for adequada, escolha 'nenhuma'. "
                "Não repita testes realizados. "
                "Ferramentas disponíveis: "
                + json.dumps(disponiveis, ensure_ascii=False)
            ),
        },
        {
            "role": "user",
            "content": json.dumps(
                {
                    "problema": problema,
                    "contexto": atendimento.obter_contexto(),
                },
                ensure_ascii=False,
            ),
        },
    ]

    resposta = consultar_ia(mensagens)
    ferramenta = resposta.get("ferramenta")

    return ferramenta if ferramenta in disponiveis else "nenhuma"


def responder_cliente(atendimento):
    mensagens = [
        {
            "role": "system",
            "content": (
                "Você é um agente profissional de suporte de TI. "
                "Responda somente JSON: "
                '{"resposta": "texto"}. '
                "Use português brasileiro e no máximo 2 frases. "
                "Seja natural e objetivo. "
                "Não invente resultados ou correções. "
                "Não declare o problema resolvido sem confirmação. "
                "Não conclua que a internet caiu apenas porque "
                "o gateway não respondeu ao ping. "
                "Se os testes não explicarem o problema, "
                "faça apenas uma pergunta objetiva ao cliente."
            ),
        },
        {
            "role": "user",
            "content": json.dumps(
                atendimento.obter_contexto(),
                ensure_ascii=False,
            ),
        },
    ]

    resposta = consultar_ia(mensagens)
    texto = resposta.get("resposta", "")

    if not isinstance(texto, str) or not texto.strip():
        return "Ainda não consegui concluir o diagnóstico."

    return texto.strip()


def iniciar_atendimento():
    atendimento = Atendimento()

    print("\nAI Support Assistant")
    print("Atendimento inteligente de TI")
    print("Digite 'sair' para encerrar.\n")

    while True:
        try:
            problema = input("Cliente: ").strip()

            if problema.lower() == "sair":
                print("Atendimento encerrado.")
                break

            if not problema:
                continue

            atendimento.registrar_mensagem("cliente", problema)

            ferramenta = escolher_ferramenta(
                problema,
                atendimento,
            )

            if ferramenta != "nenhuma":
                print(f"\nDiagnóstico sugerido: {ferramenta}")

                autorizacao = input(
                    "Autoriza executar? (s/n): "
                ).strip().lower()

                if autorizacao == "s":
                    resultado = executar_ferramenta(ferramenta)

                    if resultado.get("status") == "bloqueado":
                        print("Ferramenta bloqueada.")
                        continue

                    diagnostico = interpretar_resultado(
                        ferramenta,
                        resultado,
                    )

                    atendimento.registrar_teste(
                        ferramenta,
                        resultado,
                        diagnostico,
                    )

                    print("\nDiagnóstico:")
                    print(json.dumps(
                        diagnostico,
                        indent=2,
                        ensure_ascii=False,
                    ))
                else:
                    print("Diagnóstico não autorizado.")

            resposta = responder_cliente(atendimento)

            atendimento.registrar_mensagem(
                "assistente",
                resposta,
            )

            print(f"\nAssistente: {resposta}\n")

        except (
            error.URLError,
            TimeoutError,
            OSError,
            ValueError,
            KeyError,
            TypeError,
        ) as erro:
            print(f"\nErro: {erro}\n")


if __name__ == "__main__":
    iniciar_atendimento()
