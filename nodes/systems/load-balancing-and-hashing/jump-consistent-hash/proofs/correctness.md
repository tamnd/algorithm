---
title: Jump consistent hash returns a bucket in range, is exactly monotone, and is uniform in the ideal model
proves: [correctness]
status: full
---

We use the pseudocode of the page. Fix a key. The update of line L4 does not depend on $n$, so the key goes through the same sequence of states $x_1, x_2, \ldots$ for every $n$. Write $y_t = \lfloor x_t / 2^{33} \rfloor$, a 31-bit number, and define the sequence $J$ by $j_0 = 0$ and

$$j_{t} = \left\lfloor (j_{t-1} + 1) \cdot \frac{2^{31}}{y_t + 1} \right\rfloor \qquad (t \ge 1),$$

where the quotient and the product are computed in double precision, as in line L5. Only Theorem 3 below uses the exact real value.

**Lemma 1 (the sequence grows).** $j_t \ge j_{t-1} + 1$ for each $t \ge 1$.

*Proof.* $0 \le y_t \le 2^{31} - 1$, so $2^{31} / (y_t + 1) \ge 1$, and the product is at least $j_{t-1} + 1$, which is an integer. In double precision the quotient is at least 1.0 and the product of an integer below $2^{53}$ by a number at least 1.0 is at least that integer, so the floor is at least $j_{t-1} + 1$ in the code too. $\square$

**Lemma 2 (what the loop returns).** For $n \ge 1$, JUMP-HASH$(key, n)$ runs the loop body once for each element of $J$ below $n$, and returns $\max\{ j \in J : j < n \}$.

*Proof.* Line L1 sets $j = j_0 = 0 < n$, so the body runs. By induction on $t$, the $t$-th run of the body sets $b = j_{t-1}$ and then $j = j_t$, because lines L4 and L5 compute $x_t$ and $j_t$ from $b = j_{t-1}$. The loop stops at the first $t$ with $j_t \ge n$. By Lemma 1 the sequence grows, so this $t$ exists, and then $b = j_{t-1}$ is the largest element of $J$ below $n$. $\square$

**Theorem 1 (range).** The result is in $\{0, \ldots, n-1\}$, and the body runs at most $n$ times.

*Proof.* $j_0 = 0 < n$ is in $J$, so the maximum of Lemma 2 exists and lies in $[0, n)$. The elements of $J$ below $n$ are distinct integers in $[0, n)$, so there are at most $n$ of them. $\square$

**Theorem 2 (monotonicity).** For each key and each $n \ge 1$, JUMP-HASH$(key, n+1)$ is either JUMP-HASH$(key, n)$ or $n$.

*Proof.* By Lemma 2 the result for $n + 1$ is the largest element of $J$ below $n + 1$. If $n \in J$, this is $n$. Otherwise the elements of $J$ below $n + 1$ are the elements below $n$, and the largest one is the result for $n$. $\square$

This holds for every key, with no probabilistic assumption. Reading it backwards: when the last bucket $n$ is removed, only the keys on bucket $n$ move.

**The ideal model.** Now replace $(y_t + 1) / 2^{31}$ by independent random numbers $r_t$, uniform on $(0, 1]$, so that $j_t = \lfloor (j_{t-1} + 1) / r_t \rfloor$. For an integer $i > b$ and $j_{t-1} = b$,

$$\Pr[j_t \ge i] = \Pr\left[\frac{b + 1}{r_t} \ge i\right] = \Pr\left[r_t \le \frac{b + 1}{i}\right] = \frac{b + 1}{i}.$$

The next element depends only on the current one and a fresh $r_t$.

**Theorem 3 (uniform buckets in the ideal model).** In the ideal model, $\Pr[\text{JUMP-HASH}(key, n) = c] = 1/n$ for each $n \ge 1$ and each $c \in \{0, \ldots, n-1\}$. The expected number of runs of the loop body is the harmonic number $H_n = \sum_{i=1}^{n} 1/i$.

*Proof.* Let $q(c) = \Pr[c \in J]$ and $p_n(c) = \Pr[\text{the result for } n \text{ is } c]$. By Lemma 2 the result is $c < n$ if and only if $c \in J$ and the element of $J$ after $c$ is at least $n$. By the Markov property and the formula above with $b = c$ and $i = n$,

$$p_n(c) = q(c) \cdot \frac{c + 1}{n}. \qquad (*)$$

We show $p_n(c) = 1/n$ by induction on $n$. For $n = 1$, the result is 0 with probability 1. Assume the claim for $n$. For $c < n$, $(*)$ gives $p_{n+1}(c) = q(c)(c+1)/(n+1) = p_n(c) \cdot n / (n+1) = 1/(n+1)$. The remaining value is $c = n$, so $p_{n+1}(n) = 1 - n/(n+1) = 1/(n+1)$.

From $(*)$ with $n = c + 1$, $q(c) = p_{c+1}(c) = 1/(c+1)$. By Lemma 2 the body runs once for each element of $J$ below $n$, so the expected number of runs is $\sum_{c=0}^{n-1} q(c) = \sum_{c=0}^{n-1} 1/(c+1) = H_n$. $\blacksquare$

**Consequence.** In the ideal model, going from $n$ to $n + 1$ buckets moves a key with probability $q(n) = 1/(n+1)$, and every bucket keeps the share $1/(n+1)$. This is the smallest expected movement for which the shares stay equal: the new bucket must receive $1/(n+1)$ of the keys, and by Theorem 2 it receives nothing more.

**The real generator.** The code uses the 64-bit linear congruential generator $x \mapsto a x + 1 \bmod 2^{64}$ with $a = 2862933555777941757$. Since the increment 1 is odd and $a \equiv 1 \pmod 4$, the generator has the full period $2^{64}$ (Knuth, TAOCP Vol. 2, Theorem 3.2.1.2A). Its successive top bits are not independent, so Theorem 3 is a statement about the ideal model. Theorems 1 and 2 hold for the real code.
