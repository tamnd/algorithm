---
tag: 68ZM0D
kind: definition
slug: fp
name: FP
aliases:
- function polynomial time
area: complexity/complexity-classes
level: intro
summary: "The functions that a deterministic Turing machine computes in polynomial time. It is the function version of P, and it contains the search problems that a polynomial-time algorithm solves."
prereqs: [p, polynomial-time, multitape-turing-machine]
see_also: [p, fnp, tfnp, search-problem, search-to-decision-reduction, polynomial-time, pp, integer-factorization]
sources:
  - book: isbn:9780201530827
    title: Christos H. Papadimitriou, Computational Complexity, Addison-Wesley, 1994
    locator: Section 10.3, Function problems (FNP, FP, and the proof that FP = FNP if and only if P = NP)
  - book: isbn:9780521884730
    title: Oded Goldreich, Computational Complexity, A Conceptual Perspective, Cambridge University Press, 2008
    locator: Chapter 2, search problems and the class PF
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Chapter 1 (computable functions and running time on the multitape Turing machine) and Section 2.5 (decision versus search)
  - paper: "Alan Cobham, The intrinsic computational difficulty of functions, in Y. Bar-Hillel (editor), Logic, Methodology and Philosophy of Science, Proceedings of the 1964 International Congress, North-Holland (1965), 24 to 30"
    locator: the class of functions computable in polynomial time
---

FP (function polynomial time) is the class of functions from strings to strings that a deterministic machine computes in [polynomial time](/polynomial-time/). It is the function version of [P](/p/): P asks for a yes or no answer, and FP asks for an output string, such as a product, a sorted list or a shortest path. Cobham (1965) used this class of functions to give a notion of efficient computation that does not depend on the machine. Two conventions use the name. One reads FP as a class of functions with one value. The other, used with [FNP](/fnp/), reads FP as the class of search problems that some polynomial-time algorithm solves. This page gives both and says how they agree.

## Definition

Fix the alphabet $\{0, 1\}$ and write $|x|$ for the length of a string $x$. The machine is the deterministic [multitape Turing machine](/multitape-turing-machine/) with a separate output tape.

**FP as a class of functions.** A function $f : \{0, 1\}^* \to \{0, 1\}^*$ is in FP when there are a deterministic multitape Turing machine $M$ and a polynomial $p$ such that, for every input $x$, $M$ halts within $p(|x|)$ steps with $f(x)$ on its output tape.

The machine writes at most one symbol in each step, so $|f(x)| \le p(|x|)$. A function in FP is *polynomially bounded*: its output is never more than polynomially longer than its input. The class does not change if the model is a one-tape machine or a RAM with the logarithmic cost, because these models simulate each other with a polynomial slowdown ([multitape simulation theorem](/multitape-simulation-theorem/), [RAM and Turing machine equivalence](/ram-turing-equivalence/)). The exponent of $p$ can change between models.

**FP as a class of search problems.** A [search problem](/search-problem/) is given by a binary relation $R$. On input $x$, an algorithm *solves* $R$ when it outputs some $y$ with $(x, y) \in R$ if such a $y$ exists, and outputs "no" otherwise. In this convention, FP is the class of relations that a deterministic polynomial-time algorithm solves. Papadimitriou (Section 10.3) uses this form when he compares FP with FNP, and Goldreich (Chapter 2) calls the class PF.

**The two forms agree.** A function $f$ in FP gives the relation $R_f = \{(x, f(x))\}$, and the machine for $f$ solves it. Conversely, a polynomial-time algorithm that solves a relation $R$ picks one answer for each $x$, so its output is a function in FP. The relation form only adds that many answers can be correct.

**Basic facts.**

- *P inside FP.* A language $L$ is in P if and only if its characteristic function $\chi_L$, with $\chi_L(x) = 1$ for $x \in L$ and 0 otherwise, is in FP.
- *Closure under composition.* If $f$ runs in time $p(n)$ and $g$ runs in time $q(n)$, then $g \circ f$ runs in time $p(n) + q(p(n))$, since $|f(x)| \le p(|x|)$. This is a polynomial. So an algorithm that calls polynomial-time subroutines a polynomial number of times, on inputs of polynomial length, stays in FP.
- *Bits of the output.* For a polynomially bounded $f$, let $L_f$ be the set of triples $(x, i, b)$ such that $f(x)$ has at least $i$ bits and its $i$-th bit is $b$. Then $f \in \mathsf{FP}$ if and only if $L_f \in \mathsf{P}$. One direction computes $f(x)$ and reads bit $i$. For the other, ask about $(x, i, 0)$ and $(x, i, 1)$ for $i = 1, 2, \ldots$. If neither is in $L_f$, the output has ended. This takes at most $2(p(|x|) + 1)$ tests. So questions about FP can be turned into questions about P.

## Examples and non-examples

**Examples.**

- *Arithmetic on binary numbers.* Addition, multiplication, integer division and the gcd by Euclid's algorithm all run in time polynomial in the number of bits.
- *Modular powers.* The map $(a, b, m) \mapsto a^b \bmod m$ is in FP by [binary exponentiation](/binary-exponentiation/), with about $\log_2 b$ squarings of numbers below $m$.
- *Sorting, shortest paths and matchings.* Each returns a list or a set, not a bit, and each has a polynomial-time algorithm.
- *Search problems with polynomial-time solutions.* Find a perfect matching in a bipartite graph or say that none exists. Find a solution of a linear system over the rationals.

**Non-examples.**

- *Output too long.* The map $x \mapsto 2^x$, with $x$ and $2^x$ in binary, is not in FP. The input $x = 64$ has 7 bits, and $2^{64}$ has 65 bits. The input $x = 2^{20}$ has 21 bits, and $2^x$ has $2^{20} + 1 = 1{,}048{,}577$ bits. The output length grows exponentially in the input length, so no polynomial-time machine can write it. The map $(a, b, m) \mapsto a^b \bmod m$ above avoids this because the output is below $m$.
- *Uncomputable functions.* The function that maps a machine to the number of steps it runs before it halts, or to 0 if it never halts, is not computable at all (see the [halting problem](/halting-problem/)).

**Not known to be in FP.**

- *Satisfying assignments.* Given a formula, output a satisfying assignment or "no". This is in FNP, and it is in FP if and only if $\mathsf{P} = \mathsf{NP}$ (see [FNP](/fnp/)).
- *Factoring.* Given a number $N$, output its prime factors. Every $N \ge 2$ has a factorization, and a claimed one is checked in polynomial time by multiplication and [primality testing](/primality-testing/). No polynomial-time algorithm on a classical computer is known (see [integer factorization](/integer-factorization/) and [TFNP](/tfnp/)).
- *Counting.* Given a formula, output the number of satisfying assignments. This counting function is in the class #P, which is described on the page on [PP](/pp/). If it were in FP, then $\mathsf{P} = \mathsf{NP}$, since a formula is satisfiable exactly when the count is not 0.

**A common mistake.** A function whose *value* is a small number can still be out of reach. The output of a counting function has only polynomially many bits, so the bound on the output length does not help. What decides membership in FP is the running time, not the output length alone.

## Related definitions

- **[P](/p/)** is the class of languages decided in polynomial time. It is the case of FP with outputs of one bit.
- **[FNP](/fnp/)** is the class of search problems whose relation is polynomially balanced and decidable in polynomial time. With FP read as search problems, $\mathsf{FP} \subseteq \mathsf{FNP}$, and $\mathsf{FP} = \mathsf{FNP}$ if and only if $\mathsf{P} = \mathsf{NP}$.
- **[TFNP](/tfnp/)** is the part of FNP where every instance has a solution. It contains the problems of FP whose relation is total, and its subclasses [PLS](/pls/) and [PPAD](/ppad/) contain FP in this sense.
- **[Search problem](/search-problem/)** and **[search-to-decision reduction](/search-to-decision-reduction/)** give the general setting and the method that turns a decision procedure into a search procedure.
- **[Polynomial time](/polynomial-time/)** is the notion of a time bound that both P and FP use. The class FP is a set of functions, and polynomial time is the bound that defines it.
- **$\mathsf{FP}^{\mathsf{NP}}$** is the class of functions computed in polynomial time by an [oracle Turing machine](/oracle-turing-machine/) with an NP oracle, where each query costs one step. It contains the satisfying-assignment search problem, by the search-to-decision reduction.

## References
