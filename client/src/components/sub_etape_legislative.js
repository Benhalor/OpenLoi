import React, { Component } from 'react';
import Highlighter from "react-highlight-words";
import Amendement from './amendement'
import convertDate from './utils'

class SubEtapeLegislative extends React.Component {
    constructor(props) {
        super(props);
        this.state = { displaySubEtapeLegislative: false, subEtapeLegislative: null };
        console.log("dfdsfsdsdfsdfsdfdsfsdfsfds")
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
                                {this.state.displaySubEtapeLegislative ? "➖" : "➕"} {this.props.data.libelleActe.nomCanonique}
                            </div>
                        </div>
                       



                    </div>
                    

                </div>
            </div>
        );



    }
}

export default SubEtapeLegislative



//{this.firstLetterUppercase(this.props.data.titrePrincipal)} 