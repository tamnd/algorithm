---
tag: 4SP6AS
kind: definition
slug: inclusion-property
name: Inclusion property
aliases:
- stack property
- inclusion property of stack algorithms
area: systems/caching-policies
level: advanced
summary: "A policy has the inclusion property if, on each trace, its cache of size k always holds a subset of its cache of size k+1. Such policies are stack algorithms."
prereqs: [cache-replacement-policy]
see_also: [stack-algorithms, mattson-stack-algorithm, belady-anomaly, multilevel-caching, reuse-distance, miss-ratio-curve, lru, fifo-replacement]
sources:
  - paper: doi:10.1147/sj.92.0078
    title: "R. L. Mattson, J. Gecsei, D. R. Slutz and I. L. Traiger, Evaluation techniques for storage hierarchies, IBM Systems Journal 9(2) (1970), 78-117"
    locator: the inclusion property, the definition of stack algorithms, and priority algorithms as the stack algorithms
  - paper: doi:10.1145/363011.363155
    title: "L. A. Belady, R. A. Nelson and G. S. Shedler, An anomaly in space-time characteristics of certain programs running in a paging machine, Communications of the ACM 12(6) (1969), 349-353"
    locator: the FIFO example where inclusion fails and a larger memory has more faults
  - book: isbn:9780128119051
    title: John L. Hennessy and David A. Patterson, Computer Architecture, A Quantitative Approach, sixth edition, Morgan Kaufmann, 2017
    locator: Appendix B and Chapter 2, multilevel inclusion and exclusion in cache hierarchies
---

The inclusion property is a property of a replacement policy: on every trace, at every time, the set of items in the policy's cache of size $k$ is a subset of the set in its cache of size $k + 1$. Policies with this property are called *stack algorithms*, after Mattson, Gecsei, Slutz and Traiger (1970), because their caches of all sizes are the top parts of one ordered list, the stack. LRU and Belady's MIN have the property; FIFO and CLOCK do not. The same name is also used in hardware for a different property of a cache hierarchy, *multilevel inclusion*, which this page keeps apart below.

## Definition

Fix a replacement policy $P$ for caches of items of size 1, and run it from an empty cache on a trace $\sigma_1 \cdots \sigma_n$. Let $C_t(k)$ be the set of items in the cache of size $k$ after request $t$, with $C_0(k) = \emptyset$.

**Definition.** $P$ has the *inclusion property* if

$$C_t(k) \subseteq C_t(k + 1) \quad \text{for every trace } \sigma, \text{ every } t \ge 0 \text{ and every } k \ge 1.$$

A policy with the inclusion property is a *stack algorithm*.

For a deterministic demand policy, $|C_t(k)| = \min(k, D_t)$, where $D_t$ is the number of distinct items in $\sigma_1 \cdots \sigma_t$, because the cache fills up and then stays full. Two facts follow from the definition.

**Proposition 1 (no anomaly).** If $P$ has the inclusion property, the number of misses of size $k + 1$ is at most the number of misses of size $k$, on every trace.

*Proof.* Request $t$ hits with size $k$ when $\sigma_t \in C_{t-1}(k) \subseteq C_{t-1}(k + 1)$, so it also hits with size $k + 1$. $\square$

**Proposition 2 (the stack).** A demand policy has the inclusion property if and only if, for each $t$, there is an ordering $s_1, s_2, \ldots, s_{D_t}$ of the distinct items seen so far such that $C_t(k) = \{s_1, \ldots, s_{\min(k, D_t)}\}$ for every $k$.

*Proof.* If such an ordering exists, the top $k$ items lie in the top $k + 1$ items. For the other direction, assume inclusion. For $k \le D_t$, $C_t(k - 1) \subseteq C_t(k)$ and the sizes are $k - 1$ and $k$, so $C_t(k) \setminus C_t(k-1)$ is a single item; call it $s_k$. For $k \ge D_t$ the cache holds all $D_t$ items. Then $C_t(k) = \{s_1, \ldots, s_k\}$ by induction on $k$. $\square$

The position of an item in this list is its *stack distance*. For LRU it is the depth in the order of last use, which is the [reuse distance](/reuse-distance/) plus 1. The [Mattson stack algorithm](/mattson-stack-algorithm/) updates the list at each request and so gives the misses of every size in one pass.

## Examples and non-examples

- **LRU has it.** The LRU cache of size $k$ holds the $k$ most recently used items, which lie among the $k + 1$ most recently used items. The list of Proposition 2 is the order of last use.
- **MIN has it,** if ties are broken by a rule that does not depend on $k$. The list orders the items by their next request, soonest first, and Mattson and others showed that this order can be kept across all sizes at once. An exhaustive check over all traces of length 8 on 4 items, with the tie rule "evict the least recently used of the items never requested again", finds no violation.
- **LFU that counts all past uses has it,** with a tie rule that does not depend on $k$, such as least recently used, because the counts do not depend on $k$ either. An exhaustive check over all traces of length 8 on 4 items finds no violation. An LFU that forgets the count of an evicted item is a different policy, and its counts do depend on $k$.
- **FIFO does not.** On $1\,2\,3\,4\,1\,2\,5\,1\,2\,3\,4\,5$, after the seventh request, the FIFO cache of size 3 is $\{1, 2, 5\}$ and the cache of size 4 is $\{2, 3, 4, 5\}$. Item 1 is in the smaller cache only. This leads to [Belady's anomaly](/belady-anomaly/): 9 faults with 3 frames and 10 with 4. The order of a FIFO queue depends on the load times, and these depend on $k$.
- **CLOCK does not,** in general, for the same reason. The page on Belady's anomaly gives a short trace for one form of CLOCK.
- **Not a property of one cache.** The inclusion property compares caches of different sizes that run the same policy on the same trace. It says nothing about one cache alone.

## Related definitions

**Stack algorithms and priority algorithms.** Mattson and others showed that a policy is a stack algorithm when, at each time, it ranks the items by a priority that does not depend on the cache size, and on a miss evicts the item of lowest priority. The page [stack algorithms](/stack-algorithms/) treats the class in the language of online paging, and the [Mattson stack algorithm](/mattson-stack-algorithm/) gives the one-pass procedure.

**Multilevel inclusion.** In a hierarchy of caches, such as an L1 cache in front of an L2 cache, *inclusion* means that each block in L1 is also in L2 at all times. This is a property of a hierarchy design, not of a policy on one trace. It does not follow from the inclusion property of the policy, because L2 sees only the misses of L1. Example: let L1 be LRU with 2 blocks and L2 be LRU with 3 blocks, and request $a\,b\,a\,c\,a\,d$. L1 hits on the second and third $a$, so L2 sees only $a\,b\,c\,d$ and evicts $a$ when $d$ arrives, while L1 still holds $a$. An *inclusive* hierarchy therefore invalidates the L1 copy when L2 evicts a block. An *exclusive* hierarchy keeps each block in at most one level, and a hierarchy that is *neither* makes no promise. See [multilevel caching](/multilevel-caching/).

**Monotone miss ratio curve.** By Proposition 1, a stack algorithm has a [miss ratio curve](/miss-ratio-curve/) that never rises. A falling curve on one trace is not a test for the property: FIFO lacks inclusion, but its curve falls on most traces.

## References
