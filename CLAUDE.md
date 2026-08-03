# Instruções para agentes de código neste repositório

## Regra número um

**`index.html` NÃO deve ser reescrito, regenerado ou recriado.**

Este arquivo passou por revisão de texto linha a linha com o fundador e por revisão de conformidade. Cada frase é deliberada. Ele não é um rascunho a ser melhorado.

- ✅ Permitido: edições cirúrgicas e pontuais, uma alteração de cada vez, preservando todo o resto do arquivo.
- ❌ Proibido: gerar um `index.html` novo "do zero", "modernizar", converter para framework, separar CSS/JS em arquivos, reformatar, reindentar ou reescrever textos "para melhorar".

Se uma tarefa parecer exigir reescrever a página, **pare e pergunte**. É quase certo que existe um caminho cirúrgico.

## Como verificar que nada quebrou

Depois de qualquer alteração no `index.html`, rode:

```bash
python3 backend/verificar.py
```

Ele confere os 8 códigos Pix (CRC16), a integridade do HTML e a presença dos textos que não podem sumir. **Nenhum commit sobe com esse script falhando.**

## Conteúdo — regras invioláveis

1. **A escola parceira nunca é nomeada.** Nem nome, logo, fachada, endereço ou URL do ambiente escolar, em nenhum lugar.
2. **Nenhuma criança, família ou aluno identificado.** Depoimentos sempre anonimizados.
3. **Nunca comparar o produto a professor particular** nem citar preço de aula particular. Os quatro pilares, nesta ordem: **proximidade · organização · IA-Assistida · suporte diário**.
4. **Grafia da marca:** "IA-Assistida", sempre com hífen e maiúscula.
5. **Preços:** R$ 39,99 (1 filho) · R$ 69,99 (até 3 filhos) · Early Features Adopter.

## Textos com efeito jurídico — não alterar sem sinalizar

- Respostas do FAQ sobre natureza do apoio ("Isso é investimento?") e condicionalidade da recompensa ("Se o produto não lançar...")
- Disclaimer do rodapé
- Texto de consentimento abaixo do formulário de confirmação
- Identificação do recebedor: JTECH HUB SERVIÇOS · CNPJ 59.750.112/0001-02

Se alguma tarefa exigir mexer nestes, avise explicitamente antes.

## Códigos Pix

Os 8 códigos no bloco `const TIERS` são BR Code EMV com **CRC16** nos 4 últimos dígitos, calculado sobre toda a string. Editar um caractere invalida o código e o banco recusa o pagamento.

Para alterar chave, valores ou faixas: editar `backend/gerar-pix.py` e rodar `python3 backend/gerar-pix.py`. Nunca à mão.

## Arquitetura — decisões já tomadas

- **Arquivo único.** HTML, CSS e JS juntos em `index.html`. Sem build, sem npm, sem framework, sem bundler. É intencional: a página precisa ser publicável e editável por qualquer pessoa, em qualquer lugar, durante os dois meses da campanha.
- Dependências externas: apenas Google Fonts e `qrcodejs` via CDN. Não adicionar outras.
- Configuração da campanha: bloco `const CAMPANHA` no fim do arquivo.
- Endpoint das confirmações: `const ENDPOINT` — vazio significa fluxo por e-mail.
