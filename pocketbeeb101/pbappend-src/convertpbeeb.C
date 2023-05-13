#include <stdlib.h>
#ifndef linux
extern int errno;
#else
#include <errno.h>
#endif
#include <string>
using namespace std;
#define KEYS_LENGTH 10

#define ReadShort(sh)  \
  fread(tmp,1,2,infp); \
  sh = tmp[0]&0xff; \
  sh |= (tmp[1]&0xff)<<8;

void convert_entry(FILE * infp, FILE* outfp) {
  unsigned char tmp[12]; 
  int keys[10];
  int i;
  for (i = 0; i < KEYS_LENGTH; i++) {
    ReadShort(keys[i]);
  }
  int xScale,yScale,xOffset,yOffset;

  ReadShort(xScale);
  ReadShort(yScale);
  ReadShort(xOffset);
  ReadShort(yOffset);

  fread(tmp, 1, 1, infp);
  string userName("");
  string fileName("");
  while (tmp[0] != 0) {
    userName += tmp[0];
    fread(tmp, 1, 1, infp);
  }
  fread(tmp, 1, 1, infp);
  while (tmp[0] != 0) {
    fileName += tmp[0];
    fread(tmp, 1, 1, infp);
  }
  if (!fileName.empty()) {
    // print all that to the outfile
    fprintf(outfp, "%-32s 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x\n",
        fileName.c_str(),
        keys[0],
        keys[1],
        keys[2],
        keys[3],
        keys[4],
        keys[5],
        keys[6],
        keys[7],
        keys[8],
        keys[9]
        );
  }
}
int
main(int argc, char * argv[])
{

  if (argc < 2) {
    fprintf(stderr,"No files specified\n");
    return 1;
  }
  char * in = argv[1];
  char * out = argv[2];
  
  FILE * infp = fopen(in, "rb");
  FILE * outfp = fopen(out, "wb");

  if (outfp && infp && errno == 0)
  {
    while (!feof(infp)) {
      convert_entry(infp, outfp);
    }
  }

}
