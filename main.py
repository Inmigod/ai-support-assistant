"""Rule-based IT troubleshooting prototype (no LLM yet)."""

KNOWLEDGE_BASE = {
    "dns": (("dns", "resolver", "resolução de nome"), [
        "Verifique a conectividade com a rede.",
        "Confira os servidores DNS configurados.",
        "Teste a resolução com nslookup example.com.",
    ]),
    "network": (("internet", "wifi", "wi-fi", "rede", "conexão", "ping"), [
        "Verifique cabos, Wi-Fi e o adaptador de rede.",
        "Confira o IP e o gateway configurados.",
        "Teste a conectividade com o gateway e um endereço público.",
    ]),
    "computer": (("não liga", "nao liga", "computador", "pc", "boot"), [
        "Confira a alimentação elétrica e os cabos.",
        "Observe indicadores e mensagens de inicialização.",
        "Registre os sintomas antes de alterar o equipamento.",
    ]),
}


def diagnose(description: str) -> dict:
    """Classify a support request and return suggested diagnostic steps."""
    if not isinstance(description, str):
        raise TypeError("A descrição deve ser um texto.")
    description = description.strip().casefold()
    if not description:
        raise ValueError("Informe uma descrição do problema.")
    for category, (keywords, steps) in KNOWLEDGE_BASE.items():
        if any(keyword in description for keyword in keywords):
            return {"category": category, "steps": steps, "source": "rules"}
    return {"category": "unknown", "steps": [
        "Informe o sistema operacional, sintomas e mensagens de erro.",
        "Descreva o que já foi testado."], "source": "rules"}


if __name__ == "__main__":
    print("AI Support Assistant | Protótipo inicial")
    try:
        result = diagnose(input("Descreva o problema: "))
        print("Categoria:", result["category"])
        for index, step in enumerate(result["steps"], 1):
            print(f"{index}. {step}")
    except (ValueError, EOFError, KeyboardInterrupt) as error:
        print("Entrada inválida ou cancelada:", error)
