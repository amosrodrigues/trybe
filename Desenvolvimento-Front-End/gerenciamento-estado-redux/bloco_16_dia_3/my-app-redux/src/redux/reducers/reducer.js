import { VALID_EMAIL, VALID_CLIENTE } from '../actions';

const INITIAL_STATE = {
  login: {
    email: '',
    senha: '',
  },
  clientes: [],
} 

const reducer = (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case VALID_EMAIL:
      return { ...state, login: action.payload };
    case VALID_CLIENTE:
      return {...state, clientes: [...state.clientes, action.payload]};
    default:
      return state;
  }
}

export default reducer;