---
title: The Rocchio update computes its formula, and the difference of centroids is the best unit query
proves: [correctness]
status: full
---

Vectors are sparse maps from terms to real weights; a missing term has weight 0. For a nonempty finite set $D$ of vectors, the centroid is $c(D) = \frac{1}{|D|} \sum_{d \in D} d$. Let $q$ be the query vector, $D_r$ the judged relevant documents, $D_n$ the judged nonrelevant documents, and $\alpha, \beta, \gamma \ge 0$. The Rocchio update is

$$q' = \alpha q + \beta \, c(D_r) - \gamma \, c(D_n),$$

where a term for an empty set is left out, and the clamped query is $q^+$ with $q^+_t = \max(q'_t, 0)$, stored as the terms with $q'_t > 0$.

**Lemma 1 (the code computes the formula).** Lines L1 to L3 build $q'$, and line L4 with clamping builds $q^+$.

*Proof.* After line L1 the map holds $\alpha q_t$ for each term of $q$. The function `centroid` adds $w / |D|$ for each weight $w$ of each vector in $D$, so it returns $c(D)$ on its nonzero terms. Line L2 adds $\beta c(D_r)_t$ to the entry of $t$, creating it with 0 if needed, and line L3 subtracts $\gamma c(D_n)_t$ in the same way. So after line L3, every term $t$ with $q'_t \ne 0$ is in the map with value $q'_t$, and every term not in the map has $q'_t = 0$. Line L4 keeps exactly the entries with a positive value, which are the nonzero coordinates of $q^+$. $\square$

**Lemma 2 (only the ratios matter).** For $\lambda > 0$, the parameters $(\lambda \alpha, \lambda \beta, \lambda \gamma)$ give $\lambda q'$ and $\lambda q^+$. Ranking by cosine similarity, or by dot product, gives the same order for a query and its positive multiple.

*Proof.* The update is linear in $(\alpha, \beta, \gamma)$, and $\max(\lambda x, 0) = \lambda \max(x, 0)$ for $\lambda > 0$. The cosine of $\lambda q$ with $d$ equals the cosine of $q$ with $d$, and the dot product is multiplied by $\lambda$ for every document. $\square$

**Theorem 1 (optimal query).** Let $D_r$ and $D_n$ be nonempty, and let

$$F(x) = \frac{1}{|D_r|} \sum_{d \in D_r} x \cdot d - \frac{1}{|D_n|} \sum_{d \in D_n} x \cdot d$$

be the mean dot product of a query $x$ with the relevant documents minus its mean dot product with the nonrelevant ones. If $c(D_r) \ne c(D_n)$, then among all $x$ with $\lVert x \rVert_2 = 1$, $F$ is maximized exactly by

$$x^* = \frac{c(D_r) - c(D_n)}{\lVert c(D_r) - c(D_n) \rVert_2},$$

and the maximum is $\lVert c(D_r) - c(D_n) \rVert_2$. This $x^*$ is a positive multiple of the Rocchio update with $\alpha = 0$, $\beta = \gamma = 1$ and no clamp.

*Proof.* The dot product is linear, so $F(x) = x \cdot c(D_r) - x \cdot c(D_n) = x \cdot v$ with $v = c(D_r) - c(D_n)$. By the Cauchy-Schwarz inequality, $x \cdot v \le \lVert x \rVert_2 \lVert v \rVert_2 = \lVert v \rVert_2$ for a unit vector $x$, with equality exactly when $x$ is a nonnegative multiple of $v$, that is, $x = v / \lVert v \rVert_2$. $\square$

When all document vectors are scaled to length 1, the dot product with a unit query is the cosine similarity, so $x^*$ is the unit query that best separates the two judged sets by mean cosine. The theorem says nothing about documents that were not judged; that the new query also ranks unseen relevant documents higher is an empirical claim. The full Rocchio update adds $\alpha q$, which keeps the new query near the user's words, and uses $\gamma < \beta$, which trusts the nonrelevant set less. These are choices, not consequences of the theorem.

**Lemma 3 (clamping).** If all document weights are nonnegative, then $q^+ \cdot d \ge q' \cdot d$ for every document $d$, and $q^+$ is the nonnegative vector closest to $q'$ in the Euclidean norm.

*Proof.* For each term, $q^+_t d_t \ge q'_t d_t$ because $q^+_t \ge q'_t$ and $d_t \ge 0$; sum over $t$. For the second claim, the squared distance to a nonnegative $y$ is $\sum_t (y_t - q'_t)^2$, and each term is minimized separately over $y_t \ge 0$ by $y_t = \max(q'_t, 0)$. $\square$

So the clamp cannot lower any dot product, and it removes exactly the evidence that a term marks nonrelevant documents: a document that holds a clamped term loses its penalty. The ranking can change through these lost penalties, so the page treats the clamp as a deliberate choice.

The tests in `impl/python/test_rocchio_algorithm.py` check Lemma 1 in exact rational arithmetic on random vectors, with and without the clamp, check Theorem 1 by comparing $F(x^*)$ with $\lVert v \rVert_2$ and with $F$ at random unit vectors, and check the toy example of the page.
