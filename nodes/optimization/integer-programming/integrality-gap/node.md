---
tag: PM7HW1
kind: concept
slug: integrality-gap
name: Integrality gap
aliases:
- integrality gap of a relaxation
- integrality ratio
area: optimization/integer-programming
level: core
summary: Worst-case ratio between the integer optimum and the value of the relaxation.
prereqs: [lp-relaxation, mixed-integer-programming]
see_also: [ideal-formulation, integer-hull, lp-rounding-vertex-cover, lp-rounding-set-cover, approximation-ratio, matching-polytope, chvatal-closure, unique-games-conjecture]
sources:
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms, Cambridge University Press, 2011
    locator: Chapter 1 (integrality gaps of the vertex cover and set cover relaxations)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms, Springer, 2001
    locator: Chapter 12 (introduction to LP duality) and Chapter 13 (set cover via dual fitting)
  - book: isbn:9780471283669
    title: Laurence A. Wolsey, Integer Programming, Wiley, 1998
    locator: Chapter 1 (formulations) and Chapter 2 (relaxation and bounds)
  - book: isbn:9783319110073
    title: Michele Conforti, Gérard Cornuéjols and Giacomo Zambelli, Integer Programming, Springer, 2014
    locator: Chapter 2 (strength of formulations)
  - paper: "Subhash Khot and Oded Regev, Vertex cover might be hard to approximate to within 2 - epsilon, Journal of Computer and System Sciences 74(3) (2008), 335 to 349"
    locator: the main theorem, under the Unique Games Conjecture
---

The integrality gap of a formulation is the worst ratio, over all instances of a problem, between the integer optimum and the optimum of the [LP relaxation](/lp-relaxation/). It measures how far the relaxation can be from the truth. It is a property of the formulation, not of the problem: two formulations with the same integer solutions can have very different gaps. A gap of $\alpha$ is an upper limit for what an [approximation algorithm](/approximation-ratio/) can prove when it compares its answer only with the LP value.

## In plain words

To solve a hard whole-number problem, we often first solve an easier version that allows fractions. The easier answer is always at least as good as the true answer. The gap says how much better it can be, in the worst case.

If the gap is small, the easy answer is a good guide: it tells the solver how far it is from the best, and it helps a rounding method find a good whole-number answer. If the gap is large, the easy answer can be far from the truth for some inputs, and no proof that uses only that answer can show a good guarantee. Writing the problem in a better way can make the gap smaller.

## The idea

Fix a problem and a formulation that maps each instance $I$ to a polyhedron $P(I)$ and an objective $c(I)$. Let $z_{IP}(I)$ be the integer optimum and $z_{LP}(I)$ the value of the relaxation. For a minimization problem with $z_{LP}(I) > 0$, the *integrality gap* is

$$g = \sup_I \frac{z_{IP}(I)}{z_{LP}(I)},$$

and for a maximization problem it is $\sup_I z_{LP}(I) / z_{IP}(I)$. Some authors use the inverse for maximization, so that the gap is at most 1. Either way, $g \ge 1$, and $g = 1$ means that the relaxation gives the exact value on each instance.

Three other uses of the word occur:

- the *absolute gap* $z_{LP}(I) - z_{IP}(I)$ of one instance, often reported as a percentage of $z_{IP}(I)$;
- the *gap closed* by cuts: if cuts raise the relaxation value of a minimization from $z_{LP}$ to $z'$, the fraction closed is $(z' - z_{LP}) / (z_{IP} - z_{LP})$;
- the *relative MIP gap* that a [branch-and-cut](/branch-and-cut/) solver prints: the difference between the best known integer solution and the best bound, divided by the size of the first. The solver stops when it falls below a tolerance such as $10^{-4}$.

**Gap 1 for all objectives means an ideal formulation.** Let $P$ be a rational polyhedron with integer points, and let $P_I$ be its [integer hull](/integer-hull/). Then $\max_P c^T x = \max_{P_I} c^T x$ for each $c$ for which the left side is finite if and only if $P = P_I$. One direction is clear. For the other, take $\bar x \in P \setminus P_I$. Since $P_I$ is a closed convex set, there is a $c$ with $c^T \bar x > \max_{P_I} c^T x$, and the maximum over $P$ is finite for this $c$ because $P$ and $P_I$ have the same recession cone. This is why an [ideal formulation](/ideal-formulation/) is the goal of polyhedral combinatorics.

**Rounding proves upper bounds.** Suppose that an algorithm takes an optimal LP solution $x^*$ of a minimization and returns an integer solution $\hat x$ with $c^T \hat x \le \alpha\, c^T x^*$. Then

$$z_{IP} \le c^T \hat x \le \alpha\, z_{LP},$$

so $g \le \alpha$. The same holds for primal-dual methods that build a dual solution of value $D$ and an integer solution of cost at most $\alpha D$.

**Gaps prove limits.** Conversely, an instance with $z_{IP} = g\, z_{LP}$ shows that no algorithm can find a solution of cost below $g\, z_{LP}$ on it. So an analysis that bounds the answer by $\alpha\, z_{LP}$ must have $\alpha \ge g$. This does not limit algorithms that use other bounds, and it is not a hardness result, but the known hardness results often match the gap of the natural LP.

## Examples

**Vertex cover.** Minimize $\sum_v x_v$ subject to $x_u + x_v \ge 1$ for each edge and $0 \le x \le 1$. On the complete graph $K_k$, $x = (1/2, \ldots, 1/2)$ gives $z_{LP} = k/2$, and each cover needs $k - 1$ vertices, since two vertices outside a cover would leave their edge uncovered. The ratio is

| $k$ | 3 | 4 | 5 | 6 |
|---|---|---|---|---|
| $z_{LP}$ | 3/2 | 2 | 5/2 | 3 |
| $z_{IP}$ | 2 | 3 | 4 | 5 |
| ratio | 4/3 | 3/2 | 8/5 | 5/3 |

and in general $2(k-1)/k$, which tends to 2. [LP rounding](/lp-rounding-vertex-cover/) takes each $v$ with $x^*_v \ge 1/2$ and costs at most $2 z_{LP}$, so the gap is exactly 2. Khot and Regev (2008) showed that, if the [Unique Games Conjecture](/unique-games-conjecture/) holds, no polynomial algorithm reaches $2 - \varepsilon$.

**Set cover.** Let the elements be the $n = 2^k - 1$ nonzero vectors $u$ of $\{0,1\}^k$, and let set $S_v$ contain the $u$ with $u \cdot v = 1 \pmod 2$, for each nonzero $v$. Each element lies in $2^{k-1}$ sets, so $x_v = 2^{1-k}$ for each set is feasible, with value $(2^k - 1)/2^{k-1} < 2$. Any $k - 1$ sets miss an element: the $k - 1$ equations $u \cdot v = 0$ in $k$ unknowns over the field with two elements have a nonzero solution. So $z_{IP} \ge k$, and in fact $z_{IP} = k$, since the $k$ unit vectors give a cover. For $k = 2, 3, 4$ the LP values are $3/2$, $7/4$, $15/8$, and the IP values are 2, 3, 4. The gap is at least about $\tfrac12 \log_2 n$. The [greedy algorithm](/greedy-set-cover/) gives a cover of cost at most $H_n\, z_{LP}$, where $H_n$ is the harmonic number, so the gap is $\Theta(\log n)$.

**Knapsack.** Take two items of profit 1 and weight $W/2 + 1$, and capacity $W$, for an even $W \ge 4$. Only one item fits, so $z_{IP} = 1$, while the relaxation takes one item and a fraction of the other, with $z_{LP} = 2W/(W+2)$. For $W = 10, 20, 100$ this is $5/3$, $20/11$, $100/51$. When each item fits alone, the greedy LP solution has at most one fractional item, so $z_{LP} \le 2 z_{IP}$ and the gap of the natural [knapsack](/knapsack-problem/) relaxation is 2.

**Matching and the effect of the formulation.** For maximum matching in the triangle, the degree constraints $x(\delta(v)) \le 1$ allow $x = (1/2, 1/2, 1/2)$ with value $3/2$, while each matching has one edge. So the gap of the degree formulation is at least $3/2$. Edmonds' odd set inequality $x_{12} + x_{13} + x_{23} \le 1$ removes the point, and the LP value drops to 1. With all odd set inequalities, the formulation is the [matching polytope](/matching-polytope/), and the gap is 1. In the same way, the strong formulation of facility location on the [LP relaxation](/lp-relaxation/) page has a smaller gap than the weak one.

## Where it is used

- **Approximation algorithms.** LP rounding, [primal-dual methods](/primal-dual-approximation/) and dual fitting prove ratios against $z_{LP}$, and the gap tells whether a better ratio is possible with the same LP.
- **Formulation design.** Modelers compare formulations by their gap on test instances and add constraints, as in the [Big-M](/big-m-formulation/) and facility location examples, until the gap is small.
- **Cutting planes.** The gap closed at the root node is the standard measure of the strength of a family of cuts, such as [Gomory mixed-integer cuts](/gomory-mixed-integer-cut/) or [lift-and-project cuts](/lift-and-project/).
- **Branch and cut.** A small gap lets the solver prune many nodes, since each node bound is close to the incumbent. A large gap is the main reason that some models need millions of nodes.
- **Lower bounds for hierarchies.** Results that the gap stays large after many rounds of the [Chvátal closure](/chvatal-closure/) or of other lift-and-project systems show the limits of these methods.

## References
