import React, { Component } from "react";
import './Main.css';
import Form from "./Form";

import Tarefas from "./Tarefas";

export default class Main extends Component {

  state = {
    novoCarro: '',
    carros: [],
    index: -1,
  };

  componentDidMount() {
    const carros = JSON.parse(localStorage.getItem('carros'));

    if (!carros){
      return;
    }
    this.setState({ carros });
  }

  componentDidUpdate(prevProps, prevState) {
    const { carros } = this.state;

    if (carros === prevState.carros){
      return;
    }
    localStorage.setItem('carros', JSON.stringify(carros));
  }

  handleSubmit = (evento) => {
    evento.preventDefault();
    //console.log("Oi");
    const { carros, index } = this.state;
    let { novoCarro } = this.state;
    novoCarro = novaTarefa.trim();

    if (carros.indexOf(novoCarro) !== -1){
      return;
    }
    const novosCarros = [...carros];
    if (index === -1) {
      this.setState({
        carros: [...novosCarros, novoCarro],
        novoCarro: '',
      });
    } else {
      novosCarros[index] = novoCarro;

      this.setState({
        carros: [...novosCarros],
        index: -1,
      });
    }
  }

  handleDelete = (evento, index) => {
    const { tarefas } = this.state;
    const novasTarefas = [...tarefas];

    novasTarefas.splice(index, 1);

    this.setState({
      tarefas: [...novasTarefas],
    });

    return;
  }

  handleEdit = (evento, index) => {
    const { tarefas } = this.state;
    this.setState({
      index,
      novaTarefa: tarefas[index],
    });

  }

  handleChange = (evento) => {
    this.setState({
      novaTarefa: evento.target.value,
    });
  }

  render() {
    const { novaTarefa, tarefas } = this.state;
    return (
      <div className="main">
        <h1>Lista de Tarefas</h1>

        <Form
        handleSubmit={ this.handleSubmit }
        handleChange={ this.handleChange }
        novaTarefa={ novaTarefa }
        />

        <Tarefas
          tarefas={ tarefas }
          handleEdit={ this.handleEdit }
          handleDelete={ this.handleDelete }
        />
      </div>
    );
  }
}
