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
  int memory[500];
  int instr_words;
  int registers[32];
  int i;

  source = fopen(argv[1], "r");
  readIntNextLine(source, &instr_words);

  for(i = 0; i < instr_words; i++) 
    readIntNextLine(source, memory + i);

  registers[0] = 0;
  registers[30] = registers[31] = instr_words;

  for(;;) 
    {
      int pc = registers[0];
// printf("%d %d\n", pc, memory[pc]);

      switch (memory[pc]) 
        {
        case 1:  /* LOAD lit, reg */
          registers[memory[pc+2]] = memory[pc+1];
          pc += 3; break;
          
        case 2:   /* MOVE reg, reg */
          registers[memory[pc+2]] = registers[memory[pc+1]];
          pc += 3; break;
          
        case 3:  /* ADD reg, reg, reg */
          registers[memory[pc+3]] = 
            registers[memory[pc+1]] + registers[memory[pc+2]];
          pc += 4; break;
          
        case 4:  /*  SUB reg, reg, reg */
          registers[memory[pc+3]] = 
            registers[memory[pc+1]] - registers[memory[pc+2]];
          pc += 4; break;
          
        case 5:  /* MUL reg, reg, reg */
          registers[memory[pc+3]] = 
            registers[memory[pc+1]] * registers[memory[pc+2]];
          pc += 4; break;
          
        case 6:  /* DIV reg, reg, reg */
          registers[memory[pc+3]] = 
            registers[memory[pc+1]] / registers[memory[pc+2]];
          pc += 4; break;
          
        case 7:  /* IF reg, reg */
          pc = (registers[memory[pc+1]] == 0) ? pc + 3 : registers[memory[pc+2]];
          break;
          
        case 8:   /* PRNT reg */
          printf("%d\n", registers[memory[pc+1]]);
          pc += 2; break;
          
        case 9:   /* HALT */
          return (0);
          
        case 10: /* READ */
          registers[memory[pc+2]] = memory[registers[memory[pc+1]]];
          pc += 3; break;
          
        case 11: /* WRT */
          memory[registers[memory[pc+1]]] = registers[memory[pc+2]];
          pc += 3; break;
          
      case 12: /* JAL reg */
        registers[29] = pc + 2;
        pc = registers[memory[pc+1]];
        break;
        
      case 13: /* RET */
        pc = registers[29];
        break;
        
      case 14: /* PSH lit, reg */
        registers[memory[pc+2]] = registers[30];
        registers[30] = registers[31];
        registers[31] += memory[pc+1];
        pc += 3; break;
        
      case 15: /* POP reg */
        registers[31] = registers[30];
        registers[30] = registers[memory[pc+1]];
        pc += 2; break;
         
      case 16:  /* RELO lit, reg */
        registers[memory[pc+2]] = memory[registers[30] + memory[pc+1]];
        pc += 3; break;
        
      case 17: /* WRLO lit, reg */
        memory[registers[30] + memory[pc+1]] =  registers[memory[pc+2]];
        pc += 3; break;

        }
      registers[0] = pc;
    }
}
