---
tag: XNEPER
kind: definition
slug: exptime
name: EXP (EXPTIME)
aliases:
- EXP
- exponential time
area: complexity/complexity-classes
level: intro
summary: "Decision problems that a deterministic Turing machine decides in time 2 to the power of a polynomial. It contains PSPACE and is provably larger than P."
prereqs: [p, complexity-class]
see_also: [p, nexptime, pspace, time-hierarchy-theorem, class-inclusions-chain, expspace, complexity-class, presburger-arithmetic]
sources:
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 9.1, Hierarchy theorems (EXPTIME and the proof that P is a proper subset of EXPTIME)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach
    locator: Section 2.6.2, EXP and NEXP
  - book: isbn:9780201530827
    title: Christos H. Papadimitriou, Computational Complexity, Addison-Wesley, 1994
    locator: Chapter 20, A glimpse beyond (exponential time)
  - paper: doi:10.1090/S0002-9947-1965-0170805-7
    title: Juris Hartmanis and Richard E. Stearns, On the computational complexity of algorithms, Transactions of the American Mathematical Society 117 (1965), 285 to 306
    locator: the time hierarchy
  - paper: doi:10.1016/0097-3165(81)90016-9
    title: Aviezri S. Fraenkel and David Lichtenstein, Computing a perfect strategy for n x n chess requires time exponential in n, Journal of Combinatorial Theory, Series A 31(2) (1981), 199 to 214
    locator: the main theorem
  - paper: "Michael J. Fischer and Michael O. Rabin, Super-exponential complexity of Presburger arithmetic, in R. M. Karp (editor), Complexity of Computation, SIAM-AMS Proceedings 7 (1974)"
    locator: the doubly exponential lower bound
---

EXP, also written EXPTIME, is the class of [decision problems](/decision-problem/) that a deterministic Turing machine decides in time $2^{p(n)}$ for some polynomial $p$. It contains [P](/p/), [NP](/np/) and [PSPACE](/pspace/). It is one of the few classes for which a separation is proved: $\mathsf{P} \ne \mathsf{EXP}$ by the [time hierarchy theorem](/time-hierarchy-theorem/). So a problem that is complete for EXP is provably not in P.

## Definition

Fix the alphabet $\{0, 1\}$, and let $\mathsf{DTIME}(f(n))$ be the set of languages decided by a deterministic multitape Turing machine within $O(f(n))$ steps on inputs of length $n$. Then

$$\mathsf{EXP} = \bigcup_{k \ge 1} \mathsf{DTIME}\left(2^{n^k}\right).$$

The names EXP and EXPTIME denote the same class. The smaller class $\mathsf{E} = \bigcup_{c \ge 1} \mathsf{DTIME}(2^{cn})$ allows only a linear exponent. E is not closed under polynomial-time reductions, because a reduction can make the input longer by a polynomial factor. EXP is closed under them, and so it is the class with natural complete problems.

**The model does not matter.** A one-tape machine simulates a multitape machine of time $t(n)$ in time $O(t(n)^2)$, and $(2^{n^k})^2 = 2^{2n^k}$ is again in the class. RAMs with the logarithmic cost give the same class too ([multitape simulation theorem](/multitape-simulation-theorem/), [RAM and Turing machine equivalence](/ram-turing-equivalence/)). Each polynomial slowdown changes the exponent $n^k$ only by a constant factor.

**Closure.** EXP is closed under complement (swap the accepting and the rejecting states), under union and intersection, and under polynomial-time many-one reductions. For the last: if $A \le_p B$ by $f$, with $|f(x)| \le r(|x|)$, and $B \in \mathsf{DTIME}(2^{n^k})$, then $A \in \mathsf{DTIME}(2^{r(n)^k} + r(n))$, and $r(n)^k$ is a polynomial.

**Inclusions.**

- $\mathsf{P} \subseteq \mathsf{EXP}$, since $n^k \le 2^n$ for large $n$.
- $\mathsf{NP} \subseteq \mathsf{EXP}$: try all $2^{p(n)}$ certificates of the [verifier](/polynomial-time-verifier/).
- $\mathsf{PSPACE} \subseteq \mathsf{EXP}$. A machine with $q$ states, a tape alphabet of size $g$ and space $s(n) \ge \log n$ has at most $q \cdot (n + 2) \cdot s(n) \cdot g^{s(n)} = 2^{O(s(n))}$ configurations. A machine that halts on every input never repeats a configuration, so it runs for at most that many steps. For $s(n) = n^k$ the bound is $2^{O(n^k)}$.
- $\mathsf{EXP} \subseteq \mathsf{NEXP} \subseteq \mathsf{EXPSPACE}$. See [NEXP](/nexptime/) and [EXPSPACE](/expspace/).

**$\mathsf{P} \ne \mathsf{EXP}$.** The [time hierarchy theorem](/time-hierarchy-theorem/) (Hartmanis and Stearns, 1965) says that $\mathsf{DTIME}(f(n)) \subsetneq \mathsf{DTIME}(g(n))$ when $g$ is time-constructible and $f(n) \log f(n) = o(g(n))$. Every $n^k$ is $O(2^n)$, so $\mathsf{P} \subseteq \mathsf{DTIME}(2^n)$. With $f(n) = 2^n$ and $g(n) = 2^{2n}$, $f \log f = n 2^n = o(2^{2n})$, so $\mathsf{DTIME}(2^n) \subsetneq \mathsf{DTIME}(2^{2n}) \subseteq \mathsf{EXP}$. Hence $\mathsf{P} \subsetneq \mathsf{EXP}$.

In the chain $\mathsf{P} \subseteq \mathsf{NP} \subseteq \mathsf{PSPACE} \subseteq \mathsf{EXP}$, at least one inclusion is therefore strict. Which one is not known. See [the chain of inclusions](/class-inclusions-chain/).

**EXP-completeness.** A language is EXP-complete when it is in EXP and every language in EXP reduces to it by a polynomial-time many-one reduction. By the separation, no EXP-complete language is in P. This is a lower bound with no unproved assumption, unlike NP-hardness.

## Examples and non-examples

**Examples.**

- *Bounded halting with a binary clock.* The language $\{ \langle M, x, t \rangle : M \text{ accepts } x \text{ within } t \text{ steps} \}$, with $t$ written in binary, is EXP-complete. It is in EXP: a universal machine simulates $M$ for $t$ steps, and $t < 2^m$ where $m$ is the length of the input, so the time is $2^{O(m)}$. It is EXP-hard: let $L \in \mathsf{EXP}$ be decided by $M$, and choose $k$ so that $M$ halts within $2^{n^k}$ steps on every input of length $n \ge 2$. The map $x \mapsto \langle M, x, 2^{|x|^k} \rangle$ is a reduction. The number $2^{|x|^k}$ has $|x|^k + 1$ bits, so the map runs in polynomial time. The finitely many inputs shorter than 2 are mapped to fixed yes-instances or no-instances. With $t$ written in unary the same language is in P, which shows how the encoding of numbers matters. A clock of 64 bits already allows $2^{64} = 18{,}446{,}744{,}073{,}709{,}551{,}616$ steps, about 585 years at $10^9$ steps per second.
- *Generalized chess.* Fraenkel and Lichtenstein (1981) showed that deciding whether a player can force a win from a given position of chess on an $n \times n$ board is hard for EXP, so it takes time exponential in $n$. Games of this kind are in EXP because the number of positions is exponential in the board size, and the game tree can be evaluated position by position.
- *Every problem in PSPACE*, such as [QSAT](/qsat/) and [generalized geography](/generalized-geography/), is in EXP. Whether they are EXP-complete is open, because $\mathsf{PSPACE} = \mathsf{EXP}$ is not ruled out.
- *Brute force for NP.* Exhaustive search for [SAT](/sat/) on $n$ variables takes about $2^n$ steps times the cost of one evaluation, so SAT is in EXP.

**Non-examples.**

- *Problems not in EXP.* [Presburger arithmetic](/presburger-arithmetic/) has a doubly exponential lower bound (Fischer and Rabin, 1974), so it is not in EXP. The time hierarchy theorem also gives languages in $\mathsf{DTIME}(2^{2^n})$ that are not in EXP.
- *Not known to be outside EXP.* Problems complete for [EXPSPACE](/expspace/) are not known to be outside EXP, because $\mathsf{EXP} = \mathsf{EXPSPACE}$ is not ruled out. Only $\mathsf{PSPACE} \ne \mathsf{EXPSPACE}$ is known.
- *An exponential algorithm is not a hardness proof.* An algorithm that takes $2^n$ steps shows that a problem is in EXP. It does not show that the problem is outside P. SAT has such an algorithm, and whether it also has a polynomial one is the P versus NP problem.
- *Large polynomials are not exponential.* For $2 \le n \le 58$, $2^n \le n^{10}$, and $2^n > n^{10}$ for every $n \ge 59$. The polynomial $n^{10}$ is in P and $2^n$ is not polynomial, even though $n^{10}$ is the larger one for small inputs.

## Related definitions

- [NEXP](/nexptime/) is the nondeterministic version. $\mathsf{EXP} \subseteq \mathsf{NEXP}$, and equality is open. If $\mathsf{P} = \mathsf{NP}$, then $\mathsf{EXP} = \mathsf{NEXP}$, by padding.
- [PSPACE](/pspace/) $\subseteq$ EXP $\subseteq$ [EXPSPACE](/expspace/), and $\mathsf{PSPACE} \ne \mathsf{EXPSPACE}$ by the [space hierarchy theorem](/space-hierarchy-theorem/).
- [Subexponential time](/subexponential-time/) and [quasi-polynomial time](/quasi-polynomial-time/) lie between P and EXP: $\mathsf{P} \subseteq \mathsf{QP} \subseteq \mathsf{SUBEXP} \subseteq \mathsf{EXP}$.
- The [time hierarchy theorem](/time-hierarchy-theorem/) gives the separation $\mathsf{P} \ne \mathsf{EXP}$, and it also separates EXP from larger time classes such as $\mathsf{DTIME}(2^{2^n})$.

## References
