---
tag: WX20H4
kind: problem
slug: ordered-tree-generation
name: Ordered tree generation
aliases:
- Plane tree generation
- Generating ordered trees
- Generating rooted plane trees
area: combinatorics/generating-partitions-and-trees
level: core
summary: Enumerate all rooted trees where the children of each node are ordered, with n nodes.
model: word-ram
complexity:
  vars: {n: the number of nodes, N: the number of ordered trees (the Catalan number of n - 1)}
  time: {worst: Θ(N)}
prereqs: [rooted-tree, dyck-word, catalan-numbers]
see_also: [binary-tree-generation, balanced-parentheses-generation, rooted-tree-generation, level-sequence, zaks-tree-generation, cycle-lemma, next-balanced-bracket-sequence, euler-tour-technique]
sources:
  - url: https://page.math.tu-berlin.de/~felsner/SemWS17-18/Ruskey-Comb-Gen.pdf
    title: Frank Ruskey, Combinatorial Generation, working version, University of Victoria, 1995 to 2003
    locator: Section 2.10.1, Ordered Trees (the bijections with binary trees and well-formed parentheses), Section 4.6.1, Binary Trees, Ordered Trees, and the bibliographic remarks of Chapter 4 (ordered forests with a given degree sequence)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.2.1.6, Generating all trees (forests, nested parentheses, and the natural correspondence with binary trees)
  - paper: doi:10.1016/0012-365X(80)90168-5
    title: Nachum Dershowitz and Shmuel Zaks, Enumerations of ordered trees, Discrete Mathematics 31 (1980), 9 to 28
    locator: the counts of ordered trees by nodes, leaves and degrees, and the cycle lemma
---

Ordered tree generation is the problem of listing every ordered tree with $n$ nodes exactly once. An ordered tree, also called a plane tree, is a [rooted tree](/rooted-tree/) in which the children of each node have a fixed order, first, second and so on. There are $N = C_{n-1}$ such trees, a [Catalan number](/catalan-numbers/), because the depth-first walk of a tree is a [Dyck word](/dyck-word/) of semilength $n - 1$. So a generator for Dyck words, level sequences or binary trees lists ordered trees in $\Theta(N)$ time when the code is changed in place.

## In plain words

An ordered tree is a family tree in which the order of the children matters: a node with an older and a younger child is a different tree from the one with the two swapped, if the two subtrees differ. You want every such tree with a fixed number of nodes.

Walk around the tree, starting at the root and keeping the tree on your left. Write an opening bracket each time you go down an edge and a closing bracket each time you come back up. Every tree gives a correct bracket string, and every correct string gives back one tree. So listing all ordered trees is the same as listing all correct bracket strings, and the fast methods for the strings work here with no change.

## Definition

An *ordered tree* is a root node together with a finite sequence $(T_1, \ldots, T_d)$ of ordered trees, its subtrees, with $d \ge 0$. Its size is the number of nodes. Let $O_n$ be the set of ordered trees with $n \ge 1$ nodes, up to shape.

**Input:** an integer $n \ge 1$.

**Output:** a sequence that contains each tree of $O_n$ exactly once. Its length is $|O_n| = C_{n-1} = \frac{1}{n}\binom{2n-2}{n-1}$.

**Cost model.** The [word RAM](/word-ram/). The current tree, in one of the codes below, is kept in an array and visited in place. The cost of a step is the number of array cells read and changed. If each tree must be copied out, add $\Theta(n)$ per tree.

## Variants

- **Code.** The *depth-first word*: $\texttt{(}$ for each step down an edge and $\texttt{)}$ for each step up, a Dyck word of length $2n - 2$. The [level sequence](/level-sequence/) $(\ell_1, \ldots, \ell_n)$, the depths of the nodes in preorder, with $\ell_1 = 0$ and $1 \le \ell_{i+1} \le \ell_i + 1$. The *degree sequence* $(d_1, \ldots, d_n)$, the numbers of children in preorder, with $\sum_{j \le i} (d_j - 1) \ge 0$ for $i < n$ and total $-1$. A parent array.
- **Order.** Lexicographic order of one of the codes, or a [Gray code](/gray-code/) in which consecutive trees differ by moving one subtree.
- **Restricted trees.** Trees with a given number of leaves, there are $\frac{1}{n-1}\binom{n-1}{k}\binom{n-1}{k-1}$ with $k$ leaves for $n \ge 2$; trees with bounded height; trees with a given degree sequence; and $t$-ary trees, in which every internal node has exactly $t$ children.
- **Forests.** Ordered forests with $n$ nodes, sequences of ordered trees. Removing the root of a tree of $O_{n+1}$ gives a forest with $n$ nodes, and this is a bijection, so there are $C_n$ forests.
- **Random generation.** A uniform random ordered tree. By the [cycle lemma](/cycle-lemma/), among the $2n - 1$ rotations of a sequence of $n - 1$ up steps and $n$ down steps, exactly one is the depth-first word of a tree followed by one final down step. So a uniform random arrangement, then the right rotation, gives a uniform random tree in $O(n)$ time.

## Examples

For $n = 4$ there are $C_3 = 5$ ordered trees. The table lists them in decreasing lexicographic order of the level sequences, which is increasing lexicographic order of the depth-first words with $\texttt{(} < \texttt{)}$.

| level sequence | depth-first word | the tree |
|---|---|---|
| 0123 | `((()))` | a path of 4 nodes |
| 0122 | `(()())` | the root has one child, which has two children |
| 0121 | `(())()` | the root has two children, and the first has one child |
| 0112 | `()(())` | the root has two children, and the second has one child |
| 0111 | `()()()` | the root has three children |

The third and fourth trees are the same rooted tree with the children in a different order, so they are different ordered trees but one unordered [rooted tree](/rooted-tree-generation/).

The counts by the number $k$ of leaves are the Narayana numbers. For $n = 5$ they are 1, 6, 6, 1 for $k = 1, 2, 3, 4$, a total of $C_4 = 14$. For $n = 6$ they are 1, 10, 20, 10, 1, a total of $C_5 = 42$.

## Known algorithms

| method | order | cost of the full listing | worst step |
|---|---|---|---|
| [lexicographic successor](/next-balanced-bracket-sequence/) of the depth-first word | lexicographic | $\Theta(C_{n-1})$ | $O(n)$ |
| successor of the level sequence | reverse lexicographic | $\Theta(C_{n-1})$ | $O(n)$ |
| [Zaks' algorithm](/zaks-tree-generation/) on z-sequences | lexicographic | $\Theta(C_{n-1})$ | $O(n)$ |
| binary tree Gray code by rotations, through the rotation correspondence | one rotation per step | $\Theta(C_{n-1})$ | $O(1)$ on a pointer machine |
| [unrank](/kth-balanced-bracket-sequence/) each $k = 0, \ldots, C_{n-1} - 1$ | lexicographic | $\Theta(n C_{n-1})$ | $O(n)$ |

- **Through Dyck words.** Run the [next balanced bracket sequence](/next-balanced-bracket-sequence/) rule on the depth-first word of length $2n - 2$. It is CAT, and the word is the tree.
- **Level sequences.** In decreasing lexicographic order, the successor of $(\ell_1, \ldots, \ell_n)$ finds the largest $p$ with $\ell_p \ge 2$, lowers $\ell_p$ by 1, and sets $\ell_{i} = \ell_{i-1} + 1$ for $i > p$. The list starts at $(0, 1, \ldots, n-1)$, the path, and ends at $(0, 1, 1, \ldots, 1)$, the star. It is the same list as the Dyck word list, in another code. Adding a canonical test to this rule gives the [Beyer-Hedetniemi algorithm](/beyer-hedetniemi/) for unordered rooted trees.
- **Zaks.** The positions of the internal nodes in preorder, for binary and $t$-ary trees, in lexicographic order, with ranking and unranking.
- **Gray codes.** The rotation correspondence maps the rotation Gray code of binary trees with $n - 1$ nodes to a list of ordered trees with $n$ nodes in which each step moves one subtree. See [binary tree generation](/binary-tree-generation/).

## Bounds

- Visiting every tree takes $\Omega(C_{n-1})$ steps, and the methods above meet this bound, so the problem takes $\Theta(N)$ time in the cost model above.
- Writing every tree out in full takes $\Theta(n C_{n-1})$ time.
- Since $C_{n-1} \sim 4^{n-1} / (\sqrt{\pi}\, n^{3/2})$, a full listing is practical only for small $n$; for $n = 21$ there are already $C_{20} = 6564120420$ trees.

## Reductions

- **Dyck words.** The depth-first word is a bijection from $O_n$ onto the Dyck words of semilength $n - 1$. So this problem is [generating balanced parentheses](/balanced-parentheses-generation/) with a translation of $O(n)$ time per tree, or no translation at all when the word itself is the code.
- **Binary trees.** The *rotation correspondence* (first child becomes left child, next sibling becomes right child) maps the forest of subtrees of the root of a tree in $O_n$ to a binary tree with $n - 1$ nodes, one to one. So this problem is [binary tree generation](/binary-tree-generation/) for $n - 1$ nodes.
- **Rooted trees.** An unordered [rooted tree](/rooted-tree-generation/) is a class of ordered trees under the reordering of children. Choosing one ordered tree per class, such as the one with the lexicographically largest level sequence, turns ordered tree generation into rooted tree generation.
- **Euler tours.** The depth-first word is the [Euler tour](/euler-tour-technique/) of the tree read as up and down steps.

## Applications

- Exhaustive tests of code that walks or edits ordered trees, such as parsers, syntax trees and document trees, on every shape up to a given size.
- Listing the shapes of expressions, of nested lists or of nested function calls.
- Random test trees by the cycle lemma, with a guaranteed uniform distribution over shapes.

## References
