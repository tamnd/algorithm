---
title: The inflation form equals GreedyDual, and GreedyDual is k/(k - h + 1)-competitive
proves: [correctness]
status: full
---

We use the pseudocode of the page. The cache has capacity $k$; object $x$ has size $s(x) \ge 1$ and cost $c(x) \ge 0$. Write $r(x) = c(x)/s(x)$. Ties in line L6 go to the object whose value was set first.

The *decrement form* is the rule as Young stated it. It stores a value $G(x)$ for each cached object. A hit or a load sets $G(x) = r(x)$. To make room, it takes the least value $\delta = \min_q G(q)$, subtracts $\delta$ from $G(q)$ for each cached $q$, and evicts an object whose value is now $0$, with the same tie rule.

## 1. The two forms make the same decisions

**Claim.** On each request sequence, the inflation form and the decrement form have the same hits, evict the same objects, and after each step satisfy $H(q) = L + G(q)$ for each cached $q$.

*Proof.* By induction on the steps. At the start both caches are empty, so the claim holds.

- *Hit or load.* The inflation form sets $H(p) = L + r(p)$ and the decrement form sets $G(p) = r(p)$, so $H(p) = L + G(p)$. Other values do not change.
- *Eviction.* By the induction hypothesis $H(q) - G(q) = L$ for each cached $q$, the same number for all $q$. So both forms order the cached objects in the same way, and with the same tie rule they choose the same victim $v$. The inflation form sets $L' = H(v) = L + G(v)$, so $\delta = G(v) = L' - L$. The decrement form sets $G'(q) = G(q) - \delta$. Then $L' + G'(q) = L + G(q) = H(q)$ for each $q$ that stays.

Both forms test "is $p$ cached" and "does $p$ fit" on the same cache contents, so the hits and the loads are also the same. $\square$

A consequence: $L$ never decreases. Before an eviction each $G(q) \ge 0$, so each $H(q) \ge L$, and line L7 sets $L$ to one of these values.

## 2. LRU is a special case

With $s(x) = c(x) = 1$, line L2 or L9 sets $H(p) = L + 1$. Since $L$ never decreases, an object requested later has a value at least as large as an object requested earlier. With ties broken by the time the value was set, the object with the least $(H, \text{time})$ is the least recently requested one. So the rule evicts as [LRU](/lru/) does.

## 3. The bound for weighted paging

Now let all sizes be $1$ and let $h \le k$. Let OPT be any offline algorithm with a cache of $h$ slots. Both caches are empty at the start, and OPT loads each requested object (the forced model).

**Theorem (Young).** $(k - h + 1) \cdot \mathrm{cost}(\mathrm{GD}) \le k \cdot \mathrm{cost}(\mathrm{OPT})$.

*Proof.* We use the decrement form, which makes the same decisions by part 1. Set $G(x) = 0$ for each $x$ that GD does not hold. Each step keeps $0 \le G(x) \le c(x)$: values start at $c(x)$ and only lose the least value. Let $D$ be the set that GD holds and $O$ the set that OPT holds, and define the [potential](/potential-function/)

$$\Phi = (h - 1) \sum_{x \in D} G(x) \; + \; k \sum_{x \in O} \bigl(c(x) - G(x)\bigr).$$

Both sums are non-negative, so $\Phi \ge 0$, and $\Phi = 0$ at the start. We show that for each request to $p$, with OPT moving first,

$$(k - h + 1) \cdot \Delta\mathrm{GD} + \Delta\Phi \le k \cdot \Delta\mathrm{OPT}. \qquad (\ast)$$

*OPT moves.* If OPT evicts $y$, a non-negative term leaves the second sum, so $\Phi$ does not increase. If OPT loads $p$ at cost $c(p)$, the term $k(c(p) - G(p)) \le k \cdot c(p)$ enters the second sum. So $(\ast)$ holds for this part. After it, $p \in O$.

*GD hits.* $G(p)$ rises from $g$ to $c(p)$. The first sum gains $(h-1)(c(p) - g)$ and the second loses $k(c(p) - g)$. So $\Delta\Phi = -(k - h + 1)(c(p) - g) \le 0$, and GD pays nothing.

*GD misses and is full.* GD holds $k$ objects. Subtracting $\delta \ge 0$ from each lowers the first sum by $(h-1) k \delta$. It raises the second sum by $k \delta$ for each object in $O \cap D$. Since $p \in O$ and $p \notin D$, we have $|O \cap D| \le h - 1$, so the second sum rises by at most $k (h - 1) \delta$. The change is at most $0$. Then GD evicts an object with value $0$; its term in each sum does not change, because its value stays $0$ outside $D$.

*GD loads $p$.* $G(p)$ rises from $0$ to $c(p)$, and $p \in O$. The first sum gains $(h-1) c(p)$ and the second loses $k \cdot c(p)$. So $\Delta\Phi = -(k - h + 1) c(p)$, and GD pays $c(p)$. Then $(\ast)$ holds with equality for this part.

Adding $(\ast)$ over all steps gives $(k - h + 1)\,\mathrm{cost}(\mathrm{GD}) + \Phi_{\text{end}} - \Phi_0 \le k \cdot \mathrm{cost}(\mathrm{OPT})$. With $\Phi_0 = 0$ and $\Phi_{\text{end}} \ge 0$ the theorem follows. $\square$

With $h = k$ the ratio is $k$, which matches the [lower bound for deterministic paging](/sleator-tarjan-paging-bound/). For objects of different sizes the same rule is the full-credit case of [Landlord](/landlord-algorithm/), and Young's potential argument on that page gives the same ratio $k/(k - h + 1)$, with $k$ and $h$ in units of size.

## 4. Running time

Each request does $O(1)$ heap pushes and, at a miss, some pops. A push happens only at a hit or a load, so the number of pops, valid or stale, is at most the number of pushes, which is at most $n$. The heap is rebuilt when it holds more than $2m + 16$ entries, where $m$ is the number of cached objects. The rebuild takes $O(m)$ time and removes more than $m + 16$ stale entries, each of which needed a push, so its cost is paid by those pushes. Each heap operation takes $O(\log m)$ time, so $n$ requests take $O(n \log m)$ time with exact arithmetic of fixed size.
