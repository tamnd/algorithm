---
title: Algorithm P visits each partition of n once, in reverse lexicographic order, in Theta(p(n)) time
proves: [correctness, time.worst]
status: full
---

**Statement.** For each integer $n \ge 0$, PARTITIONS$(n)$ visits each partition of $n$ exactly once, in decreasing lexicographic order of the non-increasing sequences of parts, and stops. Its running time is $\Theta(p(n))$.

**Setup.** A partition is a sequence $a = (a_1, \ldots, a_m)$ with $a_1 \ge \cdots \ge a_m \ge 1$ and sum $n$. For two partitions of $n$, $a < b$ in lexicographic order when $a$ is a proper prefix of $b$, or when $a_i < b_i$ at the first index $i$ where they differ. Two different partitions of the same $n$ are never prefixes of each other, since the sums agree. So the second case always applies. For $a \ne (1^n)$ let $q(a)$ be the largest index with $a_q \ge 2$, and let $q(1^n) = 0$.

**Lemma 1 (greedy tail).** Let $s \ge 1$ and $x \ge 1$. Among the partitions of $s$ with each part at most $x$, the largest in lexicographic order is $G(s, x) = (x^t, \rho)$, where $t \ge 0$ and $1 \le \rho \le x$ are given by $s = tx + \rho$.

*Proof.* By strong induction on $s$. The first part of a partition of $s$ with parts at most $x$ is at most $\min(s, x)$. If $s \le x$ then $(s)$ is a partition with first part $s$, so it is the largest, and $G(s, x) = (s)$ with $t = 0$, $\rho = s$. If $s > x$, the largest first part is $x$, and a partition with first part $x$ continues with a partition of $s - x$ into parts at most $x$. Among these the largest is $G(s - x, x)$ by the induction hypothesis, since $s - x < s$. So the largest is $(x) \cdot G(s - x, x) = G(s, x)$. $\square$

**Lemma 2 (lines L10 to L12).** In the branch of line L9, lines L10 to L12 leave $a[q+1 \ldots m] = G(s_0, x)$, where $s_0 = m_{\text{old}} - q + 1$ and $x = a_q - 1$.

*Proof.* The loop of line L11 keeps the sum of the written tail plus $s$ equal to $s_0$. Each run subtracts $x \ge 2$ from $s$, so the loop stops after $t = \lceil s_0 / x \rceil - 1$ runs, with $1 \le s \le x$. It has written $x^t$, and line L12 writes $\rho = s$. This is $G(s_0, x)$. $\square$

**Lemma 3 (one step).** Let $a \ne (1^n)$ be a partition of $n$ and $q = q(a)$. Then the step of lines L7 to L13 changes $a$ into its predecessor $a^-$, the largest partition of $n$ that is smaller than $a$, and it sets $q$ to $q(a^-)$.

*Proof.* Write $a = (a_1, \ldots, a_q, 1^r)$ with $a_q \ge 2$ and $r = m - q$.

1. Let $b < a$ be a partition of $n$ and let $i$ be the first index where they differ, so $b_i < a_i$. If $i > q$ then $a_i = 1$ and $b_i < 1$, which is impossible. So $i \le q$.
2. Let $c = (a_1, \ldots, a_{q-1}, x) \cdot G(r + 1, x)$ with $x = a_q - 1 \ge 1$. Its parts are non-increasing: $a_{q-1} \ge a_q > x$, and the parts of $G(r + 1, x)$ are at most $x$. Its sum is $a_1 + \cdots + a_q - 1 + r + 1 = n$. So $c$ is a partition of $n$, and $c < a$ because they first differ at index $q$.
3. Let $b < a$ be a partition of $n$ that first differs from $a$ at $i$. If $i < q$, then $c_i = a_i > b_i$ and $c$ agrees with $b$ before $i$, so $b < c$. If $i = q$ and $b_q < x$, then $b < c$ in the same way. If $i = q$ and $b_q = x$, then $b$ continues with a partition of $r + 1$ into parts at most $x$, and Lemma 1 gives $b \le c$. So $c$ is the largest partition below $a$, that is, $c = a^-$.
4. If $a_q = 2$, then $x = 1$ and $G(r + 1, 1) = (1^{r+1})$, so $a^- = (a_1, \ldots, a_{q-1}, 1^{r+2})$. Line L8 writes exactly this. The last part greater than $1$ is now $a_{q-1}$ if $q \ge 2$ (it is at least $a_q = 2$), and there is none if $q = 1$. So $q - 1$ is $q(a^-)$.
5. If $a_q \ge 3$, then $x \ge 2$, and by Lemma 2 with $s_0 = r + 1$, lines L10 to L12 write $a^-$. If the last part $\rho$ is greater than $1$, it is the last part greater than $1$, at index $m$. If $\rho = 1$, then the part before it is $x \ge 2$ (either one of the $t$ copies of $x$ or $a_q$ itself at index $q = m - 1$). Line L13 sets $q$ to these values. $\square$

**Theorem (correctness).** PARTITIONS$(n)$ visits each partition of $n$ exactly once, in decreasing lexicographic order, and stops.

*Proof.* For $n = 0$ line L1 visits the one partition of $0$. For $n \ge 1$, line L2 makes $a = (n)$, the largest partition of $n$, since every other partition has a first part smaller than $n$. Line L3 sets $q = q((n))$: it is $1$ when $n \ge 2$ and $0$ when $n = 1$. We use the invariant

> **(I)** At line L5, $a[1 \ldots m]$ is a partition of $n$, $q = q(a)$, and the visits so far are, in order, all partitions of $n$ that are larger than $a$, from the largest down.

(I) holds at the first visit. If $q = 0$ at line L6, then $a = (1^n)$, which is the smallest partition, and the algorithm stops after it has visited all partitions. Otherwise Lemma 3 makes $a$ into $a^-$ with the correct $q$, and since no partition lies strictly between $a^-$ and $a$, (I) holds at the next visit. Each step moves $a$ to a smaller partition of a finite set, so the number of partitions below $a$ drops by exactly $1$ at each step, and the loop stops after $p(n)$ visits. $\square$

**Theorem (time).** PARTITIONS$(n)$ runs in $\Theta(p(n))$ time.

*Proof.* Lines L1 to L3 take $O(1)$ time plus the allocation of the array, which is $O(n) \subseteq O(p(n))$ since $p(n) \ge n$ for $n \ge 1$ (the partitions $(n - j, 1^j)$ for $0 \le j \le n - 1$ are distinct). Each pass of the loop, without the runs of line L11, takes $O(1)$ time, and there are $p(n)$ passes. It remains to bound the total number $R$ of runs of line L11.

A run of line L11 happens only in a step from a partition $\lambda = (a_1, \ldots, a_{q-1}, y, 1^r)$ with $y = a_q \ge 3$. With $x = y - 1$, Lemma 2 shows that the loop runs $\lceil (r + 1)/x \rceil - 1 = \lfloor r / x \rfloor$ times. Define, for $1 \le j \le \lfloor r / x \rfloor$,

$$\Phi(\lambda, j) = (a_1, \ldots, a_{q-1}, y, x^j, 1^{r - jx}).$$

This is a partition of $n$, since $a_{q-1} \ge y > x \ge 2$ and $r - jx \ge 0$. In $\Phi(\lambda, j)$ the parts greater than $1$ are $a_1, \ldots, a_{q-1}$ and $y$, all at least $y$, and $j$ copies of $x = y - 1$. So the smallest part greater than $1$ is $x$, its multiplicity is $j$, and $x + 1$ is a part. From $\Phi(\lambda, j)$ we read $x$ and $j$, and we get $\lambda$ back by replacing the $j$ parts $x$ by $jx$ ones. So $\Phi$ is injective, and $R \le p(n)$.

Hence the total time is $O(p(n))$. It is $\Omega(p(n))$ because there are $p(n)$ visits. $\blacksquare$

**Remark.** The map $\Phi$ is onto the set of partitions of $n$ whose smallest part $z > 1$ has $z + 1$ also as a part. For such a $\nu$ with $z$ of multiplicity $j$, replace the $j$ parts $z$ by $jz$ ones to get $\lambda$; then the smallest part greater than $1$ of $\lambda$ is $y = z + 1 \ge 3$, $\lambda$ has $r \ge jz$ ones, and $\Phi(\lambda, j) = \nu$. So $R$ equals the size of that set.
