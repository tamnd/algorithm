---
title: What GENIE3 computes, the sum of its importances and its invariance
proves: [correctness]
status: full
---

**Setup.** Fix a target $y$ with $\frac1n \sum_s (y_s - \bar y)^2 = 1$ (line L2) and the input rows $x_i$. A node holds a multiset $S$ of samples. For a multiset $U$, let $\sigma(U) = \sum_{s \in U} y_s$ and $\mathrm{SS}(U) = \sum_{s \in U} (y_s - \bar y_U)^2$, with $\mathrm{SS}(\emptyset) = 0$. A split of $S$ on input $i$ at threshold $t$ gives $S_L = \{s \in S : x_{i s} \le t\}$ and $S_R = S \setminus S_L$, both non-empty, and its reduction is $\Delta = \mathrm{SS}(S) - \mathrm{SS}(S_L) - \mathrm{SS}(S_R)$. GENIE3 makes no claim about recovery of the true network; the statements below are about the computed weights.

**Lemma 1.** $\Delta = \sigma(S_L)^2 / |S_L| + \sigma(S_R)^2 / |S_R| - \sigma(S)^2 / |S|$, and $\Delta \ge 0$.

*Proof.* For any multiset $U$, $\mathrm{SS}(U) = \sum_{s \in U} y_s^2 - \sigma(U)^2 / |U|$. The sums of $y_s^2$ over $S_L$ and $S_R$ add up to the sum over $S$, so they cancel in $\Delta$, which leaves the formula. $\Delta \ge 0$ because $\mathrm{SS}(S)$ is the least value of $\sum_{s \in S} (y_s - c)^2$ over one constant $c$, while $\mathrm{SS}(S_L) + \mathrm{SS}(S_R)$ is the least value over one constant on each part. $\square$

**Lemma 2 (the split search).** For a node $S$ and a list of inputs, the split search returns a split of the largest reduction among all threshold splits on these inputs, or reports that none exists when no input takes two values on $S$.

*Proof.* Fix an input $i$. Sort $S$ by $x_i$, as $s_1, \ldots, s_{|S|}$. Every threshold $t$ that gives two non-empty parts sends to the left a prefix $s_1, \ldots, s_q$, where $x_{i s_q} \le t < x_{i s_{q+1}}$, so $x_{i s_q} < x_{i s_{q+1}}$. Conversely, each such $q$ is reached by the midpoint threshold. So the threshold splits on $i$ are exactly the prefixes that end between two distinct values. The search visits every $q$ from 1 to $|S| - 1$, keeps the running sum $\sigma(\{s_1, \ldots, s_q\})$, skips the $q$ with equal values, and evaluates $\Delta$ by Lemma 1. It keeps the largest value over all inputs. If no input takes two values, no $q$ is evaluated and the search reports none. $\square$

**Lemma 3 (telescoping).** For a tree grown on $S$ with leaves $\ell_1, \ldots, \ell_r$, the reductions of all its splits add up to $\mathrm{SS}(S) - \sum_{q=1}^{r} \mathrm{SS}(\ell_q)$.

*Proof.* By induction on the number of splits. A tree with no split is one leaf $S$, and both sides are 0. Otherwise the root splits $S$ into $S_L$ and $S_R$ with reduction $\mathrm{SS}(S) - \mathrm{SS}(S_L) - \mathrm{SS}(S_R)$, and the two subtrees have fewer splits. By induction their reductions add up to $\mathrm{SS}(S_L)$ minus the sum over the leaves of the left subtree, and to $\mathrm{SS}(S_R)$ minus the sum over the leaves of the right subtree. Adding the three terms gives the claim. $\square$

**Theorem.** (a) Line L5 takes, at each node, the split of largest reduction over the $K$ drawn inputs. (b) The importances of all inputs in one tree add up to $\mathrm{SS}(S) - \sum_q \mathrm{SS}(\ell_q)$. If every leaf is pure, they add up to $\mathrm{SS}(S)$, which is $n$ when $S$ is all samples once and has expected value $n - 1$ when $S$ is a bootstrap sample of size $n$. (c) If an input row $x_i$ is replaced by $g(x_i)$ for a strictly increasing $g$, then with the same random draws the weights do not change.

*Proof.* (a) is Lemma 2. (b) The importance of an input is the sum of $\Delta$ over the splits on it, so the sum over all inputs is the sum over all splits, and Lemma 3 gives the first claim. A pure leaf has $\mathrm{SS} = 0$. With all samples once, $\mathrm{SS}(S) = n \cdot 1 = n$. For a bootstrap sample, the $n$ draws $Y_1, \ldots, Y_n$ are independent and uniform on the values $y_s$, with mean $\bar y$ and variance 1. Then $\mathrm{E}[\sum_k (Y_k - \bar Y)^2] = (n - 1) \cdot 1$ by the usual identity $\sum_k (Y_k - \bar Y)^2 = \sum_k (Y_k - \bar y)^2 - n (\bar Y - \bar y)^2$, whose expected value is $n - n \cdot \tfrac1n = n - 1$.

(c) A strictly increasing $g$ keeps the order of the values of $x_i$ and keeps equal values equal and distinct values distinct. So at every node, the set of splits on input $i$, given as sets $S_L$, is the same before and after the change, and so are their reductions by Lemma 1, which depend on $y$ only. The draws of line L4 and of the inputs at each node do not depend on the values of the inputs, but only on the number of samples and on which nodes are split; by induction on the depth, the two runs split the same nodes into the same parts and draw the same numbers. So every tree has the same splits, up to the value of the thresholds, and the same reductions, and the weights are equal. $\square$

**Remark.** Part (b) shows that, for full trees and continuous data, the weights into each target add up to about $n$ whatever the true network is. So a weight is meaningful only relative to the other weights of the same target and of the other targets, and the ranking of line L7 is a heuristic.
