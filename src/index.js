import "./styles.css";

document.getElementById("app").innerHTML = `
<h1>Hello Vanilla!</h1>
<div>
  We use the same configuration as Parcel to bundle this sandbox, you can find more
  info about Parcel 
  <a href="https://parceljs.org" target="_blank" rel="noopener noreferrer">here</a>.
</div>
`;
import "./styles.css";

const canvas = document.querySelector("#draw-area ");
const context = canvas.getContext("2d");
// ーーーーーーーーーーーーーーーーーー赤色ーーーーーーーーーーーーーーーーーーー
const inputElem = document.getElementById('Red'); // input要
const currentValueRed = document.getElementById('current-red'); // 埋め込む先のspan要素
console.log(inputElem.value);
inputElem.addEventListener("input", function() {
  currentValueRed.innerHTML = 'Red' + inputElem.value;
}, false); 
// ーーーーーーーーーーーーーーーーーー赤色ーーーーーーーーーーーーーーーーーーー
// ーーーーーーーーーーーーーーーーーー緑色ーーーーーーーーーーーーーーーーーーー
const inputElemGreen = document.getElementById('Green'); // input要
const currentValueGreen = document.getElementById('current-Green'); // 埋め込む先のspan要素
console.log(inputElemGreen.value);
inputElemGreen.addEventListener("input", function() {
  currentValueGreen.innerHTML = 'Green' + inputElemGreen.value;
}, false); 
// ーーーーーーーーーーーーーーーーーー緑色ーーーーーーーーーーーーーーーーーーー
// ーーーーーーーーーーーーーーーーーー緑色ーーーーーーーーーーーーーーーーーーー
const inputElemBlue = document.getElementById('Blue'); // input要
const currentValueBlue = document.getElementById('current-Blue'); // 埋め込む先のspan要素
console.log(inputElemBlue.value);
inputElemBlue.addEventListener("input", function() {
  currentValueBlue.innerHTML = 'Blue' + inputElemBlue.value;
}, false); 
// ーーーーーーーーーーーーーーーーーー緑色ーーーーーーーーーーーーーーーーーーー

// 現在の値をspanに埋め込む関数
const setCurrentValue = (val) => {
  currentValueRed.innerText = val;
}
// inputイベント時に値をセットする関数
const rangeOnChange = (e) =>{
  setCurrentValue(e.target.value);
}
window.onload = () => {
  inputElem.addEventListener('input', rangeOnChange); // スライダー変化時にイベントを発火
  setCurrentValue(inputElem.value); // ページ読み込み時に値をセット
}


canvas.addEventListener("mousemove", event => {
  draw(event.layerX, event.layerY);
});
canvas.addEventListener("touchmove", event => {
  draw(event.layerX, event.layerY);
});

canvas.addEventListener("mousedown", () => {
  context.beginPath();
  isDrag = true;
});
canvas.addEventListener("mouseup", () => {
  context.closePath();
  isDrag = false;
});
canvas.addEventListener("touchstart", () => {
  context.beginPath();
  isDrag = true;
});
canvas.addEventListener("touchend", () => {
  context.closePath();
  isDrag = false;
});
const clearButton = document.querySelector("#clear-button");
clearButton.addEventListener("click", () => {
  context.clearRect(0, 0, canvas.width, canvas.height);
});

let isDrag = false;
function draw(x, y) {
  if (!isDrag) {
    return;
  }
  context.lineWidth = 5;
  context.strokeStyle = 'rgb(' + inputElem.value + ',' + inputElemGreen.value + ',' + inputElemGreen.value + ')';
  context.lineTo(x, y);
  context.stroke();
}
console.log(inputElem.value);
