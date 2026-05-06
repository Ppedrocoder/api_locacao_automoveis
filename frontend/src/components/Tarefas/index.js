import React from "react";
import PropTypes from "prop-types";
import { FaEdit, FaWindowClose } from "react-icons/fa";
import './Tarefas.css';

export default function Tarefas({ tarefas, handleEdit, handleDelete }){
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
