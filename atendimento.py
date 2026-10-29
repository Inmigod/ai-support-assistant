
class Atendimento:
    def __init__(self):
        self.historico = []
        self.testes_realizados = {}
        self.estado = "iniciado"

    def registrar_mensagem(self, autor, mensagem):
        self.historico.append({
            "autor": autor,
            "mensagem": mensagem,
        })

    def registrar_teste(self, ferramenta, resultado, diagnostico):
        self.testes_realizados[ferramenta] = {
            "resultado": resultado,
            "diagnostico": diagnostico,
        }

        self.estado = "investigando"

    def ferramenta_ja_utilizada(self, ferramenta):
        return ferramenta in self.testes_realizados

    def obter_contexto(self):
        return {
            "estado": self.estado,
            "historico": self.historico,
            "testes_realizados": self.testes_realizados,
        }


if __name__ == "__main__":
    atendimento = Atendimento()

    atendimento.registrar_mensagem(
        "cliente",
        "Não consigo acessar sites.",
    )

    atendimento.registrar_teste(
        "verificar_internet",
        {
            "dns": "resolvido",
            "conectividade": "sucesso",
        },
        {
            "estado": "conectividade_parcial_confirmada",
        },
    )

    print("Estado:", atendimento.estado)
    print(
        "Teste já realizado:",
        atendimento.ferramenta_ja_utilizada(
            "verificar_internet"
        ),
    )
    print("Mensagens:", len(atendimento.historico))
