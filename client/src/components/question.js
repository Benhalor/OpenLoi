import React, { Component } from 'react';
import Highlighter from "react-highlight-words";
import * as config from './config';

import { convertDate, sanitizeWords, generateHighlightedHtml } from './utils'

class Question extends React.Component {
    constructor(props) {
        super(props);
        this.state = { displayQuestion: false, displayReponse: false, question: null };
        this.getQuestion(this.props.questionUid, this.props.questionType)
    }

    changedisplayQuestion() {
        this.setState({ displayQuestion: !this.state.displayQuestion })

    }
    changedisplayReponse() {
        this.setState({ displayReponse: !this.state.displayReponse })

    }


    getQuestion(uid, questionType) {
        var apiTag
        if (questionType === "questionEcrite") {
            apiTag = 'questionEcrite'
        } else if (questionType === "questionOraleSansDebat") {
            apiTag = 'questionOraleSansDebat'
        } else if (questionType === "questionAuGouvernement") {
            apiTag = 'questionAuGouvernement'
        }

        fetch(config.apiUrl + apiTag + "/" + uid)
            .then(response => response.json())
            .then(
                (result) => {
                    this.setState({ question: result })
                }

            )
    }




    render() {

        if (this.state.question !== null) {
            return (
                <div className="resultBloc">


                    <div className="row result-bloc-row">
                        <div className="col text-column">
                            <div className="row">
                                {this.props.questionType == "questionEcrite" && "📝 Question écrite d'un député au gouvernement"}
                                {this.props.questionType == "questionOraleSansDebat" && "📢 Question orale d'un député au gouvernement"}
                            </div>
                            <div className="row entete">
                                {<div dangerouslySetInnerHTML={{ __html: generateHighlightedHtml(this.state.question.resume, this.props.query, sanitizeWords) }}></div>}
                            </div>
                        </div>
                    </div>

                    <div className="col">
                        <div className="titleSubResultBloc cursor" onClick={this.changedisplayQuestion.bind(this)}>
                            {this.state.displayQuestion ? "➖" : "➕"} Question de {JSON.parse(this.state.question.question).texteQuestion.texte.split(' ').slice(0, 3).join(' ')}
                            <span className="dossierStatus"> {this.state.question.dateQuestion !== null && "▪ Déposée le " + convertDate(this.state.question.dateQuestion)}</span>
                        </div>
                        {this.state.displayQuestion &&
                            <div className="subResultBloc">
                                <div className="col text-column-sub">

                                    <div dangerouslySetInnerHTML={{ __html: generateHighlightedHtml(JSON.parse(this.state.question.question).texteQuestion.texte, this.props.query, sanitizeWords) }}></div>

                                </div>
                            </div>

                        }
                        <div className="titleSubResultBloc cursor" onClick={this.changedisplayReponse.bind(this)}>
                            {(this.state.displayReponse && this.state.question.dateReponse !== null) && "➖"}
                            {(!this.state.displayReponse && this.state.question.dateReponse !== null) && "➕"}
                            {(this.state.question.dateReponse === null) && "⏱"} Réponse du {this.state.question.ministere}
                            <span className="dossierStatus">{this.state.question.dateReponse !== null ?
                                "▪ Déposée le " + convertDate(this.state.question.dateReponse)
                                : "En attente de réponse"
                            }
                            </span>
                        </div>
                        {(this.state.displayReponse && this.state.question.reponse !== null) &&
                            <div className="subResultBloc">
                                <div className="col text-column-sub">
                                    <div dangerouslySetInnerHTML={{ __html: generateHighlightedHtml(JSON.parse(this.state.question.reponse).texteReponse.texte, this.props.query, sanitizeWords) }}></div>
                                </div>
                            </div>


                        }

                    </div>


                </div>);
        } else {
            return null
        }


    }
}

export default Question
