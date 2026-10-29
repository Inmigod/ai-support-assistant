
import json


def interpretar_resultado(ferramenta, resultado):
    """Interpreta evidências sem depender da IA."""

    if ferramenta == "verificar_internet":
        dns = resultado.get("dns")
        tcp = resultado.get("conectividade")

        if dns == "falhou":
            return {
                "estado": "falha_dns",
                "conclusao": "Falha na resolução DNS do domínio testado.",
                "proximo_passo": "Investigar a configuração DNS.",
            }

        if dns == "resolvido" and tcp == "sucesso":
            return {
                "estado": "conectividade_parcial_confirmada",
                "conclusao": (
                    "O domínio testado foi resolvido e "
                    "a conexão TCP na porta 443 funcionou."
                ),
                "proximo_passo": (
                    "Se o usuário ainda não acessa sites, "
                    "investigar o endereço ou aplicativo afetado."
                ),
            }

        return {
            "estado": "falha_tcp",
            "conclusao": (
                "O DNS funcionou, mas a conexão TCP "
                "ao destino testado não foi estabelecida."
            ),
            "proximo_passo": "Investigar a conectividade TCP.",
        }

    if ferramenta == "verificar_gateway":
        status = resultado.get("status")

        if status == "respondendo":
            conclusao = "O gateway respondeu ao teste ICMP."
        elif status == "sem_resposta":
            conclusao = (
                "O gateway não respondeu ao ICMP. "
                "Isso não comprova falha de internet."
            )
        else:
            conclusao = "O teste do gateway não foi concluído."

        return {
            "estado": status,
            "conclusao": conclusao,
            "proximo_passo": "Avaliar outros testes de conectividade.",
        }

    return {
        "estado": "desconhecido",
        "conclusao": "Não há interpretação disponível.",
        "proximo_passo": "Solicitar análise técnica.",
    }


if __name__ == "__main__":
    exemplo = {
        "teste": "tcp",
        "dns": "resolvido",
        "conectividade": "sucesso",
    }

    print(json.dumps(
        interpretar_resultado("verificar_internet", exemplo),
        indent=2,
        ensure_ascii=False,
    ))
