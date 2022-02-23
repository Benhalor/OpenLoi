import React, { Component } from 'react';
import DossierLegislatif from './dossier_legislatif';
import Question from './question';
import Debat from './debat';


class ResultTemplate extends React.Component {
    constructor(props) {
        super(props);
    }


    render() {
        if (this.props.data.type === "questionEcrite" || this.props.data.type === "questionOraleSansDebat") {
            return (
                <div className="">
                    <Question key={this.props.data.uid + this.props.query} questionUid={this.props.data.uid} query={this.props.query} questionType={this.props.data.type} />
                </div>
            );
        } else if (this.props.data.type === "dossierLegislatif") {
            return (
                <div className="">
                    <DossierLegislatif key={this.props.data.uid + this.props.query} dossierUid={this.props.data.uid} query={this.props.query} />
                </div>
            );
        } else if (this.props.data.type === "questionAuGouvernement") {
            return (
                <div className="">
                    <Debat key={this.props.data.uid + this.props.query} questionUid={this.props.data.uid} query={this.props.query} questionType={this.props.data.type} />
                </div>
            );
        } else {
            return (<div></div>);
        }

    }
}

export default ResultTemplate
