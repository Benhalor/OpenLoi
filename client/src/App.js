import logo from './logo.png';
import './App.css';
import React from 'react';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <div className="row align-items-center">

          <a className="col" href="/">
            <img alt="Surveiller et trouver des textes de loi avec Open loi" src={logo} />
          </a>


          <div className="col">
            <div className="row justify-content-end">
              <div className="col-auto">
                <a href="/apropos">À propos</a>
              </div>
              <div className="col-auto border-start">
                <a href="/apropos">Bonjour</a>
              </div>
            </div>
          </div>

        </div>
      </header>

      <body className="App-body">

        <div className="searchBloc">
          <div className="searchBloc-title h1">
            Surveillez le contenu législatif facilement
          </div>
          <div className="searchLine">
            <form className="row align-items-center">
              <label className="col-md-auto label-for-search">
                Rechercher :
              </label>
              <div className="col autocomplete">
                <input type="search" className="autocomplete-input" required="" placeholder="Ex: covid-19" />

              </div>
            </form>
          </div>
        </div>
      </body>



      <footer className="App-footer">

      </footer>

    </div>

  );
}

export default App;
