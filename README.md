# Campanha Meu Tutor — página de apoio ao piloto

Página independente da campanha de financiamento coletivo do **Meu Tutor**, com recebimento por **Pix direto** (sem plataforma de crowdfunding).
Não faz parte do site do produto: é um site estático próprio, publicado em subdomínio separado.

**Produção:** https://apoie.meututor.ai *(a definir)*
**Responsável:** JTECH HUB SERVIÇOS · CNPJ 59.750.112/0001-02 · contato@meututor.ai

---

## Como funciona

Um arquivo só. `index.html` contém HTML, CSS e JS — sem build, sem framework, sem `npm install`.

| Dependência externa | Para quê | Se cair |
|---|---|---|
| Google Fonts | Bricolage Grotesque + Plus Jakarta Sans | cai para fonte de sistema; layout sobrevive |
| `qrcodejs` (cdnjs) | desenha o QR Code no modal | o "Pix copia e cola" continua funcionando |

Os **códigos Pix são estáticos e já embutidos** no arquivo, um por faixa de apoio, com valor fixo e CRC16 calculado. Não dependem de rede nem de API.

> ⚠️ **Nunca edite um código Pix à mão.** Cada um termina em 4 dígitos de verificação (CRC16) calculados sobre todo o resto da string. Mudar um centavo invalida o código inteiro e o banco recusa. Para gerar novos, use `backend/gerar-pix.py`.

---

## Estrutura

```
index.html              a página inteira
backend/Code.gs         Google Apps Script que recebe as confirmações de apoio
backend/gerar-pix.py    gera os códigos Pix (BR Code EMV) com CRC16 correto
```

---

## Operação durante a campanha

### Atualizar o progresso

No fim do `index.html`, um único bloco controla os números exibidos:

```js
const CAMPANHA = {
  arrecadado: 0,          // R$ já recebidos
  meta: 20000,
  apoiadores: 0,
  encerra: '2026-09-21'   // AAAA-MM-DD
};
```

Commit + push republica em minutos. Fazer isso **semanalmente** — barra de progresso parada mata a percepção de tração.

### Receber as confirmações de apoio

O formulário do modal tem dois modos:

- **`ENDPOINT = ''`** (padrão) — abre o e-mail do apoiador já preenchido. Funciona sempre, mas perde quem não tem cliente de e-mail no celular.
- **`ENDPOINT = 'https://script.google.com/.../exec'`** — grava direto numa planilha do Google. Se a rede falhar, cai sozinho no modo e-mail.

Para ativar o segundo, siga as instruções no topo de `backend/Code.gs` e cole a URL gerada em `ENDPOINT`.

### Rastrear origem do tráfego

Qualquer link aceita `?origem=`, e o valor vai junto na confirmação:

```
https://apoie.meututor.ai/?origem=whatsapp
https://apoie.meututor.ai/?origem=instagram
https://apoie.meututor.ai/?origem=email-lancamento
```

É assim que se mede o KPI mais importante da campanha: **quantos apoios vieram da comunidade escolar** e não da rede pessoal.

---

## Publicação

Qualquer hospedagem estática serve. Recomendado: **Cloudflare Pages** — build vazio, diretório raiz, domínio próprio grátis e sem limite de banda.

1. Push para o GitHub
2. Cloudflare Pages → Connect to Git → selecionar o repositório
3. Build command: *(vazio)* · Output directory: `/`
4. Custom domain: `apoie.meututor.ai`

Alternativas equivalentes: Netlify, Vercel, GitHub Pages.

---

## Regras invioláveis do projeto

1. **A escola parceira nunca é nomeada.** Nem nome, logo, fachada, endereço ou URL do ambiente escolar — em nenhum texto, imagem ou captura de tela.
2. **Nenhuma criança, família ou aluno é identificado.** Depoimentos sempre anonimizados ("mãe de aluno do 5º ano, escola parceira").
3. **Não se compara o Meu Tutor a professor particular** nem se usa preço de aula particular como argumento. Os quatro pilares, nesta ordem: proximidade · organização · IA-Assistida · suporte diário.
4. **Textos com efeito jurídico não mudam sem revisão:** as respostas do FAQ sobre natureza do apoio e condicionalidade da recompensa, o disclaimer do rodapé e o consentimento do formulário.
5. **Preços vigentes:** R$ 39,99 (1 filho) · R$ 69,99 (até 3 filhos) · Early Features Adopter.

---

## Antes de publicar

- [ ] `CAMPANHA.encerra` com a data real
- [ ] Cada um dos 8 QR Codes testado num app de banco de verdade
- [ ] Recebedor exibido no app confere: JTECH HUB SERVIÇOS
- [ ] `ENDPOINT` configurado, ou ciência de que o fluxo é por e-mail
- [ ] Testado em celular — a maioria vai abrir por link de WhatsApp
- [ ] Autorização da direção da escola obtida
- [ ] Revisão jurídica dos termos concluída
