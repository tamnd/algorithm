---
tag: M21PE2
kind: concept
slug: church-turing-thesis
name: Church-Turing thesis
aliases:
- Church's thesis
- Church-Turing hypothesis
- Turing's thesis
area: complexity/computability
level: intro
summary: The claim that every function a person can compute by a mechanical method is computable by a Turing machine. It is a thesis about an informal notion, not a theorem.
prereqs: [turing-machine]
see_also: [turing-machine, lambda-calculus, computable-function, turing-completeness, ram-turing-equivalence, universal-turing-machine, bqp, entscheidungsproblem]
sources:
  - paper: doi:10.2307/2371045
    title: Alonzo Church, An unsolvable problem of elementary number theory, American Journal of Mathematics 58(2) (1936)
    locator: pp. 345 to 363 (the definition of effective calculability as general recursiveness or lambda-definability)
  - paper: doi:10.1112/plms/s2-42.1.230
    title: Alan M. Turing, On computable numbers, with an application to the Entscheidungsproblem, Proceedings of the London Mathematical Society (2) 42 (1936), with a correction in volume 43 (1937), pp. 544 to 546
    locator: pp. 230 to 265, Section 9 (the extent of the computable numbers, the analysis of a human computer)
  - paper: doi:10.2307/2268280
    title: Alan M. Turing, Computability and lambda-definability, Journal of Symbolic Logic 2(4) (1937)
    locator: pp. 153 to 163 (machine computability equals lambda-definability)
  - title: Stephen C. Kleene, Recursive predicates and quantifiers, Transactions of the American Mathematical Society 53 (1943)
    locator: pp. 41 to 73, Section 12 (Thesis I)
  - title: Stephen C. Kleene, Introduction to Metamathematics, Van Nostrand and North-Holland, 1952
    locator: Section 62, Church's thesis; Section 70, Turing's thesis
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 3.3, The definition of algorithm
  - paper: doi:10.25088/complexsystems.15.1.1
    title: Matthew Cook, Universality in elementary cellular automata, Complex Systems 15(1) (2004)
    locator: pp. 1 to 40 (rule 110 is universal)
  - book: isbn:9783642319327
    title: Robert I. Soare, Turing Computability, Theory and Applications, Springer, 2016
    locator: Chapter 1, Defining Computability
---

The Church-Turing thesis says that every function that can be computed by an effective, mechanical method can be computed by a [Turing machine](/turing-machine/). Church stated it in 1936 for the general recursive and the [lambda-definable](/lambda-calculus/) functions, and Turing stated it in the same year for his machines, with an analysis of what a human clerk can do with pencil and paper. The two classes were soon proved equal. The thesis is not a theorem: it links a precise class of functions to an informal notion, so it cannot be proved, only supported. It is the reason that undecidability results about Turing machines apply to every programming language.

## In plain words

Before 1936 mathematicians used the word "algorithm" without a definition. That was fine for showing that a method exists, since you just give the method. To show that no method exists for some problem, you need to know exactly what counts as a method.

Church and Turing each gave a precise definition. Turing described a clerk who follows fixed rules, looks at a few symbols at a time and writes on paper, and turned that clerk into a simple machine. The thesis says: whatever such a clerk can compute, the machine can compute.

Nobody can prove this, because "what a clerk can compute" is not a precise idea. The evidence is that every other definition people have proposed, from programming languages to rewriting systems, computes exactly the same functions.

## The idea

### Statement

**Church-Turing thesis.** A function $f : \mathbb{N} \rightharpoonup \mathbb{N}$, or $f : \Sigma^* \rightharpoonup \Sigma^*$, is effectively calculable if and only if it is computable by a Turing machine.

Here *effectively calculable* means that a finite set of exact instructions, which a person can follow mechanically, with unlimited paper and time and no insight, produces $f(x)$ from $x$ in finitely many steps when $f(x)$ is defined. The direction "Turing computable implies effectively calculable" is clear: a person can carry out the steps of a Turing machine. The thesis is the other direction.

The left side is informal, so the thesis is a claim about the right definition, not a mathematical statement. The right side is a precise class: the partial [computable functions](/computable-function/). This page uses the thesis only for statements about *what* is computable, never about *how fast*.

### The names

Church (1936) proposed to identify the effectively calculable functions with the general recursive functions, which he and Kleene had shown equal to the lambda-definable ones. Turing (1936) proposed his machines independently, and in 1937 proved that a function is Turing computable if and only if it is lambda-definable. Kleene stated the claim as "Thesis I" in 1943 and in his book of 1952 called it "Church's thesis" (Section 62) and "Turing's thesis" (Section 70). The combined name came later.

### The evidence

- **Agreement of the models.** Every model of computation proposed as general computes the same class of functions: the general recursive and [partial recursive functions](/partial-recursive-function/), the [lambda calculus](/lambda-calculus/), [combinatory logic](/combinatory-logic/), [Post canonical systems](/post-canonical-system/), [Markov algorithms](/markov-algorithm/), [register machines](/register-machine/), the [random-access machine](/random-access-machine/) ([RAM and Turing machine equivalence](/ram-turing-equivalence/)), the [multitape](/multitape-turing-machine/) and [nondeterministic](/nondeterministic-turing-machine/) Turing machines, and some [cellular automata](/cellular-automaton/). Each equivalence is a theorem with a simulation in each direction.
- **Turing's analysis.** Section 9 of Turing's paper argues from the limits of a human computer: a bounded number of symbols in view, a bounded number of states of mind, and local changes in each step. A computer with these limits is a Turing machine.
- **Stability.** Adding features that are still mechanical (more tapes, two-dimensional tapes, nondeterminism, random choices with a correct answer required) does not add computable functions.
- **No counterexample.** No method that people accept as mechanical has been found that computes a function outside the class.

### What the thesis does not say

- **It says nothing about time.** A one-tape machine may need quadratically more steps than a two-tape machine for the same task. The thesis treats them as equal.
- **The extended thesis is a different claim.** The *extended* (or *strong*, or *polynomial*) Church-Turing thesis says that every reasonable model of computation can be simulated by a [probabilistic Turing machine](/probabilistic-turing-machine/) with only a polynomial increase in time. This is a claim about cost, and it is open. Quantum computers challenge it: [factoring is in BQP](/factoring-in-bqp/), while no polynomial-time classical algorithm for [integer factorization](/integer-factorization/) is known. This does not refute the extended thesis, since it is not proved that factoring needs more than polynomial time classically. A [quantum Turing machine](/quantum-turing-machine/) computes only Turing-computable functions, so quantum computers do not challenge the thesis itself. See [BQP](/bqp/).
- **It is about functions on finite objects.** For functions on real numbers, the thesis needs a representation of the inputs, as in [computable real numbers](/computable-real-numbers/). A model with exact real arithmetic, such as the [Blum-Shub-Smale machine](/blum-shub-smale-machine/), answers a different question.
- **It is not a claim about physics or minds.** Whether every physical process can be simulated by a Turing machine is a separate claim, sometimes called the physical Church-Turing thesis. The thesis as Church and Turing meant it concerns a person following rules.
- **Oracles are not counterexamples.** An [oracle Turing machine](/oracle-turing-machine/) that can query the halting problem computes more, but its oracle is not a mechanical method.

## Examples

**Proof by the thesis.** Textbooks describe a machine in prose, for example "on input $\langle M, w \rangle$, run $M$ on $w$ for $|w|$ steps and accept if it has halted", and say that a Turing machine exists. This use of the thesis is a shortcut, not an extra axiom: in each case the machine could be written out. The [universal Turing machine](/universal-turing-machine/) is the part that is hard to write out, and it was written out once, by Turing.

**One function, three models.** Addition $x + y$ is computed:
- by a Turing machine on the input $1^x 0 1^y$: change the $0$ to $1$, go to the right end, erase the last $1$. This takes $x + y + 3$ steps; for $x = 5$ and $y = 7$ it takes $15$ steps and leaves $1^{12}$;
- by a register machine with the loop "while $y > 0$: $y \leftarrow y - 1$, $x \leftarrow x + 1$";
- in the lambda calculus by the term $\lambda m.\lambda n.\lambda f.\lambda x.\, m\,f\,(n\,f\,x)$ on Church numerals.

The functions agree; the costs do not, which is why the thesis is silent about cost.

**Cost under simulation.** The one-tape machine of the [Turing machine](/turing-machine/) page decides $\{0^k 1^k\}$ and takes $2k^2 + 2k + 1$ steps on $0^k 1^k$: $25$ steps for $k = 3$ and $145$ for $k = 8$. A two-tape machine decides the same language in $O(k)$ steps. The language is the same, the time is not.

**A universal cellular automaton.** The elementary cellular automaton rule 110 updates each cell from itself and its two neighbours. Cook (2004) proved that it can simulate any Turing machine, through cyclic tag systems, with an initial row that repeats a fixed pattern to the left and to the right. So a very simple local rule already computes every Turing-computable function, under a suitable coding of the input and output.

## Where it is used

- **Undecidability for all languages.** The [halting problem](/halting-problem/), [Rice's theorem](/rice-theorem/) and the other undecidability results are proved for Turing machines. The thesis transfers them to every programming language and every mechanical procedure.
- **The Entscheidungsproblem.** Church and Turing needed a definition of "method" to show that the [Entscheidungsproblem](/entscheidungsproblem/) has no solution.
- **Turing completeness.** A system is [Turing complete](/turing-completeness/) if it can simulate every Turing machine. By the thesis, such a system computes every function that can be computed at all.
- **Complexity theory.** Complexity classes such as P and PSPACE are defined on the [multitape Turing machine](/multitape-turing-machine/). The [multitape simulation theorem](/multitape-simulation-theorem/) and [RAM and Turing machine equivalence](/ram-turing-equivalence/) show that these classes do not change between the usual models, though exact exponents do. This robustness is the polynomial-time analogue of the thesis.

## References
