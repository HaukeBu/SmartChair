injection_test : InjectionTest.o
	g++ -std=c++11 -o injection_test InjectionTest.o -Wall -g

%.o : %.cpp
	g++ -std=c++11 -Wall -c -g $< -o $@

clean :
	rm InjectionTest.o injection_test
