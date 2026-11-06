---
title: Correctness of Pollard's rho algorithm
proves: [correctness, termination]
status: full
---

Let $N \ge 2$, $c$ an integer and $0 \le s < N$. Let $f(x) = (x^2 + c) \bmod N$ and $x_i = f^{(i)}(s)$, so $x_0 = s$.

**Lemma 1 (the passes).** After $i$ passes of the loop of lines L2 to L5, $x = x_i$ and $y = x_{2i}$.

*Proof.* Line L1 gives $x = y = s = x_0$. If $x = x_i$ and $y = x_{2i}$ before a pass, then line L3 gives $x = f(x_i) = x_{i+1}$ and line L4 gives $y = f(f(x_{2i})) = x_{2i + 2}$. $\square$

**Lemma 2 (reduction).** For each divisor $m \ge 1$ of $N$, the residues $u_i = x_i \bmod m$ satisfy $u_{i+1} = (u_i^2 + c) \bmod m$. So $u_i$ is the orbit of $u_0$ under the map $h(u) = (u^2 + c) \bmod m$ on the finite set $\{0, \dots, m - 1\}$.

*Proof.* $x_{i+1} = x_i^2 + c - kN$ for some integer $k$, and $m \mid N$, so $x_{i+1} \equiv x_i^2 + c \equiv u_i^2 + c \pmod m$. $\square$

**Lemma 3 (Floyd).** Let $u_0, u_1, \dots$ be the orbit of a map $h$ on a finite set of size $m$. There are integers $\mu \ge 0$ and $\lambda \ge 1$ with $\mu + \lambda \le m$ such that $u_0, \dots, u_{\mu + \lambda - 1}$ are distinct and $u_{i + \lambda} = u_i$ for all $i \ge \mu$. For $i \ge 1$, $u_i = u_{2i}$ holds if and only if $i \ge \mu$ and $\lambda \mid i$. The least such $i \ge 1$ is at most $\mu + \lambda \le m$.

*Proof.* Among $u_0, \dots, u_m$ there are $m + 1$ values in a set of size $m$, so some value repeats. Let $j$ be the least index such that $u_j = u_k$ for some $k < j$, and let $\mu = k$, $\lambda = j - k$. Then $u_0, \dots, u_{j - 1}$ are distinct, $j = \mu + \lambda \le m$, and $u_{\mu + \lambda} = u_\mu$. Applying $h$ repeatedly gives $u_{i + \lambda} = u_i$ for every $i \ge \mu$, and so $u_{i + t\lambda} = u_i$ for $t \ge 0$.

If $i \ge \mu$ and $\lambda \mid i$, write $i = t\lambda$; then $u_{2i} = u_{i + t\lambda} = u_i$. Conversely, let $u_i = u_{2i}$ with $i \ge 1$. If $i < \mu$, then the value $u_i$ lies on the tail, but every $u_k$ with $k \ge \mu$ is on the cycle $\{u_\mu, \dots, u_{\mu+\lambda-1}\}$, which is disjoint from the tail since $u_0, \dots, u_{\mu+\lambda-1}$ are distinct; and if $2i < \mu$ then $u_i$ and $u_{2i}$ are two distinct tail values. Either way $u_i \ne u_{2i}$, a contradiction, so $i \ge \mu$. Then $u_{2i} = u_i$ with both indices at least $\mu$, and on the cycle $u_k = u_l$ for $k, l \ge \mu$ holds only if $\lambda \mid k - l$, because $u_\mu, \dots, u_{\mu+\lambda-1}$ are distinct. So $\lambda \mid i$. Among $\mu, \mu + 1, \dots, \mu + \lambda - 1$ there is a multiple of $\lambda$, and if $\mu = 0$ then $\lambda$ itself works; so the least $i \ge 1$ with $u_i = u_{2i}$ is at most $\mu + \lambda$. $\square$

**Termination.** Apply Lemmas 2 and 3 with $m = N$. There is an $i^* \le N$ with $x_{i^*} = x_{2i^*}$. If the loop has not stopped before pass $i^*$, then at pass $i^*$, by Lemma 1, line L5 computes $\gcd(0, N) = N \ne 1$, and the loop stops. So the loop runs at most $N$ passes.

**Correctness.** The loop stops only when $g \ne 1$, and $g$ is a gcd with $N \ge 2$, so the returned $g$ is a divisor of $N$ with $g > 1$.

**When it succeeds.** Let the loop stop at pass $i$. For each prime power $r^k \parallel N$, $r^k \mid g$ if and only if $x_i \equiv x_{2i} \pmod{r^k}$. So $g < N$ exactly when some prime power part of $N$ has not yet closed its cycle in the sense of Lemma 3 at pass $i$, and $g > 1$ shows that some prime $r \mid N$ has $x_i \equiv x_{2i} \pmod r$. In particular, if a prime $p \mid N$ has its first $i \ge 1$ with $x_i \equiv x_{2i} \pmod p$ strictly smaller than the first such $i$ for $N$, then the algorithm returns a proper factor of $N$ that is a multiple of $p$. $\blacksquare$
