// Constructor
class Half_Circle {
  constructor(x, y) {

    // Define a body
    let bd = new box2d.b2BodyDef();
    bd.type = box2d.b2BodyType.b2_dynamicBody;
    bd.position = scaleToWorld(x, y);

    // Define a fixture
    let fd = new box2d.b2FixtureDef();

    let vertices = [];
    let num = 10;
    let pi_num = [];
    let R = 25;
    // for (let i = num; i >= 0; i--) {
    //     if(i == 0)
    //     {
    //       vertices[i] = scaleToWorld(R*cos(0), -R*sin(0));
    //     }
    //     else
    //     {
    //       vertices[i] = scaleToWorld(R*cos(Math.PI/i), -R*sin(Math.PI/i));
    //     }
    //     if(i == 1)
    //     {
    //       vertices[i] = scaleToWorld(R*cos(Math.PI), -R*sin(Math.PI));
    //     }
    //   }
    
    // for (let i = 0; i < num; i++) {
    //   pi_num[i] = (i/num)*Math.PI;
    //   vertices[i] = scaleToWorld(R*cos(pi_num[i]), R*sin(pi_num[i]));
    // }
    
    vertices[5] = scaleToWorld(R*cos(0), -R*sin(0));
    vertices[4] = scaleToWorld(R*cos(Math.PI/4), -R*sin(Math.PI/4));
    vertices[3] = scaleToWorld(R*cos(Math.PI/2), -R*sin(Math.PI/2));
    vertices[2] = scaleToWorld(R*cos(Math.PI*0.7), -R*sin(Math.PI*0.7));
    vertices[1] = scaleToWorld(R*cos(Math.PI*0.8), -R*sin(Math.PI*0.8));
    vertices[0] = scaleToWorld(R*cos(Math.PI), -R*sin(Math.PI));
    
    // Fixture holds shape
    fd.shape = new box2d.b2PolygonShape();
    fd.shape.SetAsArray(vertices, vertices.length);
    //println(fd.shape);

    //fd.shape.SetAsBox(scaleToWorld(10),scaleToWorld(10));

    // Some physics
    fd.density = 1.0;
    fd.friction = 500.0;
    fd.restitution = 0.02;

    // Create the body
    this.body = world.CreateBody(bd);
    // Attach the fixture
    this.body.CreateFixture(fd);

    // Some additional stuff
    //this.body.SetLinearVelocity(new Vec2(random(-5, 5), random(2, 5)));
    //this.body.SetAngularVelocity(random(-5,5));
  }

  // This function removes the particle from the box2d world
  killBody() {
    world.DestroyBody(this.body);
  }

  // Is the particle ready for deletion?
  done() {
    // Let's find the screen position of the particle
    let pos = scaleToPixels(this.body.GetPosition());
    // Is it off the bottom of the screen?
    if (pos.y > height + this.w * this.h) {
      this.killBody();
      return true;
    }
    return false;
  }

  // Drawing the box
  display() {
    // Get the body's position
    let pos = scaleToPixels(this.body.GetPosition());
    // Get its angle of rotation
    let a = this.body.GetAngleRadians();

    // Draw it!
    let f = this.body.GetFixtureList();
    let ps = f.GetShape();

    rectMode(CENTER);
    push();
    translate(pos.x, pos.y);
    //println(pos.x + " " + pos.y);
    rotate(a);
    fill(127);
    stroke(200);
    strokeWeight(2);
    // ellipse(0, 0, 20, 20);
    beginShape();
    // For every vertex, convert to pixel vector
    for (let i = 0; i < ps.m_count; i++) {
      let v = scaleToPixels(ps.m_vertices[i]);
      vertex(v.x, v.y);
    }
    endShape(CLOSE);
    pop();
  }
  output_pos(num)
  {
    let pos = scaleToPixels(this.body.GetPosition());
    fill(200, 200, 255)
    text(pos.x.toFixed(2).toString(),200,20+20*num)
    text(pos.y.toFixed(2).toString(),250,20+20*num)
    // console.log(pos.y);
  }
  pos_data()
  {
    let pos = scaleToPixels(this.body.GetPosition());
    return pos;
  }
}