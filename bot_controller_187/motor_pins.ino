struct right_pins{
  byte front_pos = 14;
  byte front_gnd = 0;
  byte rear_pos  = 3;
  byte rear_gnd  = 15;
}right;
struct left_pins{
  byte front_pos = 4;
  byte front_gnd = 5 ;
  byte rear_pos  = 12;
  byte rear_gnd  = 13;  
}left;
void pin_setup(){
  pinMode(right.front_pos, OUTPUT);
  pinMode(right.front_gnd, OUTPUT);
  pinMode(right.rear_pos, OUTPUT);
  pinMode(right.rear_gnd, OUTPUT);
  pinMode(left.front_pos, OUTPUT);
  pinMode(left.front_gnd, OUTPUT);
  pinMode(left.rear_pos, OUTPUT);
  pinMode(left.rear_gnd, OUTPUT);
  pinMode(10, OUTPUT);      //later for servo motor
  digitalWrite(10 ,LOW);
}
void right_move(int value){
   digitalWrite(right.front_pos,value);
   digitalWrite(right.rear_pos,value);
   digitalWrite(right.front_gnd,0);
   digitalWrite(right.rear_gnd,0);
}
void left_move(int value){
   digitalWrite(left.front_pos,value);
   digitalWrite(left.rear_pos,value);
   digitalWrite(left.front_gnd,0);
   digitalWrite(left.rear_gnd,0);  
}
void left_turn(){
  right_move(0);
  left_move(0);
  Swap(&left.front_pos,&left.front_gnd);
  Swap(&left.rear_pos,&left.rear_gnd);
}
void right_turn(){
  left_move(0);
  right_move(0);
  Swap(&right.front_pos,&right.front_gnd);
  Swap(&right.rear_pos,&right.rear_gnd);
}
void return_back(){
  //Serial.println("begin swap");
  Swap(&right.front_pos,&left.front_gnd);
  Swap(&right.rear_pos,&left.rear_gnd);
  Swap(&left.front_pos,&right.front_gnd);
  Swap(&left.rear_pos,&right.rear_gnd);
}

void Swap(byte *a,byte *b){
  //Serial.println("swapped");
  byte temp = *a;
  *a = *b;
  *b = temp;
}
