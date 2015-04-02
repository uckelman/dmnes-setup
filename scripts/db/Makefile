all: libdate.so

date.o: date.tab.cpp
	g++ -std=c++11 -O3 -fPIC -Wall -Wextra -pedantic -o date.o -c date.tab.cpp

libdate.so: date.o
	g++ -shared -Wl,-soname,libdate.so -o libdate.so date.o

date.tab.cpp: date.ypp
	bison -r solved -o date.tab.cpp date.ypp

.PHONY: clean

clean:
	$(RM) libdate.so date.o date.tab.cpp y.output
