// closing an alert button
window.onload = function(){
    document.getElementById('close').onclick = function(){
        window.location.href = "";
        return false;
    };
};