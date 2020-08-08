// The Nature of Code
// Daniel Shiffman
// http://natureofcode.com


// A reference to our box2d world
let world;

// 地面
let boundaries = [];
// 全ての図形
let boxes = [];// 四角形
let polygons = [];// 三角形
let half_circle = [];// 半円
let bars = [];// 図形の間に挟む板
let long = [];// 円柱
let sim = [];//シミュレーション用の図形を入れるための配列

// 全ての図形を一度格納するための配列
let boxes_num = [];// 四角形
let polygons_num = [];// 三角形
let half_circle_num = [];// 半円
let bars_num = [];// 図形の間に挟む板
let long_num = [];// 円柱

let bound_h = 10;
//default data
let get_data = false;//Pythonからのデータ取得フラグ
let key_data = NaN;//Key取得時に一旦格納するため
let data_key = [];//最新の積み木の番号格納
let new_data_pos = 0;//最新の積み木の位置格納
let x_now = [];//シミュレートする際に必要なxの範囲
let x_now_min = 0;
let x_now_max = 0;
let y_now = [];//シミュレートする際に必要な図形全体のxに対応する高さ
let y_now_min = 0;
let y_now_max = 0;
let all_pos = [];//一旦現在のすべての図形の位置を格納する

//積み木のお推定
let estimation_x = [];
let advance_x = [];
let estimation_y = [];
let advance_y = [];
let diff = NaN;
let estimation_flag = 0;
let sim_aim = 0;
let sim_step = 0;
let sim_start = 0;
//マイステップごとのシムレーション完了フラグ
let diff_flag = false;
//事前に配列に格納
let clone_boxes = [];
let clone_polygons = [];
let clone_half_circle = [];
let clone_bars = [];
let clone_long = [];
let count = 0;
let pre_simpos = 0;


//---------------------------------------setup---------------------------------------------
function setup() {
  createCanvas(1280, 640);
  // cnv.mousePressed(make_boxes); // attach listener for

  // Initialize box2d physics and create the world
  world = createWorld();

  // Add a bunch of fixed boundaries
  let bound_w = width;
  
  let real_h = height - bound_h;
  let box_step = real_h - 50 / 2;
  boundaries.push(new Boundary(width / 2, height - bound_h / 2, width, bound_h));

}
//---------------------------------------setup---------------------------------------------

//---------------------------------------draw---------------------------------------------
function draw() {
  background(0);

  // We must always step through time!
  let timeStep = 1.0 / 30;
  // 2nd and 3rd arguments are velocity and position iterations
  world.Step(timeStep, 10, 10);

  display_boundary();

  
  if(estimation_flag % 2 == 0){
    erase_shape();
    make_shape();
    SaveData();
    fill(0,255,0, 40);
    let x_range = abs(x_now_max - x_now_min);
    let y_range = abs(height - bound_h -y_now_min);
    rectMode(CORNER);
    rect(x_now_min, y_now_min, x_range, y_range);
    text('minx', x_now_min, y_now_min);
    noStroke();
    fill(0, 255, 255, 40);
    for(let i = 0; i < estimation_x.length; i++){
    rect(estimation_x[i]-25, estimation_y[i]-25, 50, 50);
    console.log(estimation_y.length);
  }

  }
  


  if(get_data){
    rectMode(CORNER);

      //初期化
    x_now = [];
    y_now = [];
    // advance_x = [];
    // advance_y = [];
    
    
    //配列のクローン作成
    clone_boxes = Array.from(boxes);
    clone_polygons = Array.from(polygons);
    clone_half_circle = Array.from(half_circle);
    clone_bars = Array.from(bars);
    clone_long = Array.from(long);
    console.log('clone_length----------------',clone_boxes.length);
    diff_flag = true;
    count = 0;
    
    
    // background(0,0,255, 100);
    estimation_x = [];
    estimation_y = [];
    estimation_flag += 1;
    //整地
    
    //------------------図形のx, y の最大最小を求めるための配列まとめと最大最小値取得---------------------
  
    for(let i = 0; i < width; i++){
      advance_x[i] = i;
      advance_y[i] = height - bound_h;
    }
    console.log('advance_y.length------------', advance_y.length);
    console.log('advance_x.length------------', advance_x[width/2]);
  
    clone_boxes_num = JSON.parse(JSON.stringify(boxes_num)); 
    clone_polygons_num = JSON.parse(JSON.stringify(polygons_num)); 
    clone_half_circle_num = JSON.parse(JSON.stringify(half_circle_num)); 
    clone_bars_num = JSON.parse(JSON.stringify(bars_num)); 
    clone_long_num= JSON.parse(JSON.stringify(long_num)); 

    clone_boxes_num.forEach(function(value) {
      //図形のx,yの最大値を取得するための計算用の配列作成
      x_now.push(value.x);
      y_now.push(value.y - 50);
      //図形のx,yの範囲をアップデートするため
      for(let i = Math.round(value.x)-50; i <= Math.round(value.x) + 50; i++){
        if(advance_y[i] > value.y - 50){
          advance_y[i] = value.y - 50;
        }
      }
    });
    clone_polygons_num.forEach(function(value) {
        x_now.push(value.x);
        y_now.push(value.y - 50);
        for(let i = Math.round(value.x) -50; i <= Math.round(value.x) + 50; i++){
          if(advance_y[i] > value.y - 50){
            advance_y[i] = value.y - 50;
          }
        }
    });
    clone_half_circle_num.forEach(function(value) {
        x_now.push(value.x);
        y_now.push(value.y - 50);
        for(let i = Math.round(value.x) -50; i <= Math.round(value.x) + 50; i++){
          if(advance_y[i] > value.y - 50){
            advance_y[i] = value.y - 50;
          }
        }
    });
    clone_bars_num.forEach(function(value) {
        x_now.push(value.x);
        y_now.push(value.y - 20);
        for(let i = Math.round(value.x) -150; i <= Math.round(value.x) + 150; i++){
          if(advance_y[i] > value.y - 20){
            advance_y[i] = value.y - 20;
          }
        }
    });
    clone_long_num.forEach(function(value) {
        x_now.push(value.x);
        y_now.push(value.y - 100);
        for(let i = Math.round(value.x) -50; i <= Math.round(value.x) + 50; i++){
          if(advance_y[i] > value.y - 100){
            advance_y[i] = value.y - 100;
          }
        }
    });
    console.log('advance_y[width/2]---------', advance_y[width/2]);
    // clone_advance_x = JSON.parse(JSON.stringify(advance_x)); 
    // clone_advance_y = JSON.parse(JSON.stringify(advance_y)); 
  
  
    // 全ての図形のxをまとめた配列から最大値最小値を取得
    x_now_max = Math.max.apply(null, x_now); // => 5
    x_now_min = Math.min.apply(null, x_now); // => 5
    y_now_max = Math.max.apply(null, y_now); // => 1
    y_now_min = Math.min.apply(null, y_now); // => 1
    console.log('max_x', x_now_max);
    console.log('min_x', x_now_min);
    console.log('max_y', y_now_max);
    console.log('max_y', y_now_min);
    for (let i = 0; i < x_now.length; i++) {
      console,log('y->', y_now[i]);
    }
  
    console.log('advance_y.length------------', advance_y.length);
    console.log('advance_x.length------------', advance_x[width/2]);
  

    sim_start = Math.round(x_now_min);
    sim_step = sim_start;
    console.log('Save Current position');
    console.log('sim_step--------------------', sim_step);
    console.log('x_now--------------------', x_now.length);



    // relocation();
    sim = [];
    let new_Box = new Box(advance_x[sim_step], advance_y[sim_step]);
    sim.push(new_Box);
    diff = 0;
    console.log('advance_x----------------', advance_x.length);
    // console.log('advance_x----------------', advance_x1[sim_step]);
  }

  
  if(estimation_flag % 2 == 1){
    console.log('Now simurate');
    
    //シミュレーションの範囲を超えたらシミュレート終了
    if(sim_step > x_now_max){
      estimation_flag += 1;
      console.log('end simurasion');
    }
    
    if(diff_flag){
      sim_step += 3;
      console.log('Update Step');
      console.log('sim_step--------------------', sim_step);
      count = 0;
      //整地
      erase_shape();
      // relocation();
      FixedLocation();
      
      sim = [];
      let new_Box = new Box(advance_x[sim_step], advance_y[sim_step]);
      sim.push(new_Box);
      diff = 0;
    }

    
    console.log('advance_x----------------', advance_x[sim_step]);
    
    for (let i = sim.length - 1; i >= 0; i--) {
      sim_aim = sim[i].pos_data();
      text(sim_aim.x.toFixed(2).toString(), 500, 500); 
      text(sim_aim.y.toFixed(2).toString(), 600, 500);
      console.log('sim_aim-----------', sim_aim.y.toFixed(2).toString());
    }
    
    diff = abs(sim_aim.y.toFixed(2) - advance_y[sim_step]);
    diff_flag = false;
    print('diff-------------', diff);

    
    
    
    count += 1;
    // let speed = abs(sim_aim.y.toFixed(2) - pre_simpos);
    // pre_simpos = sim_aim.y.toFixed(2);
    // if(speed < 0.01){
    //   diff_flag = true;
    //   estimation_x.push(advance_x[sim_step]);
    //   estimation_y.push(advance_y[sim_step]);
    //   print('安定')
    // }



    if(diff >= 30){
      print('不安定');
      fill(255,0,0);   
      diff_flag = true;
      }
    if(count > 10 && diff < 3 ){
      diff_flag = true;
      estimation_x.push(advance_x[sim_step]);
      estimation_y.push(advance_y[sim_step]);
      print('安定')
    }
    if(count > 40){
      diff_flag = true;
      estimation_x.push(advance_x[sim_step]);
      estimation_y.push(advance_y[sim_step]);
      print('安定')
    }
    console.log(advance_x[sim_step]);
    
  }

  
  display_shape();
  get_data = false;
}
//---------------------------------------draw---------------------------------------------



//----------------------------- make new shape-----------------------------
//ここで新しいデータが入力されたことを示すフラグも作成
//このフラグは、Python側からデータを受け取ったという確認をするためのフラグを想定しています。
function make_shape(){
  key_data = key;
  get_data = false;
  if( key_data == '3' && keyIsPressed == true){
    let new_Customshape = new CustomShape(mouseX, mouseY);
    polygons.push(new_Customshape);
    console.log('make Customshape');
  }
  if( key_data == '4' && keyIsPressed == true){
    let new_Box = new Box(mouseX, mouseY);
    boxes.push(new_Box);
    console.log('make box');
  }
  if( key_data == '5' && keyIsPressed == true){
    let new_long = new LongBox(mouseX, mouseY);
    long.push(new_long);
    console.log('make longbox');
  }
  if( key_data == '0' && keyIsPressed == true){
    let new_bar = new Bar(mouseX, mouseY);
    bars.push(new_bar); 
    console.log('make bar');
  }
  if( key_data == '9' && keyIsPressed == true){
    let new_half = new Half_Circle(mouseX, mouseY);
    half_circle.push(new_half);
    console.log('make halfcircle');
  }
  if( key_data == '1' && keyIsPressed == true){
    get_data = true;
    console.log('get_data = true');
  }
  keyIsPressed = false;
}

//----------------------------- Display all the boundaries-----------------------------
function display_boundary(){
  for (let i = 0; i < boundaries.length; i++) {
    boundaries[i].display();
  }
}

//----------------------------- Display all the boxes-----------------------------
function display_shape(){
  for (let i = boxes.length - 1; i >= 0; i--) {
    boxes[i].display();
    if (boxes[i].done()) {
      boxes.splice(i, 1);
    }
  }

  //polygone
  for (let i = polygons.length - 1; i >= 0; i--) {
    polygons[i].display();
    if (polygons[i].done()) {
      polygons.splice(i, 1);
    }
  }
  
  //half_circle
  for (let i = half_circle.length - 1; i >= 0; i--) {
    half_circle[i].display();
    if (half_circle[i].done()) {
      half_circle.splice(i, 1);
    }
  }
  //bar
  for (let i = bars.length - 1; i >= 0; i--) {
    bars[i].display();
    if (bars[i].done()) {
      bars.splice(i, 1);
    }
  }
  //long
  for (let i = long.length - 1; i >= 0; i--) {
    long[i].display();
    if (long[i].done()) {
      long.splice(i, 1);
    }
  }
  //sim
  for (let i = sim.length - 1; i >= 0; i--) {
    sim[i].display();
    if (sim[i].done()) {
      sim.splice(i, 1);
    }
  }
}

//---------------------最新の図形を配列に格納--------------------

function SaveData(){
  text('box', width - 100, 50);
  for (let i = boxes.length - 1; i >= 0; i--) {
    boxes_num[i] = boxes[i].pos_data();
    text(boxes_num[i].x.toFixed(2).toString(), width - 100, 100 + 10*i); 
    text(boxes_num[i].y.toFixed(2).toString(), width - 100+50, 100 + 10*i); 
  }
  //polygone

  text('triangle', width - 200, 50);
  for (let i = polygons.length - 1; i >= 0; i--) {
    polygons_num[i] = polygons[i].pos_data();
    text(polygons_num[i].x.toFixed(2).toString(), width - 200, 100 + 10*i);
    text(polygons_num[i].y.toFixed(2).toString(), width - 200+50, 100 + 10*i);
  }
  //half_circle
  text('half_circle', width - 300, 50);
  for (let i = half_circle.length - 1; i >= 0; i--) {
    half_circle_num[i] = half_circle[i].pos_data();
    text(half_circle_num[i].x.toFixed(2).toString(), width - 300, 100 + 10*i);
    text(half_circle_num[i].y.toFixed(2).toString(), width - 300+50, 100 + 10*i);
  }
  //bar
  text('bar', width - 400, 50);
  for (let i = bars.length - 1; i >= 0; i--) {
    bars_num[i] = bars[i].pos_data();
    text(bars_num[i].x.toFixed(2).toString(), width - 400, 100 + 10*i);
    text(bars_num[i].y.toFixed(2).toString(), width - 400+50, 100 + 10*i);
  }
  //long
  text('long', width - 500, 50);
  for (let i = long.length - 1; i >= 0; i--) {
    long_num[i] = long[i].pos_data();
    text(long_num[i].x.toFixed(2).toString(), width - 500, 100 + 10*i);
    text(long_num[i].y.toFixed(2).toString(), width - 500+50, 100 + 10*i);
  }
}


//存在している図形を全て削除
function erase_shape(){

  // for (let i = boxes.length - 1; i >= 0; i--) {
  //   boxes[i].killBody();
  //   boxes.pop(i);
  // }

  // //polygone
  // for (let i = polygons.length - 1; i >= 0; i--) {
  //   polygons[i].killBody();
  //   polygons.pop(i);
  // }
  
  // //half_circle
  // for (let i = half_circle.length - 1; i >= 0; i--) {
  //   half_circle[i].killBody();
  //   half_circle.pop(i);
  // }
  // //bar
  // for (let i = bars.length - 1; i >= 0; i--) {
  //   bars[i].killBody();
  //   bars.pop(i);
  // }
  // //long
  // for (let i = long.length - 1; i >= 0; i--) {
  //   long[i].killBody();
  //   long.pop(i);
  // }
  //sim
  for (let i = sim.length - 1; i >= 0; i--) {
    sim[i].killBody();
    sim.pop(i);
  }
}

//一時保存した配列データをもとに再配置
function relocation(){
  // boxes.splice();
  for (let i = clone_boxes.length - 1; i >= 0; i--) {
    boxes[0].killBody();
    boxes.pop();
    let new_Box = new Box(clone_boxes[i].x, clone_boxes[i].y);
    boxes.push(new_Box);
  }

  //polygone
  // polygons.splice();
  for (let i = clone_polygons.length - 1; i >= 0; i--) {
    polygons[0].killBody();
    polygons.pop();
    let new_Customshape = new CustomShape(clone_polygons[i].x, clone_polygons[i].y);
    polygons.push(new_Customshape);
  }
  
  //half_circle
  // half_circle.splice();
  for (let i = clone_half_circle.length - 1; i >= 0; i--) {
    half_circle[0].killBody();
    half_circle.pop();
    let new_half = new Half_Circle(clone_half_circle[i].x, clone_half_circle[i].y);
    half_circle.push(new_half);
  }

  //bar
  // bars.splice();
  for (let i = clone_bars.length.length - 1; i >= 0; i--) {
    bars[0].killBody();
    bars.pop();
    let new_bar = new Bar(clone_bars[i].x, clone_bars[i].y);
    bars.push(new_bar); 
  }
  
  //long
  // long.splice();
  for (let i = clone_long.length - 1; i >= 0; i--) {
    long[0].killBody();
    long.pop();
    let new_long = new LongBox(clone_long[i].x, clone_long[i].y);
    long.push(new_long);
  }
}
function FixedLocation(){

  text('box', width - 100, 50);
  for (let i = boxes.length - 1; i >= 0; i--) {
  boxes[i].pos_data().x = clone_boxes[i].x;
  boxes[i].pos_data().y = clone_boxes[i].y;
  }
  //polygone

  text('triangle', width - 200, 50);
  for (let i = polygons.length - 1; i >= 0; i--) {
    polygons[i].pos_data().x = clone_polygons[i].x;
    polygons[i].pos_data().y = clone_polygons[i].y;
  }
  //half_circle
  text('half_circle', width - 300, 50);
  for (let i = half_circle.length - 1; i >= 0; i--) {
    half_circle[i].pos_data().x = clone_half_circle[i].x;
    half_circle[i].pos_data().y = clone_half_circle[i].y;
  }
  //bar
  text('bar', width - 400, 50);
  for (let i = bars.length - 1; i >= 0; i--) {
    bars[i].pos_data().x = clone_bars[i].x;
    bars[i].pos_data().y = clone_bars[i].y;
  }
  //long
  text('long', width - 500, 50);
  for (let i = long.length - 1; i >= 0; i--) {
    long[i].pos_data().x = clone_long[i].x;
    long[i].pos_data().y = clone_long[i].y;
  }
}