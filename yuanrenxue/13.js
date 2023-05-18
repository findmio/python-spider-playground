/** 解题思路：
 *
 * 使用抓包工具分析 页面 yuanrenxue_cookie 来源
 *
 * */

const axios = require("axios");

const headers = {
    "User-Agent": "yuanrenxue.project",
    Cookie: "sessionid=h3qc5xqfibbzi3q0fq2e4xscdt13wojk;",
};

async function getCookie() {
    const res = await axios("https://match.yuanrenxue.cn/match/13", {
        headers,
    });
    const cookie = res.data.match(/\(.*\)/)?.[0];

    if (cookie?.length) {
        return eval(cookie);
    } else {
        throw new Error("获取 cookie 错误");
    }
}

async function getPage(page) {
    const url = `
    https://match.yuanrenxue.cn/api/match/13?page=${page}`;

    const response = await axios(url, {
        headers,
    });

    return response.data.data;
}

async function main() {
    const cookie = await getCookie();

    headers.Cookie += cookie;

    const pages = Array.from({ length: 5 }, (_, i) => i + 1);

    const results = await Promise.all(pages.map((page) => getPage(page)));

    const sum = results.flat().reduce((prev, curr) => prev + curr.value, 0);

    console.log(sum);
}

main();
