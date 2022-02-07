import React, { Component } from 'react';
import Result from './result';

class Results extends React.Component {
    constructor(props) {
        super(props);
    }


    render() {
        if (this.props.results.length>0){
            return (
                <div className="resultsBloc">
                    <div>{this.props.results.length} Résultats trouvés</div>
                    {this.props.results.map((message) => <Result key={message} message={message} />)}
                </div>
            );
        } else {
            return (<div></div>);
        }
        
    }
}

export default Results