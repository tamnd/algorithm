---
tag: ZBD1SF
kind: theorem
slug: ram-turing-equivalence
name: RAM and Turing machine equivalence
aliases:
- RAM simulates Turing machine
- Turing machine simulates RAM
area: foundations/models-of-computation
level: core
summary: Polynomial-time simulations exist in both directions, so polynomial-time classes are robust to the choice of model.
prereqs: [random-access-machine, multitape-turing-machine, logarithmic-cost-model]
see_also: [turing-machine, unit-cost-model, word-ram, polynomial-time, p, church-turing-thesis, multitape-simulation-theorem]
sources:
  - title: Alfred V. Aho, John E. Hopcroft and Jeffrey D. Ullman, The Design and Analysis of Computer Algorithms, Addison-Wesley, 1974
    locator: Chapter 1, the sections on the cost of RAM programs and on the relation between the Turing machine and the RAM
  - title: Stephen A. Cook and Robert A. Reckhow, Time-bounded random access machines, Journal of Computer and System Sciences 7(4), 1973
    locator: pp. 354 to 375
  - book: isbn:9780201530827
    title: Christos H. Papadimitriou, Computational Complexity, Addison-Wesley, 1994
    locator: Chapter 2, the section on random access machines
  - title: J. Hartmanis and J. Simon, On the power of multiplication in random access machines, 15th Annual Symposium on Switching and Automata Theory, 1974
    locator: the theorem that polynomial time with multiplication and Boolean instructions equals PSPACE
  - title: J. C. Shepherdson and H. E. Sturgis, Computability of recursive functions, Journal of the ACM 10(2), 1963
    locator: pp. 217 to 255
  - title: C. C. Elgot and A. Robinson, Random-access stored-program machines, an approach to programming languages, Journal of the ACM 11(4), 1964
    locator: pp. 365 to 399
  - title: Peter van Emde Boas, Machine models and simulations, in Handbook of Theoretical Computer Science, volume A, 1990
    locator: Chapter 1, the invariance thesis
---

A random-access machine with the logarithmic cost rule and a multitape Turing machine can simulate each other with a polynomial loss of time. A RAM program of logarithmic-cost time $t(n)$ runs on a multitape machine in $O(t(n)^2)$ steps, and a multitape machine of time $T(n)$ runs on a RAM in $O(T(n) \log T(n))$ logarithmic-cost time. So the class [P](/p/) is the same on both models. The result fails for a RAM with unit-cost multiplication, where repeated squaring builds a number with exponentially many bits in a linear number of steps.

## Statement

The RAM is the machine of the [random-access machine](/random-access-machine/) page, with the instructions `LOAD`, `STORE`, `ADD`, `SUB` (with the operands $=c$, $i$ and $*i$), `READ`, `JUMP`, `JZERO`, `JEOF` and `HALT`. It has no multiplication. A **RAM decides** a language $L \subseteq \{0,1\}^*$ if, on every input word $w \in \{0,1\}^*$, given as the $|w|$ integers $w_1, \ldots, w_{|w|}$ in order, it halts, and it halts with $R_0 = 1$ if $w \in L$ and with $R_0 = 0$ if $w \notin L$. Its **time** is the logarithmic cost of the run (the table of the RAM page), and the time $t(n)$ is the largest time over the words of length $n$. The Turing machine is the deterministic $k$-tape machine of the [multitape Turing machine](/multitape-turing-machine/) page, and its time is the number of steps.

**Theorem.**

1. **RAM by Turing machine.** Let a RAM program $P$ decide $L$ in time $t(n)$. Then a deterministic 5-tape Turing machine decides $L$ in time $O(t(n)^2)$. The constant depends on $P$ only.
2. **Turing machine by RAM.** Let a deterministic multitape machine $M$ decide $L$ in time $T(n)$ with $T(n) \ge \max(n, 2)$. Then a RAM program decides $L$ in logarithmic-cost time $O(T(n) \log T(n))$ and in unit-cost time $O(T(n))$. The constants depend on $M$ only.
3. **Unit cost without multiplication.** Let a RAM program decide $L$ in unit-cost time $t(n)$. Then it decides $L$ in logarithmic-cost time $O(t(n)^2)$, and a multitape machine decides $L$ in time $O(t(n)^4)$.
4. **Corollary.** The languages decided in polynomial time are the same for the multitape machine, for the logarithmic-cost RAM and for the unit-cost RAM without multiplication.

The statement is about decision problems with the input read in order, as the RAM page defines it.

## In plain words

A real computer reaches any memory cell in one step. A Turing machine must walk along its tape. The theorem says the computer is not much faster, in the sense that matters for polynomial time.

To copy a computer on a Turing machine, keep a list of every cell written, with its number and value. To read a cell, scan the list. The list is no longer than the work done, so the run costs about the square.

To copy a Turing machine on a computer, keep the tape in memory and the head position in a register. Each tape step takes a fixed number of instructions.

Two conditions are needed. Instruction cost must count the digits of numbers, and multiplication must not be a single fast step, because a few multiplications build a number too long to write.

## Proof

The two parts have complete proofs in separate files.

- Part 1 is proved in [the proof of the simulation of a RAM](proofs/ram-by-tm.md). The Turing machine stores the registers that the RAM has written as a list of pairs (address, value) on one tape. A step of the RAM scans this list. The list has length $O(t)$ by the cost rule, there are at most $t$ steps, and every other operation costs at most the logarithmic cost of the instruction. This gives $O(t^2)$.
- Part 2 is proved in [the proof of the simulation of a Turing machine](proofs/tm-by-ram.md). The RAM stores the cell $c$ of tape $i$ in the register $B + kc + (i-1)$ for a constant $B$, and it keeps the head positions in $k$ registers. Each step of $M$ costs a constant number of instructions, each of cost $O(\log T)$.

*Proof of part 3.* Let $V$ be the larger of $2$ and the largest number that occurs in the text of the program (operand constants and register numbers). After $s$ executed instructions, every register and the accumulator hold a value of at most $2^s V$. This is true for $s = 0$, since all values are $0$. Each instruction creates a value that is an input bit (at most $1$), a constant of the program (at most $V$), a copy of a value that exists, or a sum of two values that exist, which is at most twice the larger one; a difference is not larger than the minuend. So the bound holds for $s + 1$. Every number that an instruction uses (a constant, a register number or a register value) is a constant of the program or a value of a register or the accumulator. It has therefore at most $t + \lg V + 1$ bits. An instruction costs at most four such lengths, so it costs $O(t)$ in the logarithmic-cost rule, and the run costs $O(t^2)$ in all. Part 1 then gives a multitape machine with $O((t^2)^2) = O(t^4)$ steps. $\blacksquare$

*Proof of part 4.* Write $\mathrm{TM}$, $\mathrm{LOG}$ and $\mathrm{UNIT}$ for the three classes of languages decided in polynomial time. Part 1 gives $\mathrm{LOG} \subseteq \mathrm{TM}$, since a polynomial of a polynomial is a polynomial. A machine that halts within $p(n)$ steps also halts within $T(n) = p(n) + n + 2$ steps, which is a polynomial with $T(n) \ge \max(n, 2)$. So part 2 gives $\mathrm{TM} \subseteq \mathrm{LOG}$ and $\mathrm{TM} \subseteq \mathrm{UNIT}$. Part 3 gives $\mathrm{UNIT} \subseteq \mathrm{LOG}$. So $\mathrm{TM} \subseteq \mathrm{UNIT} \subseteq \mathrm{LOG} \subseteq \mathrm{TM}$, and the three classes are equal. $\blacksquare$

## Consequences

- The class [P](/p/) does not depend on the choice among the multitape machine and the RAM with logarithmic cost. This is the reason that [polynomial time](/polynomial-time/) is the usual meaning of "efficient" for both models.
- An algorithm analysed on the unit-cost RAM with addition and subtraction, with an input of bits, runs on a Turing machine in a time polynomial in its unit-cost time, with the exponent 4 of part 3. So a polynomial bound on the RAM is a polynomial bound in the other models.
- The two models compute the same functions, which supports the [Church-Turing thesis](/church-turing-thesis/).
- The theorem does not transfer exact bounds. A linear-time RAM algorithm is not a linear-time Turing machine algorithm. The [word RAM](/word-ram/) bounds in particular do not carry over by a constant factor.

## Tightness

**Unit-cost multiplication.** Add the instruction `MULT X` ($R_0 \leftarrow R_0 \cdot v$) at unit cost. The program below reads $k$ ones and halts with $R_0 = 2^{2^k}$.

```text
1   LOAD =2
2   STORE 1
3   JEOF 9
4   READ
5   LOAD 1
6   MULT 1
7   STORE 1
8   JUMP 3
9   LOAD 1
10  HALT
```

Each pass through lines 3 to 8 squares $R_1$, so after $k$ passes $R_1 = 2^{2^k}$. The unit-cost time is $6k + 5$. The number $2^{2^k}$ has $2^k + 1$ bits, and a Turing machine that writes it makes at least $2^k + 1$ steps. So no simulation of the unit-cost RAM with multiplication can run in time polynomial in the unit-cost time, for the task of computing the output number. This is the reason for the logarithmic cost rule. For decision problems, Hartmanis and Simon (1974) showed that polynomial time on a unit-cost RAM with multiplication and bitwise Boolean instructions equals [PSPACE](/pspace/). So the class P is not robust under that machine unless P equals PSPACE.

**Logarithmic cost with multiplication.** The same simulation, with the school method for the product, takes $O(a b)$ steps for numbers of $a$ and $b$ bits, which is at most the square of the cost of the instruction. Since the sum of the squares of costs $c_s$ with $\sum c_s \le t$ is at most $t^2$, the bound $O(t^2)$ of part 1 still holds. The proof file does not treat this instruction.

**Input in registers.** Suppose that the input $w_1 \cdots w_n$ is in $R_1, \ldots, R_n$ and that $R_0 = n$. Then the RAM reads the last symbol $w_n$ in $O(\log n)$ cost, but a Turing machine needs at least $n - 1$ steps to decide the language of the words with last symbol $1$, since its head must reach the last cell. Part 1 is false in that convention. The sequential input removes this effect. If $t(n) \ge n \lg n$, the Turing machine can write the $n$ input registers as a list in time $O(n \log n)$, the list adds $O(n \log n) = O(t)$ to its length, and the bound of part 1 is $O(t^2)$ again.

**Exponent.** The exponent 2 of part 1 comes from one scan of the list for each instruction. It is not known to be optimal for this simulation.

## History

The RAM was studied by Shepherdson and Sturgis (1963) and by Elgot and Robinson (1964), and the time-bounded RAM with the unit and the logarithmic cost rules is in Cook and Reckhow (1973). Cook and Reckhow (1973) and Aho, Hopcroft and Ullman (1974, Chapter 1) give the simulations between the RAM and the Turing machine. The proofs on this page use the accumulator machine of Aho, Hopcroft and Ullman without `MULT` and `DIV`, with sequential input. The invariance thesis (Slot and van Emde Boas, 1984; see van Emde Boas 1990) says that reasonable machines simulate each other with a polynomial loss of time and a constant factor of space.

## References
