const BASE = "http://localhost:8000";
const RELATORIOS_BASE = "http://localhost:9000";

async function request(method, url, body) {
  const opts = { method, headers: {} };
  if (body) {
    opts.headers['Content-Type'] = 'application/json';
    opts.body = JSON.stringify(body);
  }
  console.log(`[API] ${method} ${url}`, body || '');
  const res = await fetch(url, opts);
  const text = await res.text();
  console.log(`[API Response] Status: ${res.status}, Body:`, text);
  try {
    return JSON.parse(text || '{}');
  } catch {
    return text;
  }
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
  return request('GET', `${RELATORIOS_BASE}/api/relatorio`);
}

export async function callLink(link) {
  if (!link || !link.href) throw new Error('Link inválido');
  return request(link.method || 'GET', link.href);
}

export async function updateVeiculoStatus(veiculoId, status) {
  const url = `${BASE}/api/veiculos/${veiculoId}/status`;
  console.log(`[API] PATCH ${url}?status=${status}`);
  const res = await fetch(`${url}?status=${status}`, { method: 'PATCH' });
  const text = await res.text();
  console.log(`[API Response] Status: ${res.status}, Body:`, text);
  try {
    return JSON.parse(text || '{}');
  } catch {
    return text;
  }
}

export default { listLocacoes, createLocacao, listVeiculos, listVeiculosDisponiveis, getRelatorio, callLink, updateVeiculoStatus };
