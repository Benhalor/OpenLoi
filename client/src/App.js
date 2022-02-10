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
    console.log(data)
    this.setState({ queryResult: data })
  }

  render() {
    return (
      <div className="App">
        <div className="App-header">
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
