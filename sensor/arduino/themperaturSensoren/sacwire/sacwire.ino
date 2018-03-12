#include <inttypes.h>

#define TEMPERATURE_POWER_PIN 11
#define TEMPERATURE_DATA_PIN 12

#ifndef TEST_MODE
uint8_t readByte(int pin){
  uint16_t value = 0;

  // start sequence
  while(digitalRead(pin));
  while(!digitalRead(pin));

  // read 8 bits and a parity bit
  for(int i = 0; i < 9; ++i) {

    while(digitalRead(pin));
    delayMicroseconds(60);

    if(digitalRead(pin)) {
      value |= 1 << (8 - i);
    } else {
      while(!digitalRead(pin));
    }
  }

  return (uint8_t) (value >> 1);
}
#endif

uint16_t readTemperature(int pin){
  uint8_t b1 = readByte(pin);
  uint8_t b2 = readByte(pin);
  uint16_t ret = (b1 << 8) | b2;

  return ret;
}

uint16_t digitalTemperatureToCelsius(int16_t temperature_in){
  int16_t temperature_out = 0.0f;
  float temp = (float) temperature_in;

  // as seen in data sheet of "Temperature TSIC306"
  temp = (temp / 2047.0f * 200.0f) - 50.0f;

  // convert the temperature with one decimal place to 16 bit int
  temperature_out = (uint16_t) (temp * 10);

  return temperature_out;
}

void getTemperature(uint16_t* temp_out){
#ifdef TEST_MODE
  cout << "\n****In getTemperature()" << endl;
#endif

  uint16_t temperature = 0;

  // activate sensor
  digitalWrite(TEMPERATURE_POWER_PIN, HIGH);

  // wait for measurement
  delayMicroseconds(60);

  // get data from sensor
  temperature = readTemperature(TEMPERATURE_DATA_PIN);

  // deactivate sensor
  digitalWrite(TEMPERATURE_POWER_PIN, LOW);

  *temp_out = digitalTemperatureToCelsius(temperature);

#ifdef TEST_MODE
  cout << "****Leaving getTemperature()\n" << endl;
#endif
}



#ifdef AAAALT
uint8_t readByte(int signalPin,bool *error){
    uint16_t byte = 0;
    bool correkt = true;
    
    while(digitalRead(signalPin));
    while(!digitalRead(signalPin));
    
    // read 8 bits and a parity bit
    for(int i = 0; i < 9; ++i) {

        while(digitalRead(signalPin));
        delayMicroseconds(60);

        if(digitalRead(signalPin)) {
            byte |= 1 << (8 - i);
            correkt=!correkt;
        } else {
            while(!digitalRead(signalPin));
        }
    }
    
    if(!correkt) {
        *error=true;
    }

    return (uint8_t)(byte >> 1); // return just the date byte
}

uint16_t readWord(int signalPin,bool *error){
  uint8_t byte1 = readByte(signalPin,error);
  uint8_t byte2 = readByte(signalPin,error);
  return (byte1 << 8) | byte2;
}


float readTemperature(int powerPin,int signalPin){
  bool error=false;
  digitalWrite(powerPin, HIGH);  //Aktivate sensor 
  delayMicroseconds(60);  // etwas zeit für den sensor
  uint16_t word = readWord(signalPin,&error);    
  digitalWrite(powerPin, LOW);  //Deaktivate sensor
  if(error)return NAN;
  return (word / 2047.0f * 200.0f) - 50.0f; // from data sheet
}
#endif

void setup() {
    Serial.begin(9600); // set up the serial port
    pinMode(11,OUTPUT);
    pinMode(12,INPUT);
    
    Serial.println("start");
    
}

void loop() {
    Serial.print("read ...");
    // read temperature from sensor
    uint16_t t = 0;
    getTemperature(&t);
    Serial.println("[OK]");

    // seems ok - print the measured temperature
    Serial.print("Temperature: ");
    Serial.print(t/10.0f);
    Serial.println(" C");
    
    delay(500);
}

