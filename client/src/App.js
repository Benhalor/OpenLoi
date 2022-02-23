import logo from './logo.png';
import './App.css';
import React from 'react';
import NameForm from './components/name_form';
import Results from './components/results';


class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { queryResult: { "data": [] } };
  }

  pullResults = (data) => {
    this.setState({ queryResult: data })
  }

  render() {
    return (
      <div className="App">
        <div className="App-warning">
          /!\ Ce projet est encore en construction. De nombreuses fonctionnalités ne sont pas implémentées. Si vous repérez un bug, merci  
          <a href="https://github.com/Benhalor/OpenLoi/issues" target="_blank" rel="noopener noreferrer" > d'ouvrir une issue </a>
        </div>
        <div className="App-header">
          <div className="row align-items-center">

            <a className="col" href="/">
              <img alt="Surveiller et trouver des textes de loi avec Open loi" src={logo} />
            </a>


            <div className="row justify-content-end githubLink">
              <a href="https://github.com/Benhalor/OpenLoi" target="_blank" rel="noopener noreferrer">Github ↗</a>
            </div>


          </div>
        </div>

        <div className="App-body">

          <div className="searchBloc">
            <div className="searchBloc-title h1">
              Surveillez le contenu législatif facilement
            </div>
            <div className="searchLine">

              <NameForm pullResults={this.pullResults} />
            </div>
          </div>

          <Results queryResult={this.state.queryResult} />
        </div>



        <footer className="App-footer">

        </footer>

      </div>


    );
  }
}

export default App;
