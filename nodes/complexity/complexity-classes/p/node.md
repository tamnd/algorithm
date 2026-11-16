---
tag: G1SRVV
kind: definition
slug: p
name: P
aliases:
- PTIME
area: complexity/complexity-classes
level: intro
summary: The class of decision problems that a deterministic Turing machine decides in time polynomial in the input length. It is closed under complement and under polynomial-time reductions.
prereqs: [complexity-class, polynomial-time, multitape-turing-machine, decision-problem]
see_also: [np, co-np, exptime, computational-tractability, p-versus-np-problem, circuit-value-problem, fp, class-inclusions-chain]
sources:
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 7.2, The class P (PATH, RELPRIME and context-free languages in P)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach
    locator: Chapter 1 (the class P, why the model does not matter)
  - paper: "Alan Cobham, The intrinsic computational difficulty of functions, in Y. Bar-Hillel (editor), Logic, Methodology and Philosophy of Science, Proceedings of the 1964 International Congress, North-Holland (1965), 24 to 30"
    locator: the class of functions computable in polynomial time
  - paper: doi:10.4153/CJM-1965-045-4
    title: Jack Edmonds, Paths, trees, and flowers, Canadian Journal of Mathematics 17 (1965), 449 to 467
    locator: Section 2, good algorithms
  - paper: doi:10.4007/annals.2004.160.781
    title: Manindra Agrawal, Neeraj Kayal and Nitin Saxena, PRIMES is in P, Annals of Mathematics 160(2) (2004), 781 to 793
    locator: the main theorem
  - paper: doi:10.1016/0097-3165(81)90016-9
    title: Aviezri S. Fraenkel and David Lichtenstein, Computing a perfect strategy for n x n chess requires time exponential in n, Journal of Combinatorial Theory, Series A 31(2) (1981), 199 to 214
    locator: the main theorem
---

P is the class of [decision problems](/decision-problem/) that a deterministic [Turing machine](/multitape-turing-machine/) decides in [polynomial time](/polynomial-time/), that is, within $O(n^k)$ steps on inputs of length $n$ for some constant $k$. It is the standard formal meaning of "solvable efficiently" ([computational tractability](/computational-tractability/)). P is contained in [NP](/np/), and whether the two classes are equal is the [P versus NP problem](/p-versus-np-problem/). This page defines the class. The page on [polynomial time](/polynomial-time/) treats the time bound itself, and the page on tractability treats the thesis that P captures efficiency.

## Definition

Fix the alphabet $\Sigma = \{0, 1\}$ and write $|x|$ for the length of a string $x$. For a function $f : \mathbb{N} \to \mathbb{N}$, $\mathsf{DTIME}(f(n))$ is the set of languages $L \subseteq \Sigma^*$ such that some deterministic multitape Turing machine $M$ halts on every input $x$ within $O(f(|x|))$ steps and accepts exactly the strings of $L$. Then

$$\mathsf{P} = \bigcup_{k \ge 1} \mathsf{DTIME}(n^k).$$

A decision problem is in P when its language, under a reasonable encoding, is in P. Numbers are written in binary and graphs as adjacency lists or matrices. Two reasonable encodings of the same objects have polynomially related lengths and are converted into each other in polynomial time, so the choice does not change membership in P.

**The model does not matter.** The definition gives the same class for one-tape machines, because a one-tape machine simulates a $k$-tape machine that runs in time $t(n) \ge n$ in time $O(t(n)^2)$ ([multitape simulation theorem](/multitape-simulation-theorem/)). It gives the same class for the [random-access machine](/random-access-machine/) with the logarithmic cost and for the [word RAM](/word-ram/), which simulate and are simulated by Turing machines with a polynomial slowdown ([RAM and Turing machine equivalence](/ram-turing-equivalence/)). The exponent $k$ of a given problem can change from one model to another. The class does not change.

**Closure properties.** Let $A, B \in \mathsf{P}$, decided by $M_A$ in time $p(n)$ and $M_B$ in time $q(n)$, with $p$ and $q$ non-decreasing polynomials.

- *Complement.* Swap the accepting and the rejecting states of $M_A$. The new machine decides $\Sigma^* \setminus A$ in the same time. So $\mathsf{P} = \mathsf{coP}$.
- *Union and intersection.* Run $M_A$, then $M_B$ on a saved copy of the input, and combine the two answers. The time is $O(n + p(n) + q(n))$.
- *Concatenation.* $x \in AB$ when $x = uv$ with $u \in A$ and $v \in B$. Try the $n + 1$ split points. The time is $O((n+1)(n + p(n) + q(n)))$.
- *Kleene star.* $x = x_1 \cdots x_n \in A^*$ when $x$ splits into pieces that are all in $A$. Let $D[0] = \text{true}$ and, for $j = 1, \ldots, n$, let $D[j]$ be true when $D[i]$ is true and $x_{i+1} \cdots x_j \in A$ for some $i < j$. Then $x \in A^*$ exactly when $D[n]$ is true, by induction on $j$: a prefix of length $j$ splits into pieces of $A$ exactly when its last piece is $x_{i+1} \cdots x_j \in A$ and the shorter prefix of length $i$ splits too. The table needs at most $n(n+1)/2$ calls of $M_A$ on strings of length at most $n$, so the time is $O(n^2 (n + p(n)))$.
- *Reductions.* If $A \le_p B$ by a [polynomial-time many-one reduction](/polynomial-time-reduction/) $f$ computable in time $r(n)$, and $B \in \mathsf{P}$, then $A \in \mathsf{P}$. On input $x$, compute $f(x)$, whose length is at most $r(|x|)$, and run $M_B$ on it. The time is $O(r(n) + q(r(n)))$, a polynomial.

The last property makes P the base of the theory of [NP-completeness](/np-complete/): an NP-complete problem is in P if and only if $\mathsf{P} = \mathsf{NP}$.

## Examples and non-examples

**Examples.**

- *Reachability.* Given a directed graph $G$ and two vertices $s$ and $t$, is there a path from $s$ to $t$? Breadth-first search answers in $O(|V| + |E|)$ steps on a RAM. See [graph reachability](/graph-reachability/).
- *Relatively prime numbers.* Given $a$ and $b$ in binary, is $\gcd(a, b) = 1$? The [Euclidean algorithm](/euclidean-algorithm/) uses $O(n)$ division steps on $n$-bit numbers, because the remainder at least halves every two steps. For the 20-bit Fibonacci numbers $832040$ and $514229$, it takes 28 division steps and returns 1. Counting from $1$ to $a$ and testing each candidate divisor is not polynomial, because it takes about $2^n$ steps.
- *2-SAT.* Is a CNF formula with at most two literals in each clause satisfiable? [2-SAT](/2-sat/) is solved in linear time with the strongly connected components of the implication graph. [Horn-SAT](/horn-sat/) is in P too.
- *Bipartite graphs and matchings.* [Bipartiteness testing](/bipartiteness-testing/) is breadth-first search. Whether a graph has a perfect matching is in P by Edmonds's [blossom algorithm](/edmonds-blossom/), the algorithm of the paper that introduced the word "good" for polynomial time.
- *Primality.* Given $N$ in binary, is $N$ prime? This is in P by the [AKS test](/aks-primality-test/) (Agrawal, Kayal and Saxena, 2004).
- *Linear programming.* Does a system of linear inequalities with rational coefficients have a solution? This is in P by the [ellipsoid method](/ellipsoid-method/) (Khachiyan, 1979). See [linear programming in P](/lp-in-p/).
- *Context-free languages.* For each fixed context-free grammar, membership of a string of length $n$ is decided in $O(n^3)$ time by dynamic programming (Sipser, Section 7.2).
- *A Kleene star.* Let $A = \{ab, aab, b\}$ and $x = aabab$. The table of the closure proof is $D = (\text{T}, \text{F}, \text{F}, \text{T}, \text{F}, \text{T})$ for the prefixes of length 0 to 5, so $x \in A^*$, with $x = aab \cdot ab$. For $x = aba$ the table is $(\text{T}, \text{F}, \text{T}, \text{F})$ and $x \notin A^*$.

**Non-examples.**

- *Provably outside P.* Every problem that is complete for [EXP](/exptime/) under polynomial-time reductions is not in P, because $\mathsf{P} \subsetneq \mathsf{EXP}$ by the [time hierarchy theorem](/time-hierarchy-theorem/). Fraenkel and Lichtenstein (1981) showed that deciding the winner of a position in generalized chess on an $n \times n$ board takes time exponential in $n$. So this problem is not in P, with no unproved assumption.
- *Undecidable problems.* The [halting problem](/halting-problem/) is in no time class at all.
- *Not known to be in P.* [SAT](/sat/), the [subset sum problem](/subset-sum-problem/) and the other NP-complete problems are not known to be in P. Showing that one is not in P would prove $\mathsf{P} \ne \mathsf{NP}$, which is open. [Integer factorization](/integer-factorization/) has no known polynomial-time algorithm, and it is not known to be NP-complete.
- *A trap with the encoding.* The dynamic program for subset sum with target $W$ takes about $nW$ steps. This is polynomial in the value $W$, not in its bit length $\lg W$, so it does not put subset sum in P. With the numbers written in unary, the same problem is in P. See [pseudo-polynomial time](/pseudo-polynomial-time/).

## Related definitions

- [Polynomial time](/polynomial-time/) is the time bound. P is the class of decision problems with a deterministic algorithm under that bound. [FP](/fp/) is the class of functions computable in polynomial time.
- [NP](/np/) uses a nondeterministic machine with the same bound. $\mathsf{P} \subseteq \mathsf{NP} \cap \mathsf{coNP}$, because a deterministic machine is a nondeterministic one and P is closed under complement. See [coNP](/co-np/) and [good characterization](/good-characterization/).
- P sits in the [chain of inclusions](/class-inclusions-chain/) $\mathsf{L} \subseteq \mathsf{NL} \subseteq \mathsf{P} \subseteq \mathsf{NP} \subseteq \mathsf{PSPACE} \subseteq \mathsf{EXP}$, and $\mathsf{P} \ne \mathsf{EXP}$.
- A problem is P-complete when it is in P and every problem in P reduces to it by a logspace many-one reduction. The [circuit value problem](/circuit-value-problem/) is the standard P-complete problem. A P-complete problem is in [L](/logspace/) only if $\mathsf{L} = \mathsf{P}$, and in [NC](/nc/) only if $\mathsf{NC} = \mathsf{P}$.
- [BPP](/bpp/) allows random choices with two-sided error at most $1/3$. $\mathsf{P} \subseteq \mathsf{BPP}$, and equality is open.
- [P/poly](/p-poly/) is the non-uniform version: languages decided by circuit families of polynomial size, with no algorithm needed to build the circuits. It contains P and also undecidable languages.

## References
