---
tag: 7B5P5Q
kind: technique
slug: constant-folding
name: Constant folding
aliases:
- compile-time evaluation
area: compilers-and-program-analysis/optimizations
level: intro
summary: Evaluates at compile time the operations whose operands are all constants and replaces them by the result, using the arithmetic of the target machine.
prereqs: [three-address-code, basic-block]
see_also: [constant-propagation-problem, sparse-conditional-constant-propagation, local-value-numbering, peephole-optimization, dead-code-elimination, partial-evaluation, integer-overflow, ieee-754]
sources:
  - book: isbn:9781558603202
    title: Steven S. Muchnick, Advanced Compiler Design and Implementation, Morgan Kaufmann, 1997
    locator: Section 12.1 (Constant-Expression Evaluation (Constant Folding)), with the remarks on overflow, division by zero and floating point, and Section 12.3 (Algebraic Simplifications and Reassociation)
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Addison-Wesley, 2007
    locator: Section 8.5.4 (Use of Algebraic Identities, with constant folding) and Section 9.4 (Constant Propagation)
  - book: isbn:9780128154120
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, third edition, Morgan Kaufmann, 2022
    locator: Section 8.4.1 (Local Value Numbering), the extensions for constant folding and algebraic identities
  - paper: "ISO/IEC 9899:2018, Information technology, Programming languages, C, International Organization for Standardization, 2018"
    locator: Section 6.6 (Constant expressions, which the translator must evaluate) and Section 6.5 (signed overflow and division by zero are undefined behavior)
---

Constant folding replaces an operation whose operands are all known constants by its result, computed while the program is compiled. The instruction `b = 6 * 7` becomes `b = 42`. The result must be the value that the target machine would compute at run time, with its word size, its rounding and its rules for division and shifts, and an operation that would trap at run time must not be folded. Constant folding is local and needs no analysis; [constant propagation](/constant-propagation-problem/) finds the constants across the [control flow graph](/control-flow-graph/) and feeds them to it.

## In plain words

Some computations in a program have inputs that are fixed when the program is written, such as six times seven. The compiler can do this arithmetic once, while it builds the program, and put the answer in place of the computation. The program then does less work each time it runs.

The compiler must get the same answer that the real machine would get. Machines round and cut off numbers in their own ways, so the compiler cannot use its own arithmetic without care. If the computation would crash the program, such as a division by zero, the compiler must leave it alone: the program may never reach that line, and when it does, it must crash in the same way.

## When it applies

An instruction `x = a op b` can be folded when:

- both `a` and `b` are integer constants, either written in the instruction or known from an earlier `const` instruction in the same block (or from a [constant propagation](/constant-propagation-problem/) result);
- the operation does not trap on these values. In the toy IR, `/` and `%` trap when $b = 0$, and `<<` and `>>` trap when $b$ is outside 0 to 63. A real target adds its own cases, such as the trap of `INT_MIN / -1` on x86;
- the compiler can compute the result exactly as the target does.

A branch `br a L1 L2` with a constant `a` folds to `jump L1` or `jump L2`. The other target may then become unreachable, and [dead code elimination](/dead-code-elimination/) can remove it.

## The template

**The rewrite.** Walk each [basic block](/basic-block/) from top to bottom and keep a map $K$ from names to known constants. At `x = k`, set $K[x] = k$. At `x = a op b`, replace each name operand that is in $K$ by its constant. If both operands are now constants $c_1$ and $c_2$, and $c_1 \mathbin{op} c_2$ does not trap on the target, replace the instruction by `x = v` with $v = \mathrm{eval}_{target}(op, c_1, c_2)$ and set $K[x] = v$. Otherwise keep the instruction and delete $x$ from $K$. A copy `x = y` sets $K[x] = K[y]$ if $y$ is in $K$, and deletes $x$ from $K$ otherwise. At the end of the block, $K$ is dropped. Each instruction costs $O(1)$ map operations, so a block of $n$ instructions takes $O(n)$ expected time with a [hash table](/hash-table/).

**Legality.** The rewrite is legal when $\mathrm{eval}_{target}$ is the operation of the target machine on the same values, and the operation does not trap on them. The analysis fact that the rewrite needs is "operand $a$ holds $c_1$ and operand $b$ holds $c_2$ at this point on every run that reaches it". The walk gives this fact inside one block.

**Profit.** The cost model is the number of instructions executed. A folded instruction becomes a constant load, which is at most as costly and often free, because the constant can go into the immediate field of a later instruction. The larger gain is indirect: a folded branch condition removes a branch and possibly a whole region, and folded constants make more folding possible downstream. The rewrite does not pay when the constant is costly to build. A 64-bit constant takes up to several instructions to build on many RISC machines, while `x = a << 40` with `a` in a register takes one. Back ends handle this by register rematerialization or by keeping the shift.

**Proof that behavior stays the same.** It is enough to show that each changed name holds the same value at every use. The invariant of the walk is: at each point of the block, for every $y$ in $K$, the variable $y$ holds $K[y]$ on every run that reaches the point. It holds at the top of the block, where $K$ is empty. Each step keeps it: `x = k` sets $x$ to $k$; a copy of a known name copies its known value; a folded instruction `x = v` stores the value $v = c_1 \mathbin{op} c_2$ that the original instruction would store, because by the invariant its operands hold $c_1$ and $c_2$, and by legality the target computes $v$ from them without a trap; any other definition of $x$ deletes $x$ from $K$, and no other name changes. So every rewritten instruction stores the same value as the original, and the original does not trap there. Instructions that may trap are not changed, so a run that traps still traps at the same instruction. The state after each instruction is the same in both programs, so the outcome is the same.

## Classic examples

**A block with a trap on one path.** In the toy IR, `/` truncates toward zero, as in C, and `%` keeps the sign of the dividend. The parameter is `x`.

```
entry:
  a = 6
  b = a * 7
  c = b / -5
  d = c % 5
  e = x + 0
  br x big small
big:
  g = 1 << 70
  ret g
small:
  f = d - e
  ret f
```

Folding the entry block gives `b = 42`, `c = -8` (because $42 / (-5) = -8.4$ truncates to $-8$) and `d = -3` (because $-8 - 5 \cdot (-1) = -3$). The algebraic identity $x + 0 = x$ turns `e = x + 0` into the copy `e = x`. The instruction `g = 1 << 70` is not folded: the shift count is out of range, so it traps at run time. The original and the folded program both return $-3$ for $x = 0$ and both trap for $x \in \{-2, 1, 5\}$. A local folder does not change `f = d - e` in block `small`, because `d` is defined in another block. A global [constant propagation](/constant-propagation-problem/) finds $d = -3$ there.

**The host is not the target.** A folder written in Python that uses `//` and `%` computes `c = 42 // -5 = -9` and `d = -9 % 5 = 1`, because Python rounds toward minus infinity. The program would then return $1$ instead of $-3$. This is the most common bug of a toy folder.

**Fixed-width words.** On a 32-bit target, `2147483647 + 1` wraps to $-2147483648$ in two's complement (see [two's complement](/twos-complement/)). In C, signed overflow is undefined behavior, so a C compiler may fold it to any value or assume it never happens; an unsigned addition must wrap. The folder must know which rule the source language and the target use (see [integer overflow](/integer-overflow/)).

**Floating point.** Under [IEEE 754](/ieee-754/), `x + 0.0` is not always `x`: for $x = -0.0$ the sum is $+0.0$. Also `x * 0.0` is not $0.0$ when $x$ is NaN, infinite or negative. A folder of floating-point code must compute in the target precision and rounding mode, which may differ from the host, and must keep the exception flags if the language makes them visible.

## Variations

- **Algebraic simplification.** Rewrite with identities that hold for all values: $x + 0 = x$, $x \cdot 1 = x$, $x - x = 0$, $x \oplus x = 0$ and, for integers without traps, $x \cdot 0 = 0$. Each identity must hold on the target, including traps: $x / x = 1$ is false for $x = 0$, and $0 / x = 0$ removes a trap.
- **Constant propagation.** Finds the names that hold a constant at a point across blocks, by [dataflow analysis](/dataflow-analysis/) on a flat lattice; see [constant-propagation-problem](/constant-propagation-problem/) and [sparse conditional constant propagation](/sparse-conditional-constant-propagation/), which also folds branches as it goes.
- **Folding inside value numbering.** [Local value numbering](/local-value-numbering/) folds an operation when the value numbers of both operands are constants, and applies identities on value numbers.
- **Constant expressions in the language.** C requires the translator to evaluate integer constant expressions, for example array sizes and case labels. C++ `constexpr` functions and [partial evaluation](/partial-evaluation/) run larger parts of a program at compile time. These go beyond folding single operations.

## Pitfalls

- **Folding `1 / 0` into a compile-time error.** The division may sit on a path that never runs. The folder must leave it, or replace it by an explicit trap with the same effect. Only a language rule can make it an error.
- **Using host arithmetic.** Division, remainder, shifts, overflow and floating-point rounding differ between languages and machines. A cross compiler must emulate the target.
- **Shifts by large counts.** In C a shift by the word size or more is undefined. Many machines take the count modulo the word size, so a folder that computes `1 << 32` as $2^{32}$ for a 32-bit target gives a value that the hardware never produces.
- **Identities that remove traps.** $x \cdot 0 \to 0$ is safe for integers, but $0 / x \to 0$, $x \% x \to 0$ and $x / x \to 1$ remove a trap when $x = 0$.
- **Folding a load.** A load from a global constant can be folded only if no code can change that memory, for example a read-only data section.

## Exercises

1. Fold `q = -7 / 2` and `r = -7 % 2` with the toy IR rules. *Answer.* $q = -3$ and $r = -1$, because $-7 - 2 \cdot (-3) = -1$. Python's `-7 // 2` and `-7 % 2` give $-4$ and $1$.
2. Which of these may a folder rewrite for integers in the toy IR: $x \cdot 0 \to 0$, $x \% 1 \to 0$, $0 \% x \to 0$, $x \ll 0 \to x$? *Answer.* All but $0 \% x \to 0$, which removes the trap at $x = 0$. The divisor 1 and the shift count 0 never trap.
3. A block holds `a = 5`, `a = a - 5`, `b = 10 / a`. What does a correct folder produce? *Answer.* `a = 5`, `a = 0`, and `b = 10 / 0` stays, or `b = 10 / a` stays. The division traps at run time, so it must not be folded and must not be removed.
4. Show that the folder can be run again on its own output without change. *Answer.* After one pass, every instruction with two known constant operands and no trap is a `const`. A second pass computes the same map $K$, because a `const` with value $v$ sets $K[x] = v$ as the folded original did, so it finds nothing new.

## References
