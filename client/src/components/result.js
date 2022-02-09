import React, { Component } from 'react';
import Highlighter from "react-highlight-words";
import "./result.css";
import DocumentLegislatif from './document_legislatif';


class Result extends React.Component {
    constructor(props) {
        super(props);
        this.state = { dossierLegislatif: null, documentsDossierLegislatif: null };
        this.getDossierLegislatif(this.props.dossierUid)
        this.getDocumentsDossierLegislatif(this.props.dossierUid)
    }

    firstLetterUppercase(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    convertDate(str) {
        var date = new Date(str)
        let monthNames = ["jan.", "fev.", "mars", "avril",
            "mai", "juin", "juill.", "août",
            "sept.", "oct.", "nov.", "dec."];

        let day = date.getDate();

        let monthIndex = date.getMonth();
        let monthName = monthNames[monthIndex];

        let year = date.getFullYear();

        return `${day} ${monthName} ${year} `;
    }

    getDossierLegislatif(uid) {
        fetch('http://localhost:5000/api/dossierLegislatif/' + uid)
            .then(response => response.json())
            .then(
                (result) => {
                    this.setState({ dossierLegislatif: result })

                }

            )
    }

    getDocumentsDossierLegislatif(uid) {
        fetch('http://localhost:5000/api/documentsDossierLegislatif/' + uid)
            .then(response => response.json())
            .then(
                (result) => {
                    this.setState({ documentsDossierLegislatif: result })

                }

            )
    }

    extractDossierStatus(arrayOfEtapes) {
        var lastEtape = JSON.parse(arrayOfEtapes).acteLegislatif
        if (Array.isArray(lastEtape)) {
            lastEtape = lastEtape.slice(-1)[0]
        }
        return lastEtape.libelleActe.nomCanonique
    }

    convertDate(str) {
        var date = new Date(str)
        let monthNames = ["jan.", "fev.", "mars", "avril",
            "mai", "juin", "juill.", "août",
            "sept.", "oct.", "nov.", "dec."];

        let day = date.getDate();

        let monthIndex = date.getMonth();
        let monthName = monthNames[monthIndex];

        let year = date.getFullYear();

        return `${day} ${monthName} ${year} `;
    }

    render() {

        if (this.state.dossierLegislatif !== null && this.state.documentsDossierLegislatif !== null) {
            return (
                <div className="resultBloc">


                    <div className="row result-bloc-row">
                        <div className="col text-column">
                            <div className="row">

                                &#128193; Dossier Législatif<span className="dossierStatus">  ▪ {this.extractDossierStatus(this.state.dossierLegislatif.actesLegislatifs)}</span>
                                

                            </div>
                            <div className="row entete">
                                <Highlighter
                                    searchWords={this.props.query.split(' ')}
                                    autoEscape={true}
                                    textToHighlight={this.state.dossierLegislatif.titre } />
                                    {this.convertDate(this.state.dossierLegislatif.lastUpdate)}
                            </div>

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
                        {this.state.documentsDossierLegislatif.documents.map((data) => <DocumentLegislatif key={data.uid} data={data} query={this.props.query} />)}
                    </div>
                </div>);
        } else {
            return null
        }


    }
}

export default Result

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