---
title: Item-based collaborative filtering computes the adjusted cosine model and a prediction inside the user's ratings
proves: [correctness]
status: full
---

The notation is that of the page: $U_i$ is the set of users who rated item $i$, $I_u$ the set of items that user $u$ rated, $\mu_u$ the mean of the ratings of $u$, and $c_{ui} = r_{ui} - \mu_u$.

**Lemma 1 (the similarity).** After lines L1 to L5, for each pair of items $i \ne j$ the stored value $s(i, j)$ equals the adjusted cosine of the page, $s(i, j) = s(j, i)$, and $-1 \le s(i, j) \le 1$.

*Proof.* Line L1 computes each $\mu_u$ and line L2 each $c_{ui}$. Line L3 visits each unordered pair $\{i, j\}$ once, as $i < j$. Line L4 forms $U = U_i \cap U_j$, and line L5 evaluates the formula of the page with the sums over $U$, or 0 when a sum of squares is 0, and stores it under both orders, so $s(i, j) = s(j, i)$. When neither sum is 0, the value is $\langle x, y \rangle / (\lVert x \rVert \lVert y \rVert)$ for the nonzero vectors $x = (c_{ui})_{u \in U}$ and $y = (c_{uj})_{u \in U}$, and the Cauchy-Schwarz inequality $|\langle x, y \rangle| \le \lVert x \rVert \lVert y \rVert$ gives the range. $\square$

**Lemma 2 (the model).** After lines L6 and L7, each list $M_i$ holds at most $k$ items (all such items when $k$ is not given), each $j \in M_i$ has $j \ne i$ and $s(i, j) > 0$, and no item $j' \notin M_i$ with $j' \ne i$ and $s(i, j') > 0$ comes before an item of $M_i$ in the order of decreasing similarity with ties broken by the smaller id.

*Proof.* Line L7 takes the set of items $j \ne i$ with $s(i, j) > 0$, sorts it in the stated order, and keeps a prefix of length at most $k$. A prefix of a sorted list contains every element that comes before any of its elements. $\square$

**Theorem 1 (correctness of the prediction).** PREDICT$(u, i)$ returns the mean of all ratings if $u$ has no rating, $\mu_u$ if $J = M_i \cap I_u$ is empty, and

$$\hat r_{ui} = \frac{\sum_{j \in J} s(i, j)\, r_{uj}}{\sum_{j \in J} s(i, j)}$$

otherwise. In the last case

$$\min_{j \in J} r_{uj} \le \hat r_{ui} \le \max_{j \in J} r_{uj}.$$

*Proof.* Line L8 handles a user with no rating. Line L9 forms $J$ by testing each item of $M_i$ for a rating of $u$. If $J$ is empty, line L10 returns $\mu_u$. Else, by Lemma 2, each $s(i, j)$ with $j \in J$ is positive, so the denominator $S = \sum_{j \in J} s(i, j)$ is positive, and line L11 returns the stated quotient. With $\alpha_j = s(i, j) / S$ we have $\alpha_j > 0$ and $\sum_{j \in J} \alpha_j = 1$, so $\hat r_{ui} = \sum_{j \in J} \alpha_j r_{uj}$ is a convex combination of the numbers $r_{uj}$, and a convex combination lies between the smallest and the largest of its terms. $\square$

**Corollary 2 (the rating scale).** If all ratings lie in an interval $[a, b]$, then every prediction lies in $[a, b]$.

*Proof.* The mean of all ratings and $\mu_u$ are means of numbers in $[a, b]$. In the third case of Theorem 1, $\hat r_{ui}$ lies between two ratings of $u$, which are in $[a, b]$. $\square$

The corollary needs the positive similarities of line L7. If a negative $s(i, j)$ enters the sum of Sarwar et al., $\sum_j s(i, j) r_{uj} / \sum_j |s(i, j)|$, the weights $s(i, j) / \sum |s|$ are no longer all positive, and the quotient can leave $[a, b]$. With one negative neighbor of similarity $-1$ and rating 5, the quotient is $-5$.
