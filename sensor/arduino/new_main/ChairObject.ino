#define VERSION                 1

#define SERIAL_BAUDRATE         38400

#define PRESSURE_S0_PIN         8
#define PRESSURE_S1_PIN         9
#define PRESSURE_S2_PIN         10

#define TEMPERATURE_POWER_PIN   11
#define TEMPERATURE_DATA_PIN    12

#define PRESSURE_SEAT_PIN       A0
#define PRESSURE_BACK_PIN       A1
#define DISTANCE_PIN            A2

#define BACK_PRESSURE_SENSORS   6
#define SEAT_PRESSURE_SENSORS   4

#define SERIAL_START            0xAF
#define SERIAL_END              0xFE

#define CRC16MASK               0xA001

enum Header{
  DEBUG,
  DISTANCE,
  PRESSURE_BACK,
  PRESSURE_SEAT,
  TEMPERATURE
};

/*
 * Arduino Setup
 * Configure serial channel to PI and initialize pins.
 */
void setup(){
    Serial.begin(SERIAL_BAUDRATE);
  
    pinMode(PRESSURE_S0_PIN, OUTPUT);
    pinMode(PRESSURE_S1_PIN, OUTPUT);
    pinMode(PRESSURE_S2_PIN, OUTPUT); 
  
    digitalWrite(PRESSURE_S0_PIN, LOW);
    digitalWrite(PRESSURE_S1_PIN, LOW);
    digitalWrite(PRESSURE_S2_PIN, LOW);
  
    pinMode(TEMPERATURE_POWER_PIN, OUTPUT);
    digitalWrite(TEMPERATURE_POWER_PIN, LOW);
    
    pinMode(TEMPERATURE_DATA_PIN, INPUT);
}

/*
 * Arduino Loop
 * Read and send sensor values.
 */
void loop(){
    uint16_t pressure_values_back[BACK_PRESSURE_SENSORS] = {0};
    uint16_t pressure_values_seat[SEAT_PRESSURE_SENSORS] = {0};
    uint16_t temperature = 0;
    uint16_t distance = 0;

    getDistance(&distance);
    getPressure(pressure_values_back, pressure_values_seat, BACK_PRESSURE_SENSORS, SEAT_PRESSURE_SENSORS);
    getTemperature(&temperature);
    
    sendData(DISTANCE, 1, &distance);
    sendData(PRESSURE_BACK, BACK_PRESSURE_SENSORS, pressure_values_back);
    sendData(PRESSURE_SEAT, SEAT_PRESSURE_SENSORS, pressure_values_seat);
    sendData(TEMPERATURE, 1, &temperature);
}

uint16_t crc16(char* data, char len){
    uint16_t ret = 0;
  
    for (int i = 0; i < len; i++)
    {
        if ( ((ret >> 15) & 1) != data[i]){
            ret = (ret << 1) ^ CRC16MASK;
        } else {
            ret = (ret << 1);
        }
    }

    return ret;
}

/**
 * Send data over serial interface
 * Protocol:
 *      8          8         8         8        n * 16      16       8
 *  |--0xAF--|--Version--|--Type--|--Length--|--Payload--|--CRC--|--0xFE--|
 *  
 * Fields with a length of over 8 bits send their data with the first byte first
 */
void sendData(Header h, char len, uint16_t* payload){
    char* buf[255] = {0};

    buf[0] = VERSION;
    buf[1] = (char) h;
    buf[2] = len;
    for (int i = 0, int j = 0; i < len; i++, j = j + 2){
      uint16_t temp = payload[i];
      
      buf[3 + j    ] = (char) (temp & 0xFF);
      buf[3 + j + 1] = (char) (temp >> 8);      
    }

    uint16_t crc = crc16(buf, len+3);
    
    Serial.write(SERIAL_START);
  
    /*Serial.write(VERSION);

    Serial.write((char) h);

    Serial.write(len);

    for (int i = 0; i < len; i++){
      uint16_t temp = payload[i];

      Serial.write((char) (temp & 0xFF));
      Serial.write((char) (temp >> 8));
    }*/

    Serial.write(buf, len+3);

    Serial.write((char) (crc & 0xFF));
    Serial.write((char) (crc >> 8));
  
    Serial.write(SERIAL_END);
}

/***********************************************************
 * Temperature Sensor
 ***********************************************************/

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

int16_t readTemperature(int pin){
  uint8_t b1 = readByte(pin);
  uint8_t b2 = readByte(pin);
  
  return (b1 << 8) | b2;
}

uint16_t digitalTemperatureToCelsius(int16_t temperature_in){
  int16_t temperature_out = 0.0f;
  float temp = (float) temperature_in;

  // as seen in data sheet of "Temperature TSIC306"
  temp = (temp / 2047.0f * 200.0f) - 50.0f;
  temperature_out = (int16_t) temp;

  return temperature_out;
}

void getTemperature(uint16_t* temp_out){
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
}



/***********************************************************
 * Pressure Sensor TODO
 ***********************************************************/

void getPressure(uint16_t* pressure_values_back, uint16_t* pressure_values_seat, int back_len, int seat_len){
  int max_index = 0;

  // determine the maximum address to be indexed
  max_index = max(back_len, seat_len);

  for (int i = 0; i < max_index; i++){
    // send every address up until the maximum index to the 74HC4051
    digitalWrite(PRESSURE_S0_PIN, (i & 0x1) ? HIGH : LOW);
    digitalWrite(PRESSURE_S1_PIN, (i & 0x2) ? HIGH : LOW);
    digitalWrite(PRESSURE_S2_PIN, (i & 0x4) ? HIGH : LOW);

    // if the address is within the range of accessible sensors, read its value
    if (i < back_len){
      pressure_values_back[i] = analogRead(PRESSURE_BACK_PIN);
    }

    if (i < seat_len){      
      pressure_values_seat[i] = analogRead(PRESSURE_SEAT_PIN);
    }
  }

  // reset addressing
  digitalWrite(PRESSURE_S0_PIN, LOW);
  digitalWrite(PRESSURE_S1_PIN, LOW);
  digitalWrite(PRESSURE_S2_PIN, LOW);
}


/***********************************************************
 * Distance Sensor
 ***********************************************************/

void getDistance(uint16_t* distance_out){
  *distance_out = (uint16_t) analogRead(DISTANCE_PIN);
}

