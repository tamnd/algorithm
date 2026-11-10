---
title: The Boyer-Moore vote returns the majority, and only the majority
proves: [correctness, termination]
status: full
---

Let $\sigma = a_1, \ldots, a_m$, and let $f_x$ be the number of indices $t$ with $a_t = x$. Write $c_t$ and $k_t$ for the values of $candidate$ and $count$ after the loop of line L2 has read $a_1, \ldots, a_t$, with $k_0 = 0$.

**Invariant (P).** For each $t$ with $0 \le t \le m$, the multiset $\{a_1, \ldots, a_t\}$ splits into two parts:

1. a part $U_t$ of exactly $k_t$ items, each equal to $c_t$ (empty when $k_t = 0$), and
2. a part $D_t$ of $(t - k_t)/2$ pairs, where the two items of each pair are different.

In particular $k_t \ge 0$ and $t - k_t$ is even.

*Initialization.* For $t = 0$ both parts are empty, and $k_0 = 0$.

*Maintenance.* Assume (P) for $t - 1$ and let $x = a_t$. There are three cases, one for each branch.

- Line L4 runs, so $k_{t-1} = 0$. Then $U_{t-1}$ is empty. Set $U_t = \{x\}$ and $D_t = D_{t-1}$. Now $c_t = x$, $k_t = 1$, and $D_t$ has $(t - 1)/2 = (t - k_t)/2$ pairs.
- Line L6 runs, so $k_{t-1} > 0$ and $x = c_{t-1}$. Set $U_t = U_{t-1} \cup \{x\}$ and $D_t = D_{t-1}$. All items of $U_t$ equal $c_t = c_{t-1}$, and $|U_t| = k_{t-1} + 1 = k_t$. The number of pairs is $(t - 1 - k_{t-1})/2 = (t - k_t)/2$.
- Line L8 runs, so $k_{t-1} > 0$ and $x \ne c_{t-1}$. Take one item $y$ of $U_{t-1}$, so $y = c_{t-1} \ne x$. Set $U_t = U_{t-1} \setminus \{y\}$ and add the pair $\{y, x\}$ to $D_{t-1}$ to get $D_t$. The new pair has two different items. Now $|U_t| = k_{t-1} - 1 = k_t$, the candidate does not change, and the number of pairs is $(t - 1 - k_{t-1})/2 + 1 = (t - k_t)/2$.

In each case (P) holds for $t$. The loop reads each item once, so it ends after $m$ steps, and line L10 is a second loop of $m$ steps. So the algorithm terminates.

**Lemma 1.** If $x$ is a majority of $\sigma$, that is $f_x > m/2$, then $c_m = x$ and $k_m \ge 1$.

*Proof.* Apply (P) with $t = m$. Each pair of $D_m$ has two different items, so it holds at most one copy of $x$. So $D_m$ holds at most $(m - k_m)/2$ copies of $x$, and $U_m$ holds at least $f_x - (m - k_m)/2$ copies. Since $f_x > m/2$,
$$ f_x - \frac{m - k_m}{2} > \frac{m}{2} - \frac{m - k_m}{2} = \frac{k_m}{2} \ge 0 . $$
So $U_m$ holds at least one copy of $x$. Then $U_m$ is not empty, so $k_m \ge 1$, and each item of $U_m$ equals $c_m$, so $c_m = x$. $\square$

**Lemma 2 (the count bound).** For the final candidate, $k_m \ge 2 f_{c_m} - m$. For each item $x \ne c_m$, $f_x \le (m - k_m)/2$.

*Proof.* All copies of $x \ne c_m$ are in $D_m$, at most one in each pair. For $c_m$, at most one copy is in each pair that also holds an item different from $c_m$, and each pair does; so $f_{c_m} - k_m \le (m - k_m)/2$, which gives $k_m \ge 2 f_{c_m} - m$. $\square$

**Theorem.** MAJORITY$(\sigma)$ returns $x$ if $x$ is a majority of $\sigma$, and returns "none" if $\sigma$ has no majority.

*Proof.* Line L10 sets $occ = f_{c_m}$. If $x$ is a majority, Lemma 1 gives $c_m = x$, so $occ = f_x > m/2$, and line L11 returns $x$. If there is no majority, then $2 f_y \le m$ for every item $y$, in particular for $y = c_m$, so line L11 returns "none". For the empty stream, $c_0$ is "none" and line L11 returns "none". $\blacksquare$

**Merging.** Let two streams $\sigma_1$ and $\sigma_2$ end in the states $(c_1, k_1)$ and $(c_2, k_2)$, with the splits $U_1, D_1$ and $U_2, D_2$ of (P). If $c_1 = c_2$ or one count is 0, the parts $U_1 \cup U_2$ and $D_1 \cup D_2$ satisfy (P) for the concatenation with the state $(c, k_1 + k_2)$. If $c_1 \ne c_2$ and both counts are positive, pair $\min(k_1, k_2)$ copies of $c_1$ with as many copies of $c_2$. These pairs have different items, and the rest of $U_1 \cup U_2$ is $|k_1 - k_2|$ copies of the candidate with the larger count. So (P) holds for the concatenation, and Lemma 1 applies to the merged state.
