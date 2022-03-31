import React, { Component } from 'react';
import * as config from './config';
import Highlighter from "react-highlight-words";
import ParagrapheDiscussionSeancePublique from './paragraphe_discussion_seance_publique';

class PointDiscussionSeancePublique extends React.Component {
    constructor(props) {
        super(props);
        this.state = { displayPoint: false, paragraphList: null };
        this.extractParagraph();
        console.log(this.props.query)

    }

    /* Rtourine to add a single value or array*/
    concatOrPush(value, array) {
        if (value != null) {
            if (Array.isArray(value)) {
                array = array.concat(value)
            } else {
                array.push(value)
            }
        }
        return array
    }

    extractParagraph() {
        let tempParagraphList = []
        if (this.props.data.paragraphe != null) {
            tempParagraphList = this.concatOrPush(this.props.data.paragraphe, tempParagraphList)
        }
        if (this.props.data.interExtraction != null) {



            if (Array.isArray(this.props.data.interExtraction)) {
                for (var i = 0; i < this.props.data.interExtraction.length; i++) {
                    tempParagraphList = this.concatOrPush(this.props.data.interExtraction[i].paragraphe, tempParagraphList)
                }
            } else {
                tempParagraphList = this.concatOrPush(this.props.data.interExtraction.paragraphe, tempParagraphList)

            }

        }

        if (this.props.data.point != null) {
            if (Array.isArray(this.props.data.point)) {
                for (var i = 0; i < this.props.data.point.length; i++) {
                    if (this.props.data.point[i].interExtraction != null) {
                        tempParagraphList = this.concatOrPush(this.props.data.point[i].interExtraction.paragraphe, tempParagraphList)
                    }
                }
            } else {
                if (this.props.data.point.interExtraction != null) {
                    tempParagraphList = this.concatOrPush(this.props.data.point.interExtraction.paragraphe, tempParagraphList)
                }

            }

        }
        tempParagraphList.sort(function (a, b) {
            return a["@ordre_absolu_seance"] - b["@ordre_absolu_seance"];
        });
        this.state.paragraphList = tempParagraphList


        //this.setState({ paragraphList: tempParagraphList })
    }
    changeDisplayPoint() {
        this.setState({ displayPoint: !this.state.displayPoint })

    }


    render() {
        if (this.props.data["@code_grammaire"] === "TITRE_TEXTE_DISCUSSION") {
            return (


                <div className="titreDiscussion">
                    <br />

                    {this.props.data["texte"]}

                </div >
            );
        } else {
            return (

                <div className="">
                    <div className="titleDiscussion cursor hoverclear" onClick={this.changeDisplayPoint.bind(this)}>

                        {this.state.displayPoint ? "🔽": "▶"}
                        { this.props.data.texte != null && this.props.data.texte}
                    </div >


                    {
                        (this.state.paragraphList != null && this.state.displayPoint) && this.state.paragraphList.map((data) => <ParagrapheDiscussionSeancePublique key={data["@id_syceron"]} data={data} query={this.props.query} />)
                    }

                </div >
            );
        }
    }
}

export default PointDiscussionSeancePublique

/*this.props.data.interExtraction !== null  && this.props.data.interExtraction.map((data) => <BlocDiscussionSeancePublique key={data["@id_syceron"]} data={data} query={"this.state.userQuery"} />)*/
