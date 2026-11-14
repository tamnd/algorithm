---
title: The best intercept is the centre of the narrowest window, and the best slope is a pairwise slope, so LMS-LINE is exact
proves: [correctness]
status: full
---

**Setting.** The data are $(x_1, y_1), \ldots, (x_n, y_n)$ with $n \ge 2$, and $h = \lfloor n/2 \rfloor + 1$. For a line $y = a + s x$, the residuals are $r_i = y_i - a - s x_i$, and the objective $Q(s, a)$ is the $h$-th smallest of $r_1^2, \ldots, r_n^2$. LMS-LINE must return $(s, a)$ that minimize $Q$, and the value $Q^* = \min Q$. Write $z_i(s) = y_i - s x_i$, so $r_i = z_i(s) - a$.

## Part 1. A fixed slope

**Lemma 1.** Fix $s$, and let $z_{(1)} \le \cdots \le z_{(n)}$ be the sorted values $z_i(s)$. Let $w(s) = \min_{1 \le i \le n-h+1} (z_{(i+h-1)} - z_{(i)})$, attained at $i^*$. Then $\min_a Q(s, a) = (w(s)/2)^2$, attained at $a = (z_{(i^*)} + z_{(i^*+h-1)})/2$.

*Proof.* For $\rho \ge 0$, $Q(s, a) \le \rho^2$ holds exactly when at least $h$ values $z_i$ lie in the interval $[a - \rho, a + \rho]$. An interval that holds $h$ of the sorted values holds $h$ consecutive ones, $z_{(i)}, \ldots, z_{(i+h-1)}$, so its length $2\rho$ is at least $z_{(i+h-1)} - z_{(i)} \ge w(s)$. So $Q(s, a) \ge (w(s)/2)^2$ for all $a$. The interval of length $w(s)$ centred at the given $a$ holds the $h$ values $z_{(i^*)}, \ldots, z_{(i^*+h-1)}$, so equality holds there. $\square$

Lines L7 to L9 compute exactly this, in $O(n \log n)$ time for the sort and $O(n)$ for the scan.

## Part 2. The slope

For a set $S$ of $h$ indices, let $f_S(s) = \max_{i \in S} z_i(s) - \min_{i \in S} z_i(s)$, the width of $S$ at slope $s$.

**Lemma 2.** $w(s) = \min_{|S| = h} f_S(s)$.

*Proof.* A window of $h$ consecutive sorted values is a set $S$ with width equal to the window length, so $w(s) \ge \min_S f_S(s)$. Any set $S$ of $h$ values spans at least $h$ consecutive sorted values, so its width is at least the length of some window, and $f_S(s) \ge w(s)$. $\square$

**Lemma 3.** If the points of $S$ do not all have the same $x$, then $f_S$ attains its minimum at a slope $s_{ij} = (y_j - y_i)/(x_j - x_i)$ of two points $i, j \in S$. If they all have the same $x$, $f_S$ is constant.

*Proof.* Each $z_i(s)$ is linear in $s$. The maximum of finitely many linear functions is convex and piecewise linear, and it changes from one function to another only where two of them are equal, that is at some $s_{ij}$. The minimum is concave and piecewise linear with breakpoints of the same kind. So $f_S$ is convex and piecewise linear, and all its breakpoints are pairwise slopes of points of $S$. If $x_i \ne x_j$ for some $i, j \in S$, then $f_S(s) \ge |z_i(s) - z_j(s)| = |x_j - x_i| \cdot |s - s_{ij}| \to \infty$ as $s \to \pm\infty$, so $f_S$ is not a single linear piece and has a breakpoint. A convex piecewise linear function that tends to $\infty$ at both ends has its minimum at a breakpoint. If all $x_i$ in $S$ are equal, every $z_i(s) - z_j(s) = y_i - y_j$ is constant. $\square$

**Theorem 4.** $Q^* = \min_{s \in T} (w(s)/2)^2$, where $T$ is the set of pairwise slopes of line L2 (or $T = \{0\}$ when all $x$ are equal). So LMS-LINE returns an optimal line and the value $Q^*$.

*Proof.* By Lemmas 1 and 2, $Q^* = \min_s \min_S (f_S(s)/2)^2 = \min_S \min_s (f_S(s)/2)^2$. Take $S$ that attains the outer minimum. If its points have two different $x$ values, Lemma 3 gives a minimizing slope in $T$. If not, $f_S$ is constant, and any slope, in particular one in $T$, gives the same value. In both cases some $s \in T$ has $(w(s)/2)^2 \le (f_S(s)/2)^2 = Q^*$, and $(w(s)/2)^2 \ge Q^*$ for every $s$. Lines L3 to L5 take the best $s \in T$, and line L4 takes its best intercept by Lemma 1. $\square$

## Part 3. Cost

$|T| \le \binom n2$, and each slope costs $O(n \log n)$, so LMS-LINE takes $O(n^3 \log n)$ time. Storing $T$ takes $O(n^2)$ space; looping over the pairs without storing them takes $O(n)$ extra space.

## What is cited, not proved

The breakdown point $\lfloor n/2 \rfloor / n$ for simple regression in general position with this $h$ (Rousseeuw 1984; Rousseeuw and Leroy 1987, Chapter 3) and the convergence rate $n^{-1/3}$ (stated by Rousseeuw 1984 and proved in the framework of Kim and Pollard 1990) are cited on the page. They are not proved here.
