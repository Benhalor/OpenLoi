import React, { Component } from 'react';
import ResultTemplate from './result_template'


class Results extends React.Component {
    constructor(props) {
        super(props);
    }


    render() {
        if (this.props.queryResult.count > 0) {
            return (
                <div className="resultsBloc">
                    <div>{this.props.queryResult.count} Résultat(s) trouvé(s)</div>
                    {this.props.queryResult.listOfResults.map((data) => <ResultTemplate key={data.uid+this.props.queryResult.query} data={data} query={this.props.queryResult.query} />)}
                </div>
            );
        } else {
            return (
                <div className="resultsBloc">
                    <div>{this.props.queryResult.count} Résultat trouvé</div>
                </div>);
        }

    }
}

export default Results
// {this.props.queryResult.data.map((result) => <Result key={"0"} message={result} />)}