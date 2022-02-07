import React, { Component } from 'react';
import "./result.css";

class Result extends React.Component {
    constructor(props) {
        super(props);
    }


    render() {
        return (
            
            <div className="resultBloc">
            {this.props.message} <br />
            </div>
      
        );
    }
}

export default Result