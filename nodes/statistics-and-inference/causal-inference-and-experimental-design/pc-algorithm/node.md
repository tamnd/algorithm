---
tag: MTZ8ME
kind: algorithm
slug: pc-algorithm
name: PC algorithm
aliases:
- Peter-Clark algorithm
- Spirtes-Glymour algorithm
area: statistics-and-inference/causal-inference-and-experimental-design
level: advanced
summary: Learns the Markov equivalence class of a causal DAG by deleting edges by conditional independence tests of growing size, then orienting colliders and further edges.
model: real-ram
complexity:
  vars: {n: the number of variables, q: the largest number of neighbours of a node in the true DAG}
  time: {worst: "O(n^2 2^n)", best: "Θ(n^2)"}
  space: {extra: "O(n^3)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1991
  people: [Peter Spirtes, Clark Glymour]
  note: Spirtes and Glymour gave the algorithm in Social Science Computer Review; it tests conditioning sets of growing size taken only from the current neighbours, so its cost is polynomial for sparse graphs.
prereqs: [bayesian-network-structure-learning, d-separation, conditional-independence, directed-acyclic-graph, structural-causal-model]
see_also: [fci-algorithm, greedy-equivalence-search, lingam, chi-squared-test-of-independence, markov-property, bayesian-network, chow-liu-algorithm, false-discovery-rate]
sources:
  - paper: doi:10.1177/089443939100900106
    title: "Peter Spirtes and Clark Glymour, An algorithm for fast recovery of sparse causal graphs, Social Science Computer Review 9(1), 1991, pp. 62 to 72"
    locator: The whole paper (the PC algorithm and its cost for sparse graphs)
  - book: isbn:9780262194402
    title: "Peter Spirtes, Clark Glymour and Richard Scheines, Causation, Prediction, and Search, 2nd edition, MIT Press, 2000"
    locator: Chapter 5 (discovery algorithms for causally sufficient structures, with the PC algorithm, its correctness and its complexity; general locator)
  - paper: "Christopher Meek, Causal inference and causal explanation with background knowledge, Proceedings of the 11th Conference on Uncertainty in Artificial Intelligence (UAI 1995), Morgan Kaufmann, pp. 403 to 410"
    locator: The whole paper (the orientation rules, their soundness, and their completeness for the output of the v-structure step)
  - paper: "Thomas Verma and Judea Pearl, Equivalence and synthesis of causal models, Proceedings of the 6th Conference on Uncertainty in Artificial Intelligence (UAI 1990), pp. 220 to 227; also in Uncertainty in Artificial Intelligence 6, North-Holland, 1991, pp. 255 to 270"
    locator: The whole paper (two DAGs are Markov equivalent exactly when they have the same skeleton and the same v-structures)
  - paper: "Markus Kalisch and Peter Bühlmann, Estimating high-dimensional directed acyclic graphs with the PC-algorithm, Journal of Machine Learning Research 8, 2007, pp. 613 to 636"
    locator: The whole paper (uniform consistency of PC with Gaussian partial correlation tests for sparse DAGs whose number of nodes grows with the sample size)
  - paper: "Diego Colombo and Marloes H. Maathuis, Order-independent constraint-based causal structure learning, Journal of Machine Learning Research 15(116), 2014, pp. 3921 to 3962"
    locator: The whole paper (the order dependence of PC on finite data, and the PC-stable variant)
---

The PC algorithm learns causal structure from conditional independence. It assumes the data come from an unknown [directed acyclic graph](/directed-acyclic-graph/) $G$ whose [d-separations](/d-separation/) are exactly the [conditional independences](/conditional-independence/) of the distribution. It starts from the complete undirected graph and removes the edge between two variables as soon as some set of their neighbours makes them independent, trying sets of size 0, then 1, then 2, and so on. Then it directs the colliders $a \to c \leftarrow b$ that the removal steps reveal, and directs more edges by three rules that avoid new colliders and cycles. Data alone cannot tell apart DAGs with the same independences, so the output is a partially directed graph that stands for the whole class. The algorithm is the standard constraint-based method of [Bayesian network structure learning](/bayesian-network-structure-learning/).

## In plain words

If two variables become unrelated once you hold some other variables fixed, then neither causes the other directly, so the link between them goes. The algorithm checks the links with small sets of other variables first, and it only looks among the variables still linked to one of the pair, which keeps the work small when there are few links. Then it reads directions from patterns: if two unlinked variables are both linked to a third, and that third variable was not part of what made them unrelated, both point into it. A few more rules then push those directions further. Links whose direction the data cannot decide stay without direction.

## The problem

The input is a finite set $V$ of $n$ variables and a test $\mathrm{CI}(a, b, S)$ that says whether $a \perp b \mid S$. The analysis assumes that the joint distribution is Markov and faithful to an unknown DAG $G$ on $V$: $a \perp b \mid S$ holds exactly when $S$ d-separates $a$ and $b$ in $G$. This rules out hidden common causes of the variables in $V$ (causal sufficiency) and exact cancellations of paths.

Two DAGs are Markov equivalent when they have the same d-separations. By Verma and Pearl (1990), this holds exactly when they have the same skeleton (the undirected graph of their edges) and the same v-structures, the triples $a \to c \leftarrow b$ with $a$ and $b$ not adjacent. Independence tests cannot separate equivalent DAGs, so the best possible output is the class of $G$. It is drawn as its CPDAG (completed partially directed acyclic graph): the common skeleton, with the edge $a \to b$ directed when every DAG of the class has it, and undirected otherwise. The output is the CPDAG of $G$.

## The algorithm

```pseudo id=main
PC(V, CI)
L1  G ← complete undirected graph on V;  k ← 0
L2  while some node a has |adj(a)| - 1 ≥ k do
L3      for each ordered adjacent pair (a, b) with |adj(a)| - 1 ≥ k do
L4          for each S ⊆ adj(a) \ {b} with |S| = k do
L5              if CI(a, b, S) then delete a - b; sepset(a, b) ← S; go to the next pair
L6      k ← k + 1
L7  for each pair a, b not adjacent, with a common neighbour c do
L8      if c ∉ sepset(a, b) then orient a → c ← b
L9  repeat for each undirected edge b - c
L10     R1: if a → b for some a not adjacent to c
L11     R2: or b → a → c for some a
L12     R3: or b - a1, b - a2, a1 → c ← a2 for some non-adjacent a1, a2
L13         then orient b → c
L14 until no rule applies;  return G
```

Lines L1 to L6 find the skeleton and remember a separating set for each removed pair. Lines L7 and L8 orient the v-structures. Lines L9 to L13 apply the rules of Meek (1995) until none applies. R1 avoids a new v-structure, R2 avoids a cycle, and R3 combines the two. A fourth rule of Meek is needed only when background knowledge directs extra edges, and the plain PC algorithm does not use it.

## Example

Let $G$ have the arrows $A \to B$, $A \to C$, $B \to D$, $C \to D$ and $D \to E$, and use the d-separation oracle of $G$ as the test.

- Level 0. Every pair is dependent without conditioning, so no edge goes.
- Level 1. $A \perp E \mid D$, $B \perp C \mid A$, $B \perp E \mid D$ and $C \perp E \mid D$ remove four edges.
- Level 2. $A \perp D \mid \{B, C\}$ removes $A - D$. Now the largest neighbourhood is $\{B, C, E\}$ of $D$, so level 3 does not run.

The skeleton is $A - B$, $A - C$, $B - D$, $C - D$, $D - E$. The pair $B, C$ has the common neighbour $D \notin \mathrm{sepset}(B, C) = \{A\}$, so $B \to D \leftarrow C$. The pair $A, D$ has the common neighbours $B$ and $C$, both in $\mathrm{sepset}(A, D)$, and the pairs $B, E$ and $C, E$ have $D$ in their separating sets, so no other collider appears. R1 with $B \to D - E$ and $B$, $E$ not adjacent gives $D \to E$. The output is

$$A - B, \quad A - C, \quad B \to D \leftarrow C, \quad D \to E.$$

The class has three DAGs: $A$ can be the source of both edges at $A$, or $B \to A \to C$, or $C \to A \to B$. The fourth choice, $B \to A \leftarrow C$, would add a v-structure. The implementation makes 64 calls to the oracle on this graph.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It assumes a perfect oracle under the causal Markov condition and faithfulness. In outline:

1. **Skeleton.** No edge of $G$ is removed, since adjacent nodes are d-connected given every set. For non-adjacent $a$ and $b$, one of them, say $b$, is not a descendant of the other, and then $\mathrm{pa}(a)$ d-separates them. As $\mathrm{pa}(a)$ stays inside the current $\mathrm{adj}(a) \setminus \{b\}$, the loop tests it by level $|\mathrm{pa}(a)|$ at the latest.
2. **V-structures.** The separating set of $a$ and $b$ blocks the path $a - c - b$. It contains $c$ if $c$ is a non-collider on that path and does not contain $c$ if $c$ is a collider. So line L8 finds exactly the v-structures of $G$.
3. **Soundness of R1 to R3.** If a DAG of the class had $c \to b$, R1 would give it a v-structure that the class does not have, R2 a cycle, and R3 both. So every arrow of the output is in every DAG of the class.

The converse, that each edge left undirected takes both directions inside the class, is the completeness theorem of Meek (1995). It is cited, not proved, and the tests check it exhaustively on three and four nodes.

## Complexity

The cost is counted in calls to the test. At level $k$ each ordered pair $(a, b)$ tests at most $\binom{n - 2}{k}$ sets. The proof of correctness shows that the loop stops after level $q$, the largest degree in $G$. So the number of tests is at most

$$n(n - 1)\sum_{k=0}^{q}\binom{n - 2}{k},$$

which is $O(n^{q + 2})$ for a fixed $q$ and is reached up to a constant on the complete DAG, with $n(n - 1)2^{n - 2}$ tests. The best case is the empty graph: level 0 removes all edges with $\binom n2$ tests. The separating sets take $O(n^3)$ space, and the orientation phase takes polynomial time in $n$. A test with data costs extra: the Gaussian test of the implementation inverts a $(k + 2) \times (k + 2)$ matrix per test after one pass over the data.

## Properties

- **Exact with an oracle.** With a perfect test, the output is the CPDAG of $G$ for any order of the nodes.
- **Order dependent with data.** With statistical tests, the skeleton depends on the order in which line L3 visits the pairs, because a removal changes the neighbourhoods used later. The PC-stable variant of Colombo and Maathuis (2014) removes this dependence.
- **Not a score.** PC returns one graph and no measure of fit or uncertainty. The tests at level $\alpha$ do not control the error rate of the whole graph.

## Variants and improvements

- **PC-stable.** Colombo and Maathuis (2014) fix the neighbourhoods at the start of each level, so the skeleton does not depend on the order of the variables. They also give conservative and majority rules that make the v-structure step order independent.
- **High dimensions.** Kalisch and Bühlmann (2007) proved that PC with Gaussian partial correlation tests at a suitable level is uniformly consistent for sparse DAGs whose number of nodes grows like a power of the sample size. This is cited, not proved here.
- **Hidden variables.** If some common causes are not measured, PC can give wrong arrows. The [FCI algorithm](/fci-algorithm/) extends PC to that case and returns a partial ancestral graph.
- **Score-based search.** [Greedy equivalence search](/greedy-equivalence-search/) searches the same space of classes with a score instead of tests.
- **Full orientation.** With non-Gaussian noise in a linear model, [LiNGAM](/lingam/) finds the whole DAG, not only its class.
- **Tests.** Discrete data use a [chi-squared test of independence](/chi-squared-test-of-independence/) or a G-test within each cell of $S$. Gaussian data use Fisher's $z$ for the partial correlation, as in the implementation. Kernel tests cover non-linear dependence.

## When to use it

Use PC when there are many variables, the true graph is sparse, all common causes are measured, and a reliable conditional independence test is available. Its cost grows with the degree of the graph, not with the number of DAGs, so it handles hundreds of variables when degrees are small. If hidden confounders are likely, use FCI. If a score such as the [BIC](/bayesian-information-criterion/) is natural for the model and the number of variables is moderate, GES often gives a more stable answer.

## Pitfalls

- **Near-violations of faithfulness.** Faithfulness fails when two paths cancel exactly, and finite samples also suffer when they nearly cancel. In the example graph with the linear Gaussian model $B = 0.8A + e$, $C = -0.7A + e$, $D = 0.6B + 0.6C + e$, $E = 0.9D + e$ and unit noises, $\operatorname{Cov}(A, D) = 0.06$. With 500 samples and level $\alpha = 0.01$, PC returned a wrong class in 49 of 50 runs, and with 2000 samples in 48 of 50. In a typical run it removes $A - D$ at level 0 with the empty set and then returns $A \to B \leftarrow D$, $A \to C \leftarrow D$. With $C = 0.7A + e$ it recovered the true class in 48 of 50 runs at both sizes. These rates are measured on the implementation, not proved.
- **Error propagation.** A wrong removal at a low level changes later neighbourhoods and separating sets, and a wrong separating set gives wrong arrows, which R1 to R3 then spread.
- **Conflicting colliders.** With data, two v-structures can direct the same edge both ways. The implementation keeps the first arrow; other programs mark the edge as bidirected. Either choice must be reported.
- **Multiple tests.** PC makes many tests at the same level $\alpha$. The level is a tuning parameter, not the error rate of the graph; see [false discovery rate](/false-discovery-rate/) for methods that control errors over many tests.
- **Causal reading.** The output is causal only under causal sufficiency, the Markov condition and faithfulness. Undirected edges carry no causal direction.

## Implementations

## History

Spirtes and Glymour published the PC algorithm in 1991 in *Social Science Computer Review*. The name comes from their first names, Peter and Clark. Earlier constraint-based methods, such as the SGS algorithm, tested every subset of the other variables for each pair, which is exponential even for sparse graphs. PC restricts the tests to subsets of current neighbours of growing size. Verma and Pearl (1990) had characterized Markov equivalence by skeletons and v-structures, and Meek (1995) proved that the orientation rules are sound and complete. Spirtes, Glymour and Scheines described the algorithm and its correctness in *Causation, Prediction, and Search* (1993, second edition 2000). Kalisch and Bühlmann (2007) proved high-dimensional consistency, and Colombo and Maathuis (2014) made the algorithm order independent.

## References
