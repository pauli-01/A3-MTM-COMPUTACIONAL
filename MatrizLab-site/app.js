// A interface coleta os dados e desenha a explicação. Todo cálculo vem do Python.
import { PythonClient } from './python-client.js';
const $ = (id) => document.getElementById(id);
const example = {a: [[1, 2, 3], [4, 5, 6]], b: [[7, 8], [9, 10], [11, 12]]};
const state = {a: [], b: [], response: null, selected: 0, revision: 0, apiBase: '', mode: 'browser', configReady: false};
let guideIndex = null;
let calculating = false;
let python;
let request;

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function populateSelects() {
  for (const matrix of ['a', 'b']) {
    for (const axis of ['rows', 'cols']) {
      for (let size = 1; size <= 6; size++) {
        $(axis + '-' + matrix).append(new Option(size, size));
      }
      $(axis + '-' + matrix).addEventListener('change', () => {
        const rows = Number($('rows-' + matrix).value);
        const cols = Number($('cols-' + matrix).value);
        state[matrix] = Array.from({length: rows}, (_, i) =>
          Array.from({length: cols}, (_, j) => state[matrix][i]?.[j] ?? ''));
        invalidate();
        drawInput(matrix);
        showDimensions();
      });
    }
  }
}

function drawInput(matrix) {
  const grid = $('grid-' + matrix);
  const cols = state[matrix][0].length;
  grid.replaceChildren();
  grid.style.setProperty('--cols', cols);
  grid.classList.toggle('dense', cols > 4);
  grid.closest('.matrix-scroll').classList.toggle('wide-matrix',cols>4);
  grid.closest('.matrix-scroll').tabIndex = cols > 4 ? 0 : -1;
  grid.closest('.matrix-scroll').setAttribute('aria-label', cols > 4 ? 'Matriz larga: role horizontalmente para ver todas as colunas' : 'Matriz');
  state[matrix].forEach((row, i) => row.forEach((value, j) => {
    const input = document.createElement('input');
    input.type = 'text';
    input.inputMode = 'decimal';
    input.autocomplete = 'off';
    input.spellcheck = false;
    input.maxLength = 32;
    input.value = String(value);
    input.placeholder = '0';
    input.id = `cell-${matrix}-${i}-${j}`;
    input.dataset.row = i;
    input.dataset.col = j;
    input.setAttribute('aria-label', `Matriz ${matrix.toUpperCase()}, linha ${i + 1}, coluna ${j + 1}`);
    input.addEventListener('input', () => {
      state[matrix][i][j] = input.value;
      invalidate();
    });
    input.addEventListener('keydown', (event) => {
      if (event.key === 'Enter') calculate();
    });
    grid.append(input);
  }));
}

function showDimensions() {
  const [m, n, r, p] = [state.a.length, state.a[0].length, state.b.length, state.b[0].length];
  $('shape-a').textContent = `${m} × ${n}`;
  $('shape-b').textContent = `${r} × ${p}`;
  $('shape-c').textContent = n === r ? `${m} × ${p}` : '—';
  const compatible = n === r;
  for (const id of ['cols-a','rows-b']) {$(id).setAttribute('aria-invalid',String(!compatible)); $(id).setAttribute('aria-describedby','compatibility');}
  updateCalculateButton();
  $('compatibility').classList.toggle('incompatible', !compatible);
  $('compatibility').replaceChildren(
    element('span', 'check', compatible ? '✓' : '!'),
    element('span', '', compatible
      ? `Dimensões compatíveis: ${n} coluna(s) de A = ${r} linha(s) de B.`
      : `A tem ${n} coluna(s) e B tem ${r} linha(s). Ajuste esses valores para ficarem iguais.`)
  );
}

function invalidate() {
  guideIndex = null;
  calculating = false;
  document.body.classList.remove('presenting');
  $('present').textContent = 'Modo apresentação';
  $('present').setAttribute('aria-pressed','false');
  clearFieldErrors();
  $('export-status').textContent = '';
  state.revision++;
  request?.abort();
  state.response = null;
  $("result-stage").hidden = true;
  $("all-calculations").hidden = true;
  $('error').hidden = true;
  updateCalculateButton();
  $('calculate').replaceChildren(document.createTextNode('Calcular A × B '), element('span', '', '→'));
  $('result-empty').hidden = false;
  $('result-wrap').hidden = true;
  $('grid-c').replaceChildren();
  $('step-empty').hidden = false;
  $('step-content').hidden = true;
  $('step-counter').textContent = 'Explore o resultado';
  $('result-count').textContent = 'A × B';
  document.querySelectorAll('input.highlight').forEach(input => input.classList.remove('highlight'));
}

function loadExample() {
  invalidate();
  for (const matrix of ['a', 'b']) {
    state[matrix] = example[matrix].map(row => row.map(String));
    $('rows-' + matrix).value = state[matrix].length;
    $('cols-' + matrix).value = state[matrix][0].length;
    drawInput(matrix);
  }
  showDimensions();
  if (state.configReady && compatible()) calculate();
}

function setStatus(message, status) {
  $('runtime-status').textContent = message;
  $('runtime-dot').className = 'runtime-dot ' + status;
}

async function calculate() {
  if (!state.configReady || !compatible() || calculating) return;
  calculating = true;
  clearFieldErrors();
  request?.abort();
  request = new AbortController();
  const controller = request;
  const revision = ++state.revision;
  const timer = setTimeout(() => controller.abort('timeout'), 45000);
  $('error').hidden = true;
  $('calculate').disabled = true;
  $('calculate').textContent = 'Calculando…';
  setStatus('Python está calculando…', '');
  try {
    let data;
    if (state.mode === 'browser') {
      data = await python.calculate(state.a, state.b);
    } else {
      const response = await fetch(state.apiBase + '/api/multiplicar', {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({a: state.a, b: state.b}), signal: controller.signal
      });
      data = await response.json();
      if (!response.ok) throw new Error(data.erro || 'Não foi possível calcular essas matrizes.');
    }
    if (state.revision !== revision) return;
    state.response = data;
    state.selected = 0;
    guideIndex = null;
    drawResult();
    showStep();
    setStatus(state.mode === 'browser' ? 'Python pronto · executando no navegador' : 'Python conectado · cálculo no servidor', 'ready');
  } catch (error) {
    if (state.revision !== revision) return;
    const networkError = error instanceof TypeError || controller.signal.aborted || error instanceof SyntaxError;
    $('error').textContent = networkError
      ? 'O servidor está iniciando ou não respondeu. Aguarde alguns segundos e clique em Calcular novamente.'
      : error.message;
    $('error').hidden = false;
    focusInvalidField(error.message);
    setStatus(networkError ? 'Aguardando conexão com o Python' : 'Confira os dados das matrizes', networkError ? 'offline' : '');
  } finally {
    clearTimeout(timer);
    if (state.revision === revision) {
      calculating = false;
      updateCalculateButton();
      $('calculate').replaceChildren(document.createTextNode('Calcular A × B '), element('span', '', '→'));
    }
  }
}

function drawResult() {
  const data = state.response;
  $('result-stage').hidden = false;
  $('all-calculations').hidden = false;
  for (const matrix of ['a', 'b']) {
    const grid = $('read-' + matrix);
    grid.replaceChildren();
    grid.style.setProperty('--cols', data.dimensoes[matrix][1]);
    grid.classList.toggle('dense', data.dimensoes[matrix][1] > 4);
    $('read-shape-' + matrix).textContent = data.dimensoes[matrix].join(' × ');
    state[matrix].forEach((row,i) => row.forEach((value,j) => {
      const cell = element('span', 'read-cell', String(value));
      cell.dataset.row = i; cell.dataset.col = j;
      grid.append(cell);
    }));
  }
  $('all-steps').replaceChildren();
  data.passos.forEach((step,index) => {
    const button = element('button','calculation-row');
    button.type = 'button';
    button.append(element('strong','',`C[${step.linha}, ${step.coluna}]`),element('span','',step.expressao));
    button.addEventListener('click',()=>{state.selected=index;guideIndex=null;showStep();});
    $('all-steps').append(button);
  });
  const cols = data.dimensoes.c[1];
  $('grid-c').replaceChildren();
  $('grid-c').style.setProperty('--cols', cols);
  $('grid-c').classList.toggle('dense', cols > 4);
  for (const [index, step] of data.passos.entries()) {
    const button = element('button', '', step.valor);
    button.type = 'button';
    button.setAttribute('aria-label', `C, linha ${step.linha}, coluna ${step.coluna}: ${step.valor}. Ver cálculo.`);
    button.addEventListener('click', () => {state.selected = index; guideIndex=null; showStep();});
    $('grid-c').append(button);
  }
  $('result-empty').hidden = true;
  $('result-wrap').hidden = false;
  $('result-count').textContent = `${data.passos.length} elemento(s) calculado(s)`;
}

function showStep() {
  const step = state.response.passos[state.selected];
  $('step-empty').hidden = true;
  $('step-content').hidden = false;
  $('step-counter').textContent = `Elemento ${state.selected + 1} de ${state.response.passos.length}`;
  $('step-title').textContent = `C[${step.linha}, ${step.coluna}] = ${step.valor}`;
  $('step-description').replaceChildren(
    document.createTextNode('Combinamos a '), element('strong', 'a-text', `linha ${step.linha} de A`),
    document.createTextNode(' com a '), element('strong', 'b-text', `coluna ${step.coluna} de B`),
    document.createTextNode('.'));
  for (const matrix of ['a', 'b']) {
    $('grid-' + matrix).querySelectorAll('input').forEach(input => {
      input.classList.toggle('highlight', matrix === 'a'
        ? Number(input.dataset.row) === step.linha - 1 : Number(input.dataset.col) === step.coluna - 1);
    });
  }
  [...$('grid-c').children].forEach((button, index) => {
    const active = index === state.selected;
    button.classList.toggle('selected', active);
    button.setAttribute('aria-pressed', String(active));
  });
  for (const matrix of ['a','b']) {
    $('read-' + matrix).querySelectorAll('.read-cell').forEach(cell => {
      cell.classList.toggle('highlight', matrix === 'a' ? Number(cell.dataset.row) === step.linha - 1 : Number(cell.dataset.col) === step.coluna - 1);
    });
  }
  [...$('all-steps').children].forEach((button,index)=>{button.classList.toggle('selected',index===state.selected);button.setAttribute('aria-pressed',String(index===state.selected));});
  $('terms').replaceChildren();
  step.termos.forEach((term, index) => {
    if (index > 0) $('terms').append(element('span', 'plus', '+'));
    const container = element('div', 'term');
    const expression = element('div', 'term-expression');
    expression.append(element('span', 'a-text', term.a), element('span', 'multiply', '×'), element('span', 'b-text', term.b));
    container.append(expression, element('span', 'term-product', '= ' + term.produto));
    $('terms').append(container);
  });
  $('sum').replaceChildren(
    element('span', '', step.termos.map(term => Number(term.produto.replace(',', '.')) < 0 ? `(${term.produto})` : term.produto).join(' + ') + ' ='),
    element('strong', 'total', step.valor)
  );
  $('previous').disabled = state.selected === 0;
  $('next').disabled = state.selected === state.response.passos.length - 1;
  renderGuide();
}

$('example').addEventListener('click', loadExample);
$('clear').addEventListener('click', () => {
  invalidate();
  for (const matrix of ['a', 'b']) {
    state[matrix] = state[matrix].map(row => row.map(() => ''));
    drawInput(matrix);
  }
  setStatus('Preencha as matrizes para calcular', '');
  $('grid-a').querySelector('input').focus();
});
$('calculate').addEventListener('click', calculate);
$('previous').addEventListener('click', () => {if (state.selected > 0) {state.selected--; guideIndex=null; showStep();}});
$('next').addEventListener('click', () => {if (state.response && state.selected < state.response.passos.length - 1) {state.selected++; guideIndex=null; showStep();}});
populateSelects();
loadExample();
try {
  const configResponse = await fetch('./config.json', {cache: 'no-store'});
  if (!configResponse.ok) throw new Error('Configuração indisponível');
  const config = await configResponse.json();
  state.mode = config.mode || 'server';
  state.apiBase = (config.apiBase || '').replace(/\/$/, '');
  if (state.mode === 'browser') {
    setStatus('Carregando Python… O primeiro acesso pode levar alguns segundos.', '');
    $('calculate').disabled = true;
    python = new PythonClient();
    await python.ready;
  }
  state.configReady = true;
  await calculate();
} catch {
  setStatus('Não foi possível carregar o Python. Atualize a página para tentar novamente.', 'offline');
  $('error').textContent = 'O ambiente de cálculo não carregou. Confira sua conexão e atualize a página.';
  $('error').hidden = false;
}

function compatible() {return state.a[0]?.length === state.b.length;}
function updateCalculateButton() {$('calculate').disabled = !state.configReady || !compatible() || calculating;}
function clearFieldErrors() {
  document.querySelectorAll('.invalid-cell').forEach(input => {input.classList.remove('invalid-cell');input.removeAttribute('aria-invalid');input.removeAttribute('aria-describedby');});
}
function focusInvalidField(message) {
  const match = message.match(/Matriz ([AB]), linha (\d+), coluna (\d+)/);
  const field = match && $(`cell-${match[1].toLowerCase()}-${Number(match[2])-1}-${Number(match[3])-1}`);
  if (field) {field.classList.add('invalid-cell');field.setAttribute('aria-invalid','true');field.setAttribute('aria-describedby','error');field.focus();}
  else $('error').focus();
}
function renderGuide() {
  const terms=state.response.passos[state.selected].termos;
  const guided=guideIndex!==null, complete=!guided || guideIndex>=terms.length;
  $('guide').hidden=guided;$('guide-next').hidden=!guided||complete;$('guide-all').hidden=!guided;
  $('guide-next').textContent=guideIndex===terms.length-1?'Ver soma final':'Próximo produto';
  [...$('terms').children].forEach((el,i)=>{const k=Math.ceil(i/2);el.hidden=guided && k>guideIndex;el.classList.toggle('current-term',guided&&k===guideIndex);});
  $('sum').hidden=!complete;
  $('guide-status').textContent=!guided?'':complete?'Somamos os produtos para obter este elemento de C.':`Produto ${guideIndex+1} de ${terms.length}: ${terms[guideIndex].a} × ${terms[guideIndex].b} = ${terms[guideIndex].produto}.`;
  if(guided&&!complete) for(const matrix of ['a','b']) {
    $('read-'+matrix).querySelectorAll('.read-cell').forEach(cell=>cell.classList.toggle('pair-active',cell.classList.contains('highlight') && Number(cell.dataset[matrix==='a'?'col':'row'])===guideIndex));
  } else document.querySelectorAll('.pair-active').forEach(el=>el.classList.remove('pair-active'));
}
$('guide').addEventListener('click',()=>{guideIndex=0;renderGuide();$('guide-next').focus();});
$('guide-next').addEventListener('click',()=>{guideIndex++;renderGuide();if($('guide-next').hidden)$('guide-all').focus();});
$('guide-all').addEventListener('click',()=>{guideIndex=null;renderGuide();$('guide').focus();});
$('present').addEventListener('click',()=>{
  const on=document.body.classList.toggle('presenting');
  $('present').setAttribute('aria-pressed',String(on));$('present').textContent=on?'Sair da apresentação':'Modo apresentação';
  $('result-stage').scrollIntoView({block:'start'});
});
document.addEventListener('keydown',event=>{if(event.key==='Escape'&&document.body.classList.contains('presenting'))$('present').click();});
$('copy-result').addEventListener('click',async()=>{
  if(!state.response)return;
  const d=state.response, cols=d.dimensoes.c[1];
  const rows=Array.from({length:d.dimensoes.c[0]},(_,i)=>d.passos.slice(i*cols,(i+1)*cols).map(s=>s.valor).join('\t')).join('\n');
  try {await navigator.clipboard.writeText(rows);$('export-status').textContent='Matriz C copiada.';}
  catch {$('export-status').textContent='O navegador não permitiu copiar. Use Baixar cálculos.';}
});
$('download').addEventListener('click',()=>{
  if(!state.response)return;
  const text=['MatrizLab - Multiplicação de matrizes','Matriz A:',...state.a.map(r=>r.join('  ')),'','Matriz B:',...state.b.map(r=>r.join('  ')),'','Cálculos de C:',...state.response.passos.map(s=>`C[${s.linha}, ${s.coluna}]: ${s.expressao}`),'','Valores exibidos com até 12 algarismos significativos.'].join('\n');
  const url=URL.createObjectURL(new Blob([text],{type:'text/plain;charset=utf-8'}));
  const link=document.createElement('a');link.href=url;link.download='MatrizLab-calculos.txt';link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
  $('export-status').textContent='Arquivo de cálculos preparado.';
});
