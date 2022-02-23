import React, { Component } from 'react';
import Highlighter from "react-highlight-words";
import * as config from './config';

import { convertDate, sanitizeWords, generateSearchWords } from './utils'

class Debat extends React.Component {
    constructor(props) {
        super(props);
        this.state = { displayDebat: false, debat: null };
        this.getQuestion(this.props.questionUid, this.props.questionType)
    }

    changedisplayDebat() {
        this.setState({ displayDebat: !this.state.displayDebat })

    }

    getQuestion(uid, questionType) {
        var apiTag = "questionAuGouvernement"

        fetch(config.apiUrl + apiTag + "/" + uid)
            .then(response => response.json())
            .then(
                (result) => {
                    this.setState({ debat: result })
                }

            )
    }


    render() {

        if (this.state.debat !== null) {
            return (
                <div className="resultBloc">


                    <div className="row result-bloc-row">
                        <div className="col text-column">
                            <div className="row">
                                📝 Débat en hémicyle d'un député avec le gouvernement
                            </div>
                            <div className="row entete">
                                <Highlighter
                                    searchWords={this.props.query == "" ? [] : generateSearchWords(this.props.query)}
                                    sanitize={sanitizeWords}
                                    textToHighlight={this.state.debat.resume} />


                            </div>
                        </div>
                    </div>

                    <div className="col">
                        
                        <div className="titleSubResultBloc cursor" onClick={this.changedisplayDebat.bind(this)}>
                            {(this.state.displayDebat && this.state.debat.dateReponse !== null) && "➖"}
                            {(!this.state.displayDebat && this.state.debat.dateReponse !== null) && "➕"}
                            {(this.state.debat.displayDebat === null) && "⏱"} Avec le {this.state.debat.ministere}
                            <span className="dossierStatus">{this.state.debat.dateReponse !== null ?
                                "▪ Le " + convertDate(this.state.debat.dateReponse)
                                : "En attente de débat"
                            }
                            </span>
                        </div>
                        {(this.state.displayDebat && this.state.debat.reponse !== null) &&
                            <div className="subResultBloc">
                                <div className="col text-column-sub">

                                    <Highlighter
                                        searchWords={this.props.query == "" ? [] : generateSearchWords(this.props.query)}
                                        sanitize={sanitizeWords}
                                        textToHighlight={JSON.parse(this.state.debat.reponse).texteReponse.texte} />


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

export default Debat
