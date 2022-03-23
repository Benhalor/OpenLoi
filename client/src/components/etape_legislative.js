import React, { Component } from 'react';
import Highlighter from "react-highlight-words";
import Amendement from './amendement'
import {convertDate,sanitizeWords,generateSearchWords} from './utils'
import SubEtapeLegislative from './sub_etape_legislative';

class EtapeLegislative extends React.Component {
    constructor(props) {
        super(props);
        this.state = { displayEtapeLegislative: false, subEtapesLegislatives: null };
        this.getSubEtapesLegislatives(this.props.data.actesLegislatifs)
        console.log(this.props.data)
    }

    getSubEtapesLegislatives(arrayOfEtapes) {

        var jsonParse = arrayOfEtapes.acteLegislatif
        if (Array.isArray(jsonParse)) {
            this.setState({ subEtapesLegislatives: jsonParse.reverse() })
        } else {
            this.setState({ subEtapesLegislatives: [jsonParse] })
        }
    }


    changeDisplayEtapeLegislative() {
        if (this.state.subEtapesLegislatives === null && !this.state.displayEtapeLegislative) {
            this.getSubEtapesLegislatives(this.props.data.actesLegislatifs)
        }
        this.setState({ displayEtapeLegislative: !this.state.displayEtapeLegislative })

    }

    extractDossierStatus(lastEtape) {
        var assemblee = ""
        if (lastEtape.codeActe.substring(0, 2) == "AN") {
            assemblee = " - " +"AN"
        } else if (lastEtape.codeActe.substring(0, 2) == "SN") {
            assemblee = " - " +"Sénat"
        } else if (lastEtape.codeActe.substring(0, 4) == "PROM"){
            assemblee = ""
        } else if (lastEtape.codeActe.substring(0, 3) == "CMP"){
            assemblee = ""
        } else if (lastEtape.codeActe.substring(0, 2) == "CC"){
            assemblee = ""
        }  else {
            assemblee = " - " +lastEtape.codeActe
        }

        return lastEtape.libelleActe.nomCanonique +  assemblee
    }


    render() {
        return (
            <div className="subResultBloc">
                <div className="col text-column-sub">
                    <div className="col hovergrey cursor" onClick={this.changeDisplayEtapeLegislative.bind(this)}>
                        <div className="row entete" >
                            <div className="col">
                                {this.state.displayEtapeLegislative ? "➖" : "➕"} {this.extractDossierStatus(this.props.data)}
                            </div>
                        </div>
                    </div>
                    <div className="col">

                        {(this.state.displayEtapeLegislative && this.state.subEtapesLegislatives !== null) &&this.state.subEtapesLegislatives.map((data) => <SubEtapeLegislative key={data.uid} data={data} query={this.props.query} senatChemin={this.props.senatChemin} />)}

                    </div>


                </div>
            </div>
        );





    }
}

export default EtapeLegislative



//{this.firstLetterUppercase(this.props.data.titrePrincipal)} 