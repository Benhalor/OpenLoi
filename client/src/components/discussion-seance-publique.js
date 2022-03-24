import React, { Component } from 'react';
import * as config from './config';
import Highlighter from "react-highlight-words";
//import AmendementDetail from './amendement_detail.js';
import { convertDate, sanitizeWords, generateHighlightedHtml } from './utils'

class DiscussionSeancePublique extends React.Component {
    constructor(props) {
        super(props);
        this.state = { displayDiscussion: false, discussion: null };
        this.getDiscution(this.props.data.reunionRef)
    }

    changeDisplayDiscussion() {
        this.setState({ displayDiscussion: !this.state.displayDiscussion })

    }

    getDiscution(uid) {
        fetch(config.apiUrl + 'discussionAN/uid=' + uid)
            .then(response => response.json())
            .then(
                (result) => {
                    this.setState({ discussion: result })

                }

            )


    }

    render() {

        if (this.props.data.libelleActe.nomCanonique === "Discussion en séance publique") {
            return (


                <div className="amendement">

                    <div className="" >
                        <div className="col text-column-amendement">
                            <div className="row hoverclear cursor" onClick={this.changeDisplayDiscussion.bind(this)}>
                                <div className="col enteteAmendement">
                                🗣 {this.props.data.reunionRef}
                                </div>


                            </div>
                            {this.state.displayDiscussion &&
                                <div className="col textAmendement">
                                    {this.state.discussion !== null && this.state.discussion.contenu}
                                </div>
                            }

                        </div>

                    </div>
                </div >
            );
        } else {
            return (
                <div className="amendement">

                    <div className="row" >
                        <div className="col text-column-amendement">
                            <div className="row">
                                <div className="col">
                                    {this.props.data.statutConclusion.libelle === "adopté" && "✅ "} {this.props.data.statutConclusion.libelle}
                                    {" le " + convertDate(this.props.data.dateActe)}
                                </div>
                            </div>
                        </div>

                    </div>
                </div >
            );
        }



    }
}

export default DiscussionSeancePublique

