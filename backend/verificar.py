#!/usr/bin/env python3
"""
Meu Tutor — verificação de integridade da página da campanha.

Rode DEPOIS de qualquer alteração no index.html e ANTES de qualquer commit:

    python3 backend/verificar.py

Sai com código 1 se algo estiver errado.
"""
import re
import sys
from pathlib import Path

PAGINA = Path(__file__).resolve().parent.parent / "index.html"

# Textos que não podem desaparecer da página, por decisão de produto ou jurídica.
OBRIGATORIOS = [
    "IA-Assistida",
    "Os pais continuam sendo pais",
    "não substitui nenhum professor",
    "Proximidade", "Organização", "Suporte diário",
    "JTECH HUB SERVIÇOS",
    "59.750.112/0001-02",
    "não divulgamos o nome da escola parceira",
    "Não constitui investimento",
    "consentimento expresso de um responsável legal",
    "Lei nº 13.709/2018",
]

# Nada disso pode voltar à página.
PROIBIDOS = [
    "aula particular",
    "professor particular",
    "IA-ssistida",          # grafia antiga
    "Substituir por 2 linhas",
    "29,90", "49,90", "89,90",   # preços antigos
]


def crc16(payload: str) -> str:
    c = 0xFFFF
    for byte in payload.encode():
        c ^= byte << 8
        for _ in range(8):
            c = ((c << 1) ^ 0x1021) & 0xFFFF if c & 0x8000 else (c << 1) & 0xFFFF
    return f"{c:04X}"


def main() -> int:
    if not PAGINA.exists():
        print(f"ERRO: {PAGINA} não encontrado")
        return 1

    h = PAGINA.read_text(encoding="utf-8")
    erros, avisos = [], []

    # 1. Códigos Pix
    codigos = re.findall(r"code:'([^']+)'", h)
    if len(codigos) != 8:
        erros.append(f"esperados 8 códigos Pix, encontrados {len(codigos)}")
    for c in codigos:
        if crc16(c[:-4]) != c[-4:]:
            erros.append(f"CRC16 inválido no código Pix ...{c[-24:]}")
    if "contato@meututor.ai" not in "".join(codigos):
        erros.append("a chave Pix não aparece nos códigos")

    # 2. Estrutura do HTML
    if h.count("<div") != h.count("</div>"):
        erros.append(f"<div> desbalanceadas: {h.count('<div')} abertas, {h.count('</div>')} fechadas")
    if h.count("<section") != h.count("</section>"):
        erros.append("<section> desbalanceadas")
    for tag in ("html", "head", "body", "style", "script"):
        if h.count(f"<{tag}") < 1 or h.count(f"</{tag}>") < 1:
            erros.append(f"tag <{tag}> ausente ou não fechada")

    # 3. Conteúdo obrigatório
    for t in OBRIGATORIOS:
        if t not in h:
            erros.append(f"texto obrigatório ausente: {t!r}")

    # 4. Conteúdo proibido (ignora comentários HTML)
    visivel = re.sub(r"<!--.*?-->", "", h, flags=re.S)
    for t in PROIBIDOS:
        if t in visivel:
            erros.append(f"texto proibido presente: {t!r}")

    # 5. Configuração
    if "const CAMPANHA" not in h:
        erros.append("bloco const CAMPANHA ausente")
    if "const ENDPOINT" not in h:
        avisos.append("const ENDPOINT ausente — o formulário não terá backend")
    elif re.search(r"const ENDPOINT\s*=\s*''", h):
        avisos.append("ENDPOINT vazio — as confirmações vão pelo fluxo de e-mail")

    # 6. Arquivo único
    if re.search(r'<link[^>]+rel="stylesheet"[^>]+href="(?!https://fonts)', h):
        avisos.append("há CSS externo além do Google Fonts — a página deve ser arquivo único")

    for a in avisos:
        print(f"aviso:  {a}")
    if erros:
        print()
        for e in erros:
            print(f"ERRO:   {e}")
        print(f"\n{len(erros)} erro(s). Não faça commit assim.")
        return 1

    print(f"\nOK — 8 códigos Pix válidos, estrutura íntegra, "
          f"{len(OBRIGATORIOS)} textos obrigatórios presentes, nenhum texto proibido.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
