---
title: Copy-and-patch code has the same outcome as the interpreter
proves: [correctness]
status: full
---

We use COPY-AND-PATCH with lines L1 to L16, the stencil library and the word machine from the page. $P$ is a program of the supported form: its instructions are `const`, `copy`, `op` and `phi`, the phis of a block come before its other instructions, the entry block has no phi, every phi of a block $C$ has an operand for each predecessor of $C$, the parameters are distinct, and the arguments are integers.

**The interpreter.** The interpreter of the toy IR keeps an environment $E$, a partial map from names to integers, a fuel counter $f$, the current block and the previous block. A *tick* stops the run with "out of fuel" if $f = 0$, and otherwise sets $f \leftarrow f - 1$. When it enters a block $C$ from a block $B$, it does, for each phi $x_i = \varphi(\dots, B: a_i, \dots)$ in order, a tick and then reads $a_i$; after all reads it sets $x_i \leftarrow v_i$ for $i = 1, \dots, m$ in order. Then, for each other instruction in order, it does a tick and then the instruction, and for the terminator it does a tick and then jumps, branches on $v \ne 0$, or returns. Reading a name that is not in $E$ raises "undefined name". An operator traps on division or remainder by 0 and on a shift by an amount outside 0 to 63.

**Agreement.** A slot array $\sigma$ *agrees* with $E$ when, for every name $x$ of $P$, $\sigma[\mathrm{slot}(x)] = E(x)$ if $x$ is in $E$, and $\sigma[\mathrm{slot}(x)]$ is unset otherwise. Line L1 gives every name that $P$ defines or reads its own slot, and the temporaries get further slots. A temporary is not a name of $P$, so writing a temporary does not change agreement.

**Pieces.** The first pass makes a list of pieces $(p_1, S_1), (p_2, S_2), \dots$ with $p_1 = 0$ and $p_{i+1} = p_i + |S_i|$, by line L7. For a block $B$, its pieces are those of its non-phi instructions in order, then that of its terminator, and they are consecutive; $\mathrm{addr}[B]$ is the address of the first of them. All block pieces come before all stub pieces, and the blocks are placed in program order.

## Lemma 1 (copy and patch)

After line L15, for every piece $(p, S)$ and every offset $o < |S|$, $\mathrm{code}[p + o] = S.\mathrm{code}[o]$ if $o$ is not a hole of $S$, and $\mathrm{code}[p + o]$ is the value of the hole if $(o, h)$ is a hole: the slot of the variable, the constant, or $\mathrm{addr}$ of the block or stub.

*Proof.* The intervals $[p_i, p_i + |S_i|)$ are disjoint, because $p_{i+1} = p_i + |S_i|$, and their union is the whole buffer. Line L14 writes only the interval of its own piece, and line L15 overwrites only hole offsets of that interval. So after its own piece is processed, a word is never written again. Each $\mathrm{addr}$ value is defined when line L15 needs it: every block gets an address at L4, and every stub that a terminator targets is put in the list at L8 and gets an address at L10, all before the second pass starts. $\square$

## Lemma 2 (one stencil)

Let the machine be at $\mathrm{pc} = p$, the address of a piece, with a slot array that agrees with $E$ and fuel $f$, and let the interpreter be at the instruction or terminator of that piece with the same $E$ and $f$, or about to enter $C$ from $B$ when the piece is the first of the stub $B \to C$.

1. For a piece of a `const`, `copy` or `op` instruction $\iota$ of block $B$: if the interpreter stops on $\iota$, the machine stops with the same outcome. Otherwise the machine reaches the address of the next piece of $B$ with a slot array that agrees with the new environment and the same fuel as the interpreter.
2. For a piece of a terminator of $B$: if it returns $v$, the machine returns $v$. If it goes to block $C$, the machine reaches $\mathrm{addr}[B \to C]$ if $C$ has phis and $\mathrm{addr}[C]$ otherwise, with agreement and equal fuel. If the interpreter stops, the machine stops with the same outcome.
3. For the stub $B \to C$: if the interpreter stops while it runs the phis of $C$, the machine stops with the same outcome. Otherwise the machine reaches $\mathrm{addr}[C]$ with a slot array that agrees with the environment after the phis, and with the same fuel.

*Proof.* By Lemma 1 the words at $p$ are those of the stencil with the patched values, so we can read the stencil from the library.

Case 1. Every such stencil starts with TICK, which stops with "out of fuel" exactly when $f = 0$ and otherwise decrements $f$, as the interpreter's tick does. Next, the stencil loads the operands in the order of the instruction, $a$ then $b$: for a variable, LDS of its slot, which by agreement gives $E(a)$, or raises "undefined name" exactly when $a$ is not in $E$; for a constant, LDI of the constant, which is the value the interpreter uses. The variant was chosen at line L6 by the kind of each operand, so the right one of LDS or LDI is there. ALU computes the operator of the stencil on the two values with the same rules as the interpreter: the same results for the ten simple operators, division that truncates toward zero, a remainder with the sign of the dividend, a trap on a zero divisor and on a shift outside 0 to 63. So it traps exactly when the interpreter traps, and otherwise computes the same value $v$. STS writes $v$ into the slot of $x$, while the interpreter sets $E(x) \leftarrow v$, so agreement holds for the new environment. The stencil has no jump, so the machine continues at $p + |S|$, which is the address of the next piece, and by the layout that is the next instruction or the terminator of $B$.

Case 2. The stencil starts with TICK, as above. For `ret`, it loads $a$ as in Case 1 and returns it. For `br a L1 L2`, it loads $a$ and executes `BR r0 t f`, where $t$ and $f$ were patched with the targets chosen at L8 for the edges to $L1$ and $L2$; it goes to $t$ when the value is not 0, as the interpreter goes to $L1$. For `jump L` with the `jump` stencil, it goes to the patched target. For `jump L` with `jump-next`, line L8 chose this stencil only when the target is the block $L$ itself, so $L$ has no phis, and $L$ is placed right after $B$. Then $p + 1$ is the first address after the piece, which is $\mathrm{addr}[L]$, and the machine continues there. A terminator does not write any slot, so agreement holds.

Case 3. Let the phis of $C$ be $x_i = \varphi(\dots, B: a_i, \dots)$ for $i = 1, \dots, m$. By the assumption on $P$, the operand $a_i$ exists. Line L11 placed $m$ `phi` stencils, then $m$ `move` stencils, then `goto`. The $i$-th `phi` stencil does a tick, loads $a_i$ and stores it into temporary $t_i$. These stores do not touch a slot of a name of $P$, so during all $m$ reads the slot array still agrees with $E$, and each load gives $E(a_i)$, or raises "undefined name" exactly when the interpreter does. The ticks come in the same order as the interpreter's ticks, each before its read, so the run stops for lack of fuel at the same phi. After the reads, $t_i = v_i$ for every $i$. The $i$-th `move` stencil copies $t_i$ to the slot of $x_i$, for $i = 1, \dots, m$ in order, which is the order in which the interpreter assigns; if a name appears twice, the last one wins in both. So the slot array agrees with the environment after the phis. The `goto` stencil jumps to $\mathrm{addr}[C]$. The moves and the goto have no TICK, and the interpreter's assignments use no fuel, so the fuel is equal. $\square$

## Theorem

For every program $P$ of the supported form, every list of integer arguments and every fuel $f_0$, the code from COPY-AND-PATCH($P$) returns the same value as the interpreter, or traps when the interpreter traps, or runs out of fuel when the interpreter runs out of fuel, or reads an undefined name when the interpreter does.

*Proof.* We show that the following invariant holds each time the interpreter is about to run an instruction or terminator of a block, or about to enter a block from an edge: the machine is at the address of the matching piece (for entry from $B$ into a block $C$ with phis, the stub $B \to C$; for entry into a block without phis, the address of the block), its slot array agrees with $E$, and the two fuel counters are equal.

At the start, the interpreter is at the entry block, which has no phi, with $E$ mapping the parameters to the arguments and fuel $f_0$. The machine starts at address 0, which is $\mathrm{addr}$ of the entry block because it is placed first. Its slot array holds the arguments in the slots of the parameters, which come first and are distinct, and all other slots are unset. So the invariant holds.

If the invariant holds, Lemma 2 applies to the current piece. Either both stop with the same outcome, or the interpreter moves to its next position and the machine to the matching address, and the invariant holds again. For a block $C$ without phis, the interpreter's entry into $C$ does no work, and Case 2 already brought the machine to $\mathrm{addr}[C]$, the first piece of $C$.

Every instruction and every terminator uses one tick, so the interpreter takes at most $f_0 + 1$ instruction or terminator steps before it stops. Each such step is matched by one application of Lemma 2, plus one more for a stub. So the run ends, and by the invariant it ends with the same outcome on both sides. $\square$

## Remarks

- The number of TICKs that the machine runs equals the fuel that the interpreter uses, on every run, by the cases of Lemma 2. This is why the outcomes agree for every fuel value, which the tests check one fuel value at a time.
- The proof uses only two facts about each stencil: what it does to the slots and to the fuel, and where it leaves the program counter. A system with stencils made by a C++ compiler needs the same two facts about each stencil, plus the fact that the relocation records name every hole exactly.
