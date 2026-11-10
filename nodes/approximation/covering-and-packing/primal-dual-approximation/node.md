---
tag: TKR0BD
kind: technique
slug: primal-dual-approximation
name: Primal-dual method for approximation
aliases:
- primal-dual method
- primal-dual approximation algorithm
area: approximation/covering-and-packing
level: advanced
summary: Raise a feasible dual until its constraints go tight, add the tight primal variables, and bound the cost by relaxed complementary slackness; ratio f for set cover and 2 for Steiner forest.
prereqs: [lp-duality, complementary-slackness]
see_also: [primal-dual-schema, set-cover-primal-dual, primal-dual-weighted-vertex-cover, goemans-williamson-steiner-forest, jain-vazirani-facility-location, local-ratio-technique, dual-fitting, complementary-slackness]
sources:
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Chapter 7 (the primal-dual method, with set cover, feedback vertex set, shortest s-t path, Steiner forest and facility location)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 15 (set cover by the primal-dual schema) and Chapter 22 (Steiner forest)
  - book: isbn:9780534949686
    title: Dorit S. Hochbaum (editor), Approximation Algorithms for NP-Hard Problems
    locator: Chapter 4, by Michel X. Goemans and David P. Williamson (the primal-dual method for approximation algorithms and network design)
  - paper: doi:10.1016/0196-6774(81)90020-1
    title: Reuven Bar-Yehuda and Shimon Even, A linear-time approximation algorithm for the weighted vertex cover problem, Journal of Algorithms 2(2), 1981
    locator: pages 198 to 203
  - paper: doi:10.1137/S0097539793242618
    title: Michel X. Goemans and David P. Williamson, A general approximation technique for constrained forest problems, SIAM Journal on Computing 24(2), 1995
    locator: pages 296 to 317
  - title: Ajit Agrawal, Philip Klein and R. Ravi, When trees collide, an approximation algorithm for the generalized Steiner problem on networks, SIAM Journal on Computing 24(3), 1995
    locator: the main algorithm
---

The primal-dual method builds an integral solution of a covering problem and a feasible solution of the dual of its [LP relaxation](/lp-relaxation/) at the same time. It starts with the dual at zero and the solution empty, raises dual variables of constraints that the solution still violates, and adds a primal variable to the solution when its dual constraint becomes tight. The dual value is a lower bound on OPT by [weak duality](/weak-duality/), and a relaxed form of [complementary slackness](/complementary-slackness/) bounds the cost of the solution by a factor $\beta$ times this dual value. The method never solves the LP, so the algorithms are combinatorial and often fast. This page covers the method for covering problems; the general schema, with both slackness conditions relaxed, is on the [primal-dual schema](/primal-dual-schema/) page.

## In plain words

Each requirement of the problem must be met by buying some items, and each item has a price. Let the unmet requirements put money toward the items that could meet them, all at the same rate. When the money on an item reaches its price, buy the item. Stop when all requirements are met.

The money is never more than the cheapest solution, because each requirement must be met by something it paid for. If each requirement paid toward only a few of the bought items, the bought items cost at most a few times the money. At the end, throw away bought items that are no longer needed, most recent first.

## When it applies

**Convention.** A covering problem in hitting set form has elements $E$ with costs $c_e \ge 0$ and a family $\mathcal{T}$ of subsets of $E$. A solution is a set $A \subseteq E$ that meets each $T \in \mathcal{T}$. The LP and its dual are

$$\text{LP: } \min \sum_{e} c_e x_e \ \text{ s.t. } \sum_{e \in T} x_e \ge 1 \ \forall T \in \mathcal{T},\ x \ge 0. \qquad \text{Dual: } \max \sum_{T} y_T \ \text{ s.t. } \sum_{T \ni e} y_T \le c_e \ \forall e,\ y \ge 0.$$

OPT is the least cost of a solution, LP* the LP optimum, and the ratio convention is ALG $\le \rho \cdot$ OPT. The family $\mathcal{T}$ may be exponential, as for the cuts of a graph, if the violated sets can be found fast.

**Relaxed complementary slackness.** Let $A$ be a solution and $y$ a feasible dual. If each $e \in A$ is tight, $\sum_{T \ni e} y_T = c_e$, and each $T$ with $y_T > 0$ has $|A \cap T| \le \beta$, then $c(A) \le \beta \sum_T y_T \le \beta \cdot \text{LP}^* \le \beta \cdot \text{OPT}$.

*Proof.* $c(A) = \sum_{e \in A} \sum_{T \ni e} y_T = \sum_T |A \cap T| \, y_T \le \beta \sum_T y_T$. The rest is weak duality. $\square$

Exact complementary slackness would ask $|A \cap T| = 1$ for each $T$ with $y_T > 0$, which would prove optimality. The method relaxes this to $\beta$.

Use the method when:

- the problem has a covering LP with a clear dual, as in [set cover](/set-cover/), [weighted vertex cover](/weighted-vertex-cover/), Steiner forest, feedback vertex set or facility location;
- you want a combinatorial algorithm, without an LP solver, often in near-linear time;
- the constraint family is too large to write down, but a violated constraint, such as a cut, is easy to find.

## The template

The input is $(E, c, \mathcal{T})$. The output is a solution $A$ and a feasible dual $y$.

```pseudo id=main
PRIMAL-DUAL(E, c, T)
L1  A ← ∅;  y ← 0;  ℓ ← 0
L2  while some set of T does not meet A do
L3      ℓ ← ℓ + 1
L4      V ← VIOLATED(A)                          ▷ a nonempty family of sets of T that miss A
L5      raise y_T for all T ∈ V at the same rate until some e ∉ A has Σ_{T ∋ e} y_T = c_e
L6      e_ℓ ← that tight element;  A ← A ∪ {e_ℓ}
L7  A ← CLEANUP(A)                               ▷ for example, reverse delete over e_ℓ, ..., e_1
L8  return A, y
```

The holes are named in the comments.

- **VIOLATED** in line L4 chooses which unmet constraints get dual money. The simplest choice is one violated set. For network design, it is the family of all minimal violated sets, such as the components of the current forest that still need an edge.
- **CLEANUP** in line L7 removes elements that are no longer needed. *Reverse delete* considers $e_\ell, \ldots, e_1$ in this order and removes each element whose removal keeps $A$ feasible. Some problems need no cleanup.

**Invariants.** The dual stays feasible: line L5 stops at the first tight constraint, and a raised set $T$ misses $A$, so no element of $A$ gets more money. Each element of $A$ is tight. So the relaxed slackness lemma applies.

**The ratio.** Let $A_f$ be the final solution and $\varepsilon_\ell$ the raise in iteration $\ell$. Suppose that in each iteration, $\sum_{T \in V_\ell} |A_f \cap T| \le \beta |V_\ell|$. Then $c(A_f) \le \beta \cdot \text{OPT}$.

*Proof.* As in the lemma, $c(A_f) = \sum_T |A_f \cap T| \, y_T$. Each $y_T$ is the sum of the raises $\varepsilon_\ell$ of the iterations with $T \in V_\ell$, so

$$c(A_f) = \sum_\ell \varepsilon_\ell \sum_{T \in V_\ell} |A_f \cap T| \le \beta \sum_\ell \varepsilon_\ell |V_\ell| = \beta \sum_T y_T \le \beta \cdot \text{OPT}. \quad \square$$

With one set in each $V_\ell$, the condition is $|A_f \cap T| \le \beta$ for each raised $T$, which holds with $\beta = \max_T |T|$. For Steiner forest, the condition holds only on average over $V_\ell$, and reverse delete is needed to prove it.

## Classic examples

| problem | sets $T$ | VIOLATED | CLEANUP | ratio |
|---|---|---|---|---|
| [Weighted vertex cover](/primal-dual-weighted-vertex-cover/) (Bar-Yehuda and Even 1981) | the edges | one uncovered edge | none | 2 |
| [Set cover with frequency $f$](/set-cover-primal-dual/) | the sets that hold one element | one uncovered element | none | $f$ |
| [Steiner forest](/goemans-williamson-steiner-forest/) (Agrawal, Klein and Ravi 1995; Goemans and Williamson 1995) | the cuts that separate a terminal pair | all components that separate a pair | reverse delete | $2 - 2/k$ for $k$ terminals |
| Shortest $s$-$t$ path | the $s$-$t$ cuts | the component of $s$ | reverse delete | 1, and it is Dijkstra's algorithm |
| [Feedback vertex set](/feedback-vertex-set-problem/) (Chudak, Goemans, Hochbaum and Williamson 1998) | the cycles | a semi-disjoint or other chosen cycle | reverse delete | 2 |
| [Facility location](/jain-vazirani-facility-location/) (Jain and Vazirani 2001) | one constraint for each client | all unconnected clients | a maximal independent set of open facilities | 3 |

The facility location algorithm relaxes the primal slackness conditions as well, so it is an instance of the general [primal-dual schema](/primal-dual-schema/) rather than of the template above.

## Variations

- **Uniform raising.** Raising all minimal violated sets at once, instead of one, is the key idea of Agrawal, Klein and Ravi and of Goemans and Williamson. It gives ratio 2 for a large class of network design problems with proper cut functions.
- **Reverse delete.** Without it, Steiner forest and feedback vertex set lose the ratio. The order matters: deleting the latest additions first keeps the structure that the analysis needs.
- **Local ratio.** Each primal-dual algorithm of this kind is a [local ratio](/local-ratio-technique/) algorithm, and the reverse holds too (Bar-Yehuda and Rawitz 2005). The dual raise in line L5 is the local ratio weight function.
- **Dual fitting.** Greedy algorithms build a dual that is not feasible, and then scale it down to make it feasible; see [dual fitting](/dual-fitting/). This gives $H_n$ for set cover, where primal-dual gives $f$.
- **Online primal-dual.** When the constraints arrive one at a time, the dual of each new constraint is raised and the primal grows by a multiplicative rule; this gives $O(\log m \log n)$ for [online set cover](/online-set-cover-problem/) (Alon, Awerbuch, Azar, Buchbinder and Naor 2009).

## Pitfalls

- **The integrality gap is a hard limit.** The method proves $\text{ALG} \le \beta \sum_T y_T \le \beta \cdot \text{LP}^*$, so $\beta$ is at least the integrality gap of the LP. For vertex cover the gap tends to 2, so no primal-dual analysis on this LP gives less.
- **Dual infeasibility.** Line L5 must stop at the first tight element. Raising a set that already meets $A$ would make an element of $A$ overpaid, and the equality $c(A) = \sum_T |A \cap T| y_T$ breaks.
- **One set at a time for Steiner problems.** For Steiner forest, a single raised cut can meet as many final edges as there are terminals, so the bound $|A \cap T| \le \beta$ fails for single cuts. The proof of ratio 2 needs the average over all components raised together.
- **Large frequency.** When each element is in many sets, $f$ is large and greedy, with $H_d$, is better. The two methods use the same LP and different parameters.

## Exercises

1. Run the vertex cover version on the path $a$-$b$-$c$ with unit weights and the edge order $ab$, $bc$, adding all tight vertices in the order $a$, $b$, and then apply reverse delete. *Answer:* raising $y_{ab}$ to 1 makes $a$ and $b$ tight, and both are added; then $bc$ is covered. $A = \{a, b\}$ with dual value 1. Reverse delete tries $b$ first, which is needed for $bc$, and then $a$, which can go. The result is $\{b\}$, which is optimal.
2. Show that the condition of the ratio theorem holds with $\beta = f$ for set cover with one element raised in each iteration. *Answer:* the raised constraint $T$ is the family of sets that hold the element, so $|A_f \cap T| \le |T| = f_e \le f$.
3. Show that the primal-dual vertex cover algorithm without cleanup gives ratio exactly 2 on $K_{k,k}$ with unit weights, when the first $k$ edges of the order form a perfect matching. *Answer:* each matching edge raises its dual to 1 and makes both ends tight, so all $2k$ vertices are added, while OPT $= k$. The dual value is $k$, so the bound $2 \cdot k$ is reached.

## References
