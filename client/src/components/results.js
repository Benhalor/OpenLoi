import React, { Component } from 'react';
import Result from './result';

class Results extends React.Component {
    constructor(props) {
        super(props);
    }


    render() {
        if (this.props.queryResult.count > 0) {
            return (
                <div className="resultsBloc">
                    <div>{this.props.queryResult.count} Résultat(s) trouvé(s)</div>
                    {Object.entries(this.props.queryResult.data).map(([dossierUid, data]) => <Result key={dossierUid} dossierUid={dossierUid} data = {data} query={this.props.queryResult.query} />)}
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