---
title: LFU-DA evicts the smallest key with LRU ties, and its age never falls
proves: [correctness]
status: full
---

We use the pseudocode of the page, with $C_i = 1$, a cache of capacity $k \ge 1$ that starts empty, and a request sequence $\sigma_1 \ldots \sigma_n$. Let $L_t$ be the value of the age $L$ after request $t$, with $L_0 = 0$. For a cached object $i$, let $t_i$ be the time of its latest request, and $K_i$ its key, set at time $t_i$.

**Claim 1 (keys).** For each cached object $i$ after request $t$, $K_i = F_i + L_{t_i - 1}$, where $F_i$ is the number of requests to $i$ since it was last loaded, and $L_{t_i - 1}$ is the age at the start of request $t_i$. If request $t_i$ was a miss, the age used is the value after the eviction of that request.

*Proof.* Lines L3 and L10 set the key at each request to $i$ from the current count and the current age, and nothing else changes the key. Line L7 runs before line L10 in the same request, so a load uses the age after its own eviction. $\square$

**Claim 2 (the age never falls, and keys are at least the age).** For all $t$, $L_t \ge L_{t - 1}$. After request $t$, every cached object has $K_i \ge L_t$, and the object just requested has $K_i \ge L_t + 1$.

*Proof.* By induction on $t$. At $t = 0$ the cache is empty and $L_0 = 0$. Assume the claim after request $t - 1$: every cached key is at least $L_{t - 1}$. At request $t$:

- On a hit, $L$ does not change, so $L_t = L_{t - 1}$. The key of the requested object becomes $F_i + L_t \ge 1 + L_t$. The other keys do not change and are at least $L_{t - 1} = L_t$.
- On a miss with a full cache, line L7 sets $L_t$ to the key of the evicted object, which is a cached key, so $L_t \ge L_{t - 1}$ by the hypothesis. That key is the smallest cached key, so every remaining key is at least $L_t$. The new object gets the key $1 + L_t$.
- On a miss with free space, $L$ does not change and the new key is $1 + L_t$.

In all cases the age does not fall and every cached key is at least the new age. $\square$

**Claim 3 (heap with lazy deletion).** At each eviction, line L6 returns the cached object that minimizes the pair $(K_i, t_i)$.

*Proof.* The code keeps a map from each cached object to its current entry $(K_i, t_i, i)$, and every current entry is in the heap: line L3 and line L10 push it when they set it, and a rebuild puts back exactly the current entries. An entry stops being current only when the object is requested again (a new entry replaces it) or evicted (the map loses it). Line L6 pops entries in increasing order of $(K, t)$ and stops at the first one that is current. Every current entry is in the heap, so the popped entry has the smallest $(K, t)$ among the current entries. The times $t_i$ are distinct, so the pair names one object. $\square$

So the victim is the object of smallest key, and among the objects of smallest key it is the one requested least recently. The tests compare the code with a direct implementation that keeps the keys in a dictionary and scans for the smallest pair at each miss.

**Claim 4 (LFU as a special case).** If line L7 were removed, so that $L$ stays 0, then $K_i = F_i$ by claim 1, and the policy evicts the object of smallest count, least recently requested on a tie. This is LFU with LRU ties and in-cache counts.

**Aging.** Let an object $i$ hold the key $K$ and not be requested again. By claim 2, every object loaded or requested after the age reaches $K$ gets a key of at least $K + 1$. So from then on, the only objects with a key at most $K$ are objects whose keys were set before, and each eviction removes one of them or $i$. There are at most $k$ of them, so $i$ is evicted after at most $k$ more evictions once the age has reached $K$. In LFU, an object with a high count stays as long as some cached object has a smaller count, which can be forever.

**Cost.** A request does one hash lookup, at most one push, and on a miss some pops. Each pop removes an entry pushed earlier, and each request pushes one entry, so the pops over the whole run are at most the pushes. The heap holds at most $2 k + 16$ entries, because a rebuild cuts it to the $k$ current entries; a rebuild costs $O(k)$ and happens after at least $k + 16$ pushes. So the amortized time per request is $O(\log k)$, and the space is $\Theta(k)$.
