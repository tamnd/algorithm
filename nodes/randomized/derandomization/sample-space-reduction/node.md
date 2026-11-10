---
tag: R8N057
kind: technique
slug: sample-space-reduction
name: Sample space reduction
aliases:
- small sample space method
- derandomization by small sample spaces
- exhaustive search over a small sample space
area: randomized/derandomization
level: core
summary: Replaces a fully random choice by a small structured sample space that still supports the needed probability bound, then searches it exhaustively.
prereqs: [k-wise-independence, limited-independence, linearity-of-expectation]
see_also: [method-of-conditional-expectations, pessimistic-estimators, small-bias-sample-space, luby-mis, maximal-independent-set, maximum-cut, nc, pseudorandom-generator]
sources:
  - paper: doi:10.1137/0215074
    title: Michael Luby, A simple parallel algorithm for the maximal independent set problem, SIAM Journal on Computing 15(4), 1986
    locator: pages 1036 to 1053 (the pairwise independent analysis and the deterministic NC algorithm by search of a small sample space)
  - paper: doi:10.1016/0196-6774(86)90019-2
    title: Noga Alon, László Babai and Alon Itai, A fast and simple randomized parallel algorithm for the maximal independent set problem, Journal of Algorithms 7(4), 1986
    locator: pages 567 to 583 (small k-wise independent sample spaces and their use for derandomization)
  - book: isbn:9781119061953
    title: Noga Alon and Joel H. Spencer, The Probabilistic Method, fourth edition, Wiley, 2016
    locator: Chapter 16, Section 16.2 (d-wise independent random variables in small sample spaces)
  - paper: doi:10.1561/0400000010
    title: Salil P. Vadhan, Pseudorandomness, Foundations and Trends in Theoretical Computer Science 7(1-3), 2012
    locator: Chapter 3, Sections 3.1 (enumeration) and 3.5 (pairwise independence, with MAX-CUT over a pairwise independent space)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Chapter 15 (pairwise independence and universal hash functions, with derandomization by small sample spaces)
---

Sample space reduction derandomizes an algorithm whose analysis uses only a weak form of independence, such as [k-wise independence](/k-wise-independence/) for a constant $k$. The random choices are replaced by the coordinates of a uniform point of a sample space with that property and with only polynomially many points, and the deterministic algorithm tries every point. Since the analysis still holds over the small space, some point is at least as good as the average. Luby (1986) and Alon, Babai and Itai (1986) used it to give deterministic parallel algorithms for [maximal independent set](/maximal-independent-set/), since the points can be tried at the same time.

## In plain words

A randomized algorithm flips many coins, so there are too many outcomes to try them all. But often the proof that it works only looks at two or three coins at a time. Then the coins can come from a short list of outcomes, built so that any two or three coins in it look like fair independent coins. The proof works the same with the short list, so the average outcome over the list is as good as the proof says.

If the average is good, at least one outcome on the list is good. So try every outcome on the list and keep the best one. The list has a size that is a power of the input size, so this takes polynomial time, and all outcomes can be tried in parallel.

## When it applies

Notation. $X = (X_1, \ldots, X_n)$ are the random choices of the algorithm. $f(X)$ is the quantity to make large (or the indicator of success). $\Omega$ is the small sample space, $s \in \Omega$ a seed, and $G(s) \in D^n$ the choices that it gives. $\Pr_{s}$ and $\mathrm{E}_{s}$ are over a uniform $s \in \Omega$.

Use the method when:

- The analysis proves $\mathrm{E}[f(X)] \ge \mu$ (or $\Pr[\text{success}] > 0$) and uses only a property that a small space has. The usual property is $k$-wise independence with uniform or fixed marginals, because then every expectation of a function of $k$ choices is the same as under full independence. Other properties are small bias for parity tests ([small-bias sample spaces](/small-bias-sample-space/)) and almost $k$-wise independence.
- A space $\Omega$ with that property has polynomial size and $G(s)$ is easy to compute. For $k$-wise independent choices over a field of size $q \ge n$, $|\Omega| = q^k$; for $k$-wise independent bits, about $n^{\lfloor k/2 \rfloor}$ points (see [k-wise independence](/k-wise-independence/)). The number of random bits is $\log_2 |\Omega| = O(k \log n)$.
- $f$ can be computed for a fixed choice.

If the analysis needs exponential tail bounds such as the [Chernoff bound](/chernoff-bound/), $k$ must grow like the logarithm of the error, and the space no longer has polynomial size; use [pessimistic estimators](/pessimistic-estimators/) instead.

## The template

```pseudo id=main
SAMPLE-SPACE-REDUCTION(input, Ω, G, f)   ▷ the analysis holds over Ω
L1  best ← none
L2  for each seed s in Ω do              ▷ can run in parallel
L3      x ← G(s)
L4      if best = none or f(x) > f(best) then best ← x
L5  return best
```

**Claim.** If $\mathrm{E}_s[f(G(s))] \ge \mu$, the returned $x$ has $f(x) \ge \mu$.

*Proof.* The maximum of a finite list of numbers is at least their average, and line L4 keeps the maximum. $\square$

The work is in the first step, not the template: show that the analysis of the randomized algorithm uses only the property of $\Omega$, so that $\mathrm{E}_s[f(G(s))] \ge \mu$ still holds. With [linearity of expectation](/linearity-of-expectation/), this is often immediate: if $f$ is a sum of terms that each depend on at most $k$ choices, each term has the same expectation over a $k$-wise independent space as over the full space.

**Cost.** $|\Omega|$ evaluations of $G$ and $f$. With $|\Omega| = n^{O(k)}$ this is polynomial for constant $k$. Run in parallel, the depth is the depth of one evaluation plus $O(\log |\Omega|)$ for the maximum.

## Classic examples

### Maximum cut over a pairwise independent space

The random cut that puts each vertex on a random side cuts each edge with probability $1/2$. This uses only that the two sides of the ends of an edge are independent and uniform, so it holds over any pairwise independent space. Give the $n \le 2^m - 1$ vertices distinct nonzero labels $a_v \in \{0,1\}^m$, and for a seed $y \in \{0,1\}^m$ put $v$ on side $\langle a_v, y \rangle \bmod 2$. The space has $2^m \le 2n$ points, and some seed gives a cut of at least $m_E/2$ edges, where $m_E$ is the number of edges.

Example: 7 vertices with labels 001 to 111, and the 10 edges of the 7-cycle 0-1-2-3-4-5-6-0 together with 03, 15 and 26. The 8 seeds $y = 000, 001, \ldots, 111$ give cuts of sizes

$$0, 7, 4, 5, 5, 8, 5, 6,$$

with average exactly $40/8 = 5 = m_E/2$. The best seed, $y = 101$, gives 8 cut edges. The maximum cut of this graph has 9 edges, so the search over the small space finds a good cut, not an optimal one. The seed $y = 000$ puts all vertices on one side, so some seeds are very bad, as for truly random cuts.

### MAX-3SAT over a 3-wise independent space

A clause with 3 literals on 3 distinct variables depends on 3 bits only. Over a 3-wise independent and uniform assignment it is satisfied with probability $7/8$, as under full independence. The space of the vectors $(1, v)$ in [k-wise independence](/k-wise-independence/) gives $n \le 2^m$ variables with $2^{m+1} \le 4n$ points. So one of at most $4n$ assignments satisfies at least $7/8$ of the clauses, and trying them all is a parallel algorithm for the same guarantee as the [method of conditional expectations](/method-of-conditional-expectations/).

### Maximal independent set in NC (Luby 1986)

In each round of Luby's algorithm ([Luby's MIS](/luby-mis/)), each vertex $v$ marks itself with probability $1/(2 \deg(v))$. If both ends of an edge are marked, the end of lower degree is unmarked. The marked vertices join the independent set, and they and their neighbours are deleted. Luby proved that a constant fraction of the edges is deleted in expectation, and his proof uses only that the marks are pairwise independent. So he took the marks from a pairwise independent space of polynomial size, built from a linear function $a + b v$ modulo a prime $q$ with the probabilities rounded to multiples of $1/q$. In each round the algorithm tries every point of the space in parallel and keeps one that deletes at least the expected number of edges. After $O(\log n)$ rounds the graph is empty, which gives a deterministic [NC](/nc/) algorithm. Alon, Babai and Itai (1986) gave a closely related algorithm and the general small spaces of $k$-wise independent variables, with the lower bound that shows their size is nearly optimal.

## Variations

- **Conditional expectations on the seed.** In place of trying all $|\Omega|$ seeds, fix the $\log_2 |\Omega|$ seed bits one at a time with the [method of conditional expectations](/method-of-conditional-expectations/). This needs the conditional expectation over the remaining seed bits, which is often computable term by term. It reduces the work, and it is the basis of NC algorithms that use $O(\log n)$-wise independence, where the space is too large to search.
- **Small-bias spaces.** If the analysis only tests parities, or needs almost $k$-wise independence, [small-bias sample spaces](/small-bias-sample-space/) are much smaller than exact $k$-wise independent spaces when $k$ grows with $n$.
- **Pseudorandom generators.** A [pseudorandom generator](/pseudorandom-generator/) is the general form of the method: a small space that fools a whole class of tests, not only the tests of one analysis. The method of this page is the case where the class is "functions of at most $k$ choices".
- **Hitting sets.** If the analysis shows only $\Pr[\text{success}] > 0$, the space needs only to hit every large enough set, see [hitting set generators](/hitting-set-generator/).

## Pitfalls

- **Check that the analysis transfers.** Statements such as "with high probability every vertex has degree close to its mean" usually need exponential tails and fail over a pairwise independent space. Only the expectations of functions of at most $k$ choices are guaranteed to be the same.
- **Marginal probabilities.** A uniform space over $\mathrm{GF}(2^m)$ gives probabilities that are multiples of $2^{-m}$. If the analysis needs a probability such as $1/(2 \deg(v))$, round it and repeat the analysis with the rounded values.
- **The size grows with $k$.** The space has about $n^{k/2}$ points or more, and the lower bound of [k-wise independence](/k-wise-independence/) says this cannot be improved much. Exact search is practical only for $k \le 3$ or 4.
- **The guarantee is the average.** The best seed of the space can be far from optimal; in the example above, 8 against an optimum of 9.

## Exercises

1. Show that the Hadamard space of this page, used for max cut, also gives a cut of at least $m_E/2$ edges when the labels are any vectors such that the two ends of each edge get different labels. What does this say about graphs with a small chromatic number?
2. Use a pairwise independent space to find, in polynomial time and with no randomness, a set of at least $n/(4\Delta)$ vertices that is independent in a graph of maximum degree $\Delta \ge 1$ on $n$ vertices. (Hint: mark each vertex with a probability between $1/(2\Delta)$ and $1/\Delta$, then delete one end of each edge with both ends marked.)
3. A formula has clauses with exactly $k$ literals on distinct variables. How large must a sample space be for the method to find an assignment satisfying $(1 - 2^{-k})$ of the clauses?
4. Show that the max cut bound holds for a seed $y$ chosen with any distribution for which every bit $\langle a, y \rangle$, $a \ne 0$, is unbiased. Which spaces have this property?

## References
