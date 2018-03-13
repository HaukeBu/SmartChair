#include "crc16.h"

#define VERSION					1

#define SERIAL_BAUDRATE			38400

#define PRESSURE_S0_PIN			8
#define PRESSURE_S1_PIN			9
#define PRESSURE_S2_PIN			10

#define TEMPERATURE_POWER_PIN	11
#define TEMPERATURE_DATA_PIN	12

#define PRESSURE_SEAT_PIN		A0
#define PRESSURE_BACK_PIN		A1
#define DISTANCE_PIN			A2

#define BACK_PRESSURE_SENSORS	6
#define SEAT_PRESSURE_SENSORS	4

#define SERIAL_SEND_START		0xAF
#define SERIAL_SEND_END			0xFE

#define SERIAL_READ_START		0xDE
#define SERIAL_READ_END			0xED

#define CRC16MASK				0x8005

enum Header{
	DEBUG,
	DISTANCE,
	PRESSURE_BACK,
	PRESSURE_SEAT,
	TEMPERATURE,
	HEADER_END
};

enum DebugMessages{
	CONFIG_OK = 1,
	CONFIG_NO_START_SYMBOL,
	CONFIG_NO_END_SYMBOL,
	CONFIG_WRONG_VERSION,
	CONFIG_CRC_ERROR
};

uint16_t intervals[HEADER_END] = {0};
unsigned long next_measurement[HEADER_END] = {0};


/**
 * Send data over serial interface
 * Protocol:
 *		8			8		 8			8		n * 16		16		 8
 *	|--0xAF--|--Version--|--Type--|--Length--|--Payload--|--CRC--|--0xFE--|
 *
 * Fields with a length of over 8 bits send their data LSB first
 */
void sendData(Header h, char len, uint16_t* payload){
	char buf[255] = {0};
	int i = 0;
	int j = 0;

	buf[0] = VERSION;
	buf[1] = (char) h;
	buf[2] = len*2;
	for (i = 0, j = 0; i < len; i++, j = j + 2){
		uint16_t temp = payload[i];

		buf[3 + j    ] = (uint8_t) (temp & 0xFF);
		buf[3 + j + 1] = (uint8_t) (temp >> 8);
	}

	uint16_t crc = crc16_ccitt(buf, len*2+3);

#ifndef TEST_MODE
	Serial.write(SERIAL_SEND_START);

	Serial.write(buf, len*2+3);

	Serial.write((char) (crc & 0xFF));
	Serial.write((char) (crc >> 8));

	Serial.write(SERIAL_SEND_END);
#else
	Serial::write(SERIAL_SEND_START);


	Serial::write(buf, len*2+3);

	Serial::write((char) (crc & 0xFF));
	Serial::write((char) (crc >> 8));

	Serial::write(SERIAL_SEND_END);
#endif
}

/**
 * Read data over serial interface
 * Protocol:
 *		8			8		   8	 n * {8		 16}		16		 8
 *	|--0xDE--|--Version--|--Length--|--{Type--Interval}--|--CRC--|--0xED--|
 *
 * Receives the interval in which data has to be aquired and sent
 * Length indicates the amount of (type, interval) tuples
 * Fields with a length of over 8 bits were sent LSB first
 */
#ifndef TEST_MODE
int readData(){
	char buf[255] = {0};
	char length = 0;
	int i = 0;
	int j = 0;

	// Check version
  while(!Serial.available()){}
	if ((buf[0] = (char) Serial.read()) != VERSION){
		return CONFIG_WRONG_VERSION;
	}

	// Read length
  while(!Serial.available()){}
	buf[1] = Serial.read();

	// Read payload
	length = 2;
	for (i = 0, j = 0; i < buf[1]; i++, j = j + 3){
    while(!Serial.available()){}
		buf[2 + j    ] = Serial.read();
   while(!Serial.available()){}
		buf[2 + j + 1] = Serial.read();
   while(!Serial.available()){}
		buf[2 + j + 2] = Serial.read();
		length = length + 3;
	}

while(!Serial.available()){}
	unsigned char crc1 = Serial.read();
  while(!Serial.available()){}
	unsigned char crc2 = Serial.read();

while(!Serial.available()){}
	if (Serial.read() != SERIAL_READ_END){
		return CONFIG_NO_END_SYMBOL;
	}

	// Check crc
	uint16_t crc = (crc2 << 8) | crc1;
	uint16_t crc_recv = crc16_ccitt(buf, length);
	if (crc_recv != crc){
		return CONFIG_CRC_ERROR;
	}


	// Assign received intervals
	for (i = 0, j = 2; i < buf[1]; i++, j+=3){
		intervals[buf[j]] = (buf[j + 2] << 8) | (buf[j + 1] & 0xFF);
	}

	return CONFIG_OK;
}
#endif

/***********************************************************
 * Temperature Sensor
 ***********************************************************/

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



/***********************************************************
 * Pressure Sensor
 ***********************************************************/

void getPressure(uint16_t* pressure_values_back, uint16_t* pressure_values_seat, int back_len, int seat_len){
#ifdef TEST_MODE
	cout << "\n****In getPressure()" << endl;
#endif

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

#ifdef TEST_MODE
	cout << "****Leaving getPressure()\n" << endl;
#endif
}

void getDistance(uint16_t* distance_out){
#ifdef TEST_MODE
	cout << "\n****In getDistance()" << endl;
#endif


	*distance_out = (uint16_t) analogRead(DISTANCE_PIN);

#ifdef TEST_MODE
	cout << "****Leaving getDistance()\n" << endl;
#endif
}

/***********************************************************
 * Helper Functions
 ***********************************************************/

bool canMeasure(Header h){
	return intervals[h] > 0 && next_measurement[h] <= millis();
}

void setNextMeasure(Header h){
	next_measurement[h] = millis() + intervals[h];
}

/*
 * Arduino Setup
 * Configure serial channel to PI and initialize pins.
 */
void setup(){
#ifdef TEST_MODE
	cout << "\n****In setup()" << endl;
	Serial::begin(SERIAL_BAUDRATE);
#else
	Serial.begin(SERIAL_BAUDRATE);
  while(!Serial);
#endif

	pinMode(PRESSURE_S0_PIN, OUTPUT);
	pinMode(PRESSURE_S1_PIN, OUTPUT);
	pinMode(PRESSURE_S2_PIN, OUTPUT);

	digitalWrite(PRESSURE_S0_PIN, LOW);
	digitalWrite(PRESSURE_S1_PIN, LOW);
	digitalWrite(PRESSURE_S2_PIN, LOW);

	pinMode(TEMPERATURE_POWER_PIN, OUTPUT);
	digitalWrite(TEMPERATURE_POWER_PIN, LOW);

	pinMode(TEMPERATURE_DATA_PIN, INPUT);

#ifdef TEST_MODE
		cout << "****Leaving setup()\n" << endl;
#endif
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

	if (Serial.available() && Serial.read() == SERIAL_READ_START){
		// Return with debug message
		uint16_t ret = (uint16_t) readData();
		sendData(DEBUG, 1, &ret);
	}

	if (canMeasure(DISTANCE)){
		getDistance(&distance);
		sendData(DISTANCE, 1, &distance);
		setNextMeasure(DISTANCE);
	}

	if (canMeasure(PRESSURE_BACK)) {
		getPressure(pressure_values_back, pressure_values_seat, BACK_PRESSURE_SENSORS, SEAT_PRESSURE_SENSORS);
		sendData(PRESSURE_BACK, BACK_PRESSURE_SENSORS, pressure_values_back);
		setNextMeasure(PRESSURE_BACK);
	}

	if (canMeasure(PRESSURE_SEAT)){
		getPressure(pressure_values_back, pressure_values_seat, BACK_PRESSURE_SENSORS, SEAT_PRESSURE_SENSORS);
		sendData(PRESSURE_SEAT, SEAT_PRESSURE_SENSORS, pressure_values_seat);
		setNextMeasure(PRESSURE_SEAT);
	}

	if (canMeasure(TEMPERATURE)){
		getTemperature(&temperature);
		sendData(TEMPERATURE, 1, &temperature);
		setNextMeasure(TEMPERATURE);
	}
}
