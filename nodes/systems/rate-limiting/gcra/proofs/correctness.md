---
title: GCRA(T, tau) makes the same decisions as a token bucket with r = 1/T and b = 1 + tau/T, and its two forms agree
proves: [correctness]
status: full
---

**Setup.** Let $T > 0$ and $\tau \ge 0$. The requests arrive at times $t_0 \le t_1 \le t_2 \le \cdots$, where $t_0$ is the start time, and request $j$ asks for $n_j \ge 1$ units. A plain cell is a request with $n_j = 1$. Let $\theta_j$ be the value of $tat$ just before request $j$, with $\theta_1 = t_0$. The general GCRA test for request $j$ is

$$\max(t_j, \theta_j) + n_j T - t_j \le \tau + T, \qquad (\ast)$$

and on a pass it sets $\theta_{j+1} = \max(t_j, \theta_j) + n_j T$; on a fail $\theta_{j+1} = \theta_j$. Write $D_j = \max(0, \theta_j - t_j)$, so the left side of $(\ast)$ is $D_j + n_j T$. For $n_j = 1$, $(\ast)$ reads $D_j \le \tau$. Since $\tau \ge 0$, this holds exactly when $\theta_j - t_j \le \tau$, that is when $t_j \ge \theta_j - \tau$. So for cells, $(\ast)$ is line L1 of the page, and the update is line L2.

Compare a token bucket with rate $r = 1/T$ and depth $b = 1 + \tau/T$, full at $t_0$. Let $x_j$ be its tokens after the refill at request $j$, so $x_1 = b$ and $x_{j+1} = \min(b, y_j + (t_{j+1} - t_j)/T)$, where $y_j = x_j - n_j$ if request $j$ passes the test $x_j \ge n_j$, and $y_j = x_j$ otherwise.

**Lemma 1 (floors compose).** For each real $y$ and each $d \ge 0$, $\max(0, \max(0, y) - d) = \max(0, y - d)$.

*Proof.* If $y \ge 0$ both sides are $\max(0, y - d)$. Else the left side is $\max(0, -d) = 0$ and the right side is $0$ because $y - d < 0$. $\square$

**Theorem 1 (GCRA is a token bucket).** For each $j$,

$$x_j = b - \frac{D_j}{T}, \qquad (1)$$

and request $j$ passes the GCRA if and only if it passes the token bucket.

*Proof.* We show (1) by induction on $j$, and the claim on decisions at each step.

*Base.* $\theta_1 = t_0 \le t_1$, so $D_1 = 0$, and $x_1 = b$.

*Decisions.* Assume (1) for $j$. Then $x_j \ge n_j$ is the same as $b - D_j/T \ge n_j$. Multiply by $T > 0$ and put $b T = T + \tau$: this is $D_j + n_j T \le \tau + T$, which is $(\ast)$. So the two tests agree.

*Step.* We first show $y_j = b - \max(0, \theta_{j+1} - t_j)/T$. If request $j$ passes, $\theta_{j+1} - t_j = D_j + n_j T \ge 0$, so the right side is $b - D_j/T - n_j = x_j - n_j = y_j$. If it fails, $\theta_{j+1} = \theta_j$, so the right side is $b - D_j/T = x_j = y_j$. Now let $d = (t_{j+1} - t_j)/T \ge 0$. Then

$$x_{j+1} = \min\big(b,\ b - \max(0, \theta_{j+1} - t_j)/T + d\big) = b - \max\big(0,\ \max(0, \theta_{j+1} - t_j)/T - d\big),$$

and by Lemma 1 this is $b - \max(0, \theta_{j+1} - t_{j+1})/T = b - D_{j+1}/T$. $\square$

So GCRA$(T, \tau)$ on cells of size $\delta$ is the token bucket with $r = \delta/T$ and $b = (\tau/T + 1)\delta$: take $\delta$ as the unit of data. This is Corollary 1.2.1 of Le Boudec and Thiran. The theorem also says what $tat$ means: $tat - t$, when it is positive, is the time that the bucket needs to refill, and the bucket is full when $tat \le t$.

**Theorem 2 (the two forms agree).** Run the continuous-state leaky bucket form with level $X = 0$ and last conformance time $lct = t_0$ at the start, on the same cells. Before each cell $j$, $X + lct = \theta_j$, and the two forms make the same decision on cell $j$.

*Proof.* By induction on $j$. At the start $X + lct = t_0 = \theta_1$. Assume $X + lct = \theta_j$ before cell $j$. Line L4 computes $X' = \max(0, X - (t_j - lct)) = \max(0, \theta_j - t_j) = D_j$. Line L5 rejects when $D_j > \tau$; since $\tau \ge 0$ this is $\theta_j - t_j > \tau$, the reject test of line L1. On a pass, line L6 sets $X = D_j + T$ and $lct = t_j$, so $X + lct = \max(t_j, \theta_j) + T = \theta_{j+1}$. On a fail neither form changes its state, and $\theta_{j+1} = \theta_j$. $\square$

**Corollary 1 (what passes).** The passed cells fit the arrival curve $\tau' \mapsto \tau'/T + 1 + \tau/T$: each interval of length $\tau'$ holds at most $\tau'/T + 1 + \tau/T$ passed cells. Equivalently, if passed cells number $m$ and $m + k$ are $k$ passed cells apart, then $t_{m+k} \ge t_m + kT - \tau$. A cell is rejected only if passing it would break this bound, and if every cell of the input fits the bound, every cell passes.

*Proof.* By Theorem 1 the decisions are those of a token bucket with $r = 1/T$ and $b = 1 + \tau/T$. The [token bucket](/token-bucket/) proof shows that its output fits $r\tau' + b$ (soundness), that it rejects only when passing would break the curve (greedy), and that a fitting input passes whole (tightness). For $k + 1$ passed cells from $t_m$ to $t_{m+k}$, soundness gives $k + 1 \le (t_{m+k} - t_m)/T + 1 + \tau/T$, which is $t_{m+k} \ge t_m + kT - \tau$. $\blacksquare$
