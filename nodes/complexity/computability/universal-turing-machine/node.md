---
tag: YZTPVT
kind: model
slug: universal-turing-machine
name: Universal Turing machine
aliases:
- UTM
- universal machine
area: complexity/computability
level: core
summary: A Turing machine U that takes the code of any machine M and an input w, and simulates M on w. It is the theory's stored-program computer, and its language is the acceptance problem.
prereqs: [turing-machine, godel-numbering]
see_also: [turing-machine, godel-numbering, acceptance-problem, halting-problem, multitape-turing-machine, time-hierarchy-theorem, kolmogorov-complexity, turing-completeness]
sources:
  - paper: doi:10.1112/plms/s2-42.1.230
    title: Alan M. Turing, On computable numbers, with an application to the Entscheidungsproblem, Proceedings of the London Mathematical Society (2) 42 (1936)
    locator: pp. 230 to 265, Section 6, The universal computing machine, and Section 7, Detailed description of the universal machine
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Chapter 1 (machines as strings, the universal Turing machine and its efficient form with O(T log T) overhead)
  - paper: doi:10.1145/321356.321362
    title: Frederick C. Hennie and Richard E. Stearns, Two-tape simulation of multitape Turing machines, Journal of the ACM 13(4) (1966)
    locator: pp. 533 to 546
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 9.2 (the universal language and the universal Turing machine)
  - paper: doi:10.1016/S0304-3975(96)00077-1
    title: Yurii Rogozhin, Small universal Turing machines, Theoretical Computer Science 168(2) (1996)
    locator: pp. 215 to 240
  - paper: doi:10.25088/complexsystems.15.1.1
    title: Matthew Cook, Universality in elementary cellular automata, Complex Systems 15(1) (2004)
    locator: pp. 1 to 40
---

A universal Turing machine is a single [Turing machine](/turing-machine/) $U$ that can do the work of every other one. Its input is a pair $\langle M, w \rangle$, the code of a machine $M$ and a word $w$, and $U$ simulates $M$ on $w$ step by step: it accepts if $M$ accepts, rejects if $M$ rejects, and runs forever if $M$ runs forever. Turing described such a machine in his paper of 1936. It is the idea of the stored-program computer, where a program is data on the tape, and it is the starting point of the [halting problem](/halting-problem/), since the language of $U$ is the [acceptance problem](/acceptance-problem/). In complexity theory an efficient universal machine, with only a logarithmic factor of extra time on multitape machines, drives the [hierarchy theorems](/time-hierarchy-theorem/).

## The machine

**Codes.** Fix a computable encoding $M \mapsto \langle M \rangle \in \{0, 1\}^*$ of Turing machines, as on the [Gödel numbering](/godel-numbering/) page: number the states and the tape symbols, write the rule $\delta(q_i, X_j) = (q_k, X_l, D_m)$ as $0^i 1 0^j 1 0^k 1 0^l 1 0^m$, and join the rules with $11$. Write $\langle M, w \rangle$ for the code of $M$, a separator, and the word $w$ with each input symbol written by its code. Every machine has a code. The universal machine below rejects every input that is not a valid pair $\langle M, w \rangle$.

**Definition.** A Turing machine $U$ is *universal* if for every machine $M$ and every input $w$:

- $U$ accepts $\langle M, w \rangle$ if and only if $M$ accepts $w$;
- $U$ rejects $\langle M, w \rangle$ if and only if $M$ rejects $w$;
- $U$ runs forever on $\langle M, w \rangle$ if and only if $M$ runs forever on $w$.

For machines that compute functions, $U$ also leaves the output of $M$ on its tape, in coded form. In terms of indices, $U$ computes the *universal function* $(e, x) \mapsto \varphi_e(x)$ of the [computable functions](/computable-function/).

**A three-tape construction.** $U$ uses three tapes.

1. Tape 1 holds $\langle M \rangle$ and is never changed.
2. Tape 2 holds the tape of $M$, each cell of $M$ written as a block of fixed width $b$, the code of the symbol padded to $b$ bits, where $b$ is the length of the longest symbol code in $\langle M \rangle$.
3. Tape 3 holds the code $0^i$ of the current state $q_i$ of $M$.

At the start, $U$ checks that tape 1 holds a valid code, copies $w$ to tape 2 in block form and writes the code of the start state on tape 3. Then each step of $M$ takes one *round* of $U$:

1. Scan the rules on tape 1 for the one whose state block equals tape 3 and whose symbol block equals the block under the head of tape 2.
2. If none matches, $M$ halts; $U$ halts in the same way. If the new state is the accept or reject state of $M$, $U$ accepts or rejects.
3. Otherwise copy the new state block to tape 3, write the new symbol block on tape 2, and move the head of tape 2 by $b$ cells to the left or right.

A round reads the code of $M$ once and compares blocks whose length is bounded by $|\langle M \rangle|$, so it takes at most $c_M$ steps of $U$, where $c_M$ depends only on $M$ and is bounded by a polynomial in $|\langle M \rangle|$. If $M$ halts on $w$ after $T$ steps, $U$ halts after $O(c_M (T + |w|))$ steps, and uses $b$ cells of tape 2 for each cell that $M$ uses.

**A single tape.** By the [multitape simulation theorem](/multitape-simulation-theorem/), a one-tape machine simulates the three-tape $U$ with a quadratic increase in time. So a one-tape universal machine exists too.

**Worked example.** The machine $M$ of the [Turing machine](/turing-machine/) page decides $\{0^k 1^k : k \ge 0\}$. It has 6 states and 5 tape symbols, and with states and symbols numbered from $1$ its code $\langle M \rangle$ is a word of 219 bits made of 11 rule codes; the first rule, $\delta(q_0, 0) = (q_1, X, R)$, has the 14-bit code $01010010000100$. A universal machine on $\langle M, 0011 \rangle$ runs 13 rounds and accepts, as $M$ accepts $0011$ after 13 steps. On $\langle M, 001 \rangle$ it runs 8 rounds and rejects. An interpreter program that splits the code at each $11$ and counts the zeros in each block is the same algorithm, written in a programming language.

**Turing's version.** Turing's machine of 1936 works on a single tape. It reads the "standard description" of a machine, written as a word over a few letters, and prints the same sequence of digits that the described machine prints. Between the digits it writes out complete configurations of the simulated machine, and it finds the next rule by matching marked parts of the tape. Turing described it in Sections 6 and 7 of his paper.

## What it counts

A universal machine is a Turing machine, so it counts the same resources: steps and tape cells. The question is the *overhead*: how many steps and cells $U$ uses to simulate $T$ steps and $S$ cells of $M$.

| simulated machine | universal machine | time of $U$ | space of $U$ |
|---|---|---|---|
| one tape | three tapes (above) | $O(c_M T)$ | $O(c_M S)$ |
| $k$ tapes | one tape | $O(c_M T^2)$ | $O(c_M S)$ |
| $k$ tapes | two tapes | $O(c_M T \log T)$ | $O(c_M S)$ |

Here $c_M$ depends on $M$ (its number of tapes, states and symbols) but not on $w$, and $T \ge n$. The last row is the efficient universal machine. Hennie and Stearns (1966) showed that two tapes can simulate $k$ tapes with an $O(\log T)$ factor in time, and this gives a universal machine with time $O(c_M T \log T)$; Arora and Barak present it in Chapter 1. For space the overhead is only a constant factor $c_M$, which comes from the coding of the symbols of $M$.

The constant $c_M$ matters only when $M$ grows with the input. In proofs, $M$ is fixed and $w$ grows, so the overhead is a constant factor for space, and a factor of $\log T$ for time.

## Relation to other models

- **Stored-program computers.** In a universal machine the program is data on the tape. A computer that keeps its program in memory, and an interpreter for a programming language, follow the same idea.
- **The universal function.** In the language of [Gödel numberings](/godel-numbering/), the existence of $U$ is the *enumeration theorem*: the function $(e, x) \mapsto \varphi_e(x)$ is partial computable. With the [s-m-n theorem](/s-m-n-theorem/), it is what makes a numbering acceptable, and it is the base of [Kleene's recursion theorem](/kleene-recursion-theorem/).
- **Other general models.** [Register machines](/register-machine/), the [random-access machine](/random-access-machine/) and the [lambda calculus](/lambda-calculus/) each have a universal program, an interpreter written in the model for the model. A system that can simulate a universal machine is [Turing complete](/turing-completeness/).
- **Small universal machines.** Universal machines can be very small. Rogozhin (1996) built universal machines with these numbers of states and symbols: $(24, 2)$, $(10, 3)$, $(7, 4)$, $(5, 5)$, $(4, 6)$, $(3, 10)$ and $(2, 18)$. They simulate 2-tag systems, which in turn simulate Turing machines, so the input must first be coded as a tag system.
- **Cellular automata.** Cook (2004) proved that the elementary [cellular automaton](/cellular-automaton/) rule 110 is universal. The proof needs an initial row that repeats a fixed pattern without end to the left and to the right. This is a weaker form of universality than that of $U$, whose input is finite.
- **Nondeterministic and oracle machines.** A universal [nondeterministic Turing machine](/nondeterministic-turing-machine/) simulates any nondeterministic machine, by the same construction with the choices of $M$ made by $U$. A universal [oracle Turing machine](/oracle-turing-machine/) simulates any oracle machine with the same oracle.

## Known results in the model

- **The language of $U$ is c.e. and not decidable.** $L(U) = \{ \langle M, w \rangle : M \text{ accepts } w \} = A_{\mathrm{TM}}$, the [acceptance problem](/acceptance-problem/). So $A_{\mathrm{TM}}$ is [computably enumerable](/recursively-enumerable-language/). A diagonal argument shows that it is not [decidable](/decidable-language/): no machine can predict, for every $\langle M, w \rangle$, whether $U$ will halt. The set of inputs on which $U$ halts is the [halting problem](/halting-problem/). Both are complete for the c.e. sets under [many-one reductions](/many-one-reducibility/).
- **Hierarchy theorems.** The [time hierarchy theorem](/time-hierarchy-theorem/) uses the efficient universal machine: a machine with time bound $t(n) \log t(n)$ can simulate, and then contradict, each machine with time bound $t(n)$. The [space hierarchy theorem](/space-hierarchy-theorem/) uses the constant space overhead, so its gap is smaller.
- **Kolmogorov complexity.** Let $K_U(x)$ be the length of the shortest program $p$ with $U(p) = x$ for a suitable universal machine $U$. For any other machine $V$ there is a constant $c_V$ with $K_U(x) \le K_V(x) + c_V$ for all $x$. This *invariance theorem* is why [Kolmogorov complexity](/kolmogorov-complexity/) does not depend on the machine, up to an additive constant. [Chaitin's constant](/chaitins-constant/), the halting probability of such a machine, is defined through it.
- **Normal form.** Every partial computable function has the form $\varphi_e(x) = u(\mu y\, T(e, x, y))$ with fixed [primitive recursive](/primitive-recursive-function/) $T$ and $u$, where $T(e, x, y)$ says that $y$ codes a halting computation of machine $e$ on $x$. This is a universal machine written as a formula; see [partial recursive functions](/partial-recursive-function/).
- **Bounded versions.** If $U$ is run for only $t$ steps, the question "does $M$ accept $w$ within $t$ steps" becomes decidable, and with $t$ written in unary it is solvable in time polynomial in the input length. For nondeterministic $M$ the same bounded question is [NP](/np/)-complete.
- **No universal machine for total functions.** No machine computes exactly the total computable functions in the way $U$ computes all partial ones: a total universal function $u(e, x)$ for them would give the total computable function $u(x, x) + 1$, which differs from each $u(e, \cdot)$ at $e$. Universal machines must be able to run forever.

## References
