---
title: The birthday attack returns a real collision and its expected cost is Θ(2^(n/2))
proves: [correctness]
status: full
---

Let $H : \{0,1\}^\ast \to \{0,1\}^n$ and $N = 2^n$. Write $x_i$ = prefix $\|$ $i$ for the input made at line L3 in round $i$, with $i$ written in 8 bytes, so that $x_i \ne x_j$ for $i \ne j$.

**Lemma 1 (invariant).** At the start of round $i$ of line L2, the keys of $T$ are exactly the values $H(x_0), \ldots, H(x_{i-1})$, these values are pairwise distinct, and for each key $y$, $T[y]$ is the $x_j$ with $j < i$ and $H(x_j) = y$.

*Proof.* By induction on $i$. For $i = 0$, $T$ is empty, as line L1 makes it. Assume the claim at the start of round $i$, and suppose the round does not return. Then $y = H(x_i)$ is not a key of $T$ at line L5, so $H(x_i)$ differs from each earlier value. Line L6 adds the key $y$ with the value $x_i$. So the claim holds at the start of round $i + 1$. $\square$

**Lemma 2 (each output is a collision).** If the algorithm returns $(a, b)$ in round $i$, then $a \ne b$ and $H(a) = H(b)$.

*Proof.* The return happens at line L5 with $b = x_i$ and $y = H(x_i)$ a key of $T$. By Lemma 1, $a = T[y] = x_j$ for some $j < i$ with $H(x_j) = y$. So $H(a) = H(b)$, and $a = x_j \ne x_i = b$. $\square$

**Lemma 3 (termination).** The algorithm returns in round $i \le N$, so it makes at most $N + 1$ calls of $H$.

*Proof.* By Lemma 1, if it has not returned by the start of round $i$, then $T$ holds $i$ distinct values of $\{0,1\}^n$, so $i \le N$. In round $N$ the table is full, so $H(x_N)$ is a key and line L5 returns. $\square$

**Lemma 4 (expected cost).** If the values $H(x_0), H(x_1), \ldots$ are independent and uniform on $\{0,1\}^n$, let $Q$ be the number of calls of $H$. Then $\Pr[Q > q] = \prod_{i=1}^{q-1}(1 - i/N)$ for $1 \le q \le N + 1$, and

$$\sqrt{N}/2 \;\le\; \mathbb{E}[Q] \;\le\; \sqrt{\pi N/2} + 2.$$

*Proof.* The algorithm makes more than $q$ calls exactly when the first $q$ values are pairwise distinct. Given that the first $i$ values are distinct, the next one avoids them with probability $1 - i/N$. Multiply these for $i = 1, \ldots, q - 1$.

Upper bound. Since $Q$ is a positive integer, $\mathbb{E}[Q] = \sum_{q \ge 0} \Pr[Q > q]$. The terms $q = 0$ and $q = 1$ are each 1. For $q \ge 2$, since $1 - x \le e^{-x}$, $\Pr[Q > q] \le e^{-q(q-1)/2N} \le e^{-(q-1)^2/2N}$. With $k = q - 1$,

$$\mathbb{E}[Q] \le 2 + \sum_{k \ge 1} e^{-k^2/2N} \le 2 + \int_0^\infty e^{-u^2/2N}\,du = 2 + \sqrt{\pi N/2}.$$

The sum is at most the integral because the terms decrease in $k$.

Lower bound. Let $m = \lfloor \sqrt N \rfloor$. By the union bound over pairs, $\Pr[Q \le m] \le \binom{m}{2}/N \le m^2/2N \le 1/2$. So

$$\mathbb{E}[Q] \ge \sum_{q=0}^{m} \Pr[Q > q] \ge (m + 1)\Pr[Q > m] \ge (m + 1)/2 \ge \sqrt N / 2. \qquad \square$$

**Theorem.** BIRTHDAY-ATTACK always returns two distinct inputs with the same digest, after at most $2^n + 1$ calls of $H$. If $H$ acts as a random function on the inputs it is given, the expected number of calls is $\Theta(2^{n/2})$, and the table holds as many entries.

*Proof.* Lemma 3 gives termination, Lemma 2 gives correctness of the output, and Lemma 4 gives the expected cost. The table grows by one entry per call that does not return, so its size is $Q - 1$. $\blacksquare$
