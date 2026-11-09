---
tag: 56A304
kind: concept
slug: epsilon-indicator
name: Epsilon indicator
aliases:
- additive epsilon indicator
- I-epsilon
- multiplicative epsilon indicator
- binary epsilon indicator
area: optimization/multi-objective
level: advanced
summary: The smallest amount by which one set of images must be shifted so that it weakly dominates another. Its sign decides weak dominance between sets exactly.
prereqs: [epsilon-dominance, pareto-dominance]
see_also: [hypervolume-indicator, igd-indicator, spread-indicator, approximate-pareto-set, pareto-front, multi-objective-evolutionary-algorithm, spea2, nsga-ii]
sources:
  - paper: doi:10.1109/TEVC.2003.810758
    title: Eckart Zitzler, Lothar Thiele, Marco Laumanns, Carlos M. Fonseca and Viviane Grunert da Fonseca, Performance assessment of multiobjective optimizers, an analysis and review, IEEE Transactions on Evolutionary Computation 7(2), 2003, 117-132
    locator: the binary epsilon indicator, the relations between approximation sets, and the limits of unary indicators
  - paper: doi:10.1007/978-3-540-30217-9_84
    title: Eckart Zitzler and Simon Künzli, Indicator-based selection in multiobjective search, Parallel Problem Solving from Nature, PPSN VIII, Lecture Notes in Computer Science 3242, Springer, 2004, 832-842
    locator: IBEA, fitness from the additive epsilon indicator between single points
  - paper: doi:10.1162/106365602760234108
    title: Marco Laumanns, Lothar Thiele, Kalyanmoy Deb and Eckart Zitzler, Combining convergence and diversity in evolutionary multiobjective optimization, Evolutionary Computation 10(3), 2002, 263-282
    locator: epsilon-dominance and the archives whose output is an epsilon-Pareto set
  - paper: doi:10.1109/SFCS.2000.892068
    title: Christos H. Papadimitriou and Mihalis Yannakakis, On the approximability of trade-offs and optimal access of Web sources, Proceedings of the 41st IEEE FOCS, 2000, 86-92
    locator: epsilon-Pareto sets in the multiplicative form
---

The epsilon indicator compares two sets of images $A$ and $B$ by the smallest amount $\varepsilon$ by which $A$ must be moved so that every point of $B$ is weakly dominated by a moved point of $A$. Zitzler, Thiele, Laumanns, Fonseca and Grunert da Fonseca defined it in 2003 in an additive form and a multiplicative form. Unlike a single number per set, this binary indicator decides the dominance relation between the sets exactly: $I_{\varepsilon+}(A, B) \le 0$ if and only if $A$ weakly dominates $B$. With a reference set in place of $B$ it becomes a unary indicator, which is weakly but not strictly Pareto compliant.

## In plain words

Take two lists of solutions, each with several costs. Ask how much the costs of the first list would need to drop, by the same amount in every cost, before every solution in the second list is matched by one in the first that is at least as good in every cost. That amount is the epsilon indicator. If it is zero or less, the first list already matches the second. If it is positive, it says by how much the first list falls short. Asking the question both ways tells whether one list is better, worse, or neither.

## The idea

**Convention.** All objectives are minimized, $p$ is the number of objectives, $N$ is the population size, and $y = f(x)$ is the image of $x$. $A$ and $B$ are finite nonempty sets of images. $A \trianglelefteq B$ ($A$ weakly dominates $B$) when every $b \in B$ is weakly dominated by some $a \in A$; $A \triangleleft B$ ($A$ is better) when $A \trianglelefteq B$ but not $B \trianglelefteq A$.

**Definitions.** A point $a$ additively [$\varepsilon$-dominates](/epsilon-dominance/) $b$ when $a_m - \varepsilon \le b_m$ for all $m$. For positive values, $a$ multiplicatively $\varepsilon$-dominates $b$ when $a_m \le \varepsilon\, b_m$ for all $m$. The indicators are the smallest such $\varepsilon$ that works for all of $B$:

$$I_{\varepsilon+}(A, B) = \max_{b \in B} \min_{a \in A} \max_{m} (a_m - b_m), \qquad I_{\varepsilon}(A, B) = \max_{b \in B} \min_{a \in A} \max_{m} \frac{a_m}{b_m}.$$

The formula is the infimum: for one pair, $\max_m (a_m - b_m)$ is the smallest shift with $a - \varepsilon \preceq b$; each $b$ needs only its best $a$; and all of $B$ needs the worst $b$. Each value costs $O(p \lvert A \rvert \lvert B \rvert)$ time. The rest of the page uses the additive form; the multiplicative form behaves the same with $1$ in place of $0$ and ratios in place of differences.

**Theorem 1 (the sign decides weak dominance).** $I_{\varepsilon+}(A, B) \le 0$ if and only if $A \trianglelefteq B$. So $A \triangleleft B$ if and only if $I_{\varepsilon+}(A, B) \le 0 < I_{\varepsilon+}(B, A)$.

*Proof.* $I_{\varepsilon+}(A, B) \le 0$ means that for each $b$ some $a$ has $\max_m (a_m - b_m) \le 0$, that is $a \preceq b$. That is the definition of $A \trianglelefteq B$. The second claim follows by applying the first to both orders. $\square$

So the pair $(I_{\varepsilon+}(A, B), I_{\varepsilon+}(B, A))$ tells all four cases: $A$ better, $B$ better, equal in the sense $A \trianglelefteq B \trianglelefteq A$, or incomparable. Zitzler et al. (2003) showed that no unary indicator, and no finite combination of unary indicators, can do this for all pairs, which is why a binary indicator is needed.

**Theorem 2 (triangle inequality).** $I_{\varepsilon+}(A, C) \le I_{\varepsilon+}(A, B) + I_{\varepsilon+}(B, C)$.

*Proof.* Let $c \in C$. Some $b \in B$ has $b_m - c_m \le I_{\varepsilon+}(B, C)$ for all $m$, and some $a \in A$ has $a_m - b_m \le I_{\varepsilon+}(A, B)$ for all $m$. Add the two. $\square$

**Unary form.** For a reference set $R$, for example a sample of the [Pareto front](/pareto-front/), let $I_{\varepsilon+}(A) = I_{\varepsilon+}(A, R)$, smaller is better.

**Theorem 3 (weak compliance).** If $A \trianglelefteq B$, then $I_{\varepsilon+}(A, R) \le I_{\varepsilon+}(B, R)$.

*Proof.* By Theorem 2, $I_{\varepsilon+}(A, R) \le I_{\varepsilon+}(A, B) + I_{\varepsilon+}(B, R)$, and $I_{\varepsilon+}(A, B) \le 0$ by Theorem 1. $\square$

The unary form is not strictly compliant. With $R = \{(0, 10), (10, 0)\}$, the set $A = \{(0, 10), (10, 0), (5, 5)\}$ is better than $B = \{(0, 10), (10, 0)\}$, but both have $I_{\varepsilon+}(\cdot, R) = 0$. The [hypervolume](/hypervolume-indicator/) separates them; [IGD](/igd-indicator/) does not.

**Link to approximate Pareto sets.** If $Y$ is the set of all feasible images, $A$ is an additive $\varepsilon$-Pareto set exactly when $I_{\varepsilon+}(A, Y) \le \varepsilon$, and a multiplicative one with factor $1 + \varepsilon$ exactly when $I_{\varepsilon}(A, Y) \le 1 + \varepsilon$. So the indicator measures the quality of an [approximate Pareto set](/approximate-pareto-set/) in the sense of Papadimitriou and Yannakakis.

## Examples

**A better set.** Let $A = \{(1, 4), (2, 2), (4, 1)\}$ and $B = \{(1, 4), (3, 3), (4, 1)\}$. For $b = (3, 3)$ the best $a$ is $(2, 2)$ with $\max(-1, -1) = -1$; the other points of $B$ are in $A$ and give $0$. So $I_{\varepsilon+}(A, B) = 0$. In the other order, the hard point is $(2, 2)$: $(3, 3)$ gives $\max(1, 1) = 1$, $(1, 4)$ gives $\max(-1, 2) = 2$, and $(4, 1)$ gives $\max(2, -1) = 2$, so $I_{\varepsilon+}(B, A) = 1$. By Theorem 1, $A \triangleleft B$: $B$ must move by $1$ in every objective to match $A$. The multiplicative value $I_{\varepsilon}(B, A) = 3/2$ comes from $(3, 3)$ against $(2, 2)$.

**Incomparable sets.** For $A = \{(0, 2)\}$ and $B = \{(1, 1)\}$, $I_{\varepsilon+}(A, B) = \max(-1, 1) = 1$ and $I_{\varepsilon+}(B, A) = \max(1, -1) = 1$. Both are positive, so neither set weakly dominates the other.

**Multiplicative form.** For $A = \{(2, 4)\}$ and $B = \{(4, 2)\}$, $I_{\varepsilon}(A, B) = \max(2/4, 4/2) = 2$.

The implementation checks these values with exact fractions, and checks Theorem 1, the minimality of the shift, Theorem 2, Theorem 3 and the non-strict example on random sets with fixed seeds.

## Where it is used

- **Benchmarking.** Zitzler et al. (2003) recommend binary indicators such as $I_{\varepsilon+}$ for comparisons, because they can detect dominance between outputs. The unary form against a reference set is common in tables of results, often with the hypervolume.
- **Selection.** IBEA of Zitzler and Künzli (2004) gives each point a fitness from the values $I_{\varepsilon+}(\{x\}, \{y\})$ against all other points and removes the worst point one at a time.
- **Archives.** The epsilon-dominance archives of Laumanns, Thiele, Deb and Zitzler (2002) keep a set whose epsilon indicator against all points seen is at most the chosen $\varepsilon$, with a bound on its size.
- **Approximation algorithms.** Results on [approximate Pareto sets](/approximate-pareto-set/) are bounds on the multiplicative indicator against the whole feasible set.

## References
