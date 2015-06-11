// ==UserScript==
// @name        skip steamfilter
// @namespace   pverm.github.io
// @author      kama
// @description skips steam linkfilter
// @match       http://steamcommunity.com/linkfilter/*
// @match       https://steamcommunity.com/linkfilter/*
// @version     1.0
// @grant       none
// ==/UserScript==

var url = window.location.href;
var url_ttp = url.substring(1);
var pos = url_ttp.indexOf("http");
var newurl = urlmhttp.substring(pos);
window.location.href = newurl;
