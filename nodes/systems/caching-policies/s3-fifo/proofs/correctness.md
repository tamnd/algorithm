---
title: The loops of S3-FIFO stop and the cache stays within its size
proves: [correctness]
status: full
---

We use the pseudocode of the page with a cache of $c \ge 1$ objects, a small fraction $0 < s < 1$, the move threshold $\mathit{freq} > 1$, "$M$ is full" read as $|M| > (1 - s)\,c$, and a ghost limit $g = \max(1, \lceil (1 - s)\,c \rceil)$. The invariants are:

- (I1) $|S| + |M| \le c$;
- (I2) $S$, $M$ and $G$ are pairwise disjoint, and no queue holds a key twice;
- (I3) every cached object has $0 \le \mathit{freq} \le 3$;
- (I4) $|G| \le g$.

**Lemma 1 (EVICT-M stops).** If $M$ is not empty, EVICT-M removes exactly one object from $M$ and returns. It takes at most $3|M| + 1$ steps.

*Proof.* Each step looks at the tail $t$. If $t.\mathit{freq} > 0$, line L27 moves it to the head and lowers its count by one. Otherwise line L29 removes it. No step raises a count. By (I3) the sum of the counts in $M$ is at most $3|M|$, and each step that does not remove an object lowers this sum by one. So within $3|M| + 1$ steps some step removes an object. $\square$

**Lemma 2 (EVICT-S stops).** EVICT-S takes at most $|S|$ passes of its loop. When it returns, either one object of $S$ was dropped to $G$, or $S$ is empty. Every object moved to $M$ has its count set to 0.

*Proof.* Each pass removes the tail of $S$ (line L16). The pass then either inserts the object into $M$ (line L18), after which EVICT-M may run and stops by Lemma 1, or puts its key in $G$ and returns (lines L22 and L23). So $|S|$ falls by one each pass, and the loop ends when it returns or when $S$ is empty. $\square$

**Lemma 3 (the loop on line L5 stops).** Assume (I1) to (I4) before a miss. Then the loop on line L5 stops, and on exit $|S| + |M| \le c - 1$.

*Proof.* Each call of EVICT either calls EVICT-M (line L14) or EVICT-S (line L12). Line L14 runs only when $|S| < s c$, and the loop runs only when $|S| + |M| \ge c$, so then $|M| > (1 - s)\,c > 0$, and by Lemma 1 one object leaves the cache. A call of EVICT-S either drops an object to $G$, which frees one place, or by Lemma 2 empties $S$. Moves from $S$ to $M$ do not change $|S| + |M|$, and evictions from $M$ inside EVICT-S only free places. So a call that frees nothing leaves $S$ empty, and then the next call takes line L14, because $|S| = 0 < s c$, and frees one place. Hence every two calls free at least one place, the loop stops, and on exit $|S| + |M| < c$. $\square$

**Theorem.** (I1) to (I4) hold after every request, and a request is a hit if and only if its object is in $S \cup M$.

*Proof.* By induction. All hold for empty queues. Assume they hold before a request for $x$.

*Hit.* Line L2 raises one count and caps it at 3, so (I3) holds. Nothing else changes.

*Miss.* By Lemma 3, after line L6 we have $|S| + |M| \le c - 1$. Every eviction step keeps the queues disjoint: an object moves from $S$ to $M$ (it leaves $S$ first), or from $S$ to $G$ as a key (it leaves the cache), or leaves $M$ for good. Each insertion into $G$ on line L22 drops the tail of $G$ if $|G|$ would pass $g$, so (I4) holds. Counts are only set to 0 or lowered, so (I3) holds. Since $x$ was not cached, it is in neither $S$ nor $M$. Lines L7 to L10 put $x$ in exactly one of $M$ and $S$, and remove it from $G$ if it was there, so (I2) holds. Then $|S| + |M| \le c$, which is (I1). Line L4 sets the count of $x$ to 0.

A request is a hit exactly when line L1 finds $x$ in $S$ or $M$, and these two queues hold all the cached objects. $\blacksquare$

**Consequences.**

1. *One-hit objects never reach $M$ from $S$.* An object moves from $S$ to $M$ only with count at least 2, that is after at least two hits while in $S$. An object requested once is dropped to $G$.
2. *Ghosts hold no data and are bounded.* By (I4) at most $g$ keys sit in $G$, and by (I2) none of them is cached.
3. *Total time.* Each step of EVICT-M that does not evict lowers a count by one, and each move from $S$ to $M$ resets a count of at least 2 to 0. Counts are raised only on hits, by one each, so these two kinds of step together number at most the number of hits. Every other step evicts an object, drops one to $G$, or ends a loop, and there are $O(1)$ of these per miss beyond the objects evicted, which number at most $n$. So $n$ requests take $O(n)$ time in total with hash tables for membership.

**The test file.** It compares the hit sequence with a separate list-based version of Algorithm 1 on 60 seeded random traces with three values of $s$ and both thresholds, checks (I1) to (I4) after every request, checks every row of the worked example, and checks that objects requested once never enter $M$.
