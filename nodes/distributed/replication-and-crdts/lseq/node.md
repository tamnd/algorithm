---
tag: DDRN05
kind: data-structure
slug: lseq
name: LSEQ
aliases:
- LSEQ sequence CRDT
area: distributed/replication-and-crdts
level: advanced
summary: A Logoot variant whose base doubles at each level and which picks at random per level whether to allocate near the left or the right neighbour. This keeps positions short for common editing.
implements: [crdt]
model: word-ram
complexity:
  vars: {N: "the number of elements in the document", L: "the length of the longest position"}
  time: {worst: O(L log N)}
  space: {extra: Θ(N L)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [logoot, op-based-crdt, causal-broadcast]
see_also: [logoot, treedoc, rga, woot, yata, causal-tree, collaborative-text-editing, trie]
sources:
  - paper: doi:10.1145/2494266.2494278
    title: Brice Nédelec, Pascal Molli, Achour Mostefaoui and Emmanuel Desmontils, LSEQ, an adaptive structure for sequences in distributed collaborative editing, DocEng 2013
    locator: pages 37 to 46, the exponential tree with base 2^(4+depth), the boundary+ and boundary- strategies, the random choice of strategy per depth, and the experiments against Logoot
  - paper: doi:10.1109/ICDCS.2009.75
    title: Stéphane Weiss, Pascal Urso and Pascal Molli, Logoot, a scalable optimistic replication algorithm for collaborative editing on P2P networks, ICDCS 2009
    locator: pages 404 to 412, the dense positions that LSEQ keeps
  - paper: doi:10.1145/3301419.3323972
    title: Martin Kleppmann, Victor B. F. Gomes, Dominic P. Mulligan and Alastair R. Beresford, Interleaving anomalies in collaborative text editors, PaPoC 2019
    locator: the example showing that Logoot and LSEQ can interleave text typed concurrently at one place
---

LSEQ is a sequence [CRDT](/crdt/) given by Nédelec, Molli, Mostefaoui and Desmontils in 2013. It keeps the dense positions of [Logoot](/logoot/), lists of (digit, site, clock) triples sorted in lexicographic order, and changes only how new positions are made. First, the number of digits doubles at each level, so the positions form an exponential tree: level 1 has $2^5$ digits, level 2 has $2^6$, and so on. Second, there are two allocation strategies, boundary+ (near the left neighbour) and boundary− (near the right neighbour), and LSEQ picks one at random for each level. Logoot positions grow linearly when users type at the end or at the start; the LSEQ paper claims sublinear growth whatever the editing behaviour, and shows it in experiments.

## In plain words

Logoot numbers letters so that new numbers always fit between old ones. It always picks a number just to the right of the left neighbour. That works well if you type forwards, and very badly if you type backwards, because each new letter then needs a longer number.

LSEQ makes two changes. Each deeper level of numbers has twice as many choices as the level above. And at each level, a coin decides once whether to pick numbers near the left neighbour or near the right neighbour. Whatever way you type, some levels suit you, and when a level fills up, the next level has twice as much room.

## The abstract type

LSEQ implements a replicated list with updates INSERT$(i, x)$ and DELETE$(i)$ and the query READ. It is an [op-based CRDT](/op-based-crdt/).

**Model.** As for Logoot: sites with distinct numeric ids, and each operation delivered once at every replica, in a causal order, so that a delete arrives after its insert.

**Specification.** Replicas that have run the same operations show the same list. A local INSERT$(i, x)$ makes $x$ the $i$-th element at its source, and DELETE$(i)$ removes the $i$-th element. The relative order of two elements never changes.

## Representation

A position is a list of triples $(d, s, c)$, compared in [lexicographic order](/lexicographic-order/), as in [Logoot](/logoot/). The digit at level $i$, counting from 0, lies in $[0, \mathrm{base}(i))$ with $\mathrm{base}(i) = 2^{4 + i + 1}$, so 32, 64, 128 and so on. A position read as its digits is a path in a [trie](/trie/) whose fan-out doubles at each level. Each replica keeps a site id, a clock, the sorted pairs (position, value), a parameter $\mathit{boundary}$, and a map from levels to the strategy chosen there. As in Logoot, every position ends with a digit of at least 1.

## Operations

```pseudo id=main
ALLOC(p, q)                                           ▷ a position strictly between p and q
    out ← [];  bound ← (q ≠ ⊤);  i ← 0
    loop
L1      pd ← the digit of p[i], or 0 if p has run out
L2      qd ← the digit of q[i] if bound, else base(i)
L3      if qd − pd ≥ 2 then
L4          step ← min(boundary, qd − pd − 1)
L5          if level i has no strategy yet then strategy[i] ← boundary+ or boundary−, each with probability 1/2
L6          if strategy[i] = boundary+ then d ← pd + RANDOM(1, step)
L7          else d ← qd − RANDOM(1, step)                ▷ boundary−
            return out + [(d, site, clock)]
L8      copy one triple and go down, as in lines L6 to L8 of Logoot's ALLOC
L9      i ← i + 1
```

Lines L1 to L4 and L8 are the level walk of [Logoot](/logoot/). Line L2 takes the base of the current level, which doubles with depth. Line L5 fixes the strategy of a level the first time the replica allocates there, and lines L6 and L7 apply it: boundary+ stays close to the left neighbour, which leaves room for typing forwards, and boundary− stays close to the right neighbour, which leaves room for typing backwards. In both cases the digit is strictly between $pd$ and $qd$.

Local and remote operations are those of Logoot: a local insert allocates between the positions of its two neighbours and broadcasts the pair, a delete removes the pair, and a remote operation is a sorted insert or a removal.

## Example

Boundary 10, two sites 1 and 2. In this run, site 1 picked boundary+ at level 1 and site 2 picked boundary−.

| step | site | operation | allocation | position |
| --- | --- | --- | --- | --- |
| 1 | 1 | insert H at 0 | level 1, base 32, boundary+: $0 + 2$ | $\langle(2,1,1)\rangle$ |
| 2 | 1 | insert i at 1 | between 2 and $\top$: $2 + 5$ | $\langle(7,1,2)\rangle$ |
| 3 | 1 | insert e at 1 | between 2 and 7, step 4, boundary+: $2 + 1$ | $\langle(3,1,3)\rangle$ |
| 3 | 2 | insert o at 1, at the same time | between 2 and 7, step 4, boundary−: $7 - 1$ | $\langle(6,2,1)\rangle$ |
| 4 | both | apply the other's insert | sort | H e o i at both sites |

**Going one level down.** In another run, site 1 picked boundary− at level 1 and made H at $\langle(26,1,1)\rangle$ and i at $\langle(27,1,2)\rangle$. Between them no digit is free, so the insert of e copies $(26,1,1)$ and goes to level 2, where the base is 64. It picks boundary+ there and gets $\langle(26,1,1),(6,1,3)\rangle$.

## Correctness

ALLOC differs from Logoot's only in the digit it picks at the level with room, and that digit $d$ satisfies $pd < d < qd$ for both strategies, with $d \ge 1$ and $d < \mathrm{base}(i)$. The [correctness proof](proofs/correctness.md) shows this and then uses the argument of the [Logoot proof](/logoot/): the new position lies strictly between its neighbours and ends with a digit of at least 1, positions are unique, and the state is the set of inserted and not deleted pairs, so replicas that ran the same operations converge. The strategy map is local to each replica and plays no part in convergence.

**Growth.** The LSEQ paper states sublinear space complexity whatever the editing behaviour, and supports it with experiments; it leaves a proof of a polylogarithmic bound as future work. The tests check only that, in seeded runs of 2000 inserts at the end, at the start, and at random places, the average position has fewer than 12 levels.

## Complexity

Let $N$ be the number of elements and $L$ the length of the longest position. The costs are those of Logoot: ALLOC takes $O(L)$, an insert or delete in a balanced search tree takes $O(L \log N)$, and READ takes $\Theta(N)$. A position at depth $k$ has $\sum_{i=1}^{k} (4 + i) = 4k + k(k+1)/2$ bits of digits, plus a site and a clock per level.

In one seeded run of the code on these pages, with boundary 10 for both, and Logoot with base $2^{10}$ (digit bits only):

| inserts | pattern | Logoot average levels | Logoot bits | LSEQ average levels | LSEQ bits |
| --- | --- | --- | --- | --- | --- |
| 1000 | at the end | 3.25 | 32.5 | 8.06 | 69.2 |
| 1000 | at the start | 168.9 | 1689 | 8.25 | 73.2 |
| 1000 | at random places | 3.83 | 38 | 3.49 | 22.5 |
| 10000 | at the end | 27.4 | 274 | 10.6 | 105 |
| 10000 | at the start | 1688 | 16880 | 11.1 | 113 |
| 10000 | at random places | 4.89 | 49 | 4.58 | 32 |

For typing at the end, Logoot with a large base is shorter at first, because its first level holds many digits, but its length grows linearly while LSEQ's grows slowly. For typing at the start, Logoot grows linearly with a large slope. LSEQ is about the same in all three patterns.

## Variants

- **One fixed strategy.** With boundary+ at every level and a fixed base, LSEQ is Logoot. With boundary− at every level, typing at the end grows positions linearly, the mirror image of Logoot's problem with typing at the start. The random choice per level avoids both.
- **Other base functions.** The base can grow by other rules; doubling is the choice of the paper.
- **How LSEQ differs from the other sequence CRDTs.** Like [Logoot](/logoot/) it has no tombstones and dense positions, and it shares Logoot's interleaving of concurrent text shown by Kleppmann et al. (2019). [Treedoc](/treedoc/) uses a binary tree of positions and can rebalance it, at the cost of coordination. [RGA](/rga/), [YATA](/yata/), [WOOT](/woot/) and the [causal tree](/causal-tree/) store neighbour ids and keep tombstones instead.

## When to use it

Use LSEQ instead of Logoot when you want dense positions and no tombstones and the editing pattern is not known in advance, since its positions stay short for typing forwards, backwards and at random. When interleaving of concurrent words matters, prefer a design based on neighbour ids.

## Pitfalls

- **Picking the strategy once for all levels.** Then one direction of typing fills every level, as in Logoot. The choice is made for each level separately.
- **Different base functions at different replicas.** All replicas must agree on $\mathrm{base}(i)$, since it decides which digits are valid and where the end of a level lies.
- **Counting only levels.** Deeper levels have more bits per digit, so compare sizes in bits, as the table does.
- **Interleaving.** Concurrent words typed at one place can mix letter by letter, as in Logoot.

## Implementations

The Python class follows the main block with `# @line` markers for L1 to L9 and keeps the positions in a sorted Python list. The tests check the bases and the bit count, check that each level keeps one strategy, find interleaving of two concurrent words, check growth for typing at the end, at the start and at random places, and run seeded runs with 2 to 5 sites, causal delivery and up to 300 operations. They check that all replicas converge, that local edits land at their index, that every digit is below the base of its level, and that one order explains every replica's list.

## History

Nédelec, Molli, Mostefaoui and Desmontils presented LSEQ at DocEng 2013. They showed that Logoot's boundary strategy suits only typing forwards, and combined an exponential tree with two opposite strategies chosen at random per level. Kleppmann, Gomes, Mulligan and Beresford showed in 2019 that LSEQ, like Logoot, can interleave concurrent insertions.

## References
