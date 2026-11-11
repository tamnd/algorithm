---
tag: H9D744
kind: data-structure
slug: non-blocking-bst
name: Non-blocking binary search tree
aliases:
- Ellen et al. non-blocking BST
- lock-free BST
- EFRB tree
- non-blocking external binary search tree
area: concurrency/lock-free-structures
level: research
summary: Lock-free leaf-oriented binary search tree whose updates are coordinated by descriptors and helping.
implements: [ordered-set]
complexity:
  vars: {n: "the number of keys", d: "the number of internal nodes on the search path", c: "the point contention"}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: true, external: false}
prereqs: [binary-search-tree, linearizability, lock-freedom, helping, compare-and-swap]
see_also: [harris-linked-list, lock-free-skip-list, logical-deletion, multi-word-cas, epoch-based-reclamation, debra, red-black-tree, split-ordered-list]
sources:
  - paper: doi:10.1145/1835698.1835736
    title: Faith Ellen, Panagiota Fatourou, Eric Ruppert and Franck van Breugel, Non-blocking binary search trees, PODC 2010, pages 131 to 140
    locator: the leaf-oriented tree with sentinel keys, the update field with the states Clean, IFlag, DFlag and Mark, the IInfo and DInfo records, the pseudocode of Search, Find, Insert, Delete, Help, HelpInsert, HelpDelete and HelpMarked, and the proofs of linearizability and lock-freedom (full proofs in York University Technical Report CSE-2010-04)
  - paper: doi:10.1145/2555243.2555256
    title: Aravind Natarajan and Neeraj Mittal, Fast concurrent lock-free binary search trees, PPoPP 2014, pages 317 to 328
    locator: a leaf-oriented lock-free tree that marks edges instead of nodes, with no Info records, and fewer atomic steps per update
  - paper: doi:10.1145/2555243.2555267
    title: Trevor Brown, Faith Ellen and Eric Ruppert, A general technique for non-blocking trees, PPoPP 2014
    locator: the LLX and SCX primitives, which generalize the flag and mark protocol of this tree to other trees, among them a non-blocking chromatic tree
  - paper: doi:10.1145/2611462.2611486
    title: Faith Ellen, Panagiota Fatourou, Joanna Helga and Eric Ruppert, The amortized complexity of non-blocking binary search trees, PODC 2014, pages 332 to 340
    locator: a change to this tree after which a failed update does not restart from the root, and the bound of O(h + c) amortized steps per operation
---

The non-blocking binary search tree of Ellen, Fatourou, Ruppert and van Breugel (2010) was the first complete lock-free [binary search tree](/binary-search-tree/) made only from single-word [CAS](/compare-and-swap/). It is leaf oriented: the keys are in the leaves, and the internal nodes only route searches. An insert replaces a leaf by a small subtree, and a delete replaces a leaf's parent by the leaf's sibling. To keep two updates from breaking each other, each internal node has an update field. An update first *flags* the node whose child pointer it will change, and a delete also *marks* the parent it will remove. A flag or a mark points to an Info record that describes the whole update, so any process that runs into it can finish the update for its owner. This is the [helping](/helping/) that makes the tree [lock-free](/lock-freedom/). Searches only read and never help. The tree is [linearizable](/linearizability/) as a set.

## In plain words

Picture a tree of signposts. Each signpost says "smaller keys to the left, the rest to the right", and the keys hang at the ends of the branches.

To add a key, you take the key at the end of your branch and put a new small signpost in its place, with the old key and the new key below it. To remove a key, you take away its signpost and connect the other branch to the signpost above.

Before you change a signpost, you hang a tag on it with a note that says what you will do. Nobody else may change a signpost that has a tag. If you find a tag on your way, you do the work on the note, take the tag off, and then try your own change. A signpost that will be taken away gets a tag that never comes off.

## The abstract type

The tree implements a set of keys, an [ordered set](/ordered-set/) without the order queries.

- insert(k): add $k$; return true, or false if $k$ was present.
- delete(k): remove $k$; return true, or false if $k$ was absent.
- find(k): return whether $k$ is present.

## Representation

### Model and notation

We use the asynchronous shared memory model with processes that may crash, atomic read and CAS on single words, and [sequential consistency](/sequential-consistency/). CAS returns the old value of the word. The update field is one word: a state of two bits and a pointer to an Info record. Nodes and Info records are not freed in the code (the paper assumes a garbage collector); see the section on memory reclamation.

| Symbol | Meaning |
|---|---|
| $\infty_1 < \infty_2$ | two sentinel keys, larger than every key of the set |
| $x.\mathit{update}$ | the pair (state, info) of internal node $x$ |
| CLEAN, IFLAG, DFLAG, MARK | the states: free, flagged by an insert, flagged by a delete, marked for removal |
| IInfo$(p, l, \mathit{new})$ | an insert: replace leaf $l$, a child of $p$, by the internal node $\mathit{new}$ |
| DInfo$(gp, p, l, \mathit{pupdate})$ | a delete: remove leaf $l$ and its parent $p$, a child of $gp$; $\mathit{pupdate}$ is the value of $p.\mathit{update}$ that the delete saw |
| $d$ | the number of internal nodes on a search path |

### Fields

- A leaf has a key.
- An internal node has a key, a left and a right child, and the update field. Every internal node has two children.
- The root is an internal node with key $\infty_2$, with a leaf $\infty_1$ on the left and a leaf $\infty_2$ on the right. It is never removed.

**Invariant.** (1) The tree is a binary search tree in the leaf-oriented sense: every key in the left subtree of an internal node $x$ is less than $x.\mathit{key}$, and every key in the right subtree is at least $x.\mathit{key}$. (2) The child fields of a node can change only while its update field is flagged by the operation that changes them. (3) A marked node is never unmarked, and its child fields never change again. The abstract set is the set of keys of the leaves reachable from the root, without the sentinels.

## Operations

```pseudo id=main
SEARCH(k)
L1  gp ← null; p ← null; l ← root; pupdate ← gpupdate ← (CLEAN, null)
L2  while l is internal do
L3      gp ← p; p ← l; gpupdate ← pupdate
L4      pupdate ← p.update
L5      if k < l.key then l ← p.left
L6      else l ← p.right
L7  return (gp, p, l, pupdate, gpupdate)

FIND(k)
L8  (_, _, l, _, _) ← SEARCH(k); return l.key = k

INSERT(k)
    loop
L9      (_, p, l, pupdate, _) ← SEARCH(k)
L10     if l.key = k then return false
L11     if pupdate.state ≠ CLEAN then HELP(pupdate); continue
L12     make leaves k and l.key
L13     new ← internal node with key max(k, l.key), the two leaves as children (smaller on the left), update (CLEAN, null)
L14     op ← IInfo(p, l, new)
L15     result ← CAS(p.update, pupdate, (IFLAG, op))          ▷ iflag
L16     if result = pupdate then HELPINSERT(op); return true
L17     else HELP(result)

HELPINSERT(op)
L18 CASCHILD(op.p, op.l, op.new)                              ▷ ichild
L19 CAS(op.p.update, (IFLAG, op), (CLEAN, op))                ▷ iunflag

DELETE(k)
    loop
L20     (gp, p, l, pupdate, gpupdate) ← SEARCH(k)
L21     if l.key ≠ k then return false
L22     if gpupdate.state ≠ CLEAN then HELP(gpupdate)
L23     else if pupdate.state ≠ CLEAN then HELP(pupdate)
        else
L24         op ← DInfo(gp, p, l, pupdate)
L25         result ← CAS(gp.update, gpupdate, (DFLAG, op))    ▷ dflag
L26         if result = gpupdate then
L27             if HELPDELETE(op) then return true
L28         else HELP(result)

HELPDELETE(op)
L29 result ← CAS(op.p.update, op.pupdate, (MARK, op))         ▷ mark
L30 if result = op.pupdate or result = (MARK, op) then HELPMARKED(op); return true
L31 HELP(result)
L32 CAS(op.gp.update, (DFLAG, op), (CLEAN, op))               ▷ backtrack
L33 return false

HELPMARKED(op)
L34 other ← op.p.left if op.p.right = op.l, else op.p.right
L35 CASCHILD(op.gp, op.p, other)                              ▷ dchild
L36 CAS(op.gp.update, (DFLAG, op), (CLEAN, op))               ▷ dunflag

HELP(u)
L37 if u.state = IFLAG then HELPINSERT(u.info)
L38 else if u.state = MARK then HELPMARKED(u.info)
L39 else if u.state = DFLAG then HELPDELETE(u.info)

CASCHILD(parent, old, new)
L40 if new.key < parent.key then CAS(parent.left, old, new)
L41 else CAS(parent.right, old, new)
```

An insert changes one child pointer, so it flags one node, the parent $p$. A delete changes a child pointer of $gp$ and throws $p$ away, so it flags $gp$ and marks $p$. The mark stops any later update from flagging $p$, so after the mark the children of $p$ are fixed, and the sibling that L34 reads is the right one. If the mark fails because another operation holds $p$, the delete helps that operation, removes its own flag from $gp$ (L32), and starts over.

Each Info record is used by one CAS of each kind. A new update value $(s, op)$ is never written twice, because each try makes a new Info record. So a late helper's CAS at L19, L32 or L36 fails harmlessly, and a late helper's child CAS at L18 or L35 fails because the expected child (a node that was replaced) never comes back.

**Linearization points.** An insert that returns true at its ichild CAS (L18, done by the inserter or by a helper). A delete that returns true at its dchild CAS (L35). An insert that returns false, a delete that returns false, and a find: at a moment during their SEARCH at which the leaf $l$ they reached was in the tree; Ellen et al. prove that such a moment exists.

**Why the mark is needed.** Without L29, a delete of $l$ reads $p$'s other child at L34 and then swings $gp$'s pointer from $p$ to it. An insert can flag $p$ in between, because $p$ is still clean, and put a new leaf under $p$. The delete then cuts $p$ out of the tree together with the new leaf. The test `test_without_the_mark_an_insert_is_lost` replays this run: insert(2) returns true and a later find(2) returns false. The explorer also finds it by itself.

### Memory reclamation

A delete removes two nodes, $p$ and $l$, and an insert replaces one leaf; each try also makes an Info record. None of them can be freed when it leaves the tree: a search may be standing on $p$, and a helper may still read the Info record and the nodes it names. If a removed node were freed and its address reused for a new internal node, a late child CAS at L35 that expects the old $p$ could succeed on the new node and cut a part of the tree out (the [ABA problem](/aba-problem/)). The usual choice is [epoch-based reclamation](/epoch-based-reclamation/) or Brown's [DEBRA](/debra/), which was made for trees of this kind: the process whose dchild CAS succeeds retires $p$, $l$ and the DInfo record, and the inserter retires the replaced leaf and its IInfo record after the iunflag. [Hazard pointers](/hazard-pointers/) are hard to use here, because a search would have to validate each step against nodes that can be removed under it, and the paper's searches do not restart.

### Weak memory

The fields of a new node and of an Info record must be visible before the CAS that publishes them (L15, L18, L25), so those CAS steps need release order, and the reads at L4 to L6 and of Info fields need acquire order. In C++ the defaults of seq_cst atomics are safe; with weaker orders, the proof in the paper does not apply directly.

## Example

Start with $\{1, 3\}$. The tree is root($\infty_2$) with left child $A$ = internal($\infty_1$), and $A$ has left child $B$ = internal(3) with leaves 1 and 3, and right child leaf $\infty_1$.

1. $p_0$ runs delete(3). SEARCH gives $gp = A$, $p = B$, $l$ = leaf 3, both clean. $p_0$ flags $A$ with DInfo$(A, B, 3)$ and marks $B$. It reads $B$'s right child (leaf 3) and its left child (leaf 1), and stops before its dchild CAS.
2. $p_1$ runs insert(2). SEARCH ends at leaf 1 with $p = B$, and sees $B.\mathit{update} = (\mathrm{MARK}, op)$. $p_1$ helps: it swings $A.\mathit{left}$ from $B$ to leaf 1 and unflags $A$. Now the set is $\{1\}$.
3. $p_1$ searches again. Now $p = A$ and $l$ = leaf 1. It flags $A$, replaces leaf 1 by internal(2) with leaves 1 and 2, unflags $A$, and returns true. The set is $\{1, 2\}$.
4. $p_0$ resumes. Its dchild CAS expects $A.\mathit{left} = B$ and fails; its dunflag fails too. It returns true: its delete took effect in step 2.

Without the mark in step 1, $p_1$ flags $B$ in step 2, puts leaf 2 under $B$, and returns true; then $p_0$ swings $A.\mathit{left}$ from $B$ to leaf 1, and key 2 is gone.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) is a sketch. The full proof is in the technical report of Ellen et al.

- *Safety.* The flag and mark protocol makes each successful child CAS happen at most once per Info record, only while its node is flagged by that record, and only to a node that is still in the tree. From this, the invariant above holds after each step, and each successful update changes the set exactly as its linearization point says. Searches that do not help can pass through nodes that are being removed; the paper proves that each node a search visits was on the search path for $k$ at some moment during the search, which places the points of find and of the unsuccessful updates.
- *Progress.* An update fails only if a flag or a mark it saw has changed, and each such change is a step of another update. A process that meets a flag helps that update finish. The paper shows that the helping cannot go round in a cycle, because a delete flags $gp$ before it marks $p$ and the tree has no cycles, so some update always completes. The tree is lock-free and not wait-free: a process can retry for ever if others keep changing the nodes near its leaf.

The tests check all interleavings of eight small cases with two processes (deletes of siblings, of a leaf and its neighbour, an insert under a node that is being removed, two inserts at the same leaf), with the search tree property checked in every state; 300 seeded schedules of three processes on neighbouring leaves; 60 seeded runs of three processes; the run above; and that the others finish when a process stops right after its flag or its mark.

## Complexity

| quantity | bound | status |
|---|---|---|
| find alone | exactly $2d$ reads | proved, and tested |
| insert or delete alone | at most $2d + 7$ steps (one try) | proved, and tested |
| $d$ | between $\log_2 n$ and $n + 1$; the tree is not balanced | |
| amortized steps, with a changed retry | $O(h + c)$ per operation, $h$ the height | cited (Ellen, Fatourou, Helga and Ruppert, 2014) |
| with contention | unbounded per operation (lock-free, not wait-free) | |
| space | $2n + 3$ nodes, plus one Info record per try that is not yet reclaimed | |

In the original algorithm, a failed update starts its search again at the root. That is why the amortized bound needs the change of the 2014 paper, which restarts from a nearby node instead.

## Variants

- **Natarajan and Mittal (2014).** The same leaf-oriented tree, but the flag and mark bits go on the *edges* (the child pointers) instead of in update fields with Info records. A delete needs fewer CAS steps and no allocation, and an insert needs one CAS. It is often faster in practice.
- **Internal trees.** Howley and Jones (SPAA 2012) keep keys in internal nodes as well, which halves the number of nodes but makes delete of a node with two children harder.
- **Balanced trees.** Brown, Ellen and Ruppert turned the flag and mark protocol into the LLX and SCX primitives, with which they built a non-blocking chromatic tree, a relaxed form of a [red-black tree](/red-black-tree/). The tree on this page is not balanced.
- **Multi-word CAS.** With a [multi-word CAS](/multi-word-cas/), a delete could change $gp$'s child and seal $p$ in one step. The Info records are a hand-made form of that idea for the two words of one update.

## When to use it

Use it when you need a concurrent ordered set without locks and the keys arrive in a random enough order that an unbalanced tree stays shallow. For sorted or adversarial inserts the height grows to $\Theta(n)$; use a [lock-free skip list](/lock-free-skip-list/) or a balanced non-blocking tree instead. For a set without order queries, a lock-free hash table is faster. The tree is a good model to learn from: its protocol is the base of many later non-blocking trees.

## Pitfalls

- **Forgetting the mark.** The delete must seal the parent; see above.
- **Reusing update values.** The CAS steps on update fields compare whole (state, info) pairs. If an Info record were reused for a new try, a late helper's CAS could succeed on the wrong try. Make a new record for each try.
- **Freeing removed nodes at once.** A late child CAS can then hit a reused address; see the section on memory reclamation.
- **Reading the sibling before the mark.** L34 must run after the mark has succeeded (or after another process has done it); before that, $p$'s children can still change.
- **Helping from find.** Find does not help and does not need to. Adding help to it costs writes and does not change the result.
- **Expecting balance.** There is no rebalancing; the height depends on the order of the keys.

## Implementations

## History

Lock-free linked lists (Harris 2001) and skip lists (Fraser 2004, Fomitchev and Ruppert 2004) came before lock-free search trees, because a tree update can need to change more than one node at a time. Fraser's thesis gave a lock-free tree that used multi-word CAS. Ellen, Fatourou, Ruppert and van Breugel gave the first complete lock-free binary search tree from single-word CAS at PODC 2010, using flags and marks with Info records. Howley and Jones gave an internal version in 2012. In 2014 Natarajan and Mittal moved the marks onto edges, Brown, Ellen and Ruppert generalized the protocol to LLX and SCX, and Ellen, Fatourou, Helga and Ruppert bounded the amortized cost.

## References
