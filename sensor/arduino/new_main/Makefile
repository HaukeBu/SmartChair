arduino_test : mainTest.o
	g++ -std=c++11 -o arduino_test mainTest.o -Wall -g

%.o : %.cpp
	g++ -std=c++11 -Wall -c -g $< -o $@

clean :
	rm mainTest.o arduino_test
