#include <LiquidCrystal.h>
#include <stdio.h>
#include <TimedAction.h>
#include "markers.h"

LiquidCrystal lcd(12, 11, 5, 4, 6, 7);

byte h, m, s, f;

//this initializes a TimedAction class that will send MTC quarter frame every 10 milliseconds so 80 milliseconde for
// an 'entire' timecode.



//pin / state variables
const byte ledPin = 13;
boolean ledState = false;
boolean pause = false;
boolean last = true;
boolean printpoint = true;
boolean pause_sequence = true;
char toDisp[14*6];      // 6 lines of 14 characters.
int marker_point = 0;
unsigned long pause_bounce = millis();

void setup()
{
 lcd.begin(84,48);
 pinMode(ledPin,OUTPUT);
 digitalWrite(ledPin,ledState);
 Serial.begin(31250);               // 31250 use of TX3/RX3 of Arduino Mega
 h = m = s = f = 0;
 lcd.begin(16,2);

 for(int i=2; i<4; i++)
 {
  pinMode(i, INPUT);
  digitalWrite(i, HIGH);
 }
// pause button
   pinMode(8, INPUT);
  digitalWrite(8, HIGH);

  lcd.setCursor(12,0);
  lcd.print("M:");
  lcd.setCursor(14,0);
  lcd.print(marker_point);

  attachInterrupt(digitalPinToInterrupt(2), next_marker, FALLING);
  attachInterrupt(digitalPinToInterrupt(3), last_marker, FALLING);

 
}

TimedAction timedAction = TimedAction(10,GenMtc);

void next_marker() 
{
  static unsigned long last_interrupt_time1 = 0;
  unsigned long interrupt_time1 = millis();
  if (interrupt_time1 - last_interrupt_time1 > 200)
   {
      marker_point+=1;
      if(marker_point > 10){marker_point=10;}
      printpoint = true;
      
   }
 last_interrupt_time1 = interrupt_time1;
}

void last_marker() 
{
    static unsigned long last_interrupt_time2 = 0;
  unsigned long interrupt_time2 = millis();
  if (interrupt_time2 - last_interrupt_time2 > 200)
   {
    
      marker_point-=1;
      if(marker_point < 0){marker_point=0;}
      printpoint = true;
   }
   last_interrupt_time2 = interrupt_time2;
}


void loop()
{

  
if(!digitalRead(8) && pause_bounce < millis()){ 
  
  if(pause_sequence ){pause_sequence = false;}
  else{pause_sequence = true;}

  pause_bounce = millis() + 500;
  
  }

  
 timedAction.check(); 
 if(printpoint)
 {
  h = markers[marker_point][0];
  m = markers[marker_point][1];
  s = markers[marker_point][2];
  f = markers[marker_point][3];
  lcd.setCursor(15,0);
  lcd.print(" "); 
  lcd.setCursor(14,0);
  lcd.print(marker_point); 
  printpoint = false;
  pause_sequence = true;
 }
 
}

void GenMtc()
{
 static byte indice=0;
 static byte toSend;

 switch(indice)
 {
 case 0:
   toSend = ( 0x00 + (f & 0xF));        
   break;

 case 1:
   toSend = ( 0x10 + ((f & 0xF0)/16));  
   break;

 case 2:
   toSend = ( 0x20 + (s & 0xF));        
   break;

 case 3:
   toSend = ( 0x30 + ((s & 0xF0)/16));  
   break;

 case 4:
   toSend = ( 0x40 + (m & 0xF));        
   break;

 case 5:
   toSend = ( 0x50 + ((m & 0xF0)/16));  
   break;

 case 6:
   toSend = ( 0x60 + (h & 0xF));        
   break;

 case 7:
   toSend = ( 0x72 + ((h & 0xF0)/16));   // 0x70 = 24 fps // 0x72 = 25 fps // 0x74 = 30df fps // 0x76 = 30 fps
   break;
 }
 
 Serial.write(0xF1);
 Serial.write(toSend);
 
 
 if (++indice>7)
 {
   if(!pause_sequence){f+=2;}
   if (f>24)    // I'm French, so from standard is 25 frames/second
   {
     s++;
     f-=25;
   }
   if (s>59)
   {
     m++;
     s-=60;
   }
   if (m>59)
   {
     h++;
     m-=60;
   }
   ledState = ledState ? false:true;
   digitalWrite(ledPin,ledState);
   sprintf(toDisp, "%02d:%02d:%02d.%02d", h, m, s, f);
   lcd.setCursor(0,0);
   lcd.print(toDisp);
   //Serial.println(toDisp);
 
   indice=0;
 }
}

