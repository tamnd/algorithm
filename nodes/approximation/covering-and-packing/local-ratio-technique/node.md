---
tag: 681RZH
kind: technique
slug: local-ratio-technique
name: Local ratio technique
aliases:
- local ratio method
- local ratio theorem
area: approximation/covering-and-packing
level: advanced
summary: Split the weight function into a part on which every solution is r-approximate and a remainder, recurse on the remainder, and add the bounds by the local ratio theorem.
prereqs: [approximation-ratio, weighted-vertex-cover]
see_also: [bar-yehuda-even-vertex-cover, primal-dual-approximation, primal-dual-schema, weighted-vertex-cover, set-cover-primal-dual, feedback-vertex-set-problem, weighted-interval-scheduling, primal-dual-weighted-vertex-cover]
sources:
  - paper: doi:10.1016/0196-6774(81)90020-1
    title: Reuven Bar-Yehuda and Shimon Even, A linear-time approximation algorithm for the weighted vertex cover problem, Journal of Algorithms 2(2), 1981
    locator: pages 198 to 203
  - title: Reuven Bar-Yehuda and Shimon Even, A local-ratio theorem for approximating the weighted vertex cover problem, Annals of Discrete Mathematics 25, 1985
    locator: pages 27 to 46
  - paper: doi:10.1145/1041680.1041683
    title: Reuven Bar-Yehuda, Keren Bendel, Ari Freund and Dror Rawitz, Local ratio, a unified framework for approximation algorithms, ACM Computing Surveys 36(4), 2004
    locator: pages 422 to 463
  - title: Amotz Bar-Noy, Reuven Bar-Yehuda, Ari Freund, Joseph Naor and Baruch Schieber, A unified approach to approximating resource allocation and scheduling, Journal of the ACM 48(5), 2001
    locator: the local ratio theorem for maximization and its use for interval scheduling
  - title: Vineet Bafna, Piotr Berman and Toshihiro Fujito, A 2-approximation algorithm for the undirected feedback vertex set problem, SIAM Journal on Discrete Mathematics 12(3), 1999
    locator: the main algorithm
  - title: Reuven Bar-Yehuda and Dror Rawitz, On the equivalence between the primal-dual schema and the local ratio technique, SIAM Journal on Discrete Mathematics 19(3), 2005
    locator: the main theorem
---

The local ratio technique designs approximation algorithms for problems with a linear weight function. It splits the weights as $w = w_1 + w_2$, where $w_1$ is chosen so that every solution of a certain kind is $r$-approximate for $w_1$, solves the problem for $w_2$ by recursion, and combines the two bounds with the *local ratio theorem*. Bar-Yehuda and Even introduced it in 1981 and 1985 for [weighted vertex cover](/weighted-vertex-cover/), where it gives the linear-time [Bar-Yehuda-Even algorithm](/bar-yehuda-even-vertex-cover/) of ratio 2. The proofs never solve or even write down an LP, but each local ratio algorithm can be read as a [primal-dual](/primal-dual-approximation/) algorithm, and the reverse also holds.

## In plain words

You must pay for a solution, and each piece of it has a price. Take a small part of the prices away so that, under this part alone, any reasonable solution costs at most a fixed factor times the cheapest one. Put that part aside and solve the problem again with the prices that are left. Some piece now has price zero, so the problem gets easier at each step.

At the end, you take pieces of price zero, which cost nothing. Now add the parts back. The answer was good under each part, and the cheapest solution must pay for each part, so the answer is good for the full prices too.

## When it applies

**Convention.** A problem has a set $N$ of elements, a family $\mathcal{F}$ of feasible solutions, each written as a vector $x \in \{0, 1\}^N$, and a weight function $w \in \mathbb{R}^N$. For a minimization problem, $\text{OPT}(w) = \min_{x \in \mathcal{F}} w \cdot x$, and $x \in \mathcal{F}$ is *$r$-approximate for $w$* if $w \cdot x \le r \cdot \text{OPT}(w)$. The ratio convention is ALG $\le \rho \cdot$ OPT with $\rho = r$. For maximization, reverse the inequalities.

**The local ratio theorem (Bar-Yehuda and Even 1985).** Let $w = w_1 + w_2$. If $x \in \mathcal{F}$ is $r$-approximate for $w_1$ and for $w_2$, then $x$ is $r$-approximate for $w$.

*Proof.* Let $x^*$ be optimal for $w$. It is feasible, so $\text{OPT}(w_1) \le w_1 \cdot x^*$ and $\text{OPT}(w_2) \le w_2 \cdot x^*$. Then

$$w \cdot x = w_1 \cdot x + w_2 \cdot x \le r \, \text{OPT}(w_1) + r \, \text{OPT}(w_2) \le r (w_1 \cdot x^* + w_2 \cdot x^*) = r \, \text{OPT}(w). \quad \square$$

The theorem needs only that the feasible family is the same for $w$, $w_1$ and $w_2$, and that the cost is linear. The maximization form has the same proof with $\ge$.

**Effective weights.** A weight function $w_1$ is *$r$-effective* for a class of solutions, for example all minimal solutions, if each solution in the class is $r$-approximate for $w_1$. The usual way to prove it is to find a number $\beta$ with $w_1 \cdot x \ge \beta$ for each feasible $x$ and $w_1 \cdot x \le r \beta$ for each $x$ in the class.

Use the technique when:

- the problem is a covering problem with nonnegative weights, such as [vertex cover](/vertex-cover/), [set cover](/set-cover/), feedback vertex set or a Steiner problem, and a small local structure (an edge, an element, a cycle) forces each solution to pay something;
- the problem is a packing or scheduling problem with a local conflict structure, using the maximization form;
- you want a simple, combinatorial and often linear-time algorithm with a short proof, without solving an LP.

## The template

The input is a problem $(N, \mathcal{F})$ and weights $w \ge 0$. The output is a feasible solution that is $r$-approximate for $w$.

```pseudo id=main
LOCAL-RATIO(N, F, w)
L1  Z ← {j ∈ N : w_j = 0}
L2  if Z contains a feasible solution then
L3      return PRUNE(Z)                        ▷ a feasible solution inside Z, in the class
L4  w1 ← EFFECTIVE(N, F, w)                     ▷ 0 ≤ w1 ≤ w, r-effective, w1_j = w_j > 0 for some j
L5  w2 ← w − w1
L6  return LOCAL-RATIO(N, F, w2)
```

The two holes are named in the comments.

- **EFFECTIVE** in line L4 returns a weight function $w_1$ with $0 \le w_1 \le w$ that is $r$-effective for the class of solutions that PRUNE returns, and that gives at least one new element weight 0 in $w_2$.
- **PRUNE** in line L3 returns a feasible solution inside $Z$ that belongs to the class, for example by deleting elements while the solution stays feasible, so that the result is minimal.

**Correctness.** By induction on the number of positive weights. In the base case the returned $x$ uses only elements of weight 0, so $w \cdot x = 0 = \text{OPT}(w)$. In the step, the recursive call returns $x$ that is $r$-approximate for $w_2$ by induction; $x$ is in the class, so it is $r$-approximate for $w_1$ by line L4. The local ratio theorem gives that $x$ is $r$-approximate for $w$. Line L4 keeps $w_2 \ge 0$ and makes one more weight zero, so there are at most $|N|$ calls. $\square$

**The example: weighted vertex cover.** For an edge $\{u, v\}$ with $w(u), w(v) > 0$, let $\varepsilon = \min(w(u), w(v))$ and let $w_1$ be $\varepsilon$ on $u$ and $v$ and 0 elsewhere. Each cover contains $u$ or $v$, so $w_1 \cdot x \ge \varepsilon$, and each cover has $w_1 \cdot x \le 2\varepsilon$. So $w_1$ is 2-effective for all covers, PRUNE can return all of $Z$, and the result is a 2-approximation. Written as a loop over the edges, this is the [Bar-Yehuda-Even algorithm](/bar-yehuda-even-vertex-cover/), with $O(n + m)$ time.

**Link to the dual.** In the vertex cover example, set $y_{uv} = \varepsilon$ for the edge used in each step. The weights stay nonnegative, so $\sum_{e \ni v} y_e \le w(v)$ for each vertex, and $y$ is a feasible dual of the LP. The returned cover has only vertices whose weight went to 0, which are exactly the vertices whose dual constraint is tight. This is the [primal-dual algorithm](/primal-dual-weighted-vertex-cover/), and the same reading works in general (Bar-Yehuda and Rawitz 2005).

## Classic examples

- **[Weighted vertex cover](/weighted-vertex-cover/), ratio 2.** The [Bar-Yehuda-Even algorithm](/bar-yehuda-even-vertex-cover/) (1981) above. The 1985 paper adds steps that first remove short odd cycles and gets $2 - \frac{\log \log n}{2 \log n}$.
- **[Set cover](/set-cover/) with frequency $f$, ratio $f$.** For an uncovered element $e$, let $\varepsilon$ be the least weight of a set that holds $e$, and put $\varepsilon$ on each set that holds $e$. Each cover pays at least $\varepsilon$, and each cover pays at most $f_e \varepsilon \le f \varepsilon$. This matches [primal-dual set cover](/set-cover-primal-dual/).
- **[Feedback vertex set](/feedback-vertex-set-problem/) in undirected graphs, ratio 2.** Remove vertices of degree at most 1. If the graph has a semi-disjoint cycle, one with at most one vertex of degree above 2, put equal weights on its vertices; otherwise use weights proportional to $\deg(v) - 1$. Each minimal solution is then 2-approximate for these weights, so PRUNE must return a minimal solution (Bafna, Berman and Fujito 1999; Becker and Geiger 1996; the local ratio form is in the survey of Bar-Yehuda, Bendel, Freund and Rawitz).
- **[Weighted interval scheduling](/weighted-interval-scheduling/), exact.** In the maximization form, take the interval $I$ with the earliest end and put the weight $w(I)$ on $I$ and on each interval that meets it. These intervals all contain the end of $I$, so a feasible solution holds at most one of them, and a solution that holds one of them gets $w(I)$, the best possible. So $w_1$ is 1-effective for such solutions. Bar-Noy, Bar-Yehuda, Freund, Naor and Schieber (2001) extend this to resource allocation with ratio 2 and more.

## Variations

- **Iterative form.** Most local ratio algorithms are loops: apply EFFECTIVE again and again, and keep the weight reductions in place, as in Bar-Yehuda and Even. The final PRUNE pass is then a reverse delete, done in the opposite order of the steps.
- **Maximization.** The theorem holds with $\ge$, and EFFECTIVE must make every solution of the class at least $1/r$ times OPT for $w_1$. Here the class is usually the solutions that are maximal with respect to the current element, and the solution is built on the way back from the recursion.
- **Negative weights.** For maximization, $w_2$ may have negative entries; the algorithm drops elements of nonpositive weight. For minimization, the weights must stay nonnegative.
- **Fractional local ratio.** Bar-Yehuda, Halldórsson, Naor, Shachnai and Shapira (2006) choose $w_1$ from an optimal LP solution, which gives better ratios for some packing problems.
- **Layering.** The layering method for set cover in Vazirani's book subtracts degree-weighted functions in layers. Each layer is a local ratio step with weights proportional to the degree.

## Pitfalls

- **Effective only for some solutions.** For feedback vertex set, the degree weights are 2-effective only for minimal solutions. Returning all of $Z$ without PRUNE can give a much worse ratio.
- **Weights that become negative.** If $w_1 \not\le w$ in a minimization problem, $w_2$ has a negative entry, and the base case cost 0 no longer equals OPT. Take $\varepsilon$ as the least weight in the structure.
- **No progress.** EFFECTIVE must make a new weight zero, or the loop does not terminate. Taking $\varepsilon$ as a minimum makes this true.
- **Changing the feasible family.** The theorem compares the same family $\mathcal{F}$ for all weights. A step that deletes elements or contracts the instance must show that the smaller instance has the same optimum for $w_2$; zero-weight elements may be deleted only because they can be added back for free.
- **The bound is only as good as the lower bound.** The ratio of local ratio, as of primal-dual, can never beat the integrality gap of the LP that it implicitly uses. For vertex cover this gap is 2.

## Exercises

1. Run the Bar-Yehuda-Even algorithm on the triangle with vertices 1, 2 and 3, weights $w = (1, 2, 3)$, and the edge order 1-2, 1-3, 2-3. *Answer:* edge 1-2 has $\varepsilon = 1$, giving $(0, 1, 3)$; edge 1-3 has $\varepsilon = 0$; edge 2-3 has $\varepsilon = 1$, giving $(0, 0, 2)$. The cover $\{1, 2\}$ has weight 3, which is optimal.
2. Show that the numbers $\varepsilon$ of the vertex cover steps form a feasible dual, and deduce that LP* $\ge \sum \varepsilon$. *Answer:* each step lowers $w(v)$ by $\varepsilon$ for each endpoint $v$ of its edge, and the weights stay nonnegative, so $\sum_{e \ni v} y_e \le w(v)$. Weak duality gives LP* $\ge \sum_e y_e$.
3. Prove the maximization form of the local ratio theorem: if $x$ is feasible and $w_i \cdot x \ge \text{OPT}(w_i)/r$ for $i = 1, 2$, then $w \cdot x \ge \text{OPT}(w)/r$. *Answer:* for $x^*$ optimal for $w$, $w \cdot x \ge (\text{OPT}(w_1) + \text{OPT}(w_2))/r \ge (w_1 \cdot x^* + w_2 \cdot x^*)/r = \text{OPT}(w)/r$.

## References
