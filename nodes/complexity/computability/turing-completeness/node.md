---
tag: RP2K30
kind: concept
slug: turing-completeness
name: Turing completeness
aliases:
- Turing-complete
- computational universality
area: complexity/computability
level: core
summary: A system is Turing complete if it can simulate every Turing machine, so it computes every partial computable function. Its halting problem is then undecidable.
prereqs: [turing-machine, universal-turing-machine]
see_also: [church-turing-thesis, universal-turing-machine, lambda-calculus, register-machine, cellular-automaton, post-canonical-system, combinatory-logic, halting-problem]
sources:
  - paper: doi:10.1112/plms/s2-42.1.230
    title: Alan M. Turing, On computable numbers, with an application to the Entscheidungsproblem, Proceedings of the London Mathematical Society (2) 42 (1936)
    locator: pp. 230 to 265, Sections 6 and 7 (the universal computing machine)
  - paper: doi:10.2307/2268280
    title: Alan M. Turing, Computability and lambda-definability, Journal of Symbolic Logic 2(4) (1937)
    locator: pp. 153 to 163
  - paper: doi:10.2307/1970290
    title: Marvin L. Minsky, Recursive unsolvability of Post's problem of "Tag" and other topics in theory of Turing machines, Annals of Mathematics 74(3) (1961)
    locator: pp. 437 to 455 (tag systems and machines with two counters are universal)
  - paper: doi:10.1007/978-1-4612-4808-8_2
    title: John H. Conway, FRACTRAN, a simple universal programming language for arithmetic, in T. M. Cover and B. Gopinath (eds.), Open Problems in Communication and Computation, Springer, 1987
    locator: pp. 4 to 26
  - paper: doi:10.25088/complexsystems.15.1.1
    title: Matthew Cook, Universality in elementary cellular automata, Complex Systems 15(1) (2004)
    locator: pp. 1 to 40 (rule 110 is universal)
  - title: Elwyn R. Berlekamp, John H. Conway and Richard K. Guy, Winning Ways for your Mathematical Plays, Volume 2, Academic Press, 1982
    locator: Chapter 25, What is Life? (a universal computer in the Game of Life)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 3.2, Variants of Turing machines; Section 3.3, The definition of algorithm
---

A system of computation is Turing complete if it can simulate every [Turing machine](/turing-machine/). It then computes every partial [computable function](/computable-function/), once inputs and outputs are put in a suitable code. One simulation is enough: a system that can simulate a [universal Turing machine](/universal-turing-machine/) can simulate all of them. Turing completeness is a property of one system, which can be proved. The [Church-Turing thesis](/church-turing-thesis/) is a different claim: that no mechanical method computes more than a Turing machine. Together they say that a Turing complete system computes exactly what can be computed. A Turing complete system also inherits the [halting problem](/halting-problem/), so questions about its long-run behavior are undecidable.

## In plain words

A Turing complete system can run any program that any computer can run, if it gets enough memory and time. It may be very slow and very strange. It may store numbers as stones in heaps, or as patterns of cells on a grid. The rules can be tiny, as long as they let you copy, test and repeat without a fixed limit.

Many systems are Turing complete by accident: card games, puzzles, simple cell rules. To prove it, you show how the system copies the work of a machine that is already known to be complete.

There is a cost. In a Turing complete system you cannot always tell in advance whether a run will stop. Designers who want every program to finish must remove some power, for example by only allowing loops with a fixed count.

## The idea

**Definition.** A model of computation $S$ is *Turing complete* if for every Turing machine $M$ there is a program or start configuration of $S$ that simulates $M$. Inputs of $M$ are put into the code of $S$, and the result is read back, by encodings that are computable and much simpler than the computation itself. The system is *Turing equivalent* if, in addition, a Turing machine can simulate $S$. For discrete systems with explicit rules the second half is usually easy, so in practice the two words mean the same thing.

**Proof method.** Nobody proves completeness from scratch. One shows that $S$ simulates a model that is already known to be complete, often a weak one that is easy to build:

- [Lambda calculus](/lambda-calculus/) and the general recursive functions compute the same functions as Turing machines (Turing 1937), and so does [combinatory logic](/combinatory-logic/).
- A [register machine](/register-machine/) with only two counters, which can add one, subtract one and test for zero, is universal if the input $x$ is given as $2^x$ (Minsky 1961).
- Tag systems with deletion number 2 are universal (Minsky 1961). They are a special case of [Post canonical systems](/post-canonical-system/).
- Cyclic tag systems simulate tag systems, and the elementary [cellular automaton](/cellular-automaton/) rule 110 simulates cyclic tag systems (Cook 2004).
- [Markov algorithms](/markov-algorithm/) and [string rewriting systems](/string-rewriting-system/) simulate Turing machines directly, one rule per transition.

**The encodings must stay honest.** If the encoding of inputs could do any computation, then any system would look complete. The usual rule is that the encodings must be computable by a much weaker device, such as a finite-state transducer or a primitive recursive map. Some proofs also need an infinite but simple start: Cook's proof for rule 110 uses an infinite background pattern that repeats with a fixed period on each side.

**Unbounded memory.** A real computer has a fixed amount of memory, so in the strict sense it is a finite automaton. When people call a programming language Turing complete, they mean the abstract language, with unbounded integers, an unbounded heap or an unbounded tape. A language with only fixed-width integers and no growing storage has finitely many states, and its halting problem is decidable by loop detection.

**Termination costs completeness.** A language in which every program halts cannot be Turing complete. Suppose its programs are $p_0, p_1, \ldots$ and its interpreter $\mathrm{eval}(p, x)$ is computable. Then $f(n) = \mathrm{eval}(p_n, n) + 1$ is a total computable function, but $f$ differs from each $p_n$ at input $n$, so no program of the language computes it. This is the [diagonalization argument](/diagonalization-argument/). The LOOP language, in which each loop runs a number of times fixed when the loop starts, computes exactly the [primitive recursive functions](/primitive-recursive-function/), and so it cannot compute the [Ackermann function](/ackermann-function/).

**What completeness implies.** If $S$ is Turing complete by computable encodings, then $\mathrm{HALT}$ many-one reduces to the halting problem of $S$: map $\langle M, w \rangle$ to the program of $S$ that simulates $M$ on $w$. So "does this run of $S$ stop?" is undecidable, and by [Rice's theorem](/rice-theorem/) so is every nontrivial question about the function a program of $S$ computes.

## Examples

**FRACTRAN.** A FRACTRAN program is a list of fractions. Start with a positive integer $n$. At each step, multiply $n$ by the first fraction in the list that gives an integer. Stop when no fraction does. The exponents of the primes in $n$ act as registers: a fraction $p/q$ applies only if $q$ divides $n$, which tests that some registers are nonzero, and multiplying by it subtracts from the registers in $q$ and adds to those in $p$. Conway showed that FRACTRAN can simulate any counter machine, so it is Turing complete.

The program
$$\tfrac{455}{33},\ \tfrac{11}{13},\ \tfrac{1}{11},\ \tfrac{3}{7},\ \tfrac{11}{2},\ \tfrac{1}{3}$$
multiplies. Started on $2^a 3^b$, it stops at $5^{ab}$. The primes $7$, $11$ and $13$ act as markers for the state of the loop. Started on $2^2 \cdot 3^3 = 108$, it stops after $25$ steps at $5^6 = 15625$. Started on $2^3 \cdot 3^4 = 648$, it stops after $46$ steps at $5^{12}$.

**The Game of Life.** Conway's Game of Life is a two-dimensional cellular automaton with two cell states. Berlekamp, Conway and Guy showed how to build a universal computer in it: streams of gliders carry bits, and collisions between them act as logic gates and as memory. So the question "does this starting pattern eventually die out?" is undecidable.

**Rule 110.** This one-dimensional automaton has two cell states, and the new state of a cell depends only on itself and its two neighbors. Cook (2004) proved that it simulates cyclic tag systems, so it is Turing complete with an infinite periodic background.

**Non-examples.**

- Finite automata and regular expressions have a fixed amount of memory.
- Pushdown automata have a single stack. They decide [context-free languages](/context-free-grammar/), and their emptiness problem is decidable. Two stacks are enough to simulate a tape, so a machine with two stacks is Turing complete.
- The LOOP language and other languages with only bounded loops compute primitive recursive functions only.
- The core languages of proof assistants such as Coq and Agda accept only functions that they can show to terminate. By the diagonal argument above, they miss some total computable functions.

## Where it is used

- **Undecidability proofs.** To show that a question about a system is undecidable, show that the system is Turing complete. This is how the [Post correspondence problem](/post-correspondence-problem/), [Hilbert's tenth problem](/hilberts-tenth-problem/) and the [Wang tiling problem](/wang-tiling-problem/) were shown undecidable: each one can encode the runs of a Turing machine.
- **Language design.** Query languages, configuration languages and proof assistants are often made weaker on purpose so that every program halts, or so that some analysis stays decidable.
- **Program analysis.** For any Turing complete language, exact static analysis of termination or of the computed function is impossible, so practical tools are sound and incomplete.
- **Small universal machines.** Research asks how small a universal system can be: few states and symbols for a Turing machine, few counters for a register machine, or a tiny rule table for a cellular automaton.

## References
