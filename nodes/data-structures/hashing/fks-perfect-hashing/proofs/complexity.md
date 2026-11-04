---
title: FKS perfect hashing builds in O(n) expected time and uses O(n) space
proves: [time.expected, space.extra]
status: full
---

We use one fact about the family $h_{a,b,m}(x) = ((ax + b) \bmod p) \bmod m$, with $a$ uniform in $\{1, \ldots, p - 1\}$ and $b$ uniform in $\{0, \ldots, p - 1\}$:

> **(U)** For each $m \ge 1$ and each two distinct keys $x \ne y$ of $\{0, \ldots, p - 1\}$, $\Pr[h_{a,b,m}(x) = h_{a,b,m}(y)] \le 1/m$.

This is the universality of the Carter and Wegman family, proved in CLRS, Section 11.3 (fourth edition) and Section 11.3.3 (third edition). The model is the word RAM with $p < 2^w$, so each hash value costs $O(1)$.

**Lemma 1 (collisions).** Let $X \subseteq \{0, \ldots, p - 1\}$ have $k$ keys, let $h = h_{a,b,m}$ be random, and let $C$ be the number of unordered pairs $\{x, y\} \subseteq X$ with $x \ne y$ and $h(x) = h(y)$. Then $E[C] \le \binom{k}{2} / m$.

*Proof.* $C$ is the sum, over the $\binom{k}{2}$ pairs, of the indicator of the event $h(x) = h(y)$. By (U), each indicator has expectation at most $1/m$. By linearity of expectation, $E[C] \le \binom{k}{2}/m$. $\square$

**Lemma 2 (sum of squares).** If the buckets of $h$ on $X$ have sizes $k_0, \ldots, k_{m-1}$, then $\sum_j k_j^2 = k + 2C$.

*Proof.* For each integer $t \ge 0$, $t^2 = t + 2 \binom{t}{2}$. Bucket $j$ contains $\binom{k_j}{2}$ colliding pairs, and each colliding pair lies in exactly one bucket, so $C = \sum_j \binom{k_j}{2}$. Summing $k_j^2 = k_j + 2\binom{k_j}{2}$ over $j$ and using $\sum_j k_j = k$ gives the claim. $\square$

**Claim 1 (first level).** One trial of lines L3 to L5 succeeds with probability more than $1/2$.

*Proof.* If $n = 0$, the sum is $0 \le 0$ and the trial succeeds. Let $n \ge 1$, so $m = n$. By Lemmas 1 and 2, $E[\sum_j n_j^2] = n + 2E[C] \le n + 2 \binom{n}{2}/n = n + (n - 1) = 2n - 1$. The sum is a non-negative random variable, so by Markov's inequality $\Pr[\sum_j n_j^2 > 4n] \le \Pr[\sum_j n_j^2 \ge 4n] \le (2n - 1)/(4n) < 1/2$. $\square$

**Claim 2 (second level).** For a bucket with $n_j \ge 1$ keys and $m_j = n_j^2$, one trial of lines L9 and L10 succeeds with probability more than $1/2$.

*Proof.* If $n_j = 1$, there is no pair and each trial succeeds. Let $n_j \ge 2$, and let $C_j$ be the number of colliding pairs of $S_j$ under $h_j$. The choice of $h_j$ is independent of the choice of $h$, and $S_j$ is fixed once $h$ is fixed, so Lemma 1 applies to $X = S_j$: $E[C_j] \le \binom{n_j}{2}/n_j^2 = (n_j - 1)/(2 n_j) < 1/2$. $C_j$ is a non-negative integer, so by Markov's inequality $\Pr[C_j \ge 1] \le E[C_j] < 1/2$. The trial succeeds exactly when $C_j = 0$. $\square$

**Theorem (time and space).** FKS-BUILD runs in $O(n)$ expected time. The structure has at most $4n$ second-level slots and $O(n)$ words in total, in every run.

*Proof.* *Space.* The loop of lines L2 to L5 ends only when $\sum_j n_j^2 \le 4n$, and $\sum_j m_j = \sum_j n_j^2$. The first level stores $m = \max(n, 1)$ triples $(m_j, a_j, b_j)$ and the pair $(a, b)$. So the total is at most $4n + 3\max(n, 1) + 2 = O(n)$ words.

*Time of the first level.* A trial costs $O(n + m) = O(n + 1)$: one hash value for each key, and $m$ lists. By Claim 1 and the geometric distribution of the number of trials, the expected number of trials is less than 2. So the first level takes $O(n + 1)$ expected time.

*Time of the second level.* Condition on the accepted $h$, so that the sizes $n_j$ are fixed with $\sum_j n_j^2 \le 4n$. Bucket $j$ costs $O(1 + m_j)$ for line L7, and $O(n_j)$ for each trial of lines L9 and L10, since a trial writes at most $n_j$ slots and clears the ones it wrote. By Claim 2, the expected number of trials is less than 2. Line L11 costs $O(n_j)$. So the expected cost of bucket $j$ is $O(1 + m_j + n_j)$, and, by linearity of expectation, the second level costs $O(m + \sum_j m_j + n) = O(n + 1)$ in expectation, for each accepted $h$. Taking the expectation over $h$ keeps the bound.

Adding the two levels gives $O(n + 1)$ expected time, which is $O(n)$ for $n \ge 1$. $\blacksquare$

**Search.** FKS-SEARCH evaluates two hash functions and reads two arrays, so it takes $O(1)$ time in every case.
