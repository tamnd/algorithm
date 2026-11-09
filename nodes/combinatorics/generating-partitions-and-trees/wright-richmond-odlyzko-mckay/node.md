---
tag: MPQVRK
kind: algorithm
slug: wright-richmond-odlyzko-mckay
name: Wright-Richmond-Odlyzko-McKay algorithm for free trees
aliases:
- WROM algorithm
- Constant time generation of free trees
area: combinatorics/generating-partitions-and-trees
level: research
summary: Generates every unlabeled free tree once, in constant amortized time, as the level sequence of the tree rooted at a center.
solves: [free-tree-generation]
model: word-ram
complexity:
  vars: {n: the number of nodes, N: the number of free trees with n nodes}
  time: {worst: Θ(n), best: Θ(1), amortized: Θ(1)}
  space: {extra: Θ(n)}
properties: {in_place: true, deterministic: true, recursive: false}
history:
  year: 1986
  people: [Robert Alan Wright, Bruce Richmond, Andrew Odlyzko, Brendan D. McKay]
  note: They rooted each free tree at a center, characterized the level sequences that arise, and showed that a repaired Beyer-Hedetniemi successor lists free trees in constant amortized time.
prereqs: [beyer-hedetniemi, level-sequence, tree-center]
see_also: [free-tree-generation, beyer-hedetniemi, rooted-tree-generation, level-sequence, tree-center, tree-isomorphism, constant-amortized-time-generation, orderly-generation]
sources:
  - paper: doi:10.1137/0215039
    title: Robert Alan Wright, Bruce Richmond, Andrew Odlyzko and Brendan D. McKay, Constant time generation of free trees, SIAM Journal on Computing 15(2) (1986), 540 to 548
    locator: the whole paper (the rooted version of a free tree, the successor rule and the proof that the cost per tree is constant on average)
  - url: https://page.math.tu-berlin.de/~felsner/SemWS17-18/Ruskey-Comb-Gen.pdf
    title: Frank Ruskey, Combinatorial Generation, working version, University of Victoria, 1995 to 2003
    locator: Section 4.6.2, Rooted Trees, Free Trees (Theorem 4.3, Figures 4.11 to 4.14, Algorithm 4.19 and Theorem 4.4)
  - url: https://oeis.org/A000055
    title: OEIS A000055, Number of trees with n unlabeled nodes
    locator: the terms t_0 to t_20 and Otter's formula
---

The Wright-Richmond-Odlyzko-McKay algorithm lists every unlabeled free tree with $n$ nodes once. It roots each tree at its center, with a fixed rule when there are two centers, and visits the canonical [level sequences](/level-sequence/) of these rooted trees in decreasing lexicographic order, from the path to the star. Each step is a [Beyer-Hedetniemi](/beyer-hedetniemi/) step on rooted trees, followed by a simple test; when the test fails, a jump inside the first subtree and, in some cases, a path appended at the end give the next free tree. The failures are rare, and the whole list costs $O(1)$ amortized time per tree.

## In plain words

A free tree has no top node, so the same tree can be drawn with any node on top. To list each tree once, pick one standard top for each tree: its center, the node in the middle of a longest path. Some trees have two middle nodes; a fixed rule picks one of them.

Now list rooted trees in the usual way, from the tallest to the flattest, and keep only those whose top is the chosen center. The test is cheap: look at the first two branches of the top. Usually the next rooted tree passes the test. When it does not, the first branch must change, so the algorithm jumps straight to the next first branch and, if needed, adds a path as a second branch to make the top a center again.

## The problem

A *free tree* is a connected acyclic graph with no root. Two free trees are the same if they are isomorphic. The number $t_n$ of free trees with $n$ nodes is $1, 1, 1, 2, 3, 6, 11, 23, 47, 106, 235, \ldots$ for $n = 1, 2, \ldots$, and $t_n$ grows like $2.956^n / n^{5/2}$.

**Input:** an integer $n \ge 0$.

**Output:** one representative of each free tree with $n$ nodes, each exactly once, as the canonical level sequence of its *rooted version*. This is [free tree generation](/free-tree-generation/).

The rooted version is defined through the [centers](/tree-center/) of the tree. If the tree has one center, root it there. If it has two adjacent centers $u$ and $v$, delete the edge $uv$, which leaves rooted trees $T_u$ and $T_v$; root the tree at $u$ if $T_v \prec T_u$ and at $v$ otherwise, where $S \prec S'$ means that $S$ has fewer nodes, or the same number of nodes and a smaller canonical level sequence.

Let the root of a canonical level sequence $L$ have the child subtrees $T_1, T_2, \ldots, T_m$ in order, so $T_1$ is the largest and the highest, and let $h(T)$ be the height of a subtree. For $n \ge 3$, $L$ is the rooted version of a free tree exactly when

- (A) $m \ge 2$, and
- (B1) $h(T_2) = h(T_1)$, so the root is the only center, or
- (B2) $h(T_2) = h(T_1) - 1$, so the root and the first node of $T_1$ are the two centers, and also (C) $|T_1| \le n - |T_1|$, and (D) if $|T_1| = n - |T_1|$, the level sequence of $T_1$ is at most the level sequence of the rest, the root with $T_2, \ldots, T_m$.

**Cost model.** The [word RAM](/word-ram/). The generator keeps the arrays of the [Beyer-Hedetniemi algorithm](/beyer-hedetniemi/) and a few more, and changes them in place. Each tree is visited in place; copying it out costs $\Theta(n)$ and is not counted.

## The algorithm

For $n \le 2$ there is one tree. For $n \ge 3$, start with the path rooted at a center,
$$0, 1, \ldots, \lfloor n/2 \rfloor, 1, 2, \ldots, \lceil n/2 \rceil - 1,$$
with its parent array and $p = n$. Visit it, and call FREE-NEXT until it returns LAST. NEXT is the Beyer-Hedetniemi step: it finds the last entry larger than $1$ at or before $p$, moves that node up one level, and fills the rest with copies of its parent's remaining subtree.

```pseudo id=main
FREE-NEXT(L[1 .. n], par[1 .. n], p)
L1  if NEXT(L, par, p) = LAST then return LAST
L2  if L satisfies (A) and ((B1) or ((B2) and (C) and (D))) then return L
L3  k ← |T1|, the size of the first subtree of the root
L4  if NEXT(L, par, k + 1) with the copy branch only = LAST then return LAST
L5  if L[k + 1] > 1 then
L6      h ← the largest entry of L
L7      L[n − h + 1 .. n] ← 1, 2, …, h; rebuild par there; p ← n
```

Line L1 gives the next rooted tree, and line L2 accepts it when it is the rooted version of a free tree. If not, the first subtree $T_1$ must change, because every smaller rooted tree with the same $T_1$ also fails. Line L4 restarts NEXT at the last node of $T_1$, position $k + 1$, which gives the largest rooted tree with a smaller $T_1$. If the root of that tree has two or more children, it passes (B1) and is the answer. If the root has only one child, which line L5 detects because the copies then start below level $1$, lines L6 and L7 replace the last $h$ entries by a path of height $h - 1$ hanging from the root. This makes the root a center, and it is the largest valid tree below.

To test line L2 in $O(1)$ time, the generator keeps the start positions of $T_2$ and $T_3$ and, for each position $i$, the largest level from the start of the root's child that contains $i$ up to $i$. These values depend only on the entries up to $i$, so NEXT updates them in the same loop in which it writes the entries. Test (D) compares $T_1$ with the rest of the sequence and stops at the first difference.

## Example

All $t_7 = 11$ free trees with $7$ nodes. The column $s$ is the rooted tree after line L1; "fails" names the condition that line L2 rejects.

| visited tree $L$ | $s$ after line L1 | test of line L2 | action | next tree |
|---|---|---|---|---|
| 0123123 | 0123122 | (B2), (C) | accept | 0123122 |
| 0123122 | 0123121 | (B2), (C) | accept | 0123121 |
| 0123121 | 0123111 | fails (B1) and (B2) | jump at $k + 1 = 4$ to 0122222, add path | 0122212 |
| 0122212 | 0122211 | fails (C) | jump at $k + 1 = 5$ | 0122122 |
| 0122122 | 0122121 | (B1) | accept | 0122121 |
| 0122121 | 0122111 | (B2), (C) | accept | 0122111 |
| 0122111 | 0121212 | (B1) | accept | 0121212 |
| 0121212 | 0121211 | (B1) | accept | 0121211 |
| 0121211 | 0121111 | (B2), (C) | accept | 0121111 |
| 0121111 | 0111111 | (B1) | accept | 0111111 |
| 0111111 | | | LAST | |

In the third row, $s = 0123111$ has $T_1 = 123$ of height $2$ and $T_2$ a single leaf, so the root is not a center. The jump gives $0122222$, whose root has one child, so $h = 2$ and the last two entries become $1, 2$: the tree $0122212$ has two subtrees of height $1$, and its root is the center. In the fourth row, $|T_1| = 4 > 7 - 4$, so the other center must be the root; the jump gives $0122122$, which has two subtrees of height $1$. For $n = 8$, the step from $01233122$ gives $01233121$, which fails (D), and the jump gives $01232323$.

## Correctness

A tree's centers are the middle nodes of a longest path, so conditions (A), (B1) and (B2) say that the root is a center, and (C) and (D) say that the rule chooses the root among two centers. So the valid sequences are in bijection with the free trees, and the path above is the largest of them.

The valid sequences are a subset of the canonical ones, so when the Beyer-Hedetniemi successor $s$ is valid, it is the next valid sequence. When it fails, the failure depends only on $T_1$, on the height of $T_2$, and on the rest, and these can only get worse for smaller sequences with the same $T_1$, because a smaller canonical sequence never has a larger height. So the next valid tree has a smaller $T_1$, and line L4 finds the largest canonical sequence with a smaller $T_1$. If its root has two children, they are copies of the same block and have equal height. Otherwise the appended path gives the largest valid sequence below it: any larger candidate either continues the root's only child, which then has too many nodes for (C), or starts a second child that is at most the path. The full proof is below.

## Complexity

- **One step.** Line L1 costs $O(1)$ plus the number of entries it writes, as in the Beyer-Hedetniemi algorithm. Line L2 costs $O(1)$, plus the comparison of test (D) when $n = 2|T_1|$. A failure costs $O(n)$, for the jump and the path.
- **The whole list.** The successful steps cost $O(1)$ amortized by the same argument as for rooted trees. Since a failure costs $O(n)$, it is enough that the failures number $o(t_n / n)$; Wright, Richmond, Odlyzko and McKay prove the constant amortized bound with an asymptotic analysis, and Ruskey's book states it as Theorem 4.4. In the reference implementation, the total number of loop steps per tree, counting the scan, the writes, the (D) comparisons and the repairs, is $4.04$ for $n = 8$, $2.70$ for $n = 20$ and $2.59$ for $n = 22$, and the fraction of steps with a failure falls from $0.22$ at $n = 8$ to $0.021$ at $n = 22$.
- **Space.** A constant number of arrays of $n$ entries. The output is visited in place; copying each tree out costs $\Theta(n)$ per tree.

## Properties

- **Order.** Decreasing lexicographic order of the rooted versions; the trees come in decreasing order of the height of the rooted version, which is the radius of the tree.
- **Unicentral before bicentral.** For a fixed first subtree $T_1$, the trees with one center come before the trees with two centers, because a higher second subtree gives a larger sequence.
- **In place.** The state is the current sequence and its arrays; the next tree is computed from it alone.
- **Built on rooted trees.** Every step except the rare failures is a [Beyer-Hedetniemi](/beyer-hedetniemi/) step, so the algorithm is about as fast per tree as the rooted tree generator.

## Variants and improvements

- **Generate and test.** List all rooted trees with the [Beyer-Hedetniemi algorithm](/beyer-hedetniemi/) and keep those that pass line L2. This is correct and simple, but it visits $a_n$ rooted trees for $t_n$ free trees, and $a_n / t_n$ grows like $n$.
- **Bounded radius.** The height of the rooted version is the radius of the tree, and the trees come in decreasing order of it, so the trees of radius at most $r$ are a final segment of the list. Start at the largest valid sequence of height $r$.
- **Gray codes and other orders.** Other free tree generators produce the trees in different orders, for example with small changes between neighbors; see [free tree generation](/free-tree-generation/).
- **General graphs.** For graphs with cycles, no such simple canonical form is known; use [orderly generation](/orderly-generation/) or [canonical augmentation](/canonical-augmentation/).

## When to use it

Use it when you need every unlabeled tree with $n$ nodes, for example to test a conjecture about trees or a tree algorithm on every shape. It is the standard method, it is simple to add to a rooted tree generator, and it is practical up to about $n = 25$, where $t_{25} \approx 1.0 \cdot 10^8$. For labeled trees, use [labeled tree generation](/labeled-tree-generation/) instead, and for a random tree, use a random [Prüfer code](/pruefer-decoding/) for labeled trees or a uniform sampler for unlabeled ones.

## Pitfalls

- **The repair test.** The repair is needed whenever the root has one child after the jump, that is, when $L[k + 1] > 1$. Ruskey's statement of Algorithm 4.19 prints the test as $L[1 + |T_1|] > 2$; with that test the generator outputs invalid sequences such as $0122222$ for $n = 7$.
- **The value of $h$.** Take $h$ from the sequence after the jump, not before it.
- **The shortcut in the jump.** The jump starts at a position whose later entries are not $1$, so the shortcut of the Beyer-Hedetniemi step does not apply. Use the copy branch, which writes every entry up to $n$.
- **Small $n$.** The rules assume $n \ge 3$. For $n = 1$ and $n = 2$ there is one tree, and for $n = 0$ there is none.
- **Two centers with equal halves.** When $n = 2|T_1|$ and the two halves are isomorphic, both centers give the same rooted tree. Test (D) must accept equality.

## Implementations

## History

Beyer and Hedetniemi gave the constant amortized time generator for rooted trees in 1980. In 1986 Wright, Richmond, Odlyzko and McKay rooted each free tree at its center, with a size and order rule for two centers, characterized the level sequences that arise, and showed that the repaired successor costs constant time per tree on average; the analysis that the failures are rare uses the asymptotics of $a_n$ and $t_n$. Ruskey's book restates the characterization as Theorem 4.3, gives the algorithm as Algorithm 4.19, and cites the paper for the constant amortized bound as Theorem 4.4.

## References
