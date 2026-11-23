"""Adaptador WSGI para hospedar o site com Gunicorn."""

from http import HTTPStatus

from servidor import responder_calculo, resposta_json, servir_arquivo


def aplicacao(ambiente, iniciar_resposta):
    # WSGI fornece o método, a rota, os cabeçalhos e o corpo da requisição.
    metodo = ambiente["REQUEST_METHOD"]
    rota = ambiente["PATH_INFO"]

    if metodo in ("GET", "HEAD"):
        status, tipo, conteudo = servir_arquivo(rota)
    elif metodo == "POST":
        tipo_entrada = ambiente.get("CONTENT_TYPE", "").split(";", 1)[0].strip().lower()
        status, tipo, conteudo = responder_calculo(
            rota, tipo_entrada, ambiente.get("CONTENT_LENGTH"), ambiente["wsgi.input"].read
        )
    else:
        status, tipo, conteudo = resposta_json(405, {"erro": "Método não permitido."})

    cabecalhos = [
        ("Content-Type", tipo),
        ("Content-Length", str(len(conteudo))),
        ("X-Content-Type-Options", "nosniff"),
    ]
    if status == 405:
        cabecalhos.append(("Allow", "GET, HEAD, POST"))
    iniciar_resposta(f"{status} {HTTPStatus(status).phrase}", cabecalhos)
    if metodo == "HEAD":
        return []
    return [conteudo]
