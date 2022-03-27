import './content.css';
import {Component} from "react";
// const readJson = require("read-json-sync");
import jsondata from './result.json';

class Content extends Component {
    val = this.getValFromFile();
    render() {
        return (
            <div className="big-content">
                <div className="content">
                    <span id="label">ATMO index for the next 12h : </span>
                    <span id="pred-result" style={{"backgroundColor": this.getColor(this.val)}}>{this.val}</span>
                </div>
                <span id="advice">{this.getAdvice(this.val)}</span>
            </div>
        );
    }

    getColor(value) {
        const colors = {
            1: "cyan",
            2: "lime",
            3: "yellow",
            4: "orange",
            5: "red",
            6: "purple"
        }
        const intval = Math.round(value);
        return colors[intval];
    };

    getAdvice(value) {
        const advices = {
            1: "Bonne qualité de l'air :)",
            2: "Qualité de l'air moyenne, privilégiez les transports",
            3: "Qualité de l'air dégradée, évitez de prendre votre voiture",
            4: "Mauvaise qualité de l'air, ne prenez pas votre voiture",
            5: "Très mauvaise qualité de l'air, attention pour votre santé",
            6: "Qualité de l'air excrécrable, mettez un masque"
        }
        const intval = Math.round(value);
        return advices[intval];
    };

    getValFromFile() {
        const stringVal = jsondata["result"];
        return Math.round(parseFloat(stringVal) * 100) / 100;
    };
}

export default Content;
