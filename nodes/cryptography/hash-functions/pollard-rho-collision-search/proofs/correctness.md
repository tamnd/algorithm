---
title: Rho collision search returns the two predecessors of the join of tail and cycle
proves: [correctness]
status: full
---

Let $f : S \to S$ with $S$ finite, $x_0 \in S$, and $x_i = f^i(x_0)$. Since $S$ is finite, some value repeats. Let $\mu$ be the least index such that $x_\mu = x_j$ for some $j > \mu$, and let $\lambda$ be the least $\lambda \ge 1$ with $x_{\mu + \lambda} = x_\mu$.

**Lemma 1 (structure of the walk).** For $0 \le a < b$, $x_a = x_b$ if and only if $a \ge \mu$ and $\lambda \mid b - a$.

*Proof.* The values $x_0, \ldots, x_{\mu+\lambda-1}$ are pairwise distinct: a repeat among them would give a smaller $\mu$, or for $\mu$ fixed a smaller $\lambda$. Since $x_{\mu+\lambda} = x_\mu$, applying $f$ gives $x_{k+\lambda} = x_k$ for each $k \ge \mu$. So each index $k \ge \mu$ has the same value as the index $\mu + ((k - \mu) \bmod \lambda)$ in $\{\mu, \ldots, \mu + \lambda - 1\}$, and each index $k < \mu$ is its own representative. Two indices have equal values exactly when their representatives are equal, since the representatives have distinct values. For $a < b$ this means $a, b \ge \mu$ and $a \equiv b \pmod \lambda$. $\square$

**Lemma 2 (phase 1).** The loop of lines L2 and L3 ends. When it ends, $t = x_i$ and $h = x_{2i}$, where $i$ is the least multiple of $\lambda$ with $i \ge \max(\mu, 1)$.

*Proof.* Line L1 sets $t = x_1$ and $h = x_2$. Each round of line L3 adds 1 to the index of $t$ and 2 to the index of $h$. So before the test with $t = x_k$, $h = x_{2k}$, for $k = 1, 2, \ldots$. By Lemma 1 with $a = k$, $b = 2k$, the test $x_k = x_{2k}$ holds exactly when $k \ge \mu$ and $\lambda \mid k$. The least such $k \ge 1$ exists and is the $i$ of the claim. $\square$

**Lemma 3 (the FAIL test).** Line L5 returns FAIL if and only if $\mu = 0$.

*Proof.* At line L5, $t = x_0$ and $h = x_i$ with $i \ge 1$. By Lemma 1, $x_0 = x_i$ if and only if $0 \ge \mu$, that is $\mu = 0$, since $\lambda \mid i$. $\square$

**Lemma 4 (phase 2).** If $\mu \ge 1$, the loop of lines L6 and L7 ends with $t = x_{\mu-1}$ and $h = x_{i+\mu-1}$.

*Proof.* Before the $j$-th test of line L6, for $j = 0, 1, \ldots$, we have $t = x_j$ and $h = x_{i+j}$, since both move one step per round. The test compares $f(t) = x_{j+1}$ and $f(h) = x_{i+j+1}$. By Lemma 1, with $\lambda \mid i$ and $i \ge 1$, these are equal exactly when $j + 1 \ge \mu$. The least such $j \ge 0$ is $j = \mu - 1$. $\square$

**Theorem.** If $\mu = 0$, RHO-COLLISION returns FAIL. Otherwise it returns $(a, b)$ with $a \ne b$ and $f(a) = f(b)$. It makes at most $3\rho + 2\mu + 2$ calls of $f$, where $\rho = \mu + \lambda$, and stores $O(1)$ points.

*Proof.* Lemmas 2 and 3 give the first claim. For $\mu \ge 1$, Lemma 4 gives $a = x_{\mu-1}$ and $b = x_{i+\mu-1}$. Then $f(a) = x_\mu$ and $f(b) = x_{i+\mu} = x_\mu$ by Lemma 1, since $i + \mu \ge \mu$ and $\lambda \mid i$. Also $a \ne b$: by Lemma 1, $x_{\mu-1} = x_{i+\mu-1}$ would need $\mu - 1 \ge \mu$.

For the cost, phase 1 makes 3 calls at line L1 and 3 per round of line L3, for $i - 1$ rounds. Since $i$ is the least multiple of $\lambda$ that is at least $\max(\mu, 1)$, $i < \max(\mu, 1) + \lambda \le \rho + 1$, so $i \le \rho$ and phase 1 makes at most $3\rho$ calls. Phase 2 evaluates $f(t)$ and $f(h)$ once per test, for $\mu$ tests, so $2\mu$ calls; the implementation keeps these two values and reuses them at line L7. The algorithm holds only $x_0$, $t$, $h$ and two values of $f$ at any time. $\blacksquare$
