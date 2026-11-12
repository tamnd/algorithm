---
title: Liang-Barsky clipping returns the exact parameter interval of the inside part
proves: [correctness]
status: full
---

We use the pseudocode of the page and exact arithmetic. Let $d = Q - P = (d_x, d_y)$, and let $X(t) = P + t\,d$. Let $W = [x_{\min}, x_{\max}] \times [y_{\min}, y_{\max}]$ with $x_{\min} \le x_{\max}$ and $y_{\min} \le y_{\max}$. Let $T = \{t \in [0, 1] : X(t) \in W\}$. The answer is the set $X(T)$.

**Lemma 1 (the four pairs).** For each $t$, the point $X(t)$ is in $W$ if and only if $t\,a_k \le b_k$ for the four pairs $(a_k, b_k)$ of line L2.

*Proof.* $X(t)$ is in $W$ if and only if $x_{\min} \le x_P + t d_x \le x_{\max}$ and $y_{\min} \le y_P + t d_y \le y_{\max}$. The first inequality is $-t d_x \le x_P - x_{\min}$, which is $t\,a_1 \le b_1$ with $(a_1, b_1) = (-d_x, x_P - x_{\min})$. The other three are the same with $(d_x, x_{\max} - x_P)$, $(-d_y, y_P - y_{\min})$ and $(d_y, y_{\max} - y_P)$. $\square$

**Lemma 2 (one pair).** Let $S_k = \{t : t\,a_k \le b_k\}$. If $a_k = 0$, then $S_k$ is the whole line when $b_k \ge 0$ and empty when $b_k < 0$. If $a_k < 0$, then $S_k = [b_k / a_k, \infty)$. If $a_k > 0$, then $S_k = (-\infty, b_k / a_k]$.

*Proof.* For $a_k = 0$ the inequality is $0 \le b_k$, with no $t$ in it. For $a_k \ne 0$, divide by $a_k$; the division by a negative number turns the inequality around. $\square$

So $T = [0, 1] \cap S_1 \cap S_2 \cap S_3 \cap S_4$, by Lemma 1, and each $S_k$ is empty, the whole line, or a closed half-line. An intersection of closed intervals and closed half-lines is a closed interval or empty.

**Theorem.** LIANG-BARSKY$(P, Q, W)$ returns empty if $T$ is empty. Otherwise it returns $(t_0, t_1)$ with $T = [t_0, t_1]$, and line L9 returns the segment $X(T)$ from $X(t_0)$ to $X(t_1)$.

*Proof.* We use this invariant at the start of each pass of the loop of line L3, after $k$ pairs:

> **(L)** $[t_0, t_1] = [0, 1] \cap S_1 \cap \dots \cap S_k$, and $t_0 \le t_1$.

Line L1 makes (L) true for $k = 0$. Take the next pair. If $a_{k+1} = 0$ and $b_{k+1} < 0$, then $S_{k+1}$ is empty by Lemma 2, so $T$ is empty, and line L4 is right to return. If $a_{k+1} = 0$ and $b_{k+1} \ge 0$, then $S_{k+1}$ is the whole line, and nothing changes. If $a_{k+1} < 0$, the intersection with $[b_{k+1}/a_{k+1}, \infty)$ raises the lower end to $\max(t_0, b_{k+1}/a_{k+1})$, which is line L5. If $a_{k+1} > 0$, the intersection with $(-\infty, b_{k+1}/a_{k+1}]$ lowers the upper end to $\min(t_1, b_{k+1}/a_{k+1})$, which is line L6. Now $[t_0, t_1]$ is the intersection of the first $k + 1$ sets. If $t_0 > t_1$, this intersection is empty, so $T$, which is a subset of it, is empty too, and line L7 is right to return. Otherwise (L) holds for $k + 1$.

After the four pairs, (L) and Lemma 1 give $[t_0, t_1] = T$. Then $X$ maps $[t_0, t_1]$ onto the segment from $X(t_0)$ to $X(t_1)$, and this segment keeps the direction from $P$ to $Q$. When $t_0 = t_1$, the answer is the single point $X(t_0)$. $\blacksquare$

**Entering and leaving.** When $a_k < 0$, the value of $t\,a_k$ falls as $t$ grows, so the segment is outside side $k$ for small $t$ and inside it for large $t$: the parameter $b_k / a_k$ is where it enters. When $a_k > 0$, the parameter is where it leaves. So $t_0$ is the last entering parameter, and $t_1$ is the first leaving parameter, each clamped to $[0, 1]$.
