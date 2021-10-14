#include <ESP8266WiFi.h>
#include <Arduino.h>
#include <ESP8266mDNS.h>
#include <WiFiUdp.h>
#include <ArduinoOTA.h>


const char *ssid = "heiro";
const char *pass = "i_am_the_worst_fellow_@";
char packetbuffer[20];

WiFiUDP udp;

void setup() {
   pin_setup();
//Serial.begin(115200);
  //pinMode(LED_BUILTIN,OUTPUT);
  //digitalWrite(LED_BUILTIN,LOW);

  //delay(1000);
  WiFi.begin(ssid,pass);
   while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting..");
  }
   
   analogWriteFreq(200);
  Serial.print("Connected to WiFi. IP:");
  Serial.println(WiFi.localIP());
 
  udp.begin(8888);
  
   ArduinoOTA.onStart([]() {
    String type;
    if (ArduinoOTA.getCommand() == U_FLASH) {
      type = "sketch";
    } else { // U_FS
      type = "filesystem";
    }

    // NOTE: if updating FS this would be the place to unmount FS using FS.end()
    Serial.println("Start updating " + type);
  });
  ArduinoOTA.onEnd([]() {
    Serial.println("\nEnd");
    /*
    for(int i=0;i<5;i++){
    digitalWrite(LED_BUILTIN,  HIGH);
    delay(500);
    digitalWrite(LED_BUILTIN,  LOW);
    }*/
  });
 
  ArduinoOTA.begin();

}
String msg;
int data = 0, angle =0;
char dir;
int temp= 0;
int turn_gain = 10;
int delay_gain=25;           // gain for delay time
int turn_time = 350;   // in ms  (470)
int count=0;
bool is_right = false, is_left = false;
int packetsize;
bool is_backward = false;
int timer = millis();
void loop() {
 ArduinoOTA.handle();
  packetsize = udp.parsePacket();
  if(packetsize){
    Serial.println(packetsize);
        int n = udp.read(packetbuffer , 9);
          packetbuffer[n] = 0;
          Serial.println(packetbuffer);
          
        dir = packetbuffer[0];
        data = strtol((const char *)&packetbuffer[1],NULL,10);
        timer = millis();

        //delay(5000);
        //data = client.read();
        //msg = client.readStringUntil('\n');
        //Serial.println(msg);
    }

      switch(dir){
        case 'c':   
                left_move(75);  
                right_move(75);
                //client.clear_received();
                //delay(1000);
                //is_right = false;
                //is_left = false;
               //client.clear_received();
                //dir = '\0'; 
                break;
        case 'r':
                if(bool(data <0) != is_backward){                // if( xor(data<0,is_backward))
                  left_turn();
                  right_move(100);
                  left_move(100);
                  delay(map(fabs(data),0,90,0,turn_time));  
                  left_turn();                  
                }
                else{          
                  right_turn();
                  left_move(100);
                 right_move(100);
                 delay(map(fabs(data),0,90,0,turn_time));
                 right_turn();               
                }
                right_move(0);
                 left_move(0);
                 delay(100);
                udp.clear_rx_buf();
                dir = 'h';
                break;
        case 'l':
                  if(bool(data < 0) != is_backward){             // if( xor(data<0,is_backward))
                    right_turn();
                    left_move(100);
                 right_move(100);              
                 delay(map(fabs(data),0,90,0,turn_time));
                 right_turn();                             
                  }
                  else{    
                  left_turn();
                  right_move(100);
                  left_move(100);
                  delay(map(fabs(data),0,90,0,turn_time)); 
                  left_turn();                             
                  }
                 dir='h';
                 right_move(0);
                 left_move(0);
                 delay(100);
                 udp.clear_rx_buf();
                 break;
        case 'e':
                 //delay(100);
                 left_turn();
                 right_move(100);
                 left_move(100);
                 delay(turn_time+100);  
                 left_turn();
                 delay(1000);
                 udp.clear_rx_buf();
                 dir = '\0';
                 break;
        case 'i':
                 //delay(100);
                 right_turn();
                  left_move(100);
                 right_move(100);
                 delay(turn_time+100);
                 right_turn();
                 delay(1000);
                 udp.clear_rx_buf();
                 dir = '\0';
                 break; 
        case 's':
                 right_move(0);
                 left_move(0);
                 return_back();
                 is_backward = true;
                 analogWrite(10,77);
                 delay(500);
                 analogWrite(10,26);
                 delay(500);
                 digitalWrite(10,LOW);
                 delay(1000);
                 udp.clear_rx_buf();
                 dir = '\0';
                 break;
        case 'h':
                right_move(0);
                left_move(0);
                break;
        default:
                right_move(0);
                left_move(0);

      }
      //delay(1000);
      if(millis() - timer > 2500){
        dir = 'h';
        if(is_backward)
          return_back();
        is_backward = false;
      }
}
    
    
   
 
