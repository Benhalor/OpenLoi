import React, { Component } from 'react';
import * as config from './config';
import Highlighter from "react-highlight-words";
import { convertDate, sanitizeWords, generateSearchWords } from './utils'

class ParagrapheDiscussionSeancePublique extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};


    }

    render() {

        return (


            <div className="">
                <span className="orateurName">
                    {this.props.data.orateurs !== null && this.props.data.orateurs.orateur.nom + ". "}
                </span>


                <span className="orateurText">

                    {
                        <Highlighter
                            searchWords={this.props.query == "" ? [] : generateSearchWords(this.props.query)}
                            sanitize={sanitizeWords}
                            textToHighlight={this.props.data.texte["#text"]} />

                    }
                </span>
                <br />
                <br />



            </div >
        );

    }
}

export default ParagrapheDiscussionSeancePublique

