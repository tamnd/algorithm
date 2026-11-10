---
title: The chain of chain sampling has expected length (1 + 1/W)^W - 1 and a factorial tail
proves: [time.worst, space.expected, space.worst]
status: full
---

We use the random choices $K_u, D_u$ and Lemmas 1 to 3 of [the correctness proof](correctness.md).

**Time.** One step runs each of lines L1 to L7 at most once. Each line does a constant number of deque operations and at most one call of RANDOM. Line L7 replaces the chain by a new one-element chain; with garbage collection this is one assignment, and with explicit freeing it costs one step per freed element, which is $O(1)$ amortized since each element is freed at most once. So a step takes $O(1)$ time in the worst case, apart from freeing.

**Lemma 4.** Fix $t$ and an index $s$ in the window at step $t$, and let $m = t - s$, so $0 \le m \le \min(t, W) - 1$. Conditioned on $S_t = s$, the number of elements of the chain is $1 + N$, where $N$ is the largest $k$ such that $X_1 + \cdots + X_k \le m$ for independent $X_1, X_2, \ldots$ uniform on $\{1, \ldots, W\}$.

*Proof.* By Lemma 1 the chain is $c_0 = s$, $c_{j+1} = c_j + D_{c_j}$, continued while $c_j \le t$. The offsets used are $D_{c_0}, D_{c_1}, \ldots$, all of indices $c_j \ge s > t - W$. By Lemma 3 the event $S_t = s$ is a function of the coins and of the $D_u$ with $u \le t - W$, so it is independent of all $D_u$ with $u > t - W$. Given $S_t = s$, the sequence $D_{c_0}, D_{c_1}, \ldots$ is therefore a sequence of independent uniform offsets: each $c_{j+1}$ is a function of $D_{c_0}, \ldots, D_{c_j}$, and $D_{c_{j+1}}$ is a fresh offset of a larger index. The chain has $1 + k$ elements exactly when $c_k = s + X_1 + \cdots + X_k \le t$ and $c_{k+1} > t$. $\square$

**Lemma 5.** For $0 \le m \le W - 1$ and $k \ge 0$, $\Pr[X_1 + \cdots + X_k \le m] = \binom{m}{k} W^{-k}$.

*Proof.* Since $m < W$, every $k$-tuple of positive integers with sum at most $m$ has all parts at most $W$, so the tuples of $\{1, \ldots, W\}^k$ with sum at most $m$ are the $k$-tuples of positive integers with sum at most $m$. Adding a slack part $m - \sum x_i \ge 0$ and shifting it by 1 maps them one to one to the compositions of $m + 1$ into $k + 1$ positive parts, of which there are $\binom{m}{k}$. Each tuple has probability $W^{-k}$. $\square$

**Theorem 1 (expected memory).** For $t \ge W$, the expected number of chain elements after step $t$ is $(1 + 1/W)^W - 1$, which is less than $e - 1$. For $t < W$ it is $\frac{W}{t}\bigl((1 + 1/W)^t - 1\bigr)$, which is at most the value for $t = W$.

*Proof.* By Lemmas 4 and 5, conditioned on $m$, $\Pr[1 + N \ge k + 1] = \Pr[X_1 + \cdots + X_k \le m] = \binom{m}{k} W^{-k}$, so

$$\mathbb{E}[1 + N \mid m] = \sum_{k \ge 0} \binom{m}{k} W^{-k} = \Bigl(1 + \frac{1}{W}\Bigr)^m$$

by the binomial theorem. By the theorem of the correctness proof, $m = t - S_t$ is uniform on $\{0, \ldots, n - 1\}$ with $n = \min(t, W)$. So the expected length is

$$\frac{1}{n} \sum_{m=0}^{n-1} \Bigl(1 + \frac{1}{W}\Bigr)^m = \frac{1}{n} \cdot \frac{(1 + 1/W)^n - 1}{1/W} = \frac{W}{n}\Bigl(\Bigl(1 + \frac{1}{W}\Bigr)^n - 1\Bigr).$$

For $n = W$ this is $(1 + 1/W)^W - 1 < e - 1$, since $(1 + 1/W)^W < e$ for every $W \ge 1$. The function $g(x) = ((1 + 1/W)^x - 1)/x$ is non-decreasing for $x > 0$, because $(1 + 1/W)^x - 1$ is convex in $x$ and is $0$ at $x = 0$, so the value for $n = t < W$ is at most the value for $n = W$. $\square$

**Theorem 2 (tail).** For every $t$ and $k \ge 1$, the chain has more than $k$ elements with probability less than $1/k!$. For every constant $c > 0$, there is a $k = O(\log W / \log \log W)$ with $1/k! \le W^{-c}$.

*Proof.* By Lemmas 4 and 5, conditioned on $m \le W - 1$, the chain has more than $k$ elements with probability $\binom{m}{k} W^{-k} \le \frac{m^k}{k!\, W^k} < \frac{1}{k!}$. Averaging over $m$ keeps the bound. For the second claim, $\ln k! \ge k \ln k - k$, and with $k = \lceil 2c \ln W / \ln \ln W \rceil$ and $W$ large enough, $k \ln k - k \ge c \ln W$. $\square$

**Worst case.** The chain never has more than $W$ elements, since by Lemma 1 its indices are distinct and lie in the window. When every offset is 1 and every coin fails, all $W$ items of the window are in the chain. $\blacksquare$
