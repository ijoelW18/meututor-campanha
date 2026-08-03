/**
 * Meu Tutor — endpoint de confirmação de apoio da campanha
 * Google Apps Script · grava cada confirmação numa aba do Google Sheets
 *
 * COMO PUBLICAR
 * 1. Crie uma planilha nova no Google Sheets, chamada "Campanha Meu Tutor — Apoios".
 * 2. Extensões → Apps Script. Apague o conteúdo e cole este arquivo.
 * 3. Troque EMAIL_AVISO abaixo, se quiser receber alerta a cada apoio.
 * 4. Implantar → Nova implantação → Tipo: App da Web.
 *      Executar como: Eu
 *      Quem tem acesso: Qualquer pessoa
 * 5. Copie a URL gerada (termina em /exec) e cole em ENDPOINT no index.html.
 * 6. Teste enviando uma confirmação pela própria página.
 *
 * A página envia com mode:'no-cors', então o navegador não lê a resposta —
 * por isso o script nunca precisa devolver cabeçalho CORS. Se algo falhar na
 * rede, a página cai sozinha no fluxo por e-mail e o apoiador não se perde.
 */

const ABA = 'Apoios';
const EMAIL_AVISO = 'contato@meututor.ai';  // deixe '' para não receber aviso

const CABECALHO = [
  'Recebido em', 'Faixa', 'ID da faixa', 'Valor (R$)',
  'Nome', 'E-mail', 'Nome no Mural', 'Origem',
  'Comprovante recebido?', 'Recompensa entregue?', 'Recibo/NF?', 'Observações'
];

function doPost(e) {
  try {
    const d = JSON.parse(e.postData.contents);
    const aba = pegarAba_();

    aba.appendRow([
      new Date(),
      d.faixa || '',
      d.faixaId || '',
      Number(d.valor) || '',
      d.nome || '',
      d.email || '',
      d.mural || '(anônimo)',
      d.origem || 'direto',
      'Não', 'Não', 'Não', ''
    ]);

    if (EMAIL_AVISO) {
      MailApp.sendEmail(
        EMAIL_AVISO,
        'Novo apoio: ' + (d.faixa || '?') + ' — ' + (d.nome || '?'),
        'Faixa: ' + d.faixa + '\n' +
        'Valor: R$ ' + (d.valor || 'livre') + '\n' +
        'Nome: ' + d.nome + '\n' +
        'E-mail: ' + d.email + '\n' +
        'Mural: ' + (d.mural || '(anônimo)') + '\n' +
        'Origem: ' + (d.origem || 'direto') + '\n\n' +
        'Confira o Pix no extrato e marque o comprovante na planilha.'
      );
    }

    return ok_({ ok: true });
  } catch (err) {
    console.error(err);
    return ok_({ ok: false, erro: String(err) });
  }
}

function doGet() {
  return ok_({ ok: true, servico: 'Meu Tutor — confirmações de apoio' });
}

function pegarAba_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let aba = ss.getSheetByName(ABA);
  if (!aba) {
    aba = ss.insertSheet(ABA);
    aba.appendRow(CABECALHO);
    aba.getRange(1, 1, 1, CABECALHO.length).setFontWeight('bold');
    aba.setFrozenRows(1);
  }
  return aba;
}

function ok_(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
