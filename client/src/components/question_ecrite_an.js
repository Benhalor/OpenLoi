import React, { Component } from 'react';
import Highlighter from "react-highlight-words";
import * as config from './config';

import { convertDate, sanitizeWords, generateSearchWords } from './utils'

class QuestionEcriteAN extends React.Component {
    constructor(props) {
        super(props);
        this.state = { displayQuestion: false, displayReponse: false, questionEcrite: null };
        this.getQuestionEcrite(this.props.questionUid)
    }

    changedisplayQuestion() {
        this.setState({ displayQuestion: !this.state.displayQuestion })

    }
    changedisplayReponse() {
        this.setState({ displayReponse: !this.state.displayReponse })

    }


    getQuestionEcrite(uid) {
        fetch(config.apiUrl + 'questionEcrite/' + uid)
            .then(response => response.json())
            .then(
                (result) => {
                    this.setState({ questionEcrite: result })
                }

            )
    }




    render() {

        if (this.state.questionEcrite !== null) {
            return (
                <div className="resultBloc">


                    <div className="row result-bloc-row">
                        <div className="col text-column">
                            <div className="row">

                                📝 Question écrite d'un député au gouvernement
                            </div>
                            <div className="row entete">
                                <Highlighter
                                    searchWords={this.props.query == "" ? [] : generateSearchWords(this.props.query)}
                                    sanitize={sanitizeWords}
                                    textToHighlight={this.state.questionEcrite.resume} />


                            </div>
                        </div>
                    </div>

                    <div className="col">
                        <div className="titleSubResultBloc cursor" onClick={this.changedisplayQuestion.bind(this)}>
                            {this.state.displayQuestion ? "➖" : "➕"} Question de {JSON.parse(this.state.questionEcrite.question).texteQuestion.texte.split(' ').slice(0, 3).join(' ')}
                            <span className="dossierStatus"> {this.state.questionEcrite.dateQuestion !== null && "▪ Déposée le " + convertDate(this.state.questionEcrite.dateQuestion)}</span>
                        </div>
                        {this.state.displayQuestion &&
                            <div className="subResultBloc">
                                <div className="col text-column-sub">
                                    <Highlighter
                                        searchWords={this.props.query == "" ? [] : generateSearchWords(this.props.query)}
                                        sanitize={sanitizeWords}
                                        textToHighlight={JSON.parse(this.state.questionEcrite.question).texteQuestion.texte} />
                                </div>
                            </div>

                        }
                        <div className="titleSubResultBloc cursor" onClick={this.changedisplayReponse.bind(this)}>
                            {(this.state.displayReponse && this.state.questionEcrite.dateReponse !== null) && "➖"}
                            {(!this.state.displayReponse && this.state.questionEcrite.dateReponse !== null) && "➕"}
                            {(this.state.questionEcrite.dateReponse === null) && "⏱"}
                            Réponse du {this.state.questionEcrite.ministere}
                            <span className="dossierStatus">{this.state.questionEcrite.dateReponse !== null ?
                                "▪ Déposée le " + convertDate(this.state.questionEcrite.dateReponse)
                                : "En attente de réponse"
                            }
                            </span>
                        </div>
                        {(this.state.displayReponse && this.state.questionEcrite.reponse !== null) &&
                            <div className="subResultBloc">
                                <div className="col text-column-sub">

                                    <Highlighter
                                        searchWords={this.props.query == "" ? [] : generateSearchWords(this.props.query)}
                                        sanitize={sanitizeWords}
                                        textToHighlight={JSON.parse(this.state.questionEcrite.reponse).texteReponse.texte} />


                                </div>
                            </div>


                        }
                        {/*this.state.displayEtapes && this.state.etapesLegislatives.map((data) => <EtapeLegislative key={data.uid} data={data} query={this.props.query} />)*/}

                    </div>


                </div>);
        } else {
            return null
        }


    }
}

export default QuestionEcriteAN
