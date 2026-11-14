---
tag: 08T080
kind: algorithm
slug: greedy-equivalence-search
name: Greedy equivalence search
aliases:
- GES
area: statistics-and-inference/causal-inference-and-experimental-design
level: research
summary: Chickering's score-based causal discovery that adds and then deletes edges over Markov equivalence classes. With a consistent score it finds the true class in the limit.
model: real-ram
complexity:
  vars: {n: the number of variables}
  time: {worst: "O(n^4 2^n)", best: "Θ(n^2)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2002
  people: [David Maxwell Chickering, Christopher Meek]
  note: Chickering proved Meek's conjecture and gave operators that act on equivalence classes and are scored by local formulas, which made the two-phase greedy search of Meek practical and consistent.
prereqs: [bayesian-network-structure-learning, bayesian-information-criterion, d-separation, conditional-independence, directed-acyclic-graph, pc-algorithm]
see_also: [fci-algorithm, lingam, hill-climbing, tabu-search, chow-liu-algorithm, maximum-likelihood-estimation, covariance-matrix, bayesian-network]
sources:
  - paper: doi:10.1162/153244303321897717
    title: "David Maxwell Chickering, Optimal structure identification with greedy search, Journal of Machine Learning Research 3, 2002, pp. 507 to 554 (with an erratum on the Dor and Tarsi procedure)"
    locator: The whole paper (the Insert and Delete operators with their validity tests and score changes, the proof of Meek's conjecture, and the large-sample optimality of GES)
  - paper: "David Maxwell Chickering, A transformational characterization of equivalent Bayesian network structures, Proceedings of the 11th Conference on Uncertainty in Artificial Intelligence (UAI 1995), Morgan Kaufmann, pp. 87 to 98"
    locator: The whole paper (Markov equivalent DAGs are joined by a sequence of covered edge reversals)
  - paper: "Dorit Dor and Michael Tarsi, A simple algorithm to construct a consistent extension of a partially oriented graph, Technical Report R-185, Cognitive Systems Laboratory, UCLA, October 1992"
    locator: The whole report (the consistent extension procedure used after each operator)
  - paper: "Christopher Meek, Causal inference and causal explanation with background knowledge, Proceedings of the 11th Conference on Uncertainty in Artificial Intelligence (UAI 1995), Morgan Kaufmann, pp. 403 to 410"
    locator: The whole paper (the orientation rules that turn a DAG pattern into its CPDAG)
---

Greedy equivalence search (GES) learns the Markov equivalence class of a causal [directed acyclic graph](/directed-acyclic-graph/) by maximizing a score, such as the [Bayesian information criterion](/bayesian-information-criterion/). It does not search over DAGs but over equivalence classes, drawn as CPDAGs, because data cannot tell apart DAGs with the same [d-separations](/d-separation/). It starts from the empty graph. In the forward phase it adds one edge at a time, always the addition that raises the score most, until no addition helps. In the backward phase it removes one edge at a time in the same way. Chickering (2002) proved that with a consistent score and enough data this simple two-phase search finds the true class. It is the standard score-based method of [Bayesian network structure learning](/bayesian-network-structure-learning/), next to the test-based [PC algorithm](/pc-algorithm/).

## In plain words

Give every possible causal diagram a grade for how well it explains the data, with a penalty for each arrow. Diagrams that the data cannot tell apart get the same grade, so treat each group of them as one candidate. Start with no arrows. Add the single link that improves the grade most, and repeat until no single link helps. Then remove the single link whose removal improves the grade most, and repeat until no removal helps. With enough data, the first pass ends with every true link and maybe some extra ones, and the second pass takes the extra ones away.

## The problem

The input is a set $V$ of $n$ variables and a decomposable score: the score of a DAG $D$ is $\sum_{v} s(v, \mathrm{pa}_D(v))$, a sum of local scores of each variable and its parents. The score must also be score equivalent, so that Markov equivalent DAGs get the same score, and the score of a class is well defined. For Gaussian data with $N$ samples and sample covariance $\hat\Sigma$, the implementation uses

$$s(v, P) = -\frac N2 \log \hat\sigma^2_{v \mid P} - \frac{|P|}{2}\log N,$$

where $\hat\sigma^2_{v \mid P}$ is the residual variance of the [least-squares](/ordinary-least-squares/) regression of $v$ on $P$. This is $-\frac12$ times the BIC of that regression, up to terms that do not depend on $P$.

The goal is the class with the highest score. When the data come from a DAG $G$ whose d-separations are exactly the [conditional independences](/conditional-independence/) of the distribution, the hope is that this class is the class of $G$. The output is a CPDAG: arrows that all DAGs of the class share, and undirected edges elsewhere.

## The algorithm

For a current CPDAG and nodes $X$, $Y$, let $\mathrm{Pa}_Y$ be the parents of $Y$, $N_Y$ the nodes joined to $Y$ by an undirected edge, and $\mathrm{NA}_{Y, X}$ the nodes of $N_Y$ that are adjacent to $X$. A path is semi-directed from $Y$ to $X$ when each edge is undirected or points away from $Y$.

- **Insert$(X, Y, T)$**, for non-adjacent $X$, $Y$ and $T \subseteq N_Y$ with no node adjacent to $X$: add $X \to Y$ and orient $t \to Y$ for each $t \in T$.
- **Delete$(X, Y, H)$**, for $X \to Y$ or $X - Y$ and $H \subseteq \mathrm{NA}_{Y, X}$: remove the edge, and orient $Y \to h$ and $X \to h$ for each $h \in H$ whose edges are undirected.

```pseudo id=main
GES(V, s)
L1  C ← the empty graph on V
L2  repeat
L3      for each non-adjacent X, Y and each T ⊆ N_Y with no node adjacent to X do
L4          skip unless NA ∪ T is a clique and blocks every semi-directed path from Y to X
L5          Δ ← s(Y, NA ∪ T ∪ Pa_Y ∪ {X}) - s(Y, NA ∪ T ∪ Pa_Y)
L6      if the best Δ ≤ 0 then leave the loop
L7      apply the best Insert;  C ← CPDAG of a consistent extension
L8  repeat
L9      for each X → Y or X - Y and each H ⊆ NA do
L10         skip unless NA \ H is a clique
L11         Δ ← s(Y, (NA \ H) ∪ Pa_Y \ {X}) - s(Y, (NA \ H) ∪ Pa_Y ∪ {X})
L12     if the best Δ ≤ 0 then leave the loop
L13     apply the best Delete;  C ← CPDAG of a consistent extension
L14 return C
```

Here $\mathrm{NA}$ means $\mathrm{NA}_{Y, X}$. Lines L4 and L10 are the validity tests of Chickering (2002): exactly the operators that pass them turn the class into another class, and then the change of score is the local difference of line L5 or L11, so no full DAG is scored. After an operator the graph is only partly directed. Line L7 and line L13 complete it to a DAG with the same arrows and no new v-structure by the procedure of Dor and Tarsi (1992): repeatedly take a node with no outgoing arrow whose undirected neighbours are adjacent to all its other neighbours, direct its undirected edges into it, and remove it. Then they turn that DAG into its CPDAG with the rules of Meek (1995).

## Example

Take the DAG $A \to B$, $A \to C$, $B \to D$, $C \to D$, $D \to E$ with the linear model $B = 0.8A + e$, $C = 0.7A + e$, $D = 0.6B + 0.6C + e$, $E = 0.9D + e$ and independent unit-variance noises. The implementation computes its covariance exactly with fractions, for example $\operatorname{Var}(D) = 253/100$. Run GES on this covariance with $N = 1000$:

| step | operator | $\Delta$ | result |
|---|---|---|---|
| 1 | Insert$(D, E, \varnothing)$ | 554.00 | $D - E$ |
| 2 | Insert$(B, D, \varnothing)$ | 268.85 | adds $B - D$ |
| 3 | Insert$(D, C, \varnothing)$ | 253.07 | adds $C - D$ |
| 4 | Insert$(A, B, \varnothing)$ | 243.89 | adds $A - B$ |
| 5 | Insert$(C, A, \{B\})$ | 127.26 | adds $C \to A \leftarrow B$ |
| 6 | Insert$(B, C, \varnothing)$ | 0.50 | adds $B - C$ |
| 7 | Delete$(B, C, \{D\})$ | 3.45 | removes $B - C$, makes $B \to D \leftarrow C$ |

After step 5 the skeleton is the true one, but the collider is at $A$, not at $D$. That class says $B \perp C \mid D$, which is false, so step 6 adds the extra edge $B - C$, which removes the collider at $A$. Step 7, in the backward phase, removes it again with $H = \{D\}$ and puts the collider at $D$. The output is $A - B$, $A - C$, $B \to D \leftarrow C$, $D \to E$, the CPDAG of the true DAG, after 150 operator evaluations.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It is partial. It proves:

1. **Termination.** Each Insert adds exactly one edge to the skeleton and each Delete removes one, so there are at most $n(n - 1)$ steps.
2. **Score equivalence.** Reversing a covered edge $X \to Y$, one with $\mathrm{pa}(Y) = \mathrm{pa}(X) \cup \{X\}$, keeps the Gaussian BIC, because $\sigma^2_{X \mid P}\,\sigma^2_{Y \mid P \cup \{X\}} = \det\Sigma_{P \cup \{X, Y\}}/\det\Sigma_P$ is symmetric in $X$ and $Y$. Equivalent DAGs are joined by covered reversals (Chickering 1995, cited).
3. **Local consistency.** Adding $X$ to the parents $P$ of $Y$ changes the score by $-\frac N2\log(1 - \rho^2) - \frac12\log N$, where $\rho$ is the partial correlation of $X$ and $Y$ given $P$. For $N$ large enough this is positive exactly when $\rho \ne 0$.

Cited, not proved: the validity tests and local formulas of the operators, and the large-sample theorem of Chickering (2002). That theorem says that with a decomposable, score-equivalent, locally consistent score for a distribution faithful to $G$, the forward phase ends at a class whose independences all hold, and the backward phase ends at the class of $G$. Its proof rests on Meek's conjecture, which Chickering proved in the same paper. The tests check the result against exhaustive search over all DAGs on three and four nodes.

## Complexity

The cost is counted in evaluations of the score change of an operator. Each step looks at most at $n(n - 1)$ ordered pairs, each with at most $2^{n - 2}$ subsets $T$ or $H$, and there are at most $n(n - 1)$ steps. So the worst case is $O(n^4 2^n)$ evaluations. The best case is data with no dependence: the first forward step evaluates the $n(n - 1)$ operators with $T = \varnothing$, none helps, and the backward phase has nothing to do. Each evaluation needs two local scores; the Gaussian score solves a linear system of size $|P|$, and a cache keyed by $(v, P)$ avoids repeats. The graph takes $O(n^2)$ space. In practice the subsets stay small for sparse graphs, and the number of evaluations grows far more slowly than the bound.

## Properties

- **Consistent, not exact.** With a consistent score, GES returns the true class with probability tending to 1. For a fixed sample it is a greedy search and can stop at a class that is not the best; see Pitfalls.
- **Works on classes.** Each state is a whole equivalence class, so the search does not waste steps among equivalent DAGs, and the result does not depend on how the variables are numbered except through ties.
- **Deterministic.** Ties between operators are broken by the order of the variables.
- **Gives a score.** Unlike PC, GES returns the score of its answer, which can be compared with other classes.

## Variants and improvements

- **Turning phase.** Later work adds a third phase that reverses edges, which helps at finite sample sizes.
- **Speed-ups.** Fast GES implementations cache operator scores and recompute only those that touch the changed nodes, and they run on thousands of variables.
- **Search over DAGs.** Plain [hill climbing](/hill-climbing/) or [tabu search](/tabu-search/) over DAGs with edge additions, deletions and reversals is simpler, but has no large-sample guarantee.
- **Other scores.** Discrete data use the BIC of multinomial tables or the BDeu marginal likelihood, both decomposable and score equivalent.
- **Hidden variables and full orientation.** GES assumes that all common causes are measured; the [FCI algorithm](/fci-algorithm/) drops that assumption. With non-Gaussian noise, [LiNGAM](/lingam/) finds the whole DAG.

## When to use it

Use GES when a likelihood-based score fits the data well, the number of variables is moderate, and all common causes are measured. It often gives more stable answers than PC at small and medium sample sizes, because each decision weighs the whole fit of a family instead of one test. For very many variables or very dense graphs, the subsets $T$ and $H$ make it slow; then use PC, or restrict GES to a candidate set of edges.

## Pitfalls

- **Local optima at finite N.** In the example, use the same exact covariance but $N = 500$. Then step 6 no longer pays its penalty, and GES stops with $B \to A \leftarrow C$, $B - D - C$, $D - E$ and score $-17.51$. The true class scores $-15.54$: its product of residual variances is $1$, and the output's is $3086174/3061875 \approx 1.0079$. GES stops below the best class, so its guarantee is only a large-sample guarantee.
- **Measured rates with data.** On 50 data sets of each size from the example model, GES found the true class in 7 runs at $N = 200$, 17 at $N = 500$ and 40 at $N = 2000$. At $N = 500$, exhaustive search over all 29281 DAGs on five nodes showed that the BIC was highest for the true class in 44 of the 50 runs, but GES reached the highest scoring class in only 20. These rates are measured on the implementation, not proved.
- **Weak edges.** The penalty wins when a partial correlation is small for the sample size. With the exact covariance of 543 random linear models on four nodes and $N = 10^6$, GES returned the best class of all DAGs every time, but in 6 cases that class lacked one weak true edge.
- **Faithfulness.** If two paths cancel, for example $C \to A \to D$ and $C \to B \to D$ with weights whose products cancel, the guarantee fails and GES can end in a class with a lower score than the best one.
- **Causal reading.** The output is causal only if there are no hidden common causes and the score is right for the data. A Gaussian score on strongly non-Gaussian or non-linear data can prefer wrong classes.

## Implementations

## History

Meek conjectured that if every independence of a DAG $D'$ also holds in a DAG $D$, then $D'$ can be reached from $D$ by covered edge reversals and single edge additions, and he proposed a two-phase greedy search that would be optimal in the large-sample limit if the conjecture held. Chickering (1995) had shown that equivalent DAGs are joined by covered edge reversals. In 2002 Chickering proved Meek's conjecture and gave the Insert and Delete operators on CPDAGs with their validity tests and local score changes, which made the search, called GES, practical. Dor and Tarsi (1992) gave the extension procedure that GES uses after each step.

## References
