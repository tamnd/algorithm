---
title: CHD-BUILD returns a perfect hash function, minimal when m = n, and ends with probability 1 for fully random hash functions
proves: [correctness, termination]
status: full
---

Let $S$ be a set of $n$ distinct keys, let $m \ge \max(n, 1)$, and let $r \ge 1$. For an index $\ell \in \{0, \ldots, m^2 - 1\}$ write $s_\ell(x) = (f_1(x) + \lfloor \ell/m \rfloor f_2(x) + (\ell \bmod m)) \bmod m$. Then CHD-EVAL$(x) = s_{\sigma[g(x)]}(x)$, by lines L12 and L13.

**Lemma 1 (invariant of the placement loop).** Fix one attempt, that is, one pass of lines L2 to L9 with fixed $g$, $f_1$ and $f_2$. After each bucket that line L9 places, the following holds. Let $P$ be the set of buckets placed so far. The slots $s_{\sigma[i]}(x)$, for $i \in P$ and $x \in B_i$, are pairwise distinct, and the used slots are exactly these slots.

*Proof.* By induction on the buckets in the order of line L5. Before the first one, $P$ is empty and line L4 marks all slots free. Suppose the claim holds for $P$, and line L9 places bucket $i$ with index $\ell$. The loop of line L7 stopped at $\ell < m^2$ (otherwise line L8 would have left the loop), so its condition was false: the slots $s_\ell(x)$, $x \in B_i$, are pairwise distinct and none of them is used. By the hypothesis, the used slots are those of the keys of $P$, so the new slots are also distinct from all of these. Line L9 sets $\sigma[i] = \ell$ and marks exactly the new slots, so the claim holds for $P \cup \{i\}$. An empty bucket is placed with $\ell = 0$ and adds no slot. $\square$

**Theorem 1 (the output is perfect).** If CHD-BUILD returns, then CHD-EVAL maps $U$ into $[m]$, is one to one on $S$, and, when $m = n$, maps $S$ onto $[n]$.

*Proof.* Each value is reduced mod $m$, so it is in $[m]$. CHD-BUILD returns only after an attempt in which line L8 never set ok to false, so every bucket was placed. The buckets $B_0, \ldots, B_{r-1}$ partition $S$, since each key lies in exactly the bucket $g(x)$. By Lemma 1 with $P = [r]$, the slots $s_{\sigma[g(x)]}(x)$ for $x \in S$ are pairwise distinct, and these are the values of CHD-EVAL. So CHD-EVAL is one to one on $S$. If $m = n$, its $n$ distinct values on $S$ lie in a set of $n$ elements, so they are all of $[n]$. $\square$

**Lemma 2 (a sufficient condition).** If $f_1$ is one to one on $S$, the attempt succeeds.

*Proof.* We show that every bucket is placed with $\ell = 0$, the first index that line L7 tests. For $\ell = 0$, $s_0(x) = f_1(x)$. When bucket $i$ comes, the values $f_1(x)$ for $x \in B_i$ are pairwise distinct. By Lemma 1 the used slots are the values $f_1(y)$ of the keys $y$ of the buckets already placed, all different from the keys of $B_i$, so none of them equals any $f_1(x)$, $x \in B_i$. So the condition of line L7 is false at $\ell = 0$. $\square$

**Theorem 2 (termination).** If each attempt draws $f_1$ uniformly from all functions $U \to [m]$, independently of the earlier attempts, then CHD-BUILD ends with probability 1, after at most $m^n (m - n)!/m!$ attempts in expectation.

*Proof.* Each attempt runs at most $r$ buckets with at most $m^2$ values of $\ell$ each, so it ends. By Lemma 2, it succeeds when $f_1$ is one to one on $S$, which happens with probability $q = m(m - 1) \cdots (m - n + 1)/m^n > 0$ since $m \ge n$. The attempts are independent, so the number of attempts is at most a geometric random variable with mean $1/q$, which is finite. $\square$

The bound of Theorem 2 is very weak; it only shows that the restart loop cannot run forever. The expected number of attempts in practice is close to 1, see the complexity proof. For the polynomials of degree 2 of the Python version, Theorem 1 still holds, since it does not depend on how the functions are chosen, but Theorem 2 is not proved.
