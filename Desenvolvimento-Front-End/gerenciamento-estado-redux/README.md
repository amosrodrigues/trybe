# Checklist do react-redux

*Antes de começar*
- [ ] pensar como será o *formato* do seu estado global
- [ ] pensar quais actions serão necessárias na sua aplicação

*Instalação*
- [ ] npx create-react-app my-app-redux;
- [ ] npm install --save redux react-redux;
- [ ] npm install.
- [ ] npm install --save redux-devtools-extension
```
import { composeWithDevTools } from 'redux-devtools-extension';
const store = createStore(rootReducer, composeWithDevTools());
```
*Dependências (opcional)*
- [ ] npm i -D prop-types
- [ ] npm i -D eslint
- [ ] npm i -D eslint-plugin-sonarjs
- [ ] npm i -D stylelint
- [ ] npm i -D stylelint-config-standard

*Criar dentro do diretório src:*
- [ ] diretório actions;
- [ ] diretório reducers;
- [ ] diretório store.

*Criar dentro do diretório actions:*
- [ ] arquivo index.js.

*Criar dentro do diretório reducers:*
- [ ] arquivo index.js.

*Criar dentro do diretório store:*
- [ ] arquivo index.js.

*No arquivo App.js:*
- [ ] definir o Provider, `<Provider store={ store }>`, para fornecer os estados à todos os componentes encapsulados em `<App />`.

**Se a sua aplicação não terá outras páginas, não é necessário configurar as rotas. Caso contrário:**
- [ ] npm install react-router-dom

*Em src/index.js:*
- [ ] definir o BrowserRouter, <BrowserRouter>
  
*No arquivo App.js:*
- [ ] definir o Switch, <Switch>
- [ ] definir a Route, <Route>

**O BrowserRouter, o Switch e a Route são três componentes essenciais para trabalhar rotas em React.**
*Caso necessário:
- [ ] criar o diretório components
- [ ] criar o diretório pages

*No arquivo store/index.js:*
- [ ] importar o rootReducer e criar a store
- [ ] configurar o [Redux DevTools](https://github.com/reduxjs/redux-devtools)

```
  import { createStore, compose } from 'redux';
  import rootReducer from '../reducers';

  const extension = window.devToolsExtension() || ((f) => f);

  const store = createStore(rootReducer, compose(extension));

  export default store;
```

*Na pasta reducers:*
- [ ] criar os reducers necessários
  
```
  const INITIAL_STATE = {
    state: '',
    };

    function myReducer(state = INITIAL_STATE, action) {
      switch (action.type) {
        case 'NEW_ACTION':
          return { state: action.state };
        default:
          return state;
      }
    }
  
  export default myReducer;
```
  
- [ ] configurar os exports do arquivo index.js
  
```
   import { combineReducers } from 'redux';
   import myReducer from './myReducer';

   const rootReducer = combineReducers({ myReducer });

   export default rootReducer;
```

*Na pasta actions:*
- [ ] criar os actionTypes, por exemplo:
  
`export const ADD_TO_CART = 'ADD_TO_CART';`
  
- [ ] criar os actions creators necessários:
  
`export const newAction = (state) => ({ type: 'NEW_ACTION', state });`

*Nos componentes:*
- [ ] criar a função mapStateToProps
  
```
  const mapStateToProps = state => ({
    myFirstState: state.myReducer.state
  });
```

  
- [ ] criar a função mapDispatchToProps

```
  const mapDispatchToProps = (dispatch) => ({
    myFirstDispatch: (state) => dispatch(newAction(state))
  });
```
  
- [ ] fazer o connect 
  
  `export default connect(mapStateToProps, mapDispatchToProps)(Component)`

**Usando o Redux no React - Actions Assíncronas**
- [ ] npm install redux-thunk

```
// arquivo onde a redux store é criada
import { createStore, applyMiddleware } from 'redux';
import thunk from 'redux-thunk';
import reducer from '/path/to/your/root/reducer';

const store = createStore(reducer, applyMiddleware(thunk));
```

**Exemplo:**
```
export const REQUEST_MOVIES = 'REQUEST_MOVIES';
export const RECEIVE_MOVIES = 'RECEIVE_MOVIES';

// action creator que retorna um objeto, que você tem feito até então
const requestMovies = () => ({
  type: REQUEST_MOVIES});

// outro action creator que retorna um objeto, que você tem feito até então
const receiveMovies = (movies) => ({
  type: RECEIVE_MOVIES,
  movies});

// action creator que retorna uma função, possível por conta do pacote redux-thunk
export function fetchMovies() {
  return (dispatch) => { // thunk declarado
    dispatch(requestMovies());
    return fetch('alguma-api-qualquer.com')
      .then((response) => response.json())
      .then((movies) => dispatch(receiveMovies(movies)));
  };
}

// componente onde você usaria a action creator fetchMovies assíncrona como uma outra qualquer

class MyConectedAppToRedux extends Component {

  componentDidMount() {
    const { dispatch, fetchMovies } = this.props;
    dispatch(fetchMovies()); // enviando a action fetchMovies
  }

}
```

**Funcionamento do Thunk através da createThunkMiddleware**
```
function createThunkMiddleware(extraArgument) {
  return ({ dispatch, getState }) => (next) => (action) => {
    if (typeof action === 'function') {
      return action(dispatch, getState, extraArgument);
    }

    return next(action);
  };
}

const thunk = createThunkMiddleware();
thunk.withExtraArgument = createThunkMiddleware;

export default thunk;
```
  
**Sequência das ocorrências**
  
1. Pessoa usuária executa a ação na interface, chamando a action
2. A action dispara seu dispatch
3. O redux-thunk captura a action, agindo como middleware
4. O redux-thunk comunica-se com a API, aguardando sua resposta
5. O redux-thunk envia a resposta para o reducer correto
6. O reducer pega o estado atual da store e o modifica, de acordo com a action
7. A store é modificada
8. A interface é atualizada
  
**Exemplo Fetch**
  
```
const APIURL = 'https://anapioficeandfire.com/api/characters?name='

const charAPI = (char) => (
  fetch(`${APIURL}${char.split().join('+')}`)
    .then((response) => (
      response
        .json()
        .then((json) => (response.ok ? Promise.resolve(json) : Promise.reject(json)))
    ))
);

export default charAPI;
```
```
export const fetchAPI = () => async (dispatch) => {
   dispatch(requestAPI());
   try {
     const response = await fetch()
     const data = await response.json()
     dispatch(getPicture(data));
   } catch (error) {
     console.error(error);
   }
 };
  
// export function thunkCharacter(name) {
//   return (dispatch) => {
//     dispatch(searchBegin(name));
//     return charAPI(name)
//       .then(
//         (character) => dispatch(searchSuccess(character)),
//         (error) => dispatch(searchFailure(error.message)),
//       );
//   };
// };
```
  
**Relembrando RTL com Rdux**

- [ ] renderWithRouter
```
import React from 'react';
import { render } from "@testing-library/react";
import { Router } from "express";
import { createMemoryHistory } from "history";

const renderWithRouter = (component, initialEntries = ['/cadastro']) => {
  const history = createMemoryHistory({ initialEntries });
  return ({
    ...render(<Router history={ history }>{ component }</Router>), history,
  })
};

export default renderWithRouter;
```
- [ ] renderWithRedux
```
import { render } from "react-dom";
import { Provider } from "react-redux";
import { applyMiddleware, createStore } from "redux";
import rootReducer from "../../redux/reducers";
import thunk from 'redux-thunk';

const renderWithRedux = ( 
  component,
  { initialState = {}, store = createStore(rootReducer, initialState, applyMiddleware(thunk))} = {}
  ) => ({
    ...render(<Provider store={ store }>{ component }</Provider>), store,
  });

export default renderWithRedux;
```
  
- [ ] União do Router com Redux em RTL
  
```
import React from 'react';
import { Router } from 'react-router-dom';
import { createMemoryHistory } from 'history';
import { render } from '@testing-library/react';

import { Provider } from 'react-redux';
import { applyMiddleware, createStore } from 'redux';
import rootReducers from '../../reducers';
import thunk from 'redux-thunk';

const renderWithRouterAndRedux = (
  component, // componente a ser renderizado
  {
    // estado inicial para o nosso reducer
    initialState = {},

    // caso você passe uma store por parâmetro ela será utilizada
    // caso contrário vai chamar a função createStore e criar uma nova
    store = createStore(rootReducers, initialState, applyMiddleware(thunk)),

    // rota inicial da nossa aplicação
    initialEntries = ['/'],

    // caso você passe um history por parâmetro ele será utilizado
    // caso contrário vai chamar a função createMemotryHistory e criar um novo
    history = createMemoryHistory({ initialEntries }),
  } = {},
) => ({ // arrow function que retorna um objeto

  // spread do retorno do render { getByTestId, getByRole, etc }
  ...render(
    <Router history={ history }>
      <Provider store={ store }>
        {component}
      </Provider>
    </Router>,
  ),

  // history usado acima
  history,

  // store usada acima
  store,
});

// resultado dessa função:
// renderiza o componente no teste
// retorna um objeto contendo { store, history, getByTestId, getByRole, etc }

export default renderWithRouterAndRedux;
```
- [ ] Com Utilização do Thunk 
```
const createMockStore = (initialState) => (
  createStore(combineReducers({ reducer }), initialState, applyMiddleware(thunk))
);

const renderWithRedux = (
  component, { initialState, store = createMockStore(initialState) } = {},
) => ({
  ...render(<Provider store={ store }>{component}</Provider>),
  store});

export default renderWithRedux;
```
