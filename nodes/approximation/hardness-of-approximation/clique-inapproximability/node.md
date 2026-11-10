---
tag: KWSQM6
kind: theorem
slug: clique-inapproximability
name: Clique inapproximability
aliases:
- Håstad clique hardness
- Zuckerman clique hardness
area: approximation/hardness-of-approximation
level: advanced
summary: The FGLSS graph turns a PCP verifier into a clique gap, so maximum clique has no constant ratio unless P = NP. Håstad and Zuckerman pushed this to n to the power 1 - ε, which is nearly tight.
prereqs: [pcp-theorem, probabilistically-checkable-proof, gap-amplification, maximum-clique]
see_also: [graph-coloring-inapproximability, vertex-cover-inapproximability, maximum-independent-set, clique-number, gap-preserving-reduction, expander-walk-sampler, zpp, quasi-polynomial-time]
sources:
  - paper: doi:10.1145/226643.226652
    title: Uriel Feige, Shafi Goldwasser, László Lovász, Shmuel Safra and Mario Szegedy, Interactive proofs and the hardness of approximating cliques, Journal of the ACM 43(2), 1996
    locator: The reduction from a verifier to a graph whose clique number is the largest acceptance count
  - paper: doi:10.1007/BF02392825
    title: Johan Håstad, Clique is hard to approximate within n to the power 1 - ε, Acta Mathematica 182, 1999
    locator: The main theorem, under the assumption NP is not ZPP
  - paper: doi:10.4086/toc.2007.v003a006
    title: David Zuckerman, Linear degree extractors and the inapproximability of max clique and chromatic number, Theory of Computing 3, 2007
    locator: The derandomization of Håstad's result, n to the power 1 - ε unless P = NP
  - paper: doi:10.1145/278298.278306
    title: Sanjeev Arora, Carsten Lund, Rajeev Motwani, Madhu Sudan and Mario Szegedy, Proof verification and the hardness of approximation problems, Journal of the ACM 45(3), 1998
    locator: The PCP theorem and the corollary that clique has no n to the power ε approximation for some ε > 0 unless P = NP
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Chapter 11, Section 11.4 (independent set and the FGLSS view) and Chapter 22, Section 22.2.4 (expander walks for independent set)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms, Cambridge University Press, 2011
    locator: Chapter 16, Theorem 16.12 and Corollaries 16.13 and 16.14 (no constant ratio for independent set)
---

Maximum [clique](/maximum-clique/) is among the hardest problems to approximate: the trivial algorithm that returns one vertex has ratio $1/n$, and nothing in polynomial time is much better unless P = NP. The bridge is the FGLSS graph of Feige, Goldwasser, Lovász, Safra and Szegedy (1996): its vertices are the accepting views of a [PCP](/probabilistically-checkable-proof/) verifier and its clique number is the largest number of random strings on which one proof is accepted. This page proves that construction in full, with the consequences for constant ratios and quasi-polynomial gaps. It cites the polynomial bound $n^{\varepsilon - 1}$ of Håstad (1999, assuming NP $\ne$ [ZPP](/zpp/)) and of Zuckerman (2007, assuming P $\ne$ NP).

## Statement

**Notation.** $G$ is a graph on $N$ vertices and $\omega(G)$ its [clique number](/clique-number/). Clique is a maximization problem, so an $\alpha$-approximation returns a clique of size at least $\alpha\,\omega(G)$, $\alpha \le 1$; a bound "$n^{1 - \varepsilon}$" in the literature means $\alpha = N^{\varepsilon - 1}$ here, or performance ratio $R = N^{1 - \varepsilon}$.

A *nonadaptive verifier* $V$ for a language $L$ uses $r$ random bits on inputs $w$ of length $n$. For each random string $\rho \in \{0,1\}^r$ it reads $q$ proof positions $P(\rho)$, which depend on $w$ and $\rho$ only, and it accepts on a set $A(\rho)$ of bit patterns. For a proof $\pi$, $\mathrm{acc}(\pi)$ is the number of random strings on which $V$ accepts. $V$ has completeness 1 and soundness $s$ if $w \in L$ gives some $\pi$ with $\mathrm{acc}(\pi) = 2^r$, and $w \notin L$ gives $\mathrm{acc}(\pi) \le s\,2^r$ for each $\pi$.

**The FGLSS graph.** $G_{V,w}$ has one vertex $(\rho, a)$ for each random string $\rho$ and each accepted pattern $a \in A(\rho)$. Two vertices $(\rho, a)$ and $(\rho', a')$ are adjacent when $\rho \ne \rho'$ and the views are consistent: for each position $p \in P(\rho) \cap P(\rho')$, $a$ and $a'$ give the same bit to $p$.

**Theorem 1 (FGLSS; proved here).** $\omega(G_{V,w}) = \max_\pi \mathrm{acc}(\pi)$. The graph has at most $2^r \cdot 2^q$ vertices and is built in time polynomial in $2^{r + q}$ and the running time of $V$.

**Corollary 2 (proved here from the PCP theorem).** For each constant $\alpha > 0$, maximum clique has no polynomial-time $\alpha$-approximation unless P = NP. Also, there is a constant $c > 0$ such that clique has no $2^{-c\sqrt{\log N}}$-approximation unless NP $\subseteq$ DTIME$(n^{O(\log n)})$.

**Theorem 3 (Arora, Lund, Motwani, Sudan and Szegedy, with randomness-efficient repetition; sketch only).** There is a constant $\varepsilon > 0$ such that clique has no polynomial-time $N^{-\varepsilon}$-approximation unless P = NP.

**Theorem 4 (Håstad 1999; cited).** For each $\varepsilon > 0$, clique has no polynomial-time $N^{\varepsilon - 1}$-approximation unless NP = ZPP.

**Theorem 5 (Zuckerman 2007; cited).** For each $\varepsilon > 0$, clique has no polynomial-time $N^{\varepsilon - 1}$-approximation unless P = NP.

## In plain words

A probabilistically checkable proof is checked by reading a few bits at random places. Draw one dot for each way the checker could look at the proof and be satisfied: a choice of random places together with bit values that pass. Connect two dots when they could come from the same proof, which means they do not disagree on any place they both read. A group of dots that are all connected describes one consistent proof, and its size counts how many random choices that proof passes. If the claim is true, some proof passes every choice, so there is a huge connected group. If it is false, every proof fails half the choices, so every such group is small. A good clique algorithm would tell the two cases apart. Repeating the check makes the difference between the cases as large as one likes.

## Proof

**Proof of Theorem 1.** ($\ge$) Fix a proof $\pi$. Let $Q = \{(\rho, \pi|_{P(\rho)}) : V \text{ accepts } \pi \text{ on } \rho\}$, where $\pi|_{P(\rho)}$ is the pattern that $\pi$ shows at the positions of $\rho$. Each element is a vertex, since its pattern is accepted. Two elements have different random strings, and both patterns come from $\pi$, so they agree on shared positions. So $Q$ is a clique, of size $\mathrm{acc}(\pi)$.

($\le$) Let $Q$ be a clique. Two vertices with the same random string are not adjacent, so the random strings in $Q$ are distinct. Define a proof $\pi$: for each position $p$ read by some vertex of $Q$, let $\pi_p$ be the bit that this vertex gives to $p$; set the other positions to 0. This is well defined, because adjacent vertices agree on shared positions and all pairs in $Q$ are adjacent. For each $(\rho, a) \in Q$, $\pi|_{P(\rho)} = a \in A(\rho)$, so $V$ accepts $\pi$ on $\rho$. So $\mathrm{acc}(\pi) \ge |Q|$.

Size and time: there are $2^r$ random strings and at most $2^q$ patterns each. The construction runs $V$ on each random string to find $P(\rho)$, tests each pattern, and compares each pair of vertices. $\blacksquare$

The bound on the vertices is $2^r \cdot \max_\rho |A(\rho)|$. A verifier that accepts few patterns (few *free bits*) gives a smaller graph and a stronger result, which is the idea behind Håstad's theorem.

**Proof of Corollary 2.** By the [PCP theorem](/pcp-theorem/), SAT has a verifier with $r = O(\log n)$, a constant $q$, completeness 1 and soundness $1/2$. *Repetition:* let $V^{(k)}$ pick $k$ independent random strings, read the union of their positions, and accept when all $k$ tests accept. It uses $kr$ random bits and at most $kq$ queries, and for each proof $\pi$, $\mathrm{acc}_{V^{(k)}}(\pi) = \mathrm{acc}_V(\pi)^k$, because the $k$ strings range over all $k$-tuples. So completeness stays 1 and soundness becomes $2^{-k}$.

Take a constant $k$ with $2^{-k} < \alpha$. The graph $G = G_{V^{(k)}, w}$ has $N \le 2^{k(r + q)}$ vertices, a polynomial in $n$. If $w \in$ SAT, $\omega(G) = 2^{kr}$; otherwise $\omega(G) \le 2^{-k} \cdot 2^{kr}$. An $\alpha$-approximation returns a clique of size at least $\alpha\,2^{kr} > 2^{-k}\,2^{kr}$ on YES instances, and no clique on NO instances is that large. So it decides SAT, and P = NP.

For the second claim take $k = \lceil \log_2 n \rceil$. Then $\log_2 N \le k(r + q) = O(\log^2 n)$, so $N = n^{O(\log n)}$ and the construction takes time $n^{O(\log n)}$. The gap is $2^{-k} \le 1/n$, and $\log_2 n \ge c'\sqrt{\log_2 N}$ for a constant $c' > 0$. An approximation with ratio $2^{-c\sqrt{\log N}}$ for a small enough $c$ would separate the cases and put SAT in DTIME$(n^{O(\log n)})$. $\blacksquare$

**Sketch of Theorem 3 (sketch only).** Independent repetition costs $kr$ random bits, which makes the graph superpolynomial when $k$ grows. Instead, take the $k$ random strings along a random walk of length $k$ on an expander graph whose vertices are the $2^r$ random strings; see [expander walk sampler](/expander-walk-sampler/). The walk needs $r + O(k)$ random bits. Completeness stays 1. For soundness, a fixed proof is accepted on a set of at most half of the random strings, and the expander mixing property bounds the probability that all $k$ steps of the walk stay in that set by $2^{-\Omega(k)}$ (the approach of Alon, Feige, Wigderson and Zuckerman 1995; Arora and Barak, Section 22.2.4, use the same idea for independent set). With $k = \Theta(\log n)$ the graph has $N = 2^{O(\log n)}$ vertices, a polynomial, and the gap is $n^{-\Omega(1)} = N^{-\varepsilon}$ for a constant $\varepsilon > 0$.

**Theorems 4 and 5 (cited, not proved here).** Håstad builds PCPs whose amortized free bit complexity is below any constant, and uses randomness in the reduction, which is why his assumption is NP $\ne$ ZPP. Zuckerman replaces that randomness by linear degree dispersers (see [disperser](/disperser/)), which gives the same bound under P $\ne$ NP.

**Worked example.** Take the four clauses $(x_1 \lor x_2)$, $(\lnot x_1 \lor x_2)$, $(x_1 \lor \lnot x_2)$, $(\lnot x_1 \lor \lnot x_2)$, which no assignment satisfies; each assignment satisfies 3. The verifier reads an assignment, picks one of the 4 clauses at random and accepts if it is satisfied. Each test accepts 3 of the 4 patterns, so the FGLSS graph has 12 vertices; it has 12 edges and $\omega = 3$, the maximum acceptance count. For $x_1 = 1$, $x_2 = 0$, the clique uses the tests of clauses 1, 3 and 4. Two-fold repetition gives 16 tests and 36 vertices (3 patterns for each of the 4 repeated clauses, 2 for each of the 12 ordered pairs of different clauses), and $\omega = 9 = 3^2$.

**Brute-force check.** The Python code of this page builds the FGLSS graph of small random verifiers, computes its clique number by branch and bound, and checks Theorem 1 against the maximum acceptance count found by enumerating all proofs. It also checks the size bound, that each proof gives a clique, the worked example, and that repetition squares the acceptance count.

## Consequences

- **Independent set.** A clique of $G$ is an independent set of the complement graph, so all bounds hold for [maximum independent set](/maximum-independent-set/).
- **No constant ratio.** Clique is not in [APX](/apx-class/) unless P = NP. It is APX-hard, but outside APX.
- **Chromatic number.** The clique gaps, with more work, give the bounds of [graph coloring inapproximability](/graph-coloring-inapproximability/).
- **Vertex cover.** The complement map turns a clique gap $[cN, sN]$ into a vertex cover gap $[(1 - c)N, (1 - s)N]$. The bounds above have $c$ tending to 0, so they give little for vertex cover; see [vertex cover inapproximability](/vertex-cover-inapproximability/).
- **Clique in NP-hardness of approximation.** FGLSS was the first link between interactive proofs and hardness of approximation, and it led to the PCP theorem.

## Tightness

Returning one vertex gives ratio $1/N$. Feige (2004) gives a polynomial-time algorithm with ratio $(\log N)^3 / (N (\log \log N)^2)$, up to a constant factor. Theorem 5 shows that $N^{\varepsilon - 1}$ is impossible for each $\varepsilon > 0$, so the threshold is $N^{-1 + o(1)}$; the exact lower order term is open. Corollary 2 and Theorem 3, which this page proves or sketches, are far from tight.

## History

Feige, Goldwasser, Lovász, Safra and Szegedy (FOCS 1991, JACM 1996) introduced the graph of this page and, with a scaled-down version of the [multi-prover interactive proofs](/multi-prover-interactive-proofs/) for NEXP, proved that clique has no constant ratio and no $2^{-\log^{1 - \varepsilon} N}$ ratio unless NP has quasi-polynomial-time algorithms. Arora and Safra (1998) and Arora, Lund, Motwani, Sudan and Szegedy (1998) proved the PCP theorem, which gives $N^{-\varepsilon}$ under P $\ne$ NP. Bellare, Goldreich and Sudan introduced free bits and raised $\varepsilon$. Håstad (1999) reached $N^{\varepsilon - 1}$ under NP $\ne$ ZPP, and Zuckerman (2007) derandomized it to P $\ne$ NP.

## References
