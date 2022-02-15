import React, { Component } from 'react';
import Highlighter from "react-highlight-words";
import Amendement from './amendement'
import convertDate from './utils'
import SubEtapeLegislative from './sub_etape_legislative';

class EtapeLegislative extends React.Component {
    constructor(props) {
        super(props);
        this.state = { displayEtapeLegislative: false, subEtapesLegislatives: null };
        this.getSubEtapesLegislatives(this.props.data.actesLegislatifs)
    }

    getSubEtapesLegislatives(arrayOfEtapes) {

        var jsonParse = arrayOfEtapes.acteLegislatif
        if (Array.isArray(jsonParse)) {
            this.setState({ subEtapesLegislatives: jsonParse })
        } else {
            this.setState({ subEtapesLegislatives: [jsonParse] })
        }
        console.log(this.state.subEtapesLegislatives)
    }


    changeDisplayEtapeLegislative() {
        if (this.state.subEtapesLegislatives === null && !this.state.displayEtapeLegislative) {
            this.getSubEtapesLegislatives(this.props.data.actesLegislatifs)
        }
        this.setState({ displayEtapeLegislative: !this.state.displayEtapeLegislative })

    }


    render() {
        return (
            <div className="subResultBloc">
                <div className="col text-column-sub">
                    <div className="col" onClick={this.changeDisplayEtapeLegislative.bind(this)}>
                        <div className="row entete" >
                            <div className="col">
                                {this.state.displayEtapeLegislative ? "➖" : "➕"} {this.props.data.libelleActe.nomCanonique}
                            </div>
                        </div>
                    </div>
                    <div className="col">

                        {(this.state.displayEtapeLegislative && this.state.subEtapesLegislatives !== null) &&this.state.subEtapesLegislatives.map((data) => <SubEtapeLegislative key={data.uid} data={data} query={this.props.query} />)}

                    </div>


                </div>
            </div>
        );





    }
}

export default EtapeLegislative



//{this.firstLetterUppercase(this.props.data.titrePrincipal)} 