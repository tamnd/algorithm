---
title: The Borda score counts pairwise wins, and the Borda order minimizes the squared rank distance
proves: [correctness]
status: full
---

Let $L_1, \ldots, L_k$ be the input lists. Each holds distinct items, best first, and may be partial. Let $U$ be the union of their items and $n = |U|$. For a list $L$ and an item $x \in L$, $L(x)$ is the rank of $x$ in $L$, from 1. Lines L1 to L5 give each item $x$ the score

$$s(x) = \sum_{l=1}^{k} p_l(x), \qquad p_l(x) = \begin{cases} n - L_l(x) + 1 & \text{if } x \in L_l, \\ (n - |L_l| + 1)/2 & \text{if } x \notin L_l. \end{cases}$$

Line L4 adds the first case, line L5 adds the second, and line L2 starts each sum at 0, so the code computes exactly $s$. Line L6 sorts by $s$, high first, with ties broken by the item. What remains is to say what $s$ measures.

**Lemma 1 (fair share).** If $L$ misses $m = n - |L| \ge 1$ items, the ranks $|L| + 1, \ldots, n$ carry $\sum_{i = |L| + 1}^{n} (n - i + 1) = m (m + 1)/2$ points, and each missing item gets $m(m+1)/(2m) = (m + 1)/2 = (n - |L| + 1)/2$. So every list hands out $1 + 2 + \cdots + n = n(n+1)/2$ points in total, whether it is full or partial. $\square$

**Theorem 1 (pairwise form).** Extend each list $L$ to a weak order on $U$ by putting every missing item below every item of $L$, with the missing items tied with each other. For $x \in U$ let $w_L(x)$ be the number of items $y \ne x$ that this weak order puts strictly below $x$, and $t_L(x)$ the number of items $y \ne x$ tied with $x$. Then $p_L(x) = 1 + w_L(x) + \tfrac12 t_L(x)$, and so

$$s(x) = k + \sum_{l=1}^{k} \left( w_{L_l}(x) + \tfrac12 t_{L_l}(x) \right).$$

*Proof.* If $x \in L$ at rank $i$, the items below $x$ are the $|L| - i$ items of $L$ after $x$ and the $n - |L|$ missing items, so $w_L(x) = n - i$, $t_L(x) = 0$ and $1 + w_L(x) = n - i + 1 = p_L(x)$. If $x \notin L$, no item is below $x$, the other $n - |L| - 1$ missing items are tied with it, and $1 + \tfrac12 (n - |L| - 1) = (n - |L| + 1)/2 = p_L(x)$. $\square$

So the Borda score is, up to the constant $k$, the number of pairwise contests that $x$ wins over all lists, with a tie worth half a win. This is why Borda is a positional method and a pairwise method at the same time, and why it can disagree with the majority relation: it adds up the margins over all pairs, and a large win against one item can outweigh a small loss against another.

**Theorem 2 (squared rank distance).** Let all lists be full rankings of $U$, so each $L_l$ is a bijection from $U$ to $\{1, \ldots, n\}$. For a ranking $\sigma$ of $U$ let $D(\sigma) = \sum_{l=1}^{k} \sum_{x \in U} (\sigma(x) - L_l(x))^2$. Every order that line L6 can return minimizes $D$, and so does every other order that sorts the items by decreasing $s$.

*Proof.* Let $R(x) = \sum_l L_l(x)$ be the total rank of $x$. For full lists $s(x) = \sum_l (n + 1 - L_l(x)) = k(n+1) - R(x)$, so sorting by decreasing $s$ is sorting by increasing $R$. Expand the square:

$$D(\sigma) = k \sum_{x} \sigma(x)^2 + \sum_{l} \sum_{x} L_l(x)^2 - 2 \sum_{x} \sigma(x) R(x).$$

The first term is $k(1^2 + \cdots + n^2)$ for every permutation $\sigma$, and the second does not depend on $\sigma$. So $\sigma$ minimizes $D$ exactly when it maximizes $F(\sigma) = \sum_x \sigma(x) R(x)$.

Suppose $\sigma(x) < \sigma(y)$ and $R(x) > R(y)$. Let $\sigma'$ be $\sigma$ with the positions of $x$ and $y$ exchanged. Then $F(\sigma') - F(\sigma) = \sigma(y) R(x) + \sigma(x) R(y) - \sigma(x) R(x) - \sigma(y) R(y) = (\sigma(y) - \sigma(x))(R(x) - R(y)) > 0$. So a maximizer of $F$, which exists because there are finitely many permutations, has no such pair: it lists the items by increasing $R$. Any two orders by increasing $R$ differ only inside groups of equal $R$, and exchanging two items with equal $R$ does not change $F$. So all orders by increasing $R$ have the same value of $F$, one of them is a maximizer, and hence all of them are. $\square$

**Remark (cited, not proved here).** For full lists, Coppersmith, Fleischer and Rudra (ACM Transactions on Algorithms 6(3), Article 55, 2010) prove that the order by Borda score has a total Kendall tau distance to the lists at most 5 times the minimum, the Kemeny cost. The test file checks this bound by brute force over all permutations of up to 6 items. It is a property of the order, not of the code, so it needs no separate argument about lines L1 to L6.

The tests in `impl/python/test_borda_count.py` check the formula for $s$, Lemma 1, Theorem 1 with the weak-order extension, Theorem 2 by brute force, and the factor 5.
