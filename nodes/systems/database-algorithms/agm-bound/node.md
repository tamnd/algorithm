---
tag: 79KBSS
kind: theorem
slug: agm-bound
name: AGM bound
aliases:
- Atserias-Grohe-Marx bound
- fractional edge cover bound for joins
area: systems/database-algorithms
level: advanced
summary: "A join's output size is at most the product of |R_e|^(x_e) for any fractional edge cover x of its hypergraph; the best cover gives a bound that some instances reach."
prereqs: [hypergraph, relational-join, shannon-entropy, linear-programming-problem]
see_also: [generic-join, leapfrog-triejoin, multiway-join, triangle-listing-by-degree, hypercube-shares-join, strong-duality, conditional-entropy, edge-cover]
sources:
  - paper: doi:10.1137/110859440
    title: Albert Atserias, Martin Grohe and Dániel Marx, Size bounds and query plans for relational joins, SIAM Journal on Computing 42(4), 1737 to 1767 (2013); first in FOCS 2008, 739 to 748
    locator: the main size bound (output at most the product of |R_e|^(x_e) over a fractional edge cover), its tightness, and the gap between join plans and join-project plans
  - paper: "Martin Grohe and Dániel Marx, Constraint solving via fractional edge covers, SODA 2006, 289 to 298; journal version in ACM Transactions on Algorithms 11(1), Article 4 (2014)"
    locator: the bound on the number of solutions by a fractional edge cover
  - paper: doi:10.1145/2590989.2590991
    title: Hung Q. Ngo, Christopher Ré and Atri Rudra, Skew strikes back, new developments in the theory of join algorithms, SIGMOD Record 42(4), 5 to 16 (2013)
    locator: the section on the AGM bound, with the proof by the query decomposition lemma, and the skewed triangle example
  - paper: doi:10.1145/3180143
    title: Hung Q. Ngo, Ely Porat, Christopher Ré and Atri Rudra, Worst-case optimal join algorithms, Journal of the ACM 65(3), Article 16 (2018); first in PODS 2012, 37 to 48
    locator: the introduction (the AGM bound and the Loomis-Whitney special case) and the algorithm that meets the bound
  - paper: "Fan R. K. Chung, Ronald L. Graham, Peter Frankl and James B. Shearer, Some intersection theorems for ordered sets and graphs, Journal of Combinatorial Theory, Series A 43(1), 23 to 37 (1986)"
    locator: Shearer's lemma (the entropy of a joint distribution and its projections on a cover)
---

The AGM bound says that the output of a natural join is at most $\prod_e |R_e|^{x_e}$, for every fractional edge cover $x$ of the [hypergraph](/hypergraph/) of the query. With $N$ tuples in each relation, the output is at most $N^{\rho^*}$, where $\rho^*$ is the fractional edge cover number, and some instances reach this size. Atserias, Grohe and Marx proved it in 2008. For the triangle query the bound is $N^{3/2}$, while a plan of pairwise joins can make $\Theta(N^2)$ intermediate tuples; [generic join](/generic-join/) and [leapfrog triejoin](/leapfrog-triejoin/) run within the bound.

## Statement

A *join query* $Q = \bowtie_{e \in E} R_e$ is a natural [join](/relational-join/) of relations. Its hypergraph is $H = (V, E)$: the vertices $V$ are the attributes, and each relation $R_e$ has the attribute set $e \subseteq V$. Each attribute is in at least one edge. The output $Q(D)$ is the set of tuples $t$ over $V$ with $t[e] \in R_e$ for each $e \in E$. Relations are sets; a relation may appear more than once under two edge names.

A *fractional edge cover* of $H$ is a vector $x \in \mathbb{R}^E$ with $x_e \ge 0$ for each $e$, and $\sum_{e \ni v} x_e \ge 1$ for each $v \in V$. The *fractional edge cover number* $\rho^*(H)$ is the minimum of $\sum_e x_e$ over all fractional edge covers. It is the value of a [linear program](/linear-programming-problem/).

**Theorem** (Atserias, Grohe and Marx 2008; the bound for sizes, from Grohe and Marx 2006). For each database $D$ and each fractional edge cover $x$ of $H$,

$$|Q(D)| \le \prod_{e \in E} |R_e|^{x_e}.$$

In particular, if $|R_e| \le N$ for each $e$, then $|Q(D)| \le N^{\rho^*(H)}$.

The best bound for given sizes $N_e = |R_e| \ge 1$ comes from the cover that minimizes $\sum_e x_e \log N_e$, also a linear program. It is $\text{AGM}(Q, D)$ in the literature. When some $R_e$ is empty, the output is empty.

**Tightness.** For each $N \ge 1$ there is a database with $|R_e| \le N$ for each $e$ and $|Q(D)| \ge 2^{-|V|} N^{\rho^*(H)}$. So $N^{\rho^*}$ is the worst-case output size up to a factor that depends only on the query. Atserias, Grohe and Marx also show tightness for each vector of sizes $(N_e)$, up to a constant factor that depends on the query.

## In plain words

A join builds rows that agree with one row of each input table. How many rows can come out, if you know only the sizes of the tables? You give each table a weight, so that each column is covered by tables whose weights add up to at least one. Then the output is at most the product of the table sizes, each raised to its weight.

For three tables that form a triangle (A with B, B with C, A with C), a weight of one half for each table covers every column. So with a thousand rows per table, at most about thirty thousand rows come out, not a million. A plan that joins two tables first can still make a million rows in the middle.

## Proof

Fix $D$ and a cover $x$. If $Q(D)$ is empty there is nothing to prove, so assume it is not. Let $T = (T_v)_{v \in V}$ be a random tuple, uniform over $Q(D)$. We use the [Shannon entropy](/shannon-entropy/) $H(\cdot)$ with base-2 logarithms and these standard facts:

1. A random variable with $s$ possible values has entropy at most $\log s$, with equality for the uniform distribution.
2. The chain rule: for an order $v_1, \ldots, v_n$ of $V$, $H(T) = \sum_{i=1}^n H(T_{v_i} \mid T_{v_1}, \ldots, T_{v_{i-1}})$.
3. Conditioning does not increase entropy: if $S \subseteq S'$, then $H(T_v \mid T_{S'}) \le H(T_v \mid T_S)$ (see [conditional entropy](/conditional-entropy/)).
4. Each $H(T_v \mid T_S)$ is at least 0.

**Step 1 (Shearer's lemma in fractional form).** For each fractional edge cover $x$,

$$H(T) \le \sum_{e \in E} x_e \, H(T_e),$$

where $T_e = (T_v)_{v \in e}$. Order $V$ as $v_1, \ldots, v_n$, and write $h_i = H(T_{v_i} \mid T_{v_1}, \ldots, T_{v_{i-1}})$. For an edge $e$, list its vertices in the same order and apply the chain rule to $T_e$: each term is $H(T_{v_i} \mid T_{v_j} : j < i, v_j \in e)$, and by fact 3 it is at least $h_i$, since it conditions on fewer variables. So $H(T_e) \ge \sum_{i : v_i \in e} h_i$. Multiply by $x_e \ge 0$ and add over $e$:

$$\sum_e x_e H(T_e) \ge \sum_{i=1}^n h_i \sum_{e \ni v_i} x_e \ge \sum_{i=1}^n h_i = H(T).$$

The second step uses $\sum_{e \ni v_i} x_e \ge 1$ and $h_i \ge 0$ (fact 4). The equality is fact 2.

**Step 2.** For each $e$, the value of $T_e$ is $t[e]$ for some $t \in Q(D)$, so it lies in $R_e$. By fact 1, $H(T_e) \le \log |R_e|$. Also $H(T) = \log |Q(D)|$, because $T$ is uniform. With step 1,

$$\log |Q(D)| \le \sum_e x_e \log |R_e|,$$

and taking powers of 2 gives the theorem. If all $|R_e| \le N$, choose $x$ with $\sum_e x_e = \rho^*$ to get $N^{\rho^*}$. $\blacksquare$

**A second proof.** Ngo, Ré and Rudra (2013) prove the bound without entropy, by induction on $|V|$ with Hölder's inequality. Their *query decomposition lemma* splits the sum over the values of one attribute. The same induction gives the running time bound of [generic join](/generic-join/).

**Proof of tightness for equal sizes.** By [strong duality](/strong-duality/), $\rho^*(H)$ equals the maximum of $\sum_v y_v$ over the *fractional vertex packings*: $y_v \ge 0$ and $\sum_{v \in e} y_v \le 1$ for each $e$. Take an optimal $y$, give attribute $v$ the domain $\{1, \ldots, \lfloor N^{y_v} \rfloor\}$, and let each $R_e$ be the product of the domains of its attributes. Then $|R_e| \le N^{\sum_{v \in e} y_v} \le N$. Every combination of domain values is in the output, so $|Q(D)| = \prod_v \lfloor N^{y_v} \rfloor \ge \prod_v N^{y_v}/2 = 2^{-|V|} N^{\rho^*}$, because $\lfloor a \rfloor \ge a/2$ for $a \ge 1$. When each $N^{y_v}$ is an integer, the output is exactly $N^{\rho^*}$.

## Consequences

**Examples.** These values come from an exact enumeration of the vertices of the cover polytope.

| query | edges | $\rho^*$ | bound with $N$ per relation | instance that reaches it |
|---|---|---|---|---|
| triangle | $AB, BC, AC$ | $3/2$ | $N^{3/2}$ | $N = 16$: domains of size 4, output 64 |
| 4-cycle | $AB, BC, CD, AD$ | $2$ | $N^2$ | $N = 16$: domains of size 4, output 256 |
| Loomis-Whitney, 4 attributes | the four 3-subsets of $ABCD$ | $4/3$ | $N^{4/3}$ | $N = 27$: domains of size 3, output 81 |
| path | $AB, BC$ | $2$ | $N^2$ | $B$ constant, output $N^2$ |
| star with 3 rays | $AB, AC, AD$ | $3$ | $N^3$ | $A$ constant, output $N^3$ |

The vertices of the cover polytope of the triangle are $(1/2, 1/2, 1/2)$, $(1, 1, 0)$, $(1, 0, 1)$ and $(0, 1, 1)$. With sizes $|R_{AB}| = 4$, $|R_{BC}| = 9$ and $|R_{AC}| = 16$, they give $\sqrt{4 \cdot 9 \cdot 16} = 24$, $36$, $64$ and $144$, so the bound is 24. With sizes $100, 100, 1$, the covers $(1/2, 1/2, 1/2)$, $(0, 1, 1)$ and $(1, 0, 1)$ all give 100.

- **Pairwise plans are not optimal.** In the triangle query, let each relation hold $(0, i)$ and $(i, 0)$ for $i = 1, \ldots, m$, so $N = 2m$. Each pairwise join, such as $R_{AB} \bowtie R_{BC}$, has $m^2 + m$ tuples, about $N^2/4$, while the output is at most $N^{3/2}$ (here it is empty). So each plan of binary joins does $\Omega(N^2)$ work on this instance. Atserias, Grohe and Marx show that join plans can lose a polynomial factor against the bound in general, while join-project plans do better.
- **Worst-case optimal joins.** An algorithm is *worst-case optimal* if it runs in time $O(\text{AGM}(Q, D))$, up to factors that depend on the query and up to log factors, plus the input size. The NPRR algorithm (Ngo, Porat, Ré and Rudra 2012), [generic join](/generic-join/) and [leapfrog triejoin](/leapfrog-triejoin/) are worst-case optimal. Their proofs extend the entropy argument above to the work at each attribute.
- **Triangles in a graph.** Store the $m$ edges of a graph in both directions in each of the three relations. The bound gives at most $(2m)^{3/2}$ ordered triangles, the classic $O(m^{3/2})$ bound that [triangle listing by degree](/triangle-listing-by-degree/) also meets. The [triangle detection hypothesis](/triangle-detection-hypothesis/) is a different statement: it is about the time to decide if one triangle exists, which can be far less than the number of triangles. The [distributed triangle enumeration](/distributed-triangle-enumeration/) page counts rounds of communication, not output size.
- **Parallel joins.** In the [HyperCube (shares) join](/hypercube-shares-join/), each reducer runs a local worst-case optimal join; the load of the shares itself is governed by another LP, the fractional edge packing.
- **Cardinality estimation.** The bound is an upper bound that a query optimizer can use without any statistics other than the sizes. Bounds that also use degrees and functional dependencies are sharper.

## Tightness

The bound $N^{\rho^*}$ is reached up to the factor $2^{-|V|}$ by the product instance above, and exactly when the domain sizes $N^{y_v}$ are integers. No other function of the sizes alone can be smaller: for each query and each vector of sizes, some instance reaches the best bound up to a constant factor that depends only on the query (Atserias, Grohe and Marx). The bound is not tight when the input has more structure than the sizes. In the path query $R_{AB} \bowtie R_{BC}$, if $B$ is a key of $R_{BC}$, each tuple of $R_{AB}$ extends in at most one way, so the output is at most $N$, not $N^2$. It is also only an upper bound on the output, not on the work of a given plan; that is the gap that worst-case optimal joins close.

## History

Grohe and Marx proved the size bound with fractional edge covers in 2006, in the setting of constraint satisfaction, and Atserias, Grohe and Marx (FOCS 2008, journal version 2013) proved that it is tight and studied query plans. The special case of the Loomis-Whitney query is a discrete form of the Loomis-Whitney inequality of geometry. The entropy proof uses Shearer's lemma from Chung, Graham, Frankl and Shearer (1986). Ngo, Porat, Ré and Rudra (2012) gave the first join algorithm whose running time matches the bound for every query, and Ngo, Ré and Rudra (2013) described the simpler generic join in their survey "Skew strikes back".

## References
