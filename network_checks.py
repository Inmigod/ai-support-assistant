
import json
import socket
import subprocess


def testar_gateway(gateway):
    """Verifica se o gateway responde ao ping."""
    try:
        resultado = subprocess.run(
            ["ping", "-n", "2", "-w", "1000", gateway],
            capture_output=True,
            text=True,
            encoding="cp850",
            errors="replace",
            timeout=20,
            shell=False,
        )

        return {
            "teste": "gateway",
            "status": (
                "respondendo"
                if resultado.returncode == 0
                else "sem_resposta"
            ),
        }

    except (OSError, subprocess.TimeoutExpired) as erro:
        return {
            "teste": "gateway",
            "status": "erro",
            "detalhes": str(erro),
        }


def identificar_gateway():
    """Identifica o gateway IPv4 padrão do Windows."""
    try:
        resultado = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "(Get-NetRoute -AddressFamily IPv4 "
                "-DestinationPrefix '0.0.0.0/0' | "
                "Sort-Object RouteMetric, InterfaceMetric | "
                "Select-Object -First 1).NextHop",
            ],
            capture_output=True,
            text=True,
            timeout=10,
            errors="replace",
            shell=False,
        )

        if resultado.returncode != 0:
            return None

        return resultado.stdout.strip() or None

    except (OSError, subprocess.TimeoutExpired):
        return None


def testar_tcp(host="www.microsoft.com", porta=443):
    """Testa resolução DNS e conexão TCP."""
    try:
        socket.getaddrinfo(
            host,
            porta,
            type=socket.SOCK_STREAM,
        )

    except socket.gaierror:
        return {
            "teste": "tcp",
            "dns": "falhou",
            "conectividade": "nao_testada",
        }

    try:
        with socket.create_connection(
            (host, porta), timeout=5
        ):
            return {
                "teste": "tcp",
                "dns": "resolvido",
                "conectividade": "sucesso",
            }

    except OSError:
        return {
            "teste": "tcp",
            "dns": "resolvido",
            "conectividade": "falhou",
        }


def executar_diagnostico():
    """Reúne os resultados dos testes de rede."""
    gateway = identificar_gateway()

    return {
        "gateway_icmp": (
            testar_gateway(gateway)
            if gateway
            else {
                "teste": "gateway",
                "status": "nao_identificado",
            }
        ),
        "internet_tcp": testar_tcp(),
    }


if __name__ == "__main__":
    resultados = executar_diagnostico()

    print(json.dumps(
        resultados,
        indent=2,
        ensure_ascii=False,
    ))
