import React, { Component } from 'react';
import Highlighter from "react-highlight-words";
import convertDate from './utils'

class Amendement extends React.Component {
    constructor(props) {
        super(props);
    }

    firstLetterUppercase(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    extractStatus(){
        if (this.props.data.etat == "Irrecevable"){
            return "Irrecevable (" + this.props.data.sousEtat+")⚠";
        } else if (this.props.data.sort == "Adopté"){
            return "Adopté le " + convertDate(this.props.data.dateSort)+"✅";
        } else if (this.props.data.sort == "Rejeté"){
            return "Rejeté le " + convertDate(this.props.data.dateSort)+"❌";
        } else if (this.props.data.sort == "Retiré"){
            return "Retiré le " + convertDate(this.props.data.dateSort)+"🚪";
        } else {
            return this.props.data.sort + "" + this.props.data.etat + " " + this.props.data.sousEtat
        }
    }

    render() {


        return (
            <div className="subResultBloc">
                <div className="row" >
                    <div className="col text-column-sub">
                        <div className="row ">
                            <div className="col enteteAmendement">
                                📝 Amendement déposé le {convertDate(this.props.data.dateDepot)} <span className="dossierStatus"> ▪ {this.extractStatus()}</span>
                            </div>
                            <div className="col left-align">
                                <a className="btnAmendement" target="_blank" rel="noopener noreferrer" href={"https://www.assemblee-nationale.fr/dyn/15/dossiers/alt/" + this.props.data.documentURI}>Voir ↗</a>
                            </div>

                        </div>
                        <div className="row" >

                            <div dangerouslySetInnerHTML={{ __html: this.props.data.exposeSommaire }} />


                        </div>
                        <div className="row" >
                            <div dangerouslySetInnerHTML={{ __html: this.props.data.signataires }} />
                        </div>
                        <div className="row" >
                              {this.props.data.uid}
                        </div>



                    </div>


                </div>
            </div >
        );


    }
}

export default Amendement
