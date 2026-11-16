---
tag: KRGC64
kind: algorithm
slug: copy-and-patch-compilation
name: Copy-and-patch compilation
aliases:
- stencil-based code generation
area: compilers-and-program-analysis/code-generation-and-jit
level: research
summary: Generates code very fast by copying precompiled binary stencils for each operation and patching holes with operands and addresses.
model: word-ram
complexity:
  vars: {n: "the size of the IR program, counting instructions, terminators and phi operands"}
  time: {worst: O(n)}
  space: {extra: O(n)}
prereqs: [just-in-time-compilation, control-flow-graph, threaded-code]
see_also: [maximal-munch, instruction-selection-problem, phi-function, lost-copy-and-swap-problems, out-of-ssa-translation, adaptive-optimization, linear-scan-register-allocation, simulation-relation]
sources:
  - paper: doi:10.1145/3485513
    title: "Haoran Xu and Fredrik Kjolstad, Copy-and-patch compilation: a fast compilation algorithm for high-level languages and bytecode, Proceedings of the ACM on Programming Languages 5(OOPSLA), 2021, 1-30"
    locator: the abstract (the measured compile times and run times quoted on this page); the construction of binary stencils from C++ templates whose holes are external symbols that the object file records as relocations; the stencil variants per operand location; the code generation by copying stencils and patching holes; the removal of the jump to a continuation that is placed right after
  - paper: doi:10.1145/277650.277743
    title: Ian Piumarta and Fabio Riccardi, Optimizing direct threaded code by selective inlining, PLDI 1998, 291-300
    locator: the copying of the compiled code of interpreter routines into one buffer, so that a sequence of threaded instructions becomes straight machine code without dispatch
---

Copy-and-patch compilation turns a program in an intermediate representation into machine code by copying ready-made pieces of machine code. Before any program is compiled, a library of *stencils* is built: for each kind of operation, and for each variant of its operands, a short sequence of machine code with *holes*, places whose value is not yet known, such as the address of a variable, a constant, or the address of the next piece of code. The compiler then picks one stencil for each instruction of the program, copies its bytes into a buffer, and writes the right values into its holes. There is no instruction selection, no register allocation by search and no encoding of instructions at compile time: all of that was done once, when the stencils were made. Xu and Kjolstad introduced the method in 2021. They make the stencils by compiling C++ templates with an ordinary optimizing compiler, and the holes are references to external symbols, which the object file lists as relocations.

## In plain words

A normal compiler builds each machine instruction one by one, which takes time. A copy-and-patch compiler works like filling in forms. For each kind of step, such as "add two variables" or "jump if a value is zero", it has a ready piece of machine code with a few blank fields. To compile a program, it takes the piece for each step, puts the pieces one after another in memory, and fills in the blanks: which variable to read, which number to use, and where to jump.

This is very fast, because copying and filling in blanks is cheap, and the pieces were made in advance by a good compiler. The code is not as good as the code of an optimizing compiler, because each piece is made without knowing its neighbours, but it is much better than interpreting the program.

## The problem

Input: a program in [three-address code](/three-address-code/), made of [basic blocks](/basic-block/) that form a [control flow graph](/control-flow-graph/). Each block has a list of instructions `x = k`, `x = a`, `x = a op b` and phi instructions at its top, and ends with a terminator `jump L`, `br a L1 L2` or `ret a`. An operand $a$ is a variable or an integer constant.

Output: machine code for a target machine that, run on any arguments, has the same outcome as the IR program: the same returned value, a trap in the same cases (division by zero, a shift out of range), and, in the implementation of this page, running out of fuel at the same point.

The goal is to produce this code in time linear in the size of the program, with a small constant, so that a [just-in-time compiler](/just-in-time-compilation/) can use it as its first tier.

## The algorithm

The target of this page is a small word machine with two registers r0 and r1 and an array of slots, one per variable. Its instructions are `LDS r s` (load slot $s$), `LDI r k` (load a constant), `STS s r` (store), `ALU i` (r0 = r0 op$_i$ r1, or trap), `JMP a`, `BR r a b` (go to $a$ if $r \ne 0$, else to $b$), `RET r`, and `TICK`, which uses one unit of fuel so that runs can be compared with the interpreter step by step. A real system copies x86 or ARM bytes instead, and has no TICK.

**The stencil library.** A stencil is a pair: a sequence of machine words with a 0 at each hole, and a list of holes, each an offset and a name. The library has one stencil per key:

- `const`: TICK, LDI r0 $a$, STS $x$ r0.
- `copy`, for $a$ a variable or a constant: TICK, load $a$ into r0, STS $x$ r0.
- `op`, for each operator and each of the four cases variable or constant for $a$ and for $b$: TICK, load $a$ into r0, load $b$ into r1, ALU op, STS $x$ r0.
- `br`: TICK, load $a$ into r0, BR r0 $t$ $f$. `ret`: TICK, load $a$ into r0, RET r0.
- `jump`: TICK, JMP $t$. `jump-next`: TICK alone, for a jump to the code placed right after it.
- For phis: `phi`: TICK, load $a$ into r0, STS $x$ r0, where $x$ is a temporary; `move`: LDS r0 $a$, STS $x$ r0; `goto`: JMP $t$.

"Load $a$" means LDS for a variable and LDI for a constant, so the variant is chosen by the kind of the operand. With 14 operators the library has 69 stencils. The largest has 12 words.

```
COPY-AND-PATCH(P)
L1  give each variable of P a slot, and give k temporaries their own slots,
    where k is the largest number of phis in one block
L2  pc ← 0; pieces ← empty list; stubs ← empty list
L3  for each block B of P, in order:
L4      addr[B] ← pc
L5      for each instruction ι of B that is not a phi:
L6          pick the stencil S for the kind of ι and the kinds of its operands
L7          append (pc, S, the hole values of ι) to pieces; pc ← pc + |S|
L8      for the terminator of B, do the same, where the target of an edge B → C is
        the stub of the edge if C has phis, else C itself; a jump to the block placed
        right after B uses jump-next; record each new stub B → C in stubs
L9  for each stub B → C, with phis x_1 = φ(..., B: a_1, ...), ..., x_m = φ(..., B: a_m, ...):
L10     addr[B → C] ← pc
L11     append phi stencils that read a_1 .. a_m into temporaries t_1 .. t_m,
        then move stencils x_i ← t_i for i = 1 .. m, then goto C
L12 code ← a buffer of pc words
L13 for each piece (p, S, values) in pieces:
L14     copy the words of S to code[p .. p + |S| - 1]
L15     for each hole (o, h) of S: code[p + o] ← the value of h, where a variable
        becomes its slot, a constant stays itself and a block or stub becomes addr[.]
L16 return code
```

Lines L2 to L11 are the first pass: they choose and place the stencils. The size of every stencil is known in advance, so every address is known at the end of this pass, including the addresses of blocks placed later, which forward branches need. Lines L12 to L15 are the second pass: copy and patch. The phi stubs read all operands before they write any phi variable, which gives the parallel meaning of phis, as in [out-of-SSA translation](/out-of-ssa-translation/), where the same problem is known as the [lost copy and swap problems](/lost-copy-and-swap-problems/).

## Example

Take the program that sums $0 + 1 + \dots + (n-1)$:

```
# params: n
B0:  s = 0;  i = 0;  jump B1
B1:  c = i < n;  br c B2 B3
B2:  s = s + i;  i = i + 1;  jump B1
B3:  ret s
```

L1 gives the slots n = 0, s = 1, i = 2, c = 3. There are no phis, so no stubs and no temporaries. The first pass places 9 stencils:

| address | stencil | size | hole values |
|---|---|---|---|
| 0 | const | 7 | a = 0, x = 1 |
| 7 | const | 7 | a = 0, x = 2 |
| 14 | jump-next | 1 | none |
| 15 | op<, variable and variable | 12 | a = 2, b = 0, x = 3 |
| 27 | br, variable | 8 | a = 3, t = 35, f = 62 |
| 35 | op+, variable and variable | 12 | a = 1, b = 2, x = 1 |
| 47 | op+, variable and constant | 12 | a = 2, b = 1, x = 2 |
| 59 | jump | 3 | t = 15 |
| 62 | ret, variable | 6 | a = 1 |

The code has 68 words. `jump B1` in B0 becomes a lone TICK, because B1 starts right after it. The branch at 27 needs the address 62 of B3, which is placed after it; the first pass knows it because it knows the size of each stencil.

The stencil `op+`, variable and constant, is the word sequence `1, 2, 0, 0, 3, 1, 0, 5, 0, 4, 0, 0` with holes a at offset 3, b at offset 6 and x at offset 10. Words 1, 2, 3, 5 and 4 are the opcodes TICK, LDS, LDI, ALU and STS, and the 0 after ALU selects the operator `+`. For `i = i + 1` at address 47, the second pass copies the 12 words and writes 2 (the slot of i) at 50, 1 (the constant) at 53 and 2 at 57. The result is

```
47  TICK
48  LDS 0 2
51  LDI 1 1
54  ALU 0
56  STS 2 0
```

Run with $n = 4$, the code returns 6, as the interpreter does. It runs 26 TICKs: 3 in B0, 5 in each of the four rounds through B1 and B2, 2 in the last visit to B1 and 1 in B3. The interpreter uses 26 units of fuel on the same run, so both report "out of fuel" with 25 units and both return 6 with 26. With $n = 100$ both return 4950.

## Correctness

**Theorem.** For every program $P$ of the supported form, in which every phi has an operand for each predecessor of its block and the entry block has no phi, and for all arguments and every amount of fuel, the code from COPY-AND-PATCH($P$) has the same outcome as the interpreter of the toy IR: the same returned value, or a trap, or out of fuel, or the same read of an undefined name.

The proof is in [proofs/correctness.md](proofs/correctness.md). It has three steps. First, the two passes make a code buffer in which each placed stencil appears unchanged except at its holes, and each hole holds the slot, constant or address of the first pass (Lemma 1). Second, each stencil, started in a state that agrees with the interpreter on the variables and the fuel, does what the instruction does and ends at the start of the next stencil of the block, or, for a terminator or a stub, at the address of the next block or stub (Lemma 2). Third, an induction on the steps of the interpreter keeps the two states in agreement until the end of the run.

The implementation tests the theorem on random programs from the toy IR generator, with and without loops and with added phis, on several argument pairs and on every amount of fuel up to the amount the run needs.

## Complexity

Let $n$ be the size of the program, counting instructions, terminators and phi operands, and let the variables and labels be numbered, as they are in a real IR.

- **Time.** The first pass does constant work per instruction and terminator. There are at most two stubs per block, and the stub of an edge $B \to C$ has $2m + 1$ pieces, where $m$ is the number of phis of $C$. Each of those phis has an operand for $B$, so the stubs together have at most $2 \cdot (\text{phi operands}) + 2 \cdot (\text{blocks})$ pieces. Every stencil has at most 12 words, so the second pass writes $O(n)$ words. The total is $O(n)$. The implementation maps names to slots with a dictionary, which gives the same bound in expectation.
- **Space.** The code buffer and the list of pieces have $O(n)$ words. The library has a fixed size that does not depend on the program.
- **The compiled code.** Each IR instruction becomes one stencil of a fixed size, so the code runs a constant number of machine instructions per IR step, and an edge with $m$ phis costs $O(m)$.

The constant is what matters in practice. Xu and Kjolstad report, as measurements, that their WebAssembly compiler compiles 4.9 to 6.5 times faster than Liftoff, the baseline WebAssembly compiler of Chrome, and that its code runs 39% to 63% faster than the code of Liftoff on the Coremark and PolyBenchC benchmarks. For TPC-H queries in a high-level language, their compiler compiles two orders of magnitude faster than LLVM at -O0 and three orders of magnitude faster than higher LLVM levels, and its code runs 14% faster than the code of LLVM at -O0. These numbers come from their setting and machines; the algorithm does not prove them.

## Properties

- **Each stencil is copied unchanged except at its holes.** The quality of the code inside a stencil is the quality of the compiler that made the stencil.
- **The compiled code does the same steps in the same order as the interpreter.** The number of TICKs equals the fuel that the interpreter uses, on every run.
- **No optimization crosses a stencil boundary**, except what the variants express, such as a constant operand in place of a load, or a jump that is left out when its target comes next.
- **The library grows with the variants.** The number of `op` stencils is the number of operators times the square of the number of operand kinds, so a third kind for each of the two operands takes the 56 `op` stencils here to 126.

## Variants and improvements

- **Operands in registers.** Xu and Kjolstad make stencils that take some operands in machine registers and leave their result in a register, passed by a calling convention in which the stencil ends with a tail call to the next stencil. The tail call becomes a jump that is removed when the next stencil is placed right after it, as `jump-next` does here.
- **Larger stencils.** A stencil can cover a common combination of operations, such as a compare and a branch, in the spirit of superoperators for interpreters. This removes the loads and stores between the operations.
- **Bytecode and AST tiers.** The same method can compile bytecode or a syntax tree one node at a time, which makes it a cheap first tier in [adaptive optimization](/adaptive-optimization/). The experimental JIT compiler of CPython 3.13 uses copy-and-patch, with stencils made by compiling the code of the interpreter instructions with Clang.
- **Copying interpreter routines.** Piumarta and Riccardi copy the compiled code of the routines of a [threaded](/threaded-code/) interpreter into one buffer, which removes the dispatch between them. Copy-and-patch adds holes, so the copied code can contain operands and addresses as constants.

## When to use it

- A baseline JIT tier, where compile time counts as much as code quality: WebAssembly, bytecode of dynamic languages, and database queries that are compiled and run once.
- A system that wants machine code without writing an assembler or an instruction encoder for each target. The stencils come from an existing compiler for the target, so a new target needs only that compiler and its object format.
- Not for code that runs for a long time and needs register allocation and optimization across operations. There a second, optimizing tier should take over.

## Pitfalls

- **Patching the wrong field.** A hole has a size and a kind. A 32-bit relative jump needs the difference between the target and the end of the instruction, not the absolute address, and a constant that does not fit the field needs another variant. Follow the relocation records of the object file exactly.
- **Forward references.** A branch to a block that is placed later needs its address. Lay out all stencils first, or record the hole and patch it when the target is placed.
- **Phis as sequential copies.** Writing each phi variable as soon as its operand is read gives a wrong result when one phi reads the variable of another, as in a swap. Read all operands into temporaries first.
- **Executable memory.** The buffer must be made executable after patching, and on systems that forbid memory that is both writable and executable, the patching must happen before the memory is mapped as code.
- **Too many variants.** Every new operand kind multiplies the number of stencils. Keep the variants to the cases that occur often.
- **Speed claims.** The speedups above are measurements of one implementation on given benchmarks. They are not a property of the method.

## Implementations

## History

Copying ready-made machine code is an old idea in interpreters and simple JIT compilers. Piumarta and Riccardi in 1998 copied the code of the routines of a direct threaded interpreter to remove its dispatch. Xu and Kjolstad in 2021 made the idea a general code generator: stencils with holes, made automatically by a C++ compiler from templates, chosen by operand variants, and patched with the help of the relocation records of the object file. They applied it to a WebAssembly compiler and to a compiler for a high-level language used for database queries. The method then went into practice as the experimental JIT compiler of CPython 3.13.

## References
