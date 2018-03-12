#include <iostream>
#include <stdlib.h>
#include <bitset>
#include <time.h>

#define TEST_MODE
#define LOOP_RUNS	1

#define OUTPUT		"OUTPUT"
#define INPUT 		"INPUT"
#define LOW			"LOW"
#define HIGH		"HIGH"

#define A0			1
#define A1			2
#define A2			3

using namespace std;

void pinMode(int pin, string mode){
	cout << "Set pin " << pin << " to " << mode << endl;
}

void digitalWrite(int pin, string mode){
	cout << "Write " << mode << " on pin " << pin << endl;
}

uint16_t analogRead(int pin){
	uint16_t r = rand() % 1024;

	cout << "Read Analog(" << pin << "): " << +r << endl;

	return r;
}

char digitalRead(int pin){
	char r = rand() % 2;

	cout << "Read Digital(" << pin << "): " << +r << endl;

	return r;
}

uint8_t readByte(int pin){
	uint8_t r = rand() % 256;

	cout << "Read Byte(" << pin << "): " << +r << endl;

	return r;
}

void delayMicroseconds(int i){
	cout << "Sleep " << i << " microseconds" << endl;
}

class Serial{
public:
	static void begin(int baudrate){
		cout << "Initialize serial with baudrate " << baudrate << endl;
	};

	static void write(char c){
		string binary = bitset<8>(c).to_string();
		cout << "Serial char: " << binary << "(" << +c << ")" << endl;
	};

	static void write(char* buf, char len){
		cout << "Serial bulk:";
		for(int i = 0; i < len; i++){
			string binary = bitset<8>(buf[i]).to_string();
			cout << " " << binary << "(" << +buf[i] << ") ";
		}
		cout << endl;
	};
private:
	Serial();
};

#include "../ChairObject.ino"

bool temperatureConversionTest(){
	bool ret = true;

	uint16_t temperature = digitalTemperatureToCelsius(0x000);
	if (temperature != (uint16_t) -500){
		cout << "*temperatureConversionTest* Input: 0x000, Expected Output: -50, Got: " << (int16_t) temperature << endl;
		ret = false;
	}

	temperature = digitalTemperatureToCelsius(0x7FF);
	if (temperature != 1500){
		cout << "*temperatureConversionTest* Input: 0x7FF, Expected Output: 150, Got: " << temperature << endl;
		ret = false;
	}

	temperature = digitalTemperatureToCelsius(0x200);
	if (temperature != 0){
		cout << "*temperatureConversionTest* Input: 0x200, Expected Output: 0, Got: " << temperature << endl;
		ret = false;
	}

	temperature = digitalTemperatureToCelsius(0x2FF);
	if (temperature != 249){
		cout << "*temperatureConversionTest* Input: 0x2FF, Expected Output: 24, Got: " << temperature << endl;
		ret = false;
	}

	return ret;
}

int main(){
	int i = 0;
	srand(time(NULL));

	cout << "*************Manual tests*************" << endl;
	setup();

	for (i = 0; i < LOOP_RUNS; i++){
		loop();
	}

	cout << "\n\n*************Automated tests*************" << endl;
	if (temperatureConversionTest()){
		cout << "*temperatureConversionTest* PASSED" << endl;
	} else {
		cout << "*temperatureConversionTest* FAILED" << endl;
	}

	return 0;
}
