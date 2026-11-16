---
tag: W42VES
kind: algorithm
slug: qpbo
name: QPBO
aliases:
- quadratic pseudo-boolean optimization
- roof duality
area: computer-vision/stereo-and-dense-reconstruction
level: advanced
summary: Minimize a non-submodular binary pairwise energy by a min cut on a doubled graph, labeling part of the variables with values that some optimum shares, and giving a lower bound.
solves: [map-inference]
model: real-ram
complexity:
  vars: {n: the number of variables, m: the number of pair terms, F: the time of one max flow on 2n + 2 nodes and 2n + 2m edges}
  time: {worst: O(F + n + m), average: O(F + n + m), best: O(F + n + m)}
  space: {extra: O(n + m)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1984
  people: [Peter L. Hammer, Pierre Hansen, Bruno Simeone]
  note: Hammer, Hansen and Simeone introduced roof duality for quadratic 0-1 optimization and proved persistency. Kolmogorov and Rother (2007) presented the graph cut form used in vision under the name QPBO.
prereqs: [graph-representable-energies, max-flow-min-cut-theorem]
see_also: [alpha-expansion, alpha-beta-swap, boykov-kolmogorov-max-flow, submodular-function, lp-relaxation, map-inference, markov-random-field, ising-model]
sources:
  - paper: doi:10.1007/BF02612354
    title: Peter L. Hammer, Pierre Hansen and Bruno Simeone, Roof duality, complementation and persistency in quadratic 0-1 optimization, Mathematical Programming 28(2), 1984, 121-155
    locator: the roof dual bound, its equality with the bound of the linear programming relaxation, and the persistency theorem
  - paper: doi:10.1016/S0166-218X(01)00341-9
    title: Endre Boros and Peter L. Hammer, Pseudo-Boolean optimization, Discrete Applied Mathematics 123(1-3), 2002, 155-225
    locator: the parts on roof duality, the implication network and the computation of the roof dual by network flows
  - paper: doi:10.1109/TPAMI.2007.1031
    title: Vladimir Kolmogorov and Carsten Rother, Minimizing nonsubmodular functions with graph cuts, a review, IEEE Transactions on Pattern Analysis and Machine Intelligence 29(7), 2007, 1274-1279
    locator: the construction of the doubled graph, the reading of the partial labeling, and the properties of the method
  - book: isbn:9780262015776
    title: Andrew Blake, Pushmeet Kohli and Carsten Rother (editors), Markov Random Fields for Vision and Image Processing, MIT Press, 2011
    locator: Part I, Algorithms for inference of MAP estimates for MRFs (the chapter on optimizing non-submodular binary MRFs)
---

QPBO (quadratic pseudo-Boolean optimization) is a method for energies of binary variables with unary and pairwise terms when some pairwise terms are not submodular, so that a single [minimum cut](/min-cut-problem/) cannot minimize them (the [Kolmogorov-Zabih theorem](/graph-representable-energies/)). It doubles the variables: next to each $x_p$ it adds $\bar x_p$, meant to be $1 - x_p$, and writes a new energy of the $2n$ variables that is submodular and equals the old energy when $\bar x = 1 - x$. One minimum cut minimizes the new energy. Where the solution has $\bar x_p = 1 - x_p$, the variable $p$ gets a label; elsewhere it is left unlabeled. The labeled values are persistent: some minimizer of the original energy has exactly those values. The minimum of the new energy is also a lower bound on the original minimum. The method is the roof duality of Hammer, Hansen and Simeone (1984); its bound equals that of the [linear programming relaxation](/lp-relaxation/). In vision it solves the nonregular moves of fusion and stereo methods, and in general it fixes part of the variables of a hard problem for free.

## In plain words

You have many yes or no questions, and a cost for each answer and for each pair of answers. If every pair prefers to agree, a cut in a graph gives the best answers at once. When some pairs prefer to disagree, that trick fails. QPBO keeps two copies of each question, one for the answer and one for its opposite, and writes the costs so that every pair in the new problem prefers to agree. The cut then solves the new problem. Where the two copies give consistent answers, you can trust them: some best solution uses those answers. Where they do not, the method says "I do not know", and you must decide those questions another way.

## The problem

**Input.** An energy of $n$ binary variables

$$E(x) = \sum_p \theta_p(x_p) + \sum_{(p,q)} \theta_{pq}(x_p, x_q),$$

with real values and $m$ pair terms. A pair term is submodular if $\theta_{pq}(0,0) + \theta_{pq}(1,1) \le \theta_{pq}(0,1) + \theta_{pq}(1,0)$; the others are not.

**Output.** A partial labeling: a set of variables with values in $\{0, 1\}$ such that some global minimizer of $E$ has these values, and a lower bound on $\min E$.

Minimizing $E$ is NP-hard in general (it contains maximum cut), so a method that labels all variables in polynomial time on every input is not expected.

## The algorithm

```pseudo id=main
QPBO(θ)
L1  for each variable p, make two nodes: p for x_p, and p̄ for x̄_p (meant to be 1 - x_p)
L2  for each p add ½ θ_p(x_p) + ½ θ_p(1 - x̄_p)
L3  for each pair term θ_pq do
L4      if θ_pq is submodular then add ½ θ_pq(x_p, x_q) + ½ θ_pq(1 - x̄_p, 1 - x̄_q)
L5      else add ½ θ_pq(x_p, 1 - x̄_q) + ½ θ_pq(1 - x̄_p, x_q)
L6  (x, x̄) ← a minimizer of the new energy Ẽ by one minimum cut on 2n + 2 nodes
L7  for each p: if x̄_p = 1 - x_p then label p with x_p, else leave p unlabeled
L8  return the partial labeling and the lower bound Ẽ(x, x̄)
```

Line L4 keeps a submodular term on the original variables and copies it, complemented, on the doubled ones. Line L5 links a non-submodular term between $x_p$ and $\bar x_q$ and between $\bar x_p$ and $x_q$: replacing one argument by the complement of its twin turns "prefer to disagree" into "prefer to agree". Every term of $\tilde E$ is then regular, and the graph of the theorem page represents it. The code multiplies everything by 2 to keep integer costs in integers.

## Example

Take three variables with the frustrated triangle, each pair paying 1 when the two values agree, and a fourth variable tied to $x_0$:

- $\theta_{01} = \theta_{12} = \theta_{02} = [x_p = x_q]$, which are not submodular ($1 + 1 > 0 + 0$);
- $\theta_{03} = [x_0 \ne x_3]$, which is submodular;
- $\theta_3(0) = 0$, $\theta_3(1) = 3$, and no other unary costs.

Every labeling of the triangle has at least one agreeing pair, so $\min E = 1$, reached by $(0,0,1,0)$, $(0,1,0,0)$ and $(0,1,1,0)$. QPBO finds the minimizer $x = (0,0,0,0)$, $\bar x = (0,0,0,1)$ of $2\tilde E$, with $2\tilde E = 1$.

| variable | $x_p$ | $\bar x_p$ | result |
|---|---|---|---|
| 0, 1, 2 | 0 | 0 | unlabeled |
| 3 | 0 | 1 | labeled 0 |

The lower bound is $\tilde E = 0.5 \le 1$, and $x_3 = 0$ holds in every minimizer, as persistency promises. The triangle stays unlabeled, because on an odd cycle of disagreeing pairs the doubled energy can reach a smaller value with $x = \bar x$ than any real labeling. In a second example with a chain $x_0, x_1, x_2$, a strong unary cost $\theta_0 = (0, 4)$, a non-submodular term on $(x_0, x_1)$ that pays 2 when they agree, and a submodular term on $(x_1, x_2)$ that pays 3 when they differ, QPBO labels all three variables, $(0, 1, 1)$, which is the minimizer with $E = 0$.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). First, each term of $\tilde E$ is regular: a submodular term keeps its sign under complementing both arguments, and a non-submodular term becomes regular when exactly one argument is complemented. Second, $\tilde E(x, 1 - x) = E(x)$, so $\min \tilde E \le \min E$. Third, persistency. The map $\sigma(x, \bar x) = (1 - \bar x, 1 - x)$ leaves $\tilde E$ unchanged, and $\tilde E$ is submodular on $\{0,1\}^{2n}$. From the minimizer $a$ found by the cut, $a \vee \sigma(a)$ is also a minimizer that agrees with $a$ on the labeled variables and is $(1,1)$ on the others. For any minimizer $z$ of $E$, two steps of submodularity with $b = (z, 1 - z)$ give a point $(z', 1 - z')$ of no larger energy, where $z'$ takes the QPBO values on the labeled variables and the values of $z$ elsewhere. So $z'$ is also a minimizer.

## Complexity

The model is the real RAM; the tests use integer costs.

- **Time.** Building $\tilde E$ and its graph takes $O(n + m)$ time. The graph has $2n + 2$ nodes and at most $2n + 2m$ edges, so the time is that of one max-flow computation $F$ on a graph twice as large as for a submodular energy. The code uses [Edmonds-Karp](/edmonds-karp/); vision codes use the [Boykov-Kolmogorov algorithm](/boykov-kolmogorov-max-flow/).
- **Space.** $O(n + m)$.

## Properties

- **Persistency.** Labeled values agree with some global minimizer. Fixing them and solving the rest by any method loses nothing.
- **Lower bound.** $\min \tilde E \le \min E$, and the gap tells how far a heuristic solution can be from the optimum.
- **Exact for submodular energies.** If all terms are submodular and the minimizer is unique, all variables are labeled. If there are several minimizers, a cut may leave some variables unlabeled.
- **LP equivalence.** The roof dual bound equals the optimum of the standard linear programming relaxation of the quadratic 0-1 problem (Hammer, Hansen and Simeone 1984). So QPBO solves that relaxation by one cut.
- **Partial in general.** On frustrated cycles, as in the example, many variables can stay unlabeled. How many depends on the strength of the non-submodular terms against the unary terms.
- **Invariance.** Flipping the meaning of a variable ($x_p \to 1 - x_p$) changes which terms are submodular, but not the labeled set. So any energy that becomes submodular after flipping some variables (a "bipartite" frustration pattern) is solved as well as a submodular one.

## Variants and improvements

- **QPBO-P and QPBO-I.** Rother, Kolmogorov, Lempitsky and Szummer (2007) proposed probing, which tries each value of an unlabeled variable and draws conclusions from both runs, and improvement, which takes any complete labeling and returns one of no larger energy by fixing the unlabeled variables to it.
- **Fusion moves.** In multi-label problems, a move that combines the current labeling with a proposal is a binary energy that is often not submodular; QPBO solves it, and unlabeled sites keep their current label, which never raises the energy.
- **Higher order.** Energies with terms of three or more variables are first reduced to pairwise form with extra variables, then given to QPBO.
- **Implication network.** Boros and Hammer compute the same bound by a max flow on an implication network of $2n$ literals, the same idea in the language of [2-SAT](/2-sat/) and [implication graphs](/implication-graph/).

## When to use it

Use QPBO for binary pairwise energies with some non-submodular terms: image deconvolution, texture synthesis, learned pairwise terms, and the fusion moves of stereo and optical flow. It is fast, it never gives a wrong label, and its bound measures the quality of the rest. When most variables stay unlabeled, add probing, or use [loopy belief propagation](/loopy-belief-propagation/) or [simulated annealing](/simulated-annealing/) on the remaining part. For energies that are already submodular, a plain cut is simpler and half the size.

## Pitfalls

- **Unlabeled is not wrong.** An unlabeled variable has no information from QPBO. Assigning it 0 by default is a heuristic; use QPBO-I to make sure that the energy does not rise.
- **Persistency is weak.** The labeled values agree with some minimizer, not with every minimizer. Two runs with different cuts can label different sets, each correct.
- **Halves.** The definition has factors $\tfrac12$. Doubling all costs avoids fractions; the lower bound is then half the cut value.
- **The frustrated case.** Strong non-submodular terms on odd cycles, as in max-cut instances, leave almost everything unlabeled. QPBO does not make an NP-hard problem easy.

## Implementations

## History

Hammer, Hansen and Simeone (1984) defined the roof dual of a quadratic 0-1 function, showed that it equals the bound of the linear programming relaxation, and proved persistency. Boros and Hammer, with coauthors, developed the network flow computation of the bound and summarized the theory in their 2002 survey. Kolmogorov and Rother (2007) brought the method to vision under the name QPBO, with the doubled graph and an efficient code built on the Boykov-Kolmogorov max-flow algorithm, and Rother et al. (2007) added probing and improvement. QPBO then became the standard solver of fusion moves and of other nonregular binary moves.

## References
