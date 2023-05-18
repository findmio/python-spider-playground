const axios = require("axios");

var window = {};

const headers = {
    "User-Agent": "yuanrenxue.project",
    Cookie: "sessionid=h3qc5xqfibbzi3q0fq2e4xscdt13wojk;",
};

async function getWasm() {
    const { data: bytes } = await axios.get(
        "https://match.yuanrenxue.cn/static/match/match15/main.wasm",
        {
            responseType: "arraybuffer",
        }
    );

    const results = await WebAssembly.instantiate(bytes);
    const instance = results.instance;

    window.q = instance.exports.encode;
}

function getSign() {
    var t1 = parseInt(Date.parse(new Date()) / 1000 / 2);
    var t2 = parseInt(
        Date.parse(new Date()) / 1000 / 2 - Math.floor(Math.random() * 50 + 1)
    );

    return window.q(t1, t2).toString() + "|" + t1 + "|" + t2;
}

async function getPage(page) {
    const m = getSign();

    const url = `https://match.yuanrenxue.cn/api/match/15?page=${page}&m=${m}`;

    const response = await axios(url, {
        headers,
    });

    return response.data.data;
}

async function main() {
    await getWasm();
    
    const pages = Array.from({ length: 5 }, (_, i) => i + 1);

    const results = await Promise.all(pages.map((page) => getPage(page)));

    const sum = results.flat().reduce((prev, curr) => prev + curr.value, 0);

    console.log(sum);
}

main();
