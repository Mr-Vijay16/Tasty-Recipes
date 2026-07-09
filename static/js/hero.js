const cards=document.querySelectorAll(".hero-card");

cards.forEach((card,index)=>{

card.style.left=`${index*35}px`;

card.style.top=`${index*20}px`;

card.style.zIndex=cards.length-index;

});

let current=0;

setInterval(()=>{

const first=cards[current];

first.style.transform="translateX(-450px) rotate(-20deg)";

setTimeout(()=>{

document.querySelector(".hero-right").appendChild(first);

first.style.transform="";

const all=document.querySelectorAll(".hero-card");

all.forEach((card,index)=>{

card.style.left=`${index*35}px`;

card.style.top=`${index*20}px`;

card.style.zIndex=all.length-index;

});

},700);

current=(current+1)%cards.length;

},4000);