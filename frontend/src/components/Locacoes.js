import React from 'react';
import PropTypes from 'prop-types';
import LocacaoItem from './LocacaoItem';

export default function Locacoes({ locacoes = [], loading, onRefresh }) {
  if (loading) return <div className="locacoes__state">Carregando locações...</div>;
  if (!locacoes || locacoes.length === 0) return <div className="locacoes__state">Sem locações.</div>;

  return (
    <div className="locacoes">
      {locacoes.map(loc => (
        <LocacaoItem key={loc.id} locacao={loc} onRefresh={onRefresh} />
      ))}
    </div>
  );
}

Locacoes.propTypes = {
  locacoes: PropTypes.array,
  loading: PropTypes.bool,
  onRefresh: PropTypes.func,
};
