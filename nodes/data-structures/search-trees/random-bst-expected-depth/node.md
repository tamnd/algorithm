---
tag: ZDXZ6S
kind: theorem
slug: random-bst-expected-depth
name: Expected depth of random binary search trees
aliases:
- random BST height bound
area: data-structures/search-trees
level: core
summary: A BST built from random insertion orders has expected height O(log n) and expected node depth O(log n).
prereqs: [random-binary-search-tree, indicator-random-variable, linearity-of-expectation, jensens-inequality, harmonic-series]
see_also: [expected-search-cost-bst, randomized-quicksort, treap, bst-search, catalan-numbers, skip-list]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 12.4 (Randomly built binary search trees), Theorem 12.4 and its proof with exponential height
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.2 (Binary tree searching), the average number of comparisons in a tree built by random insertions
  - paper: doi:10.1145/5925.5930
    title: Luc Devroye, A note on the height of binary search trees, Journal of the ACM 33(3), 1986
    locator: pages 489 to 498
  - paper: doi:10.1145/765568.765571
    title: Bruce Reed, The height of a random binary search tree, Journal of the ACM 50(3), 2003
    locator: pages 306 to 332
  - paper: doi:10.1145/321105.321108
    title: Thomas N. Hibbard, Some combinatorial properties of certain trees with applications to searching and sorting, Journal of the ACM 9(1), 1962
    locator: pages 13 to 28
---

In a [randomly built binary search tree](/random-binary-search-tree/) on $n$ keys, the expected depth of each node is at most $2 \ln n + O(1)$, and the expected height is at most $3 \lg n + O(1)$. The depth bound is exact: the key of rank $i$ has expected depth $H_i + H_{n-i+1} - 2$. The height bound is the theorem of CLRS (third edition, Section 12.4), proved with the exponential height and [Jensen's inequality](/jensens-inequality/); Devroye (1986) found the exact constant, $4.311 \ln n \approx 2.99 \lg n$.

## Statement

Let $n \ge 1$, and let $T_n$ be the binary search tree built by inserting the keys $1, 2, \ldots, n$ into an empty tree by leaf insertion, in the order of a uniformly random permutation. The depth of the root is 0, and the height $X_n$ of $T_n$ is the largest depth of a node. $H_m = \sum_{j=1}^{m} 1/j$ is the $m$-th harmonic number.

**Theorem.**

1. **(Depth of a key.)** For $1 \le i \le n$, the depth $D_i$ of key $i$ satisfies
$$\mathbb{E}[D_i] = H_i + H_{n-i+1} - 2 \le 2 \ln n.$$
2. **(Average depth.)** $\displaystyle \frac{1}{n} \sum_{i=1}^{n} \mathbb{E}[D_i] = 2\left(1 + \frac{1}{n}\right) H_n - 4.$
3. **(Height.)** $\displaystyle \mathbb{E}[2^{X_n}] \le \frac{1}{4}\binom{n+3}{3}$, and so $\mathbb{E}[X_n] \le \lg \frac{(n+1)(n+2)(n+3)}{24} \le 3 \lg n + O(1)$.

## In plain words

Put keys into a plain search tree in a random order. Then each key ends up, on average, at a depth of about twice the natural log of the number of keys. Keys in the middle are a little deeper than keys at the ends. Also the deepest key of the whole tree is, on average, at a depth of at most about three times the base-2 log. So in a tree built from shuffled data, every search is short on average, and even the worst path is short on average.

## Proof

**Lemma 1 (ancestors).** For keys $i \ne j$, key $j$ is a proper ancestor of key $i$ in $T_n$ if and only if $j$ is inserted before every other key in the closed range $R_{ij}$ between $i$ and $j$ (that is, $\{\min(i,j), \ldots, \max(i,j)\}$).

*Proof.* Let $m$ be the first key of $R_{ij}$ inserted, and suppose $m \ne j$. If $m = i$, then $i$ is in the tree when $j$ arrives, so $j$ is not an ancestor of $i$, because the ancestors of a node are inserted before it. Otherwise $m$ lies strictly between $i$ and $j$. Each node inserted before $m$ is outside $R_{ij}$, so it is less than both $i$ and $j$ or greater than both, and the search paths of $i$ and $j$ agree down to $m$. At $m$ they part: one goes left and the other goes right. So $i$ and $j$ are in different subtrees of $m$, and neither is an ancestor of the other.

Conversely, suppose $j$ is the first key of $R_{ij}$ inserted. Each node on the search path of $j$ was inserted before $j$, so it is not in $R_{ij}$, so it is less than both $i$ and $j$ or greater than both. Hence, when $i$ is inserted later, its search path follows the path of $j$ down to $j$ (the comparisons with those nodes give the same answers) and then continues below $j$. So $j$ is a proper ancestor of $i$. $\square$

**Part 1.** Write $A_{ij}$ for the [indicator](/indicator-random-variable/) of the event "$j$ is a proper ancestor of $i$". The depth of $i$ is the number of its proper ancestors, $D_i = \sum_{j \ne i} A_{ij}$. The range $R_{ij}$ has $|i - j| + 1$ keys, and in a uniformly random order each of them is the first of the range with the same probability, so $\Pr[A_{ij} = 1] = 1/(|i - j| + 1)$. By [linearity of expectation](/linearity-of-expectation/),
$$\mathbb{E}[D_i] = \sum_{j=1}^{i-1} \frac{1}{i - j + 1} + \sum_{j=i+1}^{n} \frac{1}{j - i + 1} = \sum_{d=2}^{i} \frac{1}{d} + \sum_{d=2}^{n-i+1} \frac{1}{d} = (H_i - 1) + (H_{n-i+1} - 1).$$
Since $H_m \le 1 + \ln m$ and $i, n - i + 1 \le n$, this is at most $\ln i + \ln(n - i + 1) \le 2 \ln n$.

**Part 2.** Sum part 1 over $i$: $\sum_{i=1}^{n} (H_i + H_{n-i+1}) = 2 \sum_{i=1}^{n} H_i$, and $\sum_{i=1}^{n} H_i = (n+1)H_n - n$ (each $1/j$ appears in $H_j, \ldots, H_n$, that is $n - j + 1$ times, and $\sum_j (n+1-j)/j = (n+1)H_n - n$). So the total expected depth is $2(n+1)H_n - 2n - 2n = 2(n+1)H_n - 4n$, and dividing by $n$ gives $2(1 + 1/n)H_n - 4$.

**Part 3.** Define the exponential height $Y_n = 2^{X_n}$ for $n \ge 1$, and set $Y_0 = 0$. Let $R$ be the rank of the root, which is the first key inserted, so $R$ is uniform on $\{1, \ldots, n\}$. Given $R = i$, the left subtree is a random BST on $i - 1$ keys and the right subtree a random BST on $n - i$ keys, because the relative orders of the keys below $i$ and above $i$ are uniform and independent. For $n \ge 2$ at least one subtree is not empty, and the height of $T_n$ is one more than the larger height of the two subtrees, so
$$Y_n = 2 \max(Y_{i-1}, Y_{n-i}) \quad \text{given } R = i,$$
where the convention $Y_0 = 0$ makes the empty subtree lose the maximum. (For $n = 1$, $Y_1 = 2^0 = 1$.) Since $\max(a, b) \le a + b$ for $a, b \ge 0$, for $n \ge 2$
$$\mathbb{E}[Y_n] = \frac{1}{n} \sum_{i=1}^{n} 2\,\mathbb{E}[\max(Y_{i-1}, Y_{n-i})] \le \frac{2}{n} \sum_{i=1}^{n} \left(\mathbb{E}[Y_{i-1}] + \mathbb{E}[Y_{n-i}]\right) = \frac{4}{n} \sum_{m=0}^{n-1} \mathbb{E}[Y_m].$$
Now prove $\mathbb{E}[Y_n] \le \frac14 \binom{n+3}{3}$ by strong induction. For $n = 0$, $0 \le \frac14$. For $n = 1$, $1 \le \frac14 \binom{4}{3} = 1$. For $n \ge 2$, by the recurrence, the induction hypothesis, and the identity $\sum_{m=0}^{n-1} \binom{m+3}{3} = \binom{n+3}{4}$ (the hockey-stick identity),
$$\mathbb{E}[Y_n] \le \frac{4}{n} \cdot \frac14 \binom{n+3}{4} = \frac{(n+3)(n+2)(n+1)}{24} = \frac14 \binom{n+3}{3}.$$
Finally $2^x$ is convex, so by Jensen's inequality $2^{\mathbb{E}[X_n]} \le \mathbb{E}[2^{X_n}] = \mathbb{E}[Y_n]$. Taking $\lg$ of both sides,
$$\mathbb{E}[X_n] \le \lg \frac{(n+1)(n+2)(n+3)}{24} \le 3 \lg(n + 3) - \lg 24 = 3 \lg n + O(1). \qquad \blacksquare$$

## Consequences

- **Average search cost.** A successful search visits $D_i + 1$ nodes, so its expected cost for a uniformly random key is $2(1 + 1/n)H_n - 3$, about $1.39 \lg n$. See [expected search cost](/expected-search-cost-bst/) and [BST search](/bst-search/).
- **Building cost and quicksort.** The total depth $2(n+1)H_n - 4n$ is the number of comparisons to build the tree, and also the expected number of comparisons of [randomized quicksort](/randomized-quicksort/), whose recursion tree is a random BST.
- **Treaps.** A [treap](/treap/) has the shape of a random BST for each input, so its operations take $O(\log n)$ expected time by this theorem.
- **Worst search on average.** Part 3 bounds the expected cost of the slowest search in the tree, not only a typical one: $O(\log n)$.
- **Tail bound.** From $\mathbb{E}[2^{X_n}] \le n^3$ for $n \ge 1$ and the [Markov inequality](/markov-inequality/), $\Pr[X_n \ge c \lg n] \le n^{3 - c}$; for example the height exceeds $5 \lg n$ with probability at most $1/n^2$.

## Tightness

- **Part 1 is exact.** Part 2 is the exact average, and it is $2 \ln n + O(1)$, so the constant 2 in front of $\ln n$ cannot be improved. Over all 6 orders of 3 keys the depths of keys 1, 2, 3 average $5/6, 1, 5/6$, which is $H_i + H_{4-i} - 2$; over the 720 orders of 6 keys the average depth is $103/60 = 2(7/6)H_6 - 4$.
- **Part 3 is tight up to a factor near 1.** Devroye (1986) proved $\mathbb{E}[X_n] / \ln n \to \alpha$, where $\alpha \approx 4.31107$ is the solution above 2 of $\alpha \ln(2e/\alpha) = 1$. In base 2 this is $\alpha \ln 2 \approx 2.988$, so the bound $3 \lg n$ is off only in the lower-order terms. Reed (2003) proved $\mathbb{E}[X_n] = \alpha \ln n - \beta \ln \ln n + O(1)$ with $\beta = 3/(2 \ln(\alpha/2)) \approx 1.953$, and that the variance of $X_n$ is $O(1)$.
- **For small $n$.** The expected height for $n = 3$ is $5/3$ and for $n = 6$ is $49/15 \approx 3.27$, while part 3 gives $\lg 5 \approx 2.32$ and $\lg 21 \approx 4.39$.
- **Not in the worst case.** A fixed bad order, such as sorted input, gives height $n - 1$. The theorem is about the average over orders.

## History

Hibbard (1962) and Knuth (Volume 3, Section 6.2.2) found the exact average number of comparisons in a tree built by random insertions. CLRS gave the short proof of the $O(\log n)$ bound on the expected height with the exponential height, used here. Devroye (1986) found the constant $\alpha$, and Reed (2003) the second-order term and the bounded variance.

## References
