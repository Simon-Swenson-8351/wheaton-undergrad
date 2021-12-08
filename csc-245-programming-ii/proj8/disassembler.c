#include<stdio.h>
#include<stdlib.h>

void readIntNextLine(FILE* source, int* dest)
{
  char line[20];
  fgets(line, sizeof(line), source);
  sscanf(line, "%d", dest);
}

int main(int argc, char** argv)
{
  FILE* source;
  char line[20];
  int instr_words;
  int* code;
  int pc;

  source = fopen(argv[1], "r");
  readIntNextLine(source, &instr_words);

  code = (int*) calloc(sizeof(int), instr_words);

  for(pc = 0; pc < instr_words; pc++) 
    readIntNextLine(source, code+pc);

  for(pc = 0; pc < instr_words; ) 
    switch (code[pc]) 
      {
      case 1:  /* LOAD lit, reg */
        printf("%d: LOAD %d r%d\n", pc, code[pc+1], code[pc+2]);
        pc += 3; break;
        
      case 2:   /* MOVE reg, reg */
        printf("%d: MOVE r%d %d\n", pc, code[pc+1], code[pc+2]);
        pc += 3; break;
        
      case 3:  /* ADD reg, reg, reg */
        printf("%d: ADD r%d r%d r%d\n", pc, code[pc+1], code[pc+2], code[pc+3]);
        pc += 4; break;
        
      case 4:  /* SUB reg, reg, reg */
        printf("%d: SUB r%d r%d r%d\n", pc, code[pc+1], code[pc+2], code[pc+3]);
        pc += 4; break;
        
      case 5:  /* MUL reg, reg, reg */
        printf("%d: MUL r%d r%d r%d\n", pc, code[pc+1], code[pc+2], code[pc+3]);
        pc += 4; break;
        
      case 6:  /* DIV reg, reg, reg */
        printf("%d: DIV r%d r%d r%d\n", pc, code[pc+1], code[pc+2], code[pc+3]);
        pc += 4; break;
        
      case 7:  /* IF reg, reg */
        printf("%d: IF r%d r%d\n", pc, code[pc+1], code[pc+2]);
        pc += 3; break;                    
        
      case 8:   /* PRN reg */
        printf("%d: PRNT r%d\n", pc, code[pc+1]);
        pc += 2; break;
        
      case 9:   /* HLT */
        printf("%d: HALT\n", pc);
        pc++; break;

      case 10: /* READ */
        printf("%d: READ r%d r%d\n", pc, code[pc+1], code[pc+2]);
        pc += 3; break;

      case 11: /* WRT */
        printf("%d: WRT r%d r%d\n", pc, code[pc+1], code[pc+2]);
        pc += 3; break;
      case 12: /* JAL reg */
        printf("%d: JAL r%d\n", pc, code[pc+1]);
        pc += 2; break;

      case 13: /* RET */
        printf("%d: RET\n", pc);
        pc += 1; break;

      case 14: /* PSH lit, reg */
        printf("%d: PSH %d r%d\n", pc, code[pc+1], code[pc+2]);
        pc += 3; break;

      case 15: /* POP reg */
        printf("%d: POP r%d\n", pc, code[pc+1]);
        pc += 2;  break;

      case 16: /* RELO lit, reg */
        printf("%d: RELO %d r%d\n", pc, code[pc+1], code[pc+2]);
        pc += 3; break;

      case 17: /* WRLO lit, reg */
        printf("%d: WRLO %d r%d\n", pc, code[pc+1], code[pc+2]);
        pc += 3; break;

      }  
  
  return (0);

}
