const BASE = "http://localhost:8000";

function parseResponseData(text) {
  try {
    return JSON.parse(text || '{}');
  } catch {
    return text;
  }
}

async function request(method, url, body) {
  const opts = { method, headers: {} };
  if (body) {
    opts.headers['Content-Type'] = 'application/json';
    opts.body = JSON.stringify(body);
  }

  console.log(`[API] ${method} ${url}`, body || '');

  const res = await fetch(url, opts);
  const text = await res.text();
  const data = parseResponseData(text);

  console.log(`[API Response] Status: ${res.status}, Body:`, text);

  if (!res.ok) {
    const message = data?.message || data?.error || `Falha na requisição (${res.status})`;
    const erro = new Error(message);
    erro.status = res.status;
    erro.data = data;
    throw erro;
  }

  return data;
}

export async function listLocacoes() {
  return request('GET', `${BASE}/api/locacoes`);
}

export async function createLocacao(payload) {
  return request('POST', `${BASE}/api/locacoes`, payload);
}

export async function listVeiculos() {
  return request('GET', `${BASE}/api/veiculos`);
}

export async function listVeiculosDisponiveis() {
  return request('GET', `${BASE}/api/veiculos/disponiveis`);
}

export async function getRelatorio() {
  return request('GET', `${BASE}/api/relatorio`);
}

export async function callLink(link) {
  if (!link || !link.href) throw new Error('Link inválido');
  return request(link.method || 'GET', link.href);
}

export async function updateVeiculoStatus(veiculoId, status) {
  const statusEncoded = encodeURIComponent(status);
  const url = `${BASE}/api/veiculos/${veiculoId}/status?status=${statusEncoded}`;
  return request('PATCH', url);
}

export default { listLocacoes, createLocacao, listVeiculos, listVeiculosDisponiveis, getRelatorio, callLink, updateVeiculoStatus };
