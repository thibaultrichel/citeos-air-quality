// const spawner = require("child_process").spawn;

async function getValue() {
    const pyprocess = spawner('python', [__dirname + "/test.py"]);
    await pyprocess.stdout.on("data", (data) => {
        console.log(data.toString());
    });
}

const getAdvice = (value) => {
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

const getVal = () => {return 2.62};

const displayPred = () => {
    const base = "Prediction result : ";
    const val = getVal();
    const adv = getAdvice(val);
    document.getElementById("pred-result").innerHTML = base + "<b>" + val + "</b>";
    document.getElementById("advice").innerHTML = adv;
};