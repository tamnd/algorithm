---
title: The primal-dual algorithm returns a set cover of cost at most f times the optimum
proves: [correctness]
status: full
---

The universe $U$ has $n$ elements, the sets are $S_1, \ldots, S_m$ with costs $c_j \ge 0$, and the union of the sets is $U$. For an element $e$, $f_e$ is the number of sets that contain $e$, and $f = \max_e f_e$. For a vector $y$ on the elements, the *load* of set $j$ is $\ell_j(y) = \sum_{e \in S_j} y_e$, and set $j$ is *tight* if $\ell_j(y) = c_j$. The dual LP is

$$\max \sum_{e \in U} y_e \quad \text{subject to} \quad \ell_j(y) \le c_j \text{ for each } j, \qquad y \ge 0.$$

**Lemma 1 (the invariant).** At the start of each iteration of the loop of line L2, and at the end:

1. $y \ge 0$, and $\ell_j(y) \le c_j$ for each $j$, so $y$ is dual feasible;
2. each $j \in C$ is tight.

*Proof.* Before the loop, $y = 0$ and $c \ge 0$, so part 1 holds, and $C = \emptyset$, so part 2 holds. Take an iteration that visits $e$. If line L3 skips $e$, nothing changes. Else $e$ is not covered, so $y_e = 0$ until now, because line L5 is the only line that changes $y_e$ and it runs at most once for each element. Line L4 sets $\delta = \min_{j : e \in S_j} (c_j - \ell_j(y))$. The set of such $j$ is not empty, because the sets cover $U$, and $\delta \ge 0$ by part 1. Line L5 raises $y_e$ from 0 to $\delta$. This adds $\delta$ to the load of each set that contains $e$, and changes no other load. For each such set, the new load is $\ell_j(y) + \delta \le \ell_j(y) + (c_j - \ell_j(y)) = c_j$. So part 1 still holds. For part 2, the sets of $C$ were tight before. A set of $C$ that contains $e$ would cover $e$, and $e$ is not covered, so no set of $C$ contains $e$, and the loads of the sets of $C$ do not change. Line L6 adds only sets that are tight now. So part 2 holds. $\square$

**Lemma 2 (a cover).** At the end, $C$ covers $U$.

*Proof.* Each element $e$ is visited once in line L2. If $e$ is covered at its visit, it stays covered, because sets are never removed from $C$. Else let $j^*$ be a set containing $e$ that attains the minimum in line L4. After line L5, its load is $\ell_{j^*} + \delta = c_{j^*}$, so $j^*$ is tight and contains $e$, and line L6 adds it to $C$ if it is not there yet. So $e$ is covered after its visit. $\square$

**Theorem (Bar-Yehuda and Even 1981).** The algorithm returns a cover $C$ with

$$\sum_{j \in C} c_j \le \sum_{e \in U} f_e \, y_e \le f \sum_{e \in U} y_e \le f \cdot \text{LP}^* \le f \cdot \text{OPT}.$$

*Proof.* By Lemma 2, $C$ is a cover. By part 2 of Lemma 1, each $j \in C$ is tight at the end, so

$$\sum_{j \in C} c_j = \sum_{j \in C} \sum_{e \in S_j} y_e = \sum_{e \in U} y_e \cdot |\{ j \in C : e \in S_j \}| \le \sum_{e \in U} y_e f_e.$$

The middle step exchanges the order of summation. The last step uses $y_e \ge 0$ and $|\{ j \in C : e \in S_j \}| \le f_e$. Next, $f_e \le f$ and $y_e \ge 0$ give $\sum_e f_e y_e \le f \sum_e y_e$. By part 1 of Lemma 1, $y$ is dual feasible, so weak duality gives $\sum_e y_e \le \text{LP}^*$. An optimal cover is a feasible 0-1 point of the primal LP, so $\text{LP}^* \le \text{OPT}$. $\blacksquare$

**Remark (relaxed complementary slackness).** The proof uses two facts. If $x_j = 1$ then set $j$ is tight: this is the primal complementary slackness condition, and it holds exactly. If $y_e > 0$ then $\sum_{j \ni e} x_j \le f$: this is the dual condition relaxed by the factor $f$. Each primal-dual algorithm with these two conditions has ratio $f$; see the primal-dual method page.
