---
title: Floyd-Rivest selection returns the k-th smallest item and stops
proves: [correctness, termination]
status: full
---

For a list $S$ of $n$ items and $1 \le k \le n$, write $\operatorname{sel}(S, k)$ for the $k$-th entry of a sorted order of $S$; all sorted orders have the same entries, so it is well defined.

**Claim.** For each list $S$ with $n \ge 1$ items, each $k$ with $1 \le k \le n$, and each outcome of the random draws, FR-SELECT$(S, k)$ stops and returns $\operatorname{sel}(S, k)$.

**Lemma (split by two pivots).** Let $u \le v$ be items, and let $L$, $M$ and $G$ be the items of $S$ that are less than $u$, in $[u, v]$, and greater than $v$. Then

$$ \operatorname{sel}(S, k) = \begin{cases} \operatorname{sel}(L, k) & \text{if } k \le |L|, \\ \operatorname{sel}(M, k - |L|) & \text{if } |L| < k \le |L| + |M|, \\ \operatorname{sel}(G, k - |L| - |M|) & \text{if } k > |L| + |M|. \end{cases} $$

*Proof.* The order is total, so each item is in exactly one part. Each item of $L$ is less than $u$, which is at most each item of $M$, and each item of $M$ is at most $v$, which is less than each item of $G$. So the list "sorted $L$, sorted $M$, sorted $G$" is a sorted order of $S$, and its entry $k$ is the entry named in the case. $\square$

**Lines L7 and L8 build these parts.** In line L7, an item goes to $G$ if $x > v$; otherwise $x \le v$, and it goes to $L$ if $x < u$, and to $M$ if $u \le x \le v$. Line L8 tests $x < u$ first and $x > v$ second; since $u \le v$, an item with $x < u$ is not greater than $v$, so again each item goes to the part the lemma names.

**Proof of the claim.** By strong induction on $n$. Assume the claim for all lists with fewer than $n$ items.

1. *Line L1.* If $n \le c$, sorting returns $\operatorname{sel}(S, k)$ by definition.
2. *Lines L2 to L5.* Now $n > c \ge 2$, so $m = \min(n - 1, \lceil n^{2/3} \rceil)$ satisfies $1 \le m \le n - 1$, and $R$ is a list of $m$ items of $S$. Line L4 gives $1 \le lo \le hi \le m$: the lower end is at least $1$ by the max, the upper end is at most $m$ by the min, and $\lfloor km/n - g \rfloor \le \lceil km/n + g \rceil$ with $1 \le \lceil km/n + g \rceil$ since $km/n > 0$, and $\lfloor km/n - g \rfloor \le m$ since $k \le n$. By the hypothesis for $m < n$, line L5 returns $u = \operatorname{sel}(R, lo)$ and $v = \operatorname{sel}(R, hi)$, and $u \le v$ because $lo \le hi$. Both are items of $S$.
3. *Lines L9 and L10.* $u$ is in $S$ and is not less than itself, so $u \notin L$ and $|L| \le n - 1$; likewise $v \notin G$ and $|G| \le n - 1$. If $k \le |L|$, the call of line L9 has $1 \le k \le |L| < n$, and by the hypothesis and the lemma it returns $\operatorname{sel}(S, k)$. If $k > |L| + |M|$, then $1 \le k - |L| - |M| \le n - |L| - |M| = |G| < n$, and the same argument applies to line L10.
4. *Lines L11 and L12.* Otherwise $|L| < k \le |L| + |M|$, so $1 \le k - |L| \le |M|$. If $|M| = n$, line L11 returns $\operatorname{sel}(S, k)$ by sorting. If $|M| < n$, line L12 calls FR-SELECT$(M, k - |L|)$ on a shorter list, which by the hypothesis returns $\operatorname{sel}(M, k - |L|)$, which is $\operatorname{sel}(S, k)$ by the lemma.

Each case either returns directly or makes recursive calls on lists with fewer than $n$ items, each of which stops by the hypothesis, so the call stops and returns $\operatorname{sel}(S, k)$. The proof uses no property of the sample except that $R$ is a list of $m$ items of $S$, so it holds for every outcome of the draws. $\blacksquare$
