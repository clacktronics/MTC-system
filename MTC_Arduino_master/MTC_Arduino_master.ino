#include <DS1307RTC.h>
#include <TimeLib.h>
#include <Wire.h>
#include <stdio.h>
#include <LiquidCrystal.h>
  
int h, m, s, f, difference;

//pin / state variables
const byte ledPin = 13;
boolean ledState = false;
char toDisp[14*6];

int startPoint;

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

unsigned long last_time,last_time2;

void setup()
{
 pinMode(ledPin,OUTPUT);
 digitalWrite(ledPin,ledState);
 Serial.begin(9600);               // 31250 
 h = m = s = f = 0;
 lcd.begin(16, 2);
 lcd.setCursor(0, 0);

 setSyncProvider(RTC.get);
 startPoint = second();
 while(startPoint == second()){}
 difference = second();
 startPoint = second();
}

void loop()
{
  
  if(startPoint != second()) {

    if(f > 2) { 
        f = 0;
        }
    
    startPoint = second();
    }
    
 
  
  if((micros() - last_time) >= 10100) {
   

    GenMtc();
    last_time += 10000 ;
  
  
  }

}

void GenMtc()
{
 //Serial.println(millis() - last_time);
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

 // MIDI commands
 //Serial.write(0xF1);
 //Serial.write(toSend);
 sprintf(toDisp, "%02d:%02d:%02d.%02d", h, m, s, f);
 lcd.setCursor(0, 0);
 lcd.print(toDisp);


 
 if (++indice>7)
 {
   f+=2;
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
 
   indice=0;
 }
}


