---
tag: 13DJ1S
kind: data-structure
slug: treedoc
name: Treedoc
aliases:
- Treedoc sequence CRDT
area: distributed/replication-and-crdts
level: advanced
summary: A sequence CRDT whose positions are paths in a binary tree, read in infix order. Concurrent inserts at one path become mini-nodes, and a flatten step rebalances the tree with coordination.
implements: [crdt]
model: word-ram
complexity:
  vars: {H: "the number of nodes, tombstones included", D: "the depth of the tree"}
  time: {worst: O(D log H)}
  space: {extra: Θ(H D)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [op-based-crdt, binary-search-tree, tombstone]
see_also: [logoot, lseq, rga, woot, yata, causal-tree, collaborative-text-editing, two-phase-commit]
sources:
  - paper: doi:10.1109/ICDCS.2009.20
    title: Nuno Preguiça, Joan Manuel Marques, Marc Shapiro and Mihai Letia, A commutative replicated data type for cooperative editing, ICDCS 2009
    locator: pages 395 to 403, position identifiers as paths in a binary tree, major nodes and mini-nodes with disambiguators, the infix order, tombstones, and the flatten operation with its commitment
  - paper: doi:10.1109/ICDCS.2009.75
    title: Stéphane Weiss, Pascal Urso and Pascal Molli, Logoot, a scalable optimistic replication algorithm for collaborative editing on P2P networks, ICDCS 2009
    locator: pages 404 to 412, the other dense-identifier design of the same year, used for comparison
  - paper: doi:10.1145/3301419.3323972
    title: Martin Kleppmann, Victor B. F. Gomes, Dominic P. Mulligan and Alastair R. Beresford, Interleaving anomalies in collaborative text editors, PaPoC 2019
    locator: the discussion of Treedoc, for which the absence of interleaving is conjectured but not proved
---

Treedoc is a sequence [CRDT](/crdt/) given by Preguiça, Marques, Shapiro and Letia in 2009. The document is the infix walk of a binary tree, and the position of an element is its path from the root: a list of steps, each going left or right. To insert between two adjacent elements, a replica adds a new leaf, the right child of the first element or the left child of the second, so its path lies between theirs. Two replicas can add a child at the same place at the same time; these concurrent nodes become mini-nodes of one major node, ordered by a unique disambiguator. Deletes leave [tombstones](/tombstone/). Paths get long when the tree is unbalanced, so Treedoc has a flatten step that rebuilds a balanced tree, but flatten changes every path and needs agreement among the replicas.

## In plain words

Put the letters of a text in a binary tree so that reading the tree from left to right, a node after everything on its left and before everything on its right, gives the text. Then the way from the root to a letter, such as "right, right, left", tells where the letter is.

To type a letter after letter p, hang it as the right child of p. If p already has a right child, hang it as the left child of the next letter instead. Either way, its way from the root puts it between the two.

If two people hang a letter at the same place at once, both stay there, side by side, sorted by a unique tag. Deleted letters stay as hidden nodes. From time to time the tree can be rebuilt as a balanced tree, but all replicas must agree to do that together.

## The abstract type

Treedoc implements a replicated list with updates INSERT$(i, x)$ and DELETE$(i)$ and the query READ. It is an [op-based CRDT](/op-based-crdt/).

**Model.** There are sites with distinct numeric ids. Each operation is delivered at every replica in a causal order, possibly more than once; inserts and deletes are idempotent. Flatten runs only when all replicas have the same state and agree to run it.

**Specification.** Replicas that have run the same operations show the same list. A local INSERT$(i, x)$ makes $x$ the $i$-th visible element at its source, and DELETE$(i)$ hides the $i$-th one. Between two flattens, the relative order of two elements never changes.

## Representation

A path is a list of steps $(\mathit{side}, \mathit{dis})$, with side 0 for left and 1 for right and a disambiguator $\mathit{dis} = (\mathit{clock}, \mathit{site})$. The empty path is the root, a fixed start mark. Two paths that agree except in the disambiguator of their last step are mini-nodes of the same major node, at the same place in the tree. Each replica keeps its clock, the set of paths sorted by the key below, a map from paths to values, a set of deleted paths, and the set of paths that have a right child. A [binary search tree](/binary-search-tree/) or any sorted structure on the keys gives the infix order.

This page uses a simple encoding in which every step names one mini-node, so children always hang under one mini-node. The encoding in the paper differs in its details, such as how mini-nodes and their children are written down; the idea, a path in a binary tree read in infix order with disambiguators for concurrent nodes, is the same.

## Operations

```pseudo id=main
KEY(path)                                              ▷ a sort key for the infix order
L1  return [(2 · side, dis) for each step of path] + [(1)]
ADD(x, v)                                              ▷ an insert, local or remote
L2  if x is not present then put x into the sorted set by KEY(x);  value[x] ← v
NEWPATH(p, q)                                          ▷ q is the successor of p, tombstones included
L3  clock ← clock + 1;  dis ← (clock, site)
L4  if p has no right child then
L5      return p + [(1, dis)]
L6  else return q + [(0, dis)]
DELETE(x)
L7  add x to the deleted set                           ▷ a tombstone
```

Line L1 encodes the infix order. At a node, the mark $(1)$ sits between the left steps $(0, \mathit{dis})$ and the right steps $(2, \mathit{dis})$, so the left subtree comes before the node and the right subtree after it, and mini-nodes on the same side are ordered by $\mathit{dis}$. Lines L4 to L6 give a new leaf right after $p$: the right child of $p$ if $p$ has none, else the left child of the successor $q$, which then has no left child.

**Local insert.** Let $p$ be the path of visible element $i - 1$, or the root, and $q$ the next path after $p$ in the full order. Run NEWPATH, then ADD, and broadcast the path and the value. **Local delete.** Mark the path of visible element $i$ as deleted and broadcast it.

**Flatten.** Flatten rebuilds the tree from the visible elements alone.

```pseudo
FLATTEN()                                              ▷ only on a state that all replicas share
1  items ← the visible values in order
2  clear the tree
3  BUILD(0, |items|, [(1, FLAT)])
BUILD(lo, hi, prefix)
4  if lo ≥ hi then return
5  mid ← ⌊(lo + hi) / 2⌋
6  ADD(prefix, items[mid])
7  BUILD(lo, mid, prefix + [(0, FLAT)]);  BUILD(mid + 1, hi, prefix + [(1, FLAT)])
```

Every replica that runs FLATTEN on the same state gets the same balanced tree, with depth about $\log_2$ of the number of elements, and no tombstones. But an operation made before the flatten names a path of the old tree, so a replica must not receive it after flattening. The paper therefore runs flatten only with the agreement of the replicas, through a distributed commitment protocol in the style of [two-phase commit](/two-phase-commit/), and gives it up when a concurrent edit gets in the way.

## Example

Two sites 1 and 2. Site 1 types "Hi"; site 2 receives both.

| step | site | operation | NEWPATH | path |
| --- | --- | --- | --- | --- |
| 1 | 1 | insert H at 0 | the root has no right child | $[(1,(1,1))]$ |
| 2 | 1 | insert i at 1 | H has no right child | $[(1,(1,1)),(1,(2,1))]$ |
| 3 | 1 | insert e at 1 | H has a right child, so a left child of i | $[(1,(1,1)),(1,(2,1)),(0,(3,1))]$ |
| 3 | 2 | insert o at 1, at the same time | the same rule | $[(1,(1,1)),(1,(2,1)),(0,(1,2))]$ |
| 4 | both | apply the other's insert | e and o are mini-nodes; $(1,2) < (3,1)$ | H o e i at both sites |

The tree is a chain: H is the right child of the root and i the right child of H, which is how typing at the end makes the tree deep. The two concurrent letters are left children of i, told apart by their disambiguators.

## Correctness

[The correctness proof](proofs/correctness.md) shows four things. The key of line L1 orders all paths in the infix order of the tree, and it is a total order on distinct paths. NEWPATH returns a path strictly between $p$ and its successor, so a local insert lands at its index. Paths are unique, since the last step holds a fresh disambiguator. The state of a replica is the set of added paths and the set of deleted paths, both grown by union, so replicas that ran the same operations show the same list. Flatten is correct only under its precondition, an agreed state with no operations in flight, which the proof states and does not try to remove.

## Complexity

Let $H$ be the number of nodes, tombstones included, and $D$ the depth of the tree.

| operation | time | messages |
| --- | --- | --- |
| NEWPATH | $O(D)$ to copy a path | none |
| insert, local or remote, in a balanced search tree of keys | $O(D \log H)$, since a key comparison costs $O(D)$ | one path of $O(D)$ steps |
| delete | $O(D \log H)$ | one path |
| READ | $\Theta(H)$ | none |
| FLATTEN | $\Theta(H)$ locally, plus a commitment round | one commitment protocol run |

The depth depends on the editing pattern. Typing at the end makes each letter the right child of the one before, so $D$ grows linearly with the number of inserts. Flatten brings $D$ back to about $\log_2$ of the number of visible elements and removes all tombstones.

## Variants

- **Removing deleted leaves.** Since the order depends only on paths, a deleted node with no children can be dropped without changing the order of the others. Deleted inner nodes must stay until flatten.
- **Core and nebula.** Later work by Letia, Preguiça and Shapiro lets a small group of core sites run flatten with a commitment protocol, while other sites, the nebula, catch up afterwards.
- **How Treedoc differs from the other sequence CRDTs.** Like [Logoot](/logoot/) and [LSEQ](/lseq/), it gives each element a position from a dense order, but its positions are tree paths and it keeps tombstones, while Logoot and LSEQ remove deleted elements. [RGA](/rga/), [WOOT](/woot/), [YATA](/yata/) and the [causal tree](/causal-tree/) store the ids of neighbours instead of positions. Treedoc is the only one of these that can rebalance, and the only one that needs coordination for it. Kleppmann et al. (2019) conjecture, without proof, that Treedoc does not interleave concurrent insertions.

## When to use it

Treedoc matters mainly as one of the first two sequence CRDTs and as the design that combines tree positions with occasional coordination. Use it when the system has times with no concurrent edits, for example a small set of always-connected servers, so that flatten can run and keep paths short. For open peer-to-peer settings, where agreement is hard, a design that never needs to rebalance is simpler.

## Pitfalls

- **Sorting paths as plain lists.** Plain list order puts a node before its left subtree. The key must place a node between its left and right subtrees, as line L1 does.
- **Ordering mini-nodes by arrival.** Concurrent nodes at one path must be ordered by their disambiguators, the same way everywhere.
- **Flattening without agreement.** A replica that flattens while an old operation is in flight cannot place that operation, since its path names nodes of the old tree.
- **Long paths for typing at the end.** Without flatten, paths grow by one step per letter in this common pattern.

## Implementations

The Python class follows the main block with `# @line` markers for L1 to L7. It keeps the keys in a sorted Python list, which gives the infix order without building the tree, and has a flatten method for an agreed state. The tests run the example, run flatten on three replicas after a run and check that they agree, have no tombstones and have a balanced depth, and run seeded runs with 2 to 5 sites, causal delivery with duplicates, and up to 300 operations. They check that all replicas converge, that local edits land at their index, and that one order explains every replica's list.

## History

Preguiça, Marques, Shapiro and Letia presented Treedoc at ICDCS 2009, at the same conference as [Logoot](/logoot/), as a commutative replicated data type for cooperative editing. The work was part of the line that led Shapiro, Preguiça, Baquero and Zawirski to define CRDTs in general in 2011. Letia, Preguiça and Shapiro studied how to run flatten with a small core of sites.

## References
