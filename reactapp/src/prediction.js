import React, {useState, useEffect} from "react";
import axios from "axios";
import "./prediction.css"

function Prediction() {
    const url = "http://localhost:8000/pred";
    const [valeur, setValeur] = useState(null);

    let content = null;

    useEffect(() => {
        axios.get(url)
            .then(response => {
                setValeur(response.data);
            })
    }, [url])

    if (valeur) {
        content =
        <div className="big-content">
            <div className="content">
                <span id="label">ATMO index for the next 12h : </span>
                <span id="pred-result" style={{"backgroundColor": getColor(valeur.pred)}}>{Math.round(parseFloat(valeur.pred) * 100) / 100}</span>
            </div>
            <span id="advice">{getAdvice(valeur.pred)}</span>
        </div>
    }

    function getColor(value) {
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
    }

    function getAdvice(value) {
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
    }

    return (
        <div>
            {content}
        </div>
    )
}

export default Prediction;
