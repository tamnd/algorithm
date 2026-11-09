---
tag: CPEC3T
kind: technique
slug: pseudocost-branching
name: Pseudocost branching
aliases:
- pseudo-cost branching
- pseudocosts
area: optimization/integer-programming
level: advanced
summary: Choose the branching variable from the average bound change per unit observed in earlier branchings.
prereqs: [land-doig-algorithm, branching-rule, lp-relaxation]
see_also: [strong-branching, reliability-branching, branching-rule, node-selection-rule, diving-heuristic, branch-and-cut, mixed-integer-programming, best-first-branch-and-bound]
sources:
  - paper: doi:10.1007/BF01584074
    title: M. Bénichou, J. M. Gauthier, P. Girodet, G. Hentges, G. Ribière and O. Vincent, Experiments in mixed-integer linear programming, Mathematical Programming 1, 1971
    locator: pp. 76 to 94 (pseudocosts as average objective change per unit, and their use for branching)
  - paper: "J. M. Gauthier and G. Ribière, Experiments in mixed-integer linear programming using pseudo-costs, Mathematical Programming 12, 1977, 26 to 47"
    locator: further experiments with pseudocosts for variable and node selection
  - paper: doi:10.1287/ijoc.11.2.173
    title: Jeff T. Linderoth and Martin W. P. Savelsbergh, A computational study of search strategies for mixed integer programming, INFORMS Journal on Computing 11(2), 1999
    locator: pp. 173 to 187 (pseudocost variable selection, the initialization of pseudocosts, and the score that combines both directions)
  - paper: doi:10.1016/j.orl.2004.04.002
    title: Tobias Achterberg, Thorsten Koch and Alexander Martin, Branching rules revisited, Operations Research Letters 33(1), 2005
    locator: pp. 42 to 54; Section 2.2 (the pseudocost formulas) and Table 1 of the ZIB-Report 04-13 version
---

Pseudocost branching is a [branching rule](/branching-rule/) for LP-based [branch and bound](/land-doig-algorithm/) that learns from the branchings already done. For each integer variable and each direction it keeps the average change of the LP bound per unit of rounding, called the pseudocost, and it branches on the variable whose estimated changes are largest. The estimate costs almost nothing per node, so the rule is fast, but it has no information at the start of the search. Bénichou and others introduced it in 1971.

## In plain words

When branch and bound splits a problem on a variable, it solves the two smaller problems and sees how much worse their bounds are. Pseudocost branching keeps a record of these changes for every variable, divided by how far the variable had to move.

Later, when the solver must choose a variable to split on, it does not test the candidates. It looks up their records, multiplies by how far each would have to move now, and picks the variable that is expected to worsen the bound the most on both sides. This guess is cheap. Its weakness is that the record is empty for a variable that has never been split on, and the first choices, at the top of the tree, matter most.

## When it applies

- LP-based branch and bound or [branch-and-cut](/branch-and-cut/) for a [mixed integer program](/mixed-integer-programming/), with variable branching on a fractional $\bar{x}_j$.
- The bound change caused by rounding a variable is roughly proportional to the distance it is rounded and roughly the same at different nodes. This holds in many models, though not in all of them.
- The tree is large enough that the records fill up, so that most decisions are based on several observations.

## The template

For a node with LP value $v$ and a fractional $\bar{x}_j$, let $f_j^- = \bar{x}_j - \lfloor \bar{x}_j \rfloor$ and $f_j^+ = \lceil \bar{x}_j \rceil - \bar{x}_j$. After a child with LP value $v^-$ or $v^+$ is solved, the *unit gain* is $(v - v^-)/f_j^-$ or $(v - v^+)/f_j^+$. For each $j$ the method keeps the sum $\sigma_j^-$ and the count $\eta_j^-$ of the down unit gains, and the same for up. The pseudocosts are the averages $\Psi_j^- = \sigma_j^- / \eta_j^-$ and $\Psi_j^+ = \sigma_j^+ / \eta_j^+$. The holes are INIT (the value used when a count is 0) and SCORE.

```pseudo id=main
PSEUDOCOST-BRANCH(N, x̄)
L1  for each j ∈ I with x̄_j fractional do
L2      Ψ⁻ ← σ⁻_j / η⁻_j if η⁻_j > 0, else INIT⁻(j)
L3      Ψ⁺ ← σ⁺_j / η⁺_j if η⁺_j > 0, else INIT⁺(j)
L4      s_j ← SCORE(f⁻_j · Ψ⁻, f⁺_j · Ψ⁺)
L5  return a j with the largest s_j

UPDATE(j, direction, v, v_child, f)                 ▷ after a child LP is solved and feasible
L6  σ_j^direction ← σ_j^direction + (v − v_child) / f
L7  η_j^direction ← η_j^direction + 1
```

A common INIT is the average of the pseudocosts of all variables that have one, or 1 if none has one. A common SCORE is $(1 - \mu) \min(q^-, q^+) + \mu \max(q^-, q^+)$ with $\mu = 1/6$, or the product $\max(q^-, \varepsilon) \cdot \max(q^+, \varepsilon)$.

**Why the search stays correct.** The rule only chooses which fractional variable to branch on. Branch and bound is correct for every such choice, so the pseudocosts affect the size of the tree and never the answer. The estimates $f_j^- \Psi_j^-$ are not bounds, so they must never be used to prune a node.

**What is not proved.** No theorem says that pseudocosts predict the gains, or that the rule gives small trees. The assumption that gains are proportional to the rounding distance is a model, and its value is measured.

**Example.** Take the instance of the [strong branching](/strong-branching/) page:
$$\max\ 10x_1 + 10x_2 + 7x_3 \quad \text{s.t.} \quad 6x_1 + 4x_2 + 6x_3 \le 15,\quad 3x_1 + 8x_2 + 2x_3 \le 18,\quad x \in \{0, 1, 2, 3\}^3.$$
At the root, $\bar{x} = (\tfrac43, \tfrac74, 0)$ and $v = \tfrac{185}{6}$. Suppose the four child LPs of $x_1$ and $x_2$ are solved once at the root, as in strong branching. They give the unit gains below.

| variable | $f^-$ | gain down | $\Psi^-$ | $f^+$ | gain up | $\Psi^+$ |
|---|---|---|---|---|---|---|
| $x_1$ | $\tfrac13$ | $\tfrac{11}{15}$ | $\tfrac{11}{5}$ | $\tfrac23$ | $\tfrac{10}{3}$ | 5 |
| $x_2$ | $\tfrac34$ | $\tfrac52$ | $\tfrac{10}{3}$ | $\tfrac14$ | $\tfrac{23}{6}$ | $\tfrac{46}{3}$ |

The solver branches on $x_2$. The up child is integral, at $(0, 2, 1)$ with value 27. The down child $x_2 \le 1$ has $\bar{x} = (\tfrac{11}{6}, 1, 0)$ and value $\tfrac{85}{3}$, and $x_1$ is fractional with $f^- = \tfrac56$ and $f^+ = \tfrac16$. The pseudocosts predict the gains $\tfrac56 \cdot \tfrac{11}{5} = \tfrac{11}{6}$ down and $\tfrac16 \cdot 5 = \tfrac56$ up, without any LP solve. The true gains are $\tfrac52$ and $\tfrac56$: the up estimate is exact and the down estimate is too low by $\tfrac23$.

## Classic examples

- **Early codes.** Bénichou and others (1971) used pseudocosts in their mixed integer code, and Gauthier and Ribière (1977) reported further experiments. Pseudocost branching then became a standard rule in commercial codes.
- **The study of Linderoth and Savelsbergh.** They compared many variable selection rules in one code, including several ways to set INIT, and found that the way uninitialized pseudocosts are handled has a large effect.
- **The study of Achterberg, Koch and Martin.** On their test set of hard instances from MIPLIB 2003 and from Mittelmann's benchmarks, with cuts only at the root, they report geometric means of about 88707 nodes and 283 seconds for pseudocost branching, against about 262369 nodes and 938 seconds for the most infeasible rule and about 7242 nodes and 504 seconds for full strong branching. So pseudocost branching was faster than full strong branching while it needed about twelve times as many nodes. They also report that the most infeasible rule was no better than a random choice. These numbers are measurements for one solver and one test set.

## Variations

- **Strong branching initialization.** Use [strong branching](/strong-branching/) on a variable whose pseudocost is not yet known and use the strong branching gains as its first observations.
- **Reliability branching.** Treat a pseudocost as unreliable until it has at least $\eta_{\text{rel}}$ observations in each direction, and use strong branching until then. See [reliability branching](/reliability-branching/).
- **Node estimates.** The sum over the fractional variables of $\min(f_j^- \Psi_j^-, f_j^+ \Psi_j^+)$ estimates how much the bound drops before a node reaches an integer solution. Solvers use it in the [node selection rule](/node-selection-rule/) and in [diving heuristics](/diving-heuristic/).
- **Pseudocosts from cuts and propagation.** Some solvers also record the number of bound changes or the number of conflicts caused by branching on a variable, and add these to the score.

## Pitfalls

- **No information at the start.** At the root, every pseudocost is INIT, so the first choices, which affect the largest subtrees, are close to arbitrary. This is the main reason for strong branching initialization.
- **Infeasible children.** If a child LP is infeasible, its gain is not a number. Skip the update, or record the infeasibility separately; do not add an infinite gain to $\sigma$.
- **Gains from pruned children.** If a child LP is stopped early because its bound fell below the incumbent value, the gain is only a lower bound on the true gain. Mixing such values into the averages biases them.
- **Scale.** Pseudocosts are in units of the objective per unit of the variable. Variables with large ranges or large objective coefficients dominate the score if the gains are not compared in the same units.
- **Changing models.** Cuts added during the search change the LP, so old observations describe a different relaxation than new ones.

## Exercises

1. Check the four unit gains in the example table from the child LP values $\tfrac{903}{30}$, $\tfrac{55}{2}$, $\tfrac{85}{3}$ and 27.
2. Show that the score $(1 - \mu)\min(q^-, q^+) + \mu \max(q^-, q^+)$ with $\mu < \tfrac12$ prefers a candidate with gains $(1, 1)$ to one with gains $(0, 3)$, and explain why this preference is reasonable.
3. Give a model in which the true gain of rounding a variable down is not proportional to $f^-$.
4. Modify the template so that it also keeps the number of infeasible children per variable and direction, and design a score that uses it.
5. After the example, update the pseudocosts of $x_1$ with the observed gains at the node $x_2 \le 1$.

## References
