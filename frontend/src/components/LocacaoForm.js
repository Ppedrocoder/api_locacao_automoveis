import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import { createLocacao, listVeiculosDisponiveis, updateVeiculoStatus } from '../api';

export default function LocacaoForm({ onCreated }) {
  const [cliente, setCliente] = useState('');
  const [veiculoId, setVeiculoId] = useState('');
  const [diaInicial, setDiaInicial] = useState('');
  const [diaFinal, setDiaFinal] = useState('');
  const [saving, setSaving] = useState(false);
  const [veiculos, setVeiculos] = useState([]);
  const [loadingVeiculos, setLoadingVeiculos] = useState(false);

  const fetchVeiculos = async () => {
    setLoadingVeiculos(true);
    try {
      const data = await listVeiculosDisponiveis();
      console.log('Veículos disponíveis carregados:', data);
      const veiculos = Array.isArray(data) ? data : [];
      setVeiculos(veiculos);
      if (veiculos.length > 0) {
        setVeiculoId(veiculos[0].id);
      } else {
        setVeiculoId('');
      }
    } catch (err) {
      console.error('Erro ao buscar veículos disponíveis', err);
    } finally {
      setLoadingVeiculos(false);
    }
  };

  useEffect(() => {
    fetchVeiculos();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      await createLocacao({
        cliente,
        veiculo_id: Number(veiculoId),
        dia_inicial: diaInicial,
        dia_final: diaFinal,
      });
      
      // Atualizar status do veículo para "Alugado"
      await updateVeiculoStatus(Number(veiculoId), 'Alugado');
      
      setCliente('');
      setDiaInicial('');
      setDiaFinal('');
      await fetchVeiculos();
      if (onCreated) onCreated();
    } catch (err) {
      console.error('Erro ao criar locação', err);
      alert('Erro ao criar locação');
    } finally {
      setSaving(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{marginBottom:16}}>
      <div>
        <label>Cliente: </label>
        <input value={cliente} onChange={e=>setCliente(e.target.value)} required />
      </div>
      <div>
        <label>Veículo: </label>
        <button type="button" onClick={fetchVeiculos} disabled={loadingVeiculos} style={{marginLeft: 8, padding: '4px 8px', fontSize: '12px'}}>
          {loadingVeiculos ? '...' : '⟲'}
        </button>
        {loadingVeiculos ? (
          <div>Carregando veículos...</div>
        ) : (
          <select value={veiculoId} onChange={e=>setVeiculoId(e.target.value)} required>
            <option value="" disabled>Selecione um veículo</option>
            {veiculos.map((v) => (
              <option key={v.id} value={v.id}>{v.marca} {v.modelo}</option>
            ))}
          </select>
        )}
      </div>
      <div>
        <label>Dia Inicial: </label>
        <input value={diaInicial} onChange={e=>setDiaInicial(e.target.value)} required type="date" />
      </div>
      <div>
        <label>Dia Final: </label>
        <input value={diaFinal} onChange={e=>setDiaFinal(e.target.value)} required type="date" />
      </div>
      <button type="submit" disabled={saving}>{saving ? 'Salvando...' : 'Criar Locação'}</button>
    </form>
  );
}

LocacaoForm.propTypes = {
  onCreated: PropTypes.func,
};
