#include <Adafruit_NeoPixel.h>
#include <stdio.h>
#include <stdlib.h>

const uint16_t strip_length = 5;
const uint16_t LEDperMeter = 30;
int pixelFormat = NEO_GRB + NEO_KHZ800; // pixel format, predefined format from library
const int numPixels = strip_length*LEDperMeter;
Adafruit_NeoPixel pixels(numPixels, 5, pixelFormat); //pixels = new Adafruit_NeoPixel(numPixels, pin, pixelFormat);
uint16_t *fire_state;
uint16_t left;
uint16_t right;
float spreadRate = 0.20;
int waitTime = 500;
int brightness = 255;
int init_index;
int roll;
String fire_sim;
unsigned long timer;
int mins;
int secs;
int mills;

void setup() {
  // put your setup code here, to run once:
  pixels.begin();
  randomSeed(analogRead(0));
  fire_state = new uint16_t[numPixels];
  for(int i=0; i<numPixels; i++)  fire_state[i]=0;
  init_index = random((uint16_t)floor(((double)numPixels)/3))+(numPixels/3);
  Serial.begin(9600);
  //Serial.println(init_index, DEC);
  fire_state[init_index] = brightness;
  left = init_index;
  right = init_index;
  pixels.clear();
  fire_sim.reserve(400);
  
}

void loop() {
  //update all LEDs
  
  for(int i=0; i<numPixels; i++) { // iterate n times
    pixels.setPixelColor(i, pixels.Color(fire_state[i], 0, 0)); // setPixelColor(LED number, pixels->Color(RED, GREEN, BLUE))
    pixels.show();   // send the updated pixel colors to the control board
  }

  //update left side
  if(left < numPixels){
    roll = random()%100;
    float val = (float)roll/100;
    //Serial.print("Left: ");
    //Serial.println(val);
    if(val < spreadRate){
      fire_state[++left] = brightness;
    }
  }
  //update right side
  if(right > 0){
    roll = random()%100;
    float val = (float)roll/100;
    if(val < spreadRate){
      fire_state[--right] = brightness;
    }
  }
  lightToSerial();
  delay(waitTime);
}

void lightToSerial(){
    for(int i = 0; i < 149; i ++){
     if(fire_state[i] == 0){
      fire_sim += "0,";
     }else{
      fire_sim +="1,";
       }
      }
      if(fire_state[149] == 0){
      fire_sim += "0";
     }else{
      fire_sim +="1";
       }
    fire_sim = "," + fire_sim;
    Serial.println(fire_sim);
    fire_sim = "";
    Serial.flush();
}
