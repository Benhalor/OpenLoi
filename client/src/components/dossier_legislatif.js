import React, { Component } from 'react';
import Highlighter from "react-highlight-words";
import "./result.css";
import DocumentLegislatif from './document_legislatif';
import EtapeLegislative from './etape_legislative';

import convertDate from './utils'

class DossierLegislatif extends React.Component {
    constructor(props) {
        super(props);
        this.state = { dossierLegislatif: null, etapesLegislatives: null, displayEtapes: false, displayAmendements: false };
        this.getDossierLegislatif(this.props.dossierUid)
    }

    changeDisplayEtapes() {
        this.setState({ displayEtapes: !this.state.displayEtapes })

    }
    changeDisplayAmendements() {
        this.setState({ displayAmendements: !this.state.displayAmendements })

    }

    firstLetterUppercase(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    getDossierLegislatif(uid) {
        fetch('http://localhost:5000/api/dossierLegislatif/' + uid)
            .then(response => response.json())
            .then(
                (result) => {
                    this.setState({ dossierLegislatif: result })
                    this.getEtapesLegislatives(result.actesLegislatifs)
                }

            )
    }

    getEtapesLegislatives(arrayOfEtapes) {

        var jsonParse = JSON.parse(arrayOfEtapes).acteLegislatif
        if (Array.isArray(jsonParse)) {
            this.setState({ etapesLegislatives: jsonParse })
        } else {
            this.setState({ etapesLegislatives: [jsonParse] })
        }
    }



    extractDossierStatus(arrayOfEtapes) {
        var lastEtape = JSON.parse(arrayOfEtapes).acteLegislatif
        if (Array.isArray(lastEtape)) {
            lastEtape = lastEtape.slice(-1)[0]
        }
        var assemblee = ""
        if (lastEtape.codeActe.substring(0, 2) == "AN") {
            assemblee = "AN"
        } else if (lastEtape.codeActe.substring(0, 2) == "SN") {
            assemblee = "Sénat"
        } else {
            assemblee = lastEtape.codeActe
        }

        return lastEtape.libelleActe.nomCanonique + " - " + assemblee
    }

    sanitizeWords(string) {
        return string.normalize("NFD").replace(/\p{Diacritic}/gu, "")
    }

    generateSearchWords(spacedSeparatedWords) {
        var listOfWords = spacedSeparatedWords.split(" ")
        for (var i = 0; i < listOfWords.length; i++) {
            listOfWords[i] = "\\b(?=\\w*" + listOfWords[i] + ")\\w+\\b"
        }
        return listOfWords
    }


    render() {

        if (this.state.dossierLegislatif !== null && this.state.etapesLegislatives !== null) {
            return (
                <div className="resultBloc">


                    <div className="row result-bloc-row">
                        <div className="col text-column">
                            <div className="row">

                                &#128193; Dossier Législatif <span className="dossierStatus">  ▪ {this.extractDossierStatus(this.state.dossierLegislatif.actesLegislatifs)}</span>


                            </div>
                            <div className="row entete">
                                <Highlighter
                                    searchWords={this.props.query == "" ? [] : this.generateSearchWords(this.props.query)}
                                    sanitize={this.sanitizeWords}
                                    textToHighlight={this.state.dossierLegislatif.titre} />


                            </div>
                            <span className="dossierStatus">  ⏲ Derniers éléments du {convertDate(this.state.dossierLegislatif.lastUpdate)}</span>
                        </div>

                        <div className="left-align">
                            {
                                this.state.dossierLegislatif.anChemin === null
                                    ? <button className="btn" >
                                        ---
                                    </button>
                                    : <a className="btn" target="_blank" rel="noopener noreferrer" href={"https://www.assemblee-nationale.fr/dyn/15/dossiers/alt/" + this.state.dossierLegislatif.anChemin}>
                                        Voir ↗
                                    </a>
                            }

                            <div className="uid">
                                {this.props.dossierUid}

                            </div>
                        </div>
                    </div>
                    <div className="col">
                        <div className="titleSubResultBloc" onClick={this.changeDisplayEtapes.bind(this)}>
                            {this.state.displayEtapes ? "➖" : "➕"} Élements du dossier 📖
                        </div>
                        {this.state.displayEtapes && this.state.etapesLegislatives.map((data) => <EtapeLegislative key={data.uid} data={data} query={this.props.query} />)}

                    </div>

                </div>);
        } else {
            return null
        }


    }
}

export default DossierLegislatif

/*
{this.props.result.anChemin === null
                            ? <button className="btn" >
                                ---
                            </button>
                            : <a className="btn" target="_blank" rel="noopener noreferrer" href={"https://www.assemblee-nationale.fr/dyn/15/dossiers/alt/" + this.props.result.anChemin}>
                                Voir plus
                            </a>
                        }
                        */



/*


                */