// seneor 
int sample;
long int acc = 0;
double rms = 0;
int i;

// LED
int flag = 0;
int time0 = 0;
int time1 = 0;
int differ = 0;

// XBee
#include <XBee.h>
XBee xbee = XBee();
int j = 0;
struct Frame{ 
  unsigned long id = 0;
  float data[8];
  uint8_t ending[1] = {'\n'}; 
} frame; 

void setup() { 
  xbee.begin(57600);
  pinMode(13, OUTPUT);
}

void loop() {   
  // sensor part
  for(i=0;i<1096;i++){
    sample = analogRead(A7) - 512;
    acc = acc + sample * sample;
  }
  rms = sqrt(acc / 1096);
  acc = 0;
  
  // frame
  frame.data[j] = rms; 
  j = j + 1;
  
  // turn LED
  if (rms > 30){
    digitalWrite(13,HIGH);
    flag = 1;
    time0 = millis();
  }  
  time1 = millis();
  differ = time1 - time0;
  if (differ > 3000 && flag == 1){ 
    digitalWrite(13,LOW);
    flag = 0;
  }
  
  // XBee
  if(j==8){
    frame.id = frame.id + 1;
    uint8_t *payload; 
    payload = (uint8_t *)&frame;
    Tx16Request packet = Tx16Request(0x1111, payload, sizeof(frame));
    xbee.send(packet);    
    j = 0;  
  }
  
}
