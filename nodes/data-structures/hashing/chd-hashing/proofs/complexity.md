---
title: CHD evaluates in O(1) time, uses O(n) words, and builds in O(n) expected time in an idealized model
proves: [time.expected, space.extra]
status: sketch
---

The model is the word RAM, with keys and hash values of $O(1)$ words. Let $\lambda = n/r$ be the average bucket size and $\alpha = n/m$ the load.

**Claim 1 (evaluation).** CHD-EVAL takes $O(1)$ time in the worst case.

*Proof.* Lines L12 and L13 compute $g$, $f_1$ and $f_2$ once each, read $\sigma[i]$, and do one division, one multiplication, two additions and one reduction. With $\sigma$ stored as a plain array, the read is one memory access. $\square$

**Claim 2 (plain space).** The function takes $r + O(1)$ words: the array $\sigma$ of $r = \lceil n/\lambda \rceil$ entries, each less than $m^2$, and the descriptions of $g$, $f_1$ and $f_2$. For a constant $\lambda$ this is $O(n)$ words. The build uses $O(n + m + r)$ more words for the buckets and the marks of the slots. $\square$

**Lemma 3 (cost of one attempt).** One attempt of lines L2 to L9 takes $O(n + m + r + \sum_i |B_i| \, t_i)$ time, where $t_i$ is the number of indices that line L7 tests for bucket $i$.

*Proof.* Line L3 takes $O(n + r)$ time. Line L4 takes $O(m)$. The order of line L5 is a sort of $r$ sizes between 0 and $n$, which counting sort does in $O(n + r)$. One test of line L7 computes $|B_i|$ slots, and checks that they are free and distinct in $O(|B_i|)$ time: it puts a temporary mark on each slot, stops at a slot that is used or already marked, and then removes the temporary marks. Line L9 takes $O(|B_i| + 1)$. Summing over the buckets gives the claim. $\square$

**Lemma 4 (expected trials, idealized model).** Assume that $g$ is fully random, and that for each bucket the slot vectors $(s_\ell(x))_{x \in B_i}$ for $\ell = 0, 1, 2, \ldots$ are independent, each with independent uniform entries in $[m]$, and independent of everything that happens before the bucket is placed. Let $\alpha \le \alpha_0 < 1$ for a constant $\alpha_0$, and ignore the cap $\ell < m^2$. Then $E[\sum_i |B_i| \, t_i] \le n c \, e^{\lambda (c - 1)}$, where $c = 1/(1 - \alpha_0)$.

*Proof.* Consider bucket $i$ with $k = |B_i| \ge 1$ keys, and let $u$ be the number of used slots when it is placed. The buckets not yet placed hold at least the $k$ keys of $B_i$, so $u \le n - k$. A test succeeds when $k$ independent uniform slots are distinct and free, which has probability

$$\frac{(m - u)(m - u - 1) \cdots (m - u - k + 1)}{m^k} \ge \Big( \frac{m - n + 1}{m} \Big)^k \ge (1 - \alpha_0)^k,$$

since each factor is at least $m - u - k + 1 \ge m - n + 1$. The tests are independent, so $t_i$ is geometric and $E[t_i \mid g] \le c^k$. So $E[\sum_i |B_i| t_i \mid g] \le \sum_i |B_i| c^{|B_i|}$. For fully random $g$, each $|B_i|$ is binomial with $n$ trials and success probability $1/r$, and for such a $K$, $E[K c^K] = (n/r) \, c \, (1 + (c - 1)/r)^{n - 1} \le \lambda c \, e^{(c - 1) n / r}$. Summing over the $r$ buckets gives $r \lambda c \, e^{\lambda (c - 1)} = n c \, e^{\lambda (c - 1)}$. $\square$

For constant $\lambda$ and $\alpha_0$, Lemmas 3 and 4 give $O(n + m) = O(n)$ expected time for one attempt in the idealized model. An attempt fails only if some bucket needs more than $m^2$ tests, which by Markov's inequality has probability at most $n c \, e^{\lambda(c - 1)} / m^2$, less than $1/2$ once $m$ is large enough. Then the expected number of attempts is at most 2, and the expected build time is $O(n)$.

**What is a sketch here.** Three steps are not proved on this page.

1. *The idealized model.* The real slot vectors $s_\ell$ for different $\ell$ are built from the same values $f_1(x)$ and $f_2(x)$, so they are not independent: the indices with the same $d_0$ are cyclic shifts of each other. The analysis of Belazzougui, Botelho and Dietzfelbinger (ESA 2009, LNCS 5757, pages 682 to 693) treats the hash functions as fully random and analyzes the scheme with its own assumptions; we do not reproduce it. The bound of Lemma 4 also grows like $e^{\lambda \alpha_0/(1 - \alpha_0)}$ and does not use the order of line L5; the paper's analysis of the placement in order of decreasing size gives much better constants.
2. *The compressed space.* The statement that the compressed $\sigma$ takes about 2 bits for each key, close to the lower bound for perfect hash functions, is from the same paper (its abstract gives about 1.4 bits for each key for $m = 1.23n$ and about 1.98 bits for $m = 1.01n$), together with the $O(1)$ access time of its compressed code.
3. *The minimal case $m = n$.* Lemma 4 needs $\alpha_0 < 1$. With $m = n$, the last buckets are placed in a table with very few free slots; a bucket of one key still always fits within $m$ tests, by the index $\ell = (t - f_1(x)) \bmod m$ for a free slot $t$, but no bound for buckets of two or more keys is proved here.
