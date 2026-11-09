---
tag: DTW645
kind: algorithm
slug: multi-objective-simulated-annealing
name: Multi-objective simulated annealing
aliases:
- MOSA
- Pareto simulated annealing
- multiobjective simulated annealing
area: optimization/multi-objective
level: advanced
summary: Simulated annealing with a weighted rule that combines the changes of all objectives into one acceptance probability, and an archive of the non-dominated points evaluated.
solves: [multi-objective-optimization]
model: real-ram
complexity:
  vars: {K: the number of steps, M: the archive size, p: the number of objectives, n: the length of a solution vector, c: the cost of one evaluation of f}
  time: {worst: O(K (p M + n + c))}
  space: {extra: O(M (n + p))}
properties: {deterministic: false, iterative: true, population: false, elitist: true}
history:
  year: 1994
  people: [Paolo Serafini, Ekunda L. Ulungu, Jacques Teghem, Piotr Czyżak, Andrzej Jaszkiewicz]
  note: Serafini studied acceptance rules for several objectives in 1992 and 1994. Ulungu, Teghem and coauthors gave the MOSA method in 1999, and Czyżak and Jaszkiewicz gave Pareto simulated annealing in 1998.
prereqs: [simulated-annealing, metropolis-criterion, pareto-dominance, weighted-sum-method]
see_also: [simulated-annealing-convergence, cooling-schedule, paes, pareto-local-search, multi-objective-evolutionary-algorithm, scalarization, weighted-tchebycheff-method, approximate-pareto-set]
sources:
  - paper: "Paolo Serafini, Simulated annealing for multi objective optimization problems, in G. H. Tzeng, H. F. Wang, U. P. Wen and P. L. Yu (eds.), Multiple Criteria Decision Making, Proceedings of the Tenth International Conference, Springer, 1994, 283-292"
    locator: the acceptance rules for several objectives, among them the product rule and the weighted sum rule
  - paper: "E. L. Ulungu, J. Teghem, Ph. Fortemps and D. Tuyttens, MOSA method, a tool for solving multiobjective combinatorial optimization problems, Journal of Multi-Criteria Decision Analysis 8(4), 1999, 221-236"
    locator: the MOSA method with a set of weight vectors and an archive of potentially efficient solutions
  - paper: "Piotr Czyżak and Andrzej Jaszkiewicz, Pareto simulated annealing, a metaheuristic technique for multiple-objective combinatorial optimization, Journal of Multi-Criteria Decision Analysis 7(1), 1998, 34-47"
    locator: Pareto simulated annealing, a sample of interacting solutions with adapted weights
  - paper: doi:10.1109/TEVC.2007.900837
    title: Sanghamitra Bandyopadhyay, Sriparna Saha, Ujjwal Maulik and Kalyanmoy Deb, A simulated annealing-based multiobjective optimization algorithm, AMOSA, IEEE Transactions on Evolutionary Computation 12(3), 2008, 269-283
    locator: the amount of domination as the energy difference and the clustered archive
---

Multi-objective simulated annealing (MOSA) is [simulated annealing](/simulated-annealing/) for several objectives. It moves one current solution to a random neighbour with a probability that combines the changes of all objectives through a weight vector, and it keeps an archive of the non-dominated points that it evaluates. Serafini (1994) studied several such rules, and Ulungu, Teghem and coauthors (1999) built the MOSA method on them. With the weighted sum rule the current solution is a plain annealing chain on the weighted sum, so the annealing convergence theorem reaches only supported Pareto points for fixed weights; there is no general guarantee to reach the whole [Pareto front](/pareto-front/).

## In plain words

The search keeps one candidate and tries a small change at each step. Every candidate it tries is offered to a list of the best trade-offs found so far, and the list keeps only those that nothing else beats. Whether the search moves to the new candidate depends on a weighted total of how much each cost got worse. A change that makes nothing worse is always taken. A change that makes things worse is taken with a chance that is smaller when the loss is larger. A temperature controls this chance: it starts high, so the search wanders, and falls over time, so the search settles.

## The problem

**Convention.** All objectives are minimized, $p$ is the number of objectives, $N$ is the population size ($N = 1$ here), and $y = f(x)$ is the image of $x$.

The input is a search space $X$ with a neighbour proposal, the map $f : X \to \mathbb{R}^p$, a weight vector $w \ge 0$, a start temperature $T_0$, a cooling factor $\alpha \in (0, 1)$ and a number $K$ of steps. With $\Delta_m = f_m(y) - f_m(x)$, the two rules of the implementation are:

- **Sum rule.** $\pi_S = \min(1, \exp(-\sum_m w_m \Delta_m / T))$, the [Metropolis criterion](/metropolis-criterion/) for $h(x) = \sum_m w_m f_m(x)$.
- **Product rule.** $\pi_P = \prod_m \min(1, \exp(-w_m \Delta_m / T))$, which counts only the objectives that get worse.

The output is the archive: the non-dominated images of all points evaluated, an approximation of the front of the [multi-objective optimization](/multi-objective-optimization/) problem.

## The algorithm

```pseudo id=main
MOSA(f, w, T_0, α, K)
L1  x ← a random solution with its image; A ← {x}
L2  repeat K times
L3      y ← a random neighbour of x, with its image
L4      remove from A the members that f(y) dominates; add y if no member weakly dominates f(y)
L5      π ← the acceptance probability of the move from f(x) to f(y) at temperature T, with weights w
L6      if π = 1 or a uniform random number is below π then x ← y
L7      T ← α T
L8  return A
```

Line L4 offers every evaluated neighbour to the archive, accepted or not. Line L7 is the geometric [cooling schedule](/cooling-schedule/); a logarithmic schedule is needed for the convergence theorem. Ulungu et al. run the method for several weight vectors spread over the simplex and merge the archives.

## Example

Let $w = (\tfrac12, \tfrac12)$, $T = 1$ and $f(x) = (4, 4)$.

| $f(y)$ | $\Delta$ | $\sum_m w_m \Delta_m$ | $\pi_S$ | $\pi_P$ |
|---|---|---|---|---|
| (5, 2) | (1, −2) | −1/2 | 1 | $e^{-1/2} \approx 0.607$ |
| (5, 5) | (1, 1) | 1 | $e^{-1} \approx 0.368$ | $e^{-1/2} e^{-1/2} = e^{-1}$ |
| (6, 3) | (2, −1) | 1/2 | $e^{-1/2} \approx 0.607$ | $e^{-1} \approx 0.368$ |

The move to $(5, 2)$ is a trade-off. The sum rule always takes it, because the weighted total falls; the product rule counts only the loss of $1$ in the first objective. The dominated move to $(5, 5)$ gets the same value from both rules. At $T = \tfrac12$, the sum rule gives $e^{-1}$ for $(6, 3)$. In each case $\pi_P \le \pi_S$.

## Correctness

The proof covers the archive and the acceptance rules. The archive is exactly the set of non-dominated images of all points evaluated, by the induction of an elitist archive. With $w \ge 0$, a move that no objective makes worse is always accepted; with $w > 0$, a dominated move is accepted with probability below $1$. Both rules satisfy detailed balance with the Boltzmann weights $e^{-h(x)/T}$, because $a^+ - (-a)^+ = a$ for each term. With the sum rule, the current solution is a Metropolis chain on $h$, so under the hypotheses of the annealing convergence theorem it reaches a minimizer of $h$ with probability tending to $1$. Each minimizer of $h$ with $w > 0$ is Pareto-optimal, but unsupported Pareto-optimal points minimize $h$ for no $w$. The full proof is below.

## Complexity

- **One step.** The neighbour costs $O(n)$ and the evaluation $c$. The archive update of line L4 costs $O(p M)$, the rule $O(p)$.

The total is $O(K (p M + n + c))$ time and $O(M (n + p))$ space. The archive is not bounded; on a continuous problem it can grow at each step, and bounded archives such as those of [PAES](/paes/) or [approximate Pareto sets](/approximate-pareto-set/) cap $M$.

## Properties

- **Archive equals the front of the points seen.** It does not depend on the rule or the schedule.
- **The product rule is stricter.** $\pi_P \le \pi_S$ for every move.
- **Same equilibrium.** At a fixed temperature, with a symmetric proposal and a connected neighbour graph, both rules have the stationary distribution $e^{-h(x)/T}/Z$.
- **Convergence for fixed weights.** With the sum rule and a logarithmic schedule, the current solution converges in probability to the minimizers of $h$ (Hajek's theorem applied to $h$). These are supported Pareto-optimal points.
- **Scale.** The rule depends on the scale of each objective through $w_m \Delta_m$; normalize the objectives or choose $w$ for their ranges.

## Variants and improvements

- **Several weight vectors.** Ulungu et al. (1999) run one chain per weight vector from a spread set and merge the archives.
- **Pareto simulated annealing.** Czyżak and Jaszkiewicz (1998) run a sample of solutions and change each one's weights to push it away from its nearest neighbour in objective space.
- **Dominance-based energy.** AMOSA of Bandyopadhyay, Saha, Maulik and Deb (2008) measures a move by the amount of domination, the area between the two images, against the archive, and clusters the archive.
- **Tchebycheff rule.** Replace the weighted sum in the rule with the [weighted Tchebycheff](/weighted-tchebycheff-method/) function, which can reach unsupported points.

## When to use it

Use MOSA when a single-objective annealing code exists, the neighbourhood is natural, and a front approximation is wanted at low cost per step, for example on combinatorial problems. Run it with several weight vectors to cover the front. Results reported for MOSA, PSA and AMOSA are measured results on given instances, budgets and settings.

## Pitfalls

- **Supported points only.** For a fixed $w$ the sum rule drives the chain toward minimizers of the weighted sum; points in non-convex parts of the front are reached only by chance and kept only by the archive.
- **Geometric cooling.** The convergence theorem needs a logarithmic schedule; a geometric one is faster in practice and has no such guarantee.
- **Scale of $\Delta$.** One objective with large values dominates both rules; normalize.
- **Zero weights.** With $w_m = 0$, losses in objective $m$ are free, so the chain can drift to points that are dominated, though the archive does not keep them.
- **Archive growth.** On continuous problems the archive can grow with every step.

## Implementations

## History

Serafini (1992, 1994) proposed several acceptance rules for multi-objective annealing and studied their limit behaviour. Ulungu and Teghem developed the MOSA method in the 1990s, published in full in 1999 with Fortemps and Tuyttens. Czyżak and Jaszkiewicz gave Pareto simulated annealing in 1998, Suppapitnarm, Seffen, Parks and Clarkson gave an archive-based form in 2000, and Bandyopadhyay, Saha, Maulik and Deb gave AMOSA in 2008.

## References
