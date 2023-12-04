import time

import requests

import helpers
from helpers import check_for_captcha


def get(url, retries=3, wait=300):
    user_agent = {
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    trials = 0
    while trials < retries:
        time.sleep(wait * trials)
        html = requests.get(url, headers=user_agent, verify=False)
        html.encoding = "utf-8"
        if check_for_captcha(html.text):
            # try again
            trials += 1
            continue
        else:
            # finish loop
            break
    if html.status_code != 200:
        return {"error_status_code": html.status_code}
    else:
        return html.json()


def get_pauta_presencial(data):
    url_presencial = "https://portal.stf.jus.br/pauta/services/calendario-service.asp?dados=sessao-presencial&data={}"
    url = url_presencial.format(data)
    return get(url)


def get_pauta_virtual(data):
    url_virtual = "https://portal.stf.jus.br/pauta/services/calendario-service.asp?dados=sessao-virtual&inicio={}&fim={}"
    url = url_virtual.format(data["dataInicial"], data["dataFinal"])
    return get(url)


def get_info_lista(id_lista):
    url = "https://portal.stf.jus.br/pauta/services/lista-service.asp?lista="
    url += str(id_lista)
    return get(url)


def get_votacoes_proc(soi):
    url = f"https://sistemas.stf.jus.br/repgeral/votacao?oi={soi}"
    response = get(url)
    if "error_status_code" in response:
        response["objetoIncidente"] = {"principal": int(soi)}
        return [response]
    else:
        return response


def get_info_votacao(id_sessao):
    url = f"https://sistemas.stf.jus.br/repgeral/votacao?sessaoVirtual={id_sessao}"
    return get(url)


def collect_composicao_listas(listas):
    composicao_listas = dict()
    sois_em_listas = set()

    for lista in listas:
        id_lista = lista.get("id")
        try:
            procs_lista = get_info_lista(id_lista)
            composicao_listas[id_lista] = procs_lista
            for proc in procs_lista:
                soi = proc["id"]
                sois_em_listas.add(soi)
        except Exception as e:
            print("Erro ao coletar lista:", id_lista, e)
            continue
    # save composicao_listas to zip
    helpers.save_json_to_zip(composicao_listas, "composicao_listas")
    # return unique sois
    return sois_em_listas


def collect_votacoes_sois(sois):
    votacoes_proc = list()
    ids_votacoes = set()
    # coleta relacoes entre soi e votacoes
    for soi in sois:
        try:
            vots = get_votacoes_proc(soi)
            votacoes_proc.extend(vots)
        except Exception as e:
            print("Erro ao coletar votacoes:", soi, e)
            continue
        for vot in vots:
            # checa se requisição gerou erro
            if "error_status_code" in vot:
                continue
            ids_votacoes.add(vot["objetoIncidente"]["id"])
    helpers.save_json_to_zip(votacoes_proc, 'votacoes_proc')

    # coleta votacoes
    info_votacoes = list()
    for id_votacao in ids_votacoes:
        try:
            info_vot = get_info_votacao(id_votacao)
            info_votacoes.append(info_vot)
        except Exception as e:
            print("Erro ao coletar info votacao:", id_votacao, e)
            continue

    helpers.save_json_to_zip(info_votacoes, 'info_votacoes')
    return info_votacoes
