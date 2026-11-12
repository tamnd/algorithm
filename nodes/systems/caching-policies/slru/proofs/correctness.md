---
title: SLRU keeps disjoint segments within their sizes, always has a victim, is LRU when p is 0, and is not competitive when p is at least 1
proves: [correctness]
status: full
---

We use the pseudocode of the page, a cache of capacity $k \ge 1$, a protected size $0 \le p < k$, both segments empty at the start, and a request sequence $\sigma_1 \ldots \sigma_n$. The resident pages are $R = PROB \cup PROT$.

**Invariant.** After each request:

1. $PROB$ and $PROT$ are disjoint;
2. $|PROT| \le p$;
3. $|R| = |PROB| + |PROT| \le k$;
4. the requested page is in $R$.

*Proof.* By induction on the requests. The empty segments satisfy parts 1 to 3.

*Lines L1 and L2.* The page $x$ is in $PROT$ and moves inside it. No set changes, so parts 1 to 3 hold, and $x \in R$.

*Lines L3 to L7.* The page $x$ leaves $PROB$ and joins $PROT$, so the segments stay disjoint and $|R|$ does not change. Now $|PROT|$ is at most $p + 1$. If it is $p + 1$, line L6 moves one page $y$ from $PROT$ to $PROB$; $y$ was in $PROT$ only, so the segments stay disjoint, $|PROT| = p$ and $|R|$ does not change. The page $y$ is not $x$: $x$ is at the MRU end of $PROT$, and $y$ is at the LRU end, and $|PROT| = p + 1 \ge 2$ when $p \ge 1$. When $p = 0$, $y = x$, and $x$ moves to $PROB$, which is still resident. In all cases $x \in R$.

*Lines L8 to L11.* The page $x$ is not resident. If $|R| = k$, then $|PROB| = k - |PROT| \ge k - p \ge 1$ by part 2, so the LRU page of $PROB$ exists, and line L9 evicts it; then $|R| = k - 1$. Line L10 adds $x$ to $PROB$ only, so the segments stay disjoint, $|R| \le k$ and $x \in R$. $\square$

The tests check parts 1 to 4 after each request, and compare the code with a direct version on Python lists on random traces and random values of $k$ and $p$.

**Claim (LRU as a special case).** If $p = 0$, SLRU has the same hits, misses and victims as LRU with $k$ pages.

*Proof.* We show by induction that $PROT$ is empty after each request and that $PROB$, read from its MRU end, is the LRU list of the same requests. At the start both are empty. Line L1 never applies, because $PROT$ is empty. On a hit, lines L4 to L6 put $x$ in $PROT$, find $|PROT| = 1 > 0$, and move $x$ to the MRU end of $PROB$. So $x$ goes from its place in $PROB$ to the MRU end, and $PROT$ is empty again. This is the LRU rule for a hit. On a miss, $|R| = |PROB|$, so a full cache evicts the LRU page of $PROB$, and $x$ enters at the MRU end. This is the LRU rule for a miss. $\square$

**Claim (not competitive).** For $k = 2$ and $p = 1$, the sequence $\sigma_m = a, a, (x, y)^m$ costs SLRU $1 + 2m$ misses, and an optimal offline algorithm 3 misses. So no constant $c$ and $b$ give $\text{SLRU}(\sigma) \le c \cdot \text{OPT}(\sigma) + b$ for all $\sigma$.

*Proof.* The first $a$ misses and enters $PROB$. The second $a$ hits and moves $a$ to $PROT$, which now holds $p = 1$ page. From then on, $a$ stays in $PROT$, since only a hit in $PROB$ changes $PROT$, and no request after that is a hit in $PROB$: $PROB$ has $k - 1 = 1$ slot, and each of $x$ and $y$ is requested right after the other, so each request finds the other page in that slot, evicts it, and misses. So all $2m$ requests to $x$ and $y$ miss, for $1 + 2m$ misses. An offline algorithm misses on $a$, on the first $x$ and on the first $y$, evicting $a$ at that time, and then hits on all other requests: 3 misses. $\square$

The same idea works for any $k$ and $1 \le p < k$. Make $p$ pages protected with two requests each, then cycle through $k - p + 1$ new pages. Each of them misses, while an offline algorithm with $k$ slots keeps them all after $p$ evictions. The tests check the case $k = 2$, $p = 1$ against Belady MIN for $m = 10, 40, 160$.

**Scan resistance.** Assume that after some request $PROT = P$, and that from then on each request is to a page that is not resident. Each such request takes lines L8 to L11, which change only $PROB$. So $PROT = P$ for as long as the scan lasts, whatever its length. The tests check this with $k = 8$, $p = 4$ and a scan of 200 new pages.

**Cost.** Each segment is a hash map with a doubly linked list. Membership, removal, insertion at the MRU end and removal at the LRU end take $O(1)$ expected time, and each request runs a constant number of these steps. The space is $\Theta(k)$.
