---
title: ARC is a cache of c pages inside DBL(2c)
proves: [correctness]
status: full
---

We use the pseudocode of the page with cache size $c \ge 1$. All four lists start empty and $p = 0$. Write $A \cdot B$ for list $A$ followed by list $B$, and write every list LRU first.

**The policy DBL($2c$).** It keeps two LRU lists, $L_1$ and $L_2$. On a request for $x$:

1. If $x \in L_1 \cup L_2$, move $x$ to the MRU end of $L_2$.
2. Else, if $|L_1| = c$, delete the LRU page of $L_1$. Else, if $|L_1| + |L_2| = 2c$, delete the LRU page of $L_2$. Then put $x$ at the MRU end of $L_1$.

So $|L_1| \le c$ and $|L_1| + |L_2| \le 2c$ always hold. Both lists are in order of the time of the last request, because every request puts its page at an MRU end.

**Claim.** Run ARC and DBL($2c$) on the same trace. After every request:

- (a) $B_1 \cdot T_1 = L_1$ and $B_2 \cdot T_2 = L_2$, as lists;
- (b) $|T_1| + |T_2| = \min(c, |L_1| + |L_2|)$;
- (c) $0 \le p \le c$.

*Proof.* By induction on the number of requests. At the start all lists are empty and $p = 0$. Assume (a), (b) and (c) before a request for $x$. Note two facts. First, by (b), if $B_1 \cup B_2$ is not empty then $|L_1| + |L_2| > |T_1| + |T_2|$, so $|T_1| + |T_2| = c$. Second, the clamps on lines L5 and L10 keep (c).

*REPLACE is well defined and keeps (a).* REPLACE is only called when $|T_1| + |T_2| = c$; we check this for each call below. If line L27 picks $T_1$, then $|T_1| \ge 1$. If it picks $T_2$, suppose $T_2$ is empty. Then $|T_1| = c \ge p$, so the test failed only because $|T_1| = p = c$ and $x \notin B_2$. REPLACE is called from Case II, IV(A) with $|T_1| < c$, or IV(B). In Case II, $x \in B_1$, so $|L_1| \ge |T_1| + 1 = c + 1$, which is false. In Case IV(B), $|L_1| < c$, so $|T_1| < c$. Both are contradictions, so the picked list is not empty. Moving the LRU page of $T_i$ to the MRU end of $B_i$ moves the boundary inside $B_i \cdot T_i$ by one place and does not change the list $B_i \cdot T_i$. So (a) still holds, and $|T_1| + |T_2|$ drops by one.

*Case I, $x \in T_1 \cup T_2$.* Then $x \in L_1 \cup L_2$, and DBL moves $x$ to the MRU end of $L_2$. ARC moves $x$ to the MRU end of $T_2$, which is the MRU end of $B_2 \cdot T_2$. Removing $x$ from $T_1$ removes it from $B_1 \cdot T_1$ at the same place. So (a) holds, and no size in (b) changes.

*Case II, $x \in B_1$.* Then $x \in L_1$, and DBL moves $x$ to the MRU end of $L_2$. Since $B_1$ is not empty, $|T_1| + |T_2| = c$, so REPLACE may be called. It keeps (a). Then ARC moves $x$ from $B_1$ to the MRU end of $T_2$, which matches DBL. The cache size goes from $c$ to $c - 1$ to $c$, and $|L_1| + |L_2|$ does not change and is more than $c$. So (b) holds.

*Case III, $x \in B_2$.* The same as Case II with the indices swapped.

*Case IV, $x$ is not in the directory.* Then $x \notin L_1 \cup L_2$, and DBL takes its second branch.

- IV(A), $|T_1| + |B_1| = c$, that is, $|L_1| = c$. DBL deletes the LRU page of $L_1$. If $|T_1| < c$, then $B_1$ is not empty, the LRU page of $L_1$ is the LRU key of $B_1$, and line L16 deletes it. Since $B_1$ was not empty, the cache was full, so REPLACE may be called. After it and line L25, the cache size is $c$ again, and $|L_1| + |L_2| \ge |L_1| = c$. If $|T_1| = c$, then $B_1$ is empty, the LRU page of $L_1$ is the LRU page of $T_1$, and line L19 deletes it. The cache size stays $c$ after line L25.
- IV(B), $|L_1| < c$. If $|L_1| + |L_2| = 2c$, DBL deletes the LRU page of $L_2$. In that case $|L_2| > c \ge |T_2|$, so $B_2$ is not empty, and the LRU page of $L_2$ is the LRU key of $B_2$, which line L23 deletes. If $|L_1| + |L_2| \ge c$ before the request, then by (b) the cache is full, so REPLACE may be called, and after line L25 the cache size is $c$ with $|L_1| + |L_2| \ge c$ after the request. If $|L_1| + |L_2| < c$, then by (b) both ghost lists are empty, nothing is evicted, and line L25 makes both sides of (b) grow by one.

In all cases line L25 puts $x$ at the MRU end of $T_1$, which is the MRU end of $B_1 \cdot T_1$, as DBL does. So (a), (b) and (c) hold after the request. $\blacksquare$

**Consequences.** The following hold after every request.

1. *The lists are disjoint.* $L_1$ and $L_2$ are disjoint, and (a) splits each one.
2. *$|T_1| + |T_2| \le c$, $|T_1| + |B_1| \le c$ and $|T_1| + |T_2| + |B_1| + |B_2| \le 2c$.* From (b), $|L_1| \le c$ and $|L_1| + |L_2| \le 2c$.
3. *If $|T_1| + |T_2| < c$, both ghost lists are empty. If the directory has at least $c$ keys, the cache is full, and once full it stays full.* From (b), and because $|L_1| + |L_2|$ never decreases (every branch of DBL that deletes a page also inserts one).
4. *Each cached page on one side is more recent than each ghost on that side.* From (a), because $L_i$ is in recency order and $T_i$ is its MRU end.
5. *A request is a hit if and only if its page is in $T_1 \cup T_2$*, and the cache holds exactly the pages of $T_1 \cup T_2$. This is the definition in the code: pages are loaded on lines L7, L12 and L25 and evicted only by REPLACE and line L19.

These are the conditions that Section III of the paper asks of every policy in its class.

**The directory contains the $c$ most recent distinct pages.** A page $y$ leaves $L_1 \cup L_2$ only in DBL step 2. If it leaves as the LRU page of $L_1$ with $|L_1| = c$, then the other $c - 1$ pages of $L_1$ and the new page $x$ were all requested after $y$. If it leaves as the LRU page of $L_2$ with $|L_1| < c$ and $|L_1| + |L_2| = 2c$, then $|L_2| \ge c + 1$, and the other $c$ or more pages of $L_2$ were all requested after $y$. In both cases at least $c$ distinct pages in the directory are more recent than $y$ after the request. A page that was not among the $c$ most recent stays out of that set until it is requested again, and a request puts it back in the directory. So the $c$ most recently requested distinct pages are always in $L_1 \cup L_2$, which is the directory of ARC by (a).

**The test file.** It checks (a) against a direct DBL($2c$) after every request, the consequences 1 to 3 and the bound on $p$ on 60 seeded random traces, the recency claim, and the hit flags against a second ARC written with plain lists.
