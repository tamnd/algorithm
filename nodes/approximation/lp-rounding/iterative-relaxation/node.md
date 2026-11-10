---
tag: 5PMBXS
kind: technique
slug: iterative-relaxation
name: Iterative relaxation
aliases:
- iterative relaxation method
- Singh-Lau iterative relaxation
area: approximation/lp-rounding
level: advanced
summary: Iterative rounding that may also delete a constraint whose violation is provably small; Singh and Lau used it for a spanning tree of cost at most OPT with each degree at most its bound plus 1.
prereqs: [iterative-rounding, extreme-point, spanning-tree-polytope, degree-constrained-spanning-tree]
see_also: [iterative-rounding, jain-iterative-rounding-network-design, shmoys-tardos-gap, minimum-spanning-tree, matroid, matroid-intersection, bicriteria-approximation, lp-relaxation]
sources:
  - paper: doi:10.1145/1250790.1250845
    title: Mohit Singh and Lap Chi Lau, Approximating minimum bounded degree spanning trees to within one of optimal, Proceedings of the 39th ACM Symposium on Theory of Computing, 2007
    locator: the +1 algorithm and its counting lemma
  - book: isbn:9781107007512
    title: Lap Chi Lau, R. Ravi and Mohit Singh, Iterative Methods in Combinatorial Optimization, Cambridge University Press, 2011
    locator: Chapter 4 (spanning trees, with the minimum bounded degree spanning tree) and Chapter 11 (constrained optimization problems)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 11.2 (minimum-cost bounded-degree spanning trees)
  - title: Michel X. Goemans, Minimum bounded degree spanning trees, Proceedings of the 47th IEEE Symposium on Foundations of Computer Science, 2006
    locator: the +2 result by matroid intersection
---

Iterative relaxation extends [iterative rounding](/iterative-rounding/) with a second kind of step. When no variable is large enough to round, the counting argument shows that some *constraint* can be deleted at a small, bounded cost in violation, and the LP is solved again without it. The main example is due to Singh and Lau (2007). Given a graph with edge costs and a degree bound $B_v$ for some vertices, they find a spanning tree of cost at most the LP optimum, so at most the cheapest tree that meets the bounds, in which each vertex has degree at most $B_v + 1$. This is the best possible in the additive sense, since deciding whether a tree with all degrees at most 2 exists is the Hamiltonian path problem. Relaxation steps are also behind the degree-bounded results for network design and matroids, and they appear in the proof for the [generalized assignment problem](/shmoys-tardos-gap/).

## In plain words

Some problems have two kinds of rules: the main rule, such as "connect all towns", and side rules, such as "no town may have more than three roads". Solve the fractional version with all the rules. Look at a corner answer and count.

Sometimes a side rule is almost safe: the town has so few roads left to choose from that even if all of them are used, it breaks its limit by at most one. Then drop that side rule and solve again. Dropping a rule can only make the fractional answer cheaper.

The counting shows that some side rule is always almost safe, while side rules remain. When none are left, the main rule alone has a whole answer, and it costs no more than the first fractional answer.

## When it applies

Iterative relaxation fits problems with a well-behaved core LP and some side constraints.

1. **An integral core.** Without the side constraints, the LP has integral vertices: the [spanning tree polytope](/spanning-tree-polytope/), a [matroid](/matroid/) polytope, the intersection of two matroids, or a flow polytope.
2. **Side constraints with a bounded footprint.** Each side constraint has the form $\sum_{e \in D_v} x_e \le B_v$ over a set $D_v$ of variables, such as the edges at a vertex.
3. **A counting lemma.** At each vertex of the LP with side constraints present, after the variables with $x_e = 0$ are deleted, some side constraint has $|D_v \cap \text{support}| \le B_v + k$ for a small $k$. Deleting it can violate it by at most $k$ in the end, since the support only shrinks.

The cost stays at most the first LP value, because deleting constraints and deleting variables with value 0 never raise the LP optimum. The result is a [bicriteria](/bicriteria-approximation/) guarantee with factor 1 on cost and an additive $k$ on the side constraints.

## The template

```pseudo id=main
ITERATIVE-RELAXATION(core constraints, side constraints W)
L1  repeat
L2      find a vertex x of the LP with the core constraints and the side constraints in W
L3      delete each variable with x_e = 0
L4      if some variable has x_e = 1, fix it and update the residual problem
L5      if some v ∈ W has |D_v ∩ support(x)| ≤ B_v + k then remove v from W
L6  until W = ∅
L7  return a vertex of the core LP on the remaining variables
```

Line L4 is optional for spanning trees, and Singh and Lau's +1 algorithm uses only lines L2, L3 and L5. Line L7 returns an integral solution, because the core LP alone has integral vertices.

**Theorem (Singh and Lau 2007).** For a graph $G$ with costs $c$ and degree bounds $B_v$ for $v \in W$, let $\text{LP}$ be the optimum of

$$\min c \cdot x \ \text{ s.t. } x(E) = |V| - 1, \quad x(E(S)) \le |S| - 1 \ (\emptyset \ne S \subseteq V), \quad x(\delta(v)) \le B_v \ (v \in W), \quad x \ge 0.$$

If the LP is feasible, the algorithm with $k = 1$ returns a spanning tree $T$ with $c(T) \le \text{LP}$ and $\deg_T(v) \le B_v + 1$ for each $v \in W$.

*Proof sketch.* The cost and degree parts are short, and the counting lemma is only sketched here; the full proof is in Singh and Lau (2007) and in Chapter 4 of Lau, Ravi and Singh.

1. *Cost.* Deleting a variable with $x_e = 0$ keeps $x$ feasible and optimal. Deleting a side constraint can only lower the optimum. The last LP is the spanning tree polytope on the remaining edges, whose vertices are spanning trees (Edmonds 1971). So $c(T) \le \text{LP}$.
2. *Degree.* When $v$ leaves $W$, it has at most $B_v + 1$ edges in the support, and later supports are subsets. $T$ uses only edges of the last support, so $\deg_T(v) \le B_v + 1$.
3. *Progress (the counting lemma, sketched).* Let $x$ be a vertex with $x_e > 0$ on all remaining edges $E$, and $W \ne \emptyset$. The function $S \mapsto x(E(S))$ is supermodular, so tight sets that meet can be uncrossed. By the rank lemma, there is a laminar family $\mathcal{L}$ of tight sets and a set $T_W \subseteq W$ of tight degree rows with $|\mathcal{L}| + |T_W| = |E|$ and independent vectors. Suppose that each $v \in W$ has at least $B_v + 2$ edges. Give each edge $e = uv$ the token $(1 - x_e)/2$ for each of its ends, and $x_e$ for the smallest set of $\mathcal{L}$ that holds both ends. A set $S \in \mathcal{L}$ receives $|S| - 1 - \sum_R (|R| - 1)$ over its children $R$, which is a positive integer by independence. A vertex $v \in T_W$ receives $\sum_{e \in \delta(v)} (1 - x_e)/2 = (\deg(v) - B_v)/2 \ge 1$. So the rows receive at least $|E|$, while the edges give out exactly $|E|$. So no token is lost, and a linear dependence among the rows follows, against independence. $\square$ (sketch)

## Classic examples

| problem | core LP | side constraints | result |
|---|---|---|---|
| minimum bounded degree spanning tree | spanning tree polytope | $x(\delta(v)) \le B_v$ | cost $\le$ OPT, degree $\le B_v + 1$ (Singh and Lau 2007) |
| bounded degree survivable network design | cut LP of Jain | $x(\delta(v)) \le B_v$ | cost $\le 2 \cdot$ OPT, degree $\le 2B_v + 3$ (Lau, Naor, Salavatipour and Singh 2007) |
| degree bounded matroid basis | matroid base polytope | $x(D_v) \le B_v$, each element in at most $\Delta$ sets | cost $\le$ OPT, violation $\le \Delta - 1$ (Király, Lau and Singh 2008) |
| [generalized assignment](/shmoys-tardos-gap/) | assignment rows | machine loads $\le T$ | cost $\le$ LP, load $\le 2T$ (in Williamson and Shmoys, Section 11.1) |

In the GAP proof, a machine with only one fractional job, or with two fractional jobs whose LP values add up to at least 1, loses its load constraint. It can get at most one extra job, of time at most $T$, which gives the load bound $2T$.

## Variations

- **Relax and round together.** Most uses mix both steps: round variables equal to 1, delete variables equal to 0, and relax a side constraint when the counting allows it. Lau, Ravi and Singh give an iterative proof of Goemans's earlier +2 result in this way: it fixes leaf edges with $x_e = 1$ and relaxes degree bounds.
- **Multiplicative violations.** For directed problems, such as bounded degree arborescences, the counting gives violations that are a constant factor or a constant plus a factor of the bound.
- **Relaxing only the lower side.** With both lower and upper degree bounds $A_v \le \deg(v) \le B_v$, the same method gives a tree with degrees in $[A_v - 1, B_v + 1]$ and cost at most the LP.
- **Limits.** For some problems no relaxation lemma holds with small $k$. The last chapter of Lau, Ravi and Singh discusses where the method fails.

## Pitfalls

- **Relaxing a constraint too early.** The degree bound of $v$ may be dropped only when the current support at $v$ has at most $B_v + k$ edges. Dropping it earlier lets the final tree have many more edges at $v$.
- **Forgetting that deleted variables must stay deleted.** The degree argument uses that the support only shrinks. If a later LP may use a deleted edge again, the bound fails.
- **Rounding up to 1 with degree bounds.** Fixing an edge with $x_e \ge 1/2$, as in iterative rounding, can raise a degree past $B_v + 1$. The +1 result needs relaxation steps, not threshold rounding.
- **A core LP that is not integral.** If the core has fractional vertices, line L7 has nothing to return, and the cost bound against the LP needs a separate rounding step.

## Exercises

1. Show that the +1 bound is best possible unless P = NP. *Answer:* take $B_v = 2$ for every vertex. A spanning tree with all degrees at most 2 is a Hamiltonian path, and deciding whether one exists is NP-hard. If a polynomial algorithm always found a tree with all degrees at most $B_v$ when one exists, it would decide Hamiltonian path. So an additive violation of at least 1 must be allowed.
2. Show that deleting a side constraint cannot raise the LP optimum. *Answer:* the feasible region with fewer constraints contains the old region, so its minimum is at most the old minimum.
3. In the counting lemma, why does a vertex with $\deg(v) \ge B_v + 2$ in the support receive at least 1 token? *Answer:* if its degree row is tight, $x(\delta(v)) = B_v$, so $\sum_{e \in \delta(v)} (1 - x_e)/2 = (\deg(v) - B_v)/2 \ge 1$.
4. Why does the final tree cost at most the first LP, and not just at most OPT? *Answer:* each step deletes a constraint or a variable of value 0, and neither raises the LP optimum. The last LP has integral vertices, so its optimal vertex is a tree of cost at most the first LP value, which is at most OPT.

## References
