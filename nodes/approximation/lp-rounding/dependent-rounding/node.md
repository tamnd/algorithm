---
tag: VR57AT
kind: technique
slug: dependent-rounding
name: Dependent rounding
aliases:
- Gandhi et al. dependent rounding
- dependent randomized rounding
- bipartite dependent rounding
- Srinivasan level-set rounding
area: approximation/lp-rounding
level: advanced
summary: Randomized rounding that keeps chosen sums and degrees of the fractional solution, via cycles and paths in a bipartite graph, with exact marginals and negative correlation.
prereqs: [randomized-rounding, bipartite-graph, linearity-of-expectation, chernoff-bound]
see_also: [pipage-rounding, swap-rounding, randomized-rounding, linear-programming-rounding, bipartite-matching, max-coverage, generalized-assignment-problem, independent-random-variables]
sources:
  - paper: doi:10.1145/1147954.1147956
    title: Rajiv Gandhi, Samir Khuller, Srinivasan Parthasarathy and Aravind Srinivasan, Dependent rounding and its applications to approximation algorithms, Journal of the ACM 53(3), 2006
    locator: pages 324 to 360
  - paper: "Aravind Srinivasan, Distributions on level-sets with applications to approximation algorithms, Proceedings of the 42nd IEEE Symposium on Foundations of Computer Science (FOCS), 2001"
    locator: pages 588 to 597
---

Dependent rounding is a randomized rounding for values on the edges of a [bipartite graph](/bipartite-graph/) that keeps the degree of each vertex, up to rounding, while each edge keeps its probability. Independent [randomized rounding](/randomized-rounding/) gets the probabilities right, but a vertex whose fractional degree is 1 can end with degree 0 or 2. Dependent rounding moves value around cycles and maximal paths of fractional edges, alternately up and down, so that the sum at each inner vertex does not change. Gandhi, Khuller, Parthasarathy and Srinivasan (2006) proved three properties: exact marginals, degrees in $\{\lfloor d_v \rfloor, \lceil d_v \rceil\}$, and negative correlation of the edges at each vertex. The last property lets Chernoff bounds hold for sums at a vertex, as for independent coins. Srinivasan (2001) had given the case of a star, which rounds a vector and keeps its sum.

## In plain words

Picture people on one side, jobs on the other, and a share of each job given to each person. Each person must get a whole number of jobs, close to the share total. Flipping a coin for each pair gets each pair right on average, but a person can end with too many or too few jobs.

Dependent rounding moves shares in a loop: one pair gains a bit, the next loses the same bit, and so on around the loop. Each person on the loop gains on one pair and loses on another, so the total stays the same. A coin with carefully chosen odds decides the direction, so on average each pair keeps its share. Each move makes at least one share whole, so the process ends.

## When it applies

- **Values on a bipartite graph.** The fractional solution is $x \in [0, 1]^E$ on the edges of a bipartite graph $G = (A \cup B, E)$, such as an assignment of jobs to machines or of items to groups.
- **Degree constraints.** The LP has constraints on the sums $d_v = \sum_{e \ni v} x_e$, and the rounded solution must keep them, up to rounding.
- **Concentration at a vertex.** The analysis needs tail bounds or expectations of products of edges at one vertex, which negative correlation gives.

## The template

```pseudo id=main
DEPENDENT-ROUND(G, x)
L1  while some edge has 0 < x_e < 1
L2      F ← the edges with 0 < x_e < 1
L3      P ← a cycle in F, or else a maximal path in F                      ▷ hole: FIND
L4      split P into alternate edge sets M1 and M2
L5      α ← min( min_{e ∈ M1} (1 − x_e), min_{e ∈ M2} x_e )
L6      β ← min( min_{e ∈ M1} x_e, min_{e ∈ M2} (1 − x_e) )
L7      with probability β/(α+β): x_e += α on M1, x_e −= α on M2
L8      else: x_e −= β on M1, x_e += β on M2
L9  return x                                                               ▷ now in {0,1}^E
```

The graph is bipartite, so a cycle in $F$ has even length and the alternate split in line L4 is well defined. If $F$ has no cycle it is a forest, and a maximal path ends at two vertices with exactly one fractional edge each.

**Theorem (Gandhi et al.).** Let $X \in \{0, 1\}^E$ be the output. Then:

1. *Marginals:* $\Pr[X_e = 1] = x_e$ for each edge $e$.
2. *Degrees:* $\sum_{e \ni v} X_e \in \{ \lfloor d_v \rfloor, \lceil d_v \rceil \}$ for each vertex $v$, with probability 1.
3. *Negative correlation:* for each vertex $v$ and each set $S$ of edges at $v$, $\Pr[\bigwedge_{e \in S} X_e = 1] \le \prod_{e \in S} x_e$ and $\Pr[\bigwedge_{e \in S} X_e = 0] \le \prod_{e \in S} (1 - x_e)$.

*Proof.* Each step changes the edges of $M1$ by a random $\Delta$ and those of $M2$ by $-\Delta$, where $\Delta = \alpha$ with probability $\beta/(\alpha+\beta)$ and $\Delta = -\beta$ with probability $\alpha/(\alpha+\beta)$. So $\mathbb{E}[\Delta] = \frac{\alpha \beta - \beta \alpha}{\alpha + \beta} = 0$, and each $x_e$ is a martingale. The choice of $\alpha$ and $\beta$ keeps all values in $[0, 1]$ and makes at least one edge integral, so there are at most $|E|$ steps, and item 1 follows. An inner vertex of $P$ has one edge in $M1$ and one in $M2$, so its sum does not change. An end of a maximal path has one fractional edge, so its sum is an integer plus that edge, and stays in $[\lfloor d_v \rfloor, \lceil d_v \rceil]$; this gives item 2. For item 3, at most two edges at $v$ change in a step. If one changes, $\prod_{e \in S} x_e$ changes by a multiple of $\Delta$ and its expectation does not change. If two change, by $\Delta$ and $-\Delta$, the factor $(x_e + \Delta)(x_f - \Delta)$ has expectation $x_e x_f - \mathbb{E}[\Delta^2] \le x_e x_f$. So the expectation of the product does not grow, and at the end the product is the indicator of the event. The same proof with $1 - x_e$ gives the second bound. $\square$

Each step finds a cycle or path in $O(|V| + |E|)$ time, so the whole rounding takes $O(|E| (|V| + |E|))$ time in the worst case.

**The hole.** FIND picks the cycle or path. Any choice gives the theorem; a choice that uses long cycles makes more edges integral per step.

## Classic examples

- **A 4-cycle.** Let $a_1 b_1 a_2 b_2$ be a 4-cycle with $x_e = \frac12$ on each edge, so each vertex has degree 1. Then $M1 = \{a_1 b_1, a_2 b_2\}$, $M2 = \{b_1 a_2, b_2 a_1\}$, $\alpha = \beta = \frac12$, and with probability $\frac12$ each, the output is one of the two perfect matchings. Each vertex has degree 1. Independent rounding gives $a_1$ degree 0 or 2 with probability $\frac12$.
- **A path.** Let $a_1 b_1 a_2$ have $x = (0.3, 0.4)$, so $M1 = \{a_1 b_1\}$, $M2 = \{b_1 a_2\}$, $\alpha = \min(0.7, 0.4) = 0.4$ and $\beta = \min(0.3, 0.6) = 0.3$. With probability $\frac37$ the values become $(0.7, 0)$, and with probability $\frac47$ they become $(0, 0.7)$. The expectations are $\frac37 \cdot 0.7 = 0.3$ and $\frac47 \cdot 0.7 = 0.4$, and $b_1$ keeps its degree $0.7$. One more step rounds the remaining edge to 1 with probability $0.7$, so $b_1$ ends with degree 0 or 1.
- **Keeping a sum.** On a star with center $v$, the rounding turns $x \in [0, 1]^n$ into $X \in \{0, 1\}^n$ with $\Pr[X_i = 1] = x_i$, $\sum_i X_i \in \{\lfloor \sum_i x_i \rfloor, \lceil \sum_i x_i \rceil\}$, and negative correlation. This is Srinivasan's level-set rounding. It picks exactly $k$ items when $\sum_i x_i = k$, as for [maximum coverage](/max-coverage/) with a budget of $k$ sets.
- **Assignment problems.** In an assignment of jobs to machines, each job keeps exactly one machine, and each machine gets a number of jobs close to its fractional load, while each pair keeps its probability. Gandhi et al. used this for scheduling on unrelated machines, for broadcast scheduling, and for coverage problems with partition constraints; compare the [generalized assignment problem](/generalized-assignment-problem/).

## Variations

- **Pipage rounding.** The same moves along cycles and paths, but with the direction chosen to keep a nonlinear objective from falling; see [pipage rounding](/pipage-rounding/).
- **Swap rounding.** Rounding a point of a matroid base polytope by merging bases, with the same kind of negative correlation; see [swap rounding](/swap-rounding/).
- **Deterministic forms.** Choosing the direction that does not raise a pessimistic estimator gives a deterministic rounding with the degree property; see [pessimistic estimators](/pessimistic-estimators/).
## Pitfalls

- **Graphs that are not bipartite.** An odd cycle cannot be split into alternate sets, and a vertex where two edges of the same set meet loses its degree. On a triangle with $\frac12$ on each edge, no rounding keeps all degrees at 1.
- **Negative correlation only at one vertex.** The theorem bounds products of edges at one vertex. Edges at different vertices can be positively correlated, so a Chernoff bound for a sum over edges from many vertices needs another argument.
- **Ends of a path that is not maximal.** The degree property at an end uses that the end has only one fractional edge. A path that stops at a vertex with two fractional edges changes that vertex's sum.
- **Floating point.** The values $\alpha$ and $\beta$ come from differences of values, and errors build up over $|E|$ steps. Round values within a tolerance of 0 or 1 to exact integers after each step.

## Exercises

1. Show that the choice of $\alpha$ and $\beta$ in lines L5 and L6 keeps all values in $[0, 1]$ and makes at least one edge of $P$ integral.
2. Run the rounding on the path $a_1 b_1 a_2 b_2$ with $x = (0.5, 0.5, 0.5)$, and list the outputs and their probabilities. Check that each vertex keeps its degree up to rounding.
3. Prove that negative correlation at each vertex gives the Chernoff upper tail bound for $\sum_{e \in S} X_e$, with $S$ the edges at that vertex.
4. Show that on the triangle with $\frac12$ on each edge, every 0-1 vector with the same marginals has a vertex of degree 0 or 2 with positive probability.

## References
