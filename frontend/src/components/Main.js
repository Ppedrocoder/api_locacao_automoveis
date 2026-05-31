import React, { useEffect, useState } from "react";
import './Main.css';
import LocacaoForm from './LocacaoForm';
import Locacoes from './Locacoes';
import { listLocacoes } from '../api';

const RELATORIO_WS_URL = 'ws://localhost:8000/ws/relatorio';

const relatorioInicial = {
  total: 0,
  reservados: 0,
  em_uso: 0,
  devolvidos: 0,
  atrasados: 0,
  cancelados: 0,
};

export default function Main() {
  const [locacoes, setLocacoes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [relatorio, setRelatorio] = useState(relatorioInicial);
  const [atualizadoEm, setAtualizadoEm] = useState(null);

  const fetchLocacoes = async () => {
    setLoading(true);
    try {
      const data = await listLocacoes();
      setLocacoes(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error('Erro ao listar locações', err);
      setLocacoes([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLocacoes();

    let ativo = true;
    let reconectarTimer = null;
    let socket = null;

    const conectarWebSocket = () => {
      socket = new WebSocket(RELATORIO_WS_URL);
      console.log('WebSocket do relatório: conectando...');

      socket.onopen = () => {
        if (!ativo) {
          return;
        }

        console.log('WebSocket do relatório: conectado');
      };

      socket.onmessage = (event) => {
        try {
          const payload = JSON.parse(event.data);

          if (payload?.relatorio) {
            setRelatorio(payload.relatorio);
            setAtualizadoEm(payload.atualizadoEm || new Date().toISOString());
          }
        } catch (err) {
          console.error('Erro ao ler mensagem do websocket', err);
        }
      };

      socket.onerror = (err) => {
        if (!ativo) return;
        console.error('WebSocket do relatório: erro', err);
      };

      socket.onclose = () => {
        if (!ativo) {
          return;
        }

        console.log('WebSocket do relatório: desconectado, tentando reconectar em 3s');
        reconectarTimer = window.setTimeout(conectarWebSocket, 3000);
      };
    };

    conectarWebSocket();

    return () => {
      ativo = false;

      if (reconectarTimer) {
        window.clearTimeout(reconectarTimer);
      }

      if (socket) {
        socket.close();
      }
    };
  }, []);

  const formatarData = (valor) => {
    if (!valor) {
      return 'Aguardando atualização';
    }

    return new Date(valor).toLocaleString('pt-BR');
  };

  const metricas = [
    { label: 'Total', value: relatorio.total },
    { label: 'Reservados', value: relatorio.reservados },
    { label: 'Em uso', value: relatorio.em_uso },
    { label: 'Devolvidos', value: relatorio.devolvidos },
    { label: 'Atrasados', value: relatorio.atrasados },
    { label: 'Cancelados', value: relatorio.cancelados },
  ];

  return (
    <div className="main">
      <section className="relatorio-panel">
        <div className="relatorio-panel__header">
          <h1>Locações em tempo real</h1>
        </div>

        <div className="relatorio-panel__meta">
          <span>Última atualização: {formatarData(atualizadoEm)}</span>
        </div>

        <div className="relatorio-grid">
          {metricas.map((item) => (
            <article className="relatorio-card" key={item.label}>
              <span className="relatorio-card__label">{item.label}</span>
              <strong className="relatorio-card__value">{item.value}</strong>
            </article>
          ))}
        </div>
      </section>

      <LocacaoForm onCreated={fetchLocacoes} />

      <Locacoes
        locacoes={locacoes}
        loading={loading}
        onRefresh={fetchLocacoes}
      />
    </div>
  );
}
