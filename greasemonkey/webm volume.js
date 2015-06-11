// ==UserScript==
// @name        webm volume
// @namespace   pverm.github.io
// @author      kama
// @description lowers default webm volume
// @include     *.webm
// @run-at      document-start
// @version     1.0
// @grant       none
// ==/UserScript==


var vids = document.getElementsByTagName("video");
for (var i = 0; i < vids.length; i++) vids[i].volume = 0.5;
void 0;
