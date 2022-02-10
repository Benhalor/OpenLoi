import React, { Component } from 'react';

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
    this.updateSearchResults(this.state.userQuery)
    event.preventDefault();
  }

 
  updateSearchResults(query) {
    fetch('http://localhost:5000/api/search/' + query)
      .then(response => response.json())
      .then(
        (result) => {
          this.props.pullResults(result)

        }

      )
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit} className="row align-items-center">
        <label className="col-md-auto label-for-search">
          Rechercher :
        </label>
        <div className="col autocomplete">
          <input type="search" className="autocomplete-input" value={this.state.userQuery} autoComplete="off" onChange={this.handleChange} placeholder="Ex: climat" />
        </div>
      </form>
    );
  }
}

export default NameForm