import React, { Component } from 'react';
import * as config from './config';
import Highlighter from "react-highlight-words";
//import AmendementDetail from './amendement_detail.js';
import { convertDate, sanitizeWords, generateHighlightedHtml } from './utils'
import PointDiscussionSeancePublique from './point_discussion_seance_publique';

class DiscussionSeancePublique extends React.Component {
    constructor(props) {
        super(props);
        this.state = { displayDiscussion: false, discussion: null };
        this.getDiscution(this.props.data.reunionRef)
       // console.log(this.props.data)
        
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
                    console.log(JSON.parse(result.contenu).point)

                }

            )


    }

    render() {

        if (this.props.data.libelleActe.nomCanonique === "Discussion en séance publique") {
            return (


                <div className="discussion">

                    <div className="" >
                        <div className="col text-column-amendement">
                            <div className="row hoverclear cursor" onClick={this.changeDisplayDiscussion.bind(this)}>
                                <div className="col enteteAmendement">
                                🗣 Discussion du {convertDate(this.props.data.dateActe)}
                                </div>


                            </div>
                            {this.state.displayDiscussion &&
                                <div className="col textAmendement">
                                    {this.state.discussion !== null && 
                                    JSON.parse(this.state.discussion.contenu).point.map((data) => <PointDiscussionSeancePublique key={data["@id_syceron"]} data={data} query={this.props.query} />)
                                    
                                    
                                    }
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

