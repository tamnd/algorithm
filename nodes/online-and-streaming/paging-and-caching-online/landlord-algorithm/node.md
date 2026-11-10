---
tag: ESNB1H
kind: algorithm
slug: landlord-algorithm
name: Landlord algorithm
aliases:
- Young's landlord
- Landlord
- LANDLORD
area: online-and-streaming/paging-and-caching-online
level: research
summary: Credit-based k-competitive algorithm for weighted caching, generalizing GreedyDual.
solves: [weighted-paging-problem]
model: word-ram
complexity:
  vars: {n: the number of requests, k: the cache size}
  time: {worst: O(n k)}
  space: {extra: O(k)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1998
  people: [Neal E. Young]
  note: Young gave GreedyDual for weighted caching in 1994 and the Landlord rule for files of any size and cost at SODA 1998, with the journal version in 2002. Cao and Irani found the same rule, GreedyDual-Size, for web caches in 1997.
prereqs: [weighted-paging-problem, competitive-ratio, potential-function]
see_also: [greedy-dual, gdsf, variable-size-caching, lru, marking-algorithm, belady-algorithm, sleator-tarjan-paging-bound]
sources:
  - paper: doi:10.1007/s00453-001-0124-5
    title: "Neal E. Young, On-line file caching, Algorithmica 33(3) (2002), 371-383"
    locator: the Landlord algorithm and the proof that it is k/(k - h + 1)-competitive for file caching
  - paper: doi:10.1007/BF01189992
    title: "Neal E. Young, The k-server dual and loose competitiveness for paging, Algorithmica 11(6) (1994), 525-541"
    locator: the GreedyDual algorithm for weighted caching and its bound k/(k - h + 1)
  - paper: "Pei Cao and Sandy Irani, Cost-aware WWW proxy caching algorithms, Proceedings of the USENIX Symposium on Internet Technologies and Systems, 1997"
    locator: the GreedyDual-Size rule for web proxy caches
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 3, paging, deterministic algorithms, the section on weighted caching and GreedyDual
---

The Landlord algorithm is a deterministic online rule for *file caching*, where each file has its own size and its own cost to fetch. Each file in the cache holds a credit, like rent paid in advance. When room is needed, all files pay rent in proportion to their size, and a file whose credit reaches zero is evicted. Young proved that Landlord is $k$-competitive, the best ratio for a deterministic rule, and $k/(k-h+1)$-competitive against an optimum with a smaller cache of size $h$. It generalizes GreedyDual for [weighted paging](/weighted-paging-problem/) and [LRU](/lru/) for [paging](/paging-problem/).

## In plain words

A cache is like a small building with rooms for rent. Each file that lives there has some money in its account. When a file comes in, it gets money equal to what it cost to fetch it. When a new file needs space and the building is full, every file pays rent. Big files pay more rent, because they use more space. A file with no money left must leave.

When a file that is already in the cache is used again, its account can be filled up again. So files that are used often, or that are expensive to fetch again, stay longer. Files that are big and cheap leave first. This simple rule is never much worse than the best plan made with full knowledge of the future.

## The problem

There is a set of files, and file $f$ has a size $\mathrm{size}(f)$, a positive integer, and a cost $\mathrm{cost}(f) \ge 0$. The cache holds files of total size at most $k$, and $\mathrm{size}(f) \le k$ for each $f$. A request for $f$ is free if $f$ is in the cache. Otherwise $f$ must be fetched at cost $\mathrm{cost}(f)$, and files may be evicted to make room. The cost is the total fetch cost. With all sizes $1$ this is [weighted paging](/weighted-paging-problem/), and with all sizes and costs $1$ it is [paging](/paging-problem/). We compare with an offline optimum $\mathrm{OPT}_h$ whose cache has size $h \le k$.

## The algorithm

```pseudo id=main
LANDLORD(σ, k)
L1  total ← 0, the cache is empty
L2  for each request f in σ do
L3      if f is in the cache then raise credit[f] to any value up to cost(f)
L4      else while the files in the cache and f do not fit in size k do
L5          if some file g in the cache has credit[g] = 0 then evict g
L6          else Δ ← min over g in the cache of credit[g] / size(g); credit[g] ← credit[g] − Δ · size(g) for each g in the cache
L7          put f in the cache, credit[f] ← cost(f), total ← total + cost(f)
L8  return total
```

Line L6 charges rent: the rent per unit of size is $\Delta$, the largest value that keeps all credits at least $0$. After line L6 at least one file has credit $0$, so the next round of line L5 evicts a file, and the loop stops. Line L3 leaves a free choice. The two usual choices are a *full reset* to $\mathrm{cost}(f)$ and *no change*. The bound holds for each choice. The program evicts, among the files with credit $0$, the one used least recently.

## Example

The cache size is $k = 4$. The files are $a$ (size 1, cost 4), $b$ (size 2, cost 6), $c$ (size 1, cost 1) and $d$ (size 2, cost 2). Line L3 uses the full reset.

| request | rent $\Delta$ | evicted | cache with credits after the request | total |
|---|---|---|---|---|
| a | | | a 4 | 4 |
| b | | | a 4, b 6 | 10 |
| c | | | a 4, b 6, c 1 | 11 |
| d | 1, then 2 | c, then b | a 1, d 2 | 13 |
| a | | | a 4, d 2 | 13 |
| c | | | a 4, d 2, c 1 | 14 |
| b | 1 | d | a 3, c 0, b 6 | 20 |

For $d$, the first rent is $\Delta = \min(4/1, 6/2, 1/1) = 1$, which leaves $a$ with 3, $b$ with 4 and $c$ with 0. So $c$ leaves, but there is still no room. The second rent is $\Delta = \min(3/1, 4/2) = 2$, so $b$ reaches $0$ and leaves. For the last $b$, both $d$ and $c$ reach $0$; $d$ is used less recently, and its removal makes enough room. The offline optimum with $h = 4$ pays $18$ here, and Landlord pays $20$, far below $k \cdot 18$.

## Correctness

The proof uses the [potential function](/potential-function/)

$$\Phi = (h - 1) \sum_{f \in \mathrm{LL}} \mathrm{credit}[f] + k \sum_{f \in \mathrm{OPT}} \bigl( \mathrm{cost}(f) - \mathrm{credit}[f] \bigr),$$

where $\mathrm{LL}$ and $\mathrm{OPT}$ are the two caches and the credit of a file outside $\mathrm{LL}$ is $0$. A fetch by the optimum raises $\Phi$ by at most $k \cdot \mathrm{cost}(f)$. Each step of Landlord lowers $\Phi$ by at least $(k - h + 1)$ times its own cost. The rent step is the key: it does not raise $\Phi$, because the files of Landlord fill more than $k - \mathrm{size}(f)$ while the shared files fill at most $h - \mathrm{size}(f)$. The sum gives $(k - h + 1)\,\mathrm{LL}(\sigma) \le k \cdot \mathrm{OPT}_h(\sigma)$ from empty caches. The full proof is below.

## Complexity

Each round of line L6 takes $O(c)$ time for the $c \le k$ files in the cache, and each round is followed by an eviction. A file is evicted at most once for each time it is fetched, so the total time is $O(nk)$ for $n$ requests. The rent can also be kept as a global offset: store $L + \mathrm{credit}[f]$ in a priority queue and raise $L$ instead of all credits. This is how GreedyDual-Size is built in web caches, and it takes $O(\log k)$ time per operation. The space is $O(k)$, one credit for each file in the cache.

## Properties

- **$k$-competitive.** With $h = k$ and empty start caches, $\mathrm{LL}(\sigma) \le k \cdot \mathrm{OPT}(\sigma)$ with additive constant $0$. No deterministic algorithm does better, even for paging (Sleator and Tarjan 1985).
- **Resource augmentation.** $\mathrm{LL}(\sigma) \le \frac{k}{k-h+1} \mathrm{OPT}_h(\sigma)$ for $h \le k$. With twice the cache size of the optimum, the ratio is about $2$.
- **It contains LRU and GreedyDual.** With sizes $1$, Landlord is Young's GreedyDual for weighted paging. With sizes and costs $1$ and the full reset, and ties broken by least recent use, it is LRU. The tests check the second claim.
- **Any reset works.** The proof allows any raise of the credit on a hit. So Landlord is a family of rules, and a system can choose the reset by experiment.

## Variants and improvements

- **GreedyDual-Size (GDS).** Cao and Irani used the same rule with the full reset for web proxies, where documents differ widely in size and in fetch cost.
- **GreedyDual-Size-Frequency.** [GDSF](/gdsf/) adds a frequency count to the credit, to keep popular objects longer.
- **Randomized algorithms.** For weighted paging, randomized algorithms reach $O(\log k)$ against an [oblivious adversary](/oblivious-adversary/) (Bansal, Buchbinder and Naor 2007). For general file caching, $O(\log k)$ is also known (Adamaszek, Czumaj, Englert and Räcke 2012).
- **Offline.** The offline file caching problem with general sizes is NP-hard, so the offline optimum in the tests comes from a brute-force search over cache contents.

## When to use it

Use Landlord, or its GreedyDual-Size form, when objects have different sizes or different costs to fetch again, as in web caches, CDN caches and caches of query results. For pages of one size and one cost, LRU or [CLOCK](/clock/) is simpler and has the same bound. If the cost is the number of bytes fetched, set $\mathrm{cost}(f) = \mathrm{size}(f)$; if the cost is the number of misses, set $\mathrm{cost}(f) = 1$, and Landlord then prefers to evict large files.

## Pitfalls

- **Charging the same rent to each file.** The rent must be proportional to the size. With a flat rent, a large cheap file can stay for a long time and block many small files.
- **Floating point credits.** Repeated subtraction of rents in floating point can leave a credit at $10^{-17}$ instead of $0$, and the loop of line L4 then makes one extra round. Use exact numbers, or compare with a tolerance, or use the global offset form.
- **Files larger than the cache.** A file with $\mathrm{size}(f) > k$ cannot be served from the cache. The model needs $\mathrm{size}(f) \le k$, and a system must bypass the cache for such files.
- **Integer sizes in the proof.** The proof uses that the free space is an integer, so that Landlord fills at least $k - \mathrm{size}(f) + 1$ when it must evict. With real sizes, scale them to integers first.

## Implementations

## History

Sleator and Tarjan proved in 1985 that LRU is $k$-competitive for paging and that $k/(k-h+1)$ is the best ratio against a cache of size $h$. Young introduced GreedyDual for weighted caching in 1994, in a paper that derived it from the dual of a linear program for the k-server problem on a star. Cao and Irani proposed GreedyDual-Size for web proxy caches in 1997. Young then gave the Landlord rule for general file caching, with a short potential proof, at SODA 1998, and in Algorithmica in 2002.

## References
