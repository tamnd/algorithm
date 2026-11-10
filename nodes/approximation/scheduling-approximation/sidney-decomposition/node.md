---
tag: YXCAK6
kind: concept
slug: sidney-decomposition
name: Sidney decomposition
aliases:
- ratio decomposition
- Sidney's theorem
area: approximation/scheduling-approximation
level: research
summary: Splits jobs with precedence into initial sets of largest weight to time ratio. Some optimal schedule runs the pieces in order, and any such order is a 2-approximation for 1|prec|sum wjCj.
prereqs: [weighted-completion-time-scheduling, smith-rule, maximum-weight-closure]
see_also: [precedence-constrained-scheduling, parametric-max-flow-problem, exchange-argument, topological-sort, lawler-algorithm, approximation-ratio, max-flow-problem, minimizing-weighted-completion-time]
sources:
  - paper: "Jeffrey B. Sidney, Decomposition algorithms for single-machine sequencing with precedence relations and deferral costs, Operations Research 23(2), 1975"
    locator: pages 283 to 298 (initial sets of largest ratio, and an optimal schedule that runs them first)
  - paper: "Chandra Chekuri and Rajeev Motwani, Precedence constrained scheduling to minimize sum of weighted completion times on a single machine, Discrete Applied Mathematics 98(1-2), 1999"
    locator: pages 29 to 38 (the factor 2 for any order that respects the decomposition)
  - paper: "François Margot, Maurice Queyranne and Yaoguang Wang, Decompositions, network flows, and a precedence constrained single-machine scheduling problem, Operations Research 51(6), 2003"
    locator: pages 981 to 992 (the factor 2, and the decomposition by parametric minimum cuts)
  - paper: "José R. Correa and Andreas S. Schulz, Single-machine scheduling with precedence constraints, Mathematics of Operations Research 30(4), 2005"
    locator: pages 1005 to 1021 (the known 2-approximations respect a Sidney decomposition)
  - paper: "Eugene L. Lawler, Sequencing jobs to minimize total weighted completion time subject to precedence constraints, Annals of Discrete Mathematics 2, 1978"
    locator: pages 75 to 90 (series-parallel orders and strong NP-hardness)
---

The Sidney decomposition splits the jobs of the scheduling problem $1 \mid prec \mid \sum w_j C_j$ into pieces $S_1, S_2, \ldots, S_k$. The first piece is a set of jobs that is closed under predecessors and has the largest ratio of weight to processing time, $w(S)/p(S)$. The second piece is such a set among the remaining jobs, and so on. Sidney (1975) proved that some optimal schedule runs all of $S_1$ first, then all of $S_2$, and so on. Chekuri and Motwani (1999) and Margot, Queyranne and Wang (2003) proved more: every schedule that runs the pieces in this order, and each piece in any order the precedence constraints allow, costs at most twice the optimum. The pieces come from minimum cut computations, so this gives a simple 2-approximation for a strongly NP-hard problem. Without precedence constraints, the decomposition is [Smith's rule](/smith-rule/).

## In plain words

Some jobs must wait for others, each job has a length and a weight, and you want to finish heavy jobs early. A single job can be very heavy but stuck behind light jobs. So look at groups instead: a group that you can start right away, together with everything it needs. Pick the group that gives the most weight per unit of time and do it first. Then pick the best group among what is left. Inside a group, the order matters little: any allowed order is within a factor 2 of the best schedule.

## The idea

**Setting.** Jobs $N = \{1, \ldots, n\}$ have processing times $p_j > 0$ and weights $w_j \ge 0$. A precedence order on $N$ says which jobs must complete before others start. For a set $X$ write $p(X) = \sum_{j \in X} p_j$ and $w(X) = \sum_{j \in X} w_j$. A set $I$ is an **initial set** if it contains every predecessor of each of its jobs. The prefixes of a feasible schedule are initial sets. Unions and intersections of initial sets are initial sets. The **ratio** of a nonempty set is $\rho(X) = w(X)/p(X)$.

```pseudo id=main
SIDNEY-DECOMPOSITION(p, w, precedence order)
L1  R ← N
L2  while R is not empty do
L3      S ← a nonempty initial set of R, in the order induced on R, with the largest ratio w(S)/p(S)
L4      append S to the list of pieces
L5      R ← R − S
L6  return the pieces S1, S2, ..., Sk
```

The ratios of the pieces do not increase: $\rho(S_1) \ge \rho(S_2) \ge \cdots$. If $\rho(S_2) > \rho(S_1)$, then $S_1 \cup S_2$ would be an initial set of $N$ with ratio above $\rho(S_1)$, because the ratio of a disjoint union lies between the two ratios.

**Computing line L3.** For a number $\lambda$, an initial set with $w(I) - \lambda\,p(I) > 0$ exists if and only if the largest ratio is above $\lambda$. The largest value of $w(I) - \lambda\,p(I)$ over initial sets is a [maximum weight closure](/maximum-weight-closure/) problem with node weights $w_j - \lambda p_j$, which one minimum cut solves. The implementation of this page uses Dinkelbach's method: start with $S = R$ and $\lambda = \rho(S)$; find an initial set $I$ with the largest $w(I) - \lambda\,p(I)$; if this value is positive, set $S = I$ and $\lambda = \rho(I)$, which is larger, and repeat; else return $S$. The ratio grows in each round and takes finitely many values, so the method stops. Margot, Queyranne and Wang compute the whole decomposition with [parametric minimum cuts](/parametric-max-flow-problem/). Either way the decomposition takes polynomial time.

**Theorem (Sidney 1975).** Let $S$ be a nonempty initial set of $N$ with the largest ratio. Then some optimal schedule runs all jobs of $S$ before all other jobs.

*Proof.* Let $\rho^* = \rho(S)$ and $g(X) = w(X) - \rho^* p(X)$. Then $g(I) \le 0$ for every initial set $I$, including the empty set, and $g(S) = 0$. Two facts follow.

1. If $P$ is an initial set, then $g(S - P) \ge 0$. Indeed $S \cap P$ is an initial set, so $g(S - P) = g(S) - g(S \cap P) \ge 0$.
2. If $P$ is an initial set, then $g(P - S) \le 0$. Indeed $S \cup P$ is an initial set, so $g(P - S) = g(S \cup P) - g(S) \le 0$.

Take an optimal order $\sigma$. Let $\sigma'$ list the jobs of $S$ in their order in $\sigma$, followed by the other jobs in their order in $\sigma$. It is feasible: a predecessor of a job in $S$ is in $S$, and the relative order inside each part is unchanged. On one machine without idle time, $\sum_j w_j C_j = \sum_j w_j p_j + \sum_{i \text{ before } j} p_i w_j$. So only the pairs $(a, b)$ with $a \notin S$, $b \in S$ and $a$ before $b$ in $\sigma$ change, from $p_a w_b$ to $p_b w_a$. Substitute $w_j = g_j + \rho^* p_j$, where $g_j = g(\{j\})$:

$$\mathrm{cost}(\sigma') - \mathrm{cost}(\sigma) = \sum_{(a, b)} (p_b w_a - p_a w_b) = \sum_{(a, b)} (p_b g_a - p_a g_b) = \sum_{b \in S} p_b\, g(A_b) - \sum_{a \notin S} p_a\, g(B_a).$$

Here $A_b$ is the set of jobs not in $S$ that come before $b$ in $\sigma$, and $B_a$ is the set of jobs of $S$ that come after $a$. $A_b = P - S$ for the prefix $P$ of $\sigma$ before $b$, so $g(A_b) \le 0$ by fact 2. $B_a = S - P$ for the prefix $P$ of $\sigma$ up to $a$, so $g(B_a) \ge 0$ by fact 1. All $p$ are positive, so the difference is at most 0, and $\sigma'$ is optimal too. ∎

The cost of $\sigma'$ is the cost of its $S$ part, plus $p(S)\,w(N - S)$, plus the cost of its other part run from time 0. The middle term does not depend on the order. So the other part is optimal for the jobs $N - S$, and the theorem applies to them again. By induction, some optimal schedule runs $S_1, S_2, \ldots, S_k$ in this order, for any decomposition that the algorithm can return.

**Theorem (Chekuri and Motwani 1999; Margot, Queyranne and Wang 2003).** Any feasible order that runs $S_1, \ldots, S_k$ in this order costs at most $2\,\mathrm{OPT}$.

*Proof.* Let $\rho_i = \rho(S_i)$ and $Q_i = S_1 \cup \cdots \cup S_i$. Each job of $S_i$ completes by $p(Q_i)$, so the cost of the order is at most $\sum_i w(S_i)\, p(Q_i)$.

For the lower bound, take an optimal order that runs the pieces in order, from the first theorem. It costs $\sum_i \bigl( w(S_i)\, p(Q_{i-1}) + c_i \bigr)$, where $c_i$ is the cost of its $S_i$ part run from time 0. Let the $S_i$ part run the jobs $j_1, \ldots, j_s$, and let $F_t = \{j_t, \ldots, j_s\}$. Then $c_i = \sum_t p_{j_t}\, w(F_t)$. The set $\{j_1, \ldots, j_{t-1}\}$ is an initial set of the jobs $N - Q_{i-1}$, and $S_i$ has the largest ratio among those, so fact 1 gives $w(F_t) \ge \rho_i\, p(F_t)$. Hence

$$c_i \ge \rho_i \sum_t p_{j_t}\, p(F_t) = \rho_i\, \frac{p(S_i)^2 + \sum_{j \in S_i} p_j^2}{2} \ge \frac{w(S_i)\, p(S_i)}{2}.$$

So $\mathrm{OPT} \ge \sum_i w(S_i) \bigl( p(Q_{i-1}) + p(S_i)/2 \bigr) \ge \frac12 \sum_i w(S_i)\, p(Q_i)$, which is at least half the cost of the order. ∎

The proof does not need the pieces to be minimal, and it does not look at the order inside a piece. So the algorithm "decompose, then use a [topological sort](/topological-sort/) inside each piece" is a 2-approximation in polynomial time.

## Examples

**Five jobs.** Take the jobs below, numbered from 0, with the constraints "0 before 1" and "3 before 4".

| job | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| $p_j$ | 3 | 1 | 2 | 1 | 2 |
| $w_j$ | 1 | 6 | 4 | 1 | 3 |

Job 1 has the best single ratio, 6, but it needs job 0. Some initial sets and their ratios:

| set | $\{0, 1\}$ | $\{2\}$ | $\{3, 4\}$ | $\{0, 1, 2\}$ | $\{2, 3\}$ | $\{0, 1, 2, 3\}$ | all |
|---|---|---|---|---|---|---|---|
| ratio | $7/4$ | $2$ | $4/3$ | $11/6$ | $5/3$ | $12/7$ | $5/3$ |

The largest ratio is 2, for $\{2\}$, so $S_1 = \{2\}$. Among jobs $0, 1, 3, 4$, the best is $\{0, 1\}$ with $7/4$, so $S_2 = \{0, 1\}$, and then $S_3 = \{3, 4\}$ with $4/3$. The order $2, 0, 1, 3, 4$ has completion times $2, 5, 6, 7, 9$ and cost $4 \cdot 2 + 1 \cdot 5 + 6 \cdot 6 + 1 \cdot 7 + 3 \cdot 9 = 83$. A search over all feasible orders confirms that 83 is optimal. Smith's rule without the constraints would run job 1 first, which is not allowed.

**The order inside a piece matters.** Take $p = (3, 1, 2, 4)$, $w = (0, 3, 0, 3)$, with "0 before 1", "0 before 3" and "1 before 2". Both $\{0, 1\}$ and $\{0, 1, 3\}$ have the largest ratio $3/4$. If line L3 returns $\{0, 1, 3\}$, the allowed orders inside it give the schedules $0, 1, 3, 2$ with cost 36, which is optimal, and $0, 3, 1, 2$ with cost 45. The ratio $45/36 = 1.25$ is within the bound 2. The smaller piece $\{0, 1\}$, followed by $\{3\}$ and $\{2\}$, leaves only the optimal order.

**No constraints.** Every set is an initial set, and the largest ratio is that of the single jobs with the largest $w_j / p_j$. A set of jobs with the same ratio can be one piece, in any order, and all orders of such a piece have the same cost. So the decomposition sorts by $w_j / p_j$, which is Smith's rule.

The tests of this page check, on seeded random instances with at most 7 jobs, that each piece is an initial set of largest ratio, found by a search over all subsets; that the best order that respects the pieces is optimal; that every such order is within a factor 2; and that without constraints the result equals the optimum.

## Where it is used

- **2-approximations for $1 \mid prec \mid \sum w_j C_j$.** The methods of Chekuri and Motwani and of Margot, Queyranne and Wang are the algorithm above. Correa and Schulz (2005) show that the other known 2-approximations, which come from linear programs, also produce schedules that respect a Sidney decomposition. See [weighted completion time scheduling](/weighted-completion-time-scheduling/).
- **Exact algorithms for special orders.** For series-parallel precedence orders, Lawler (1978) solves the problem in $O(n \log n)$ time by merging sequences of decreasing ratio, which is the same ratio rule applied to parts of the order.
- **The link to vertex cover.** Correa and Schulz, and Ambühl and Mastrolilli (2009), show that $1 \mid prec \mid \sum w_j C_j$ is a special case of vertex cover in a graph built from the precedence order, and the Sidney decomposition is a tool in these proofs.
- **Branch and bound.** The decomposition splits a large instance into independent smaller ones, since an optimal schedule exists that respects it.
- **Sequencing with deferral costs.** Sidney's paper states the problem as the order of tasks that each have a cost per unit of delay, which is the weight $w_j$.

## References
