---
title: The Stromquist moving knife gives an envy-free division into three intervals
proves: [correctness]
status: full
---

**Setting.** The cake is $[0, 1]$. Agents 1, 2 and 3 have nonnegative, additive and nonatomic valuations $V_i$ with $V_i([0, 1]) = 1$. We also assume that every interval of positive length has positive value to every agent; this is the assumption under which we prove the result, and the implementation meets it by positive densities. Let $G_i(x) = V_i([0, x])$. Then $G_i$ is continuous, strictly increasing, $G_i(0) = 0$ and $G_i(1) = 1$, so it has a continuous inverse $G_i^{-1}$ on $[0, 1]$. We refer to the lines L1 to L9 of the page.

**Lemma 1 (the knives move continuously).** For $x \in [0, 1]$, agent $i$ has exactly one knife position $k_i(x) \in [x, 1]$ with $V_i([x, k_i(x)]) = V_i([k_i(x), 1])$, namely
$$k_i(x) = G_i^{-1}\left(\frac{1 + G_i(x)}{2}\right).$$
The maps $k_i$ and the median knife $y(x) = \mathrm{med}(k_1(x), k_2(x), k_3(x))$ are continuous, and $x \le y(x) \le 1$.

*Proof.* The condition says $G_i(k) - G_i(x) = 1 - G_i(k)$, that is $G_i(k) = (1 + G_i(x))/2$. Since $G_i$ is a strictly increasing bijection of $[0, 1]$, there is exactly one such $k$, and $G_i(x) \le (1 + G_i(x))/2 \le 1$ gives $x \le k \le 1$. The formula is a composition of continuous maps. The median of three numbers is $\max(\min(a, b), \min(a, c), \min(b, c))$, which is continuous in $(a, b, c)$. Each $k_i(x)$ lies in $[x, 1]$, so the median does too. $\square$

**Lemma 2 (the first shout).** Let $h_i(x) = V_i([0, x]) - \max(V_i([x, y(x)]), V_i([y(x), 1]))$. Line L5 stops at $x^* = \min\{x \in [0, 1] : h_i(x) \ge 0 \text{ for some } i\}$. This minimum exists, $x^* > 0$, $h_s(x^*) \ge 0$ for the shouter $s$, and $h_i(x^*) \le 0$ for every agent $i$.

*Proof.* Each $h_i$ is continuous by Lemma 1. At $x = 0$, $V_i([0, 0]) = 0$ and the two right pieces have total value 1, so the larger is at least $1/2$ and $h_i(0) \le -1/2 < 0$. At $x = 1$, $y(1) = 1$ and $h_i(1) = 1 > 0$. So the set $S = \{x : \max_i h_i(x) \ge 0\}$ is nonempty, and it is closed because $\max_i h_i$ is continuous. Its least element $x^*$ exists, and $x^* > 0$. The knife stops at the first $x$ where some agent's condition holds, which is $x^*$; line L6 picks one such agent $s$, so $h_s(x^*) \ge 0$. For every $i$ and every $x < x^*$, $h_i(x) < 0$, so $h_i(x^*) = \lim_{x \to x^*,\, x < x^*} h_i(x) \le 0$. $\square$

So $h_s(x^*) = 0$: the shouter shouts at the moment of equality.

**Lemma 3 (the knives of the others).** Let $a$ and $b$ be the two agents other than $s$, with $k_a(x^*) \le k_b(x^*)$ as in line L8. Then $k_a(x^*) \le y \le k_b(x^*)$, where $y = y(x^*)$.

*Proof.* The median $y$ is one of the three knives, and at most one knife is below it and at most one above it in the sorted order. If $y = k_s$, then $k_a$ and $k_b$ are the other two, one on each side. If $y = k_a$ (as a value), then $k_a \le y$, and $k_b \ge k_a = y$. If $y = k_b$, then $k_b \ge y$, and $k_a \le k_b = y$. $\square$

**Lemma 4 (each other agent gets its better right piece).** Agent $a$ values $[x^*, y]$ at least as much as $[y, 1]$, and agent $b$ values $[y, 1]$ at least as much as $[x^*, y]$.

*Proof.* Write $x = x^*$. Since $k_a \le y$, monotonicity gives $V_a([x, y]) \ge V_a([x, k_a]) = V_a([x, 1])/2$, so $V_a([y, 1]) = V_a([x, 1]) - V_a([x, y]) \le V_a([x, 1])/2 \le V_a([x, y])$. The case of $b$ is the mirror image, with $k_b \ge y$. $\square$

**Theorem 1 (envy-free with connected pieces).** The pieces $[0, x^*]$, $[x^*, y]$ and $[y, 1]$ of lines L7 to L9 form a partition of $[0, 1]$ into three intervals, and no agent envies another.

*Proof.* $0 < x^* \le y \le 1$ by Lemmas 1 and 2, so the three intervals cover $[0, 1]$ and meet only at end points. The shouter $s$ has $h_s(x^*) \ge 0$, so $V_s([0, x^*])$ is at least the value of each right piece. Agent $a$ gets $[x^*, y]$, which by Lemma 4 is its better right piece, so $V_a([x^*, y]) = \max(V_a([x^*, y]), V_a([y, 1])) \ge V_a([0, x^*])$, where the last step is $h_a(x^*) \le 0$ from Lemma 2. The same argument holds for $b$ with $[y, 1]$. $\square$

**Lemma 5 (exact simulation for the implementation).** Let every $V_i$ have a positive density that is constant on each of the $k$ segments $[j/k, (j+1)/k]$. Let $B$ be the set of points $j/k$, together with each $x$ where some knife $k_i(x)$ equals some $j/k$, together with each $x$ where two knives cross between two such points. On each interval $[p, q]$ between consecutive points of $B$, the knives, the median $y$, and the two gaps $g_1 = V_i([0, x]) - V_i([x, y])$ and $g_2 = V_i([0, x]) - V_i([y, 1])$ are affine in $x$.

*Proof.* On $[p, q]$, $x$ stays in one segment, so $G_i(x)$ is affine. The knife $k_i(x)$ stays in one segment too, because it does not cross a point $j/k$ inside $(p, q)$; on that segment $G_i^{-1}$ is affine, so $k_i$ is affine. Two knives do not cross inside $(p, q)$, so the order of the knives is the same on all of $(p, q)$ and $y$ is one fixed knife $k_l$, hence affine. All agents use the same segments, so $y = k_l$ also stays in one segment and $G_i(y)$ is affine. Then $g_1 = 2 G_i(x) - G_i(y)$ and $g_2 = G_i(x) + G_i(y) - 1$ are affine. $\square$

An affine function is determined by its values at $p$ and $q$, and the set where it is nonnegative is an interval whose end points the code computes exactly in Fraction. The condition of line L5 is $g_1 \ge 0$ and $g_2 \ge 0$, so the code finds the least such point in the first interval $[p, q]$ where it exists, and that point is $x^*$. The crossing points of two knives between consecutive points of the first kind are found by the same linear interpolation, because both knives are affine there.
