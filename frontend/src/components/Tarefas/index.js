import React from "react";
import PropTypes from "prop-types";
import { FaEdit, FaWindowClose, FaAdjust } from "react-icons/fa";
import './Tarefas.css';

export default function Tarefas({ handleEdit, handleDelete, handleStatus }){
  return (
    <ul className="tarefas" >
      { tarefas.map((tarefa, index) => (
        <li key={ tarefa } >
          { tarefa }
        <span>
            <FaEdit
              className="edit"
              onClick={
                (evento) => handleEdit(evento, index)
              }
            />
            <FaAdjust
              className="alocacao"
              onClick={
                (evento) => handleStatus(evento)
              }
            />
            <FaWindowClose
              className="delete"
              onClick={
                (evento) => handleDelete(evento, index)
              }
            />
        </span>
        </li>
      ))}
    </ul>
  );
}

Tarefas.propTypes = {
  tarefas: PropTypes.array.isRequired,
  handleEdit: PropTypes.func.isRequired,
  handleDelete: PropTypes.func.isRequired,
}
