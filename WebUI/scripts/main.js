// const spawner = require("child_process").spawn;

async function getValue() {
    const pyprocess = spawner('python', [__dirname + "/test.py"]);
    await pyprocess.stdout.on("data", (data) => {
        console.log(data.toString());
    });
}

const getColorAndAdvice = (value) => {
    const utils = {
        1: ["Bonne qualité de l'air :)", "cyan"],
        2: ["Qualité de l'air moyenne, privilégiez les transports", "lime"],
        3: ["Qualité de l'air dégradée, évitez de prendre votre voiture", "yellow"],
        4: ["Mauvaise qualité de l'air, ne prenez pas votre voiture", "orange"],
        5: ["Très mauvaise qualité de l'air, attention pour votre santé", "red"],
        6: ["Qualité de l'air excrécrable, mettez un masque", "purple"]
    }
    const intval = Math.round(value);
    return utils[intval];
};

const getVal = () => {return 2.62};

const displayPred = () => {
    const val = getVal();
    const utils = getColorAndAdvice(val);
    const advice = utils[0];
    const color = utils[1];
    document.getElementById("pred-result").innerHTML = val.toString();
    document.getElementById("pred-result").style.backgroundColor = color;
    document.getElementById("advice").innerHTML = advice;
};