---
tag: 5916QP
kind: technique
slug: iterative-rounding
name: Iterative rounding
aliases:
- Jain's iterative rounding
- iterative LP rounding
area: approximation/lp-rounding
level: advanced
summary: Solve the LP for a vertex, round up the variables that are large, update the residual problem and solve again; a counting argument on the vertex shows some variable is always large.
prereqs: [lp-relaxation, extreme-point, basic-feasible-solution, linear-programming-rounding]
see_also: [jain-iterative-rounding-network-design, iterative-relaxation, survivable-network-design, shmoys-tardos-gap, threshold-rounding, half-integrality, primal-dual-schema, integrality-gap]
sources:
  - paper: doi:10.1007/s004930170004
    title: Kamal Jain, A factor 2 approximation algorithm for the generalized Steiner network problem, Combinatorica 21(1), 2001
    locator: the main theorem (a vertex of the cut LP has an edge with value at least 1/2)
  - book: isbn:9781107007512
    title: Lap Chi Lau, R. Ravi and Mohit Singh, Iterative Methods in Combinatorial Optimization, Cambridge University Press, 2011
    locator: Chapter 2 (the rank lemma), Chapter 3 (bipartite matching) and Chapter 10 (network design)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Chapter 11 (further uses of deterministic rounding, Sections 11.1 to 11.3)
  - paper: doi:10.1016/j.orl.2010.02.006
    title: Viswanath Nagarajan, R. Ravi and Mohit Singh, Simpler analysis of LP extreme points for traveling salesman and survivable network design problems, Operations Research Letters 38(3), 2010
    locator: the fractional token argument
---

Iterative rounding is a way to round an LP relaxation a little at a time. Solve the LP for a vertex, fix every variable whose value is at least a threshold $1/\alpha$ to 1, change the problem to account for what is fixed, and solve the LP again. The method works when a structural lemma holds: every vertex of the LP has a variable of value at least $1/\alpha$. Then each round makes progress, and a simple telescoping argument bounds the cost by $\alpha$ times the first LP value. The method is due to Jain (2001), who used it with threshold $1/2$ for the [survivable network design problem](/survivable-network-design/). His key lemma says that a vertex of the cut LP always has an edge with $x_e \ge 1/2$, and its proof is by uncrossing and counting. The same pattern, with a rank lemma and a counting argument, proves many LP integrality results and approximation ratios.

## In plain words

Solve the easy, fractional version of the problem. Some parts of the answer are already large, such as an edge that is half bought or more. Commit to those parts fully. That costs at most a fixed factor more than the fractional answer paid for them.

Now the rest of the problem is smaller, because the committed parts already do some of the work. Solve the fractional version of what is left, commit to its large parts, and repeat.

Two facts make this work. The first is a promise that a corner answer of the fractional problem always has some large part, so you never get stuck. The second is that what is left can still use the old answer minus the committed parts, so its cost goes down by at least what the committed parts were worth.

## When it applies

Iterative rounding needs three things.

1. **A residual problem.** After some variables are fixed, what is left must be a problem of the same kind, with an LP of the same kind. In network design, buying an edge lowers each cut requirement by one when the edge crosses the cut, and the residual requirement keeps the property the proof needs.
2. **A structural lemma.** Every vertex of the residual LP has a variable with $x_e \ge 1/\alpha$, or some other step that makes progress, such as a variable with $x_e = 0$ that can be deleted. This is the hard part, and it is proved from the rank of the tight constraints.
3. **Monotone residual cost.** The current LP solution, restricted to the variables that are not fixed, must be feasible for the next residual LP.

The structural lemma is usually proved by the **rank lemma**: at a vertex $x$ of a polyhedron in $\mathbb{R}^m$, some $m$ linearly independent constraints are tight. If $0 < x_e < 1$ for all $e$, none of the bounds is tight, so $m$ independent problem constraints are tight. Then a counting argument shows that $m$ variables cannot all be small while $m$ independent constraints are tight. For cut constraints, the tight sets can first be **uncrossed** into a laminar family, which makes the counting possible.

## The template

```pseudo id=main
ITERATIVE-ROUNDING(problem P, threshold 1/α)
L1  F ← ∅
L2  while the residual problem P(F) has an unmet constraint do
L3      find a vertex x of the LP of P(F)
L4      delete each variable with x_e = 0
L5      H ← { e : x_e ≥ 1/α }
L6      F ← F ∪ H;  update P(F) so that the variables of H count as 1
L7  return F
```

**The ratio lemma.** Suppose that in each round, $H \ne \emptyset$, and that $x$ restricted to the variables outside $F \cup H$ is feasible for the LP of $P(F \cup H)$. Then $c(F) \le \alpha \cdot \text{LP}_1$, where $\text{LP}_1$ is the first LP value, and the loop ends after at most $m$ rounds.

*Proof.* Let $\text{LP}$ and $\text{LP}'$ be the values of a round and the next. The restricted point is feasible for the next LP, so $\text{LP}' \le \text{LP} - \sum_{e \in H} c_e x_e \le \text{LP} - c(H)/\alpha$, since $x_e \ge 1/\alpha$ on $H$ and $c \ge 0$. So $c(H) \le \alpha (\text{LP} - \text{LP}')$. Summing over the rounds telescopes to $c(F) \le \alpha(\text{LP}_1 - \text{LP}_{\text{last}}) \le \alpha \cdot \text{LP}_1$. Each round fixes at least one new variable, so there are at most $m$ rounds. $\square$

**Jain's lemma.** Let $f$ be an integer, weakly supermodular function on the subsets of $V$. Then every vertex $x$ of $\{ x \in [0, 1]^E : x(\delta(S)) \ge f(S) \text{ for all } S \}$ with $x \ne 0$ has an edge with $x_e \ge 1/2$.

*Proof outline.* The full proof, with all case checks, is in the proof file of [Jain's algorithm](/jain-iterative-rounding-network-design/). Delete the edges with $x_e = 0$, and assume that $0 < x_e < 1/2$ for all remaining edges $E'$, for a contradiction.

1. *Rank.* By the rank lemma, some $|E'|$ tight cut constraints are linearly independent.
2. *Uncrossing.* If two tight sets $A, B$ cross, weak supermodularity of $f$ and the submodularity of the cut function show that $A \cap B$ and $A \cup B$ are tight, or $A \setminus B$ and $B \setminus A$ are. In either case, the incidence vectors satisfy $\chi_{\delta(A)} + \chi_{\delta(B)} = \chi_{\delta(A \cap B)} + \chi_{\delta(A \cup B)}$, or the same with the differences. Choosing a tight set that crosses the fewest sets of a maximal laminar family shows that a laminar family $\mathcal{L}$ of $|E'|$ tight sets has independent vectors.
3. *Counting.* Each edge $uv$ hands out tokens: $x_e$ to the smallest set of $\mathcal{L}$ holding $u$, $x_e$ to the smallest holding $v$, and $1 - 2x_e > 0$ to the smallest holding both. A set $S$ receives $f(S) - \sum_{R \text{ child of } S} f(R)$ plus the number of edges whose smallest common set is $S$. This is an integer, and it is positive by independence, so it is at least 1. A maximal set of $\mathcal{L}$ has an edge leaving it whose token $1 - 2x_e$ goes to no set. So fewer than $|E'|$ tokens reach the $|E'|$ sets, a contradiction. $\square$

With the ratio lemma, Jain's lemma gives ratio 2 for every such $f$. The [odd cycle](/jain-iterative-rounding-network-design/) shows that the threshold $1/2$ cannot be raised.

## Classic examples

| problem | structural lemma at a vertex | result |
|---|---|---|
| survivable network design | some edge has $x_e \ge 1/2$ (Jain 2001) | ratio 2 |
| element connectivity network design | some edge has $x_e \ge 1/2$ (Fleischer, Jain and Williamson 2006) | ratio 2 |
| [generalized assignment](/shmoys-tardos-gap/) | some $x_{ij} \in \{0, 1\}$, or some machine has at most two fractional jobs whose total is at least 1, or has only one fractional job | cost at most LP, makespan at most $2T$ |
| [bipartite matching](/bipartite-matching/) | some $x_e \in \{0, 1\}$ | the LP is integral |
| [spanning trees](/spanning-tree-polytope/) | some edge has $x_e = 1$ at a leaf | the LP is integral |
| bounded degree spanning tree | some degree bound can be dropped ([iterative relaxation](/iterative-relaxation/)) | cost at most OPT, degree at most $B_v + 1$ |
| Steiner tree | random sampling of components of the directed component LP (Byrka, Grandoni, Rothvoss and Sanità 2010) | ratio $\ln 4 + \varepsilon < 1.39$ |

The GAP row is the proof in Williamson and Shmoys (Section 11.1). Its residual step drops the load constraint of a machine, so it is also an example of iterative relaxation. For bipartite matching and spanning trees, the threshold is 1, and the method proves that the LP has integral vertices; Lau, Ravi and Singh build their book on this view.

## Variations

- **Relaxation steps.** Besides fixing variables, a round may delete a constraint that the counting shows can be violated by only a small amount. This is [iterative relaxation](/iterative-relaxation/), used for degree bounds.
- **Different thresholds.** For element connectivity the threshold is again $1/2$. For other problems it is $1/\alpha$ for a constant $\alpha$, and the ratio is $\alpha$. A lemma with threshold $1/\alpha$ also shows that the [integrality gap](/integrality-gap/) of the LP is at most $\alpha$.
- **Iterative randomized rounding.** Byrka, Grandoni, Rothvoss and Sanità solve an LP, pick one component at random in proportion to its value, contract it, and repeat; the analysis bounds the expected cost.
- **The fractional token argument.** Jain's original counting gave each set integer tokens with a long case analysis. Nagarajan, Ravi and Singh showed that the fractional tokens above give a short proof.
- **Rounding a single variable.** Some versions fix only one variable per round, which gives the same bound and is easier to analyze when fixed variables change the structure.

## Pitfalls

- **Rounding an optimal point that is not a vertex.** The structural lemma speaks only of vertices. An optimal point in the middle of a face may have all values small. Use a vertex, for example from the simplex method.
- **Forgetting the residual update.** The next LP must reflect the fixed variables. Without it, the next LP is the same, and nothing changes.
- **A residual problem of a different kind.** The structural lemma must hold for every residual problem, not just the first. For SNDP, this holds because the residual requirement $f - d_F$ stays weakly supermodular.
- **Losing feasibility of the old point.** The ratio lemma needs the old solution, restricted, to be feasible for the residual LP. This often needs upper bounds such as $x_e \le 1$, so that fixing a variable to 1 does not remove more than $x_e$ from any constraint's slack.

## Exercises

1. Show that a vertex of $\{ x \ge 0 : x(\delta(v)) = 1 \text{ for all } v \}$ for a bipartite graph is integral, by the iterative argument. *Answer:* delete the edges with $x_e = 0$. If some $x_e = 1$, its ends have no other edge in the support; delete the edge and its ends and use induction. Otherwise each vertex of the support has degree at least 2, so $|E'| \ge |V'|$. The tight constraints are the $|V'|$ degree rows, and they are dependent, because the rows of the left side and the rows of the right side both sum to $\chi_{E'}$. So their rank is at most $|V'| - 1 < |E'|$, against the rank lemma.
2. Use the ratio lemma to show that a structural lemma with threshold $1/\alpha$ gives integrality gap at most $\alpha$. *Answer:* the algorithm finds an integral solution of cost at most $\alpha \cdot \text{LP}_1$, so the optimum is at most $\alpha$ times the LP value on every instance.
3. On a cycle of odd length with unit costs and requirement 1 for every pair, find the vertex of the cut LP and show that Jain's lemma is tight. *Answer:* each vertex $v$ must have $x(\delta(v)) \ge 1$, and the sum of these $n$ rows gives $2 \sum_e x_e \ge n$. Equality at all rows forces $x_e = 1/2$ on all edges, since the system $x_{e_{i-1}} + x_{e_i} = 1$ has a unique solution on an odd cycle. So the vertex has no edge with value above $1/2$.
4. Explain why the cut LP needs the bounds $x_e \le 1$ for the ratio lemma. *Answer:* without them, a single edge could carry $x_e = 2$ across a cut of requirement 2. Fixing it to 1 lowers the requirement by only 1, while the restricted point loses 2 from the cut, so it is not feasible for the residual LP.

## References
