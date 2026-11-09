---
tag: MGQQRJ
kind: concept
slug: utility-function
name: Utility function
aliases:
- multi-attribute utility function
- value function
- preference function
area: optimization/multi-objective
level: intro
summary: A real function on the objective space that ranks outcomes the way a decision maker does. When it is known, the multi-objective problem becomes a single-objective one.
prereqs: [pareto-optimality]
see_also: [preference-articulation, scalarization, weighted-sum-method, weighted-tchebycheff-method, lexicographic-optimization, multi-objective-optimization]
sources:
  - book: isbn:9780521438834
    title: Ralph L. Keeney and Howard Raiffa, Decisions with Multiple Objectives, Preferences and Value Tradeoffs, Cambridge University Press, 1993 (first published by Wiley, 1976)
    locator: Chapter 3 (value functions and trade-offs under certainty, additive value functions and preferential independence)
  - book: isbn:9780792382782
    title: Kaisa Miettinen, Nonlinear Multiobjective Optimization, Kluwer, 1999
    locator: Part I, Chapter 2 (decision maker and value function) and Part II, Chapter 4 (the value function method)
  - book: isbn:9783540213987
    title: Matthias Ehrgott, Multicriteria Optimization, second edition, Springer, 2005
    locator: Chapter 1 (orders and preferences in the objective space)
  - paper: "Gerard Debreu, Representation of a preference ordering by a numerical function, in R. M. Thrall, C. H. Coombs and R. L. Davis (editors), Decision Processes, Wiley, 1954, 159 to 165"
    locator: the existence of a continuous utility for a continuous complete preorder
  - paper: "Gerard Debreu, Topological methods in cardinal utility theory, in K. J. Arrow, S. Karlin and P. Suppes (editors), Mathematical Methods in the Social Sciences 1959, Stanford University Press, 1960, 16 to 26"
    locator: additive representations under preferential independence
---

A utility function (or value function) is a real function $u$ on the objective space that orders the outcomes the way a decision maker does: $u(y) > u(y')$ exactly when the decision maker prefers $y$ to $y'$. If $u$ is known, the [multi-objective optimization](/multi-objective-optimization/) problem becomes the single-objective problem of maximizing $u(f(x))$. When $u$ is monotone in the objectives, its maximizers are [Pareto optimal](/pareto-optimality/). In practice $u$ is rarely known in full, and this is why most methods compute the [Pareto front](/pareto-front/) or ask the decision maker step by step (see [preference articulation](/preference-articulation/)).

## In plain words

A utility function is a scoring rule. It takes the numbers of one choice, for example the price, the weight and the speed of a laptop, and gives one score. A higher score means that the buyer likes the choice more.

If you had the buyer's exact scoring rule, the problem would be easy: compute the score of each choice and take the best. The hard part is to get the rule. People can say which of two laptops they prefer, but they find it hard to write down a formula.

A sensible rule never prefers a choice that is worse on every count. Such a rule always picks a fair trade-off, a choice that no other choice beats on every count.

## The idea

**Convention.** All objectives are minimized unless a page says otherwise. The number of objectives is $p \ge 2$, $y = f(x)$ is the image of $x \in X$, and $Y = f(X)$. A utility function is maximized: a larger $u(y)$ is better. Some books minimize a "value function" or a loss instead; the results are the same with the signs reversed.

**Representation.** A decision maker has a preference relation $\succsim$ on $\mathbb{R}^p$: $y \succsim y'$ means "$y$ is at least as good as $y'$". A function $u : \mathbb{R}^p \to \mathbb{R}$ *represents* $\succsim$ when $y \succsim y' \iff u(y) \ge u(y')$ for all $y, y'$. A relation that has a representation must be complete (any two outcomes are comparable) and transitive. Debreu (1954) showed that a complete, transitive and continuous preference relation on $\mathbb{R}^p$ has a continuous representation.

**Not every preference has a utility.** The lexicographic preference on $\mathbb{R}^2$ (smaller $y_1$ is better, and on ties smaller $y_2$ is better) is complete and transitive, but no real function represents it.

*Proof.* Assume $u$ represents it. For each $a \in \mathbb{R}$, $(a, 0)$ is better than $(a, 1)$, so the open interval $I_a = (u(a, 1), u(a, 0))$ is not empty. For $a < b$, each point $(a, t)$ is better than each point $(b, s)$, so $u(a, 1) > u(b, 0)$, and $I_a$ and $I_b$ are disjoint. Choose a rational number in each $I_a$. Distinct $a$ give distinct rationals, so this maps the uncountable set $\mathbb{R}$ one-to-one into the countable set $\mathbb{Q}$, which is impossible. $\square$

So [lexicographic optimization](/lexicographic-optimization/) is a real preference model that no scalar function captures on a continuum.

**Monotone utilities give Pareto optimal answers.** Call $u$ *strictly decreasing* when $y \prec y'$ implies $u(y) > u(y')$, and *weakly decreasing* when $y < y'$ implies $u(y) > u(y')$.

1. If $u$ is strictly decreasing and $\hat{x}$ maximizes $u(f(x))$ over $X$, then $\hat{x}$ is Pareto optimal.
2. If $u$ is weakly decreasing and $\hat{x}$ maximizes $u(f(x))$ over $X$, then $\hat{x}$ is weakly Pareto optimal.

*Proof.* For 1: if some $x \in X$ has $f(x) \prec f(\hat{x})$, then $u(f(x)) > u(f(\hat{x}))$, which contradicts the maximality of $\hat{x}$. For 2, the same argument with $f(x) < f(\hat{x})$. $\square$

A scalarizing function is a utility function of a special form chosen by the method, not by the decision maker. The linear utility $u(y) = -\sum_i \lambda_i y_i$ with all $\lambda_i > 0$ is strictly decreasing; it is the [weighted sum method](/weighted-sum-method/). The function $u(y) = -\max_i w_i (y_i - z_i)$ with $w > 0$ is only weakly decreasing; it is the [weighted Tchebycheff method](/weighted-tchebycheff-method/), and an added term $-\rho \sum_i y_i$ with $\rho > 0$ makes it strictly decreasing.

**Additive utilities.** A utility is *additive* when $u(y) = \sum_{i=1}^p u_i(y_i)$ for functions $u_i$ of one variable. Let the preference be continuous, and let at least three objectives matter to it. Then it has an additive representation exactly when each subset of objectives is preferentially independent of the others: the order on the values of the subset does not depend on the fixed values of the other objectives (Debreu, 1960; Keeney and Raiffa, Chapter 3). Additive utilities are the base of multi-attribute utility theory. The weighted sum is the linear special case.

## Examples

Take the seven images $a = (2, 9)$, $b = (3, 6)$, $c = (4, 7)$, $d = (5, 4)$, $e = (7, 3)$, $f = (8, 5)$ and $g = (9, 1)$, with both objectives minimized.

| utility $u(y)$ | a | b | c | d | e | f | g | best |
|---|---|---|---|---|---|---|---|---|
| $-(y_1 + 2 y_2)$ | $-20$ | $-15$ | $-18$ | $-13$ | $-13$ | $-18$ | $-11$ | $g$ |
| $-(y_1^2 + y_2^2)$ | $-85$ | $-45$ | $-65$ | $-41$ | $-58$ | $-89$ | $-82$ | $d$ |
| $-\max((y_1 - 1)/6, y_2/3)$ | $-3$ | $-2$ | $-7/3$ | $-4/3$ | $-1$ | $-5/3$ | $-4/3$ | $e$ |

All three utilities are decreasing, and each best point is in the front $\{a, b, d, e, g\}$. The third utility selects $e$, which no linear utility with positive weights can select: $e$ is not supported, because the segment from $d$ to $g$ passes below it.

**A utility that is not decreasing.** The utility $u(y) = -|y_1 - y_2|$, which prefers balanced outcomes, gives $-1$ for $d$ and $-3$ for $c$, but it gives $0$ to the dominated outcome $(10, 10)$ if that outcome exists. Its maximizer can then be a dominated point. Such a utility is not a model of a rational decision maker who wants both objectives small.

## Where it is used

- [Preference articulation](/preference-articulation/): with an a priori method, the decision maker gives the utility, or its parameters, before the search.
- [Scalarization](/scalarization/) uses a family of utilities with parameters to reach the points of the front: the [weighted sum method](/weighted-sum-method/), the [weighted Tchebycheff method](/weighted-tchebycheff-method/) and the [achievement scalarizing function](/achievement-scalarizing-function/).
- Interactive methods, such as the [reference point method](/reference-point-method/), assume an implicit utility that the decision maker does not state, and they move toward its maximum.
- [Goal programming](/goal-programming/) and [lexicographic optimization](/lexicographic-optimization/) model preferences that are not linear and, in the lexicographic case, not representable by a utility at all.

## References
