
.SUFFIX :

# I hackily compiled it for windoze with:
# i586-mingw32msvc-gcc pbappend.c -o pbappend.exe -I /usr/include /usr/i586-mingw32msvc/lib/libiberty.a
# i586-mingw32msvc-g++ convertpbeeb.C -o convertpbeeb.exe -I /usr/i586-mingw32msvc/include /usr/i586-mingw32msvc/lib/libiberty.a
# I have no idea where errno and regex.h are in the mingw debian distribution. MIA?

ifndef GCC
GCC := gcc
endif
ifndef GXX
GXX := g++
endif

all : pbappend convertpbeeb

CFLAGS += -Wall -g -O2

pbappend : pbappend.c
	@$(GCC) $(CFLAGS) $^ -o $@

convertpbeeb : convertpbeeb.C
	@$(GXX) $(CFLAGS) $^ -o $@

dist:
	tar czvf pbappend.tar.gz convertpbeeb.C pbappend.c Makefile README
	zip pbappend.zip pbappend.exe convertpbeeb.exe README
