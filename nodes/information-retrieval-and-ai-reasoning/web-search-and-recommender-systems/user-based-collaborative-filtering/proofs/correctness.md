---
title: User-based collaborative filtering returns the Pearson-weighted prediction, and its weights and predictions are bounded
proves: [correctness]
status: full
---

The notation is that of the page: $I_v$ is the set of items that user $v$ rated, $\mu_v$ is the mean of the ratings of $v$, $I_{uv} = I_u \cap I_v$, and $C$ is the set of users left after line L5.

**Lemma 1 (range and symmetry).** For all users $u, v$, $-1 \le w(u, v) \le 1$ and $w(u, v) = w(v, u)$.

*Proof.* If $I_{uv}$ is empty or one of the sums $\sum x_t^2$, $\sum y_t^2$ is 0, line L11 returns 0 for both orders of the pair. Else let $x = (r_{ut} - \mu_u)_{t \in I_{uv}}$ and $y = (r_{vt} - \mu_v)_{t \in I_{uv}}$, two nonzero vectors. Line L12 returns $\langle x, y \rangle / (\lVert x \rVert \, \lVert y \rVert)$. By the Cauchy-Schwarz inequality $|\langle x, y \rangle| \le \lVert x \rVert \, \lVert y \rVert$, so the value is in $[-1, 1]$. Swapping $u$ and $v$ swaps $x$ and $y$, and the inner product and the product of the norms do not change. $\square$

**Lemma 2 (invariance).** Let $a > 0$ and $c$ be real numbers, and replace every rating $r_{vt}$ of one user $v$ by $a r_{vt} + c$. Then $w(u, v)$ does not change for any $u$.

*Proof.* The new mean of $v$ is $a \mu_v + c$, so each centered value $r_{vt} - \mu_v$ becomes $a (r_{vt} - \mu_v)$, and the vector $y$ of Lemma 1 becomes $a y$. The set $I_{uv}$ does not change. If $y = 0$ then $a y = 0$ and line L11 returns 0 before and after. Else $\langle x, a y \rangle / (\lVert x \rVert \, \lVert a y \rVert) = a \langle x, y \rangle / (a \lVert x \rVert \, \lVert y \rVert)$, because $a > 0$. The case where $v$ is the first argument follows by Lemma 1. $\square$

**Theorem 1 (correctness).** PREDICT$(u, i)$ returns the global mean if $u$ has no rating, $\mu_u$ if $\sum_{v \in C} |w(u, v)| = 0$, and

$$\hat r_{ui} = \mu_u + \frac{\sum_{v \in C} w(u, v)\,(r_{vi} - \mu_v)}{\sum_{v \in C} |w(u, v)|}$$

otherwise, where $C = U_i \setminus \{u\}$ if no $k$ is given, and $C$ is the set of the $k$ users of $U_i \setminus \{u\}$ that come first in the order of decreasing weight, ties broken by the smaller id, if $k$ is given.

*Proof.* Line L1 handles a user with no rating. Line L2 sets $C = U_i \setminus \{u\}$, and line L3 stores $w_v = w(u, v)$ for each $v \in C$, by the definition of WEIGHT in lines L9 to L12. Lines L4 and L5 replace $C$ by the first $k$ users in the stated order when $k$ is given, and leave it unchanged otherwise. Line L6 computes $D = \sum_{v \in C} |w_v|$. If $D = 0$, line L7 returns $\mu_u$. Else line L8 returns the stated expression. Each $v \in C$ is in $U_i$, so $r_{vi}$ is known, and each $v$ rated at least $i$, so $\mu_v$ is defined. $\square$

**Theorem 2 (range of the prediction).** If $D > 0$ then

$$|\hat r_{ui} - \mu_u| \le \max_{v \in C} |r_{vi} - \mu_v|.$$

*Proof.* Let $d_v = r_{vi} - \mu_v$ and $\alpha_v = |w_v| / D$. Then $\alpha_v \ge 0$ and $\sum_{v \in C} \alpha_v = 1$. Write $w_v = |w_v| \sigma_v$ with $\sigma_v \in \{-1, 1\}$ (any choice when $w_v = 0$). Then

$$\hat r_{ui} - \mu_u = \sum_{v \in C} \alpha_v \, (\sigma_v d_v),$$

a convex combination of the numbers $\sigma_v d_v$, each in $[-|d_v|, |d_v|]$. A convex combination lies between the smallest and the largest of its terms. $\square$

The bound cannot be improved to the rating scale. In the toy matrix of the page, $\mu_{u_4} = 2$ and the prediction for $(u_4, i_1)$ is $2 - 3.288 / 2.868 \approx 0.854$, below the smallest rating 1.

**Corollary 3 (shift of another user).** If every rating of one user $v \ne u$ is shifted by a constant $c$, then $\hat r_{ui}$ does not change for any item $i$. If every rating of $u$ is shifted by $c$, then each $\hat r_{ui}$ increases by $c$.

*Proof.* By Lemma 2 with $a = 1$, no weight changes, so the set $C$ chosen in line L5 is the same. A shift of $v$ changes $r_{vi}$ and $\mu_v$ by the same $c$, so $d_v$ does not change, and $\mu_u$ does not change. A shift of $u$ changes $\mu_u$ by $c$ and no $d_v$ with $v \ne u$; the global mean of line L1 is not used, since $u$ has ratings. $\square$
