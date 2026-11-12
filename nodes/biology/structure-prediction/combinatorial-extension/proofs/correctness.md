---
title: The path that CE returns is a valid path, it is the longest of the greedy paths, and the search stops
proves: [correctness]
status: full
---

CE with the "best" strategy is a heuristic, so the claim is not that it finds the longest path that the criteria allow. The claim is about what it returns. We use the notation of the page: an AFP $p = (p^A, p^B)$ matches residues $p^A, \ldots, p^A + m - 1$ of $A$ with $p^B, \ldots, p^B + m - 1$ of $B$; $D_{pq}$ is the distance of eq. (6) for $p \ne q$ and the self-distance of eq. (7) for $p = q$; $P$ is the set of line L2.

A path $(p_1, \ldots, p_k)$ is valid if (a) each $p_t$ is in $P$, that is, $D_{p_t p_t} < D_0$; (b) for each $t < k$, the gaps $g^A = p^A_{t+1} - p^A_t - m$ and $g^B = p^B_{t+1} - p^B_t - m$ satisfy $g^A, g^B \ge 0$, $\min(g^A, g^B) = 0$ and $\max(g^A, g^B) \le G$, which are the conditions (1) to (5); (c) for each $t < k$, $\frac{1}{t} \sum_{s \le t} D_{p_s p_{t+1}} < D_1$, criterion (10); and (d) for each $t < k$, $\frac{1}{(t+1)^2} \sum_{s \le t+1} \sum_{u \le t+1} D_{p_s p_u} < D_1$, criterion (11). Each prefix of a valid path is valid. For a start $p \in P$, the greedy path $\Gamma(p)$ is the path that lines L6 to L12 build from $p$.

**Claim.** (1) CE terminates. (2) If $P$ is empty, it returns the empty path. Otherwise it returns a valid path $\Gamma(p)$ for some $p \in P$, and (3) its length is $\max_{p \in P} |\Gamma(p)|$.

**Lemma 1 (symmetry).** $D_{pq} = D_{qp}$.

*Proof.* Eq. (6) is a mean of terms $|d^A(p^A + x, q^A + y) - d^B(p^B + x, q^B + y)|$ over the offset pairs $(x, y) \in \{(0, 0), (m - 1, m - 1)\} \cup \{(k, m - 1 - k) : 1 \le k \le m - 2\}$. This set is closed under $(x, y) \mapsto (y, x)$: the first two pairs are fixed, and $(k, m - 1 - k)$ goes to $(k', m - 1 - k')$ with $k' = m - 1 - k$, again in $1..m-2$. Distance matrices are symmetric, so swapping $p$ and $q$ permutes the terms. $\square$

**Lemma 2 (the running sum).** At each test of line L11, the variable $T$ equals $\sum_{s, u \le k} D_{p_s p_u}$ for the current path $(p_1, \ldots, p_k)$, and the value tested is the mean of criterion (11) for the path with $q$ appended.

*Proof.* At line L6, $T = D_{p_1 p_1}$, the sum for $k = 1$. Appending $q$ adds the terms $D_{p_s q}$ and $D_{q p_s}$ for $s \le k$, and $D_{qq}$. By Lemma 1 the first two groups have the same sum, the value $c = \sum_{s \le k} D_{p_s q}$ that line L8 computed. So the sum for the longer path is $T + 2c + D_{qq}$, which is the value tested and, after line L12, the new $T$. $\square$

**Lemma 3 (each greedy path is valid).** $\Gamma(p)$ is valid for each $p \in P$.

*Proof.* By induction on the length. The path $(p)$ is valid since $p \in P$. Suppose the current path is valid and line L12 appends $q$. Line L8 takes $q$ from the successors of the last AFP, which are exactly the AFPs that fit in both chains and satisfy (b), and keeps only those in $P$, so (a), and those whose mean in (10) is below $D_1$, so (c). Line L12 is reached only if the test of line L11 failed, and by Lemma 2 that test is criterion (11) for the longer path, so (d). The conditions for the earlier steps hold by the hypothesis. $\square$

**Lemma 4 (the bound of line L5).** Each valid path that starts at $p$ has at most $\beta(p) = 1 + \min(\lfloor (n - m - p^A)/m \rfloor, \lfloor (r - m - p^B)/m \rfloor)$ AFPs, where $n = |A|$ and $r = |B|$.

*Proof.* Along a valid path, $p^A_{t+1} \ge p^A_t + m$ by (b), so $p^A_k \ge p^A + (k - 1) m$. The last AFP must fit in $A$, $p^A_k + m \le n$, so $(k - 1) m \le n - m - p^A$. The same holds for $B$. Since $k$ is an integer, $k \le \beta(p)$. $\square$

**Proof of (1).** Line L2 and the loop of line L4 are finite. In the loop of line L7, each pass either leaves the loop or appends an AFP whose first coordinate is at least $m \ge 1$ larger than the last one; the coordinates are below $n$, so there are at most $n$ passes. Each pass looks at finitely many successors. $\square$

**Proof of (2) and (3).** If $P$ is empty, line L4 does not run and line L14 returns the initial empty path. Otherwise, $best$ changes only at line L13, to a path $\Gamma(p)$, so the returned path is a greedy path and it is valid by Lemma 3. The first start is not skipped, since $\beta(p) \ge 1 > 0$, so the result is not empty.

For (3), let $\ell$ be the final length of $best$, which never decreases. For each start $p$ that line L5 skips, $|\Gamma(p)| \le \beta(p)$ by Lemmas 3 and 4, and $\beta(p) \le |best| \le \ell$ at that time. For each start that runs, line L13 makes $|best| \ge |\Gamma(p)|$. So $|\Gamma(p)| \le \ell$ for each $p \in P$, and $\ell$ is the length of one of them. Hence $\ell = \max_{p \in P} |\Gamma(p)|$. $\blacksquare$

**Remark.** The longest valid path can be longer than each greedy path: line L10 commits to the candidate of least mean in (10), and a candidate of larger mean can allow a longer path later. The "all" strategy of the paper searches every extension, and the tests compare both strategies with a plain enumeration of the valid paths on small inputs. Validity is about the criteria of the paper; it does not say that the residues of the path correspond in a biological sense.
