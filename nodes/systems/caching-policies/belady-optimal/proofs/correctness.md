---
title: MIN evicts the furthest item and has the fewest misses
proves: [correctness]
status: full
---

We use the setting of the page: a trace $\sigma_0 \cdots \sigma_{n-1}$, a cache of $k$ items of size 1, an empty start, and a cost of 1 per miss. A *demand schedule* changes the cache only on a miss: it loads the requested item and, if the cache is full, evicts one cached item. Its cost is its number of misses. For a time $t$ and an item $q$, let $\mathrm{next}_t(q)$ be the smallest $s > t$ with $\sigma_s = q$, or $n$ if there is none.

**Lemma 1 (the code follows the rule).** At each eviction at time $t$, line L11 selects a cached item $y$ with the largest value of $\mathrm{next}_t(y)$.

*Proof.* Claim: after line L13 at time $t$, for each cached item $y$, $key[y] = \mathrm{next}_t(y)$, and the pair $(key[y], y)$ is in $H$. Line L13 sets $key[x] = \mathrm{next}[t] = \mathrm{next}_t(x)$ for the requested item $x$ and pushes the pair. For another cached item $y$, the last request $t' < t$ set $key[y] = \mathrm{next}[t']$, the first request for $y$ after $t'$. There is no request for $y$ in $(t', t]$, so this is also $\mathrm{next}_t(y)$. Line L12 removes only the evicted item from $key$, so the claim holds at each step.

Each pair pushed for an item $y$ has the key $\mathrm{next}[t']$ of a request $t'$ for $y$. These keys strictly increase with $t'$: $\mathrm{next}[t']$ is the next request for $y$, which is the following $t''$, and $\mathrm{next}[t''] > t''$. So a stale pair for a cached $y$ has a smaller key than its current pair, and it fails the test $key[y] = d$. A pair for an evicted item fails the test $y \in key$, unless $y$ was loaded again later, in which case it is again a stale pair of a smaller key. So the pairs that pass the test are exactly the current pairs. POP-MAX returns pairs in order of decreasing key, so the first pair that passes has the largest key among the cached items. At an eviction at time $t$ the code is between L10 and L13 of step $t$, and the keys are those set by step $t - 1$, which equal $\mathrm{next}_{t-1}(y) = \mathrm{next}_t(y)$ for each cached $y \ne \sigma_t$. Here $\sigma_t$ is not cached, so this covers all cached items. $\square$

So MIN, as coded, is the demand schedule that at each eviction evicts a cached item with the largest $\mathrm{next}_t$, with some fixed tie rule.

**Lemma 2 (exchange).** Let $S$ be a demand schedule that makes the same choices as MIN at times $0, \ldots, t-1$ and a different choice at time $t$. Then there is a demand schedule $S'$ that makes the same choices as MIN at times $0, \ldots, t$ and has $\mathrm{cost}(S') \le \mathrm{cost}(S)$.

*Proof.* Before time $t$ the two caches are the same set $C$. At time $t$ there is a miss on $r = \sigma_t$ with $|C| = k$, and $S$ evicts $u$ while MIN evicts $v \ne u$. By Lemma 1, $\mathrm{next}_t(u) \le \mathrm{next}_t(v)$. Two different items do not have the same next request unless both have the value $n$, so either $u$ is requested before $v$, or neither is requested again.

Let $S'$ evict $v$ at time $t$. After time $t$ the caches are

$$S: D \cup \{v\}, \qquad S': D \cup \{x\}, \qquad \text{where } D = C \setminus \{u, v\} \cup \{r\} \text{ and } x = u.$$

We define $S'$ after $t$ while the caches have this form, with $x \notin D \cup \{v\}$ and $v \notin D$. Once the caches are equal, $S'$ makes the same choices as $S$ from then on. Both caches are full after $t$, since demand schedules never shrink a full cache. Look at a request $s > t$ while the caches differ, with item $q = \sigma_s$.

1. **$q \in D$.** Both hit. Nothing changes.
2. **$q \notin D \cup \{v, x\}$.** Both miss. If $S$ evicts $v$, $S'$ evicts $x$; both caches become $D \cup \{q\}$. If $S$ evicts $y \in D$, $S'$ also evicts $y$; the caches keep the form with $D' = D \setminus \{y\} \cup \{q\}$ and the same $x$. Both pay 1.
3. **$q = x$.** $S$ misses and $S'$ hits. If $S$ evicts $v$, the caches become equal. If $S$ evicts $y \in D$, the cache of $S$ is $(D \setminus \{y\}) \cup \{x, v\}$ and that of $S'$ is $(D \setminus \{y\}) \cup \{x, y\}$, which is the form with $D' = D \setminus \{y\} \cup \{x\}$ and the new $x' = y$. $S$ pays 1 and $S'$ pays 0.
4. **$q = v$.** $S$ hits. $S'$ misses, loads $v$ and evicts $x$; both caches become $D \cup \{v\}$. $S$ pays 0 and $S'$ pays 1.

In each case $S'$ loads only the requested item on a miss and evicts one item of its full cache, so $S'$ is a demand schedule. It makes the choices of MIN up to $t$.

Now compare the costs. Let $c(s)$ be the cost of $S$ minus the cost of $S'$ on requests $0, \ldots, s$. Then $c(t) = 0$. Only case 3 changes $c$ while the caches differ, by $+1$, and only case 4, by $-1$, which ends the difference. Once the caches are equal, $c$ stays fixed. So it is enough to show that case 4 cannot come before case 3.

Until case 3 first happens, $x = u$, because only case 3 changes $x$. Case 3 with $x = u$ is a request for $u$. Case 4 is a request for $v$. If $v$ is requested again, then $u$ is requested before $v$, at time $\mathrm{next}_t(u) < \mathrm{next}_t(v)$, and neither $u$ nor $v$ can be requested in between. So at time $\mathrm{next}_t(u)$ either the caches are already equal, or case 3 happens. If $v$ is never requested again, case 4 never happens. In each case $c$ never goes below 0, so $\mathrm{cost}(S') \le \mathrm{cost}(S)$. $\square$

**Theorem.** MIN has the fewest misses among all demand schedules on $\sigma$ with $k$ items, so it has the fewest misses of any schedule.

*Proof.* There are finitely many demand schedules, so an optimal one exists. Among the optimal demand schedules, take $S$ that agrees with MIN on the longest prefix of times, say on times $0, \ldots, t-1$. If $S$ differs from MIN at time $t$, Lemma 2 gives a demand schedule $S'$ with cost at most that of $S$, so $S'$ is optimal, and it agrees with MIN on times $0, \ldots, t$. This contradicts the choice of $S$. So $S$ agrees with MIN everywhere, and MIN is optimal among demand schedules. A schedule that loads items early or evicts them without need can be turned into a demand schedule with at most the same number of loads, by the conversion on the page on demand paging, so MIN is optimal among all schedules. $\square$

**Remark (sizes).** The proof uses unit sizes in case 3 and case 4: one eviction of $S'$ always makes room for one load. With sizes, evicting $v$ may free more or less room than evicting $u$, and the example on the page shows that the rule then fails.
