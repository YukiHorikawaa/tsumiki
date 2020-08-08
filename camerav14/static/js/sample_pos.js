
let all_pos = [];
let advance_x = [];
let advance_y = [];
let x_now = [];//シミュレートする際に必要なxの範囲
let x_now_min = 0;
let x_now_max = 0;
let y_now = [];//シミュレートする際に必要な図形全体のxに対応する高さ
let y_now_min = 0;
let y_now_max = 0;

function setup() {
  createCanvas(400, 400);
  let vec1 = createVector(100, 100);
  let vec2 = createVector(100, 200);
  let vec3 = createVector(100, 300);
  let vec4 = createVector(100, 400);
  let vec5 = createVector(100, 500);
  let vec6 = createVector(100, 600);
  let vec7 = createVector(100, 700);

  let boxes_num = [vec1, vec2]; // 四角形
  let polygons_num = [vec3]; // 三角形
  let half_circle_num = [vec4]; // 半円
  let bars_num = [vec5] // 図形の間に挟む板
  let long_num = [vec6, vec7] // 円柱
  let data_key = ['boxes_num', 'polygons_num', 'half_circle_num', 'bars_num', 'long_num']; //最新の積み木の全種類格納
  
  //全種類の全てのvecを一つの配列にまとめたい
  //全種類の中から一つづつshapeを参照
  boxes_num.forEach(function(value) {
    //図形のx,yの最大値を取得するための計算用の配列作成
    x_now.push(value.x);
    y_now.push(value.y - 50);
    console.log(parseInt(value.x, 10));
    //図形のx,yの範囲をアップデートするため
    for(let i = Math.round(value.x)-25; i <= Math.round(value.x) + 25; i++){
      if(advance_y[i] < value.y - 50){
        advance_y[i] = value.y - 50;
      }
    }
  });
    polygons_num.forEach(function(value) {
      x_now.push(value.x);
      y_now.push(value.y - 50);
      for(let i = Math.round(value.x) -25; i <= Math.round(value.x) + 25; i++){
        if(advance_y[i] < value.y - 50){
          advance_y[i] = value.y - 50;
        }
      }
  });
    half_circle_num.forEach(function(value) {
      x_now.push(value.x);
      y_now.push(value.y - 50);
      for(let i = Math.round(value.x) -25; i <= Math.round(value.x) + 25; i++){
        if(advance_y[i] < value.y - 50){
          advance_y[i] = value.y - 50;
        }
      }
  });
    bars_num.forEach(function(value) {
      x_now.push(value.x);
      y_now.push(value.y - 20);
      for(let i = Math.round(value.x) -100; i <= Math.round(value.x) + 100; i++){
        if(advance_y[i] < value.y - 20){
          advance_y[i] = value.y - 20;
        }
      }
  });
    long_num.forEach(function(value) {
      x_now.push(value.x);
      y_now.push(value.y - 100);
      for(let i = Math.round(value.x) -25; i <= Math.round(value.x) + 25; i++){
        if(advance_y[i] < value.y - 50){
          advance_y[i] = value.y - 50;
        }
      }
  });
}

function draw() {
  background(220);
}