---
tag: TJBKC0
kind: problem
slug: three-coloring
name: 3-colorability problem
aliases:
- 3-coloring
- 3-COL
area: complexity/reductions-catalogue
level: core
summary: Decide whether a graph's vertices can get three colors with no edge between two vertices of one color. NP-complete by a gadget reduction from 3-SAT; two colors is in P.
prereqs: [np-complete, 3-sat, graph-coloring, gadget-reduction]
see_also: [k-coloring, chromatic-number, bipartite-testing, planar-graph-coloring, four-color-theorem, brooks-theorem, graph-coloring-inapproximability, karps-21-np-complete-problems]
sources:
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Appendix A1.1, problem GT4 (Graph k-colorability), with the comments on k = 3, planar graphs and maximum degree 4
  - paper: doi:10.1145/1008293.1008294
    title: Larry Stockmeyer, Planar 3-colorability is polynomial complete, SIGACT News 5(3), 1973, pages 19 to 25
    locator: the main result (3-colorability is NP-complete, also for planar graphs)
  - paper: doi:10.1016/0304-3975(76)90059-1
    title: Michael R. Garey, David S. Johnson and Larry Stockmeyer, Some simplified NP-complete graph problems, Theoretical Computer Science 1(3), 1976
    locator: the result on planar graph 3-colorability with no vertex degree above 4
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: Richard M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, Plenum Press, 1972, pages 85 to 103
    locator: Section 4, problem 12 (CHROMATIC NUMBER) and its reduction from SATISFIABILITY WITH AT MOST 3 LITERALS PER CLAUSE
  - paper: doi:10.1006/jcss.2001.1774
    title: Russell Impagliazzo, Ramamohan Paturi and Francis Zane, Which problems have strongly exponential complexity?, Journal of Computer and System Sciences 63(4), 2001
    locator: the sparsification lemma and its use for problems with linear-size reductions from 3-SAT
---

The 3-colorability problem asks whether the vertices of a graph can be given three colors so that the two ends of every edge get different colors. It is the smallest case of [graph coloring](/graph-coloring/) that is hard: with two colors the question is whether the graph is bipartite, which [breadth-first search](/breadth-first-search/) answers in linear time, but with three colors it is [NP-complete](/np-complete/). Karp (1972) proved chromatic number NP-complete, and Stockmeyer (1973) proved that 3-colorability stays NP-complete on [planar graphs](/planar-graph/). This page gives the standard gadget reduction from [3-SAT](/3-sat/) with a full proof.

## In plain words

A country has several regions, and two regions that share a border must get different colors on the map. With only two colors there is a fast test: color one region, and every neighbor is then forced, so a conflict shows up at once.

With three colors, a choice does not force its neighbors, and wrong early choices can show up only much later. The reason this is hard is that three colors can imitate logic. One color plays "true", one plays "false", and the third is a helper. Small pieces of map, called gadgets, force each variable to be true or false and force each clause of a formula to contain a true part. So a coloring exists exactly when the formula can be satisfied.

## Definition

**Instance.** An undirected graph $G = (V, E)$.

**Question.** Is there a map $c : V \to \{1, 2, 3\}$ with $c(u) \ne c(v)$ for every edge $\{u, v\} \in E$?

**Encoding.** The graph is given as an adjacency list, so the input length is $\Theta(\lvert V \rvert + \lvert E \rvert)$ words up to logarithmic factors. The certificate is the coloring $c$, with two bits per vertex. The verifier checks every edge once, in $O(\lvert V \rvert + \lvert E \rvert)$ time on a [word RAM](/word-ram/), and in polynomial time on the [multitape Turing machine](/multitape-turing-machine/) on which classes are defined. So the problem is in NP.

**Complexity.** NP-complete under Karp (polynomial-time many-one) reductions. Stockmeyer (1973) proved this, also for planar graphs, and Garey, Johnson and Stockmeyer (1976) for planar graphs with no vertex of degree above 4. It is problem GT4 with $K = 3$ in Garey and Johnson.

## Variants

- **Two colors.** A graph is 2-colorable if and only if it is bipartite, if and only if it has no odd cycle. [Bipartite testing](/bipartite-testing/) decides this in $O(\lvert V \rvert + \lvert E \rvert)$ time, so 2-coloring is in P.
- **$k$ colors for $k \ge 4$.** Add one new vertex joined to every vertex. The new graph is $(k+1)$-colorable if and only if the old one is $k$-colorable, because the new vertex needs a color of its own. So [$k$-coloring](/k-coloring/) is NP-complete for every fixed $k \ge 3$, and computing the [chromatic number](/chromatic-number/) is NP-hard.
- **Planar graphs.** 3-coloring stays NP-complete on planar graphs, even with maximum degree 4 (Garey, Johnson and Stockmeyer 1976). In contrast, every planar graph is 4-colorable by the [four color theorem](/four-color-theorem/), so planar 4-coloring has the answer "yes" on every instance. See [planar graph coloring](/planar-graph-coloring/).
- **Maximum degree 3.** By [Brooks' theorem](/brooks-theorem/), a connected graph with maximum degree at most 3 is 3-colorable unless it is $K_4$. So on these graphs the problem is in P, and degree 4 is the smallest bound at which it is hard.
- **Coloring a 3-colorable graph.** Even when the graph is known to be 3-colorable, coloring it with a few more colors is hard; see [graph coloring inapproximability](/graph-coloring-inapproximability/).

## Examples

**A yes-instance and a no-instance.** The 5-cycle is 3-colorable but not 2-colorable, since it is an odd cycle: color the vertices 1, 2, 1, 2, 3 in order around the cycle. The complete graph $K_4$ is not 3-colorable, since its four vertices are pairwise adjacent and need four colors.

**The reduction on a small formula.** Take
$$\varphi = (x_1 \lor x_2 \lor \lnot x_3) \land (\lnot x_1 \lor x_2 \lor x_3) \land (\lnot x_1 \lor \lnot x_2 \lor \lnot x_3),$$
with $n = 3$ variables and $m = 3$ clauses. The construction in the Reductions section gives a graph with $3 + 2n + 6m = 27$ vertices and $3 + 3n + 12m = 48$ edges. A script built the graph and listed its colorings.

- **Forward.** The assignment $x_1 = 0, x_2 = 1, x_3 = 0$ satisfies $\varphi$. Color $x_2$, $\lnot x_1$ and $\lnot x_3$ with the color T, and their negations with F. In clause 1 the first OR gadget has the input $x_2$ colored T, so its output can be T, and the clause output is T. In the same way each clause has a true input, and the script confirmed that the coloring extends to the whole graph.
- **Backward.** With the three palette vertices fixed to T, F and B, the graph has 88 proper colorings. The script read an assignment from each one ($x_i$ is true when its vertex has color T). The 88 colorings give exactly 5 different assignments, and these are the 5 satisfying assignments of $\varphi$: 000, 010, 011, 101 and 110.
- **No-instances.** The formula with all 8 clauses on $x_1, x_2, x_3$ is unsatisfiable, and its graph is not 3-colorable. The script also compared the reduction with brute force on 200 random satisfiable formulas and on 60 dense formulas, 20 of them unsatisfiable, and the graph was 3-colorable exactly when the formula was satisfiable.

## Known algorithms

- **Brute force.** Try all $3^n$ colorings, where $n = \lvert V \rvert$; each test takes $O(n + \lvert E \rvert)$ time.
- **Through chromatic number.** [Lawler's algorithm](/lawler-chromatic-number/) computes the chromatic number by dynamic programming over subsets of vertices, and the [inclusion-exclusion principle](/inclusion-exclusion-principle/) gives a $2^n n^{O(1)}$ time algorithm for the chromatic number. Both decide 3-colorability.
- **Heuristics.** [Greedy coloring](/greedy-coloring/) and [DSatur](/dsatur/) run in polynomial time but may use more than three colors on a 3-colorable graph.
- **Special graphs.** On graphs with maximum degree 3, the proof of [Brooks' theorem](/brooks-theorem/) gives a polynomial-time algorithm. On graphs of bounded treewidth, dynamic programming over a tree decomposition decides the problem in linear time for each fixed width.

## Bounds

- **NP-completeness.** There is no polynomial-time algorithm unless P = NP.
- **Exponential time.** The reduction below maps a 3-CNF formula with $n$ variables and $m$ clauses to a graph with $O(n + m)$ vertices. By the sparsification lemma of Impagliazzo, Paturi and Zane (2001), the exponential time hypothesis then implies that 3-coloring has no algorithm with time $2^{o(\lvert V \rvert)}$.
- **Complement.** Deciding that a graph is not 3-colorable is [coNP-complete](/co-np-complete/).

## Reductions

**From 3-SAT (Karp reduction).** Let $\varphi$ have variables $x_1, \ldots, x_n$ and clauses $C_1, \ldots, C_m$, each with exactly three literals.

*Map.* Build the graph $G_\varphi$ in three parts.

1. **Palette.** A triangle on three vertices T, F and B. In every proper 3-coloring they get three different colors, and we name each color after its palette vertex.
2. **Variable gadget.** For each variable $x_i$, two vertices $x_i$ and $\lnot x_i$, and a triangle on $x_i$, $\lnot x_i$ and B. So each literal vertex has color T or F, and $x_i$ and $\lnot x_i$ have different colors.
3. **Clause gadget.** An *OR gadget* with inputs $a$ and $b$ is a new triangle $p, q, r$ with the edges $a$-$p$ and $b$-$q$; its output is $r$. For the clause $(\ell_1 \lor \ell_2 \lor \ell_3)$, build an OR gadget with inputs $\ell_1, \ell_2$ and output $r_1$, then an OR gadget with inputs $r_1, \ell_3$ and output $r_2$, and join $r_2$ to F and to B. So $r_2$ must have color T.

*Cost.* The graph has $3 + 2n + 6m$ vertices and $3 + 3n + 12m$ edges, and each part is written in constant time per variable or clause. So the map runs in time $O(n + m)$, which is polynomial (it is even computable in logarithmic space).

*OR gadget lemma.* Let $a$ and $b$ have colors in $\{T, F\}$ in a proper coloring. (1) If $a$ and $b$ both have color F, then $r$ has color F in every proper extension. (2) If $a$ or $b$ has color T, then the gadget has a proper extension in which $r$ has color T.

*Proof of (1).* The vertex $p$ is adjacent to $a$, so $c(p) \ne F$, and in the same way $c(q) \ne F$. Since $p$ and $q$ are adjacent, they take T and B in some order. The vertex $r$ is adjacent to both, so $c(r) = F$.

*Proof of (2).* Say $c(a) = T$; the case $c(b) = T$ is symmetric. Give $r$ the color T. If $c(b) = F$, give $q$ the color B and $p$ the color F. If $c(b) = T$, give $q$ the color F and $p$ the color B. In both cases $p \ne c(a) = T$, $q \ne c(b)$, and $p, q, r$ have three different colors.

The second OR gadget has input $r_1$, which might have color B. The proof only uses the cases where $r_1$ has color T or F, as the two directions below show.

*If $\varphi$ is satisfiable, then $G_\varphi$ is 3-colorable.* Fix a satisfying assignment. Color T, F and B with their own colors, each true literal with T and each false literal with F. For a clause with literals $\ell_1, \ell_2, \ell_3$: if $\ell_1$ or $\ell_2$ is true, color the first gadget by (2) so that $r_1$ has color T, and then color the second gadget by (2) with $r_2$ colored T. If $\ell_1$ and $\ell_2$ are both false, then $\ell_3$ is true. The first gadget has a proper extension, with $r_1$ colored F by (1): take $p$ and $q$ as T and B. Then the second gadget has the input $\ell_3$ colored T, and (2) gives $r_2$ the color T. In all cases $r_2$ has color T, which differs from F and B, and gadgets of different clauses share only literal and palette vertices. So the coloring is proper.

*If $G_\varphi$ is 3-colorable, then $\varphi$ is satisfiable.* Let $c$ be any proper 3-coloring. The palette triangle uses all three colors; name them T, F and B after their vertices. Each literal vertex is adjacent to B, so it has color T or F, and $x_i$ and $\lnot x_i$ have different colors. Set $x_i$ true if and only if $c(x_i) = T$; then a literal is true exactly when its vertex has color T. Suppose some clause $(\ell_1 \lor \ell_2 \lor \ell_3)$ has all three literals false. By (1), $r_1$ has color F. Then the second gadget has two inputs colored F, and by (1) again $r_2$ has color F. But $r_2$ is adjacent to F, a contradiction. So every clause has a true literal.

*Membership.* The certificate and verifier are under Definition. With the NP-completeness of 3-SAT, this proves that 3-colorability is NP-complete. This is the construction of the [gadget reduction](/gadget-reduction/) page, which uses it as one of its examples.

**Other reductions.** Karp's own reduction to chromatic number is different; it uses a clique on the variables and one vertex per clause, and is proved on [Karp's reduction tree](/karp-21-np-complete/). From 3-colorability, adding apex vertices gives $k$-coloring for every $k \ge 3$, as under Variants. Planar 3-colorability uses a planar crossover gadget that replaces each crossing of two edges.

## Applications

- **Hardness of scheduling and allocation.** Register allocation, exam timetabling and frequency assignment are coloring problems; 3-colorability shows that their exact versions are hard even with three registers, time slots or frequencies. See [graph coloring](/graph-coloring/).
- **A source problem.** 3-coloring is a common source for NP-hardness proofs of problems on planar or bounded-degree graphs, because it stays hard there.
- **Hardness of approximation.** The hardness of coloring 3-colorable graphs with few colors starts from this problem; see [graph coloring inapproximability](/graph-coloring-inapproximability/).

## References
