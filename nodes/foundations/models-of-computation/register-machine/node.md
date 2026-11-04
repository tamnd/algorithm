---
tag: 3AR7TQ
kind: model
slug: register-machine
name: Register machine
aliases:
- Minsky machine
- counter machine
- two-counter machine
area: foundations/models-of-computation
level: advanced
summary: Machine with a finite program and unbounded registers; with two counters it is Turing-complete.
prereqs: [turing-machine]
see_also: [random-access-machine, ram-turing-equivalence, church-turing-thesis, halting-problem, lambda-calculus, unit-cost-model]
sources:
  - title: "Marvin L. Minsky, Recursive unsolvability of Post's problem of 'Tag' and other topics in theory of Turing machines, Annals of Mathematics 74(3), 1961"
    locator: pp. 437 to 455, the two-counter result
  - title: Richard Schroeppel, A two counter machine cannot calculate 2^N, MIT Artificial Intelligence Laboratory Memo 257, 1972
    locator: the whole memo
  - title: John C. Shepherdson and Howard E. Sturgis, Computability of recursive functions, Journal of the ACM, volume 10, issue 2, 1963
    locator: pp. 217 to 255
  - title: "Marvin L. Minsky, Computation: Finite and Infinite Machines, Prentice-Hall, 1967"
    locator: Chapter 11, models similar to digital computers
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Chapter 3, the Church-Turing thesis, for the Turing machine side of the equivalence
---

A register machine is a model of computation with a finite program and a finite number of registers, each of which holds a natural number of any size. A step adds one to a register, subtracts one from it, or jumps if a register is zero. Shepherdson and Sturgis (1963) showed that such machines compute exactly the partial recursive functions, and Minsky (1961) showed that two registers are enough. When the registers are used only as counters, the machine is also called a counter machine or a Minsky machine. It is one of the simplest Turing-complete models, and its memory is a few numbers instead of a tape.

## The machine

A register machine has registers $R_1, \ldots, R_k$, each holding a value in $\mathbb{N} = \{0, 1, 2, \ldots\}$, and a program $P = (I_0, I_1, \ldots, I_{m-1})$ of instructions. Each instruction is one of these:

- $\mathrm{INC}\ r$: set $R_r \leftarrow R_r + 1$, and go to the next instruction;
- $\mathrm{DEC}\ r$: set $R_r \leftarrow \max(R_r - 1, 0)$, and go to the next instruction;
- $\mathrm{JZ}\ r, j$: if $R_r = 0$, go to instruction $j$, else go to the next instruction;
- $\mathrm{JMP}\ j$: go to instruction $j$;
- $\mathrm{HALT}$: stop.

A **configuration** is a tuple $(c, v_1, \ldots, v_k)$ with the program counter $c \in \{0, \ldots, m-1\}$ and the register values $v_i$. The start configuration has $c = 0$, the input values in the first registers and $0$ in all others. One **step** executes the instruction $I_c$ as above. The machine halts when $I_c$ is $\mathrm{HALT}$. It **computes** a partial function $f : \mathbb{N}^a \to \mathbb{N}$ if, started with the arguments in $R_1, \ldots, R_a$, it halts exactly when $f$ is defined, and then $R_1$ holds $f(x_1, \ldots, x_a)$. The jump $\mathrm{JMP}$ is a $\mathrm{JZ}$ on a register that is never changed, if the machine has such a register. It is a separate instruction so that two registers suffice in the result below. A *two-counter machine* has $k = 2$.

Many texts merge the three basic operations into two: $\mathrm{INC}\ r$ and the test-and-decrement $\mathrm{DECJZ}\ r, j$ (if $R_r = 0$ go to $j$, else decrement and continue), with an explicit successor in each instruction. The models are equivalent, with a constant factor in time.

**Example: addition.** The program below, for registers $R_1$ (the number $a$) and $R_2$ (the number $b$), sets $R_1 \leftarrow a + b$ and $R_2 \leftarrow 0$.

| Instruction | Meaning |
|---|---|
| $I_0$: $\mathrm{JZ}\ 2, 4$ | if $R_2 = 0$ go to $I_4$ |
| $I_1$: $\mathrm{DEC}\ 2$ | $R_2 \leftarrow R_2 - 1$ |
| $I_2$: $\mathrm{INC}\ 1$ | $R_1 \leftarrow R_1 + 1$ |
| $I_3$: $\mathrm{JMP}\ 0$ | go to $I_0$ |
| $I_4$: $\mathrm{HALT}$ | stop |

Here is the run on $a = 3$ and $b = 2$. The columns give the configuration after each step.

| steps done | $c$ | $R_1$ | $R_2$ |
|---|---|---|---|
| 0 | 0 | 3 | 2 |
| 1 | 1 | 3 | 2 |
| 2 | 2 | 3 | 1 |
| 3 | 3 | 4 | 1 |
| 4 | 0 | 4 | 1 |
| 5 | 1 | 4 | 1 |
| 6 | 2 | 4 | 0 |
| 7 | 3 | 5 | 0 |
| 8 | 0 | 5 | 0 |
| 9 | 4 | 5 | 0 |

Each pass of the loop takes $4$ steps and moves one unit from $R_2$ to $R_1$. So the program takes $4b + 1$ steps before it halts, which is $9$ for $b = 2$.

## What it counts

The time is the number of steps before the machine halts. A step costs one unit, whatever the values of the registers are. Only $\mathrm{INC}$ makes a value larger, and it adds $1$. So after $t$ steps, every register holds at most $s + t$, where $s$ is the largest starting value. Two consequences follow. A machine that outputs $y$ from small inputs needs at least $y - s$ steps. So the time is measured against the value of the numbers and not against their length in bits. To write the number $2^n$ from small inputs, the machine needs at least $2^n - s$ steps, while a machine that can add two registers in one step needs about $n$ steps. The model has no such addition, and the addition of two registers costs a number of steps proportional to the value of one of them ($4b + 1$ in the example).

The space is the number of registers, which is fixed by the program, together with the size of the values. The size of a value $v$ is $\lceil \lg (v+1) \rceil$ bits. A machine has no way to address a register by the content of another register. This is the difference with the [random-access machine](/random-access-machine/), where a register can be chosen at run time.

## Relation to other models

The [random-access machine](/random-access-machine/) adds indirect addressing, more instructions, and in some versions arithmetic on whole numbers in one step. The [unit-cost model](/unit-cost-model/) and the [logarithmic cost model](/logarithmic-cost-model/) are two ways to charge those steps. [RAM and Turing machine equivalence](/ram-turing-equivalence/) shows that the RAM and the [Turing machine](/turing-machine/) compute the same functions. The register machine of this page computes the same functions, but its steps are much weaker than those of the RAM.

The [Turing machine](/turing-machine/) keeps its data on a tape in a finite alphabet. A register machine keeps a number. The two links between them are the Shepherdson and Sturgis theorem below, and the encoding of a tape as a pair of numbers: the cells to the left of the head as a number in base $b$, the cells to the right as a second number in base $b$, with $b$ the size of the alphabet. A move of the head is then a multiplication by $b$ of one number and a division by $b$ of the other, and both are loops of $\mathrm{INC}$ and $\mathrm{DEC}$ that use a third register.

## Known results in the model

- **Turing completeness (Shepherdson and Sturgis, 1963).** Register machines with the instructions above, with as many registers as the program needs, compute exactly the partial recursive functions. So they compute exactly the functions that a [Turing machine](/turing-machine/) computes, and the [Church-Turing thesis](/church-turing-thesis/) applies to them.
- **Two counters suffice (Minsky, 1961).** For every partial computable function $f : \mathbb{N} \to \mathbb{N}$ there is a two-counter machine that, started with $(2^n, 0)$, halts if and only if $f(n)$ is defined, and then holds $(2^{f(n)}, 0)$. The proof is below.
- **The coding is needed.** With the input $n$ given directly, no two-counter machine computes $2^n$ (Schroeppel, 1972). So two counters are universal only up to this exponential coding of inputs and outputs.
- **One counter does not suffice.** A machine with one register and a finite program is not Turing complete. It is a one-counter automaton (a pushdown automaton with one stack symbol and a bottom marker), and its halting problem is decidable.
- **Undecidability.** The halting problem for two-counter machines is undecidable. Every Turing machine is simulated by a register machine (Shepherdson and Sturgis), and that machine by a two-counter machine (by the theorem below). So the [halting problem](/halting-problem/) for two-counter machines is undecidable, because it is undecidable for Turing machines.
- **Cost of the reduction.** The theorem below makes each simulated step cost time proportional to the current value of $X$, and $X$ is exponential in the values of the simulated registers. So the two-counter machine is far slower than the machine that it simulates.

**Theorem (Minsky).** Let $M$ be a register machine with $k$ registers and let $p_1 = 2, p_2 = 3, p_3 = 5, \ldots, p_k$ be the first $k$ primes. There is a two-counter machine $M'$ such that for all $v_1, \ldots, v_k \in \mathbb{N}$: if $M$ started in $(0, v_1, \ldots, v_k)$ halts with the values $(v_1', \ldots, v_k')$, then $M'$ started with $X = p_1^{v_1} \cdots p_k^{v_k}$ and $Y = 0$ halts with $X = p_1^{v_1'} \cdots p_k^{v_k'}$ and $Y = 0$, and if $M$ does not halt, $M'$ does not halt.

*Proof.* The counters of $M'$ are $X$ and $Y$. We keep the invariant that after the simulation of $s$ steps of $M$, the program counter of $M'$ is at the first instruction of the code for the instruction of $M$ that is next, $Y = 0$, and $X = \prod_i p_i^{R_i}$ for the current registers $R_i$ of $M$. The invariant holds at the start by the choice of the input. We give the code for each instruction. Let $p = p_r$.

- *$\mathrm{INC}\ r$.* Repeat while $X \ne 0$: decrement $X$ once, then increment $Y$ $p$ times. Then repeat while $Y \ne 0$: decrement $Y$ and increment $X$. Now $X$ is $p$ times the old value, which is $\prod_i p_i^{R_i}$ with $R_r$ increased by $1$, and $Y = 0$.
- *Divisibility test.* Since $X \ge 1$ and the $p_i$ are distinct primes, unique factorization gives $p \mid X$ if and only if $R_r \ge 1$. Repeat this: try to decrement $X$ for $p$ times in a row, checking for $X = 0$ before each decrement. If all $p$ decrements work, increment $Y$ and repeat. If $X$ is $0$ before the first of the $p$ decrements, then $p \mid X$, $Y$ holds $X/p$ and $X = 0$. If $X$ is $0$ before the $u$-th decrement with $2 \le u \le p$, then the remainder is $u - 1$ and $Y$ holds the quotient $q$. The code knows $u$ by its position, so it needs no further counter.
- *$\mathrm{DEC}\ r$.* Do the divisibility test. If $p \mid X$, move $Y$ into $X$, which makes $X$ the old value divided by $p$. If not, restore $X = pq + (u-1)$ by adding $u - 1$ to $X$ and then moving $Y$ into $X$ with $p$ added for each unit of $Y$. In the first case $R_r$ drops by $1$ as the instruction says, and in the second case $R_r = 0$ stays.
- *$\mathrm{JZ}\ r, j$.* Do the divisibility test and restore $X = pq$ or $X = pq + (u-1)$ in the same way. Go to the code of $I_{c+1}$ if $p \mid X$ and to the code of $I_j$ otherwise.
- *$\mathrm{JMP}\ j$, $\mathrm{HALT}$.* $\mathrm{JMP}\ j$ becomes a jump to the first instruction of the code of $I_j$, and $\mathrm{HALT}$ is copied. The code does not touch $X$ or $Y$.

Each loop in the code of an instruction decrements $X$ or $Y$ in every pass, so the code of one instruction always ends. After it, the second counter is $0$ again, so the invariant holds. It follows by induction on $s$ that after $s$ steps of $M$ the code of $M'$ is at the right place with the right $X$. When $M$ halts, $M'$ halts with the stated $X$, and when $M$ runs forever, $M'$ runs forever. $\square$

To get the claim for $f$, take a register machine for $f$ (Shepherdson and Sturgis) that has the argument in $R_1$, that ends with $f(n)$ in $R_1$, and that sets $R_2, \ldots, R_k$ to zero before it halts, each with a loop of $\mathrm{DEC}$. The input $(n, 0, \ldots, 0)$ gives $X = 2^n$.

As an example, the addition program above, translated, halts with $X = 2^{a+b}$ when it starts with $X = 2^a 3^b$. For $a = b = 3$, the original takes $13$ steps. Each simulated step of the translation costs time proportional to $X$, which starts at $2^3 \cdot 3^3 = 216$.

## References
