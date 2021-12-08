/*
 *for (i = 18; i <= 24; i++)
 *    print gcd(180, i);
 *  
 *int gcd(int a, int b) {
 *    if (b == 0) return a;
 *    else return gcd(b, a mod b);
 *}
 */

/*
 * r0 - pc - program counter - next instruction to be executed
 * r29 - rap - return address pointer - where RET will take us
 * r30 - fp - frame pointer - top of current stack frame
 * r31 - sp - stack pointer - points to the memory location directly after the current stack frame
 */
 
    /* CONSTANTS */
    LOAD 180 r1 //constant param 1.
    LOAD /*Address location of L1 (beginning of loop)*/ r25
    LOAD /*Address location of L2 (gcd function)*/ r26
    LOAD /*Address location of L3 (base case of GCD function)*/ r27
    LOAD /*Address location of L4 (recursive case of GCD function*/ r28
    
    /* BEGIN PROGRAM */
    LOAD 18 r2 //loop index i
    LOAD 1 r3 //constant 1 to help with ++
    LOAD 25 r4 //loop guard of 24. stop when i <= 24.
L1:
    //Let's store the return value in r5.
    WRLO 0 r1 //passing param 1
    WRLO 1 r2 //passing param 2
    JAL r26 //gcd function call
    PRNT r5 //print result of function
    ADD r2 r3 r2 //i++
    SUB r2 r4 r6//finding if statement
    IF r6 r25//continue loop if we have not hit the guard
L2:
    RELO 0 r1
    RELO 1 r2
    IF r2 r28
L3:
    
L4:
    //finding modulo: r = a - nq
