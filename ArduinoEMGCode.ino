#include <SPI.h>
#include <SD.h>
#include <LiquidCrystal.h>
//////////////////////////////////////////////////////////////////////////
String stringa;
const unsigned long Timeout = 10; //10 ms timeout bc yes
String stringa1;
String stringa2;
///////////////////////////////////////////////////////////////////////////
File myFile;
float signal =0;
/////////////////////////////////////////////////////////////////////////////
 int forpin = A1;
 float forehead = 0;

 int rcheekpin = A2;
 float Rcheek = 0;

 int lcheekpin = A3;
 float Lcheek =0;

 int rjawpin = A4;
 float Rjaw = 0;


 int ljawpin = A5;
 float Ljaw = 0;

File myFile;
float signal = 0;
/////////////////////////////////////////////////////////////////////////////////
void setup() {
  // put your setup code here, to run once:
 Serial.begin(9600);
}

void setup() {
 // initialize the lcd screen and begin serial output
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
    // tell patient to actuate muscles, and collect data from each pin and write to SD card
  Serial.print("Please srcunch up your face for 5 seconds....");
  // --------------------> start collect analog signal from each pin 
  forehead = analogRead(forehead*(-0.01)); // read forehead
  Serial.print("collecting forehead  EMG")
  delay(1000);
  Rcheek = analogRead(Rcheek*(-0.01)); // read right cheek
  Serial.print("collecting right cheek EMG")
  delay(1000);
  Lcheek = analogRead(Lcheek*(-0.01)); // read left cheek
  Serial.print("collecting left cheek EMG")
  delay(1000);
  float Rjaw = analogRead(Lcheek*(-0.01)); // read right jaw
  Serial.print("collecting right jaw EMG")
  delay(1000);
  float Ljaw = analogRead(Ljaw*(-0.01)); // read left jaw
  Serial.print("collecting left jaw EMG")
  reading = reading*(-10);
  Serial.println(reading);
  delay(10000);
  Serial.print("Please relax your face and wait for your determination.....");

  // initialize string a to be passed from the python code into here, all of this is basically setting up the arduino to receive a string from python
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
  delay(10000)
  //////////////////// Here we are outputting the string received from the python code
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