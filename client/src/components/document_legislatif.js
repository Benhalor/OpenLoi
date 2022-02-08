import React, { Component } from 'react';
import Highlighter from "react-highlight-words";

class DocumentLegislatif extends React.Component {
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
            <div className="subResultBloc">
                <div className="row">
                    <div className="col text-column-sub">
                        <div className="row entete">
                            <div className="col">
                                {this.props.data.denominationStructurelle} - le {this.convertDate(this.props.data.dateDepot)}
                            </div>
                        </div>
                        <div className="row">
                            <Highlighter
                                searchWords={this.props.query.split(' ')}
                                autoEscape={true}
                                textToHighlight={this.firstLetterUppercase(this.props.data.titrePrincipal)} />

                        </div>
                        <div className="row">
                            
                        </div>
                        <div className="row">

                        {this.props.data.uid}
                        </div>
                    </div>

                    
                </div>
            </div>
        );


    }
}

export default DocumentLegislatif

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