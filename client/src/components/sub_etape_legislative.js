import React, { Component } from 'react';
import Highlighter from "react-highlight-words";
import Amendement from './amendement'
import { convertDate, sanitizeWords, generateSearchWords, firstLetterUppercase } from './utils'
import * as config from './config';

class SubEtapeLegislative extends React.Component {
    constructor(props) {
        super(props);
        this.state = { texteAssocie: null, amendements: null, amendementsQuery: null, dateActe: null, userQuery: "" };
        this.getAssociatedDocument()
        console.log(this.props.senatChemin.split("/").slice(-1)[0].slice(0, -5))
    }

    getAssociatedDocument() {
        //console.log(this.props.data)
        if (this.props.data.texteAssocie !== undefined) {
            fetch(config.apiUrl + 'documentById/' + this.props.data.texteAssocie)
                .then(response => response.json())
                .then(
                    (result) => {
                        this.setState({ texteAssocie: result })
                        this.getAmendements(result.uid, this.props.data.codeActe)
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
            // TODO placer ici les discussions en séance publique.
            //console.log(lastEtape)
        } else if (this.props.data.libelleActe.nomCanonique == "Travaux des commissions") {
            try {
                var lastEtape = this.props.data.actesLegislatifs.acteLegislatif.actesLegislatifs.acteLegislatif
                if (Array.isArray(lastEtape)) {
                    lastEtape = lastEtape.slice(-1)[0]
                } else {
                    lastEtape = lastEtape
                }
                this.state.dateActe = lastEtape.dateActe

                fetch(config.apiUrl + 'documentById/' + lastEtape.texteAdopte)
                    .then(response => response.json())
                    .then(
                        (result) => {
                            this.setState({ texteAssocie: result })
                            this.getAmendements(result.uid, this.props.data.codeActe)
                        }

                    )
            } catch (error) {
                console.error(error);
                console.log(this.props.data)
            }



        } else if (this.props.data.libelleActe.nomCanonique == "Commission Mixte Paritaire") {
            var lastEtape = this.props.data.actesLegislatifs.acteLegislatif
            if (Array.isArray(lastEtape)) {
                lastEtape = lastEtape.slice(-1)[0]
            } else {
                lastEtape = lastEtape
            }
            fetch(config.apiUrl + 'documentById/' + lastEtape.texteAdopte)
                .then(response => response.json())
                .then(
                    (result) => {
                        this.setState({ texteAssocie: result })
                        this.getAmendements(result.uid, this.props.data.codeActe)
                    }

                )
            this.state.dateActe = lastEtape.dateActe
        }

    }

    getAmendements(uid, codeActe) {
        if (codeActe.slice(0, 2) == "AN") {
            fetch(config.apiUrl + 'amendementsAN/uid=' + uid)
                .then(response => response.json())
                .then(
                    (result) => {
                        this.setState({ amendements: result })

                    }

                )
        } else if (codeActe.slice(0, 2) == "SN") {
            var projectId
            var id
            try {
                projectId = this.props.senatChemin.split("/").slice(-1)[0].slice(0, -5) // something like pjl21-350
                id = uid.slice(-4)
                fetch(config.apiUrl + 'amendementsSenat/id=' + id + '&projectId=' + projectId)
                    .then(response => response.json())
                    .then(
                        (result) => {
                            this.setState({ amendements: result })

                        }

                    )
            } catch {

            }

        }

    }

    updateAmendementsQuery(event) {
        if (this.state.userQuery != "") {
            fetch(config.apiUrl + 'amendementsQuery/' + this.state.userQuery + "&" + this.state.texteAssocie.uid)
                .then(response => response.json())
                .then(
                    (result) => {
                        this.setState({ amendementsQuery: result })

                    }

                )
        } else {
            this.setState({ amendementsQuery: null })
            this.getAmendements(this.state.texteAssocie.uid)
        }
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
                            <div className={(this.state.amendements != null && this.state.amendements.numberOfAmendement != 0) ? "row voirAmendements " : ""} >
                                {(this.state.amendements != null && this.state.amendements.numberOfAmendement != 0)
                                    && <div className="cursor hoverclear showAmendements" onClick={this.changedisplayAmendements.bind(this)}>
                                        {this.state.displayAmendements ? "Voir " : "Voir "} {this.state.amendements.numberOfAmendement} amendements {this.state.displayAmendements ? "⬇ " : "⬆ "}
                                    </div>

                                }

                                {/*Search form in amendements*/}
                                {(this.state.amendements != null && this.state.amendements.numberOfAmendement != 0 && this.state.displayAmendements)
                                    &&
                                    <form onSubmit={this.updateAmendementsQuery.bind(this)} className="row align-items-center">

                                        <input className="search-amendements-input" value={this.state.userQuery} autoComplete="off" onChange={this.handleChange.bind(this)} placeholder="🔎 Rechercher" />
                                    </form>


                                }
                            </div>

                            {/* Display Amendements*/}
                            {(this.state.amendementsQuery === null && this.state.amendements !== null && this.state.displayAmendements) && this.state.amendements.amendements.map((data) => <Amendement key={data.uid + this.props.query} data={data} query={this.props.query} />)}
                            {(this.state.amendementsQuery === null && this.state.displayAmendements && this.state.amendements.amendements.length < this.state.amendements.numberOfAmendement)
                                && <div className="voirPlus">Voir {this.state.amendements.numberOfAmendement - this.state.amendements.amendements.length} amendements de plus...</div>

                            }

                            {/* Display Amendements got by search*/}
                            {(this.state.amendementsQuery !== null && this.state.displayAmendements) && this.state.amendementsQuery.amendements.map((data) => <Amendement key={data.uid + this.state.userQuery} data={data} query={this.state.userQuery} />)}
                            {(this.state.amendementsQuery !== null && this.state.displayAmendements && this.state.amendementsQuery.amendements.length < this.state.amendementsQuery.numberOfAmendement)
                                && <div className="voirPlus">Voir {this.state.amendementsQuery.numberOfAmendement - this.state.amendementsQuery.amendements.length} amendements de plus...</div>

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