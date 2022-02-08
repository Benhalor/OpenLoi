import React, { Component } from 'react';
import Highlighter from "react-highlight-words";
import "./result.css";
import DocumentLegislatif from './document_legislatif';


class Result extends React.Component {
    constructor(props) {
        super(props);
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



    render() {


        return (
            <div className="resultBloc">
                <div className="row">
                    <div className="col text-column">
                        <div className="row ">

                            &#128193; Dossier Législatif

                        </div>
                        <div className="row entete">
                            <Highlighter
                                searchWords={this.props.query.split(' ')}
                                autoEscape={true}
                                textToHighlight={this.firstLetterUppercase((this.props.data.dossier.titre))} />

                        </div>
                        <div className="row">
                            Dépôt:
                        </div>
                        <div className="row">


                        </div>
                    </div>

                    <div className="col">
                        {
                            this.props.data.dossier.anChemin === null
                                ? <button className="btn" >
                                    ---
                                </button>
                                : <a className="btn" target="_blank" rel="noopener noreferrer" href={"https://www.assemblee-nationale.fr/dyn/15/dossiers/alt/" + this.props.data.dossier.anChemin}>
                                    Voir plus
                                </a>
                        }

                        <div className="uid">
                            {this.props.dossierUid}
                        </div>
                    </div>
                </div>
                <div className="row">
                {this.props.data.documents.map((data) => <DocumentLegislatif key={data.uid} data = {data} query={this.props.query} />)}
                </div>
            </div>);


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