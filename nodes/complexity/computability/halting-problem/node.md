---
tag: JFPX09
kind: problem
slug: halting-problem
name: Halting problem
aliases:
- Turing's halting problem
area: complexity/computability
level: intro
summary: Given a Turing machine and an input, decide whether the machine halts on it. The problem is computably enumerable but undecidable, and complete for the c.e. sets.
prereqs: [universal-turing-machine, diagonalization-argument, recursively-enumerable-language]
see_also: [acceptance-problem, undecidability, rice-theorem, many-one-reducibility, busy-beaver-function, universal-turing-machine, turing-jump, termination-proof]
sources:
  - paper: doi:10.1112/plms/s2-42.1.230
    title: Alan M. Turing, On computable numbers, with an application to the Entscheidungsproblem, Proceedings of the London Mathematical Society (2) 42 (1936)
    locator: pp. 230 to 265, Section 8, Application of the diagonal process (no machine decides whether a machine is circle-free), and Section 11
  - title: Martin Davis, Computability and Unsolvability, McGraw-Hill, 1958
    locator: the halting problem, under this name
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 4.2, Undecidability; Chapter 5, Reducibility
  - paper: doi:10.1090/S0002-9904-1944-08111-1
    title: Emil L. Post, Recursively enumerable sets of positive integers and their decision problems, Bulletin of the American Mathematical Society 50(5) (1944)
    locator: pp. 284 to 316 (the set K and its completeness among recursively enumerable sets)
  - book: isbn:9783642319327
    title: Robert I. Soare, Turing Computability, Theory and Applications, Springer, 2016
    locator: Chapter 2, Computably Enumerable Sets
---

The halting problem asks, for a [Turing machine](/turing-machine/) $M$ and an input $w$, whether $M$ halts on $w$ or runs forever. It is the standard example of an [undecidable](/undecidability/) problem: no machine answers it correctly for every $M$ and $w$. Half of it is solvable: a [universal Turing machine](/universal-turing-machine/) can run $M$ on $w$ and report when it halts, so the language is [computably enumerable](/recursively-enumerable-language/). Every c.e. problem reduces to it, and most undecidability proofs start from it. Turing proved the undecidability of a closely related problem in 1936; the name "halting problem" first appears in print in Davis's book of 1958.

## In plain words

Given a program and its input, will the program stop, or will it run forever? For a single program you can often tell, but there is no general method that always gives the right answer.

The reason is a trap of self-reference. Suppose a checker could always answer the question. Build a new program that asks the checker about itself, and then does the opposite: if the checker says "it stops", the new program loops forever, and if the checker says "it loops", it stops at once. Whatever the checker says about this new program is wrong. So no such checker exists.

You can still wait and watch. If a program stops, running it will show this. What you cannot do in general is be sure that a program that is still running will never stop.

## Definition

**Instance.** A Turing machine $M$, given by its code $\langle M \rangle$, and an input word $w$.

**Question.** Does $M$ halt on input $w$, in its accept or its reject state?

As a language,
$$\mathrm{HALT} = \{ \langle M, w \rangle : M \text{ halts on } w \}.$$
The *diagonal form* uses the [Gödel numbering](/godel-numbering/) $\varphi_0, \varphi_1, \ldots$ of the partial computable functions:
$$K = \{ e \in \mathbb{N} : \varphi_e(e) \text{ is defined} \}.$$
The two forms are many-one equivalent (see Reductions). This page means $\mathrm{HALT}$ unless it says $K$.

**Theorem.** $\mathrm{HALT}$ is c.e. and not decidable. Its complement $\overline{\mathrm{HALT}}$ is not c.e. The same holds for $K$.

*Proof that HALT is c.e.* A machine that, on input $\langle M, w \rangle$, simulates $M$ on $w$ with a universal machine, and accepts when the simulation halts, accepts exactly $\mathrm{HALT}$.

*Proof that HALT is not decidable.* Suppose a machine $H$ decides $\mathrm{HALT}$. Let $D$ be the machine that, on input $\langle M \rangle$:

1. runs $H$ on $\langle M, \langle M \rangle \rangle$;
2. if $H$ accepts, runs forever;
3. if $H$ rejects, halts.

$D$ is a Turing machine, since $H$ halts on every input. Now run $D$ on its own code. If $D$ halts on $\langle D \rangle$, then $H$ accepts $\langle D, \langle D \rangle \rangle$, so $D$ runs forever on $\langle D \rangle$ by step 2. If $D$ does not halt on $\langle D \rangle$, then $H$ rejects $\langle D, \langle D \rangle \rangle$, so $D$ halts by step 3. Both cases are impossible, so $H$ does not exist. This is the [diagonalization argument](/diagonalization-argument/) against the list of all machines. $\blacksquare$

*Proof that the complement is not c.e.* If $\overline{\mathrm{HALT}}$ were c.e., then $\mathrm{HALT}$ would be c.e. and co-c.e., and so decidable by Post's theorem on the [decidable language](/decidable-language/) page.

**Completeness.** For every c.e. language $A$, $A \le_m \mathrm{HALT}$ by a [many-one reduction](/many-one-reducibility/). Let $M_A$ accept exactly $A$, and let $M_A'$ be $M_A$ with its moves into the reject state replaced by moves into a state that loops forever. Then $x \in A$ if and only if $M_A'$ halts on $x$, so $x \mapsto \langle M_A', x \rangle$ is a reduction. Hence $\mathrm{HALT}$ is complete for the c.e. sets under $\le_m$, and so is $K$. In Post's terms, $K$ is a *creative* set.

**History.** Turing's 1936 paper does not state the halting problem. Its machines print infinite sequences of digits, and a machine is *circle-free* if it prints infinitely many. In Section 8, Turing shows by a diagonal argument that no machine decides whether a given machine is circle-free, and then that no machine decides whether a given machine ever prints a given symbol. In Section 11 he uses this to show that the [Entscheidungsproblem](/entscheidungsproblem/) is unsolvable. The modern form, about halting on an input, became standard later, and the name appears in Davis (1958).

## Variants

- **Blank-tape halting.** $\mathrm{HALT}_\varepsilon = \{ \langle M \rangle : M \text{ halts on the empty input} \}$ is undecidable too. Map $\langle M, w \rangle$ to the code of a machine $M_w$ that writes $w$ on its tape and then runs $M$.
- **The diagonal set** $K$, and the set $K_0 = \{ \pi(e, x) : \varphi_e(x) \text{ is defined} \}$ with the Cantor pairing $\pi$, are the numeric forms used in recursion theory.
- **Totality.** $\mathrm{TOT} = \{ \langle M \rangle : M \text{ halts on every input} \}$ is harder: it is neither c.e. nor co-c.e., and it is complete at level $\Pi_2$ of the [arithmetical hierarchy](/arithmetical-hierarchy/).
- **Bounded time.** "Does $M$ halt on $w$ within $t$ steps?" is decidable for every given $t$: simulate $t$ steps.
- **Bounded tape.** A machine that may use only $s$ cells of tape, as a linear bounded automaton uses only the cells of its input, has a decidable halting problem. Its configurations are at most $|Q| \cdot s \cdot |\Gamma|^s$, so if it runs longer than that, it repeats a configuration and loops forever.
- **Halting relative to an oracle.** For an [oracle Turing machine](/oracle-turing-machine/) with oracle $A$, the halting problem $A'$ is c.e. relative to $A$ and not decidable relative to $A$. This is the [Turing jump](/turing-jump/); $K$ is the jump of the empty set.
- **Real programs.** By the [Church-Turing thesis](/church-turing-thesis/) the same result holds for programs in any general programming language. Restricted languages, in which every loop has a bound fixed before it starts, have a trivial halting problem: every program halts.

## Examples

**A machine that halts on every input.** The decider for $\{0^k 1^k\}$ on the [Turing machine](/turing-machine/) page halts on every input: it accepts $0^k 1^k$ after $2k^2 + 2k + 1$ steps ($25$ for $000111$) and rejects $001$ after $8$ steps. So $\langle M, w \rangle \in \mathrm{HALT}$ for every $w$.

**A machine that halts on some inputs.** Replace its reject moves by moves that run right forever. The new machine halts on $0^k 1^k$ and on no other input. So $\langle M', 0011 \rangle \in \mathrm{HALT}$ and $\langle M', 001 \rangle \notin \mathrm{HALT}$.

**Open problems as halting questions.** Let $G$ be the machine that, for $n = 4, 6, 8, \ldots$, checks whether $n$ is a sum of two primes and halts at the first $n$ that is not. Then $G$ halts on the empty input if and only if Goldbach's conjecture is false. A decider for $\mathrm{HALT}_\varepsilon$ would settle this conjecture, and every other conjecture of the form "no number $n$ has the decidable property $P$". This shows how strong a halting decider would be, though it is not a proof that none exists.

**The self-referential machine.** In the proof, $D$ does not need to know its own code: it runs on every code $\langle M \rangle$, and the proof then looks at the one input $\langle D \rangle$. [Kleene's recursion theorem](/kleene-recursion-theorem/) gives machines that do obtain their own code, and with it a second proof: a machine that gets its own code, asks $H$ about itself and does the opposite.

## Known algorithms

- **Semi-decision by simulation.** Run $M$ on $w$ with a universal machine. If $M$ halts after $T$ steps, the simulation answers "yes" after $O(c_M T \log T)$ steps on a multitape machine. If $M$ does not halt, it never answers.
- **Loop detection.** If the run of $M$ on $w$ repeats a configuration, $M$ runs forever. With bounded tape this always happens, and a cycle finder such as [Floyd's cycle detection](/floyd-cycle-detection/) finds the repeat with a constant number of stored configurations.
- **Termination proofs.** For programs, a [termination proof](/termination-proof/) gives a ranking function into a well-founded order that decreases in each step. Tools search for such functions ([ranking function synthesis](/ranking-function-synthesis/)), and for term rewriting there are methods such as [size-change termination](/size-change-termination/). Each such method is sound but, by the theorem, incomplete: it must answer "unknown" on some terminating programs.

## Bounds

- **No algorithm.** No Turing machine decides $\mathrm{HALT}$, by the theorem above. The same holds for every model equivalent to Turing machines.
- **No computable bound on the halting time.** There is no total computable $f$ such that every machine with code length $n$ that halts on the empty input does so within $f(n)$ steps. Otherwise $\mathrm{HALT}_\varepsilon$ would be decidable: simulate $f(|\langle M \rangle|)$ steps and answer. So the [busy beaver function](/busy-beaver-function/), the longest halting time of an $n$-state machine on the empty input, grows faster than every computable function.
- **Degree.** $K$ has [Turing degree](/turing-degrees/) $\mathbf{0}'$, the highest degree of a c.e. set. With an oracle for $K$, the halting problem for oracle machines is still undecidable.

## Reductions

All reductions here are many-one reductions by total computable maps.

- **HALT to A_TM.** Map $\langle M, w \rangle$ to $\langle M_1, w \rangle$, where $M_1$ is $M$ with every move into the reject state redirected to the accept state. Then $M$ halts on $w$ if and only if $M_1$ accepts $w$. So $\mathrm{HALT} \le_m A_{\mathrm{TM}}$, and the [acceptance problem](/acceptance-problem/) is undecidable too.
- **A_TM to HALT.** Map $\langle M, w \rangle$ to $\langle M_2, w \rangle$, where $M_2$ is $M$ with every move into the reject state redirected to a state that loops forever. Then $M$ accepts $w$ if and only if $M_2$ halts on $w$.
- **K to HALT.** Map $e$ to $\langle M_e, e \rangle$, where $M_e$ is the machine with index $e$ and $e$ is written as a word.
- **HALT to K.** Map $\langle M, w \rangle$ to an index $e'$ of the machine that ignores its input and runs $M$ on $w$. The [s-m-n theorem](/s-m-n-theorem/) makes $e'$ a computable function of $\langle M, w \rangle$. Then $\varphi_{e'}(e')$ is defined if and only if $M$ halts on $w$.
- **From HALT to other problems.** Through $A_{\mathrm{TM}}$, the halting problem reduces to the [Post correspondence problem](/post-correspondence-problem/), and through it to [ambiguity of context-free grammars](/cfg-ambiguity-undecidable/). It also reduces to [Hilbert's tenth problem](/hilberts-tenth-problem/), the [word problem for groups](/word-problem-for-groups/) and [termination of rewriting](/undecidability-of-termination/). Its complement reduces to the emptiness problem and to totality, so these are not c.e. [Rice's theorem](/rice-theorem/) packages these reductions for all properties of languages.

## Applications

- **Undecidability proofs.** Most proofs of [undecidability](/undecidability/) are reductions from $\mathrm{HALT}$ or $A_{\mathrm{TM}}$.
- **Program analysis.** No tool can decide termination, or any nontrivial property of what a program computes; see [Rice's theorem](/rice-theorem/) and the [full employment theorem](/full-employment-theorem/). Practical verifiers are sound and incomplete.
- **Logic.** The undecidability of the [Entscheidungsproblem](/entscheidungsproblem/) and a proof of [Gödel's incompleteness theorem](/godel-incompleteness-theorem/) follow from it: a complete, consistent theory with a decidable set of axioms that can describe Turing machines would decide $\mathrm{HALT}$.
- **Kolmogorov complexity.** [Kolmogorov complexity](/kolmogorov-complexity/) is not computable, and [Chaitin's constant](/chaitins-constant/), the probability that a random program halts, is a real number whose digits encode the halting problem.

## References
