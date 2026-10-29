
from network_checks import (
    identificar_gateway,
    testar_gateway,
    testar_tcp,
)


# Ferramentas que a IA pode solicitar
FERRAMENTAS_PERMITIDAS = {
    "verificar_gateway": "Verifica a resposta ICMP do gateway.",
    "verificar_internet": "Testa DNS e conexão TCP HTTPS.",
}


def executar_ferramenta(nome):
    """Executa apenas ferramentas autorizadas."""

    if nome == "verificar_gateway":
        gateway = identificar_gateway()

        if not gateway:
            return {
                "teste": "gateway",
                "status": "nao_identificado",
            }

        return testar_gateway(gateway)

    if nome == "verificar_internet":
        return testar_tcp()

    return {
        "status": "bloqueado",
        "motivo": "Ferramenta não autorizada.",
    }


if __name__ == "__main__":
    print("Ferramentas disponíveis:")
    for nome, descricao in FERRAMENTAS_PERMITIDAS.items():
        print(f"- {nome}: {descricao}")

    print("\nTeste de segurança:")
    print(executar_ferramenta("formatar_computador"))
