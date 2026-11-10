---
tag: TWC8P7
kind: technique
slug: tree-contraction
name: Tree contraction
aliases:
- Miller-Reif tree contraction
- rake and compress
area: parallel/parallel-primitives
level: research
summary: Shrink a rooted tree to its root by rounds of RAKE (remove all leaves) and COMPRESS (splice out an independent set of one-child nodes). O(log n) rounds suffice, for any shape of tree.
prereqs: [rooted-tree, binary-tree, list-contraction, work-span-model]
see_also: [tree-expression-evaluation, list-contraction, euler-tour-technique, list-ranking, parallel-list-ranking, pointer-jumping, expression-tree, lowest-common-ancestor]
sources:
  - paper: doi:10.1109/SFCS.1985.43
    title: Gary L. Miller and John H. Reif, Parallel tree contraction and its application, 26th Annual Symposium on Foundations of Computer Science (FOCS), 1985
    locator: pp. 478 to 489 (RAKE and COMPRESS; O(log n) time with n / log n processors randomized, or n processors deterministic)
  - paper: "Gary L. Miller and John H. Reif, Parallel tree contraction, Part 1: fundamentals, in Silvio Micali (editor), Randomness and Computation, Advances in Computing Research 5, JAI Press, 1989"
    title: Parallel tree contraction, Part 1, fundamentals
    locator: pp. 47 to 72 (the full version with the proofs of the round bounds)
  - paper: "Karl Abrahamson, Norm Dadoun, David G. Kirkpatrick and Teresa Przytycka, A simple parallel tree contraction algorithm, Journal of Algorithms 10(2), 1989"
    title: A simple parallel tree contraction algorithm
    locator: pp. 287 to 302 (the deterministic shunt method in O(log n) time with n / log n processors on the EREW PRAM)
  - paper: "Richard Cole and Uzi Vishkin, The accelerated centroid decomposition technique for optimal parallel tree evaluation in logarithmic time, Algorithmica 3, 1988"
    title: The accelerated centroid decomposition technique for optimal parallel tree evaluation in logarithmic time
    locator: pp. 329 to 346 (a work-efficient deterministic tree evaluation)
  - book: isbn:9780201548563
    title: Joseph JaJa, An Introduction to Parallel Algorithms, Addison-Wesley, 1992
    locator: Chapter 3, Section 3.3 (tree contraction with the rake operation and arithmetic expression evaluation)
---

Tree contraction is a parallel technique that reduces a rooted tree to its root in $O(\log n)$ rounds, whatever the shape of the tree. Each round does two steps. RAKE removes every leaf and folds its value into its parent. COMPRESS removes an [independent set](/independent-set/) of nodes with exactly one child and links each one's child to its parent, which is one round of [list contraction](/list-contraction/) on the chains of the tree. RAKE alone is slow on a long path, and COMPRESS alone does nothing on a complete binary tree, but together they remove a constant fraction of the nodes in each round. Miller and Reif (1985) introduced it, and it gives $O(\log n)$ span algorithms for [expression evaluation](/tree-expression-evaluation/) and many other computations on trees. With random choices it does $O(n)$ expected work.

Notation on this page: $n$ is the number of nodes, $m$ the number of live nodes other than the root at the start of a round, $W$ the work and $S$ the span in the [work-span model](/work-span-model/). The tree is rooted and each node has at most two children; a node with one child is *unary*.

## In plain words

You want to fold a big family tree into one card held by the oldest person. Each person holds a card with a number.

In each round two things happen. First, every person with no children gives their card to their parent and leaves. Second, in each chain of people with one child each, some people step out: each one gives their card to their parent and hands their child over to that parent. A coin decides who steps out, and two neighbours in a chain never both step out.

The first step clears bushy trees fast, and the second clears long chains fast. Each round removes a fair share of the people in any family shape, so the tree is gone in a few rounds. Each person who left can later get their own answer back.

## When it applies

- The input is a rooted tree, and the result is a fold over the tree: the value at a node depends on the values of its children through a known rule.
- RAKE needs a way to fold a leaf into its parent, and COMPRESS needs a way to fold a unary node into the link between its parent and its child. COMPRESS works when the effect of a chain of unary nodes on the value that passes up has a constant-size closed form, such as a sum, a linear function or a $2 \times 2$ matrix.
- You need low span. A sequential postorder walk does $\Theta(n)$ work, and recursion on the subtrees has span equal to the height, which can be $n$.

## The template

Each live node $v$ has $parent[v]$, its live children, and a value $val[v]$. The holes are the RAKE fold, the COMPRESS fold, the CHOOSE rule, the BASE case at the root and the EXPAND step.

```pseudo id=main
TREE-CONTRACT(T)                               ▷ T: a rooted tree, each node with at most two children
L1  while the root has a live child do
L2      for each live node p in parallel: for each leaf child u of p: val[p] ← RAKE(val[p], val[u]); remove u
L3      for each live node v in parallel: coin[v] ← a fair random bit
L4      C ← { v : v is unary, v ≠ root, coin[v] = H, and not (parent[v] is unary, parent[v] ≠ root, coin[parent[v]] = H) }    ▷ CHOOSE
L5      for each v ∈ C in parallel: c ← the child of v; parent[c] ← parent[v]; the parent takes c as its child and sets val[parent[v]] ← COMPRESS(val[parent[v]], val[v])
L6      pack the live nodes; push C on a stack
L7  BASE: compute the result at the root from val[root]
L8  pop the sets C, the last first, and EXPAND each removed node from the result of its child
```

In line L2 the parent does the work for its leaf children (owner computes), so no two leaves write to the same parent at the same time. In line L4 the rule is the random mate rule of [list contraction](/list-contraction/) on the chains of unary nodes. A node in $C$ has heads, and its parent, if unary, has tails, so no two nodes of $C$ are adjacent. Line L5 again lets each parent pull in the values of its children in $C$, since a node with two children can have both of them in $C$.

### Why a round removes a constant fraction

**Lemma 1.** Let a round start with $m \ge 1$ live non-root nodes, and let $D$ be the set removed by lines L2 and L5. Then $\mathbb{E}[|D|] \ge m/8$.

*Proof.* Let $\ell$ be the number of leaves (all non-root, since $m \ge 1$), $b$ the number of nodes with two children and $u$ the number of unary nodes, counting the root in $b$ or $u$. In a tree with at most two children per node, $b \le \ell - 1$, because the leaves of a tree number one more than its nodes with two children, and nodes with one child do not change this. If $\ell \ge m/8$, line L2 alone removes $\ell \ge m/8$ nodes. Otherwise $u = (m + 1) - \ell - b \ge m - 2\ell + 2$. A unary node whose child is not a leaf keeps its one child after line L2. At most $\ell$ unary nodes have a leaf child, and at most one is the root, so at least $u - \ell - 1 \ge m - 3\ell + 1 > 5m/8$ non-root nodes are unary at line L4. Each such node $v$ is in $C$ when $coin[v] = H$ and its parent is not a unary non-root node with heads, which has probability at least $\frac12 \cdot \frac12 = \frac14$. By [linearity of expectation](/linearity-of-expectation/), $\mathbb{E}[|C|] > \frac14 \cdot \frac{5m}{8} \ge \frac{m}{8}$. $\square$

**Rounds.** Let $m_r$ be the number of live non-root nodes at the start of round $r$, so $m_1 = n - 1$. Lemma 1 gives $\mathbb{E}[m_{r+1} \mid m_r] \le \frac78 m_r$, so $\mathbb{E}[m_{r+1}] \le (7/8)^r (n - 1)$. The loop runs more than $r$ rounds only if $m_{r+1} \ge 1$, so by the [Markov inequality](/markov-inequality/) $\Pr[R > r] \le (7/8)^r (n - 1)$. Summing as on the [list contraction](/list-contraction/) page gives $\mathbb{E}[R] \le \log_{8/7} n + 9$, and $R \le (k + 1)\log_{8/7} n$ with probability at least $1 - n^{-k}$. Here $\log_{8/7} n \approx 5.19 \lg n$; the bound is loose, and the tests measure about $2 \lg n$ rounds on a path, which is the slowest shape.

**Work and span.** A round costs $O(m_r)$ work, including the pack of line L6, so $\mathbb{E}[W] = O(\sum_r (7/8)^r n) = O(n)$. A round has span $O(\log n)$ for the pack and $O(1)$ for the rest, so $S = O(\log^2 n)$ with high probability. On a PRAM with the pack done by prefix sums, the time is $O(\log^2 n)$ with $n$ processors; the next sections give the ways to reach $O(\log n)$.

**Correctness of EXPAND.** A removed node keeps its child pointer and value from the moment it left, because later rounds only change live nodes. The child of a node removed by COMPRESS stays live in that round, so it is removed later or is the root, and its result is ready when line L8 handles the earlier round. A raked leaf has no live child, so its result is already final when it leaves.

## Classic examples

**All subtree sums.** Let $val[v]$ start as the weight of $v$, and let both RAKE and COMPRESS add the value of the removed node to its parent. Then for each live $v$ the invariant is: the subtree sum of $v$ is $val[v]$ plus the subtree sums of its live children. A raked leaf has subtree sum $val[u]$ when it leaves. A compressed node $v$ with child $c$ has subtree sum $val[v] + \mathrm{sub}(c)$, which EXPAND computes. The implementation on this page does this and checks it against a postorder walk with an explicit stack.

Take the tree with root 0, children 1 and 2 of node 0, child 3 of node 1, children 4 and 5 of node 3, child 6 of node 2, child 7 of node 6 and child 8 of node 7, all with weight 1.

| round | RAKE removes | after RAKE | unary non-root nodes, coins | COMPRESS removes | values after the round |
|---|---|---|---|---|---|
| 1 | 4, 5, 8 | val[3] = 3, val[7] = 2 | 1 H, 2 T, 6 H | 1, 6 | val[0] = 2, val[2] = 2; tree 0 → {3, 2}, 2 → {7} |
| 2 | 3, 7 | val[0] = 5, val[2] = 4 | none | none | tree 0 → {2} |
| 3 | 2 | val[0] = 9 | none | none | only the root |

Node 6 is removed because its parent 2 has tails; node 1 is removed because its parent is the root. EXPAND gives $\mathrm{sub}(1) = 1 + \mathrm{sub}(3) = 4$ and $\mathrm{sub}(6) = 1 + \mathrm{sub}(7) = 3$. The full result is $[9, 4, 4, 3, 1, 1, 3, 2, 1]$ by node number.

**Expression evaluation.** The [tree expression evaluation](/tree-expression-evaluation/) page keeps on each edge a linear function $x \mapsto ax + b$ that tells how a value changes on its way up. RAKE evaluates a leaf into its parent's operator, which gives a linear function of the other child, and COMPRESS composes linear functions. This was the first application of Miller and Reif.

**Dynamic programs on trees.** Many tree dynamic programs pass a small vector up the tree, and a unary chain acts on it as a fixed map. When these maps have a constant-size closed form under composition, for example a $2 \times 2$ matrix over the $(\max, +)$ semiring for a maximum weight [independent set](/independent-set/) on a tree, tree contraction evaluates the program in $O(\log n)$ rounds.

**Dynamic trees.** The rake and compress operations are also the base of data structures for trees that change over time, such as top trees (Alstrup, Holm, de Lichtenberg and Thorup) and rake and compress trees (Acar, Blelloch and coworkers), which keep a contraction of the tree and repair it after each edge change.

## Variations

- **Deterministic shunt.** Abrahamson, Dadoun, Kirkpatrick and Przytycka (1989) number the leaves from left to right with the [Euler tour technique](/euler-tour-technique/) and [list ranking](/list-ranking/). Each round rakes the leaves with odd numbers, first the left children and then the right children, and each rake also removes the leaf's parent (the shunt). The numbers halve in each round, so a tree with $\ell$ leaves needs exactly $\lceil \lg \ell \rceil$ rounds, with $O(n)$ work and no random bits, on the [EREW PRAM](/erew-pram/). The [tree expression evaluation](/tree-expression-evaluation/) page uses this form.
- **Work-efficient and O(log n) time.** Miller and Reif gave $O(\log n)$ time with $n / \log n$ processors randomized, and with $n$ processors deterministic. Cole and Vishkin (1988) and the shunt method reach $O(\log n)$ time with $O(n)$ work deterministically.
- **Trees of any degree.** Replace each node with $d$ children by a chain of $d - 1$ nodes with two children each. The tree keeps $O(n)$ nodes, and with an associative fold the results at the original nodes do not change. Or rake all leaf children of a node at once with a [parallel reduce](/parallel-reduce/), which costs $O(\log d)$ span.
- **Forests.** A forest needs no change: each tree contracts to its own root at the same time.

## Pitfalls

- **Two leaves rake into one parent.** If line L2 lets each leaf write into its parent, the two children of a node write $val[p]$ at the same time, and one update can be lost. Let the parent pull in its leaf children, or rake the left children and the right children in two substeps.
- **Compressing adjacent nodes.** If line L4 takes all unary nodes with heads, a node and its parent can both leave, and the node then links its child to a parent that is gone. Line L4 must ask that the parent is not a unary node with heads.
- **Compressing the root.** The root has no parent to take its child. Line L4 excludes it, and the loop of line L1 stops when only the root is left.
- **EXPAND in the wrong order.** A compressed node needs the result of its child, which may have been removed in a later round. Line L8 must handle the last round first.
- **Folding the wrong way.** For subtree sums the value of a compressed node must go to its parent, not to its child, because the child's subtree does not contain it. For a value that flows up, such as an expression, the fold must instead be composed in the right order with the function on the child's edge.

## Exercises

1. Show that on a path of $n$ nodes RAKE removes exactly one node per round, so the progress comes from COMPRESS. Show that on a perfect binary tree with $2^k - 1$ nodes COMPRESS never removes a node, and RAKE needs exactly $k - 1$ rounds.
2. In the proof of Lemma 1, show the bound $b \le \ell - 1$ for a tree in which each node has at most two children.
3. Change the CHOOSE rule so that $v$ is removed when it has heads and its child has tails. Prove that $C$ is still independent and that Lemma 1 still holds.
4. Use tree contraction to compute the depth of each node. What do RAKE, COMPRESS and EXPAND store?

## References
