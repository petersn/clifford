
CPPFLAGS=-O3 -ffast-math -std=c++11

all: clifford finder

clifford: clifford.o
	g++ -o $@ $<

finder: finder.o
	g++ -o $@ $<

