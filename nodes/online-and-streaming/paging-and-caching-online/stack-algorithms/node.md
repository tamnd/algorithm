---
tag: 834MQC
kind: concept
slug: stack-algorithms
name: Stack algorithms
aliases:
- Mattson stack algorithm property
- inclusion property of replacement policies
- priority replacement algorithms
area: online-and-streaming/paging-and-caching-online
level: advanced
summary: Replacement policies whose cache contents with size k are always a subset of contents with size k+1, enabling one-pass simulation.
prereqs: [cache-replacement-policy, lru]
see_also: [inclusion-property, mattson-stack-algorithm, belady-anomaly, reuse-distance, miss-ratio-curve, miss-ratio-curve-computation, fifo-replacement, belady-algorithm]
sources:
  - paper: doi:10.1147/sj.92.0078
    title: "R. L. Mattson, J. Gecsei, D. R. Slutz and I. L. Traiger, Evaluation techniques for storage hierarchies, IBM Systems Journal 9(2) (1970), 78-117"
    locator: the definition of stack algorithms by the inclusion property, priority algorithms, and the one-pass evaluation of all cache sizes
  - paper: doi:10.1145/363011.363155
    title: "L. A. Belady, R. A. Nelson and G. S. Shedler, An anomaly in space-time characteristics of certain programs running in a paging machine, Communications of the ACM 12(6) (1969), 349-353"
    locator: the anomaly of FIFO, where a larger memory gives more page faults
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 3, Section 3.1, the paging algorithms LRU and FIFO
---

A replacement policy is a *stack algorithm* if, on every request sequence and at every time, the set of pages in its cache of size $k$ is a subset of the set of pages in its cache of size $k + 1$. This *inclusion property* was defined by Mattson, Gecsei, Slutz and Traiger in 1970. It holds for LRU and for Belady's optimal rule, and it fails for FIFO. A stack algorithm never has more faults with a larger cache, and one pass over a trace gives its number of faults for all cache sizes at once.

## In plain words

Run the same rule twice on the same requests, once with a small cache and once with a cache one page larger. The rule is a stack algorithm if the larger cache always holds every page that the smaller cache holds.

Then a request that hits in the small cache also hits in the large one, so more memory never hurts. The pages can be kept in one ordered list, a stack, where the small cache is the top part and the large cache a longer top part. One run of the list answers the question "how many misses?" for each size.

Some rules do not have this property. With them, more memory can mean more misses.

## The idea

**Definition.** Let $C_t(k)$ be the cache of a policy with size $k$ after request $t$, from an empty start. The policy has the **inclusion property** if $C_t(k) \subseteq C_t(k+1)$ for all $\sigma$, $t$ and $k$. Then a hit with size $k$ is a hit with size $k + 1$, so the fault count $F(k)$ is non-increasing in $k$.

**Priority rules.** Call a policy a *priority rule* if at each time $t$ it has a total order on the pages that does not depend on $k$, and on a fault with a full cache it evicts the cached page that is lowest in this order. The order may depend on the requests, also on future requests.

**Claim.** Each priority rule is a stack algorithm.

*Proof.* By induction on $t$. At $t = 0$ both caches are empty. Assume $C_{t-1}(k) \subseteq C_{t-1}(k+1)$, and let $p = \sigma_t$.

- If $p \in C_{t-1}(k)$, then $p \in C_{t-1}(k+1)$, and both caches stay the same.
- If $p \notin C_{t-1}(k)$ and $p \in C_{t-1}(k+1)$, the large cache stays the same, and the small one loses at most one page and gains $p$, which the large cache holds.
- If $p$ is in neither cache and the large cache is not full, it only gains $p$, and the small cache loses at most one page and gains $p$.
- If $p$ is in neither cache and the large cache is full, then the small cache is also full, and $C_{t-1}(k+1) = C_{t-1}(k) \cup \{r\}$ for one page $r$. The small cache evicts its lowest page $q$. The lowest page of $C_{t-1}(k) \cup \{r\}$ is $r$ or $q$. In both cases the new small cache $C_{t-1}(k) \setminus \{q\} \cup \{p\}$ is a subset of the new large cache. $\square$

So the cache of size $k$ is the top $k$ pages of one list, the *stack* $S_t$, which holds the pages that have been requested, in order. The *stack distance* of request $t$ is the position of $\sigma_t$ in $S_{t-1}$, or $\infty$ for a first request. Request $t$ faults with size $k$ exactly when its stack distance is greater than $k$.

**LRU.** LRU is the priority rule with the order "most recently requested first". This order does not depend on $k$, so LRU is a stack algorithm. Its stack is the list of pages by recency: a request moves its page to the top, and the stack distance is the number of distinct pages requested since the last request for the page, plus 1. This is the [reuse distance](/reuse-distance/).

**OPT.** [Belady's algorithm](/belady-algorithm/) is the priority rule with the order "next request soonest first", with ties among pages that are never requested again broken by a rule that does not depend on $k$. So OPT is a stack algorithm.

**Others.** LFU that counts all past requests of a page, and MRU, are also priority rules. Mattson et al. list LRU, LFU, the optimal rule and random replacement among the stack algorithms.

**FIFO is not a stack algorithm.** FIFO evicts the page loaded first. The time a page was loaded depends on $k$, because it depends on which earlier requests were faults. So the order is not the same for both cache sizes, and the claim does not apply. The examples show a failure of inclusion and a larger fault count for the larger cache. The same happens for [CLOCK](/clock/), for LFU that counts only the requests since the last load, and for [flush when full](/flush-when-full/).

## Examples

**Belady's anomaly for FIFO.** Take $\sigma = 1\,2\,3\,4\,1\,2\,5\,1\,2\,3\,4\,5$ and an empty start (Belady, Nelson and Shedler 1969). The table gives the FIFO cache after each request, and F for a fault.

| $t$ | $\sigma_t$ | fault, $k = 3$ | cache, $k = 3$ | fault, $k = 4$ | cache, $k = 4$ | inclusion |
|---|---|---|---|---|---|---|
| 1 | 1 | F | {1} | F | {1} | yes |
| 2 | 2 | F | {1, 2} | F | {1, 2} | yes |
| 3 | 3 | F | {1, 2, 3} | F | {1, 2, 3} | yes |
| 4 | 4 | F | {2, 3, 4} | F | {1, 2, 3, 4} | yes |
| 5 | 1 | F | {1, 3, 4} | | {1, 2, 3, 4} | yes |
| 6 | 2 | F | {1, 2, 4} | | {1, 2, 3, 4} | yes |
| 7 | 5 | F | {1, 2, 5} | F | {2, 3, 4, 5} | no |
| 8 | 1 | | {1, 2, 5} | F | {1, 3, 4, 5} | no |
| 9 | 2 | | {1, 2, 5} | F | {1, 2, 4, 5} | yes |
| 10 | 3 | F | {2, 3, 5} | F | {1, 2, 3, 5} | yes |
| 11 | 4 | F | {3, 4, 5} | F | {1, 2, 3, 4} | no |
| 12 | 5 | | {3, 4, 5} | F | {2, 3, 4, 5} | yes |

FIFO has 9 faults with $k = 3$ and 10 faults with $k = 4$. The small cache keeps 1 and 2 at $t = 7$ because it loaded them again at $t = 5$ and $t = 6$, while the large cache loaded them at $t = 1$ and $t = 2$ and evicts them first.

**LRU on the same sequence.** The stack distances are $\infty, \infty, \infty, \infty, 4, 4, \infty, 3, 3, 5, 5, 5$. A request faults with size $k$ when its distance is greater than $k$, so one pass gives all the fault counts.

| $k$ | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| LRU faults $F(k)$ | 12 | 12 | 10 | 8 | 5 |

**LFU that counts since the last load.** Take $k = 2$ and $\sigma = 2\,1\,2\,0\,4\,0\,4\,3$, with ties broken by the oldest load. After the last request the cache of size 2 is $\{2, 3\}$ and the cache of size 3 is $\{0, 3, 4\}$. In the small cache, pages 0 and 4 evict each other, and each new load starts again with a count of 1, so page 2 with its count of 2 stays. In the large cache, 0 and 4 stay and reach a count of 2 each, and at the last request the tie goes against page 2, the oldest load.

## Where it is used

- **Miss ratio curves.** For a stack algorithm, the histogram of stack distances gives $F(k)$ for all $k$ in one pass. This is the [miss ratio curve](/miss-ratio-curve/), used to size caches and to divide a cache among programs. See [miss ratio curve computation](/miss-ratio-curve-computation/) and the [Mattson stack algorithm](/mattson-stack-algorithm/). With a balanced tree over the times of last requests, the LRU stack distances of $n$ requests take $O(n \log n)$ time.
- **Cache design.** A stack algorithm can be studied by its curve alone, because a larger cache never has more misses. The anomaly of FIFO shows that this is not true for every policy.
- **Multilevel caches.** The [inclusion property](/inclusion-property/) of hardware cache levels has the same form, with the smaller level a subset of the larger one.
- **Optimal miss counts.** Since OPT is a stack algorithm, one pass gives the optimal miss count for all cache sizes, to compare with the curve of an online policy.

## References
