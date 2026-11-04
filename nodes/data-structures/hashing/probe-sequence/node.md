---
tag: 868PP7
kind: concept
slug: probe-sequence
name: Probe sequence
aliases:
- probing
area: data-structures/hashing
level: intro
summary: Ordered list of slots tried for a key during insertion or search.
prereqs: [hash-table, hash-function]
see_also: [open-addressing, linear-probing, quadratic-probing, double-hashing, uniform-hashing-assumption, primary-clustering, secondary-clustering, robin-hood-hashing]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 11.4, Open addressing (probe sequences, linear probing, double hashing, and the exercise on quadratic probing)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.4, Hashing (the probe sequences of Algorithms L and D, and the exercises on quadratic probing)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.4, Hash Tables, the part on linear probing
---

A probe sequence is the ordered list of slots that an [open addressing](/open-addressing/) [hash table](/hash-table/) tries for a key: first the home slot, then the next choice, and so on. An insert puts the key in the first free slot of its sequence, and a search walks the same sequence until it finds the key or an empty slot. The rule that makes the sequence, such as [linear probing](/linear-probing/), [quadratic probing](/quadratic-probing/) or [double hashing](/double-hashing/), decides whether every slot can be reached and how much the sequences of different keys overlap, and so it decides the cost of the table.

## In plain words

A key does not always get its first choice of slot, so it needs a list of second, third and later choices. That list is the probe sequence. It is computed from the key, so the same key always gets the same list, and a search can retrace the steps of the insert.

A good list has two qualities. It reaches every slot of the table, so an insert never fails while there is room. And two different keys usually have different lists, so the keys do not crowd onto the same few slots. The simple rule "try the next slot" reaches every slot but makes keys crowd together. A rule that jumps by a step that depends on the key crowds much less.

## The idea

Let the table have slots $0, \ldots, m-1$ and let $U$ be the set of possible keys. A probe rule is a function

$$h : U \times \{0, 1, \ldots, m-1\} \to \{0, 1, \ldots, m-1\},$$

and the probe sequence of key $k$ is $\langle h(k, 0), h(k, 1), \ldots, h(k, m-1) \rangle$. The slot $h(k, 0)$ is the home slot of $k$. An insert or a search for $k$ that ends at probe $i$ (counting from 0) costs $i + 1$ probes, and $i$ is the *displacement* of $k$, also called its probe sequence length in [Robin Hood hashing](/robin-hood-hashing/).

**Full coverage.** The rule is *complete* when, for each key $k$, the sequence is a permutation of $\{0, \ldots, m-1\}$. Then an insert finds a free slot whenever one exists, and a failed search makes at most $m$ probes. With an incomplete rule, an insert can fail while the table has free slots.

**The common rules.** With ordinary hash functions $h'$ and $h_2$:

| rule | $h(k, i)$ | complete when | distinct sequences |
|---|---|---|---|
| linear probing | $(h'(k) + i) \bmod m$ | always | $m$ |
| quadratic probing | $(h'(k) + c_1 i + c_2 i^2) \bmod m$ | for some $c_1$, $c_2$, $m$ only | at most $m$ |
| double hashing | $(h'(k) + i \cdot h_2(k)) \bmod m$ | $\gcd(h_2(k), m) = 1$ | up to $m(m-1)$ for prime $m$ |
| uniform hashing (a model) | a random permutation for each key | always | $m!$ |

A rule in which the whole sequence depends only on the home slot has at most $m$ distinct sequences. The [uniform hashing assumption](/uniform-hashing-assumption/) is the ideal at the other end, with all $m!$ permutations equally likely, and double hashing comes close to it in practice.

**Two facts about completeness, with proofs.**

*Double hashing.* Let $s = h_2(k)$ and $g = \gcd(s, m)$. For $0 \le i < j < m$, the probes $i$ and $j$ hit the same slot exactly when $m$ divides $(j - i)s$, that is, when $m/g$ divides $j - i$. If $g = 1$, this needs $m \mid j - i$, which is impossible for $0 < j - i < m$, so the $m$ probes are distinct. If $g > 1$, the probes $0$ and $m/g$ hit the same slot, and the sequence visits only $m/g$ slots, again and again.

*Triangular probing.* Let $m = 2^t$ and $h(k, i) = (h'(k) + i(i+1)/2) \bmod m$, which is quadratic probing with $c_1 = c_2 = 1/2$. Suppose probes $i < j$, both less than $m$, hit the same slot. Then $2^t$ divides $j(j+1)/2 - i(i+1)/2$, so $2^{t+1}$ divides $(j - i)(i + j + 1)$. The two factors have a sum $2j + 1$ that is odd, so one of them is odd. Hence $2^{t+1}$ divides the other one. But $0 < j - i < 2^t$ and $0 < i + j + 1 < 2^{t+1}$, so neither factor is a multiple of $2^{t+1}$. This is a contradiction, so the rule is complete.

**Clustering.** Two kinds of overlap make probe sequences long.

- *[Primary clustering](/primary-clustering/).* With linear probing, a key whose sequence enters a run of full slots follows the run to its end, whatever its home slot was. So runs grow, and two runs merge when the slot between them is filled. When home slots are uniform, an empty slot that follows a run of $\ell$ full slots is the next slot to be filled with probability $(\ell + 1)/m$, so long runs grow faster than short ones.
- *[Secondary clustering](/secondary-clustering/).* With quadratic probing, keys with the same home slot have the same whole sequence. The sequences of keys with different homes diverge after they meet, so primary clustering is gone, but keys with equal homes still collide at each probe.

Double hashing has neither kind, because two keys share a sequence only if both $h'$ and $h_2$ agree.

**Cost of the next probe.** A probe sequence also decides the memory traffic. Linear probing reads adjacent slots, often in the same cache line. Double hashing jumps across the array, so each probe can be a cache miss. Bucketed schemes such as the [Swiss table](/swiss-table/) probe a group of slots at a time and move between groups by a quadratic rule.

## Examples

**Linear probing**, $m = 11$, home slot 3: the sequence is 3, 4, 5, ..., 10, 0, 1, 2. It is complete for every home slot.

**Squares modulo a power of 2 are not complete.** With $m = 8$, $h(k, i) = (3 + i^2) \bmod 8$ gives 3, 4, 7, 4, 3, 4, 7, 4. Only the slots 3, 4 and 7 are reached, because the squares modulo 8 are only 0, 1 and 4.

**Triangular offsets modulo a power of 2 are complete.** With $m = 8$, $h(k, i) = (3 + i(i+1)/2) \bmod 8$ gives 3, 4, 6, 1, 5, 2, 0, 7, which is all 8 slots, as the proof above says.

**Squares modulo a prime reach half the table.** With $m = 11$ and offsets $i^2$, the offsets modulo 11 take only the 6 values 0, 1, 3, 4, 5, 9. In general an odd prime $m$ has $(m+1)/2$ squares modulo $m$, counting 0: if $i^2 \equiv j^2$, then $m$ divides $(j-i)(j+i)$, which is impossible for $0 \le i < j \le (m-1)/2$. So the first $(m+1)/2$ probes are distinct, and an insert succeeds whenever the table is at most half full.

**Double hashing with a bad step.** With $m = 12$, home 5 and step $h_2(k) = 4$, the sequence is 5, 9, 1, 5, 9, 1, ..., which reaches 3 slots, since $\gcd(4, 12) = 4$ and $12/4 = 3$. With step 5, which has no common factor with 12, it is 5, 10, 3, 8, 1, 6, 11, 4, 9, 2, 7, 0, which is all 12 slots.

**A non-example.** [Separate chaining](/separate-chaining/) has no probe sequence: a key always goes to its home bucket, and collisions are handled by a list in the bucket. [Cuckoo hashing](/cuckoo-hashing/) gives each key two possible slots, but an insert may move other keys, so the slot of a key is not the first free slot of a fixed sequence.

## Where it is used

- [Open addressing](/open-addressing/) is defined by its probe rule: [linear probing](/linear-probing/), [quadratic probing](/quadratic-probing/) and [double hashing](/double-hashing/) are the classic ones.
- The [uniform hashing assumption](/uniform-hashing-assumption/) models the probe sequence as a random permutation, and gives the bound $1/(1 - \alpha)$ for a failed search at [load factor](/load-factor/) $\alpha$.
- The [analysis of linear probing](/linear-probing-analysis/) measures the cost of primary clustering exactly.
- [Yao's lower bound](/yao-open-addressing-lower-bound/) shows that uniform hashing is close to optimal for a successful search, among the schemes that put each key in the first free slot of its sequence and never move it.
- [Robin Hood hashing](/robin-hood-hashing/) reorders keys along their probe sequences by displacement.
- [Lazy deletion](/lazy-deletion/) exists because a search must be able to walk past a deleted key on its probe sequence.

## References
