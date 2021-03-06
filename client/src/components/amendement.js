import React, { Component } from 'react';
import Highlighter from "react-highlight-words";
//import AmendementDetail from './amendement_detail.js';
import { convertDate, sanitizeWords, generateHighlightedHtml } from './utils'

class Amendement extends React.Component {
    constructor(props) {
        super(props);
        this.state = { displayAmendement: false };
    }

    changeDisplayAmendement() {
        this.setState({ displayAmendement: !this.state.displayAmendement })

    }


    extractStatus() {
        if (this.props.data.etat.includes("Irrecevable")) {
            return "Irrecevable (" + this.props.data.sousEtat + ")⚠";
        } else if (this.props.data.sort == "Adopté") {
            return "Adopté le " + convertDate(this.props.data.dateSort) + "✅";
        } else if (this.props.data.sort == "Rejeté") {
            return "Rejeté le " + convertDate(this.props.data.dateSort) + "❌";
        } else if (this.props.data.sort.includes("Retiré") || this.props.data.etat.includes("Retiré")) {
            if (this.props.data.dateSort !== null) {
                return "Retiré le " + convertDate(this.props.data.dateSort) + "🚪";
            } else {
                return "Retiré🚪";
            }

        } else if (this.props.data.sort == "Tombé") {
            return "Tombé le " + convertDate(this.props.data.dateSort) + "🪂";
        } else if (this.props.data.sort == "Non soutenu") {
            return "Non soutenu le " + convertDate(this.props.data.dateSort) + "😑";
        } else if (this.props.data.etat == "A discuter") {
            return "A discuter 💬";
        } else {
            return this.props.data.sort + "|" + this.props.data.etat + "| " + this.props.data.sousEtat
        }
    }

    render() {


        return (
            

            <div className="amendement">
                
                <div className="row" >
                    <div className="col text-column-amendement">
                        <div className="row hoverclear cursor" onClick={this.changeDisplayAmendement.bind(this)}>
                            <div className="col enteteAmendement">
                                📝 {this.props.data.article} {this.props.data.alinea}  - déposé le {convertDate(this.props.data.dateDepot)} <span className="dossierStatus"> ▪ {this.extractStatus()}</span>
                            </div>
                            <div className="col left-align">
                                <a className="btnAmendement" target="_blank" rel="noopener noreferrer" href={"http://www.assemblee-nationale.fr/dyn/15/amendements/" + this.props.data.uid}>Voir ↗</a>
                            </div>

                        </div>
                        {this.state.displayAmendement &&
                            <div className="col">
                                <div className="row textDispositifAmendement" >
                                    <div dangerouslySetInnerHTML={{ __html: generateHighlightedHtml(this.props.data.dispositif, this.props.query, sanitizeWords) }}></div>
                                </div>
                                <div className="row textAmendement" >
                                    <div dangerouslySetInnerHTML={{ __html: generateHighlightedHtml(this.props.data.exposeSommaire, this.props.query, sanitizeWords) }}></div>
                                </div>
                                <div className="row deputeNames" >
                                    <div dangerouslySetInnerHTML={{ __html: generateHighlightedHtml(this.props.data.signataires, this.props.query, sanitizeWords) }}></div>
                                </div>

                            </div>
                        }

                    </div>

                </div>
            </div >
        );


    }
}

export default Amendement


/*                                <a className="btnAmendement" target="_blank" rel="noopener noreferrer" href={"https://www.assemblee-nationale.fr" + this.props.data.urlDivisionTexteVise}>Voir ↗</a>
*/