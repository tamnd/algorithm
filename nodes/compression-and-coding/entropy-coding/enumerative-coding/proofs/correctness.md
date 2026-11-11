---
title: Cover's rank is a bijection from the sequences of length n and weight k onto the integers below C(n, k), unrank inverts it, and the two-part code is within lg(n + 1) + 2 bits of n h(k/n)
proves: [correctness, termination, length]
status: full
---

Notation. Positions are numbered $1$ to $n$. For a binary sequence $x$ of length $n$ and weight $k$ (the number of ones), let $S_{n,k}$ be the set of all such sequences, ordered lexicographically with $0 < 1$. For a prefix $u$ of length $i - 1$, let $N(u)$ be the number of sequences in $S_{n,k}$ that start with $u$. We use $\binom{m}{j} = 0$ for $j > m$ or $j < 0$.

**Lemma 1 (counting).** If $u$ has length $i - 1$ and $k - j$ ones, with $0 \le j \le k$, then $N(u) = \binom{n - i + 1}{j}$, $N(u0) = \binom{n - i}{j}$ and $N(u1) = \binom{n - i}{j - 1}$.

*Proof.* A sequence in $S_{n,k}$ that starts with $u$ is fixed by the positions of its $j$ remaining ones among the $n - i + 1$ remaining places. The other two counts follow in the same way with $n - i$ places and $j$ or $j - 1$ ones. $\square$

**Lemma 2 (Cover's formula).** For $x \in S_{n,k}$, the number of sequences $y \in S_{n,k}$ with $y < x$ is

$$\operatorname{rank}(x) = \sum_{i=1}^{n} \sum_{c < x_i} N(x_1 \ldots x_{i-1} c) = \sum_{i : x_i = 1} \binom{n - i}{j_i},$$

where $j_i$ is the number of ones of $x$ at positions $i$ to $n$.

*Proof.* If $y < x$, there is a first position $i$ where they differ, and there $y_i < x_i$. So the set of smaller sequences splits into disjoint classes, one for each $i$ and each $c < x_i$: the sequences that start with $x_1 \ldots x_{i-1} c$. Their sizes add up to the first sum. In the binary case, $c < x_i$ exists only when $x_i = 1$ and then $c = 0$. The prefix $x_1 \ldots x_{i-1}$ has $k - j_i$ ones, so by Lemma 1 the class has $\binom{n - i}{j_i}$ elements. $\square$

The loop of lines L1 to L6 computes this sum: $j$ starts at $k$ and drops by one after each 1, so at position $i$ it equals $j_i$.

**Theorem 1 (bijection).** The map $x \mapsto \operatorname{rank}(x)$ is a bijection from $S_{n,k}$ onto $\{0, 1, \ldots, \binom{n}{k} - 1\}$ that keeps the order.

*Proof.* By Lemma 2, the rank of $x$ is the number of elements of $S_{n,k}$ before it. In a finite totally ordered set of $M$ elements, this number takes each value $0, \ldots, M - 1$ exactly once, in increasing order. Here $M = \binom{n}{k}$. $\square$

**Theorem 2 (unrank).** For $0 \le r < \binom{n}{k}$, UNRANK$(n, k, r)$ returns the element of $S_{n,k}$ with rank $r$.

*Proof.* Let $x$ be the element with rank $r$. We show that before step $i$ the output so far is $x_1 \ldots x_{i-1}$, $j = j_i$, and the remaining value of $r$ equals the rank of $x$ among the sequences that start with $x_1 \ldots x_{i-1}$, that is, $r$ minus the sum of the first $i - 1$ terms of Lemma 2. Before step 1 this holds. At step $i$, the sequences that start with $u = x_1 \ldots x_{i-1}$ come in order: first the $N(u0) = \binom{n-i}{j}$ that continue with 0, then the $N(u1)$ that continue with 1. So $x_i = 1$ exactly when the remaining rank is at least $\binom{n-i}{j}$, which is the test of line L10; in that case $x$ has rank $r - \binom{n-i}{j}$ among the sequences that start with $u1$, and $j$ drops by one. Otherwise $x_i = 0$ and nothing changes. The invariant holds after step $n$, so the output is $x$. $\square$

The edge cases need no special code. If $j = 0$, the remaining rank is below $N(u) = 1$, so it is 0 and the test with $\binom{n-i}{0} = 1$ gives 0. If $j = n - i + 1$, then $\binom{n-i}{j} = 0$ and the test gives 1.

**Theorem 3 (length).** Let $h(p) = -p \lg p - (1 - p) \lg(1 - p)$ be the [binary entropy function](/binary-entropy-function/). Then

$$n\, h(k/n) - \lg(n + 1) \le \lg \binom{n}{k} \le n\, h(k/n),$$

and the two-part code, $\lceil \lg(n + 1) \rceil$ bits for $k$ and $\lceil \lg \binom{n}{k} \rceil$ bits for the rank, has length at most $n\, h(k/n) + \lg(n + 1) + 2$.

*Proof.* Let $p = k/n$ and $t_i = \binom{n}{i} p^i (1 - p)^{n - i}$. For $0 < k < n$, $t_k = \binom{n}{k} 2^{-n h(p)}$, because $p^k (1-p)^{n-k} = 2^{k \lg p + (n-k) \lg(1-p)} = 2^{-n h(p)}$. The cases $k = 0$ and $k = n$ give $\binom{n}{k} = 1$ and $h = 0$, and the claims hold. By the binomial theorem $\sum_i t_i = 1$, so $t_k \le 1$, which is the upper bound. For the lower bound, $t_{i+1}/t_i = \frac{(n - i)k}{(i + 1)(n - k)}$, which is at least 1 exactly when $n(i + 1) \le k(n + 1)$. This holds for $i \le k - 1$ and fails for $i \ge k$, so $t_k$ is the largest of the $n + 1$ terms and $t_k \ge 1/(n + 1)$. The code length bound follows from $\lceil z \rceil < z + 1$ for both parts. $\square$

**Remark (the link with the Laplace estimator).** The sequential Laplace estimator gives the bit after $i$ bits with $m$ ones the probability $(m + 1)/(i + 2)$ for a 1 and $(i - m + 1)/(i + 2)$ for a 0. The product over a sequence with $k$ ones has the numerators $1 \cdot 2 \cdots k$ and $1 \cdot 2 \cdots (n - k)$ and the denominators $2 \cdot 3 \cdots (n + 1)$, so it equals $\frac{k!\,(n - k)!}{(n + 1)!} = \frac{1}{(n + 1)\binom{n}{k}}$. An ideal arithmetic coder with this adaptive model therefore spends $\lg(n + 1) + \lg \binom{n}{k}$ bits, the same as the two-part enumerative code before rounding.

**Termination.** RANK and UNRANK each run one loop of $n$ steps with one binomial coefficient per step, so both end. $\blacksquare$
