#!/usr/bin/env python3
"""
Meu Tutor — gerador dos códigos Pix (BR Code EMV) da campanha.

Gera um "Pix copia e cola" por faixa de apoio, com valor fixo e CRC16 correto.
Use SEMPRE este script para alterar chave, valores ou faixas — editar o código
à mão invalida o dígito verificador e o banco recusa o pagamento.

    python3 gerar-pix.py

Cole a saída no bloco `const TIERS` do index.html, campo `code:`.
"""

CHAVE  = "contato@meututor.ai"
NOME   = "JTECH HUB SERVICOS"   # máx. 25 caracteres, sem acento
CIDADE = "SAO PAULO"            # máx. 15 caracteres, sem acento

FAIXAS = [
    (18,   "SEMENTE"),
    (50,   "APOIADOR"),
    (120,  "FUNDADORA"),
    (240,  "FUNDPLUS"),
    (490,  "EARLY2027"),
    (1200, "PADRINHO"),
    (3500, "PARCEIRO"),
    (None, "LIVRE"),            # sem valor: o apoiador digita no app do banco
]


def campo(tag: str, valor: str) -> str:
    return f"{tag}{len(valor):02d}{valor}"


def crc16(payload: str) -> str:
    c = 0xFFFF
    for byte in payload.encode():
        c ^= byte << 8
        for _ in range(8):
            c = ((c << 1) ^ 0x1021) & 0xFFFF if c & 0x8000 else (c << 1) & 0xFFFF
    return f"{c:04X}"


def brcode(valor, txid: str) -> str:
    p = (
        campo("00", "01")
        + campo("01", "11")
        + campo("26", campo("00", "BR.GOV.BCB.PIX") + campo("01", CHAVE))
        + campo("52", "0000")
        + campo("53", "986")
    )
    if valor:
        p += campo("54", f"{valor:.2f}")
    p += campo("58", "BR") + campo("59", NOME[:25]) + campo("60", CIDADE[:15])
    p += campo("62", campo("05", txid))
    p += "6304"
    return p + crc16(p)


def validar(codigo: str) -> bool:
    return crc16(codigo[:-4]) == codigo[-4:]


if __name__ == "__main__":
    for valor, txid in FAIXAS:
        codigo = brcode(valor, txid)
        assert validar(codigo), f"CRC inválido em {txid}"
        rotulo = f"R$ {valor}" if valor else "valor livre"
        print(f"\n{txid} ({rotulo})\n{codigo}")
    print(f"\n{len(FAIXAS)} códigos gerados, todos com CRC16 validado.")
