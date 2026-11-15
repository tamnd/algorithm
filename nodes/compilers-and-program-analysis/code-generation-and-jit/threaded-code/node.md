---
tag: Q67BT1
kind: technique
slug: threaded-code
name: Threaded code
aliases:
- direct threading
- indirect threading
area: compilers-and-program-analysis/code-generation-and-jit
level: core
summary: Represents an interpreted program as a list of addresses of routines, each ending with a jump to the next, to cut dispatch cost.
prereqs: [stack]
see_also: [just-in-time-compilation, copy-and-patch-compilation, inline-caching, self-optimizing-ast-interpreter, tracing-jit-compilation, peephole-optimization, partial-evaluation, activation-record]
sources:
  - paper: doi:10.1145/362248.362270
    title: James R. Bell, Threaded code, Communications of the ACM 16(6), 1973, 370-372
    locator: the code as a list of routine addresses, the dispatch by one indirect jump through the interpretive program counter, and its use in a PDP-11 FORTRAN compiler
  - paper: doi:10.1145/360825.360849
    title: Robert B. K. Dewar, Indirect threaded code, Communications of the ACM 18(6), 1975, 330-331
    locator: one more level of indirection, so that the code points to descriptors that hold the address of the routine, and its use in SPITBOL
  - paper: "M. Anton Ertl and David Gregg, The structure and performance of efficient interpreters, Journal of Instruction-Level Parallelism 5, 2003"
    locator: the cost of dispatch, the prediction of indirect branches on switch dispatch and on threaded code
  - paper: "Todd A. Proebsting, Optimizing an ANSI C interpreter with superoperators, POPL 1995"
    locator: superoperators, new virtual instructions made of frequent sequences of old ones
---

Threaded code is a way to lay out a program for an interpreter. The program is a list of addresses of routines, one for each virtual instruction, and each routine ends with the code that fetches the next address and jumps to it. There is no central dispatch loop. Bell introduced *direct threading* in 1973, where the list holds the addresses of the routines. Dewar introduced *indirect threading* in 1975, where the list holds addresses of descriptors, and each descriptor starts with the address of its routine. Both cut the cost of dispatch, which is the main overhead of an interpreter whose virtual instructions do little work.

## In plain words

An interpreter runs a program one small step at a time. A simple interpreter has a loop: read the next step, look up its kind, run the matching code, and go back to the top. The look-up and the trip back to the loop can cost more than the step itself.

Threaded code removes the loop. The program is stored as a list of the places in memory where the matching pieces of code start. Each piece of code ends by reading the next place from the list and jumping there at once. So control goes from one piece straight to the next, like a needle along a thread.

A second form adds one more step. The list points to small records, and each record starts with the place of its code. The code can then read the rest of the record.

## When it applies

- The program is run by an interpreter, not compiled to machine code, because the compiler must be small, portable, or fast to start.
- The virtual instructions are small, such as stack operations, so the time spent in dispatch is a large part of the total.
- The host language can store the address of a piece of code and jump to it. In assembly this is natural. In C it needs a compiler extension such as the labels-as-values of GNU C. In standard C, each routine must be a function, and the dispatch becomes a call, which loses part of the gain.
- The code is created and run in the same process. Direct threaded code holds absolute addresses, so it cannot be saved to a file and loaded at another address without a fix-up step.

## The template

Let the interpretive program counter IP point into the code list, and let `goto *a` mean a jump to address $a$. A *switch* interpreter, the baseline, stores an opcode for each instruction and runs a loop:

```
loop:  op ← code[IP]; IP ← IP + 1
       if op is out of range then error
       goto *table[op]                ▷ one shared indirect jump
ADD:   b ← pop; a ← pop; push a + b; goto loop
```

A *direct threaded* interpreter stores in the code list the address of each routine, so the translation through the table is done once, when the code is built. Each routine ends with its own copy of the dispatch:

```
ADD:   b ← pop; a ← pop; push a + b
       w ← code[IP]; IP ← IP + 1; goto *w
PUSH:  push code[IP]; IP ← IP + 1     ▷ the operand follows in the list
       w ← code[IP]; IP ← IP + 1; goto *w
```

An *indirect threaded* interpreter stores the address $w$ of a descriptor, whose first word is the address of the routine. The routine gets $w$ and can read the rest of the descriptor:

```
NEXT:  w ← code[IP]; IP ← IP + 1; goto *mem[w]
LOADVAR: push mem[w + 1]; NEXT        ▷ the descriptor of a variable holds its value
```

To use the template:

1. Choose the virtual instructions and write one routine for each, ending with the dispatch.
2. Translate the source, or the bytecode, into the code list, with the address of each routine and the operands inline.
3. Start by setting IP to the first entry and jumping to the first routine.

On the PDP-11 of Bell's paper, the whole dispatch of direct threading is one instruction, `JMP @(R)+`, where the register R is IP. The switch version needs a load, a bounds check, a table load, an indirect jump and a jump back to the loop. The threaded version needs a load, an increment and an indirect jump.

## Classic examples

- **Bell's FORTRAN.** Bell described direct threading for a FORTRAN compiler on the PDP-11. The compiler emitted a list of addresses of run-time routines, which made the code smaller than inline machine code, at a small cost in speed.
- **SPITBOL.** Dewar used indirect threading in SPITBOL, a compiler for SNOBOL4. A variable in the code is the address of its descriptor, and the first word of the descriptor says what to do with it. So the same code list works for all kinds of operands, and each operand is one word.
- **Forth.** Classic Forth systems store each word, the Forth name for a routine, with a code field, and a compiled definition is a list of the addresses of these words. This is indirect threading. A primitive word has machine code in its code field, and a word defined in Forth has the address of a routine that runs its list.
- **Bytecode interpreters in C.** Many interpreters, including the reference interpreter of Python when built with GNU C, keep compact bytecode and dispatch with `goto *table[*ip++]` at the end of each routine. This is *token threading*: the table look-up stays, but each routine has its own indirect jump. The OCaml bytecode interpreter can go one step further and replace each opcode by the address of its routine when it loads the code, which is direct threading.

## Variations

- **Token threading.** The code holds opcodes, and each routine ends with a look-up and a jump. The code is compact and can be saved to a file, and dispatch is still spread over the routines.
- **Subroutine threading.** The code list becomes real machine code: a sequence of call instructions, one for each virtual instruction. The return of each routine goes back to the list. This is a first step toward a simple [JIT compiler](/just-in-time-compilation/), and [copy-and-patch compilation](/copy-and-patch-compilation/) goes further by copying the bodies of the routines instead of calling them.
- **Superinstructions.** A frequent sequence of virtual instructions, such as a load followed by an add, becomes one new instruction, so it pays for one dispatch instead of two. This is a [peephole](/peephole-optimization/) step on the virtual code.
- **Replication.** Several copies of the routine of a frequent instruction get separate addresses, so that each copy has its own indirect jump.
- **Quickening and inline caches.** A routine can write a faster version of its own instruction into the code list after the first run, for example once the type of an operand is known. [Inline caching](/inline-caching/) works in this way.

## Pitfalls

- **Branch prediction.** The gain of threaded code on a modern processor comes mostly from the indirect branches, not from the saved instructions. A switch interpreter has one shared indirect jump, which the branch predictor must guess from the previous instruction alone, and it is often wrong. With threaded code, each routine has its own indirect jump, and its target depends on the pair of instructions, which is easier to predict. Ertl and Gregg measured this effect.
- **The C compiler undoes the threading.** An optimizing C compiler may merge the identical dispatch sequences at the end of the routines into one shared jump. Then the code is a switch again, with the same poor prediction.
- **Absolute addresses.** Direct threaded code cannot be saved and loaded at another address. Store bytecode, and thread it at load time.
- **Code size against speed.** Direct threading uses one machine word for each instruction, against one byte for a typical bytecode. On a 64-bit machine this is 8 times more memory for the code.
- **Very small routines.** If a routine does almost nothing, dispatch still dominates. Superinstructions or a compiler are then a better answer than a faster dispatch.

## Exercises

1. Write a small stack machine with the instructions PUSH, ADD, MUL and HALT in C with GNU labels-as-values, once with a switch and once with direct threading. Count the machine instructions per virtual instruction in each version.
2. Show the code list, in the direct and in the indirect form, for the expression $(2 + 3) \cdot 4$. In the indirect form, how can a single LOAD routine serve every variable?
3. A program executes $n$ virtual instructions, the switch dispatch costs $c_s$ cycles, the threaded dispatch costs $c_t$ cycles, and the routines cost $w$ cycles on average. Give the speedup of threading as a function of $c_s$, $c_t$ and $w$, and show that it tends to 1 as $w$ grows.
4. Design a routine for a conditional jump in direct threaded code. Where does the target address go, and what does the routine do with IP?
5. Explain why a superinstruction for LOAD followed by ADD helps a switch interpreter more than a threaded one, in terms of the number of mispredicted branches.

## References
