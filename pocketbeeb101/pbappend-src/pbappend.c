
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <regex.h>
#include <string.h>

#define UEF_CODE 2
#define SSD_CODE 1
#define KEYCONFIG  "pbkeys.cfg"
#define BUFFER_SIZE 100

#ifndef linux
#define regexec xregexec
#define regfree xregfree
#define regcomp xregcomp
int errno;
#else
#include <ctype.h>
#include <errno.h>
#endif

typedef struct { 
  unsigned long size;
  unsigned char name[12];
  unsigned char keyCodes[12];
  unsigned short xScale;
  unsigned short yScale;
  unsigned short xOff;
  unsigned short yOff;
} gameheader_t;

typedef struct {
  const char * name;
  unsigned char keyCodes[12];
  int xScale;
  int yScale;
  int xOffset;
  int yOffset;
} keycfg_t;

int g_keycfg_entries = 0;
keycfg_t * g_keycfg = 0;

gameheader_t default_header = {0, "           ", {0xc, '.', ' ',  0xd, 'Z', 'X', ':', '/', 0x4, 0x3} , 128, 256, 0, 0};
  
char * load_data(FILE * bin, unsigned long * length) 
{
  if (bin==0 || errno) {
    return 0;
  }
  fseek(bin, 0, SEEK_END);
  size_t len = ftell(bin);
  char * data = (char*)malloc(len);
  rewind(bin);
  fread(data, 1, len, bin);
  fflush(bin);
  *length = len;
  return data;
}

char * trim_uef_data(FILE * uef, unsigned long * length)
{
  char * data = load_data(uef, length);
  if (data == 0)
    return 0;
  if (strncmp("UEF File!", &data[0], 9) != 0) {
    return 0;
  }
  int index = 10;
  int full_length = *length;
  unsigned char *trimmed = (unsigned char *)malloc(full_length);
  index += 2;
  //int hv=data[index++]&0xff;
  //int lv=data[index++]&0xff; 

  memcpy(trimmed, data, 12);
  int trimmedIndex = 12;
  int recognised = 0;

  while (index < full_length) {
    int blockPos = index;
    int Block = (data[index]&0xff) | ( (data[index+1]&0xff) <<8);
    index += 2;

    int Length = (0xff&data[index]) | ( (0xff&data[index+1]) <<8)
      | ( (0xff&data[index+2]) <<16) | ( (0xff&data[index+2]) <<24);

    index += 4;
    if (Length > full_length || index >= full_length)
      break;
    int CPos = index;
    if (Block==0x0460 ||
	Block==0x0462 ||
	Block==0x0467 ||
	Block==0x0468)
    {
      memcpy(trimmed+trimmedIndex, data+blockPos, Length+6);
      trimmedIndex += (Length+6);
      recognised++;
    } 

    index = CPos+Length;
  }
  memcpy(data, trimmed, trimmedIndex);
  *length = trimmedIndex;
  free(trimmed);
  if (recognised == 0)
    return 0;
  return data;
  
}

char * strip_filename(char * filename, char *name)
{
  regex_t preg;
  //regcomp(&preg, "/[[:alnum:],_,-,.]+.(uef|ssd)$" , REG_ICASE|REG_EXTENDED);
  regcomp(&preg, "/[^/]+.(uef|ssd)$" , REG_ICASE|REG_EXTENDED);
  regmatch_t pmatch;
  if (regexec(&preg, filename, 1, &pmatch, 0) == 0) {
    int size = pmatch.rm_eo - pmatch.rm_so - 1 - 4;  // strip / and .uef or .ssd
    if (size < 0 || size > 11)
      size = 11;
    if (name)
      strncpy(name, &filename[pmatch.rm_so+1], size);
    regfree(&preg);
    return &filename[pmatch.rm_so+1];
  } else {
    if (name)
      strncpy(name, &filename[0], 11);
    regfree(&preg);
    return filename;
  }
}

int keycfgcmp(const void * a, const void * b)
{
  keycfg_t * keya = (keycfg_t*)a;
  keycfg_t * keyb = (keycfg_t*)b;
  return strcmp(keya->name, keyb->name);
  
}

void configure_keys(const char * filename, gameheader_t * header)
{
  if (g_keycfg_entries == 0)
    return;


  const keycfg_t tmp = { filename , {}, 0,0,0,0};
  keycfg_t * got = bsearch(&tmp, g_keycfg, g_keycfg_entries, sizeof(keycfg_t), keycfgcmp);
  if (got)
  {
      printf("Found key entry for %s\n", filename);
      int j;
      for (j = 0; j < 10; j++)
      {
        header->keyCodes[j] = got->keyCodes[j];
      }
      header->xScale = got->xScale;
      header->yScale = got->yScale;
      header->xOff = got->xOffset;
      header->yOff = got->yOffset;
  }

  
#if 0
  // FIXME : This linear search is slow when KEYCONFIG file is large.
  //         Should qsort in initialise_keycfg then bsearch here.
  int i,j;
  for (i =0; i < g_keycfg_entries; i++)
  {
    if (strcasecmp(g_keycfg[i].name, filename) == 0)
    {
      printf("Found key entry for %s\n", filename);
      for (j = 0; j < 10; j++)
      {
        header->keyCodes[j] = g_keycfg[i].keyCodes[j];
      }
      header->xScale = g_keycfg[i].xScale;
      header->yScale = g_keycfg[i].yScale;
      header->xOff = g_keycfg[i].xOffset;
      header->yOff = g_keycfg[i].yOffset;
    }
  }
#endif
}

void append_files(int files, char * filev[], FILE * outfp) {

  int i;
  regex_t preg_uef, preg_ssd;
  regcomp(&preg_uef, ".uef$" , REG_ICASE|REG_NOSUB);
  regcomp(&preg_ssd, ".ssd$" , REG_ICASE|REG_NOSUB);
  int totalSize = 0;
  for (i =0 ; i < files; i++)
  {
    errno = 0;
    char *data = 0;
    gameheader_t header = default_header;
    const char * file_shortname = 
      strip_filename(filev[i], header.name);

    // check if file_shortname is in the config file
    // if so then need to get the keys for this game
    configure_keys(file_shortname, &header);

    
    FILE * fp = fopen(filev[i], "rb");
    if (regexec(&preg_uef, filev[i], 0, 0, 0) == 0) {
      // is a UEF file
      data = trim_uef_data(fp, &header.size);
      header.keyCodes[11] = UEF_CODE;
    } else if (regexec(&preg_ssd, filev[i], 0, 0, 0) == 0){
      // it is an SSD 
      data = load_data(fp, &header.size);
      header.keyCodes[11] = SSD_CODE;
    } else {
      printf("Skipping %s - unsupported file type.\n", filev[i]);
      continue;
    }
    if (data == 0) {
      printf("Skipping %s - problem with the data.\n", filev[i]);
      continue;
    }
    printf("Appending %i bytes of %s (%s)\n", (int)header.size, header.name,  filev[i]);
    fwrite(&header, sizeof(gameheader_t), 1 , outfp); 
    fwrite(data, 1, header.size , outfp); 
    fclose(fp);
    free(data);

    // make sure alignment is kept ok
    totalSize += header.size + sizeof(gameheader_t);
    if (0 != (totalSize&3)) {
      int tmp = 4-(totalSize&3);
      totalSize += tmp; 
      long zero = 0x00000000;
      fwrite(&zero, 1, tmp , outfp); 
    }
  }
  regfree(&preg_uef);
  regfree(&preg_ssd);

}


static void print_usage(const char * program)
{
#if 1
  printf("PocketBeeb command line append program. Use to add games to PocketBeeb emulator.\n");
  printf("Example:\n  %s -i bbc.gba -o menu.gba *.uef *.ssd \n",program);
  printf("Usage : %s [OPTIONS ... ] file ...  \n", program);
  printf("Where OPTIONS are:\n");
  printf("  -o FILE                Output to FILE.\n");
  printf("  -i FILE                Emulator input FILE\n");
  printf("  -k FILE                Keyboard configuration is in FILE\n");
  printf("\n\
One or more file may of be Single Sided Disc (ssd) images or BeebEm UEF save\n\
states.  Format guessed by file extension (.uef or .ssd). UEF states are\n\
stripped and only used blocks are appended to the output.  By default the file\n\
`pbkeys.cfg' is checked for keyboard definitions but this can be changed with\n\
the -k switch.\n");

#endif
}


int count_file(int filec, char * filev[], char * mask)
{
  regex_t preg;
  regcomp(&preg, mask , REG_ICASE|REG_NOSUB);
  int matches = 0; 
  int i;
  
  for (i =0; i < filec; i++) {
    if (regexec(&preg, filev[i], 0, 0, 0) == 0) {
      matches++;
    } 
  }
  regfree (&preg);
  return matches;
}

void initialise_keycfg(char * keycfg)
{
  // read in keycfg file. scanf the lines and store in mem, sorted, as char * name; keys
  errno = 0;
  FILE *keyfp = fopen(keycfg, "r");
  if (errno != 0)
    return;
  char buffer[BUFFER_SIZE];
  int lines = 0;
  regex_t preg;
  regcomp(&preg, "^#" , REG_ICASE|REG_NOSUB);

  while (!feof(keyfp)) {
    fgets(buffer, BUFFER_SIZE, keyfp);
    if (regexec(&preg, buffer, 0, 0, 0) != 0) {
      lines++;
    }
  }
  rewind(keyfp);
  g_keycfg = (keycfg_t*) malloc(lines*sizeof(keycfg_t));
  
  // use this regexp to match lines that start with a comment
  while (!feof(keyfp)) {
    char name_buffer[BUFFER_SIZE]={};
    buffer[0]=0;
    char key_buffer[10][6];
    int xScale, yScale, xOffset, yOffset;
    fgets(buffer, BUFFER_SIZE, keyfp);

    if (regexec(&preg, buffer, 0, 0, 0) != 0) {
      int match = sscanf(buffer, "%s%s%s%s%s%s%s%s%s%s%s%i %i %i %i\n", name_buffer, 
          key_buffer[0],
          key_buffer[1],
          key_buffer[2],
          key_buffer[3],
          key_buffer[4],
          key_buffer[5],
          key_buffer[6],
          key_buffer[7],
          key_buffer[8],
          key_buffer[9],
          &xScale, &yScale, &xOffset, &yOffset
          );
      if (match > 0) {
        int j;
        g_keycfg[g_keycfg_entries].name =(char*) malloc(strlen(name_buffer)+1);
        if (match > 11) {
          g_keycfg[g_keycfg_entries].xScale = xScale;
          g_keycfg[g_keycfg_entries].yScale = yScale;
          g_keycfg[g_keycfg_entries].xOffset = xOffset;
          g_keycfg[g_keycfg_entries].yOffset = yOffset;
        } else {
          g_keycfg[g_keycfg_entries].xScale = 0;
          g_keycfg[g_keycfg_entries].yScale = 0;
          g_keycfg[g_keycfg_entries].xOffset = 0;
          g_keycfg[g_keycfg_entries].yOffset = 0;
        }
        strncpy(g_keycfg[g_keycfg_entries].name, name_buffer, strlen(name_buffer)+1);
        for (j = 0; j < 10; j++) {
          if (strlen(key_buffer[j]) > 1) {
            g_keycfg[g_keycfg_entries].keyCodes[j] = strtol(key_buffer[j],0,0); 
          } else {
            // assume it is a char to map
            if (isalpha(key_buffer[j][0])) {
              g_keycfg[g_keycfg_entries].keyCodes[j] = toupper(key_buffer[j][0]);
            } else {
              g_keycfg[g_keycfg_entries].keyCodes[j] = key_buffer[j][0];
            }
          }
        }
        g_keycfg_entries++;
      }
    }
  }

  qsort(g_keycfg, g_keycfg_entries, sizeof(keycfg_t), keycfgcmp);

  fclose(keyfp);
  regfree(&preg);

}

void destroy_keycfg()
{
  if (g_keycfg) {
    int i;
    for (i = 0; i < g_keycfg_entries; i++) {
      if (g_keycfg[i].name)
        free(g_keycfg[i].name);
    }
    free(g_keycfg);
  }
}

int main(int argc, char * argv[])
{

  char * emulator = "bbc.gba";
  char * output = 0;
  char * keycfg_char = KEYCONFIG;
  int op = -1;
  
  int files = argc-1;
  
  while (1)
  {
    op = getopt(argc, argv,
                 "o:i:k:");
    if (op == -1)
      break;
    switch (op)
    {
      case 'o':
        output = optarg;
        files -=2;
        break;
      case 'i':
        emulator = optarg;
        files -=2;
        break;
      case 'k':
        keycfg_char = optarg;
        files -= 2;
        break;
      case '?':
        print_usage(argv[0]);
        return 1;
      default: break;
    }
  }

  if (files == 0) {
    printf("No files to append\n");
    print_usage(argv[0]);
    return 1;
  }

  
  FILE * outfp;
  FILE * infp;
  
  if (output == 0) {
    print_usage(argv[0]);
    return 1;
  } else {
    outfp = fopen(output, "wb");
  }

  infp = fopen(emulator, "rb");
  if (infp == 0 || outfp == 0 || errno)
  {
    printf("Couldn't open input or output files.\nDo the files %s and %s exist?\n",
        emulator, output);
    return 1;
  }

  int c = fgetc(infp);
  while (c != EOF)
  {
    fputc(c , outfp);
    c = fgetc(infp);
  }
  fclose(infp);
  fflush(outfp);
  int err = fseek(outfp, -4, SEEK_END);
  if (err != 0) 
  {
    printf( "Unable to seek to -4\n");
    return 1;
  }

  // write game count
  int fileindex = optind;
  int uefs = count_file(files, &argv[fileindex], ".uef$");
  int ssds = count_file(files, &argv[fileindex], ".ssd$");

  fwrite(&uefs, 1, 2, outfp);
  fwrite(&ssds, 1, 2, outfp);
  

  initialise_keycfg(keycfg_char);
  
  append_files(files, &argv[fileindex], outfp);
  fclose(outfp);

  destroy_keycfg();
  
  return 0;
}
