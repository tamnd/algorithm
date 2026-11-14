---
title: The Kolmogorov-Smirnov statistic, its exact null law, and why the p-values are valid
proves: [correctness]
status: full
---

We use the pseudocode of the page. $F_0$ is continuous, $u_i = F_0(x_{(i)})$, and $c = nd$ with $k = \lfloor c \rfloor + 1$ and $h = k - c \in (0, 1]$, as in line L4.

**Claim 1 (the statistic).** Lines L1 and L2 return $D^+ = \sup_t (F_n(t) - F_0(t))$ and $D^- = \sup_t (F_0(t) - F_n(t))$.

*Proof.* On $[x_{(i)}, x_{(i+1)})$ the function $F_n$ equals $i/n$ (or more, at tied points, which only raises the value at the last index of the tie) and $F_0$ is nondecreasing, so $\sup (F_n - F_0)$ on this interval is $i/n - u_i$. Before $x_{(1)}$, $F_n - F_0 \le 0 \le 1 - u_n$. So $D^+ = \max_i (i/n - u_i)$. On $[x_{(i-1)}, x_{(i)})$, $F_n = (i-1)/n$ and $\sup F_0 = F_0(x_{(i)}-) = u_i$ by continuity, which gives $u_i - (i-1)/n$. After $x_{(n)}$, $F_0 - F_n \le 0$. $\square$

**Claim 2 (distribution-free).** Under $H_0$, $(u_1, \ldots, u_n)$ has the law of the order statistics $U_{(1)} < \cdots < U_{(n)}$ of $n$ independent uniforms on $(0, 1)$. So the laws of $D$, $D^+$ and $D^-$ depend only on $n$, and $D^+$ and $D^-$ have the same law.

*Proof.* For continuous $F_0$, $P(F_0(X) \le s) = s$ for $s \in [0, 1]$, so $F_0(X_i)$ is uniform, and $F_0$ is nondecreasing, so it maps the sorted data to the sorted uniforms. By Claim 1 the statistics are functions of these values. The map $U_i \mapsto 1 - U_i$ keeps the joint law and turns $\max_i (i/n - U_{(i)})$ into $\max_j (U'_{(j)} - (j-1)/n)$ with $j = n + 1 - i$, so it exchanges $D^+$ and $D^-$. $\square$

**Claim 3 (the band).** $D < d$ if and only if $i/n - d < U_{(i)} < (i-1)/n + d$ for every $i$.

*Proof.* This is Claim 1: $D^+ < d$ means $i/n - U_{(i)} < d$ for all $i$, and $D^- < d$ means $U_{(i)} - (i-1)/n < d$ for all $i$. $\square$

**Claim 4 (the matrix formula).** $P(D < d) = \frac{n!}{n^n} (H^n)_{kk}$ with $H$ from lines L5 and L6.

*Proof.* Let $N$ be a Poisson process of rate 1 on $[0, n]$ with jump times $S_1 < S_2 < \cdots$. Given $N(n) = n$, the points $S_i / n$ are distributed as $U_{(1)}, \ldots, U_{(n)}$. By Claim 3, $D < d$ becomes the event $E$ that $i - c < S_i < i - 1 + c$ for $i = 1, \ldots, n$. Let $V(s) = N(s) - s$. Between jumps $V$ falls at slope 1, and at a jump it rises by 1. The condition $S_i > i - c$ says that $V$ stays below $c$ just after each jump, and $S_i < i - 1 + c$ says that $V$ stays above $-c$ just before each jump. So $E$ is the event that $V(s) < c$ and $V(s-) > -c$ for all $s \in [0, n]$.

At integer times $V$ is an integer. Take first $h < 1$; then $k - 1 < c < k$, and $\lvert V \rvert < c$ allows the $m = 2k - 1$ values $k - 1, \ldots, -(k-1)$. Give the value $v$ the index $i = k - v$, so $i = 1$ is the top value $k - 1$ and $i = m$ is the bottom value $-(k-1)$. A step from time $s$ to $s + 1$ from index $i$ to index $j$ needs exactly $i - j + 1$ jumps, which has probability $e^{-1}/(i - j + 1)!$, or 0 if $i - j + 1 < 0$. This is $e^{-1}$ times the entry of line L5.

Now remove the steps that leave the band between integer times. Suppose that $V$ reaches $c$ at a time $\tau$ inside the step. After $\tau$ it falls by at most $1 - \tau$, so the end value is at least $c - 1 + \tau = k - h - 1 + \tau$. For an end value of at most $k - 2$ this needs $\tau \le h - 1 \le 0$, which is not possible. So upper exits happen only in steps that end at index 1, and then only with $\tau \le h$. A step from index $i$ to index 1 has $i$ jumps. With $J$ jumps by time $\tau$, $V$ reaches $c$ when $J - \tau \ge i - h$, and $J \le i$, so all $i$ jumps must be in $[0, h]$. That has probability $e^{-h} h^i / i! \cdot e^{-(1-h)} = e^{-1} h^i / i!$. In the same way, $V$ reaches $-c$ from the start value $v$ before the first jump at time $\tau$ when $v - \tau \le -c$, that is $\tau \ge v + k - h$. This is possible inside a step only for $v = -(k-1)$, the index $m$, and then exactly when no jump falls in $[0, 1 - h]$. After a jump, $V$ is at least $v + 1 - \tau > -c$. A step from index $m$ to index $j$ has $m - j + 1$ jumps, and all of them in $(1 - h, 1]$ has probability $e^{-1} h^{m-j+1}/(m-j+1)!$. A step from index $m$ to index 1 can do both: all $m$ jumps in $(1 - h, h]$, with probability $e^{-1} \max(0, 2h - 1)^m / m!$. By inclusion and exclusion, $e^{-1} H_{ij}$ after line L6 is the probability of the step from $i$ to $j$ with $V$ in the band for the whole step.

The process has independent increments, so given the values at integer times the steps are independent. The path starts at $V(0) = 0$, index $k$, and the event $N(n) = n$ means $V(n) = 0$, index $k$. So $P(E, N(n) = n) = e^{-n} (H^n)_{kk}$. Divide by $P(N(n) = n) = e^{-n} n^n / n!$. $\square$

The argument above takes $h < 1$, so that all $m$ values are inside the band. For $h = 1$, $c = k - 1$ and the values $\pm(k-1)$, the indices 1 and $m$, are outside it. For values inside, the same computation shows that no exit happens strictly inside a step: an upper exit needs $\tau \le 0$, and a lower exit from $v \ge -(k-2)$ needs $\tau \ge 1$. Line L6 with $h = 1$ makes column 1 and row $m$ zero, so no path of positive weight enters index 1, and a path that enters index $m$ cannot leave it. The path must end at index $k$, and $1 < k < m$ because $k \ge 2$ when $d > 0$, so these paths get weight 0. The formula therefore needs no special case.

**Claim 5 (the one-sided sum).** For $0 < d \le 1$, $P(D^- \ge d) = d \sum_{j=0}^{\lfloor n(1-d) \rfloor} \binom{n}{j} (1 - d - j/n)^{n-j} (d + j/n)^{j-1}$, and $D^+$ has the same law.

*Proof.* Let $a_j = d + j/n$ and $g(j) = N(a_j) - j$, where $N(a)$ is now the number of the $n$ uniforms below $a$. $D^- \ge d$ means $U_{(j+1)} \ge a_j$ for some $j \le n - 1$, that is $g(j) \le 0$ for some $j$ with $a_j \le 1$. $g(0) \ge 0$, and $g$ falls by at most 1 from $j$ to $j + 1$, so the first $j$ with $g(j) \le 0$ has $g(j) = 0$. The events "the first such $j$" are disjoint. For a fixed $j$, the event is $N(a_j) = j$, of probability $\binom{n}{j} a_j^j (1 - a_j)^{n-j}$, together with $g(i) > 0$ for $i < j$. Given $N(a_j) = j$, the $j$ points below $a_j$ are independent and uniform on $(0, a_j)$. Measure from the right end: with $M(s)$ the number of these points in $[a_j - s, a_j)$, the condition $g(i) > 0$ for all $i < j$ is $M(l/n) < l$ for $l = 1, \ldots, j$, and this is the same as $M(s) < ns$ for all $s \in (0, a_j]$, because $M$ is a nondecreasing step function and $ns > j$ for $s > j/n$. By the continuous form of the [ballot theorem](/ballot-theorem/) (Takacs), this has probability $1 - j/(n a_j) = d / a_j$. Multiply and add over $j$. Claim 2 gives the same law for $D^+$. $\square$

**Claim 6 (the doubled tail).** $P(D \ge d) \le 2 P(D^+ \ge d)$ for every $d$, with equality for $d \ge 1/2$.

*Proof.* $\{D \ge d\} = \{D^+ \ge d\} \cup \{D^- \ge d\}$, and the two events have the same probability by Claim 2. Suppose both happen, with $i/n - U_{(i)} \ge d$ and $U_{(j)} - (j-1)/n \ge d$. If $j \le i$, then $U_{(j)} \le U_{(i)}$ gives $2d \le (i - j + 1)/n \le 1$. If $j > i$, then $U_{(i)} \ge 0$ and $U_{(j)} \le 1$ give $i/n \ge d$ and $1 - (j - 1)/n \ge d$, so $2d \le 1 - (j - 1 - i)/n \le 1$. So for $d > 1/2$ the events are disjoint. At $d = 1/2$ both cases need equalities between continuous random variables or with 0 or 1, which have probability 0. $\square$

**Claim 7 (validity).** Each p-value returned is $P(T \ge t_{obs})$ for the statistic $T$, or an upper bound of it, so $P_{H_0}(p \le \alpha) \le \alpha$.

*Proof.* Line L8 returns $1 - P(D < d) = P(D \ge d)$ by Claim 4, and line L3 returns $2 P(D^+ \ge d)$ by Claim 5, which is $P(D \ge d)$ or an upper bound by Claim 6. For any statistic $T$ with tail function $G(t) = P(T \ge t)$, $P(G(T) \le \alpha) \le \alpha$: let $t^* = \inf\{t : G(t) \le \alpha\}$; the event $G(T) \le \alpha$ is $T \ge t^*$ or $T > t^*$, and both have probability at most $\alpha$ by the right-continuity of $t \mapsto P(T > t)$ and the monotonicity of $G$. A larger p-value only shrinks the rejection event. $\square$

**Discrete models.** If $F_0$ has jumps, write $X_i = F_0^{-1}(U_i)$ with the generalized inverse. Then $F_n(t) - F_0(t) = G_n(F_0(t)) - F_0(t)$, where $G_n$ is the empirical distribution function of the $U_i$, so $D$ is a sup over a subset of the points used for the uniforms, and it is at most the uniform statistic. The p-values computed as for a continuous model are therefore conservative.

**Two samples.** Without ties, under $H_0$ the pooled sample is exchangeable, so each of the $\binom{m+n}{m}$ assignments of the labels to the sorted pooled values is equally likely. Each assignment is a lattice path from $(0, 0)$ to $(m, n)$ with a step in the first coordinate for each value of the first sample. At the point $(i, j)$, $F_m - G_n = (in - jm)/(mn)$, and without ties these points are all the points where the two functions change. So $D_{m,n} < t/(mn)$ exactly when the path keeps $\lvert in - jm \rvert < t$, and the dynamic program counts these paths by adding the counts from the left and from below. The p-value is $P(D_{m,n} \ge t/(mn))$. With ties, break them at random: the statistic with ties is a max over a subset of the points of the path after the tie break, so it is at most the statistic of that path, and the p-value is conservative.

**The limit law.** The asymptotic p-values use Kolmogorov's limit $P(\sqrt{n} D_n > \lambda) \to 2 \sum_{k \ge 1} (-1)^{k-1} e^{-2k^2\lambda^2}$, which we cite and do not prove here. For $\lambda < 1$ the code uses the equal form $1 - \frac{\sqrt{2\pi}}{\lambda} \sum_{k \ge 1} e^{-(2k-1)^2 \pi^2 / (8\lambda^2)}$, from the Jacobi theta-function identity, because the alternating series converges slowly there.
