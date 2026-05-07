import React, { useEffect, useState } from "react";
import './Main.css';
import LocacaoForm from './LocacaoForm';
import Locacoes from './Locacoes';
import { listLocacoes } from '../api';

export default function Main() {
  const [locacoes, setLocacoes] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchLocacoes = async () => {
    setLoading(true);
    try {
      const data = await listLocacoes();
      setLocacoes(data || []);
    } catch (err) {
      console.error('Erro ao listar locações', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLocacoes();
  }, []);

  return (
    <div className="main">
      <h1>Locações</h1>

      <LocacaoForm onCreated={fetchLocacoes} />

      <Locacoes
        locacoes={locacoes}
        loading={loading}
        onRefresh={fetchLocacoes}
      />
    </div>
  );
}
