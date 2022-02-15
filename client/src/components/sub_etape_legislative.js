import React, { Component } from 'react';
import Highlighter from "react-highlight-words";
import Amendement from './amendement'
import convertDate from './utils'

class SubEtapeLegislative extends React.Component {
    constructor(props) {
        super(props);
        this.state = { texteAssocie: null };
        this.getAssociatedDocument()
        console.log(this.state.data)
    }

    getAssociatedDocument() {
        console.log(this.props.data)
        if (this.props.data.texteAssocie !== undefined) {
            fetch('http://localhost:5000/api/documentById/' + this.props.data.texteAssocie)
                .then(response => response.json())
                .then(
                    (result) => {
                        this.setState({ texteAssocie: result })
                    }

                )
            
        }

    }

    changedisplaySubEtapeLegislative() {
        this.setState({ displaySubEtapeLegislative: !this.state.displaySubEtapeLegislative })
    }



    render() {

        return (
            <div className="subResultBloc">
                <div className="col text-column-sub">
                    <div className="col" onClick={this.changedisplaySubEtapeLegislative.bind(this)}>
                        <div className="row entete" >
                            <div className="col">
                                ▪ {this.props.data.libelleActe.nomCanonique} <span className="dossierStatus">  ▪ {convertDate(this.props.data.dateActe)}</span>
                            </div>
                        </div>

                        <div className="col">
                        {this.state.texteAssocie !== null && this.state.texteAssocie.titrePrincipal}

                        </div>



                    </div>


                </div>
            </div>
        );



    }
}

export default SubEtapeLegislative



//{this.firstLetterUppercase(this.props.data.titrePrincipal)} 