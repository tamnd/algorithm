---
tag: VB34EV
kind: algorithm
slug: beyer-hedetniemi
name: Beyer-Hedetniemi algorithm for rooted trees
aliases:
- Beyer-Hedetniemi tree generation
- Constant amortized time rooted tree generation
- Relex generation of canonical level sequences
area: combinatorics/generating-partitions-and-trees
level: advanced
summary: Generates rooted unlabeled trees in constant amortized time per tree using level sequences.
solves: [rooted-tree-generation]
model: word-ram
complexity:
  vars: {n: the number of nodes, N: the number of unlabeled rooted trees with n nodes}
  time: {worst: Θ(n), best: Θ(1), amortized: Θ(1)}
  space: {extra: Θ(n)}
properties: {in_place: true, deterministic: true, recursive: false}
history:
  year: 1980
  people: [Terry Beyer, Sandra Mitchell Hedetniemi]
  note: Beyer and Hedetniemi listed the canonical level sequences of rooted trees in decreasing lexicographic order and showed that the cost per tree is constant on average.
prereqs: [level-sequence, rooted-tree, lexicographic-order]
see_also: [rooted-tree-generation, level-sequence, wright-richmond-odlyzko-mckay, free-tree-generation, zaks-tree-generation, constant-amortized-time-generation, tree-isomorphism, canonical-form]
sources:
  - paper: doi:10.1137/0209055
    title: Terry Beyer and Sandra Mitchell Hedetniemi, Constant time generation of rooted trees, SIAM Journal on Computing 9(4) (1980), 706 to 712
    locator: the whole paper (canonical level sequences, the successor rule and the constant average time bound)
  - url: https://page.math.tu-berlin.de/~felsner/SemWS17-18/Ruskey-Comb-Gen.pdf
    title: Frank Ruskey, Combinatorial Generation, working version, University of Victoria, 1995 to 2003
    locator: Section 4.6.2, Rooted Trees, Free Trees (the relex successor, Lemma 4.5, Algorithm 4.18, Figure 4.10 and Theorem 4.2 of Kubicka)
  - url: https://oeis.org/A000081
    title: OEIS A000081, Number of unlabeled rooted trees with n nodes
    locator: the terms a_1 to a_14 used in the tests
---

The Beyer-Hedetniemi algorithm lists every unlabeled rooted tree with $n$ nodes once, as its canonical [level sequence](/level-sequence/), in decreasing lexicographic order from the path to the star. The successor takes the last node that is deeper than level $1$, moves it up to be a sibling of its parent, and fills the rest of the sequence with copies of the parent's remaining subtree. With a parent array next to the sequence, one step costs $O(1)$ plus the number of entries it rewrites, and the total over all $N$ trees is $O(n + N)$, so the algorithm runs in constant amortized time.

## In plain words

Draw each tree in one standard way: at every node, put the deepest and largest branch on the left. Then walk the drawing from left to right and write down the depth of each node. Each tree gets exactly one list of numbers.

Start with the tallest tree, a single path. To get the next tree, find the last node that is not directly under the root. Lift it up by one level, so that it hangs next to its old parent. Then fill the rest of the list by repeating the branch of the old parent, as many times as fits. This gives the next smaller standard list. Stop at the star, where every node hangs from the root.

Most steps change only one or two numbers at the end of the list.

## The problem

A *level sequence* is a list $\ell_1, \ldots, \ell_n$ with $\ell_1 = 0$ and $1 \le \ell_{i+1} \le \ell_i + 1$. It gives the depths, in preorder, of the nodes of an ordered rooted tree. A level sequence is *canonical* if it is the largest one among all orderings of the children of the same rooted tree, so canonical sequences are one to one with unlabeled rooted trees.

**Input:** an integer $n \ge 0$.

**Output:** the $N = a_n$ canonical level sequences of length $n$, each once, where $a_n$ is $1, 1, 2, 4, 9, 20, 48, \ldots$ for $n = 1, 2, \ldots$, and $a_0 = 0$. This is [rooted tree generation](/rooted-tree-generation/).

**Cost model.** The [word RAM](/word-ram/). The generator keeps one array $L[1..n]$ and one array $\mathit{par}[1..n]$, with $\mathit{par}[i]$ the position of the parent of node $i$ and $\mathit{par}[1] = 0$, and changes them in place. Each tree is visited in place; the time counts the reads and writes of the generator, not the cost of copying each tree out.

## The algorithm

Start with the path: $L[i] = i - 1$ and $\mathit{par}[i] = i - 1$ for $i = 1, \ldots, n$, and $p = n$. Visit $L$, then call NEXT and visit again until it returns LAST. The index $p$ keeps its value from one call to the next.

```pseudo id=main
NEXT(L[1 .. n], par[1 .. n], p)
L1  while L[p] = 1 do p ← p − 1
L2  if p ≤ 1 then return LAST
L3  if L[p] = 2 and L[p − 1] = 1 then
L4      L[p] ← 1; par[p] ← par[p − 1]
L5  else
L6      d ← p − par[p]
L7      for i ← p to n do
L8          L[i] ← L[i − d]
L9          if d + par[i − d] < p then par[i] ← par[i − d] else par[i] ← d + par[i − d]
L10     p ← n
```

Line L1 finds $p$, the last position with $L[p] > 1$; all positions after $p$ hold $1$. If there is none, the current tree is the star and line L2 stops. Otherwise let $q = \mathit{par}[p]$, the parent of $p$, and $d = p - q$. Node $p$ is the last node in the subtree of $q$, so $L[q..p-1]$ is that subtree without $p$. Lines L7 and L8 copy this block again and again from position $p$ to the end; since $L[p] \leftarrow L[q]$, node $p$ moves up one level and becomes a sibling of $q$. Line L9 shifts the parent pointers by $d$, except for the first node of each copy, whose parent is the parent of $q$.

Lines L3 and L4 are a shortcut for the case $q = p - 1$ with $L[q] = 1$. Then the block is the single entry $1$, and the copy would only set $L[p] = 1$, since the later entries are already $1$. In this case $p$ is not reset, because all entries from $p$ on are now $1$.

## Example

All $a_6 = 20$ rooted trees with $6$ nodes, in the order that NEXT produces. The column $p$ is the value after line L1, "branch" is the line taken, $d$ is the block length of line L6, and "writes" is the number of passes of line L7.

| level sequence | parent array | $p$ | branch | $d$ | writes |
|---|---|---|---|---|---|
| 012345 | 0 1 2 3 4 5 | 6 | L5 | 1 | 1 |
| 012344 | 0 1 2 3 4 4 | 6 | L5 | 2 | 1 |
| 012343 | 0 1 2 3 4 3 | 6 | L5 | 3 | 1 |
| 012342 | 0 1 2 3 4 2 | 6 | L5 | 4 | 1 |
| 012341 | 0 1 2 3 4 1 | 5 | L5 | 1 | 2 |
| 012333 | 0 1 2 3 3 3 | 6 | L5 | 3 | 1 |
| 012332 | 0 1 2 3 3 2 | 6 | L5 | 4 | 1 |
| 012331 | 0 1 2 3 3 1 | 5 | L5 | 2 | 2 |
| 012323 | 0 1 2 3 2 5 | 6 | L5 | 1 | 1 |
| 012322 | 0 1 2 3 2 2 | 6 | L5 | 4 | 1 |
| 012321 | 0 1 2 3 2 1 | 5 | L5 | 3 | 2 |
| 012312 | 0 1 2 3 1 5 | 6 | L4 | | 0 |
| 012311 | 0 1 2 3 1 1 | 4 | L5 | 1 | 3 |
| 012222 | 0 1 2 2 2 2 | 6 | L5 | 4 | 1 |
| 012221 | 0 1 2 2 2 1 | 5 | L5 | 3 | 2 |
| 012212 | 0 1 2 2 1 5 | 6 | L4 | | 0 |
| 012211 | 0 1 2 2 1 1 | 4 | L5 | 2 | 3 |
| 012121 | 0 1 2 1 4 1 | 5 | L4 | | 0 |
| 012111 | 0 1 2 1 1 1 | 3 | L4 | | 0 |
| 011111 | 0 1 1 1 1 1 | 1 | LAST | | |

Take the row $012341$. The last entry larger than $1$ is at $p = 5$, its parent is $q = 4$, and $d = 1$. The block $L[4..4] = 3$ is copied to positions $5$ and $6$, which gives $012333$: the node at depth $4$ moved up to depth $3$, and the last leaf joined it as a third child of node $3$. In the row $012311$, $p = 4$ and $q = 3$, so $d = 1$ and the block $L[3] = 2$ fills positions $4$ to $6$, which gives $012222$. The total number of writes is $23$ for $20$ trees.

## Correctness

By the swap argument, a level sequence is canonical exactly when the child blocks of every node are in non-increasing lexicographic order, where a proper prefix counts as smaller. Every prefix of a canonical sequence is canonical, and if two consecutive entries are $1$ then all later entries are $1$.

Let $\ell$ be canonical and not the star, and let $p$, $q$ and $A = \ell_q \cdots \ell_{p-1}$ be as above. The sequence $s$ that keeps $\ell_1 \cdots \ell_{p-1}$ and then repeats $A$ to length $n$ is canonical: the copies of $A$ are children of the parent of $q$, each copy is not larger than the block of $q$ or the copy before it, and the last child block of every higher ancestor only becomes smaller. It is smaller than $\ell$ at position $p$. And no canonical $y$ lies strictly between: if $y$ agrees with $s$ up to $p$, then the blocks of $y$ after $p$ that hang from the parent of $q$ are each at most $A$, so $y$ cannot pass the periodic sequence $AAA\cdots$. So $s$ is the next smaller canonical sequence.

The arrays implement this rule. Line L6 gets $q$ from the parent array, lines L7 and L8 write $s$, and line L9 keeps the parent array exact. The full proof, with the cost bound, is below.

## Complexity

- **One step.** Line L1 makes at most $2$ decrements per call: after line L4, exactly $2$, by the rule on two consecutive $1$s; after line L10, at most $1$. Lines L7 to L9 cost $n - p + 1$ passes. So one call costs $\Theta(1)$ in the best case and $\Theta(n)$ in the worst case, for example from $0, 1, 2, 3, 1, \ldots, 1$, where $p = 4$ and $n - 3$ entries are rewritten.
- **The whole list.** Each pass of line L7 comes from a reset of line L10, which raises $p$ by $n - p$, and $p$ can only rise as much as line L1 lowers it. So the total number of passes is at most $3N$, and the whole list costs $O(n + N)$, or $O(1)$ amortized per tree. In the example, $23$ passes serve $20$ trees.
- **Sharper constant.** Without the shortcut of line L3, the sum of $n - p + 1$ over all trees equals $a_1 + a_2 + \cdots + a_n$, which is $1.676\,a_n$ for $n = 10$ and $1.607\,a_n$ for $n = 15$. Kubicka showed that this ratio tends to $1/(1 - \rho) \approx 1.511$, where $\rho \approx 0.3383$ is the radius of convergence of $\sum a_n x^n$.
- **Space.** The two arrays of $n$ entries each, and $O(1)$ more. The output is visited in place; copying each tree out costs $\Theta(n)$ per tree, $\Theta(n N)$ in total.

## Properties

- **Order.** Decreasing lexicographic order of the canonical level sequences, called relex order in Ruskey's book. The first tree is the path, the last is the star.
- **Height is monotone.** A canonical sequence of height $h$ starts with $0, 1, \ldots, h$, so the trees come in decreasing order of height.
- **Restartable.** The state is the current sequence, its parent array and $p$. Both arrays can be rebuilt from $L$ in $O(n)$ time, and $p = n$ is a valid restart value, so the generation can start at any canonical sequence.
- **Not a Gray code.** One step can rewrite $n - 3$ entries: from $0, 1, 2, 3, 1, \ldots, 1$ to $0, 1, 2, 2, \ldots, 2$, as from $012311$ to $012222$ in the example.
- **Subroutine for free trees.** The [Wright-Richmond-Odlyzko-McKay algorithm](/wright-richmond-odlyzko-mckay/) calls the same NEXT, sometimes with $p$ set to a smaller value, to list free trees.

## Variants and improvements

- **Without the parent array.** Find $q$ by scanning left from $p$ for the first entry equal to $L[p] - 1$. This is correct, but the average of $n - q$ grows close to linearly in $n$, so the listing is no longer constant amortized time.
- **Rooted forests.** Drop the root of each tree with $n + 1$ nodes, and subtract $1$ from each remaining entry, to list the $a_{n+1}$ rooted forests with $n$ nodes.
- **Bounded height.** Since the trees come in decreasing height, the trees of height at most $h$ are a final segment of the list. Start at the sequence $0, 1, \ldots, h, h, \ldots, h$ with $p = n$ and its parent array.
- **Free trees.** Restrict the sequence to trees rooted at a center, with extra tests on the first two subtrees; this is the [Wright-Richmond-Odlyzko-McKay algorithm](/wright-richmond-odlyzko-mckay/), and it solves [free tree generation](/free-tree-generation/).
- **Ordered trees.** If the children are ordered, every level sequence is a different tree. Then all $C_{n-1}$ level sequences are listed, for example by [Zaks' algorithm](/zaks-tree-generation/) or by [ordered tree generation](/ordered-tree-generation/) methods.

## When to use it

Use the Beyer-Hedetniemi algorithm when you need every unlabeled rooted tree of a given size, for example to test a tree algorithm on every shape, and when the order of the list does not matter or decreasing height is useful. It is simple, it needs only two arrays, and it is the fastest known way to list rooted trees. If you need free trees, use the [Wright-Richmond-Odlyzko-McKay algorithm](/wright-richmond-odlyzko-mckay/) instead of generating rooted trees and rejecting duplicates. If you only need the count $a_n$, use Otter's recurrence on the [rooted tree generation](/rooted-tree-generation/) page.

## Pitfalls

- **Searching for the parent.** Finding $q$ by a scan from $p$ makes the listing slower than constant amortized time; keep the parent array.
- **Resetting $p$ after the shortcut.** After line L4 all entries from $p$ on are $1$. Resetting $p$ to $n$ is still correct, but it adds a scan of the trailing $1$s and loses the bound of two decrements per call.
- **Order of the copy.** Lines L7 to L9 must run with increasing $i$, because the copy can overlap its source when the block is shorter than the rest of the sequence.
- **Root parent.** With $\mathit{par}[1] = 0$, the test of line L9 works for children of the root as well; another sentinel can break the comparison $d + \mathit{par}[i - d] < p$.
- **Size zero.** For $n = 0$ there is no tree, and the path start $L[1] = 0$ does not exist. Handle $n = 0$ before the loop.

## Implementations

## History

Beyer and Hedetniemi published the algorithm in 1980, under the title "Constant time generation of rooted trees". They coded rooted trees by canonical level sequences and showed that their successor rule takes constant time on average. Ruskey's book presents the algorithm with a parent array and the shortcut of line L3, proves the constant amortized bound by counting the decrements of $p$, and quotes Kubicka's limit $1/(1 - \rho)$ for the average number of rewritten entries. In 1986 Wright, Richmond, Odlyzko and McKay used the same successor as the core of their constant amortized time generator for free trees.

## References
