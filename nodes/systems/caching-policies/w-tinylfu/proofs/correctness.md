---
title: W-TinyLFU keeps its segment limits and admits by the TinyLFU rule
proves: [correctness]
status: full
---

We use the pseudocode of the page with a cache of $c \ge 2$ objects, a window limit $w$ with $1 \le w < c$, a main limit $m = c - w \ge 1$, and a protected limit $p = \lfloor 4m/5 \rfloor < m$. Write $V$ for the window, $B$ for probation and $P$ for protected. The invariants are:

- (I1) $|V| \le w$;
- (I2) $|P| \le p$;
- (I3) $|B| + |P| \le m$;
- (I4) $V$, $B$ and $P$ are pairwise disjoint, and no segment holds a key twice.

Together (I1) and (I3) give $|V| + |B| + |P| \le c$.

**Lemma 1 (a victim exists).** If (I2) and (I3) hold and line L12 runs, then $B$ is not empty.

*Proof.* Line L12 runs only when line L11 finds $|B| + |P| \ge m$, so $|B| + |P| = m$ by (I3). By (I2), $|P| \le p < m$, so $|B| \ge 1$. $\square$

**Theorem.** (I1) to (I4) hold after every request. A request is a hit if and only if its object was in $V \cup B \cup P$ before the request. On a miss that overflows the window when the main cache is full, the window victim $u$ replaces the probation victim $v$ exactly when $\mathrm{EST}(u) > \mathrm{EST}(v)$, and otherwise $u$ leaves the cache.

*Proof.* By induction on the requests; all hold for empty segments. Assume they hold before a request for $x$. Line L1 changes only the filter.

*Hit in $V$ or $P$ (lines L2 and L3).* Only the order inside one segment changes.

*Hit in $B$ (lines L4 to L7).* Line L5 moves $x$ from $B$ to $P$, so $|B| + |P|$ does not change and the segments stay disjoint. Now $|P| \le p + 1$. If $|P| = p + 1$, line L6 moves one object from $P$ to $B$, so $|P| \le p$ and $|B| + |P|$ is still the same. So (I2) to (I4) hold.

*Miss (lines L8 to L15).* By (I4), $x$ is in no segment, so after line L8 the segments are still disjoint and $|V| \le w + 1$. If $|V| \le w$, nothing more happens. Otherwise line L10 removes $u$ from $V$, so $|V| = w$ again, which is (I1). If $|B| + |P| < m$, line L11 puts $u$ in $B$, and then $|B| + |P| \le m$. Otherwise, by Lemma 1, line L12 finds $v$ in $B$. On line L13, if $\mathrm{EST}(u) > \mathrm{EST}(v)$ then $v$ leaves and $u$ enters $B$, so $|B|$ does not change. Else, on line L14, $u$ leaves the cache. In every case $|P|$ does not change, and $u$ was removed from $V$ before it entered $B$, so (I2) to (I4) hold.

The hit test on lines L2 to L4 looks at exactly the three segments, which hold all cached objects. $\blacksquare$

**Consequences.**

1. *A new object always gets a place.* Every missed object enters the window on line L8, whatever its estimate. So a burst of requests to a new object hits in the window while the object is among the $w$ most recent new objects, even if its count is low.
2. *The filter guards only the main cache.* Only line L13 reads the filter, and only for a window victim and the probation victim.
3. *Cost.* Lines L2 to L15 each do $O(1)$ work on hash tables and linked lists, plus at most two calls of EST, so a request costs $O(d)$ besides the amortized cost of a reset.

**The test file.** It checks the hit sequence against a separate list-based version of the pseudocode on seeded random traces, checks (I1) to (I4) after every request, checks the default sizes for $c = 1000$ and $c = 50$, checks every duel and segment of the worked example, and checks that short bursts of requests to new keys hit in the window while protected stays full of hot keys.
