import React, { Component } from 'react';
import Highlighter from "react-highlight-words";
import Amendement from './amendement'
import convertDate from './utils'

class DocumentLegislatif extends React.Component {
    constructor(props) {
        super(props);
        this.state = { displayAmendements: false, amendements: null };
        this.getAmendements(this.props.data.uid)
    }


    changeDisplayAmendements() {
        this.setState({ displayAmendements: !this.state.displayAmendements })

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

    firstLetterUppercase(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    render() {

        return (
            <div className="subResultBloc">
                <div className="row">
                    <div className="col text-column-sub">
                        <div className="col" onClick={this.changeDisplayAmendements.bind(this)}>
                            <div className="row entete" >
                                <div className="col">
                                    {this.state.displayAmendements ? "➖" : "➕"} {convertDate(this.props.data.dateDepot)} 
                                    <span className="dossierStatus">{(this.state.amendements != null && this.state.amendements.numberOfAmendement!=0) ? "▪ " + this.state.amendements.numberOfAmendement+ " amendements":""} </span>
                                </div>
                            </div>
                            <div className="row" >
                                <Highlighter
                                    searchWords={this.props.query.split(' ')}
                                    autoEscape={true}
                                    textToHighlight={this.firstLetterUppercase(this.props.data.titrePrincipal)} />

                            </div>



                        </div>
                        <div className="col">

                            {this.state.displayAmendements && this.state.amendements.amendements.map((data) => <Amendement key={data.uid} data={data} query={this.props.query} />)}
                            {(this.state.displayAmendements && this.state.amendements.amendements.length < this.state.amendements.numberOfAmendement) 
                            &&  <div className="voirPlus">Voir {this.state.amendements.numberOfAmendement - this.state.amendements.amendements.length} amendements de plus...</div>
                            
                            }
                        </div>
                    </div>


                </div>
            </div>
        );
    


    }
}

export default DocumentLegislatif


//

/*<div className="col">
                        <button className="btn">
                            Lien
                        </button>
                        <div className="uid">
                            {this.props.data.uid}
                        </div>
                    </div>
                    
                    
                    
                    
                    
                    {this.props.data.datePublication === null
                                ? "Non publié"
                                : "Publication: " + this.convertDate(this.props.data.datePublication)}
                                
                                
                                */