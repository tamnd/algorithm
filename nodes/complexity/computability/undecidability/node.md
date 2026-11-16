---
tag: XY2YCN
kind: concept
slug: undecidability
name: Undecidability
aliases:
- undecidable problem
- uncomputable problem
area: complexity/computability
level: intro
summary: A decision problem is undecidable if no algorithm halts on every instance with the correct yes or no answer. The halting problem is the first example, and reductions give many more.
prereqs: [decidable-language, countability]
see_also: [decidable-language, halting-problem, diagonalization-argument, many-one-reducibility, rice-theorem, recursively-enumerable-language, countability, godel-incompleteness-theorem]
sources:
  - paper: doi:10.1112/plms/s2-42.1.230
    title: Alan M. Turing, On computable numbers, with an application to the Entscheidungsproblem, Proceedings of the London Mathematical Society (2) 42 (1936)
    locator: pp. 230 to 265, Section 8, Application of the diagonal process, and Section 11, Application to the Entscheidungsproblem
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 4.2, Undecidability; Chapter 5, Reducibility
  - paper: doi:10.1090/S0002-9904-1944-08111-1
    title: Emil L. Post, Recursively enumerable sets of positive integers and their decision problems, Bulletin of the American Mathematical Society 50(5) (1944)
    locator: pp. 284 to 316
  - book: isbn:9783642319327
    title: Robert I. Soare, Turing Computability, Theory and Applications, Springer, 2016
    locator: Chapter 1, Defining Computability, and Chapter 2, Computably Enumerable Sets
---

A decision problem is *undecidable* if no algorithm solves it: no [Turing machine](/turing-machine/) halts on every instance with the correct yes or no answer. In other words, the language of its yes-instances is not a [decidable language](/decidable-language/). By the [Church-Turing thesis](/church-turing-thesis/), the result holds for every programming language and every mechanical method. Turing gave the first examples in 1936, the problem now called the [halting problem](/halting-problem/) among them, and used one to show that the [Entscheidungsproblem](/entscheidungsproblem/) of first-order logic is undecidable. Since then, undecidable problems have been found in logic, algebra, number theory, formal languages, tilings and program analysis.

## In plain words

Some yes-or-no questions cannot be answered by any program, however clever, if the program must always give an answer and always be right. The best known one: given a program and its input, will the program ever stop?

This does not mean that no case can be answered. Many programs clearly stop, and many clearly loop. It means that no single program answers the question correctly for every program and input. Any tool that tries will either give a wrong answer somewhere, or run forever somewhere, or answer "I don't know" somewhere.

Undecidable questions are not rare puzzles. Questions about what a program does, such as whether it ever divides by zero, whether two programs do the same thing, or whether a grammar is ambiguous, are all undecidable in general.

## The idea

### Definition

A *decision problem* is a set of instances, each with the answer yes or no. Under a fixed computable encoding of the instances as words, it is the language $L$ of the yes-instances. The problem is *decidable* if some Turing machine halts on every input and accepts exactly $L$, and *undecidable* otherwise. Equivalently, the characteristic function of $L$ is not a [computable function](/computable-function/).

Undecidability is a property of a problem with infinitely many instances. Every finite set of instances is decidable: a machine can hold a table of the answers. So "is this one program on this one input going to halt" is not undecidable; we may just not know which of two trivial machines answers it.

### Levels of undecidability

An undecidable language can still have one half of an algorithm.

| class | meaning | example |
|---|---|---|
| c.e. but not decidable | a machine accepts exactly the yes-instances, and may run forever on no-instances | the halting problem $\mathrm{HALT}$, $A_{\mathrm{TM}}$ |
| co-c.e. but not decidable | a machine accepts exactly the no-instances | $\overline{\mathrm{HALT}}$, emptiness $E_{\mathrm{TM}}$ |
| neither c.e. nor co-c.e. | no machine confirms either answer | totality $\mathrm{TOT}$, equivalence $\mathrm{EQ}_{\mathrm{TM}}$ |

By Post's theorem a language is decidable if and only if it is both [c.e.](/recursively-enumerable-language/) and co-c.e. The [arithmetical hierarchy](/arithmetical-hierarchy/) and the [Turing degrees](/turing-degrees/) measure how far a problem is from decidable: $\mathrm{HALT}$ is at level $\Sigma_1$, $\mathrm{TOT}$ at level $\Pi_2$, and there are problems at every level.

### Three ways to prove it

1. **Counting.** There are countably many machines and uncountably many languages, so most languages are undecidable ([countability](/countability/)). This proves existence but names no problem.
2. **Diagonalization.** Assume a decider $H$ for the problem and build a machine that does the opposite of what $H$ predicts about it. This gives the first concrete undecidable problems, $A_{\mathrm{TM}}$ and $\mathrm{HALT}$; see the [diagonalization argument](/diagonalization-argument/).
3. **Reduction.** If $A$ is undecidable and $A \le_m B$, a [many-one reduction](/many-one-reducibility/), then $B$ is undecidable: a decider for $B$ composed with the reduction would decide $A$. Almost all known undecidable problems are proved this way, starting from the halting problem. [Rice's theorem](/rice-theorem/) does the reduction once for all nontrivial properties of the language of a machine.

The direction of the reduction matters. To show that $B$ is undecidable, reduce a known undecidable problem *to* $B$. A reduction from $B$ to $\mathrm{HALT}$ only shows that $B$ is no harder than $\mathrm{HALT}$.

### Undecidable is not independent

[Gödel's incompleteness theorem](/godel-incompleteness-theorem/) gives a *single sentence* that a theory such as Peano arithmetic can neither prove nor refute. Undecidability is about an infinite *family* of questions and an algorithm for all of them. The two are linked: if a consistent theory with a decidable set of axioms proved or refuted every arithmetic sentence, a machine could list all proofs until one settles a given sentence, and the set of true arithmetic sentences would be decidable. Since the halting problem reduces to that set, it is not decidable, so some sentences are independent. In the older literature "undecidable sentence" means an independent sentence; this page uses "undecidable" only for problems.

### Bounded versions are decidable

A Turing machine that uses at most $s$ cells of tape has at most $|Q| \cdot s \cdot |\Gamma|^s$ configurations, for $|Q|$ non-halting states and $|\Gamma|$ tape symbols. If it runs longer than this, some configuration repeats, and the machine loops forever. So halting is decidable for machines with a fixed bound on the tape: simulate for that many steps. With $4$ states and $5$ symbols, $s = 4$ cells give $10000$ configurations and $s = 10$ give $390625000$. The count grows exponentially in $s$, so the decision is possible, but not fast. In the same way, "does $M$ halt within $t$ steps" is decidable for every given $t$. Undecidability needs unbounded memory, which real computers approximate.

### What undecidability does not say

- It does not say that every instance is hard. Most instances of an undecidable problem may be easy; what fails is a single method for all of them.
- It does not stop useful tools. A sound analyzer may answer "yes", "no" or "unknown", and [abstract interpretation](/abstract-interpretation/) and termination provers do this. Undecidability says only that such a tool cannot avoid "unknown" (or wrong answers, or running forever) on all inputs.
- It is not about speed. A decidable problem can need any computable amount of time; undecidability is a different, absolute limit.

## Examples

**Machines and programs.** The [halting problem](/halting-problem/), the [acceptance problem](/acceptance-problem/), emptiness, totality and equivalence of Turing machines, and every nontrivial property of the language of a machine ([Rice's theorem](/rice-theorem/)).

**Logic.** The [Entscheidungsproblem](/entscheidungsproblem/): validity of first-order sentences is undecidable ([Church's theorem](/church-theorem/)). Truth in the standard model of arithmetic is not even c.e.

**Number theory.** [Hilbert's tenth problem](/hilberts-tenth-problem/): whether a polynomial equation with integer coefficients has a solution in integers.

**Combinatorics and algebra.** The [Post correspondence problem](/post-correspondence-problem/), the [word problem for groups](/word-problem-for-groups/), and the [Wang tiling problem](/wang-tiling-problem/) of covering the plane with given tiles.

**Formal languages and rewriting.** [Ambiguity](/cfg-ambiguity-undecidable/) and [equivalence](/cfg-equivalence-undecidable/) of context-free grammars, [termination of term rewriting systems](/undecidability-of-termination/), and the [word problem for rewriting systems](/undecidability-of-word-problem/).

**Busy beaver.** The [busy beaver function](/busy-beaver-function/) is not computable, so no algorithm can give, for every $n$, the largest number of steps that a halting $n$-state machine takes on a blank tape. For each fixed $n$ the value is a finite number, so each single value is computable by a trivial machine; what fails is one machine for all $n$.

## Where it is used

- **Program analysis and compilers.** By Rice's theorem, exact answers to questions such as dead code, constant values, [may-alias](/may-alias-undecidability/) or termination are impossible in general. Analyzers therefore approximate, and the [full employment theorem](/full-employment-theorem/) says that no compiler is the best optimizer.
- **Logic and verification.** Undecidability of first-order validity explains why theorem provers are semi-decision procedures, and why automated tools work in decidable fragments such as [Presburger arithmetic](/presburger-arithmetic/) with a [decision procedure](/decision-procedure/).
- **Mathematics.** Reductions from the halting problem show that some questions in algebra, number theory and combinatorics have no uniform answer.
- **Complexity theory.** The diagonal and reduction methods of undecidability, with resource bounds added, give the [hierarchy theorems](/time-hierarchy-theorem/) and the theory of [polynomial-time reductions](/polynomial-time-reduction/).

## References
