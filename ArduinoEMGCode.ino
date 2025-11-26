#include <SPI.h>
#include <SD.h>
#include <LiquidCrystal.h>
String stringa;
const unsigned long Timeout = 10; //10 ms timeout bc yes
String stringa1;
String stringa2;

File myFile;
float signal =0;
void setup() {
  lcd.begin(16,2)
  Serial.begin(9600);
  while (!Serial){
    ;
  }
  Serial.print("Arduino is getting ready .....");
  if (!SD.begin(4)){
    Serial.print("failed to start serial output");
    while(1);
  }
  Serial.print("Arduino is ready to receive EMG Signal!")
  myFile = SD.open('text.txt', FILE_WRITE); // create new file to write serial output into SD
  if (myFile){
    Serial.print("writing to SD card...");
    signal = Serial.read();
    myFile.println(signal)
  }
}

void loop(){
  stringa = "";
  unsigned long T = 0; // timer
  T = millis(); // timer running
  while (millis() - T < TimeOut) {
    // waiting timeout
    while (Serial.available() > 0) {
      // receiving Serial
      stringa += char(Serial.read()); // add char
      T = millis(); // reset timer
    }
  }
  if (stringa.length() > 32) {
    lcd.setCursor(0, 1);
    lcd.print("stringa length: " + stringa.length());
    delay(2000);
    lcd.print("                ");
  } else {
    stringa1 = stringa.substring(0 , 16);
    stringa2 = stringa.substring(16);
    lcd.setCursor(0, 0);
    lcd.print(stringa1);
    lcd.setCursor(0, 1);
    lcd.print(stringa2);
    delay(5000);
  }
}