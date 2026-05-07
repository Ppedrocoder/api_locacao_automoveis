import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { callLink, updateVeiculoStatus } from '../api';

function findLink(links, rel) {
  if (!links) return null;
  return links.find(l => l.rel === rel) || null;
}

export default function LocacaoItem({ locacao, onRefresh }) {
  const [busy, setBusy] = useState(false);

  const doAction = async (rel) => {
    const link = findLink(locacao.links, rel);
    if (!link) return;
    
    // Pedir confirmação para deletar
    if (rel === 'deletar' && !window.confirm(`Deseja deletar a locação #${locacao.id}?`)) {
      return;
    }
    
    setBusy(true);
    try {
      // Para deletar, primeiro liberar o veículo, depois deletar
      if (rel === 'deletar') {
        await updateVeiculoStatus(locacao.veiculo_id, 'Disponível');
      }
      
      await callLink(link);
      
      // Atualizar status do veículo após a ação
      if ((rel === 'cancelar' || rel === 'finalizar') && rel !== 'deletar') {
        await updateVeiculoStatus(locacao.veiculo_id, 'Disponível');
      }
      
      if (onRefresh) onRefresh();
    } catch (err) {
      console.error('Erro na ação', err);
      alert('Erro na ação: ' + (err.message || err));
    } finally {
      setBusy(false);
    }
  };

  const iniciarLink = findLink(locacao.links, 'iniciar');
  const cancelarLink = findLink(locacao.links, 'cancelar');
  const finalizarLink = findLink(locacao.links, 'finalizar');
  const deletarLink = findLink(locacao.links, 'deletar');

  return (
    <div style={{border:'1px solid #ccc', padding:8, marginBottom:8}}>
      <div><strong>#{locacao.id}</strong> - {locacao.cliente} — Veículo: {locacao.veiculo_id}</div>
      <div>Período: {locacao.dia_inicial} → {locacao.dia_final}</div>
      <div>Status: {locacao.status}</div>

      <div style={{marginTop:8}}>
        <button onClick={()=>doAction('iniciar')} disabled={!iniciarLink || busy}>Iniciar</button>
        <button onClick={()=>doAction('cancelar')} disabled={!cancelarLink || busy} style={{marginLeft:8}}>Cancelar</button>
        <button onClick={()=>doAction('finalizar')} disabled={!finalizarLink || busy} style={{marginLeft:8}}>Finalizar</button>
        <button onClick={()=>doAction('deletar')} disabled={!deletarLink || busy} style={{marginLeft:8}}>Deletar</button>
      </div>
    </div>
  );
}

LocacaoItem.propTypes = {
  locacao: PropTypes.shape({
    id: PropTypes.number,
    cliente: PropTypes.string,
    veiculo_id: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
    dia_inicial: PropTypes.string,
    dia_final: PropTypes.string,
    status: PropTypes.string,
    links: PropTypes.arrayOf(PropTypes.object),
  }).isRequired,
  onRefresh: PropTypes.func,
};
