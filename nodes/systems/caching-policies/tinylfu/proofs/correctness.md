---
title: The TinyLFU estimate never falls below an exact count, and the cache admits exactly by the rule
proves: [correctness]
status: full
---

We use the pseudocode of the page with a cache of $c \ge 1$ objects, a sample size $W$ that is a positive multiple of $c$, and the cap $K = W/c$. Fix the hash functions. For a key $x$ let $\min(x)$ be the least of its $d$ counters.

**The exact filter.** As a reference, define an exact filter that follows the same rules without hashing. It has an exact doorkeeper set $E$ and an exact count $e(x)$ for every key. On RECORD($x$): if $x \notin E$, add $x$ to $E$; otherwise, if $e(x) < K$, raise $e(x)$ by one. On RESET, halve every $e(x)$, rounding down, and empty $E$. Its estimate is $e(x) + [x \in E]$. Both filters see the same requests, so their counters $n$ of additions are equal and they reset at the same moments.

**Lemma 1 (no underestimate).** At all times, for every key $x$:

- (a) $E \subseteq D$;
- (b) $\min(x) \ge e(x)$;
- (c) every counter of the sketch is at most $K$.

*Proof.* By induction on the steps; at the start all values are 0 and both sets are empty. A Bloom filter has no false negatives, so (a) holds while both only grow, and both are emptied together at a reset. Now take RECORD($y$).

- If $y \notin D$, then $y \notin E$ by (a). Both filters only insert $y$ into the doorkeeper. Nothing else changes.
- If $y \in D$ but $y \notin E$ (a false positive), the exact filter only inserts $y$ into $E$, and $e$ does not change. The sketch may raise counters. Counters never fall, so (b) holds.
- If $y \in E$, then $y \in D$. If $\min(y) < K$, line L11 raises every counter of $y$ that equals $\min(y)$, so $\min(y)$ rises by one, while $e(y)$ rises by at most one. If $\min(y) = K$, the sketch does not change and $e(y) \le K$ after the step, since the exact filter also stops at $K$.

For a key other than $y$, counters only rise and $e$ does not change. A counter is raised only from a value $\min(y) < K$, so (c) holds. On RESET, halving with rounding down is monotone, $\lfloor a/2 \rfloor \ge \lfloor b/2 \rfloor$ when $a \ge b$, so (b) and (c) still hold. $\square$

**Corollary 1.** $\mathrm{EST}(x) = \min(x) + [x \in D] \ge e(x) + [x \in E]$ for every key $x$. Collisions and false positives can only raise the estimate.

**Lemma 2 (estimate and true count).** Let $f(x)$ be the true number of requests of $x$ since the last reset, or since the start. If $f(x) \le K$, then $\mathrm{EST}(x) \ge f(x)$.

*Proof.* In the exact filter, the first request of $x$ in the sample puts it in $E$, and each later one raises $e(x)$, which stays below the cap because $f(x) - 1 < K$. So $e(x) + [x \in E] = f(x)$. Apply Corollary 1. $\square$

Right after a reset the exact estimate is $\lfloor e(x)/2 \rfloor$, with $E$ empty, so older requests count half as much. This is the aging of Section 3.3 of the paper.

**Lemma 3 (reset).** Line L13 starts a reset exactly when the counter $n$ of additions reaches $W$. After the reset, $n = W/2$ rounded down, $D$ is empty, and every counter is half its old value, rounded down. So each reset after the first comes $W - \lfloor W/2 \rfloor$ additions after the one before it.

*Proof.* Line L12 raises $n$ by one per RECORD and line L13 tests $n = W$ right after, so $n$ never passes $W$. Line L14 does the rest. $\square$

**Theorem.** After every request:

1. (I1) at most $c$ objects are cached;
2. (I2) a request is a hit if and only if its object was cached before the request;
3. (I3) on a miss with a full cache, the new object $x$ replaces the LRU object $v$ exactly when $\mathrm{EST}(x) > \mathrm{EST}(v)$, both read after RECORD($x$); otherwise the cache does not change.

*Proof.* By induction; all hold for an empty cache. Lines L2 and L3 handle a cached object and do not change the set of cached objects. Lines L4 and L5 insert $x$ only when fewer than $c$ objects are cached, so afterwards at most $c$ are cached. Otherwise exactly $c$ are cached; line L8 removes one object and adds one, so the count stays $c$, and when the test on line L7 fails nothing changes. This gives (I1) and (I3). The filter affects which objects are cached only through line L7, and line L2 tests membership in the cache, so (I2) holds. $\blacksquare$

**Consequences.**

1. *Counter width.* By Lemma 1(c), a counter of this code fits in $\lceil \log_2 (K + 1) \rceil$ bits, which is 4 bits for $W = 10c$. The paper counts the doorkeeper as one more request and gives 3 bits for $W = 8c$; this code does not use that saving.
2. *Cost of a request.* RECORD and EST each touch $d$ counters and a fixed number of doorkeeper bits. A reset touches every counter once.

**The test file.** It runs the filter beside the exact filter above on 25 seeded random traces with a small sketch, so that collisions happen, and checks Corollary 1 for every key after every request. It checks every row of the worked example, the cap, the halving of a reset, the admission rule against the LRU victim on every full miss, that keys seen once do not push out hot objects, and that two runs with the same seed give the same hits.
