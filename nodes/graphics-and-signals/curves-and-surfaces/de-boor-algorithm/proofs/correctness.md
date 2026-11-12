---
title: De Boor's algorithm returns the point C(u) of the B-spline curve
proves: [correctness]
status: full
---

We use the pseudocode and the notation of the page. The B-splines $N_{i,q}$ come from the [Cox-de Boor recursion](/cox-de-boor-recursion/), with half-open spans and the rule that a term whose weight has a zero denominator is $0$. We write $\omega_{i,q}(u) = (u - t_i)/(t_{i+q} - t_i)$ when $t_{i+q} > t_i$.

**Claim.** Let $p \ge 0$, $n \ge p$, $t_0 \le \cdots \le t_{n+p+1}$ with $t_p < t_{n+1}$, and $t_p \le u \le t_{n+1}$. Then DE-BOOR$(t, p, P, u)$ returns $C(u) = \sum_{i=0}^{n} N_{i,p}(u) P_i$ when $u < t_{n+1}$, and $\lim_{v \to t_{n+1}^-} C(v)$ when $u = t_{n+1}$. Every step of line L6 is a convex combination.

**Step 1 (the span).** Let $u < t_{n+1}$. The binary search keeps $t_{lo} \le u < t_{hi}$, which holds at the start with $lo = p$ and $hi = n + 1$. Each step halves $hi - lo$ and keeps the inequalities, and it stops with $hi = lo + 1$. So $\mu = lo$ satisfies $p \le \mu \le n$ and $t_\mu \le u < t_{\mu+1}$, and the span is nonempty. For $u = t_{n+1}$ the search goes down from $\mu = n$ while $t_\mu = t_{\mu+1}$. It stops at a $\mu \ge p$, because $t_p < t_{n+1}$, and then $t_\mu < t_{\mu+1} = t_{n+1}$.

**Step 2 (local support).** If $N_{i,q}(u) \ne 0$ then $t_i \le u < t_{i+q+1}$; this follows by induction on $q$ from the recursion (see the proof on the Cox-de Boor page). So for $t_\mu \le u < t_{\mu+1}$, $N_{i,q}(u) \ne 0$ needs $\mu - q \le i \le \mu$. In particular

$$C(u) = \sum_{i=\mu-p}^{\mu} N_{i,p}(u) P_i, \tag{1}$$

and the indices $\mu - p, \ldots, \mu$ lie in $0, \ldots, n$ because $p \le \mu \le n$.

**Step 3 (one round of the recursion).** Let $1 \le q \le p$ and let $Q_{\mu-q}, \ldots, Q_\mu$ be points. Then, for $t_\mu \le u < t_{\mu+1}$,

$$\sum_{i=\mu-q}^{\mu} N_{i,q}(u) \, Q_i = \sum_{i=\mu-q+1}^{\mu} N_{i,q-1}(u) \bigl( (1 - \omega_{i,q}(u)) \, Q_{i-1} + \omega_{i,q}(u) \, Q_i \bigr). \tag{2}$$

*Proof.* Put the recursion $N_{i,q} = \omega_{i,q} N_{i,q-1} + (1 - \omega_{i+1,q}) N_{i+1,q-1}$ into the left side and split it into two sums. In the first sum, $\sum_{i=\mu-q}^{\mu} \omega_{i,q} N_{i,q-1}(u) Q_i$, the term $i = \mu - q$ is $0$, because $N_{\mu-q,q-1}(u) = 0$ by Step 2. In the second sum, $\sum_{i=\mu-q}^{\mu} (1 - \omega_{i+1,q}) N_{i+1,q-1}(u) Q_i$, replace $i$ by $i - 1$; it becomes a sum over $i = \mu - q + 1, \ldots, \mu + 1$ of $(1 - \omega_{i,q}) N_{i,q-1}(u) Q_{i-1}$, and its term $i = \mu + 1$ is $0$, because $N_{\mu+1,q-1}(u) = 0$. The dropped terms are zero also when their weight has a zero denominator, by the rule. For the remaining $i$, $\mu - q + 1 \le i \le \mu$, we have $t_{i+q} - t_i \ge t_{\mu+1} - t_\mu > 0$, because $i \le \mu$ and $i + q \ge \mu + 1$, so the weights are ordinary numbers. Adding the two sums term by term gives the right side. $\square$

**Step 4 (the array holds the levels).** Define $P_i^{[0]} = P_i$ for $\mu - p \le i \le \mu$, and for $1 \le r \le p$ and $\mu - p + r \le i \le \mu$

$$P_i^{[r]} = (1 - \alpha_{i,r}) P_{i-1}^{[r-1]} + \alpha_{i,r} P_i^{[r-1]}, \qquad \alpha_{i,r} = \frac{u - t_i}{t_{i+p-r+1} - t_i} = \omega_{i,p-r+1}(u).$$

We show by induction on $r$: after round $r$ (after line L2 for $r = 0$), $d[j] = P_{\mu-p+j}^{[r]}$ for $r \le j \le p$. For $r = 0$ it is line L2. Assume it for $r - 1$. In round $r$, line L4 visits $j = p, p - 1, \ldots, r$, and the step for $j$ writes only $d[j]$. When the step for $j$ runs, the steps for larger indices have run, but $d[j]$ and $d[j-1]$ have not been written in this round. So they hold $P_{\mu-p+j}^{[r-1]}$ and $P_{\mu-p+j-1}^{[r-1]}$ by the hypothesis, which applies because $j - 1 \ge r - 1$. Line L5 computes $\alpha_{i,r}$ with $i = \mu - p + j$, because $t_{\mu+j-r+1} = t_{i+p-r+1}$, and line L6 stores $P_i^{[r]}$ in $d[j]$. This proves the step.

The weights are convex: $t_i \le t_\mu \le u$ because $i \le \mu$, and $u < t_{\mu+1} \le t_{i+p-r+1}$ because $i + p - r + 1 \ge \mu + 1$, so $0 \le \alpha_{i,r} < 1$.

**Step 5 (the result).** Apply (2) with $q = p - r + 1$ and $Q_i = P_i^{[r-1]}$, for $r = 1, \ldots, p$. Its weights are $\omega_{i,p-r+1}(u) = \alpha_{i,r}$, so (2) reads

$$\sum_{i=\mu-p+r-1}^{\mu} N_{i,p-r+1}(u) \, P_i^{[r-1]} = \sum_{i=\mu-p+r}^{\mu} N_{i,p-r}(u) \, P_i^{[r]} .$$

Start from (1) and use this for $r = 1, 2, \ldots, p$. After the last use, $C(u) = N_{\mu,0}(u) P_\mu^{[p]} = P_\mu^{[p]}$, because $t_\mu \le u < t_{\mu+1}$. By Step 4 this is $d[p]$, which line L7 returns.

**Step 6 (the right end).** Fix $\mu$ and let $v$ run over $[t_\mu, t_{\mu+1})$. The algorithm does the same operations for each such $v$, and each weight $\alpha_{i,r}$ is a polynomial of degree 1 in $v$ with a fixed positive denominator. So the output is a polynomial $g(v)$ in each coordinate, and $g(v) = C(v)$ on the half-open span by Step 5. For $u = t_{n+1}$, Step 1 gives the last nonempty span, with $t_{\mu+1} = t_{n+1}$, and the algorithm returns $g(t_{\mu+1}) = \lim_{v \to t_{n+1}^-} C(v)$, by the continuity of a polynomial. The weights there are $\alpha_{i,r} = (t_{\mu+1} - t_i)/(t_{i+p-r+1} - t_i) \in [0, 1]$, so line L6 is still a convex combination.

**Cost.** Round $r$ does $p - r + 1$ steps of lines L5 and L6, so there are $p(p + 1)/2$ steps, each with one division and $O(d)$ operations on points of $\mathbb{R}^d$; the span search takes $O(\log n)$ comparisons, and the array holds $p + 1$ points. $\blacksquare$
