---
tag: D9EX5G
kind: data-structure
slug: woot
name: WOOT
aliases:
- WithOut Operational Transform
area: distributed/replication-and-crdts
level: advanced
summary: The first sequence CRDT for text. Each W-character keeps the ids of its neighbours at creation, deletes leave it hidden, and a recursive integration places remote characters.
implements: [crdt]
model: word-ram
complexity:
  vars: {H: "the number of characters ever inserted, hidden ones included"}
  time: {worst: O(H^3)}
  space: {extra: Θ(H)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [op-based-crdt, tombstone, collaborative-text-editing]
see_also: [yata, rga, causal-tree, logoot, treedoc, operational-transformation, collaborative-text-editing, tombstone]
sources:
  - paper: doi:10.1145/1180875.1180916
    title: Gérald Oster, Pascal Urso, Pascal Molli and Abdessamad Imine, Data consistency for P2P collaborative editing, CSCW 2006
    locator: pages 259 to 268, W-characters, the generation of insert and delete, the pool of waiting operations, and the IntegrateIns procedure
  - paper: doi:10.1145/2034691.2034717
    title: Mehdi Ahmed-Nacer, Claudia-Lavinia Ignat, Gérald Oster, Hyun-Gul Roh and Pascal Urso, Evaluating CRDTs for real-time document editing, DocEng 2011
    locator: pages 103 to 112, the cost of WOOT integration, cubic in the number of characters, against the quadratic WOOTO and WOOTH
  - url: https://www.isa-afp.org/entries/WOOT_Strong_Eventual_Consistency.html
    title: Emin Karayel and Edgar Gonzàlez, Strong eventual consistency of the collaborative editing framework WOOT, Archive of Formal Proofs, 2020
    locator: the formal proof in Isabelle/HOL that WOOT is strongly eventually consistent
  - paper: doi:10.1145/3301419.3323972
    title: Martin Kleppmann, Victor B. F. Gomes, Dominic P. Mulligan and Alastair R. Beresford, Interleaving anomalies in collaborative text editors, PaPoC 2019
    locator: the discussion of WOOT, for which the absence of interleaving is conjectured but not proved
---

WOOT (WithOut Operational Transform) is a sequence [CRDT](/crdt/) for collaborative text, given by Oster, Urso, Molli and Imine in 2006 as an alternative to [operational transformation](/operational-transformation/). Each character is a W-character: a unique id (site, clock), a value, and the ids of the characters just before and just after it at the moment it was typed. A delete only hides a character, so every id named by an operation stays in the sequence. To place a remote character between its two neighbours, a replica looks at the characters that now lie between them, keeps only those whose own neighbours lie outside that gap, finds the place of the new character among them by id, and repeats on the smaller gap. Operations whose neighbours have not arrived wait in a pool, so WOOT needs no causal broadcast.

## In plain words

Every letter remembers its left and right neighbour from the moment it was typed. On another screen, the letter must go somewhere between those two.

If other letters now sit in that gap, the editor does not compare against all of them. It picks only the letters that were themselves typed "straight into this gap", meaning their own neighbours are the gap's edges or further out. Among these, it sorts by id to find a smaller gap, and it repeats until the gap is empty.

A deleted letter is never thrown away, only hidden, because some other letter may still name it as a neighbour. An operation that names a letter which has not arrived yet waits.

## The abstract type

WOOT implements a replicated list with updates INSERT$(i, x)$ and DELETE$(i)$ and the query READ. It is an [op-based CRDT](/op-based-crdt/).

**Model.** There are sites with distinct numeric ids. Operations are broadcast with eventual delivery, in any order and possibly more than once. An insert can run when its two neighbours are present, and a delete when its character is present; until then the operation waits in a pool.

**Specification.** Replicas that have run the same operations show the same sequence. A local INSERT$(i, x)$ makes $x$ the $i$-th visible character at its source, and DELETE$(i)$ hides the $i$-th one. Every character lies after its previous neighbour and before its next neighbour at every replica. Oster et al. state these as convergence, causality preservation through the pool, and intention preservation.

## Representation

A replica stores the sequence of W-characters, hidden ones included, between two marks $c_b$ (begin) and $c_e$ (end), a set of hidden ids, a map from ids to W-characters, and the pool. A W-character is $(\mathit{id}, \mathit{value}, \mathit{prev}, \mathit{next})$. Ids are compared as (site, clock) pairs in [lexicographic order](/lexicographic-order/). At its source, $\mathit{prev}$ and $\mathit{next}$ are the visible characters at positions $i - 1$ and $i$, or the marks.

## Operations

```pseudo id=main
INTEGRATE(c, cp, cn)                                  ▷ place c between cp and cn
L1  S′ ← the characters strictly between cp and cn
L2  if S′ is empty then
L3      put c right before cn;  return
L4  L ← [cp]
L5  for each d ∈ S′ in order with prev(d) at or before cp and next(d) at or after cn do append d to L
    append cn to L
L6  i ← 1
L7  while i < |L| − 1 and id(L[i]) < id(c) do i ← i + 1
L8  INTEGRATE(c, L[i − 1], L[i])                      ▷ a smaller gap
```

Lines L4 and L5 keep the characters that were typed straight into the gap, not into a smaller gap inside it. These characters are ordered by id among themselves at every replica, and line L7 finds where $c$ goes among them. Line L8 recurses into the gap between two consecutive kept characters, which is strictly smaller.

**Local insert.** At the source, $\mathit{cp}$ and $\mathit{cn}$ are the visible characters $i - 1$ and $i$. Hidden characters may lie between them, so the source also runs INTEGRATE, and $c$ ends up between them, at visible index $i$. **Delete.** Hide the character. **Pool.** On receipt, put the operation in the pool, then run every operation in the pool whose characters are present until none is left that can run; skip an insert whose id is already present.

## Example

Three sites 1, 2 and 3 share "a b", typed by site 1 with ids $(1,1)$ and $(1,2)$. At the same time each types a character between a and b: site 1 types "1" with id $(1,3)$, site 2 types "2" with id $(2,1)$, site 3 types "3" with id $(3,1)$. Each has $\mathit{prev} = $ a and $\mathit{next} = $ b.

| site | delivery order | after the first remote character | after the second |
| --- | --- | --- | --- |
| 1 | "3", then "2" | a 1 3 b: both kept, $(1,3) < (3,1)$ | a 1 2 3 b: "2" goes between "1" and "3" |
| 2 | "1", then "3" | a 1 2 b | a 1 2 3 b |
| 3 | "2", then "1" | a 2 3 b | a 1 2 3 b |

All sites show a 1 2 3 b. In each step all characters in the gap were typed straight into it, so all are kept, and the id order decides.

**The pool.** Site 1 types x, then y after x, then deletes x. Site 2 receives the delete and then y first. Both wait in the pool, since x is missing. When x arrives, the pool runs y and then the delete, and site 2 shows "y", like site 1. A second copy of x is ignored.

## Correctness

Three properties are proved in [the correctness proof](proofs/correctness.md): integration stops and puts the character strictly between its two neighbours, a local insert lands at its visible index, and characters typed concurrently into the same gap, with the same neighbours, end in id order at every replica. The proof of termination shows that lines L4 and L5 always keep at least one character when the gap is not empty, by following neighbour links back to an earlier character. Convergence in general is the main theorem of Oster et al. (2006), and Karayel and Gonzàlez (2020) proved WOOT strongly eventually consistent in Isabelle/HOL; the proof file does not repeat their argument. The tests check convergence on seeded runs with delivery in any order and duplicates.

## Complexity

Let $H$ be the number of characters ever inserted, hidden ones included.

| operation | time | messages |
| --- | --- | --- |
| integrate a remote insert | $O(H^3)$ worst for the direct algorithm, as reported by Ahmed-Nacer et al. | none |
| local insert or delete at index $i$ | $O(H)$ to find the neighbours, plus integration | one W-character with three ids |
| delete | $O(1)$ expected with an index | one id |
| READ | $\Theta(H)$ | none |

The sequence never shrinks: every deleted character stays hidden. Each W-character carries three ids. The pool can hold operations for as long as their neighbours are missing.

## Variants

- **WOOTO.** Weiss, Urso and Molli (2007) store a degree with each character and drop the recursion over neighbours, which brings integration down to $O(H^2)$.
- **WOOTH.** Ahmed-Nacer et al. (2011) add a hash table from ids to positions, also with quadratic integration.
- **How WOOT differs from the other sequence CRDTs.** [YATA](/yata/) also records two neighbours but integrates with one forward scan. [RGA](/rga/) and the [causal tree](/causal-tree/) record only the left neighbour and need causal delivery. [Logoot](/logoot/), [LSEQ](/lseq/) and [Treedoc](/treedoc/) give each character a position identifier from a dense order and remove deleted characters. Kleppmann et al. (2019) conjecture, without proof, that WOOT does not interleave concurrent insertions.

## When to use it

WOOT matters mostly as the first sequence CRDT and as a reference design. It needs no causal broadcast and no central server, which suits peer-to-peer editing. For production use, later designs such as YATA or RGA integrate faster and keep less per character.

## Pitfalls

- **Comparing against all characters in the gap.** Ordering $c$ against every character between its neighbours, not just the ones kept by lines L4 and L5, gives different results on different replicas.
- **Dropping hidden characters.** A remote insert may name a hidden character as a neighbour. Without it, the insert waits for ever.
- **Taking neighbours from the full sequence at the source.** In the original design $\mathit{prev}$ and $\mathit{next}$ are visible characters. Any rule works only if every replica uses the same one when it generates operations.
- **Slow integration.** The direct recursion is cubic in the worst case, and long documents with many hidden characters are slow.

## Implementations

The Python class follows the main block with `# @line` markers for L1 to L8, written as a loop instead of a recursion. Operations wait in a pool until they can run, and duplicates are ignored. The tests run the example and the pool case, check that two runs typed at the same place stay apart, and run seeded runs with 2 to 5 sites and up to 300 operations, delivered in any order with duplicates. They check that all sites converge with empty pools, that local edits land at their index, that every character lies between its neighbours, and that one order explains every site's sequence.

## History

Oster, Urso, Molli and Imine presented WOOT at CSCW 2006 as a way to get consistency for peer-to-peer text editing without operational transformation, and with that the first CRDT for sequences, before the term existed. Weiss, Urso and Molli gave the faster WOOTO in 2007 and the wiki system Wooki built on it. Ahmed-Nacer et al. (2011) measured WOOT and its variants against later sequence CRDTs, and Karayel and Gonzàlez (2020) proved its strong eventual consistency in Isabelle/HOL.

## References
