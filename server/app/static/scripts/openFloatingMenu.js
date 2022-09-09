let flowing_menu = document.querySelector(".flowing-container");
let flowing_content = document.querySelector(".flowing-container-content");
let floating_p = document.querySelector("#admin-heading");


function openMenu() {
  flowing_menu.style.width = "400px";
  flowing_content.style.width = "320px";
  document.querySelector(".flowing-container").style.boxShadow = "10px 5px 30px #8d8d8d";
}

function closeMenu() {
  flowing_menu.style.width = "80px";
  flowing_content.style.width = "180px";
  document.querySelector(".flowing-container").style.boxShadow = "none";
}
