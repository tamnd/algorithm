---
tag: QBKXJ6
kind: technique
slug: dsu-on-tree
name: DSU on tree
aliases:
- Sack
- small-to-large on trees
area: graphs/tree-algorithms
level: advanced
summary: Answer subtree queries by keeping the heavy child's data and adding light subtrees.
prereqs: [subtree-sizes, euler-tour-technique, heavy-light-decomposition]
see_also: [heavy-light-decomposition, euler-tour-subtree-queries, weighted-union-find, mo-algorithm, range-distinct-count-query, centroid-decomposition, union-by-rank, subtree-sizes]
sources:
  - url: https://codeforces.com/blog/entry/44351
    title: Arpa, Sack (dsu on tree), Codeforces blog
    locator: the O(n log^2 n) version with merged maps, the O(n log n) version that keeps the big child, and the list of practice problems
  - url: https://usaco.guide/plat/merging
    title: USACO Guide, Small-To-Large Merging
    locator: the sections Merging Data Structures, Better Solution and Generalizing, with the O(n log n) bound on the number of moves
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 19, Section 19.2 (Linked-list representation of disjoint sets), the weighted-union heuristic and the argument that each element moves O(log n) times
---

DSU on tree, also called *sack* or small-to-large on trees, answers a question about every subtree of a [rooted tree](/rooted-tree/) offline, when the answer depends on a multiset of vertex data that can be built up by adding one vertex at a time: "how many distinct colors are in the subtree of $v$", "which color is most frequent". For each vertex, the data of its *heavy* child, the child with the largest subtree, is kept and extended, and the *light* children's subtrees are added vertex by vertex. Each vertex is added once for itself and once for each light edge above it, which is at most $\lfloor \log_2 n \rfloor$ times, so all $n$ answers cost $O(n \log n)$ additions and removals. The name comes from the weighted-union rule of disjoint sets: the smaller set is moved into the larger one.

## In plain words

Each person in a family tree has a favorite color. For every person, you want to know how many different colors their whole family branch likes. Counting each branch from scratch is slow, because a big branch is counted again and again for every person above it.

Instead, keep one notebook of colors. For each person, take over the notebook of their biggest child branch as it is, and then add the people of the smaller child branches one by one, and the person. A person is copied in only when they sit in a smaller branch, and each time that happens the branch around them at least doubles in size. So nobody is copied more than a few times, even in a huge tree.

## When it applies

- The tree is static and rooted, with vertices numbered $0, \ldots, n-1$; weights or colors sit on the vertices, and the edges are unweighted.
- All queries are known in advance (offline) and each one asks about one whole subtree.
- The answer comes from a data structure $D$ that supports $\mathrm{add}(x)$, $\mathrm{remove}(x)$ and $\mathrm{answer}()$ quickly, for example a count per color and a count of colors with a non-zero count. The data structure does not need to support merging two structures, which is the point of the technique.
- The answer is not a simple sum: for sums and other group operations, the [Euler tour with a Fenwick tree](/euler-tour-subtree-queries/) answers the same questions online and with updates.

## The template

Let $size(v)$ be the number of vertices in the subtree of $v$. The *heavy child* $heavy(v)$ is a child with the largest size (ties broken by the smallest label), and the other children are light. The heavy edges form vertex-disjoint *heavy paths*, as in [heavy-light decomposition](/heavy-light-decomposition/): each path starts at a *head*, the root or a light child, and follows heavy children down to a leaf. Let $tin$ and $tout$ be entry and exit times of an [Euler tour](/euler-tour-technique/), and $ver[t]$ the vertex with $tin = t$, so the subtree of $u$ is $ver[tin(u) .. tout(u) - 1]$.

The usual recursive form, "solve the light children and forget them, solve the heavy child and keep it, add the light subtrees", is replaced by an equivalent loop over the heavy paths, with no recursion:

```pseudo id=main
DSU-ON-TREE(T, r)                 ▷ holes: ADD, REMOVE, ANSWER of the structure D
L1  compute size, heavy, tin, tout and ver by BFS and loops
L2  for each head h of a heavy path do
L3      let h = v_1, v_2, ..., v_k be the heavy path, from the head down to the leaf v_k
L4      for j ← k down to 1 do                       ▷ bottom-up; D holds the subtree of v_{j+1}
L5          ADD(v_j)
L6          for each light child u of v_j do
L7              for t ← tin(u) to tout(u) - 1 do ADD(ver[t])
L8          answer[v_j] ← ANSWER()                    ▷ D holds exactly the subtree of v_j
L9      for t ← tin(h) to tout(h) - 1 do REMOVE(ver[t])   ▷ D is empty again
```

The holes are the three operations of $D$. The order of the heavy paths in line L2 does not matter, so the loop can take the heads in any order.

**Why it works.** The subtree of $v_j$ is $v_j$, the subtree of $v_{j+1}$, and the subtrees of the light children of $v_j$. By induction from the bottom of the path, after lines L5 to L7 at step $j$, $D$ holds the subtree of $v_{j+1}$ (from the step before; empty for $j = k$, since $v_k$ is a leaf) plus $v_j$ plus its light subtrees, which is the subtree of $v_j$. So line L8 reads the right answer. After $j = 1$, $D$ holds the subtree of $h$, and line L9 removes exactly those vertices.

**Why it is fast.** A vertex $x$ is added in line L5 once, at its own heavy path, and in line L7 once for each light child $u$ of an ancestor such that $x$ is in the subtree of $u$, that is, once per light edge on the path from $x$ to the root. Line L9 removes $x$ once per head whose subtree contains it, which is again 1 plus the number of light edges above $x$. If $u$ is a light child of $v$, then $size(v) \ge 2\, size(u)$, because the heavy child is at least as big as $u$. So the sizes at least double at each light edge going up, and there are at most $\lfloor \log_2 n \rfloor$ light edges above any vertex.

### Cost

Lines L2 to L9 call ADD and REMOVE at most $n(\lfloor \log_2 n \rfloor + 1)$ times each and ANSWER $n$ times. With $O(1)$ operations on $D$, such as arrays of counts indexed by color, the total time is $O(n \log n)$, and the extra space is $O(n)$ plus the size of $D$. Line L1 takes $O(n)$.

## Classic examples

The examples use the tree on $0, \ldots, 11$ rooted at 0 with the parent array $[-, 0, 1, 2, 3, 4, 2, 6, 0, 8, 3, 7]$, children ordered by label, and subtree sizes $[12, 9, 8, 4, 2, 1, 3, 2, 2, 1, 1, 1]$:

```
0
├── 1
│   └── 2
│       ├── 3
│       │   ├── 4
│       │   │   └── 5
│       │   └── 10
│       └── 6
│           └── 7
│               └── 11
└── 8
    └── 9
```

The heavy children are $heavy = [1, 2, 3, 4, 5, -, 7, 11, 9, -, -, -]$. The heavy paths are $0, 1, 2, 3, 4, 5$; $6, 7, 11$; $8, 9$; and $10$, with the heads 0, 6, 8 and 10. The light edges are $0 \to 8$, $2 \to 6$ and $3 \to 10$.

**1. Distinct colors in each subtree.** The colors are $c = [1, 2, 1, 3, 2, 2, 3, 1, 1, 2, 3, 1]$. $D$ is an array $cnt$ of counts per color and the number $dist$ of colors with $cnt > 0$; ADD and REMOVE update both in $O(1)$. On the path with head 0, from the bottom:

| $v_j$ | added in L5 and L7 | colors in $D$ | answer |
|---|---|---|---|
| 5 | 5 | 2 | 1 |
| 4 | 4 | 2, 2 | 1 |
| 3 | 3; light child 10 | 2, 2, 3, 3 | 2 |
| 2 | 2; light child 6: 6, 7, 11 | adds 1, 3, 1, 1 | 3 |
| 1 | 1 | adds 2 | 3 |
| 0 | 0; light child 8: 8, 9 | adds 1, 1, 2 | 3 |

The other paths give 2 for vertex 6 (colors 3 and 1), 1 for 7 and 11, 2 for 8, and 1 for 9 and 10. So the answers are $[3, 3, 3, 2, 1, 1, 2, 1, 2, 1, 1, 1]$, which agree with a direct count in each subtree. There are 18 ADD calls in all: the 12 vertices once each, and the 6 vertices 6, 7, 11, 8, 9 and 10 once more, each below one light edge. Building each subtree from scratch would take $\sum_v size(v) = 46$ additions, and $\Theta(n^2)$ on a path.

**2. The most frequent color in each subtree.** $D$ keeps $cnt$ per color, the number of colors with each count, and the largest count; ADD and REMOVE keep them in $O(1)$. This is Codeforces 600E, Lomsat gelral, the classic practice problem for the technique.

**3. Queries "how many vertices of the subtree of $v$ at depth $d$ have property $P$".** $D$ keeps an array indexed by depth. Attach each query to its $v$ and answer it in line L8.

**4. Pairs of vertices whose LCA is $v$.** For each light child $u$ of $v$, first ask $D$ about the vertices of the subtree of $u$, then add them; this counts pairs from different branches of $v$, for example pairs whose values sum to $k$, in $O(n \log n)$.

## Variations

- **Small-to-large with mergeable maps.** Give each vertex its own map, and merge the smaller map into the larger one at each vertex, keeping the larger. Each element moves $O(\log n)$ times; with balanced-tree maps that costs $O(n \log^2 n)$ and with hash maps $O(n \log n)$ expected. This is the first version in Arpa's blog and the main idea of the USACO Guide page.
- **The recursive form.** dfs$(v, keep)$: solve the light children with $keep = $ false, the heavy child with $keep = $ true, add the light subtrees and $v$, answer, and remove the subtree if $keep$ is false. It does the same additions as the loop above, but its recursion is as deep as the tree.
- **The weighted union of disjoint sets.** In the linked-list representation of disjoint sets, appending the shorter list to the longer one makes each element move $O(\log n)$ times (CLRS Section 19.2). DSU on tree is the same argument applied to the subtrees of a tree, hence its name.
- **[Mo's algorithm](/mo-algorithm/) on the Euler tour.** Subtree queries are ranges of the Euler tour, so Mo's algorithm also answers them, with $O(n \sqrt{q})$ additions. DSU on tree is faster for subtree queries; Mo's handles paths too.
- **Online and with updates.** If colors change between queries, the technique does not apply; a range structure over the Euler tour, or a persistent structure, is needed.

## Pitfalls

- **Wrong heavy child.** Choosing the first child instead of the largest one breaks the bound: on a "caterpillar" where the big part is always the last child, the additions become $\Theta(n^2)$.
- **Clearing too much or too little.** The removal of line L9 must take exactly the subtree of the head. Clearing the whole array $cnt$ instead costs $O(\text{number of colors})$ per head and can be quadratic; forgetting to clear leaves stale counts in the next path.
- **Answering too early.** Line L8 must come after the light subtrees of $v_j$ are added. In the recursive form, answering before adding the light children gives the answer for the heavy child's subtree plus $v$.
- **Recursion depth.** The recursive form fails on a path of $10^5$ vertices in Python; the loop over heavy paths above, with a BFS for line L1, does not.
- **Queries that need the order of additions.** $D$ sees the vertices in no particular order. A question such as "the $k$-th vertex of the subtree in preorder" needs another method.

## Exercises

1. Show that on a path $0 - 1 - \cdots - (n-1)$ rooted at 0, there is one heavy path and DSU on tree makes exactly $n$ ADD calls.
2. Show that on a star rooted at its center with $n - 1$ leaves, there are $2n - 2$ ADD calls, and that this is less than $n(\lfloor \log_2 n \rfloor + 1)$ for $n \ge 2$.
3. Find a family of trees on which the number of ADD calls is $\Theta(n \log n)$. (Hint: a perfect binary tree.)
4. For the single-vertex tree, check that the loop answers vertex 0 with one ADD and one REMOVE.
5. Extend example 1 to answer, for each $v$, the number of colors that occur exactly twice in the subtree of $v$.
6. Explain why the order in which line L2 takes the heads does not change the result, and why the loop needs no stack.

## References
