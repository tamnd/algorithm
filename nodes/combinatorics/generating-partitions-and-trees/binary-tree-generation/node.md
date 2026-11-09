---
tag: 3YAKJD
kind: problem
slug: binary-tree-generation
name: Binary tree generation
aliases:
- Enumerating binary trees
- Generating all binary trees
- Listing binary tree shapes
area: combinatorics/generating-partitions-and-trees
level: core
summary: Enumerate all binary trees with n nodes; there are Catalan-many of them.
model: word-ram
complexity:
  vars: {n: the number of nodes, N: the number of binary trees (the Catalan number of n)}
  time: {worst: Θ(N)}
prereqs: [binary-tree, catalan-numbers, dyck-word]
see_also: [balanced-parentheses-generation, ordered-tree-generation, zaks-tree-generation, next-balanced-bracket-sequence, kth-balanced-bracket-sequence, tree-rotation, random-binary-search-tree, output-sensitive-generation]
sources:
  - url: https://page.math.tu-berlin.de/~felsner/SemWS17-18/Ruskey-Comb-Gen.pdf
    title: Frank Ruskey, Combinatorial Generation, working version, University of Victoria, 1995 to 2003
    locator: Section 4.6.1, Binary Trees, Ordered Trees (tree sequences, Algorithm 4.16 and its CAT analysis), Section 5.5.2, Binary Trees (Theorem 5.3 and Algorithm 5.17, a Gray code by rotations), Section 5.12.1 (the loopless version) and the bibliographic remarks of Chapter 4
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.2.1.6, Generating all trees (binary trees, nested parentheses and their correspondences)
  - paper: doi:10.1016/0304-3975(80)90073-0
    title: Shmuel Zaks, Lexicographic generation of ordered trees, Theoretical Computer Science 10 (1980), 63 to 82
    locator: the z-sequence of a binary tree or t-ary tree, its lexicographic generation and its ranking
---

Binary tree generation is the problem of listing every binary tree with $n$ nodes exactly once, where each node has a left subtree and a right subtree, either of which can be empty. There are $N = C_n$ such trees, the $n$-th [Catalan number](/catalan-numbers/). Each tree is encoded as a bracket word, a bit sequence or a sequence of integers, and a generator for the code is a generator for the trees. With the tree kept in one data structure and only the changes made, the problem takes $\Theta(N)$ time, and a Gray code of rotations does it with $O(1)$ worst-case time per tree.

## In plain words

You want every possible shape of a binary tree with a fixed number of nodes. A shape says, for each node, whether it has a left child and whether it has a right child. Three nodes give five shapes; ten nodes give 16796.

One way is to write each shape as a string of brackets: put the left subtree inside a pair of brackets, and the right subtree after it. Then list all correct bracket strings in dictionary order. Another way changes the tree in place by one small move, a rotation, between one shape and the next, so that each new shape costs only a few pointer changes.

## Definition

A *binary tree* is either empty or a triple $(L, r, R)$ of a root node $r$ and two binary trees, the left subtree $L$ and the right subtree $R$. Its size is its number of nodes. Let $B_n$ be the set of binary trees with $n$ nodes, where two trees are the same when they have the same shape.

**Input:** an integer $n \ge 0$.

**Output:** a sequence that contains each tree of $B_n$ exactly once. The number of trees satisfies $|B_0| = 1$ and $|B_n| = \sum_{\ell = 0}^{n-1} |B_\ell|\, |B_{n-1-\ell}|$, by the size $\ell$ of the left subtree, so $|B_n| = C_n = \frac{1}{n+1}\binom{2n}{n}$.

**Cost model.** The [word RAM](/word-ram/). The current tree, or its code, is kept in one data structure and visited in place after each step. The cost of a step is the number of cells or pointers read and changed. If each tree must be copied out, add $\Theta(n)$ per tree.

## Variants

- **Order.** Lexicographic order of a code (bracket words, bit sequences or Zaks' sequences), or a [Gray code](/gray-code/) in which consecutive trees differ by one [rotation](/tree-rotation/).
- **Code.** The bracket word $\mathrm{code}(\varnothing) = \varepsilon$, $\mathrm{code}(L, r, R) = \texttt{(}\,\mathrm{code}(L)\,\texttt{)}\,\mathrm{code}(R)$; the *tree sequence* of Ruskey, which writes 1 for each node and 0 for each empty subtree in preorder and drops the last 0, and is the same word with $1 = \texttt{(}$; the *z-sequence* of Zaks, the preorder positions of the nodes in the extended tree; or a linked structure with left and right pointers.
- **Direct access.** [Ranking](/balanced-bracket-sequence-ranking/) and [unranking](/kth-balanced-bracket-sequence/) of the code. See [ranking and unranking](/ranking-unranking/).
- **Random generation.** Draw one tree of $B_n$ uniformly at random. Unranking a uniform integer in $[0, C_n)$ does it with big integers; Rémy's method grows a uniform tree by inserting one node at a time in $O(n)$ time.
- **Restricted trees.** Trees of bounded height, trees with a given number of leaves, or full $t$-ary trees, in which every internal node has exactly $t$ children. There are $\frac{1}{(t-1)n + 1}\binom{tn}{n}$ full $t$-ary trees with $n$ internal nodes.

## Examples

For $n = 3$ the $C_3 = 5$ trees are listed below in the lexicographic order of their bracket codes with $\texttt{(} < \texttt{)}$. A node is named by its path from the root: L for a step to the left child and R for a step to the right child.

| bracket code | tree sequence | nodes |
|---|---|---|
| `((()))` | 111000 | root, L, LL |
| `(()())` | 110100 | root, L, LR |
| `(())()` | 110010 | root, L, R |
| `()(())` | 101100 | root, R, RL |
| `()()()` | 101010 | root, R, RR |

The first tree is a path of left children and the last one a path of right children. The middle one is the only tree with 3 nodes whose root has two children.

The number of trees grows fast:

| $n$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| $C_n$ | 1 | 1 | 2 | 5 | 14 | 42 | 132 | 429 | 1430 | 4862 | 16796 |

## Known algorithms

| method | order | cost of the full listing | worst step |
|---|---|---|---|
| [lexicographic successor](/next-balanced-bracket-sequence/) of the code | lexicographic | $\Theta(C_n)$ | $O(n)$ |
| recursion on the size of the left subtree | by left size | $\Theta(C_n)$ with shared subtrees | $O(n)$ |
| [Zaks' algorithm](/zaks-tree-generation/) on z-sequences | lexicographic | $\Theta(C_n)$ | $O(n)$ |
| Gray code by rotations (Lucas, Roelants van Baronaigien and Ruskey) | one rotation per step | $\Theta(C_n)$ | $O(1)$ on a pointer machine |
| [unrank](/kth-balanced-bracket-sequence/) each $k = 0, \ldots, C_n - 1$ | lexicographic | $\Theta(n C_n)$ | $O(n)$ |

- **Lexicographic successor.** Ruskey's Algorithm 4.16 finds the rightmost 0 of the tree sequence that has a 1 to its right, sets it to 1, and fills the rest in the smallest way. It is the [next balanced bracket sequence](/next-balanced-bracket-sequence/) rule in the other alphabet. A step costs $O(q)$, where $q$ is the length of the last block of 0s, and the average of $q$ over all trees is less than 3, so the method is CAT.
- **Recursion on the left subtree.** For $\ell = 0, \ldots, n - 1$, combine each tree of $B_\ell$ as the left subtree with each tree of $B_{n-1-\ell}$ as the right subtree. This is the natural method in a functional language. When subtrees are shared, the number of new nodes built is $\Theta(C_n)$; when every tree is built from scratch, the cost is $\Theta(n C_n)$.
- **Zaks' sequences.** The z-sequence of a tree with $n$ nodes is the increasing list $z_1 < \cdots < z_n$ of the preorder positions of its nodes in the extended tree with $2n + 1$ nodes. The valid sequences are exactly those with $z_i \le 2i - 1$. Zaks lists them in lexicographic order, which is the lexicographic order of the bracket codes, and ranks them, for binary and for $t$-ary trees. The successor step changes a suffix, and its average cost is below 2 array cells.
- **Rotations.** The rotation graph, whose vertices are the trees of $B_n$ and whose edges are single rotations, has a Hamilton path (Ruskey, Theorem 5.3). The list starts from the list for $n - 1$ nodes and moves node $n$ up and down the right path of the tree by rotations. The recursive form is CAT, because the recursion tree has $C_1 + \cdots + C_n$ nodes, which is less than $1.5 C_n$ for $n \ge 6$. With extra pointers and a direction bit per node, the next rotation can be found in $O(1)$ worst-case time.

## Bounds

- Visiting every tree takes $\Omega(C_n)$ steps, and the methods above meet this bound, so the problem takes $\Theta(N)$ time in the cost model above.
- Writing every tree out in full takes $\Theta(n C_n)$ time.
- In a lexicographic list of codes, a single step can change $\Theta(n)$ cells, so a loopless method that keeps a code in an array must use a Gray code order. On a linked structure, one rotation changes $O(1)$ pointers, and the rotation Gray code is loopless.
- Since $C_n \sim 4^n / (\sqrt{\pi}\, n^{3/2})$, a full listing is practical only up to about $n = 20$, where $C_{20} = 6564120420$.

## Reductions

- **Bracket words.** The map $\mathrm{code}$ above is a bijection from $B_n$ onto the [Dyck words](/dyck-word/) of semilength $n$, and so binary tree generation and [generating balanced parentheses](/balanced-parentheses-generation/) are the same problem with a translation of $O(n)$ time per object.
- **Ordered trees and forests.** The *rotation correspondence* (left child becomes first child, right child becomes next sibling) is a bijection from $B_n$ onto ordered forests with $n$ nodes, and so onto ordered trees with $n + 1$ nodes, by adding a root. See [ordered tree generation](/ordered-tree-generation/).
- **Other Catalan families.** Triangulations of a convex polygon with $n + 2$ sides ([Catalan triangulation theorem](/catalan-triangulation-theorem/)) and full parenthesizations of a product of $n + 1$ factors ([counting parenthesizations](/counting-parenthesizations/)) are also in bijection with $B_n$.
- **Binary search trees.** The shapes of $B_n$ are exactly the shapes of the [binary search trees](/binary-search-tree/) on $n$ keys. A rotation keeps the inorder sequence of the keys, which is why the rotation Gray code also lists all binary search trees on fixed keys.

## Applications

- Exhaustive tests of code for [binary search trees](/binary-search-tree/), balanced trees and tree traversals on every shape up to a given size.
- Listing all evaluation orders of an expression, or all candidate shapes in an [optimal binary search tree](/optimal-binary-search-tree/) study.
- Random test inputs, by unranking or by Rémy's method. Note that a uniform random shape differs in distribution from the shape of a [random binary search tree](/random-binary-search-tree/), which is built from a random permutation.

## References
