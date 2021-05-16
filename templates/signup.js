const msg = document.querySelector(".msg");

function myfunct() {
    if ( msg.classList.contains("hidden") ) {
        msg.classList.remove("hidden");
    }
    else {
        msg.classList.add("hidden");
    }
}