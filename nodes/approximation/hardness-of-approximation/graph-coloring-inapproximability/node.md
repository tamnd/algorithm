---
tag: 92EGHS
kind: theorem
slug: graph-coloring-inapproximability
name: Graph coloring inapproximability
aliases:
- chromatic number hardness
area: approximation/hardness-of-approximation
level: research
summary: The chromatic number has no ratio below 4/3 unless P = NP, since 3-coloring is NP-hard. Feige and Kilian and then Zuckerman showed that no ratio n to the power 1 - ε is possible either.
prereqs: [chromatic-number, clique-inapproximability, three-coloring]
see_also: [graph-coloring, k-coloring, clique-number, independence-number, lovasz-theta-function, gap-problem, approximation-threshold, zpp]
sources:
  - paper: doi:10.1016/0304-3975(76)90059-1
    title: Michael R. Garey, David S. Johnson and Larry Stockmeyer, Some simplified NP-complete graph problems, Theoretical Computer Science 1(3), 1976
    locator: The NP-completeness of graph 3-colorability
  - paper: doi:10.1145/321921.321926
    title: Michael R. Garey and David S. Johnson, The complexity of near-optimal graph coloring, Journal of the ACM 23(1), 1976
    locator: The main theorem (no polynomial-time algorithm uses fewer than about twice the chromatic number plus a constant, unless P = NP)
  - paper: doi:10.1145/185675.306789
    title: Carsten Lund and Mihalis Yannakakis, On the hardness of approximating minimization problems, Journal of the ACM 41(5), 1994
    locator: The n to the power ε bound for chromatic number unless P = NP
  - paper: doi:10.1006/jcss.1998.1587
    title: Uriel Feige and Joe Kilian, Zero knowledge and the chromatic number, Journal of Computer and System Sciences 57(2), 1998
    locator: The main theorem, n to the power 1 - ε unless NP = ZPP
  - paper: doi:10.4086/toc.2007.v003a006
    title: David Zuckerman, Linear degree extractors and the inapproximability of max clique and chromatic number, Theory of Computing 3, 2007
    locator: The derandomized bound for chromatic number, n to the power 1 - ε unless P = NP
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, W. H. Freeman, 1979
    locator: Chapter 6, Section 6.2 (approximation of graph coloring and the factor 4/3 from 3-colorability)
---

The [chromatic number](/chromatic-number/) $\chi(G)$ is the least number of colors in a proper coloring of a graph. It is as hard to approximate as [maximum clique](/clique-inapproximability/). This page proves the simplest bound in full: since [3-coloring](/three-coloring/) is NP-complete, no polynomial-time algorithm has ratio below $4/3$ unless P = NP. That bound matters only for graphs with few colors. For general graphs, Lund and Yannakakis (1994) proved a bound $n^{\varepsilon}$, Feige and Kilian (1998) proved $n^{1 - \varepsilon}$ for each $\varepsilon > 0$ under NP $\ne$ [ZPP](/zpp/), and Zuckerman (2007) proved the same under P $\ne$ NP; these are cited, with a sketch of the common idea.

## Statement

**Notation.** $G$ is a graph on $n$ vertices; $\chi(G)$ is its chromatic number, $\alpha(G)$ its [independence number](/independence-number/) and $\omega(G)$ its clique number. Coloring is a minimization problem, so a $\rho$-approximation returns a proper coloring with at most $\rho\,\chi(G)$ colors, $\rho \ge 1$. In the literature "$n^{1 - \varepsilon}$-hardness" means $\rho = n^{1 - \varepsilon}$.

**Theorem 1 (the $4/3$ bound; proved here).** Unless P = NP, there is no polynomial-time $\rho$-approximation for the chromatic number with $\rho < 4/3$.

**Lemma 2 (proved here).** For each graph, $\chi(G) \ge n / \alpha(G)$ and $\chi(G) \ge \omega(G)$.

**Theorem 3 (Garey and Johnson 1976; cited).** Unless P = NP, for each constant $r < 2$ and each constant $d$, no polynomial-time algorithm colors every graph with at most $r\,\chi(G) + d$ colors.

**Theorem 4 (Lund and Yannakakis 1994; cited).** There is a constant $\varepsilon > 0$ such that, unless P = NP, there is no polynomial-time $n^{\varepsilon}$-approximation for the chromatic number.

**Theorem 5 (Feige and Kilian 1998; cited).** For each $\varepsilon > 0$, unless NP = ZPP, there is no polynomial-time $n^{1 - \varepsilon}$-approximation for the chromatic number.

**Theorem 6 (Zuckerman 2007; cited).** For each $\varepsilon > 0$, unless P = NP, there is no polynomial-time $n^{1 - \varepsilon}$-approximation for the chromatic number.

## In plain words

Coloring a map or a graph means giving each point a color so that neighbours differ, with as few colors as possible. Deciding whether three colors are enough is already one of the classic hard problems. So no fast method can promise to use fewer than four colors on every graph that needs only three, and that already rules out getting within a factor of four thirds. For graphs that need many colors, much stronger results hold. Hard instances are built so that in one case the graph splits into a few groups with no edges inside, and in the other case every group with no edges inside is tiny, so very many colors are needed. A fast method could tell these cases apart if it came within a factor close to the number of vertices, and that would make NP problems easy.

## Proof

**Proof of Theorem 1.** Let $\mathcal{A}$ be a polynomial-time algorithm that returns a proper coloring with at most $\rho\,\chi(G)$ colors, with $\rho < 4/3$. Given a graph $G$ with at least one edge, run $\mathcal{A}$ and let $k$ be the number of colors it uses. If $\chi(G) \le 3$, then $k \le \rho\,\chi(G) < (4/3) \cdot 3 = 4$, so $k \le 3$, because $k$ is an integer. If $\chi(G) \ge 4$, then $k \ge \chi(G) \ge 4$, because the coloring is proper. So "$k \le 3$?" decides 3-colorability (graphs with no edge are 1-colorable). 3-colorability is NP-complete (Garey, Johnson and Stockmeyer 1976), so P = NP. $\blacksquare$

In the language of [gap problems](/gap-problem/), the NP-hardness of 3-coloring is the NP-hardness of the gap "$\chi \le 3$" versus "$\chi \ge 4$", and the argument above is the gap-to-ratio step for integer values.

**Proof of Lemma 2.** Each color class of a proper coloring is an independent set, so it has at most $\alpha(G)$ vertices. The $\chi(G)$ classes cover all $n$ vertices, so $n \le \chi(G)\,\alpha(G)$. The vertices of a clique need pairwise different colors, so $\chi(G) \ge \omega(G)$. $\blacksquare$

**Why Theorem 1 says nothing for large $\chi$.** Take any 3-colorable graph $H$ and a graph $K$ with large chromatic number $t$. The disjoint union has chromatic number $t$, and an algorithm that colors $K$ optimally and $H$ with 4 colors still has ratio 1. A gap of one color matters only when $\chi$ is a small constant. For a ratio that grows with $n$, the gap must grow too.

**Sketch of Theorems 5 and 6 (sketch only).** The reductions start from a PCP verifier for an NP language and build a graph $G$ on $N$ vertices from its accepting views, in the spirit of the FGLSS graph of [clique inapproximability](/clique-inapproximability/), but with the roles arranged for coloring.

- *YES case: few independent sets cover the graph.* If the input is in the language, there are many correct proofs, and the graph is built so that the views consistent with each correct proof form an independent set, and a small number of such sets, at most $N^{\varepsilon}$, cover all vertices. So $\chi(G) \le N^{\varepsilon}$.
- *NO case: every independent set is small.* If the input is not in the language, soundness of the verifier, amplified as in [gap amplification](/gap-amplification/), bounds each independent set by $\alpha(G) \le N^{\varepsilon}$. By Lemma 2, $\chi(G) \ge N / \alpha(G) \ge N^{1 - \varepsilon}$.

The ratio between the cases is $N^{1 - 2\varepsilon}$, and $\varepsilon$ is arbitrary. The covering property in the YES case is the hard new part compared with clique: Feige and Kilian obtain it from verifiers with a zero-knowledge type property and from randomized constructions, which is why their assumption is NP $\ne$ ZPP. Zuckerman replaces the random choices by explicit linear degree dispersers, which gives the result under P $\ne$ NP. Lund and Yannakakis had earlier obtained $N^{\varepsilon}$ for a small fixed $\varepsilon$ through a reduction from a two-prover proof system and graph products.

## Consequences

- **Not in APX.** The chromatic number has no constant ratio unless P = NP, so it is outside [APX](/apx-class/), with threshold $n^{1 - o(1)}$ like clique.
- **Related problems.** Clique cover is coloring of the complement graph, so it has the same bounds. Fractional chromatic number has the same $n^{1 - \varepsilon}$ hardness, since the reductions bound it through Lemma 2 in the NO case and through the cover by independent sets in the YES case.
- **Lower bounds by relaxations.** Lemma 2 gives $\chi \ge \omega$ and $\chi \ge n/\alpha$, both NP-hard to compute. The [Lovász theta function](/lovasz-theta-function/) of the complement lies between $\omega(G)$ and $\chi(G)$ and is computable in polynomial time, but by the theorems above it can be far from $\chi$.

## Tightness

Any graph can be colored with $n$ colors, and Halldórsson (1993) gives ratio $O(n (\log \log n)^2 / (\log n)^3)$, so the hardness $n^{1 - \varepsilon}$ is tight up to the lower order term. For graphs with small chromatic number the picture is different. Wigderson (1983) colors 3-colorable graphs with $O(\sqrt{n})$ colors, and semidefinite programming improves this to $n^{c}$ for constants $c$ well below $1/2$. On the hardness side, coloring a 3-colorable graph with 4 colors is NP-hard (Khanna, Linial and Safra), and later work raised 4 to 5. The gap between "a constant number of colors is NP-hard" and "$n^{c}$ colors are possible" is a major open problem.

## History

Garey, Johnson and Stockmeyer (1976) proved that 3-coloring is NP-complete, which gives Theorem 1. Garey and Johnson (1976) improved it to Theorem 3, a factor close to 2 with any additive constant. Lund and Yannakakis (1994) proved the first polynomial factor $n^{\varepsilon}$, by reductions from two-prover proof systems that came out of the PCP work. Feige and Kilian (1998) reached $n^{1 - \varepsilon}$ under NP $\ne$ ZPP, building on Håstad's clique result. Zuckerman (2007) derandomized both Håstad's clique bound and the Feige and Kilian coloring bound with linear degree extractors and dispersers, so that both now hold under P $\ne$ NP.

## References
