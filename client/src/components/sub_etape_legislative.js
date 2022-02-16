import React, { Component } from 'react';
import Highlighter from "react-highlight-words";
import Amendement from './amendement'
import { convertDate, sanitizeWords, generateSearchWords, firstLetterUppercase } from './utils'
import NameForm from './name_form';

class SubEtapeLegislative extends React.Component {
    constructor(props) {
        super(props);
        this.state = { texteAssocie: null, amendements: null, dateActe: null, userQuery: '' };
        this.getAssociatedDocument()
        //console.log(this.state.data)
    }

    getAssociatedDocument() {
        //console.log(this.props.data)
        if (this.props.data.texteAssocie !== undefined) {
            fetch('http://localhost:5000/api/documentById/' + this.props.data.texteAssocie)
                .then(response => response.json())
                .then(
                    (result) => {
                        this.setState({ texteAssocie: result })
                        this.getAmendements(result.uid)
                    }

                )

        } else if (this.props.data.libelleActe.nomCanonique == "Discussion en séance publique") {
            var lastEtape
            if (Array.isArray(this.props.data.actesLegislatifs.acteLegislatif)) {
                lastEtape = this.props.data.actesLegislatifs.acteLegislatif.slice(-1)[0]
            } else {
                lastEtape = this.props.data.actesLegislatifs.acteLegislatif
            }
            this.state.dateActe = lastEtape.dateActe
            //console.log(lastEtape)
        } else if (this.props.data.libelleActe.nomCanonique == "Travaux des commissions") {
            var lastEtape = this.props.data.actesLegislatifs.acteLegislatif.actesLegislatifs.acteLegislatif
            if (Array.isArray(lastEtape)) {
                lastEtape = lastEtape.slice(-1)[0]
            } else {
                lastEtape = lastEtape
            }
            this.state.dateActe = lastEtape.dateActe

            fetch('http://localhost:5000/api/documentById/' + lastEtape.texteAdopte)
                .then(response => response.json())
                .then(
                    (result) => {
                        this.setState({ texteAssocie: result })
                        this.getAmendements(result.uid)
                    }

                )

        } else if (this.props.data.libelleActe.nomCanonique == "Commission Mixte Paritaire") {
            var lastEtape = this.props.data.actesLegislatifs.acteLegislatif
            if (Array.isArray(lastEtape)) {
                lastEtape = lastEtape.slice(-1)[0]
            } else {
                lastEtape = lastEtape
            }
            fetch('http://localhost:5000/api/documentById/' + lastEtape.texteAdopte)
                .then(response => response.json())
                .then(
                    (result) => {
                        this.setState({ texteAssocie: result })
                        this.getAmendements(result.uid)
                    }

                )
            this.state.dateActe = lastEtape.dateActe
        }

    }

    getAmendements(uid) {
        fetch('http://localhost:5000/api/amendements/' + uid)
            .then(response => response.json())
            .then(
                (result) => {
                    this.setState({ amendements: result })

                }

            )
    }

    updateAmendementsQuery(event) {
        fetch('http://localhost:5000/api/amendements/' + this.state.texteAssocie.uid)
            .then(response => response.json())
            .then(
                (result) => {
                    this.setState({ amendements: result })

                }

            )
        event.preventDefault();
    }


    refactorNomCanonique(nomCanonique) {
        var prefix = ""
        if (nomCanonique.includes("Discussion en séance publique")) {
            prefix = "🗣"
        } else if (nomCanonique.includes("Travaux des commissions")) {
            prefix = "👷"
        } else if (nomCanonique.includes("Le gouvernement déclare l'urgence")) {
            prefix = "⏰"
        } else if (nomCanonique.includes("Avis du Conseil d'Etat")) {
            prefix = "🏤"
        } else if (nomCanonique.includes("Etude d'impact")) {
            prefix = "👩‍🎓"
        } else if (nomCanonique.includes("1er dépôt d'une initiative")) {
            prefix = "📖"
        } else if (nomCanonique.includes("Dépôt d'une initiative en navette")) {
            prefix = "🚌"
        } else if (nomCanonique.includes("1er dépôt d'une initiative")) {
            prefix = "📖"
        }
        return prefix + " " + nomCanonique
    }

    changedisplayAmendements() {
        this.setState({ displayAmendements: !this.state.displayAmendements })
    }

    handleChange(event) {
        this.setState({ userQuery: event.target.value });
    }

    render() {

        return (
            <div className="subResultBloc">
                <div className="col text-column-sub">
                    <div className="col" >
                        <div className="row entete"  >
                            <div className="col">
                                {this.refactorNomCanonique(this.props.data.libelleActe.nomCanonique)}
                                <span className="dossierStatus">
                                    {this.props.data.dateActe !== null ? "▪ " + convertDate(this.props.data.dateActe) : "▪ " + convertDate(this.state.dateActe)}
                                </span>
                            </div>

                        </div>

                        <div className="col">

                            {/*Title of document legislatif*/}
                            {this.state.texteAssocie !== null &&
                                <Highlighter
                                    searchWords={this.props.query == "" ? [] : generateSearchWords(this.props.query)}
                                    sanitize={sanitizeWords}
                                    textToHighlight={firstLetterUppercase(this.state.texteAssocie.titrePrincipal)} />
                            }

                            {/*Button for show/hide amendements*/}
                            {(this.state.amendements != null && this.state.amendements.numberOfAmendement != 0)
                                && <div className="cursor voirAmendements" onClick={this.changedisplayAmendements.bind(this)}>
                                    {this.state.displayAmendements ? "Cacher " : "Voir "} {this.state.amendements.numberOfAmendement} amendements {this.state.displayAmendements ? "⬇ " : "⬆ "}
                                </div>

                            }

                            {/*Search form in amendements*/}
                            {(this.state.amendements != null && this.state.amendements.numberOfAmendement != 0 && this.state.displayAmendements)
                                && <div className="searchAmendements" >
                                    <form onSubmit={this.updateAmendementsQuery.bind(this)} className="row align-items-center">
                                        <label className="col-md-auto label-for-search-amendements">
                                            Rechercher :
                                        </label>
                                        <div className="col">
                                            <input className="search-amendements-input" value={this.state.userQuery} autoComplete="off" onChange={this.handleChange.bind(this)} placeholder="Ex: climat" />
                                        </div>
                                    </form>
                                </div>

                            }

                            {/* Display Amendements*/}
                            {(this.state.amendements !== null && this.state.displayAmendements) && this.state.amendements.amendements.map((data) => <Amendement key={data.uid} data={data} query={this.props.query} />)}
                            {(this.state.displayAmendements && this.state.amendements.amendements.length < this.state.amendements.numberOfAmendement)
                                && <div className="voirPlus">Voir {this.state.amendements.numberOfAmendement - this.state.amendements.amendements.length} amendements de plus...</div>

                            }
                        </div>



                    </div>


                </div>
            </div >
        );



    }
}

export default SubEtapeLegislative



//{this.firstLetterUppercase(this.props.data.titrePrincipal)} 