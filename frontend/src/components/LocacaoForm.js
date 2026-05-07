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
    <form className="locacao-form" onSubmit={handleSubmit}>
      <div className="locacao-form__field">
        <label className="locacao-form__label">Cliente</label>
        <input
          className="locacao-form__control"
          value={cliente}
          onChange={e => setCliente(e.target.value)}
          required
        />
      </div>
      <div className="locacao-form__field">
        <div className="locacao-form__row">
          <label className="locacao-form__label">Veículo</label>
          <button
            type="button"
            className="locacao-form__reload"
            onClick={fetchVeiculos}
            disabled={loadingVeiculos}
          >
            {loadingVeiculos ? '...' : '⟲'}
          </button>
        </div>
        {loadingVeiculos ? (
          <div className="locacao-form__hint">Carregando veículos...</div>
        ) : (
          <select
            className="locacao-form__control"
            value={veiculoId}
            onChange={e => setVeiculoId(e.target.value)}
            required
          >
            <option value="" disabled>
              Selecione um veículo
            </option>
            {veiculos.map((v) => (
              <option key={v.id} value={v.id}>
                {v.marca} {v.modelo}
              </option>
            ))}
          </select>
        )}
      </div>
      <div className="locacao-form__field">
        <label className="locacao-form__label">Dia Inicial</label>
        <input
          className="locacao-form__control"
          value={diaInicial}
          onChange={e => setDiaInicial(e.target.value)}
          required
          type="date"
        />
      </div>
      <div className="locacao-form__field">
        <label className="locacao-form__label">Dia Final</label>
        <input
          className="locacao-form__control"
          value={diaFinal}
          onChange={e => setDiaFinal(e.target.value)}
          required
          type="date"
        />
      </div>
      <button className="locacao-form__submit" type="submit" disabled={saving}>
        {saving ? 'Salvando...' : 'Criar Locação'}
      </button>
    </form>
  );
}

LocacaoForm.propTypes = {
  onCreated: PropTypes.func,
};
