---
tag: VTZKC2
kind: algorithm
slug: carp
name: CARP
aliases:
- Cache Array Routing Protocol
area: systems/load-balancing-and-hashing
level: advanced
summary: CARP sends each URL to the proxy cache with the highest score, a 32-bit hash of the URL and the proxy name times a load factor multiplier that makes the shares match the set load factors.
solves: [dynamic-partitioning-problem]
model: word-ram
complexity:
  vars: {n: the number of member proxies, L: the length of the URL in bytes}
  time: {worst: Θ(n + L)}
  space: {extra: Θ(n)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1998
  people: [Vinod Valloppillil, Keith W. Ross]
  note: The Internet-Draft for CARP v1.0 is dated February 1998. Microsoft Proxy Server and Squid implemented it (RFC 3040).
prereqs: [rendezvous-hashing, hash-function]
see_also: [consistent-hashing, monotonicity-property, balance-property, weighted-random-load-balancing, ecmp-hashing, cache-hit-ratio, failover, bounded-load-consistent-hashing]
sources:
  - url: https://datatracker.ietf.org/doc/html/draft-vinod-carp-v1-03
    title: Vinod Valloppillil and Keith W. Ross, Cache Array Routing Protocol v1.0, Internet-Draft draft-vinod-carp-v1-03, February 1998
    locator: Section 2 (the Proxy Array Membership Table), Section 3.1 (hash function), Section 3.2 (hash combination), Section 3.3 (load factor multipliers), Section 3.4 (route selection) and Section 3.5 (member failure routing)
  - paper: doi:10.1109/65.642358
    title: Keith W. Ross, Hash routing for collections of shared Web caches, IEEE Network 11(6), 1997, pages 37 to 44
    locator: the comparison of hash routing schemes for a group of shared caches on a LAN (section level not checked)
  - paper: doi:10.1109/90.663936
    title: David G. Thaler and Chinya V. Ravishankar, Using name-based mappings to increase hit rates, IEEE/ACM Transactions on Networking 6(1), 1998, pages 1 to 14
    locator: the highest random weight mapping that CARP uses
  - url: https://www.rfc-editor.org/rfc/rfc3040
    title: Ian Cooper, Ingrid Melve and Gary Tomlinson, Internet Web Replication and Caching Taxonomy, RFC 3040, January 2001
    locator: "Section 6.3 (CARP for user agent to proxy configuration: implemented in Microsoft Proxy Server, Squid) and Section 7.2.1 (CARP as a hashing function that divides the URL space among a cluster)"
---

The Cache Array Routing Protocol (CARP) splits the URLs of the web among an array of proxy caches, so that each URL is cached on one member only. It is a form of [rendezvous hashing](/rendezvous-hashing/), or highest random weight hashing: each member gets a score from a 32-bit [hash](/hash-function/) of the URL and the member name, the score is multiplied by a *load factor multiplier* $X_k$, and the URL goes to the member with the highest score. The multipliers are chosen so that member $k$ gets the share $P_k$ of the URLs that the administrator sets. A lookup costs one pass over the URL and one score for each of the $n$ members.

## In plain words

A company has several proxy caches. If every cache stored every popular page, the group would hold the same pages many times. CARP gives each page one home cache, and every browser and every proxy computes the same home with no messages.

To find the home of a page, compute a ticket for each cache from the page address and the cache name, and pick the cache with the highest ticket. A bigger cache should get more pages, so its tickets are stretched by a fixed factor. The factors come from a short formula that makes each cache win exactly its planned share, if the tickets behave like random numbers.

If a cache fails, the pages it owned go to their second best cache, and the other pages stay where they are.

## The problem

There are $n$ member proxies, each with a name and a load factor $P_k > 0$, with $\sum_k P_k = 1$. Each request carries a URL. Every agent that knows the member list must map each URL to one member so that:

- all agents agree, with no communication, so that a URL is fetched and stored once in the array;
- member $k$ gets the fraction $P_k$ of the URLs;
- when a member fails, few URLs move.

This is the [dynamic partitioning problem](/dynamic-partitioning-problem/) with weights. The draft lists the members in a Proxy Array Membership Table, a text file that agents fetch from a URL. Each line gives a member's name, address, port, status (UP or DOWN) and load factor, and a time to live tells agents when to fetch the table again. The guarantee below is in the random oracle model: the combined hashes of a URL with the members behave as independent uniform numbers.

## The algorithm

All hash arithmetic is on 32-bit unsigned integers, and $\mathrm{ROTL}(x, r)$ rotates $x$ left by $r$ bits. Each agent precomputes, once per table, the member hash $M_k$ and the multiplier $X_k$ of each member. The member hash is the URL hash loop of lines L1 to L3 run over the member name, followed by $M \leftarrow M + M \cdot \texttt{0x62531965}$ and $M \leftarrow \mathrm{ROTL}(M, 21)$.

```pseudo id=main
CARP-ROUTE(url)              ▷ M[1..n]: member hashes, X[1..n]: multipliers
L1  u ← 0
L2  for each byte c of url do
L3      u ← u + ROTL(u, 19) + c                  ▷ mod 2^32
L4  best ← none, bestScore ← −1
L5  for k ← 1 to n do
L6      h ← u XOR M[k]
L7      h ← h + h · 0x62531965                    ▷ mod 2^32
L8      h ← ROTL(h, 21)
L9      s ← h · X[k]                              ▷ a real number
L10     if s > bestScore then best ← k, bestScore ← s
L11 return member best
```

**Load factor multipliers.** Number the members so that $P_1 \le P_2 \le \cdots \le P_n$. Section 3.3 of the draft sets

$$X_1 = (n P_1)^{1/n}, \qquad X_k = \left( \frac{(n - k + 1)(P_k - P_{k-1})}{X_1 X_2 \cdots X_{k-1}} + X_{k-1}^{\,n-k+1} \right)^{1/(n-k+1)} \quad \text{for } 2 \le k \le n.$$

The printed formula in the draft has unbalanced parentheses. The form above is the one that gives the exact shares, and it is the one in the implementation below. With equal load factors every $X_k$ is 1, and CARP is plain rendezvous hashing with the score of lines L6 to L8.

**Failure.** If an agent cannot reach the member chosen by line L11, Section 3.5 sends the request to the member with the second highest score.

## Example

Three members, cache-a, cache-b and cache-c, with load factors 0.2, 0.3 and 0.5 (already in increasing order).

- $X_1 = (3 \cdot 0.2)^{1/3} = 0.6^{1/3} = 0.843433$.
- $X_2 = \left(2 \cdot 0.1 / 0.843433 + 0.843433^2\right)^{1/2} = (0.237126 + 0.711379)^{1/2} = 0.973912$.
- $X_3 = 1 \cdot 0.2 / (0.843433 \cdot 0.973912) + 0.973912 = 0.243478 + 0.973912 = 1.217390$.

The product of the three is 1, as the proof shows it must be. The member hashes are `0x33dc6ff7`, `0x6088ba5a` and `0x8d5504bd`. The URL hash is a short loop: for the string "ab", the hash is 97 after the first byte, and $97 + \mathrm{ROTL}(97, 19) + 98 = 97 + 50{,}855{,}936 + 98 = 50{,}856{,}131$ after the second. The table routes four URLs. It gives each combined hash $h$ of lines L6 to L8 divided by $2^{32}$, and the score $h X_k / 2^{32}$.

| URL | $h$ for a, b, c | score for a, b, c | member |
|---|---|---|---|
| `http://www.example.com/` | 0.7725, 0.2189, 0.1615 | **0.6515**, 0.2131, 0.1966 | cache-a |
| `http://www.example.com/a.html` | 0.0686, 0.6226, 0.0548 | 0.0578, **0.6063**, 0.0668 | cache-b |
| `http://www.example.com/b.html` | 0.0189, 0.9727, 0.7044 | 0.0160, **0.9473**, 0.8575 | cache-b |
| `http://www.example.com/c.html` | 0.5912, 0.0997, 0.2807 | **0.4986**, 0.0971, 0.3417 | cache-a |

In the second row the multipliers swap the order of cache-a and cache-c: the raw hash of cache-a is larger, but the score of cache-c is larger. If cache-b fails, `b.html` goes to its second highest score, cache-c.

**Many URLs.** Route 40,000 URLs of the form `http://www.example.com/` followed by 16 random hex digits (seed 2). With four members cache-a to cache-d and load factors 0.1, 0.2, 0.3 and 0.4, the members get 3,938, 8,021, 11,821 and 16,220 URLs, against 4,000, 8,000, 12,000 and 16,000. Now remove cache-d and give the others 1/6, 2/6 and 3/6. Its 16,220 URLs move, and 1,540 more URLs move between cache-a, cache-b and cache-c, because all three multipliers change. With equal load factors, the removal of cache-c moves exactly its 10,102 URLs and no others.

## Correctness

The loop of line L5 keeps the first member with the largest score seen so far, so the route is the argmax of the scores; it depends only on the URL and the table, so all agents agree. The main result is that the multipliers give the exact shares: if the combined hashes are independent and uniform, member $k$ wins with probability exactly $P_k$. The proof shows that the multipliers are increasing and have product 1, that the largest score falls in the interval $(X_{j-1}, X_j]$ with probability $(n - j + 1)(P_j - P_{j-1})$, and that, given this event, the $n - j + 1$ members $j, \ldots, n$ win with equal probability. Summing over $j \le k$ gives $P_k$. With equal load factors, the removal of a member moves only its own URLs, as in rendezvous hashing. The full proof is below.

## Complexity

- **Lookup.** $\Theta(L)$ for the URL hash and $\Theta(n)$ for the scores, so $\Theta(n + L)$ in every case. In the original setting $n$ is a handful of proxies, and the URL hash dominates.
- **Table change.** Recompute the $n$ member hashes and multipliers: $O(n \log n)$ for the sort of the load factors and $O(n)$ arithmetic after it.
- **Space.** $\Theta(n)$ for the member hashes and the multipliers, and $\Theta(1)$ extra space for a lookup.
- **Balance.** In the random oracle model the number of URLs of member $k$ among $m$ distinct URLs is binomial with mean $m P_k$. This is an expected share, not a cap; a single popular URL still loads one member.

## Properties

- **Stateless and deterministic.** The route is a function of the URL and the membership table.
- **Exact weighted shares** in the random oracle model, from the multipliers.
- **Monotone only with equal load factors.** Then a failed member's URLs go to their second best member and no other URL moves. With unequal factors, a change of the table changes all multipliers and moves some URLs between members that stay.
- **Second choice for free.** The scores give a full order of the members for each URL, so failover needs no extra state.

## Variants and improvements

- **Logarithmic weights.** The score $-w_k / \ln c_k$ of Schindelhauer and Schomaker, on the [rendezvous hashing](/rendezvous-hashing/) page, also gives shares in proportion to the weights, and a change of one weight moves URLs only to or from that member. CARP's multipliers do not have this property.
- **Client side and proxy side.** A user agent can run CARP and pick the member itself. Or a client sends the request to any member, and the member forwards a miss to the member that CARP chooses. RFC 3040 lists both uses.
- **Hash modulo the number of caches.** The simplest hash routing sends a URL to member $h(\text{url}) \bmod n$. It balances as well, but a change of $n$ moves almost every URL, and every moved URL is a miss in its new cache.
- **Other weighted schemes.** A ring with [virtual nodes](/virtual-nodes/) in proportion to the weights, and [weighted random load balancing](/weighted-random-load-balancing/) when there is no need to keep a URL on one member.

## When to use it

Use CARP, or its idea, when a small group of caches must share the URL space without duplicates, when the caches have different sizes, and when every client must be able to compute the owner from a published list. Today the same goal is usually met with rendezvous hashing with a stronger hash and logarithmic weights, or with [consistent hashing](/consistent-hashing/). Squid still offers CARP to choose among parent caches.

## Pitfalls

- **A weak hash.** The URL hash and the combination of lines L6 to L8 mix poorly. With the same 40,000 URLs and four members named proxy1.example.com to proxy4.example.com, equal load factors give 8,819, 10,267, 12,616 and 8,298 URLs, against a mean of 10,000. Members named cache-a to cache-d give 9,995, 9,969, 10,102 and 9,934. Test the shares with your real names and URLs.
- **Load factors as plain multipliers.** Using $X_k = P_k$, or any multipliers proportional to the weights, gives the wrong shares. With weights 1 and 2, the scores $c_1$ and $2 c_2$ give the shares 1/4 and 3/4. CARP's multipliers for 1/3 and 2/3 are $\sqrt{2/3} = 0.816497$ and $\sqrt{3/2} = 1.224745$.
- **The wrong order.** The multipliers must be computed from the smallest load factor to the largest. Run from the largest down, the same recurrence for 0.4, 0.3, 0.2 and 0.1 gives the shares 0.352, 0.286, 0.214 and 0.148.
- **Load factors that do not sum to 1.** The formula assumes $\sum_k P_k = 1$. After a member is removed, normalize the remaining factors before the multipliers are recomputed.
- **Stale tables.** Agents with different tables can send a URL to different members, and the URL is then cached twice. The time to live of the table bounds how long this lasts.
- **Floating point ties.** The draft stores multipliers as 32-bit floats. Equal scores are rare, but agents must break a tie in the same way, for example by member order, or they disagree.

## Implementations

## History

Vinod Valloppillil of Microsoft and Keith W. Ross of the University of Pennsylvania wrote CARP v1.0 as an Internet-Draft; version 03 is dated February 1998. Ross also published an analysis of hash routing for shared web caches in IEEE Network in 1997. The scoring rule is the highest random weight mapping that Thaler and Ravishankar published in 1998. Microsoft Proxy Server and Squid implemented CARP, as RFC 3040 records in 2001. The draft never became an RFC.

## References
