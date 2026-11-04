---
tag: TD808H
kind: technique
slug: randomized-linking
name: Randomized linking
aliases:
- random linking
- randomized union
area: data-structures/disjoint-sets
level: research
summary: Linking roots by random priorities, giving the same bounds as union by rank in expectation.
prereqs: [disjoint-set-forest, union-by-rank, path-compression]
see_also: [union-by-rank, union-by-size, path-compression, path-halving, path-splitting, union-find-amortized-bound, disjoint-set-forest]
sources:
  - paper: doi:10.1137/1.9781611973402.75
    title: "Ashish Goel, Sanjeev Khanna, Daniel H. Larkin and Robert E. Tarjan, Disjoint Set Union with Randomized Linking, Proceedings of the 25th Annual ACM-SIAM Symposium on Discrete Algorithms (SODA 2014)"
    locator: the analysis of linking by random index with compression, splitting or halving, and the results on linking by coin flips
  - paper: doi:10.1145/62.2160
    title: "Robert E. Tarjan and Jan van Leeuwen, Worst-case analysis of set union algorithms, Journal of the ACM 31(2) (1984), 245-281"
    locator: the linking rules by rank and by size and the compaction rules
---

Randomized linking is a rule for UNION in a [disjoint-set forest](/disjoint-set-forest/): give each element a random priority once, for example a random permutation of $0, \ldots, n - 1$, and always make the root with the smaller priority a child of the root with the larger one. It needs no rank or size field that changes, only a fixed random key. Goel, Khanna, Larkin and Tarjan (2014) proved that this *linking by random index*, combined with [path compression](/path-compression/), [path halving](/path-halving/) or [path splitting](/path-splitting/), has the same bounds as [union by rank](/union-by-rank/) in expectation: $O(m\,\alpha(m, n))$ expected time for $m$ operations, against an adversary that fixes the operations without seeing the keys. Linking by a fixed index, without randomness, can build a path of $n$ nodes.

## In plain words

When two groups merge, one leader must go under the other. Union by rank keeps a count for each leader and puts the smaller tree under the larger. Here, each item instead draws a random ticket at the start. The leader with the lower ticket goes under the one with the higher ticket.

The leader of a group is then always its member with the highest ticket. When a small group meets a big one, the highest ticket is most likely in the big group, so the small group usually goes under, just as with sizes. The tickets never change, so there is nothing to keep up to date, and the trees stay short on average.

## When it applies

- **A forest of parent pointers with roots as names.** The rule only decides which root goes under the other, so it works with every find rule.
- **An oblivious sequence.** The bound is in expectation over the random keys, for each fixed sequence of operations. An adversary who sees the keys, or the shape of the trees, can choose unions that build deep trees.
- **When a rank field is not wanted.** For example when the elements already carry a random hash or a random order, or when fewer writes per union matter, as in some concurrent forms of union-find.
- **When an expected bound is enough.** For a guaranteed bound, use [union by rank](/union-by-rank/) or [union by size](/union-by-size/).

## The template

```pseudo id=main
INIT(elements)
L1  give each x a distinct random key x.key, for example a random permutation

UNION(x, y)
L2  r ← FIND(x); s ← FIND(y)
L3  if r = s then return false
L4  if r.key < s.key then r.p ← s else s.p ← r
L5  return true

FIND(x)
L6  return the root of x, with the compaction rule ⟨COMPACT⟩
```

The hole ⟨COMPACT⟩ is the find rule: none, [path compression](/path-compression/), [path halving](/path-halving/) or [path splitting](/path-splitting/). Line L4 is the only difference from union by rank: it compares the fixed keys instead of ranks, and it writes one pointer and no other field.

**The root is the largest key.** By line L4 and induction, the root of each tree is the element of the set with the largest key, and keys increase along each path to the root. So the keys play the part of ranks: each parent has a larger key than its child.

**Expected depth without compression.** Fix a sequence of unions that does not depend on the keys, and an element $x$. Each union that involves the set $A$ of $x$ merges it with another set $B$, and the depth of $x$ grows by 1 exactly when the largest key of $A \cup B$ is in $B$. For a random permutation, this has probability $|B|/(|A| + |B|) \le \ln\frac{|A| + |B|}{|A|}$. The sizes of the set of $x$ grow from 1 to at most $n$, so the sum of these logarithms telescopes, and the expected depth of $x$ is at most $\ln n \approx 0.69 \lg n$. Union by rank gives the bound $\lg n$ for every sequence.

## Classic examples

### Six elements in a chain of unions

Let the keys of $0, \ldots, 5$ be $3, 0, 5, 1, 4, 2$, and do the unions $(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)$ without compression.

| union | roots and keys | result | parents of 0 to 5 | depths |
|---|---|---|---|---|
| (0, 1) | 0 (3), 1 (0) | 1 under 0 | 0 0 2 3 4 5 | 0 1 0 0 0 0 |
| (1, 2) | 0 (3), 2 (5) | 0 under 2 | 2 0 2 3 4 5 | 1 2 0 0 0 0 |
| (2, 3) | 2 (5), 3 (1) | 3 under 2 | 2 0 2 2 4 5 | 1 2 0 1 0 0 |
| (3, 4) | 2 (5), 4 (4) | 4 under 2 | 2 0 2 2 2 5 | 1 2 0 1 1 0 |
| (4, 5) | 2 (5), 5 (2) | 5 under 2 | 2 0 2 2 2 2 | 1 2 0 1 1 1 |

Once element 2, with the largest key, is in the big set, every later singleton goes under it. The largest depth is 2.

### Linking by a fixed index

Now let the key of each element be its own index, with no randomness, and do the same unions. The root of $\{0, \ldots, i\}$ is $i$, which goes under $i + 1$ at the next union. The result is the path $0 \to 1 \to \cdots \to 5$, of depth 5. On $n$ elements, $n - 1$ unions build a path of depth $n - 1$, as with [quick-union](/quick-union/). The random permutation is what prevents this.

### With compression

With path compression or one of its one-pass forms in ⟨COMPACT⟩, Goel, Khanna, Larkin and Tarjan show the expected total time $O(m\,\alpha(m, n))$, the bound of [Tarjan's union-find bound](/union-find-amortized-bound/) for union by rank. Their proof treats the keys like ranks: the key order gives a random structure in which few nodes have many nodes below them, as with ranks.

## Variations

- **Linking by a coin flip.** Instead of fixed keys, flip a fair coin at each union to choose which root goes under. Goel, Khanna, Larkin and Tarjan show that this rule is worse than linking by random index: it can give a larger expected cost than union by rank on some sequences.
- **Keys from a hash.** A hash of the element, from a family with enough independence, can replace the random permutation. The bound then depends on the properties of the hash.
- **Random keys of a few bits.** The keys need only break ties between roots; random reals or random words work with high probability, because ties are rare.
- **Concurrent union-find.** Fixed keys make a link a single compare-and-swap on the parent pointer, with no rank to update. Some concurrent union-find structures link by a fixed order of the elements for this reason.

## Pitfalls

- **An adaptive adversary.** If the sequence of unions may depend on the keys or on the trees, the bound fails: the adversary can always merge a set with a set of smaller key, and build a path.
- **Indices that are not random.** Linking by the index of the element, when the indices come from the input in a fixed order, is the fixed-index case and can be linear per find.
- **Recomputing keys.** The keys must be drawn once. Drawing a new key for the new root at each union is a different rule, closer to coin flips.
- **Expectation is not a guarantee.** One run can be slow. For a deadline per operation, use [Blum's structure](/blum-union-find/); for a guaranteed total, use rank or size.

## Exercises

1. Prove that after any unions, the root of each tree is its element of largest key, and that keys increase along every path to the root.
2. Complete the proof that the expected depth of each node is at most $\ln n$ without compression. Where is it used that the sequence does not depend on the keys?
3. Give a sequence of $n - 1$ unions on which linking by a fixed index builds a path of depth $n - 1$, and show that union by size builds a tree of depth at most $\lg n$ on the same sequence.
4. Show that $|B|/(|A| + |B|) \le \ln\big((|A| + |B|)/|A|\big)$ for positive integers $|A|$ and $|B|$.

## References
