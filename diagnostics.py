
import json
import platform
import socket
import subprocess


def executar_comando(comando):
    """Executa somente comandos definidos pelo programa."""
    try:
        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            encoding="cp850",
            timeout=10,
            shell=False,
            errors="replace",
        )
        return resultado.stdout.strip() or resultado.stderr.strip()
    except (OSError, subprocess.TimeoutExpired) as erro:
        return f"Erro ao executar diagnóstico: {erro}"


def mapear_computador():
    """Coleta informações básicas do computador local."""
    dados = {
        "hostname": socket.gethostname(),
        "sistema": platform.system(),
        "versao": platform.release(),
        "arquitetura": platform.machine(),
        "rede": {},
    }

    if platform.system() == "Windows":
        dados["rede"]["configuracao"] = executar_comando(
            ["ipconfig", "/all"]
        )
    elif platform.system() == "Linux":
        dados["rede"]["configuracao"] = executar_comando(
            ["ip", "-brief", "address"]
        )

    return dados


if __name__ == "__main__":
    print(json.dumps(
        mapear_computador(),
        indent=2,
        ensure_ascii=False,
    ))
