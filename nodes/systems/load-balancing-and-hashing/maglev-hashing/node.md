---
tag: DA1P19
kind: algorithm
slug: maglev-hashing
name: Maglev hashing
aliases:
- Maglev consistent hashing
- Maglev lookup table
area: systems/load-balancing-and-hashing
level: advanced
summary: Fill a lookup table of prime size M by letting backends take turns at their next preferred empty slot. Each backend gets the floor or ceiling of M/N slots; a change moves a few extra slots.
solves: [dynamic-partitioning-problem]
model: word-ram
complexity:
  vars: {n: the number of backends, m: "the table size, a prime"}
  time: {worst: O(n m), average: O(m log m)}
  space: {extra: Θ(m + n)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 2016
  people: [Daniel E. Eisenbud, Cheng Yi, Carlo Contavalli, Cody Smith, Roman Kononov, Eric Mann-Hielscher, Ardas Cilingiroglu, Bin Cheyney, Wentao Shang, Jinnah Dylan Hosein]
  note: The Maglev paper at NSDI 2016 describes the software network load balancer of Google and its lookup table, which Google had used for several years before.
prereqs: [hash-function, rendezvous-hashing, consistent-hashing]
see_also: [layer-4-load-balancing, load-balancer, ecmp-hashing, jump-consistent-hash, monotonicity-property, balance-property, prime-number]
sources:
  - url: https://www.usenix.org/conference/nsdi16/technical-sessions/presentation/eisenbud
    title: Daniel E. Eisenbud, Cheng Yi, Carlo Contavalli, Cody Smith, Roman Kononov, Eric Mann-Hielscher, Ardas Cilingiroglu, Bin Cheyney, Wentao Shang and Jinnah Dylan Hosein, Maglev, a fast and reliable software network load balancer, 13th USENIX Symposium on Networked Systems Design and Implementation (NSDI), 2016, pages 523 to 535
    locator: Section 3.4 (Consistent Hashing), Pseudocode 1 and Table 1 on page 528; Section 3.3 (backend selection with a connection tracking table); Section 5.3 (the evaluation of the consistent hashing)
  - paper: doi:10.1109/90.663936
    title: David G. Thaler and Chinya V. Ravishankar, Using name-based mappings to increase hit rates, IEEE/ACM Transactions on Networking 6(1), 1998, pages 1 to 14
    locator: the highest random weight mapping, which the Maglev paper cites as rendezvous hashing
  - paper: doi:10.1145/258533.258660
    title: David Karger, Eric Lehman, Tom Leighton, Rina Panigrahy, Matthew Levine and Daniel Lewin, Consistent hashing and random trees, Proceedings of the 29th ACM Symposium on Theory of Computing (STOC), 1997
    locator: the monotonicity and balance properties that Maglev trades against an even load
---

Maglev hashing builds a lookup table of prime size $M$ in which each of $N$ backends owns either $\lfloor M/N \rfloor$ or $\lceil M/N \rceil$ slots, and then sends a key, such as the hash of a connection's 5-tuple, to the backend in slot $h(\text{key}) \bmod M$. Each backend has a preference order over the slots, and the backends take turns taking their next preferred empty slot. It was designed for Maglev, the software [layer 4 load balancer](/layer-4-load-balancing/) of Google (Eisenbud et al., NSDI 2016). Unlike [rendezvous hashing](/rendezvous-hashing/) and the [ring](/consistent-hashing/), it puts even load first: when a backend leaves, its slots move and a small number of other slots move too, so it does not have the [monotonicity property](/monotonicity-property/) exactly.

## In plain words

Picture a board with a fixed, large number of seats, and a group of backends that want seats. Each backend has its own list of all the seats, in its own shuffled order. The backends take turns: in each turn a backend takes the first seat on its list that is still free. When the board is full, every backend has the same number of seats, give or take one.

To route a connection, hash it to a seat and send it to the backend in that seat. That is one array read. When a backend leaves, the board is filled again from the start with the remaining backends. Because each backend still follows its own list, most backends get almost the same seats as before. A few seats still change hands, because the turns are different.

## The problem

A load balancer receives packets of many connections and must send all packets of one connection to the same backend among $N$ backends. It needs:

- an even spread, so that no backend is overloaded (the paper prefers this to minimal movement);
- a lookup in a few nanoseconds, on every packet;
- few changed assignments when a backend is added or removed, so that connections whose state is lost (for example, after a load balancer restart) still reach the right backend.

This is the [dynamic partitioning problem](/dynamic-partitioning-problem/) for a packet path. The key is a hash of the 5-tuple. Maglev also keeps a connection tracking table, so the hash table is the fallback when the tracking state is missing.

## The algorithm

Each backend $i$ has a name. Two hash functions give

$$\text{offset}[i] = h_1(\text{name}_i) \bmod M, \qquad \text{skip}[i] = h_2(\text{name}_i) \bmod (M - 1) + 1,$$

and the preference list of backend $i$ is $\text{permutation}[i][j] = (\text{offset}[i] + j \cdot \text{skip}[i]) \bmod M$ for $j = 0, \ldots, M - 1$. Because $M$ is prime and $1 \le \text{skip}[i] \le M - 1$, this list is a permutation of the slots.

```pseudo id=main
POPULATE(offset[0 .. N − 1], skip[0 .. N − 1], M)      ▷ M prime, N ≥ 1
L1  next[i] ← 0 for each backend i
L2  entry[c] ← −1 for each slot c
L3  filled ← 0
L4  while true do
L5      for i ← 0 to N − 1 do
L6          c ← (offset[i] + next[i] · skip[i]) mod M
L7          while entry[c] ≥ 0 do                      ▷ skip filled slots
L8              next[i] ← next[i] + 1, c ← (offset[i] + next[i] · skip[i]) mod M
L9          entry[c] ← i
L10         next[i] ← next[i] + 1, filled ← filled + 1
L11         if filled = M then return entry

LOOKUP(key)
L12 return entry[h(key) mod M]
```

This is Pseudocode 1 of the paper, with the permutation computed on the fly instead of stored. On any change of the backend set, Maglev runs POPULATE again with the new list and swaps in the new table.

## Example

The paper's own example has $M = 7$ and three backends B1, B2 and B3 with (offset, skip) pairs (3, 4), (0, 2) and (3, 1). The preference lists are:

| backend | preference list |
|---|---|
| B1 | 3, 0, 4, 1, 5, 2, 6 |
| B2 | 0, 2, 4, 6, 1, 3, 5 |
| B3 | 3, 4, 5, 6, 0, 1, 2 |

Round 1: B1 takes 3, B2 takes 0, and B3 finds 3 taken and takes 4. Round 2: B1 finds 0 and 4 taken and takes 1, B2 takes 2, and B3 takes 5. Round 3: B1 finds 5 and 2 taken and takes 6. The table is full after 7 turns.

| slot | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| with B1, B2, B3 | B2 | B1 | B2 | B1 | B3 | B3 | B1 |
| without B2 | B1 | B1 | B1 | B1 | B3 | B3 | B3 |

Without B2, slots 0 and 2 (the slots of B2) change, as they must. Slot 6 also changes, from B1 to B3: B1 now gets its third slot earlier in its list, and B3 reaches slot 6 first. With 7 slots this is one extra change; the counts are 3, 2, 2 before and 4, 3 after.

**Measured disruption.** The implementation below uses BLAKE2b for $h_1$ and $h_2$ and backends named b0, b1, and so on. The table gives the fraction of slots that change when one backend is removed. The necessary part is the share of the removed backend, about $1/N$; the rest is extra.

| $M$ | $N$ | slots per backend | changed on removing the last backend | of which extra | changed on adding one |
|---|---|---|---|---|---|
| 65,537 | 10 | 6,553 or 6,554 | 10.29% | 0.29% | 9.32% |
| 65,537 | 100 | 655 or 656 | 1.57% | 0.57% | 1.50% |
| 5,003 | 10 | 500 or 501 | 10.73% | 0.74% | 10.15% |
| 5,003 | 100 | 50 or 51 | 3.80% | 2.80% | 3.70% |
| 251 | 10 | 25 or 26 | 15.54% | 5.58% | 16.73% |

The extra movement falls as $M/N$ grows. The paper chooses $M$ larger than $100 N$, with $M = 65537$ as its default size.

## Correctness

Because $M$ is prime and $0 < \text{skip}[i] < M$, the list of each backend is a permutation of the slots. Each pointer $\text{next}[i]$ only passes filled slots, so while some slot is empty, backend $i$ still has an empty slot further down its list, and its turn succeeds. So each turn fills exactly one slot, the run stops after exactly $M$ turns with a full table, and the turns go round the backends in order. Writing $M = qN + r$, backends $0$ to $r - 1$ get $q + 1$ slots and the others get $q$. There is no exact statement about movement: removing a backend changes the order of the turns of the others. The full proof is below.

## Complexity

- **Lookup.** $O(1)$: one hash and one array read. This is the reason for the design.
- **Population, worst case.** Each backend's pointer moves at most $M$ times, so POPULATE takes $O(NM)$ steps. The paper states a worst case of $O(M^2)$, reached when $N = M$ and all backends hash to the same list.
- **Population, typical case.** If the lists behave like random permutations, the turn that fills the $n$-th slot needs about $M/(M - n)$ tries, so the total is about $\sum_{n=1}^{M} M/n = O(M \log M)$. This is the paper's argument; the lists are not truly random, so it is a heuristic estimate, not a proved bound.
- **Space.** $\Theta(M)$ for the table and $\Theta(N)$ for the pointers.
- **Balance.** Exact: each backend has $\lfloor M/N \rfloor$ or $\lceil M/N \rceil$ slots. With $M > 100N$ the shares differ by less than 1% of a share. The traffic share also depends on the spread of the connection hashes over the slots.
- **Movement.** Not bounded by a theorem. Measured values are in the example table.

## Properties

- **Near-perfect balance** by construction (Theorem 2 of the proof).
- **Approximate monotonicity.** Most slots keep their backend on a change, but the movement is above the minimum. Maglev accepts this because its connection tracking table keeps existing connections on their backends.
- **Deterministic.** Two load balancers with the same backend list and the same order build the same table, so connections reach the same backend through either one.
- **Order dependent.** The turns follow the index order of the backends. All load balancers must sort the backends the same way.
- **Not online.** A change rebuilds the whole table.

## Variants and improvements

- **Weighted backends.** The paper says weights can be given by changing how often each backend takes a turn, without details. A backend of weight 2 takes two turns per round, for example.
- **Better permutations.** The paper notes that other ways to make the lists, such as the [Fisher-Yates shuffle](/fisher-yates-shuffle/) seeded by the name, give better random permutations at the cost of more state.
- **Connection tracking.** Maglev first looks up the 5-tuple in a local table of recent connections, and uses the hash table only for new connections or lost state. The table hash is what keeps the choice the same across load balancers.
- **Related schemes.** [Rendezvous hashing](/rendezvous-hashing/) has exact minimal movement and an $O(N)$ lookup. [Jump consistent hash](/jump-consistent-hash/) has no table but needs numbered buckets. A [hash ring](/hash-ring/) with [virtual nodes](/virtual-nodes/) needs many points per backend for the balance that Maglev gets by construction.

## When to use it

Use Maglev hashing in a packet path or any path where the lookup must be one memory read, the backends change rarely compared with the number of lookups, and an even load matters more than a small extra movement. It fits [layer 4 load balancing](/layer-4-load-balancing/) behind [ECMP](/ecmp-hashing/), where several balancers must agree on the backend of a flow without sharing state. For a cache where each extra moved key is a miss, a scheme with exact monotonicity may be better.

## Pitfalls

- **A table size that is not prime.** If $M$ and some skip share a factor, that backend's list visits only part of the table. Its turn can then find no empty slot, and the loop of line L7 never stops. Use a prime $M$.
- **A table that is too small.** With $M$ close to $N$, the counts differ by 1 out of a few, which is a large relative error, and the extra movement grows (5.58% extra with $M = 251$, $N = 10$). Choose $M > 100 N$.
- **Different backend orders.** Two balancers that list the same backends in different orders build different tables and send a flow to different backends.
- **Claiming minimal disruption.** The movement is small but above the minimum. Do not count on a key staying when an unrelated backend leaves.
- **Rebuilding on the packet path.** POPULATE costs $O(M \log M)$ steps or more. Build the new table aside and swap a pointer.

## Implementations

## History

Google ran Maglev as its network load balancer for several years before the NSDI 2016 paper by Eisenbud and colleagues. The paper cites consistent hashing (Karger et al., 1997) and rendezvous hashing (Thaler and Ravishankar, 1998), and argues that both put minimal disruption first, while Maglev needs an even load over hundreds of backends with a small table. The lookup table and its population by turns are the paper's contribution; the name Maglev hashing comes from the paper.

## References
