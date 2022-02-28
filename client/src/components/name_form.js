import React, { Component } from 'react';
import * as config from './config';

class NameForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = { userQuery: '', numberOfResults: null };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({ userQuery: event.target.value });
  }

  handleSubmit(event) {
    if (this.state.userQuery == "") {
      this.getLastNews()
    } else {
      this.updateSearchResults(this.state.userQuery)
    }

    event.preventDefault();
  }


  updateSearchResults(query) {
    fetch(config.apiUrl + 'search/' + query)
      .then(response => response.json())
      .then(
        (result) => {
          console.log(result)
          this.props.pullResults(result)
        }

      )
  }

  getLastNews() {
    fetch(config.apiUrl + 'lastNews/')
      .then(response => response.json())
      .then(
        (result) => {
          console.log(result)
          this.props.pullResults(result)

        }

      )
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit} className="row align-items-center">
        <div className="col autocomplete">
          <input type="search" className="autocomplete-input" value={this.state.userQuery} autoComplete="off" onChange={this.handleChange} placeholder="Rechercher" />
        </div>
      </form>
    );
  }
}

export default NameForm