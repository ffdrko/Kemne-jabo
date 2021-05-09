const point = document.querySelector(".point");
const balance = document.querySelector(".balance");
const withdraw = document.querySelector(".withdraw");
const click_search = document.querySelector(".click-search");
const click_guide = document.querySelector(".click-guide");
const src_bar = document.querySelector(".src-bar");
const gd_bar = document.querySelector(".guide-bar");

function myfunct() {
    if (
        point.classList.contains("hidden") &&
        balance.classList.contains("hidden") &&
        balance.classList.contains("hidden") &&
        gd_bar.classList.contains("hidden") &&
        !src_bar.classList.contains("hidden")
    ) {
        point.classList.remove("hidden");
        balance.classList.remove("hidden");
        withdraw.classList.remove("hidden");
        gd_bar.classList.remove("hidden");
        src_bar.classList.add("hidden");
    } else {
        point.classList.add("hidden");
        balance.classList.add("hidden");
        withdraw.classList.add("hidden");
        gd_bar.classList.add("hidden");
        src_bar.classList.remove("hidden");
    }
}