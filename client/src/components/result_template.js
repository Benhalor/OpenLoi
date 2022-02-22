import React, { Component } from 'react';
import DossierLegislatif from './dossier_legislatif';
import QuestionEcriteAN from './question_ecrite_an';


class ResultTemplate extends React.Component {
    constructor(props) {
        super(props);
    }


    render() {
        if (this.props.data.type === "questionEcrite") {
            return (
                <div className="">
                     <QuestionEcriteAN key={this.props.data.uid + this.props.query} questionUid={this.props.data.uid} query={this.props.query} />
                </div>
            );
        } else if (this.props.data.type === "dossierLegislatif") {
            return (
                <div className="">
                    <DossierLegislatif key={this.props.data.uid + this.props.query} dossierUid={this.props.data.uid} query={this.props.query} />
                </div>
            );
        }

    }
}

export default ResultTemplate
