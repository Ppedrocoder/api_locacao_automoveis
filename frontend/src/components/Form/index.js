import React from "react";
import PropTypes from 'prop-types';
import { FaPlus, Fa } from "react-icons/fa";

import './Form.css';

export default function Form({ handleSubmit, handleChange, carros }) {

  const lista = [{ ...carros }];
  return (
    <form
      onSubmit={ handleSubmit }
      action='#'
      className="form"
    >
      <select>
        { lista.map((carro) => (
          <option key={ carro.id } >{ carro.nome }</option>
        )) }
      </select>
      <input
        type="text"
        onChange={ handleChange }
        value='cliente'
      />
      <input
        type="date"
        onChange={ handleChange }
        value='dia-inicio'
      />
      <input
        type="date"
        onChange={ handleChange }
        value='dia-final'
      />
      <button type="submit" >
        <FaPlus />
      </button>
    </form>
  );
}

Form.propTypes = {
  handleSubmit: PropTypes.func.isRequired,
  handleChange: PropTypes.func.isRequired,
  carros: PropTypes.array.isRequired,
}
