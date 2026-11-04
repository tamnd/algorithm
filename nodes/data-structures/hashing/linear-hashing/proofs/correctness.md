---
title: Linear hashing keeps its invariant and answers each operation correctly
proves: [correctness, termination]
status: full
---

We use the names of the page: $N \ge 1$, $\alpha_{\max} > 0$, $0 \le \alpha_{\min} \le \alpha_{\max} / 2$, the level $L$, the pointer $p$, the number of pairs $n$, the array of $B$ lists, and $M = N 2^L$. For a pair $(L, p)$ we write

$$\mathrm{addr}_{L,p}(k) = \begin{cases} h(k) \bmod M & \text{if } h(k) \bmod M \ge p, \\ h(k) \bmod 2M & \text{if } h(k) \bmod M < p. \end{cases}$$

This is the value of ADDRESS (lines L1 to L3). We call $(L, p)$ *extended valid* if $L \ge 0$, $0 \le p \le M$ and $B = M + p$. It is *valid* if also $p < M$; this is (I1).

**Lemma 1 (the address is a bucket).** If $(L, p)$ is extended valid, then $0 \le \mathrm{addr}_{L,p}(k) < B$ for every key $k$. Moreover $\mathrm{addr}_{L,p}(k) = j$ implies $h(k) \bmod M = j \bmod M$.

*Proof.* Let $r = h(k) \bmod M$. If $r \ge p$, the address is $r$ with $p \le r < M \le B$. If $r < p$, the address $a = h(k) \bmod 2M$ satisfies $a \bmod M = r$, because $M$ divides $2M$; so $a = r$ or $a = r + M$, and both are less than $p + M = B$. In both cases $a \bmod M = r$. $\square$

**Lemma 2 (end of a round).** If $p = M$, then $(L, M)$ and $(L + 1, 0)$ give the same $B$ and the same address for every key.

*Proof.* $B = M + M = 2M = 2M + 0$. Under $(L, M)$ every $r = h(k) \bmod M$ is less than $p = M$, so the address is $h(k) \bmod 2M$. Under $(L + 1, 0)$ the small table has size $2M$ and every value is at least $p = 0$, so the address is again $h(k) \bmod 2M$. $\square$

**Lemma 3 (SPLIT).** Assume (I1), (I2) and (I3) before SPLIT. Then after SPLIT, (I1), (I2) and (I3) hold, $n$ is the same, and $B$ is one larger.

*Proof.* Let $L, p, M, B = M + p$ be the values before. Line L11 adds the list with index $B = p + M$. Consider a pair $(k, v)$ in the old list $\mathit{bucket}[p]$. By (I2), $\mathrm{addr}_{L,p}(k) = p$, so by Lemma 1, $h(k) \bmod M = p$. Then $h(k) \bmod 2M$ is $p$ or $p + M$, and line L14 puts the pair in that list, which exists after line L11. Lines L12 to L14 move only the pairs of $\mathit{bucket}[p]$ and keep each of them, so (I3) holds and $n$ does not change.

Line L15 sets $p' = p + 1 \le M$, and $(L, p')$ is extended valid with $B + 1 = M + p'$. We show that each pair is in the list $\mathrm{addr}_{L,p'}(k)$. Let $r = h(k) \bmod M$.

- If $r = p$, the pair came from the old $\mathit{bucket}[p]$, because by (I2) and Lemma 1 every pair with $r = p$ was in the list $p$ (its old address was $r = p$, since $r \ge p$). Now $r < p'$, so its new address is $h(k) \bmod 2M$, which is the list of line L14.
- If $r > p$, then $r \ge p'$, and both the old and the new address are $r$. The pair did not move.
- If $r < p$, then $r < p'$, and both addresses are $h(k) \bmod 2M$. The pair did not move.

If $p' < M$, line L16 does nothing and $(L, p')$ is valid. If $p' = M$, line L16 sets $(L + 1, 0)$, which is valid because $0 < 2M$, and by Lemma 2 neither $B$ nor any address changes. So (I1) and (I2) hold. $\square$

**Lemma 4 (MERGE).** Assume (I1), (I2), (I3) and $B > N$ before MERGE. Then after MERGE, (I1), (I2) and (I3) hold, $n$ is the same, and $B$ is one smaller.

*Proof.* First, line M1. If $p = 0$, then $B = M = N 2^L > N$, so $L \ge 1$. Line M1 sets $L' = L - 1$ and $p' = N 2^{L'} = M / 2$. The pair $(L', p')$ is extended valid with $p' = N 2^{L'}$, and by Lemma 2 applied to it, it has the same $B$ and the same addresses as $(L, 0)$. So after line M1 we have an extended valid state with $1 \le p \le M$, for its own $M$, in which (I2) and (I3) hold. If $p \ge 1$ at the start, the same is true without a change.

Now let $q = p - 1$, so $0 \le q < M$, and the last list has index $B - 1 = M + q$. By Lemma 1, each pair in the list $M + q$ and each pair in the list $q$ has $h(k) \bmod M = q$. Line M2 sets the pointer to $q$. Let $r = h(k) \bmod M$ for a pair $(k, v)$.

- If $r = q$, the pair was in the list $q$ or in the list $M + q$, since its old address was $h(k) \bmod 2M$, which is one of these two. Its new address is $r = q$, because now $r \ge q$. Line M3 moves the pairs of the list $M + q$ to the list $q$, so the pair is in the list $q$.
- If $r > q$, then $r \ge p$ (the old pointer), and both the old and the new address are $r$.
- If $r < q$, both the old and the new address are $h(k) \bmod 2M$.

After line M3 the list $M + q$ is empty, and line M4 removes it. Now $B = M + q$ with $0 \le q < M$, so (I1) holds, and (I2) holds by the three cases. Line M3 moves pairs without loss or copy, so (I3) holds and $n$ does not change. $\square$

**Theorem.** NEW makes a state that satisfies (I1) to (I4). If (I1) to (I4) hold before an operation, then SEARCH, INSERT and DELETE terminate, return the value that the abstract type asks for, and leave a state that satisfies (I1) to (I4) and represents the new map.

*Proof.*

*NEW.* $L = 0$, $p = 0 < N = M$, and $B = N$, so (I1) holds. There are no pairs and $n = 0$, so (I2), (I3) and (I4) hold.

*SEARCH$(k)$.* By (I2), a pair with key $k$ can only be in the list $\mathrm{addr}(k)$, which exists by Lemma 1, and by (I3) there is at most one such pair. Lines L4 to L6 scan this list, which is finite, and return its value or NIL. The state does not change.

*INSERT$(k, v)$.* If $k$ is present, its pair is in the list $a$ of line L7 by (I2), and line L8 replaces its value. The keys, $n$ and $B$ do not change, so (I1) to (I4) hold, and the map now sends $k$ to $v$. Otherwise line L9 appends $(k, v)$ to the list $\mathrm{addr}(k)$, so (I2) holds for the new pair, (I3) holds with $n + 1$, and (I1) is unchanged. By Lemma 3, each SPLIT of line L10 keeps (I1) to (I3) and $n$, and makes $B$ one larger. So the loop ends after at most $\lceil n / \alpha_{\max} \rceil$ steps, which is a finite number, and at the end $n \le \alpha_{\max} B$, which is (I4).

*DELETE$(k)$.* By (I2) and (I3), lines D1 and D2 find the pair of $k$ exactly when $k$ is present; if it is absent, nothing changes and the result is false. Otherwise line D3 removes the pair and sets $n$ to $n - 1$; (I1) to (I3) hold, and (I4) holds because $n$ decreased. Each step of the loop of line D4 runs with $B > N$, so Lemma 4 applies: (I1) to (I3) stay true and $B$ drops by 1. The loop ends after at most $B - N$ steps. For (I4): a step runs only when $n < \alpha_{\min} B$, with $B \ge 2$ because $B > N \ge 1$. Then after the step

$$n < \alpha_{\min} B \le \frac{\alpha_{\max}}{2} B \le \alpha_{\max} (B - 1),$$

where the last inequality is $B \le 2(B - 1)$, true for $B \ge 2$. So (I4) holds for the new size $B - 1$. The result is true, and the map no longer has $k$.

In each case the set of pairs is exactly the new map, by (I3) and the description of each step. $\blacksquare$
