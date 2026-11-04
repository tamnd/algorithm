---
tag: WJ2D8W
kind: concept
slug: random-binary-search-tree
name: Randomly built binary search tree
aliases:
- random BST
- randomly built BST
area: data-structures/search-trees
level: core
summary: A binary search tree built by inserting keys in random order, whose expected height is logarithmic in the number of keys.
prereqs: [binary-search-tree, bst-insertion, random-permutation, harmonic-series]
see_also: [random-bst-expected-depth, expected-search-cost-bst, randomized-quicksort, treap, zip-tree, catalan-numbers, bst-deletion, skip-list]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.2 (Binary tree searching), the analysis of trees built by random insertions
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 12.4 (Randomly built binary search trees)
  - paper: doi:10.1145/5925.5930
    title: Luc Devroye, A note on the height of binary search trees, Journal of the ACM 33(3), 1986
    locator: pages 489 to 498
  - paper: doi:10.1145/765568.765571
    title: Bruce Reed, The height of a random binary search tree, Journal of the ACM 50(3), 2003
    locator: pages 306 to 332
---

A randomly built binary search tree is the [binary search tree](/binary-search-tree/) that results when $n$ distinct keys are inserted by [leaf insertion](/bst-insertion/) into an empty tree in a uniformly [random order](/random-permutation/), each of the $n!$ orders having the same probability. Its expected depth of a node is about $2 \ln n \approx 1.39 \lg n$, and its expected height is about $4.311 \ln n \approx 2.99 \lg n$ (Devroye 1986). It is the model behind the average-case analysis of BST search, of [randomized quicksort](/randomized-quicksort/), and of randomized trees such as the [treap](/treap/), which build this same tree whatever the input order.

## In plain words

If you put keys into a plain search tree in sorted order, you get a long chain, and searches are slow. If you put them in a shuffled order, the first key is the root, and it is a random key, so it splits the rest into two parts of random sizes. Each part is again built from a shuffled order, so it splits again.

A split is rarely very uneven, so after a few levels the parts are small. The tree is not perfectly balanced, but a typical path from the root has length close to twice the natural log of the number of keys, which is short.

## The idea

**The model.** Fix keys $x_1 < x_2 < \cdots < x_n$. Choose a permutation $\pi$ uniformly at random and insert $x_{\pi(1)}, x_{\pi(2)}, \ldots, x_{\pi(n)}$. Only the relative order of the keys matters, so the keys can be taken as $1, 2, \ldots, n$.

**The recursive view.** The first key inserted is the root, and its rank is uniform on $1, \ldots, n$. Given that the root has rank $i$, the keys below it arrive in a uniformly random relative order, and so do the keys above it, independently. So the left subtree is a random BST on $i - 1$ keys and the right subtree is a random BST on $n - i$ keys. Most results follow from this recursion.

**Ancestors.** Key $j$ is an ancestor of key $i$ exactly when $j$ is the first key inserted among the keys with ranks from $\min(i,j)$ to $\max(i,j)$. This has probability $1/(|i - j| + 1)$. Summing over $j$ gives the expected depth of the key of rank $i$,
$$\mathbb{E}[\mathrm{depth}(i)] = H_i + H_{n-i+1} - 2,$$
where $H_m$ is the $m$-th harmonic number. The proof is on the page [expected depth of random BSTs](/random-bst-expected-depth/).

**Link with quicksort.** In the tree, a key is compared with exactly its ancestors when it is inserted. In quicksort with the pivot chosen as the first element of a randomly ordered array, two keys are compared exactly when one is an ancestor of the other in this tree. So the cost of building the tree equals the number of comparisons of quicksort, $2(n+1)H_n - 4n$ in expectation.

**Shapes are not uniform.** There are $C_n$ BST shapes on $n$ keys (a [Catalan number](/catalan-numbers/)) but $n!$ orders, and the map from orders to shapes is not even. For $n = 3$, 6 orders give 5 shapes: the balanced shape comes from the 2 orders $(2,1,3)$ and $(2,3,1)$, and each of the 4 chains from one order. So the random BST favours bushy shapes; a tree with uniform shape has expected height of order $\sqrt n$, not $\log n$.

**The main facts.** For a random BST on $n$ keys:

| quantity | exact value or asymptotics |
|---|---|
| expected depth of the key of rank $i$ | $H_i + H_{n-i+1} - 2$ |
| average node depth | $2(1 + 1/n) H_n - 4 \sim 2 \ln n$ |
| nodes visited in a successful search, $C_n$ | $2(1 + 1/n) H_n - 3$ |
| nodes visited in an unsuccessful search, $C'_n$ | $2 H_{n+1} - 2$ |
| comparisons to build the tree | $2(n+1)H_n - 4n$ |
| expected height | $\le 3 \lg n + O(1)$; asymptotically $\alpha \ln n - \beta \ln \ln n + O(1)$ |
| expected number of leaves ($n \ge 2$) | $(n + 1)/3$ |
| probability of a chain | $2^{n-1}/n!$ |

Here $\alpha \approx 4.311$ is the root above 2 of $\alpha \ln(2e/\alpha) = 1$ (Devroye 1986), and Reed (2003) found $\beta = 3/(2 \ln(\alpha/2)) \approx 1.953$ and showed that the variance of the height is $O(1)$.

**Deletions.** The model covers trees built by inserts only. A tree that is built at random and then changed by [Hibbard deletion](/bst-deletion/) is no longer a random BST: the asymmetric choice of the successor tilts the shape. Treaps and randomized BSTs keep the exact distribution under both inserts and deletes.

## Examples

**All orders of 3 keys.**

| order | shape | height | depths of 1, 2, 3 |
|---|---|---|---|
| 1, 2, 3 | right chain | 2 | 0, 1, 2 |
| 1, 3, 2 | 1 with right child 3, which has left child 2 | 2 | 0, 2, 1 |
| 2, 1, 3 | balanced | 1 | 1, 0, 1 |
| 2, 3, 1 | balanced | 1 | 1, 0, 1 |
| 3, 1, 2 | 3 with left child 1, which has right child 2 | 2 | 1, 2, 0 |
| 3, 2, 1 | left chain | 2 | 2, 1, 0 |

The expected height is $(4 \cdot 2 + 2 \cdot 1)/6 = 5/3$. The expected depths of keys 1, 2, 3 are $5/6$, $1$, $5/6$, which match $H_i + H_{4-i} - 2$: for $i = 1$, $1 + 11/6 - 2 = 5/6$, and for $i = 2$, $3/2 + 3/2 - 2 = 1$. The average depth is $8/9 = 2(1 + 1/3)H_3 - 4$. The expected number of leaves is $(4 \cdot 1 + 2 \cdot 2)/6 = 4/3 = (3 + 1)/3$.

**Six keys.** Over all $720$ orders of 6 keys, the height is 2 in 80 orders, 3 in 400, 4 in 208 and 5 (a chain) in $32 = 2^5$, so the expected height is $49/15 \approx 3.27$, against the bound $\lg(9 \cdot 8 \cdot 7/24) = \lg 21 \approx 4.39$ of CLRS. The average depth is $103/60 \approx 1.72$, and the 132 shapes appear between 1 and 20 times each.

**Large $n$.** For $n = 10^6$, $2 \ln n \approx 27.6$ while $\lg n \approx 19.9$, so a typical search in a random BST takes about 39% more comparisons than in a perfectly balanced tree, and the expected height is near $4.311 \ln n - 1.953 \ln \ln n \approx 59.6 - 5.1 \approx 54$ up to the $O(1)$ term.

## Where it is used

- **Average-case analysis of BST operations.** Search, insert and the cost of [tree sort](/tree-sort/) on random input. See [expected search cost](/expected-search-cost-bst/).
- **Quicksort and quickselect.** The recursion tree of [randomized quicksort](/randomized-quicksort/) is a random BST, so its comparisons and depth follow from the same facts.
- **Treaps and zip trees.** A [treap](/treap/) gives each key a random priority and keeps the tree that the priority order would build, so it is a random BST for each input order, under inserts and deletes. A [zip tree](/zip-tree/) does the same with random ranks.
- **Skip lists.** A [skip list](/skip-list/) has a similar analysis: random levels play the role of the random order.
- **Testing.** A random BST is the standard random input for tests and benchmarks of tree code.
- **Probability.** The height of a random BST is a classic problem on branching random walks, and the methods of Devroye and Reed are used for other random trees.

## References
