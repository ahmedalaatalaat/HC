document.getElementById('site-name').firstElementChild.innerHTML = 'Bluecare System'
window.onload = function() {
    try {
        // document.getElementsByClassName('vDateField')[0].setAttribute("autocomplete", "off");
        // document.getElementsByClassName('vTimeField')[0].setAttribute("autocomplete", "off");

        var date = document.getElementsByClassName('vDateField');
        for (var i = 0; i < date.length; i++){
            date[i].setAttribute("autocomplete", "off");
        }

        var time = document.getElementsByClassName('vTimeField');
        for (var i = 0; i < time.length; i++){
            time[i].setAttribute("autocomplete", "off");
        }

    } catch (err) {}

    var side_links = document.getElementsByClassName('sidebar-link');
    for (var i = 0; i < side_links.length; i++) {
        if (side_links[i].href == "" && side_links[i].className != 'sidebar-link bookmark-item clone') {
            side_links[i].parentElement.setAttribute("style", "display:none");
        }
    }



};
