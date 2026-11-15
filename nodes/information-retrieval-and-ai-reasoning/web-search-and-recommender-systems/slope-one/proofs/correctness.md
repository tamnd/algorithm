---
title: Slope One keeps exact difference tables under updates and returns the Slope One predictions
proves: [correctness]
status: full
---

The notation is that of the page: $I_u$ is the set of items that user $u$ rated, $S(j, i)$ the set of users who rated both $j$ and $i$, $c(j, i) = |S(j, i)|$, and $\operatorname{dev}(j, i)$ the mean of $r_{wj} - r_{wi}$ over $w \in S(j, i)$. All statements are about exact arithmetic.

**Lemma 1 (the offset of slope one).** Let $(x_1, y_1), \ldots, (x_c, y_c)$ be real pairs with $c \ge 1$. The function $L(b) = \sum_{t=1}^{c} (x_t + b - y_t)^2$ has the unique minimizer $b^* = \frac{1}{c} \sum_{t=1}^{c} (y_t - x_t)$. With $x_t = r_{wi}$ and $y_t = r_{wj}$ for the users $w \in S(j, i)$, $b^* = \operatorname{dev}(j, i)$.

*Proof.* $L$ is a quadratic polynomial in $b$ with leading coefficient $c > 0$. Its derivative is $L'(b) = 2 \sum_t (x_t + b - y_t) = 2 c b - 2 \sum_t (y_t - x_t)$, which is zero exactly at $b = b^*$. Since $L''(b) = 2c > 0$, $L$ is strictly convex, so $b^*$ is its unique minimizer. $\square$

**Lemma 2 (antisymmetry).** $S(j, i) = S(i, j)$, $c(j, i) = c(i, j)$ and $\operatorname{dev}(j, i) = -\operatorname{dev}(i, j)$.

*Proof.* "Rated both $j$ and $i$" is symmetric in $i$ and $j$, and each term $r_{wj} - r_{wi}$ is the negative of $r_{wi} - r_{wj}$. $\square$

**Lemma 3 (the table invariant).** Call the tables *exact* for a rating set $K$ if, for every ordered pair of distinct items $(j, i)$, an entry exists exactly when $c(j, i) > 0$, and then $\mathit{count}(j, i) = c(j, i)$ and $\mathit{diff}(j, i) = \sum_{w \in S(j, i)} (r_{wj} - r_{wi})$, with $S$ and $c$ taken in $K$. If the tables are exact for $K$, then after ADD$(u, i, v)$ they are exact for the new rating set, and after REMOVE$(u, i)$ they are exact for $K \setminus \{(u, i)\}$.

*Proof.* First let ADD be called with $(u, i) \notin K$, so line L1 does nothing. The new set is $K' = K \cup \{(u, i)\}$. A set $S(a, b)$ changes only if $u$ joins it, which happens exactly for the pairs $\{a, b\} = \{i, j\}$ with $j \in I_u$, the items that $u$ rated before the call. For such a pair, $S'(i, j) = S(i, j) \cup \{u\}$, so $c$ grows by 1 and the sum for $(i, j)$ gains the term $v - r_{uj}$, and the sum for $(j, i)$ gains $r_{uj} - v$. Lines L2 to L4 make exactly these changes, creating an entry with the value 0 first when none exists. No other pair changes, and line L5 stores $r_{ui}$, so the tables are exact for $K'$.

Now let REMOVE$(u, i)$ be called with $(u, i) \in K$ and $v = r_{ui}$. By the same argument, the sets that change are $S(i, j)$ and $S(j, i)$ for $j \in I_u \setminus \{i\}$, which lose $u$. REMOVE subtracts 1 from each such count and the term of $u$ from each such sum, and deletes the entry when the count becomes 0, which is when $S$ becomes empty. So the tables are exact for $K \setminus \{(u, i)\}$.

Last, let ADD be called with $(u, i) \in K$. Line L1 calls REMOVE, after which the tables are exact for $K \setminus \{(u, i)\}$, and the rest of ADD is the first case for this set. $\square$

**Corollary 4 (order independence).** Start from empty tables, which are exact for the empty set. After any sequence of ADD and REMOVE calls, the tables are exact for the current rating set. In particular, they do not depend on the order of the calls.

*Proof.* Induction on the number of calls, with Lemma 3 for the step. $\square$

**Theorem 5 (the predictions).** If the tables are exact, PREDICT$(u, j, \text{false})$ returns the Slope One prediction and PREDICT$(u, j, \text{true})$ returns the Weighted Slope One prediction of the page when $R_j$ is not empty, and the fallback otherwise. Moreover

$$\hat r^{\,w}_{uj} = \frac{1}{\sum_{i \in R_j} c(j, i)} \sum_{i \in R_j} \sum_{w \in S(j, i)} \bigl(r_{ui} + r_{wj} - r_{wi}\bigr),$$

the plain mean of the votes $r_{ui} + r_{wj} - r_{wi}$ over all pairs $(i, w)$ with $i \in R_j$ and $w \in S(j, i)$.

*Proof.* Line L6 forms $R = \{ i \in I_u : i \ne j, \mathit{count}(j, i) > 0 \}$, which is $R_j$ because the tables are exact. If it is empty, line L7 returns the fallback. Else line L8 computes $g_i = \mathit{diff}(j, i) / \mathit{count}(j, i) + r_{ui} = \operatorname{dev}(j, i) + r_{ui}$, and line L9 returns the mean of the $g_i$ with weights 1 or $c(j, i)$, which are the two formulas of the page. For the identity, $c(j, i) \, g_i = c(j, i) \, r_{ui} + \sum_{w \in S(j, i)} (r_{wj} - r_{wi}) = \sum_{w \in S(j, i)} (r_{ui} + r_{wj} - r_{wi})$; sum over $i \in R_j$ and divide by $\sum_i c(j, i)$. $\square$

**Proposition 6 (shift of one user).** If every rating of one user $u$ is shifted by a constant $a$, no $\operatorname{dev}$ changes, and every prediction for $u$ by either scheme, including the fallback when $u$ has ratings, increases by $a$.

*Proof.* Each $w \in S(j, i)$ contributes $r_{wj} - r_{wi}$, and for $w = u$ the shift cancels in the difference. The sets $S$ do not change, so neither do $R_j$ and the counts. Each $g_i = \operatorname{dev}(j, i) + r_{ui}$ grows by $a$, and a weighted mean of numbers that all grow by $a$, with fixed weights, grows by $a$. The mean of $u$ also grows by $a$. $\square$

In floating point, Lemma 3 holds up to rounding: REMOVE subtracts a term that was added before, and the result can differ from the exact sum in the last bits. The tests compare the online tables with a batch build within $10^{-9}$.
