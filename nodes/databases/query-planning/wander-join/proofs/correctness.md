---
title: One wander join walk is an unbiased estimate of SUM(v) over the join, and the mean of W walks has variance Var[X]/W
proves: [correctness]
status: full
---

**Setting.** The query is a natural join of relations $R_1, \ldots, R_k$, taken in the walk order, with a selection predicate $\theta_i$ on each $R_i$ (true if there is none) and an expression $v$ of the joined row. The join result $J$ is the set of tuples $\gamma = (t_1, \ldots, t_k)$ with $t_i \in R_i$, $\theta_i(t_i)$ true for each $i$, and $t_i$ and $t_j$ equal on the attributes they share, for each pair $i, j$. The answer is $Q = \sum_{\gamma \in J} v(\gamma)$; COUNT is the case $v = 1$. The walk order has, for each $i \ge 2$, a parent $\eta(i) < i$ that shares attributes with $R_i$, and an index on $R_i$ for those shared attributes. For a row $t$ of $R_{\eta(i)}$, let $M_i(t)$ be the set of rows of $R_i$ that agree with $t$ on those attributes. Every other pair $j < i$ of relations that share attributes is a check of step $i$ (line L7). For $i = 1$, let $M_1 = R_1$.

**The walk.** Line L2 picks $t_1$ uniformly from $R_1$. For $i = 2, \ldots, k$, lines L4 to L6 pick $t_i$ uniformly from $M_i(t_{\eta(i)})$, and the walk fails if this set is empty. The walk also fails if some $t_i$ fails $\theta_i$ or a check of line L7. A walk that does not fail is successful, and its estimate is $X = v(\gamma)/p(\gamma)$, where

$$p(\gamma) = \prod_{i=1}^{k} \frac{1}{|M_i(t_{\eta(i)})|}$$

is the product of the probabilities of the choices (with $M_1(t_{\eta(1)})$ read as $R_1$). A failed walk has estimate $X = 0$.

**Lemma 1 (successful walks are the join result).** The successful walks are exactly the tuples of $J$, and the walk that ends with $\gamma \in J$ has probability $p(\gamma) > 0$.

*Proof.* Let a walk be successful and end with $\gamma = (t_1, \ldots, t_k)$. Each $\theta_i(t_i)$ holds, because the walk did not fail. Take a pair $j < i$ of relations that share attributes. If $j = \eta(i)$, then $t_i \in M_i(t_j)$, so the two rows agree on all shared attributes; the key of step $i$ is the full set of attributes shared with the parent. Otherwise the pair is a check of step $i$, and line L7 passed. So $\gamma \in J$.

Now let $\gamma = (t_1, \ldots, t_k) \in J$. Then $t_1 \in R_1$, and for each $i \ge 2$, $t_i$ agrees with $t_{\eta(i)}$ on their shared attributes, so $t_i \in M_i(t_{\eta(i)})$ and this set is not empty. So the walk can choose $t_1, t_2, \ldots, t_k$ in turn, and the probability of these choices is the product of the probabilities $1/|M_i(t_{\eta(i)})|$, that is $p(\gamma) > 0$. All predicates and checks hold for $\gamma$, so this walk is successful. Two walks with different choices end with different tuples, so each $\gamma$ comes from exactly one sequence of choices. $\square$

**Theorem 1 (unbiased).** $E[X] = Q$.

*Proof.* Failed walks add 0 to the expectation. By Lemma 1 the successful walks are the events "the walk ends with $\gamma$", one for each $\gamma \in J$; they are disjoint and have probability $p(\gamma)$. So

$$E[X] = \sum_{\gamma \in J} p(\gamma) \cdot \frac{v(\gamma)}{p(\gamma)} = \sum_{\gamma \in J} v(\gamma) = Q. \qquad \blacksquare$$

This is the Horvitz-Thompson argument: each unit of the population has a known probability of selection that is not zero, and its value is divided by that probability. A walk that fails is not rejected and walked again. If failed walks were thrown away, the estimate would be divided by the probability of success, which is not known, and the result would be biased. The walk order does not change $E[X]$; it changes only the distribution of $X$. The code computes $E[X]$ exactly as a fraction by going through every sequence of choices, and the tests compare it with a nested loop join, for chain, star and cyclic queries, with and without a selection, in every valid walk order.

**Theorem 2 (the mean of W walks).** Let $X_1, \ldots, X_W$ be independent walks and $\bar X$ their mean (line L8). Then $E[\bar X] = Q$ and $\mathrm{Var}[\bar X] = \sigma^2 / W$, where $\sigma^2 = \mathrm{Var}[X]$. The sample variance $s^2 = \frac{1}{W - 1} \sum_w (X_w - \bar X)^2$ has $E[s^2] = \sigma^2$.

*Proof.* The walk has finitely many outcomes, so $\sigma^2$ is finite. Linearity of expectation gives $E[\bar X] = Q$, independence gives $\mathrm{Var}[\bar X] = \sigma^2/W$, and the statement on $s^2$ is the standard fact for independent samples with the same distribution. $\square$

**The interval.** By the central limit theorem, $(\bar X - Q)/(\sigma/\sqrt W)$ tends in distribution to a standard normal variable, and so does $(\bar X - Q)/(s/\sqrt W)$, because $s \to \sigma$ in probability. So $\bar X \pm z\, s/\sqrt W$ with $z = 1.96$ covers $Q$ with probability that tends to 0.95 as $W$ grows. This is a large sample statement, not a bound for a fixed $W$. For a bound that holds for every $W$, Chebyshev's inequality gives $P(|\bar X - Q| \ge c\,\sigma/\sqrt W) \le 1/c^2$, which needs $\sigma$ or an upper bound on it.

**Cost of a walk.** A walk does at most $k - 1$ index lookups (line L4), one uniform choice per step (line L6), and checks of the predicates and of the non tree pairs, so with hash indexes that store each group as an array, a walk takes $O(k)$ expected time when the attributes per relation are bounded. A walk that fails early is cheaper. With a B-tree, a uniform choice in a range needs the size of the range, for example from counts in the inner nodes, and a lookup costs $O(\log N)$. The extra space is the current path, $O(k)$, and three running sums for $\bar X$ and $s^2$.

**Choice of walk order.** After time $t$, a plan with mean time $E[T]$ per walk has done about $t/E[T]$ walks, so the variance of its estimate is about $\sigma^2 E[T]/t$. Choosing the plan with the smallest estimated $\sigma^2 E[T]$, as the function `choose_plan` does, is a heuristic for speed; Theorem 1 holds for every order, so the choice does not add bias to walks done after it. Walks from the trial phase that are kept in the estimate were used to make the choice, so in theory they can add a small bias; the code does not reuse them.

**Example.** Take $R_1(A, B) = \{(a_1, b_1), (a_2, b_1), (a_3, b_2)\}$, $R_2(B, C) = \{(b_1, c_1), (b_1, c_2), (b_2, c_3)\}$, $R_3(C, D) = \{(c_1, 5), (c_2, 1), (c_2, 3)\}$ and COUNT. The join has 6 tuples. In the order $R_1, R_2, R_3$, the walk fails with probability $1/3$ (from $a_3$, the row $(b_2, c_3)$ has no match), gives $1/p = 3 \cdot 2 \cdot 1 = 6$ with probability $1/3$, and gives $3 \cdot 2 \cdot 2 = 12$ with probability $1/3$. The mean is $6$ and the variance is $24$. In the order $R_3, R_2, R_1$, every walk succeeds with $1/p = 3 \cdot 1 \cdot 2 = 6$, so the estimate is always 6 and the variance is 0.
