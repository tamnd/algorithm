---
title: The ListNet top-one loss is convex with gradient P_s minus P_y, and the step 1/M never increases it
proves: [correctness]
status: full
---

One query has documents $x_1, \ldots, x_n$ with labels $y_1, \ldots, y_n$ and scores $s_j = w \cdot x_j$. With $\varphi = \exp$, the top-one probabilities are

$$P_s(j) = \frac{e^{s_j}}{\sum_l e^{s_l}}, \qquad P_y(j) = \frac{e^{y_j}}{\sum_l e^{y_l}},$$

and the loss of the query is the cross-entropy $L(s) = -\sum_j P_y(j) \log P_s(j)$. The training loss is the sum over the queries.

**Lemma 1 (top-one probability).** Under the Plackett-Luce model with weights $e^{s_j}$, the probability that document $j$ is ranked first is $P_s(j)$.

*Proof.* The model picks the first document with probability $e^{s_{\pi(1)}} / \sum_l e^{s_l}$ and then each next document in the same way among those left. Group the permutations by their first element. For first element $j$, the remaining factors are the probabilities of a Plackett-Luce ranking of the other $n - 1$ documents, and these sum to 1 over all such rankings, by induction on $n$. So the sum over the permutations that start with $j$ is $e^{s_j} / \sum_l e^{s_l}$. $\square$

This is the theorem of Cao et al. (2007) that lets ListNet replace the $n!$ permutation probabilities by $n$ top-one probabilities.

**Lemma 2 (gradient).** $\partial L / \partial s_j = P_s(j) - P_y(j)$, and $\nabla_w L = \sum_j (P_s(j) - P_y(j)) x_j$.

*Proof.* Since $\sum_j P_y(j) = 1$, $L(s) = \log \sum_l e^{s_l} - \sum_j P_y(j) s_j$. The derivative of the first term in $s_j$ is $P_s(j)$, and of the second term $P_y(j)$. The chain rule with $\partial s_j / \partial w = x_j$ gives the rest. $\square$

Line L4 of the code computes $P_s - P_y$, and lines L3 and L5 form the sum. The gradient of one query costs $O(n d)$ for $n$ documents with $d$ features, in place of the $O(n^2 d)$ of a pairwise loss.

**Lemma 3 (convex and smooth).** The loss is convex in $w$, and its Hessian satisfies $0 \preceq \nabla^2 L \preceq M I$ with $M = \sum_{\text{queries}} \max_j \lVert x_j \rVert^2$.

*Proof.* For one query, $\nabla^2_w L = X^\top (\operatorname{diag}(p) - p p^\top) X$ with $p = P_s$ and $X$ the matrix with rows $x_j$. For a vector $u$, let $a_j = u \cdot x_j$. Then $u^\top \nabla^2_w L\, u = \sum_j p_j a_j^2 - (\sum_j p_j a_j)^2$, the variance of $a$ under $p$. It is at least 0, and at most $\sum_j p_j a_j^2 \le \max_j a_j^2 \le \max_j \lVert x_j \rVert^2 \lVert u \rVert^2$. Sum over the queries. $\square$

**Theorem (monotone descent).** With $w_{t+1} = w_t - \frac{1}{M} \nabla L(w_t)$, as in lines L1 and L6,

$$L(w_{t+1}) \le L(w_t) - \frac{1}{2M} \lVert \nabla L(w_t) \rVert^2.$$

*Proof.* Lemma 3 and Taylor's theorem give $L(v) \le L(w) + \nabla L(w) \cdot (v - w) + \frac{M}{2} \lVert v - w \rVert^2$. Put $v = w - \nabla L(w)/M$. $\square$

**Lemma 4 (the minimum and two invariances).** For each query, $L(s) \ge H(P_y) = -\sum_j P_y(j) \log P_y(j)$, with equality exactly when $P_s = P_y$, that is when $s - y$ is a constant vector. Adding the same constant to all scores of a query leaves $L$ unchanged.

*Proof.* $L(s) - H(P_y)$ is the Kullback-Leibler divergence of $P_s$ from $P_y$, which is nonnegative and zero exactly when the two distributions are equal. The softmax does not change when a constant is added to every entry. $\square$

So the loss is not zero at its minimum, and its minimum depends on the label values, not only on their order: the labels $2, 0, 1$ and $4, 0, 2$ give different targets. With a linear model the minimum over $w$ is usually larger than $\sum H(P_y)$, since no $w$ needs to reproduce $y$ up to a shift.

**What is not proved.** A smaller loss does not imply a larger NDCG, and nothing here bounds the error on new queries. The tests measure NDCG before and after training on one planted set.

The tests in `impl/python/test_listnet.py` check Lemma 2 by central finite differences in $s$ and in $w$, Lemma 1 by a brute force over the 24 permutations of 4 documents, convexity on random segments, the shift invariance, the theorem along 200 steps, Lemma 4, and the worked example of the page.
