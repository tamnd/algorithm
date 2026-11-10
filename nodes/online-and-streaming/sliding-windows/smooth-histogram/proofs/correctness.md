---
title: The smooth histogram gives a (1 - alpha) approximation with O((1/beta) log F) instances
proves: [correctness]
status: full
---

The notation is that of the page. The function $f$ is $(\alpha, \beta)$-smooth, the instances are exact, $a_1, a_2, \ldots$ is the stream, $t$ is the current time and $f(x, t) = f(a_x, \ldots, a_t)$ for $x \le t$. The list after the update at time $t$ is $x_1 < \cdots < x_s$. Condition 2 of smoothness gives, for $x \le y \le t$,
$$f(x, t) \ge f(y, t), \tag{M}$$
since $a_y \ldots a_t$ is a suffix of $a_x \ldots a_t$.

**Lemma 1 (the list).** After each update, $x_s = t$, and if $t > W$ then $x_1 \le t - W < x_2$. If $t \le W$ then $x_1 = 1$.

*Proof.* Line L2 adds $t$, line L7 never deletes the last index, and line L8 deletes only indices before an expired one, while $t$ is not expired. So $x_s = t$. The start time 1 is added at time 1 as the first index. Line L7 never deletes the first index, and line L8 deletes indices only before an index $x_i \le t - W$. So 1 stays $x_1$ while $t \le W$. Once $t > W$: at time $W + 1$ the index 1 is expired, so an expired index exists; after line L8 the first index is the largest expired one, and it stays expired at later times. So $x_1 \le t - W$. And $x_2$ exists, since $x_s = t > t - W$ means $s \ge 2$, and it is not expired, since $x_1$ is the largest expired index. $\square$

**Lemma 2 (close neighbors).** After the update at time $t$, for each $i < s$, either $x_{i+1} = x_i + 1$, or
$$(1 - \alpha) f(x_i, t) \le f(x_{i+1}, t).$$

*Proof.* Look at the moment when $x_i$ and $x_{i+1}$ became neighbors in the list. Only lines L2 and L7 make new pairs of neighbors: line L8 deletes a prefix and leaves the other pairs as they are.

- Line L2 at time $t'$ appends $t'$ after the last index of the list. That index is $t' - 1$, because it was appended at time $t' - 1$, and lines L7 and L8 at time $t' - 1$ did not delete the last index (Lemma 1). So $x_{i+1} = x_i + 1$.
- Line L7 at time $t'$, for an index $y = x_i$, deletes the indices between $y$ and $z = x_j$. If nothing is deleted, no new pair is made. Otherwise $j$ is not the default $i + 1$, so $f(z, t') \ge (1 - \beta) f(y, t')$, with the values after line L3, which has fed $a_{t'}$.

In the second case, let $A = a_y \ldots a_{t'}$ and $B = a_z \ldots a_{t'}$. Then $B$ is a suffix of $A$ and $(1 - \beta) f(A) \le f(B)$. If $t = t'$, then $(1 - \alpha) f(A) \le (1 - \beta) f(A) \le f(B)$, since $\beta \le \alpha$. If $t > t'$, let $C = a_{t'+1} \ldots a_t$, which is adjacent to $A$. Condition 4 of smoothness gives $(1 - \alpha) f(A \cup C) \le f(B \cup C)$, that is $(1 - \alpha) f(y, t) \le f(z, t)$. From time $t'$ to time $t$ no index comes between $y$ and $z$, because line L2 adds indices only at the end. $\square$

**Theorem 1 (accuracy).** For $1 \le w \le W$, SH-QUERY$(w)$ returns $\hat f$ with $(1 - \alpha) f_w \le \hat f \le f_w$, where $f_w = f(\max(1, t - w + 1), t)$.

*Proof.* If $x_1 > t - w$, then $t - w < x_1$. By Lemma 1, $t \le W$ would give $x_1 = 1$, and $t > W$ would give $x_1 \le t - W \le t - w$, which is false. So $x_1 = 1$ and $t - w < 1$; the window is the whole stream, and line L9 returns $f(1, t) = f_w$ exactly.

Otherwise let $i$ be the largest index with $x_i \le t - w$; then $x_{i+1}$ exists and $x_{i+1} > t - w$, because $x_s = t$. With $u = t - w + 1$, we have $x_i < u \le x_{i+1}$, and (M) gives
$$f(x_{i+1}, t) \le f(u, t) = f_w \le f(x_i, t).$$
If $x_{i+1} = x_i + 1$, then $x_{i+1} = u$ and line L11 returns $f_w$. Otherwise Lemma 2 gives $f(x_{i+1}, t) \ge (1 - \alpha) f(x_i, t) \ge (1 - \alpha) f_w$. $\square$

**Lemma 3 (decay).** After the update at time $t$, for each $i \le s - 2$, $f(x_{i+2}, t) < (1 - \beta) f(x_i, t)$.

*Proof.* Consider the pass of line L6 for $y = x_i$ at time $t$. After line L7, the next index is $z = x_j$, the largest index after $y$ with $f(z, t) \ge (1 - \beta) f(y, t)$, or the index right after $y$ if there is none. In both cases each index after $z$ in the list fails the test: $f(\cdot, t) < (1 - \beta) f(y, t)$. Later passes of the loop, for indices after $y$, only delete indices, and line L8 deletes only a prefix. So the index after the neighbor of $y$ at the end of the update is one of the indices after $z$, and the claim holds. $\square$

**Theorem 2 (size).** Assume that $f$ takes values in $\{0, 1, 2, \ldots\}$ and that $f$ of each stream of at most $W$ items is at most $F$. Then after each update
$$s \le 2 \left\lceil \frac{\ln(F + 1)}{\beta} \right\rceil + 3.$$

*Proof.* Let $p = 2$ if $t > W$ and $p = 1$ if $t \le W$. The items $a_{x_p}, \ldots, a_t$ are at most $W$ items: for $t \le W$ because $t \le W$, and for $t > W$ because $x_2 > t - W$ (Lemma 1). So $f(x_p, t) \le F$. By Lemma 3 and induction, for $m \ge 1$ with $p + 2m \le s$,
$$f(x_{p + 2m}, t) < (1 - \beta)^m F \le e^{-\beta m} F.$$
Let $M = \lceil \ln(F + 1)/\beta \rceil$. If $F = 0$ then $f(x_p, t) = 0$; otherwise $M \ge 1$ and $e^{-\beta M} F \le F/(F + 1) < 1$, so $f(x_{p + 2M}, t) = 0$ if that index exists. In both cases some index at position at most $p + 2M$ has the value 0, if the list is that long. If $f(x_q, t) = 0$, then each later index $x_j$ has $f(x_j, t) \ge 0 = (1 - \beta) f(x_q, t)$, so in the pass for $x_q$ line L6 picks $j = s$, and $x_q$ has only one index after it. Hence $s \le p + 2M + 1 \le 2M + 3$. $\square$

**Time.** Line L3 makes $s$ instance updates. In lines L4 to L7, by (M) the values along the list do not increase, so the largest $j$ of line L6 is found by moving a pointer forward from $i + 1$, and the pointer for the next pass starts where the last one stopped. So the loop reads $O(s)$ values. Line L8 takes $O(s)$ steps. By Theorem 2 the update time is $O(\frac{h}{\beta} \log F)$, where $h$ bounds the time of one instance update and one value read. $\square$
