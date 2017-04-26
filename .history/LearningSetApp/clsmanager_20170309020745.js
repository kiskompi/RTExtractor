document.addEventListener('click', function(e) {
    e = e || window.event;
    var target = e.target || e.srcElement,
        text = target.textContent || text.innerText;   
}, false);

var wn = window.open("", "_blank", "height=300, width=500");
wn.document.write("
<html>
<head>
</head>
<body>
    <!-- textbox to display element (only for user to check) -->
    <div style="float:left;" id = "elementcode">Element code:</div>
    <!-- list of possible crawler classes -->
    <div style="float:right;">
    <label>Select list</label>
    <br>
    <select id = "myList">
        <option value = "1">SectionReveal</option>
        <option value = "2">LanguageSelection</option>
        <option value = "3">InnerLink</option>
        <option value = "4">OuterLink</option>
    </select>
    </div>
</body>
</html>
");