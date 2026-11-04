---
tag: 3YJ33R
kind: data-structure
slug: ctrie
name: Ctrie (concurrent hash-array mapped trie)
aliases:
- concurrent trie
area: data-structures/concurrent-structures
level: research
summary: Lock-free hash trie with cheap atomic snapshots, supporting linearizable lookups and insertions.
prereqs: [trie, compare-and-swap, lock-freedom]
see_also: [concurrent-hash-table, split-ordered-list, hash-table, persistent-data-structure, atomic-snapshot, population-count, linearizability, linearization-point]
sources:
  - paper: doi:10.1145/2145816.2145836
    title: Aleksandar Prokopec, Nathan G. Bronson, Phil Bagwell and Martin Odersky, Concurrent tries with efficient non-blocking snapshots, PPoPP 2012
    locator: pages 151 to 160, the node types, lookup, insert and remove with tombs and compression, GCAS and the snapshot, and the proofs of linearizability and lock-freedom
  - paper: doi:10.1007/978-3-642-36036-7_11
    title: Aleksandar Prokopec, Phil Bagwell and Martin Odersky, Lock-free resizeable concurrent tries, LCPC 2011, Lecture Notes in Computer Science 7146
    locator: the first version of the Ctrie, without snapshots, with the operations and the cleaning of tombs
---

A Ctrie is a concurrent map that is shaped like a hash array mapped trie: the hash of a key is cut into groups of $W$ bits, usually 5, and each group selects one of up to 32 branches on the next level of the [trie](/trie/). Each branching node keeps a bitmap of the branches that exist and a compact array of only those branches. The Ctrie makes this structure lock-free by adding one level of indirection: every branching node hangs from an *indirection node* (I-node) whose single word is changed by [compare-and-swap](/compare-and-swap/) (CAS). All other nodes are immutable. An update copies the small branching node it changes and swings the I-node to the copy with one CAS, so lookups take no locks and never wait. Prokopec, Bagwell and Odersky introduced it in 2011, and Prokopec, Bronson, Bagwell and Odersky added constant-time atomic snapshots in 2012. The Scala standard library ships it as TrieMap.

## In plain words

Think of a filing cabinet that sorts papers by a code. The first letter of the code picks a drawer, the second a folder in the drawer, the third a sheet in the folder. You only open as many levels as you need.

To change a folder, you do not edit it in place. You write a new copy of the folder with your change, and then swap the label on the drawer so that it points to the new copy, in one quick move. If someone else swapped the label first, you start again with their copy. Readers never wait: they always see either the old folder or the new one.

## The abstract type

A Ctrie implements a map from keys to values:

- lookup$(k)$ returns the value of $k$, or NOTFOUND.
- insert$(k, v)$ sets the value of $k$ to $v$.
- remove$(k)$ deletes $k$ and returns its old value, or NOTFOUND.

Each operation is [linearizable](/linearizability/), and the structure is [lock-free](/lock-freedom/). With snapshots it also offers snapshot(), which returns an independent, linearizable copy of the whole map in constant time, and with it a linearizable size and iteration.

## Representation

The nodes:

- **I-node**: one mutable word $main$, changed only by CAS. It points to a C-node, a T-node or an L-node.
- **C-node**: a bitmap $bmp$ of $2^W$ bits and an array with one branch for each set bit, in bit order. A branch is an I-node or an S-node. The branch for the hash group $g$ is at position $|\{b < g : b \in bmp\}|$, which a [population count](/population-count/) of the masked bitmap gives in one instruction.
- **S-node**: a key and its value.
- **T-node** (tomb): a single S-node in an I-node that is due to be removed, after a removal left only that key below it.
- **L-node**: a list of S-nodes whose hashes are equal in every bit, at the bottom of the trie.

The root is an I-node whose $main$ is a C-node; the root is never a tomb. Every node except an I-node is immutable once it has been published. A key $k$ with hash $h$ lives, if anywhere, on the unique path that follows the groups $h_0, h_1, \ldots$ of $W$ bits of $h$ from the root.

## Operations

```pseudo id=main
LOOKUP(T, k)
L1  r ← ILOOKUP(T.root, k, 0, NIL); if r = RESTART then go to L1 else return r
ILOOKUP(i, k, lev, parent)
L2  m ← READ(i.main)
L3  if m is a C-node then flag, pos ← FLAGPOS(hash(k), lev, m.bmp); if flag ∉ m.bmp then return NOTFOUND
L4      b ← m.array[pos]; if b is an I-node then return ILOOKUP(b, k, lev + W, i)
L5      if b.key = k then return b.value else return NOTFOUND
L6  if m is a T-node then CLEAN(parent, lev − W); return RESTART
L7  m is an L-node: return the value of k in m, or NOTFOUND

INSERT(T, k, v)
L8  r ← IINSERT(T.root, S-node(k, v), 0, NIL); if r = RESTART then go to L8
IINSERT(i, s, lev, parent)
L9  m ← READ(i.main)
L10 if m is a C-node then flag, pos ← FLAGPOS(hash(s.key), lev, m.bmp); if flag ∉ m.bmp then return OK if CAS(i.main, m, m with s inserted at pos) else RESTART
L11     b ← m.array[pos]; if b is an I-node then return IINSERT(b, s, lev + W, i)
L12     if b.key = s.key then n ← s else n ← I-node(DUAL(b, s, lev + W))
L13     return OK if CAS(i.main, m, m with array[pos] ← n) else RESTART
L14 if m is a T-node then CLEAN(parent, lev − W); return RESTART
L15 m is an L-node: return OK if CAS(i.main, m, m with s in place of any old pair of s.key) else RESTART

REMOVE(T, k)
L16 r ← IREMOVE(T.root, k, 0, NIL); if r = RESTART then go to L16 else return r
IREMOVE(i, k, lev, parent)
L17 m ← READ(i.main)
L18 if m is a C-node then flag, pos ← FLAGPOS(hash(k), lev, m.bmp); if flag ∉ m.bmp then return NOTFOUND; b ← m.array[pos]
L19     if b is an I-node then r ← IREMOVE(b, k, lev + W, i)
L20     else if b.key ≠ k then r ← NOTFOUND
L21     else r ← b.value if CAS(i.main, m, CONTRACT(m without pos, lev)) else RESTART
L22     if r is a value and READ(i.main) is a T-node then CLEAN-PARENT(parent, i, hash(k), lev − W)
L23     return r
L24 if m is a T-node then CLEAN(parent, lev − W); return RESTART
L25 m is an L-node: if k ∉ m return NOTFOUND; m' ← m without k, a T-node if one pair is left; return the value of k if CAS(i.main, m, m') else RESTART

CLEAN(p, lev)
L26 m ← READ(p.main); if m is a C-node then CAS(p.main, m, COMPRESS(m, lev))
CLEAN-PARENT(p, i, h, lev)
L27 m ← READ(p.main); if m is not a C-node, or the branch of h in m is not i, then return
L28 if READ(i.main) is a T-node t and not CAS(p.main, m, CONTRACT(m with i replaced by t.sn, lev)) then go to L27
```

The helpers are pure functions on immutable nodes:

- FLAGPOS$(h, lev, bmp)$ takes the group $g = (h \gg lev) \bmod 2^W$, the flag $2^g$, and the position, the number of set bits of $bmp$ below $g$.
- DUAL$(x, y, lev)$ builds the subtree for two S-nodes whose hashes agree below $lev$: a C-node with both, if their groups at $lev$ differ; else a C-node with one I-node whose node is DUAL$(x, y, lev + W)$; and an L-node when the hash bits are used up.
- CONTRACT$(c, lev)$ turns a C-node below the root with a single branch that is an S-node into a T-node of that S-node, and returns any other C-node as it is.
- COMPRESS$(c, lev)$ replaces each branch I-node whose node is a T-node by the T-node's S-node (it *resurrects* the key one level up), and then applies CONTRACT.

**Tombs.** A removal can leave a C-node with a single key. Keeping it would leave long chains of almost empty levels. So line L21 contracts it into a T-node, and line L22 asks the parent to replace the whole I-node by the lone S-node. Another thread that meets a T-node, at line L6, L14 or L24, cleans the parent itself and restarts. A T-node is final: no CAS ever replaces it, since every CAS expects a C-node or an L-node.

**Why restart.** Each operation descends by plain reads. A CAS on an I-node succeeds only if its C-node is still the one that was read, so every change is computed from the current node of that I-node. A failed CAS means that someone else changed this I-node, and the operation starts again from the root.

**Snapshots.** The 2012 version adds a generation object to each I-node and replaces each CAS on $main$ by GCAS, a generation-compare-and-swap that commits only if the generation of the root has not changed in the meantime; otherwise it rolls back. snapshot() changes the root to a fresh I-node of a new generation with a restricted double-compare single-swap (RDCSS) on the root. Each later operation that walks into an I-node of an older generation first copies it into the new generation, so the two tries share all nodes that neither side has changed since. A snapshot therefore costs $O(1)$, and the copying is spread over later operations. A read-only snapshot gives linearizable size and iteration. The Python module on this page leaves out snapshots.

## Example

Use $W = 2$, 4-bit hashes and $hash(k) = k$. Insert 0, 4 and 1. The low 2 bits of 0 and 4 are both 00, so the second insert meets the S-node of 0 at line L12 and replaces it with an I-node whose C-node splits on the next 2 bits: 0 in group 0 and 4 in group 1. Key 1 goes into group 1 of the root.

| step | operation | change |
|---|---|---|
| 1 | insert 0 | root: [0] |
| 2 | insert 4 | root: [I-node: [0, 4]] |
| 3 | insert 1 | root: [I-node: [0, 4], 1] |
| 4 | remove 4, line L21 | the inner C-node keeps only 0, so it becomes the T-node of 0 |
| 5 | lookup 0 reads the T-node, line L6 | CLEAN of the root resurrects 0: root [0, 1]; lookup restarts and finds 0 |
| 6 | remove 4, line L22 | CLEAN-PARENT finds that the branch is no longer the I-node, and returns |

At step 5 the lookup had read the old root before step 4. It goes down to the I-node, finds a tomb, cleans the root on behalf of the removal and starts over. Either way the key 0 was never missing: the T-node still holds it.

## Correctness

The full proof is in [the correctness proof](proofs/correctness.md).

- *The abstract map.* At each moment the map is the set of key-value pairs in the S-nodes that can be reached from the root, through C-node branches, T-nodes and L-nodes.
- *Shape.* Every reachable S-node lies on the path that its hash selects, and each key occurs at most once. Every CAS keeps this: inserts add at the empty group of the key or replace its S-node, DUAL splits two keys by their next groups, and COMPRESS and CONTRACT move a lone S-node one level up into the same group.
- *Detached I-nodes.* An I-node is removed from the trie only by CLEAN or CLEAN-PARENT, and only when its node is a T-node, which never changes again. So a successful CAS on an I-node always happens while it is reachable, at its fixed position.
- *Linearization points.* An insert, and a removal that finds its key, take effect at their successful CAS (line L10, L13, L15, L21 or L25). A lookup, and a removal that does not find its key, take effect at the last READ of an I-node (line L2 or L17): the node read is immutable and was the current node of a reachable I-node on the key's path at that moment. CLEAN, CLEAN-PARENT and contraction do not change the abstract map.
- *Progress.* A RESTART follows either a failed CAS, which means another CAS succeeded, or a tomb, whose cleaning removes it. With finitely many tombs, some operation finishes: the Ctrie is lock-free. Lookups do not write except to clean tombs.

## Complexity

| quantity | value |
|---|---|
| lookup, insert, remove, without contention | $O(\log_{2^W} n)$ levels for well-spread hashes, each with $O(2^W)$ work to copy a C-node |
| snapshot (2012 version) | $O(1)$, with copying spread over later operations |
| size or iteration on a read-only snapshot | $O(n)$ |
| space | $O(n)$ nodes; one C-node per I-node |

With $W = 5$ and 32-bit hashes, the trie has at most 7 levels, and a million keys sit about 4 levels deep. An update copies one C-node of at most 32 branches. Prokopec et al. compare the Ctrie with the concurrent skip list and the concurrent hash map of Java and report competitive throughput for lookups and updates, with snapshots that the other two do not offer.

## Variants

- **Hash array mapped tries.** Bagwell's sequential HAMT, with the same bitmap and compact array, is the base. Its persistent form, which copies the path to the root on each update, is the map of Clojure and of Scala's immutable collections; see [persistent data structures](/persistent-data-structure/).
- **Ctrie with snapshots.** The 2012 version, with GCAS and RDCSS, described above.
- **Cache-trie.** Later work by Prokopec (2018) adds a cache of the deep levels, so that most operations skip the top of the trie.
- **Other lock-free maps.** The [split-ordered list](/split-ordered-list/) of Shalev and Shavit is a lock-free hash table on a single list; a [concurrent hash table](/concurrent-hash-table/) with lock striping uses locks but is simpler. Neither offers cheap snapshots.

## When to use it

Use a Ctrie as a concurrent map when lookups must never block, when the map grows and shrinks a lot (it has no global resize), and when you need consistent snapshots or iteration while other threads update it, for example to read a consistent view of a cache or an index. If snapshots are not needed and the size is known, a well-tuned concurrent hash table is often faster for small keys.

## Pitfalls

- **Writing a C-node in place.** All nodes except I-nodes must be immutable once they are published; a change must go through a copy and a CAS, or readers see half-done changes.
- **Forgetting the tombs.** Without contraction and cleaning, a trie that has seen many removals keeps long chains of nearly empty C-nodes, and lookups slow down. And a T-node must be final: if an insert could still CAS into an I-node that is being detached, its key would be lost with the I-node.
- **A tomb at the root.** CONTRACT must not apply at level 0, since the root has no parent to clean it.
- **Bad hashes.** Keys with equal hashes end up in L-nodes, which are lists. A weak hash function makes the trie degrade to a list.
- **Snapshots in a garbage-free setting.** The snapshot scheme shares nodes between generations and relies on a garbage collector to reclaim them. In C or C++ it needs a separate memory reclamation scheme.

## Implementations

The Python module follows the 2011 version, without snapshots. I-nodes hold their word under a lock that simulates CAS by identity; all other nodes are immutable objects. Every read of an I-node and every CAS is one step of a generator. The trie takes the number of bits per level and the number of hash bits as parameters, so the tests can use $W = 2$ and 4-bit hashes to make deep paths and L-nodes easy to reach. The tests replay the example, including the lookup that meets the tomb and cleans it, check L-nodes for full collisions, compare random sequential runs with a Python dictionary, check random interleavings of three threads with a linearizability search and a final check of the shape, and run the plain methods under real threads.

## History

Bagwell described hash array mapped tries in 2001. Prokopec, Bagwell and Odersky made them concurrent and lock-free with I-nodes, tombs and compression in the Ctrie of 2011. Prokopec, Bronson, Bagwell and Odersky added GCAS and constant-time snapshots in 2012, and the Ctrie became scala.collection.concurrent.TrieMap. Ports exist for Java, C++, Go and other languages.

## References
