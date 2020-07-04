// https://ko.wiktionary.org/?action=render&oldid=
var a = [];
var trs = document.querySelectorAll('tr[valign]');
for (var i = 0; i < trs.length; i++) {
	var syllChars = {
		mid: trs[i].cells[1].innerText,
		high: (trs[i].cells[2] ? trs[i].cells[2].innerText : ''),
	};
	// don't do this in the browser
	if (false) {
		for (var grade in syllChars) {
			if (syllChars[grade]) {
				syllChars[grade] = syllChars[grade].replace(/•/g, ',').replace(/\s*\(/g, ':').replace(/\s*[()]\s*/g, '').split(',');
				for (var i = 0; i < syllChars[grade].length; i++) {
					var temp = syllChars[grade][i].split(':');
					var char = temp[0];
					var eumhun = temp[1];
					a.push((grade == "mid" ? 2 : 1) + "\t" + char + "\t" + eumhun);
				}
			}
		}
	}
	a.push(syllChars);
}
console.log(JSON.stringify(a));
