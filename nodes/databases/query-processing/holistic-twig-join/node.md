---
tag: JKP2FG
kind: algorithm
slug: holistic-twig-join
name: Holistic twig join
aliases:
- TwigStack
area: databases/query-processing
level: advanced
summary: "Match a tree pattern of an XML query over sorted element streams with one stack per query node. With only ancestor-descendant edges, no intermediate result is wasted."
model: word-ram
complexity:
  vars: {n: the number of elements in all streams, k: the number of query nodes, l: the number of leaves of the twig, z: the number of matches, d: the depth of the document}
  time: {worst: "O(k (n + l z))"}
  space: {extra: "O(k d + k l z)"}
properties: {deterministic: true, exact: true, external: true, online: false, in_place: false, recursive: true}
history:
  year: 2002
  people: [Nicolas Bruno, Nick Koudas, Divesh Srivastava]
  note: "Bruno, Koudas and Srivastava gave PathStack and TwigStack at SIGMOD 2002."
prereqs: [euler-tour-technique, stack, multiway-join]
see_also: [generic-join, yannakakis-algorithm, sort-merge-join, depth-first-search, tree-pattern-matching, lowest-common-ancestor, interval-tree, relational-join]
sources:
  - paper: doi:10.1145/564691.564727
    title: "Nicolas Bruno, Nick Koudas and Divesh Srivastava, Holistic twig joins: optimal XML pattern matching, SIGMOD 2002, pages 310 to 321"
    locator: the algorithms PathStack and TwigStack, getNext, the proof of correctness and the optimality for twigs with only ancestor-descendant edges
  - paper: doi:10.1109/ICDE.2002.994704
    title: "Shurug Al-Khalifa, H. V. Jagadish, Nick Koudas, Jignesh M. Patel, Divesh Srivastava and Yuqing Wu, Structural joins: a primitive for efficient XML query pattern matching, ICDE 2002, pages 141 to 152"
    locator: binary structural joins on region codes with stacks, which a plan of binary joins combines
  - paper: doi:10.1145/375663.375722
    title: "Chun Zhang, Jeffrey Naughton, David DeWitt, Qiong Luo and Guy Lohman, On supporting containment queries in relational database management systems, SIGMOD 2001, pages 425 to 436"
    locator: the region encoding of elements and containment joins on it
  - paper: doi:10.1007/978-3-540-45227-0_4
    title: "Byron Choi, Malika Mahoui and Derick Wood, On the optimality of holistic algorithms for twig queries, DEXA 2003, Lecture Notes in Computer Science, pages 28 to 37"
    locator: the limits of optimality of holistic twig algorithms when the twig has parent-child edges
  - paper: doi:10.1145/1031171.1031272
    title: "Jiaheng Lu, Ting Chen and Tok Wang Ling, Efficient processing of XML twig patterns with parent child edges: a look-ahead approach, CIKM 2004, pages 533 to 542"
    locator: a look-ahead variant of TwigStack for twigs with parent-child edges
---

A holistic twig join finds all matches of a small tree pattern, a *twig*, in an XML document. It reads one sorted stream of elements for each node of the twig, and it keeps one stack per node, so that it handles the whole pattern at once. TwigStack, the algorithm of Bruno, Koudas and Srivastava, outputs a partial match for each root-to-leaf path of the twig and then joins these. When every edge of the twig is an ancestor-descendant edge, every partial match is part of a final match. A plan of binary structural joins can build large intermediate results that the final answer does not use. This is a [multiway join](/multiway-join/) on containment of intervals, not on equal values as in [generic join](/generic-join/), and it is not the [tree pattern matching](/tree-pattern-matching/) of term rewriting, which matches children in a fixed order.

## In plain words

A book has chapters, sections and figures, nested inside each other. You want every chapter that holds both a figure and a table somewhere inside it.

In one walk through the book, give each part two numbers: where it begins and where it ends. Then one part is inside another exactly when its numbers lie between the numbers of the other.

Now keep a list of all chapters, all figures and all tables, each in order of where it begins. Read the three lists together from the front. Keep a pile of the chapters that are still open. When you read a figure, pair it with each open chapter, and do the same for a table. At the end, join the figure pairs and the table pairs on their chapter. The algorithm opens a chapter only when it already sees a figure and a table ahead inside it.

## The problem

**Data model.** An XML document is an ordered tree of *elements*, and each element has a tag, such as `book` or `figure`. Text and attributes do not matter here. One depth-first walk gives each element a *region code* $(\mathit{start}, \mathit{end}, \mathit{level})$: a counter value when the walk enters the element, a counter value when it leaves, and the depth. This is the [Euler tour](/euler-tour-technique/) numbering of the tree. Then $u$ is an ancestor of $v$ if and only if $u.\mathit{start} < v.\mathit{start}$ and $v.\mathit{end} < u.\mathit{end}$, and $u$ is the parent of $v$ if also $v.\mathit{level} = u.\mathit{level} + 1$.

**Query.** A twig is a tree of query nodes. Each node has a tag, and each edge has an axis: // (ancestor-descendant) or / (parent-child). In XPath, `a[.//b]//c` is the twig with root $a$ and two children $b$ and $c$ on // edges. A *match* maps each query node to an element with its tag so that every edge holds. Two query nodes may map to the same element if the edges allow it.

**Input and output.** For each query node $q$ the input is the stream $T_q$ of all elements with the tag of $q$, sorted by start, as an index on tags gives them. The output is the set of all matches. The cost is the number of elements read and the size of the intermediate results, in the [word RAM](/word-ram/).

## The algorithm

Each query node $q$ has a [stack](/stack/) $S_q$. Each entry of $S_q$ holds an element and a pointer to the top entry of the parent stack at the time of its push. The entries of a stack are nested, the innermost on top, so the stack is a path in the document.

```pseudo id=main
TWIGSTACK(Q)
L1  while some leaf stream of Q is not exhausted do
L2      q ← GETNEXT(root)
L3      if q is not the root then pop from S_parent(q) every entry that ends before start(head(T_q))
L4      if q is the root or S_parent(q) is not empty then
L5          pop from S_q every entry that ends before start(head(T_q)); push (head(T_q), top of S_parent(q)) on S_q; advance T_q
L6          if q is a leaf then output the path solutions of the new entry, through the pointers; pop it
        else
L7          advance T_q              ▷ this element has no ancestor that can be part of a match
L8  join the path solutions of all leaves on their common query nodes
GETNEXT(q)
L9  if q is a leaf then return q
L10 for each child c of q whose leaf streams are not all exhausted do n ← GETNEXT(c); if n ≠ c then return n
L11 n_min ← that child with the smallest start of its head; far ← the largest start of a head among all children, ∞ for an exhausted child
L12 while end(head(T_q)) < far do advance T_q
L13 if start(head(T_q)) < start(head(T_{n_min})) then return q else return n_min
```

GETNEXT returns a query node whose head can be the start of a match below it: the heads of its children lie inside its head, and so on down to the leaves. Line L12 drops heads of $T_q$ that end before the head of some child begins, because such an element cannot hold an element of that child stream. A path solution is the list of elements on one root-to-leaf path. Line L6 forms it by taking, in the parent stack, every entry at or below the pointer, and so on up to the root, and it keeps a combination only when each edge of the path holds. For a // edge the test always passes; for a / edge it compares levels.

The implementation does not call GETNEXT on a child whose leaf streams are all exhausted (line L10) and treats that child as being at infinity (line L11). Without this, GETNEXT can return a node whose stream is empty.

## Example

Take the document $a_1(b_1, a_2(b_2, c_1), c_2, a_3(b_3))$ and the twig `a[.//b]//c`. The region codes are $a_1 = (0, 15, 0)$, $b_1 = (1, 2, 1)$, $a_2 = (3, 8, 1)$, $b_2 = (4, 5, 2)$, $c_1 = (6, 7, 2)$, $c_2 = (9, 10, 1)$, $a_3 = (11, 14, 1)$ and $b_3 = (12, 13, 2)$. The streams are $T_a = a_1, a_2, a_3$, $T_b = b_1, b_2, b_3$ and $T_c = c_1, c_2$.

| step | GETNEXT returns | action | $S_a$ after the step | path solutions output |
|---|---|---|---|---|
| 1 | $a$ | push $a_1$ | $a_1$ | |
| 2 | $b$ | push $b_1$, output, pop | $a_1$ | $(a_1, b_1)$ |
| 3 | $a$ | push $a_2$ | $a_1, a_2$ | |
| 4 | $b$ | push $b_2$, output, pop | $a_1, a_2$ | $(a_1, b_2)$, $(a_2, b_2)$ |
| 5 | $c$ | push $c_1$, output, pop | $a_1, a_2$ | $(a_1, c_1)$, $(a_2, c_1)$ |
| 6 | $c$ | pop $a_2$, which ends at 8, before 9; push $c_2$, output, pop | $a_1$ | $(a_1, c_2)$ |
| 7 | $b$ | inside GETNEXT, $T_c$ is exhausted, so line L12 drops $a_3$; then push $b_3$, output, pop | $a_1$ | $(a_1, b_3)$ |

Line L8 joins the 4 path solutions of $b$ with the 3 path solutions of $c$ on $a$. This gives $3 \cdot 2 = 6$ matches with $a_1$ and 1 match $(a_2, b_2, c_1)$, so 7 in all. Every path solution is used. The element $a_3$ is never pushed, because no $c$ lies inside it.

## Correctness

The proof keeps an invariant for each match: an element of the match is never skipped or dropped, it is pushed after the element of its parent, it stays on its stack while a leaf below it still waits, and its pointer reaches the element of its parent. The key lemma is that the node that GETNEXT returns has a head that starts no later than any waiting element of a match in the relevant part of the twig. So a stack never loses an element that a later leaf still needs. When a leaf element of a match is pushed, its whole path is on the stacks, and its path solution is output. The join of line L8 then gives every match once. The full proof is in [the proof page](proofs/correctness.md).

For twigs with only // edges, the same lemma gives more. When GETNEXT returns $q$, the heads below $q$ form a match of the subtwig at $q$. So each pushed element can be extended below, and every path solution is part of some match. This is the optimality of TwigStack. With a / edge the heads are nested but need not be parent and child, and the guarantee fails.

## Complexity

- **Reads.** Each element of each stream is read once, in order, so the streams can be scanned from disk. The main loop runs at most $n$ times, and each call of GETNEXT visits each query node at most once, which gives $O(k n)$ for the scan with the exhausted streams tracked by counters.
- **Path solutions.** For twigs with only // edges, each leaf has at most $z$ path solutions, so there are at most $l z$ of them, each of length at most $k$. Bruno et al. prove that TwigStack then runs in time and I/O linear in the size of the input and the output, with the query size as a factor.
- **Space.** Each stack is a chain of nested elements, so it holds at most $d$ entries. The path solutions are kept until line L8, or written to disk in sorted order and merged.
- **Parent-child edges.** The bound in the front matter is for twigs with only // edges. With / edges, the number of path solutions is not bounded by the output. In the document $a(b(c))$, the twig `a[.//b]/c` gives the path solution $(a, b)$ and no match.

## Properties

- **Holistic.** The algorithm treats the twig as one unit. A plan of binary structural joins has to choose an order, and each intermediate result is a match of part of the twig that may not extend to the whole.
- **Streaming.** Each stream is read once from the front, so the input needs only a sort by start, which an index on tags provides.
- **Output order.** Path solutions of a leaf come out in order of the leaf element. The final join needs them sorted on the common prefix, or a hash table.
- **Non-injective matches.** Two sibling query nodes with the same tag can match the same element, as in XPath.

## Variants and improvements

- **PathStack.** For a twig that is a single path, the same stacks give the matches directly, without the join of line L8. Bruno et al. give it in the same paper.
- **Skipping with an index.** Bruno et al. also use a B-tree variant on each stream, so that line L12 and the advance of line L7 can skip many elements at once.
- **Look-ahead for parent-child edges.** Lu, Chen and Ling (2004) look ahead in the streams before a push, to avoid many useless path solutions when the twig has / edges. Choi, Mahoui and Wood (2003) studied the limits of optimality for such twigs.
- **Binary structural joins.** Al-Khalifa et al. (2002) join two streams at a time on ancestor-descendant or parent-child with a stack. A plan of such joins is simpler, but its intermediate results can be much larger than the output.

## When to use it

Use a holistic twig join when XML or other tree-shaped data is stored with region codes and an index on tags, and queries are twigs of a few nodes, mainly with // edges. With many / edges a look-ahead variant is better, and with a selective index on values a navigation from the few candidate elements can be faster.

## Pitfalls

- **Region codes from different walks.** The ancestor test needs start and end values from one walk of one document. Codes of different documents need a document id in front.
- **An exhausted subtree.** If GETNEXT goes into a child whose leaf streams are all exhausted, it can return a node with an empty stream, and the main loop then makes no progress. The implementation skips such children and treats them as infinitely far.
- **Parent-child edges.** The level test removes wrong combinations, so the result is correct, but the path solutions are no longer bounded by the output.
- **Non-strict tests.** The ancestor test must be strict on both sides. Since all codes of one walk are distinct, a test with $\le$ in place of $<$ makes an element its own ancestor.

## Implementations

## History

Zhang, Naughton, DeWitt, Luo and Lohman (2001) stored XML in relations with region codes and evaluated containment queries with joins. Al-Khalifa, Jagadish, Koudas, Patel, Srivastava and Wu (2002) gave stack-based binary structural joins. Bruno, Koudas and Srivastava (SIGMOD 2002) gave PathStack and TwigStack, which process the whole twig at once, and proved that TwigStack is optimal for twigs with only ancestor-descendant edges. Later work, such as that of Choi, Mahoui and Wood (2003) and of Lu, Chen and Ling (2004), studied twigs with parent-child edges.

## References
