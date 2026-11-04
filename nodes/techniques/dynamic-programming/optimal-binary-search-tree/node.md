---
tag: JN2M83
kind: problem
slug: optimal-binary-search-tree
name: Optimal binary search tree
aliases:
- Optimal binary search tree problem
- optimal BST
- optimal BST problem
- static optimal BST
area: techniques/dynamic-programming
level: core
summary: Build a binary search tree that minimises expected search cost for given access probabilities.
prereqs: [binary-search-tree, expected-search-cost-bst, interval-dp]
see_also: [optimal-bst-dynamic-programming, knuth-optimization, hu-tucker-algorithm, garsia-wachs-algorithm, weight-balanced-tree, huffman-coding, matrix-chain-multiplication, splay-tree]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 14.5 (optimal binary search trees)
  - paper: doi:10.1007/BF00264289
    title: Donald E. Knuth, Optimum binary search trees, Acta Informatica 1(1), 1971
    locator: pp. 14 to 25
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.2 (binary tree searching, optimum binary search trees)
  - paper: doi:10.1137/0121057
    title: T. C. Hu and A. C. Tucker, Optimal computer search trees and variable-length alphabetical codes, SIAM Journal on Applied Mathematics 21(4), 1971
    locator: pp. 514 to 532
  - paper: doi:10.1137/0206045
    title: Adriano M. Garsia and Michelle L. Wachs, A new algorithm for minimum cost binary trees, SIAM Journal on Computing 6(4), 1977
    locator: pp. 622 to 642
  - paper: doi:10.1007/BF00264563
    title: Kurt Mehlhorn, Nearly optimal binary search trees, Acta Informatica 5(4), 1975
    locator: pp. 287 to 295
---

The optimal binary search tree problem asks for a [binary search tree](/binary-search-tree/) over fixed sorted keys that minimizes the [expected search cost](/expected-search-cost-bst/), when the probability of each search is known in advance. Searches can hit a key or fall into one of the gaps between keys, and each has its own probability. Knuth solved the problem in 1971 in $O(n^2)$ time with an [interval DP](/interval-dp/) and a monotonicity property of the optimal roots. When only the gaps have weight, the problem is the optimal alphabetic tree problem, which the [Hu-Tucker](/hu-tucker-algorithm/) and [Garsia-Wachs](/garsia-wachs-algorithm/) algorithms solve in $O(n \log n)$ time.

## In plain words

A search tree for a dictionary is fast when the words you look up most often sit near the top. A balanced tree treats every word the same, so it is not the best tree when some words are far more common than others.

You know in advance how often each word is searched, and how often a search is for a word that is not there, between two given words. You want the tree that makes the average search as short as possible. Putting the most common word at the root seems natural, but it can be a poor choice. The right method tries every word as the root of every range of words, from short ranges to long, and keeps the best. A clever observation about where the best roots can be makes this fast enough for large dictionaries.

## Definition

**Input.** Keys $k_1 < k_2 < \cdots < k_n$, probabilities $p_1, \ldots, p_n \ge 0$ and $q_0, q_1, \ldots, q_n \ge 0$ with $\sum_i p_i + \sum_i q_i = 1$. A search is for $k_i$ with probability $p_i$. With probability $q_i$ it is for a value strictly between $k_i$ and $k_{i+1}$; $q_0$ covers the values below $k_1$ and $q_n$ the values above $k_n$. Following CLRS, these gaps are written as *dummy keys* $d_0, \ldots, d_n$. Non-negative frequencies that do not sum to 1 work the same way, with all costs scaled by the total.

**Trees.** A binary search tree $T$ on the keys has $k_1, \ldots, k_n$ as its internal nodes, in symmetric order, and $d_0, \ldots, d_n$ as its leaves, in order. The search for $k_i$ visits the path from the root to $k_i$, and an unsuccessful search in gap $i$ ends at $d_i$.

**Cost.** With the root at depth 0, the expected number of nodes visited is
$$\mathbb{E}[T] = \sum_{i=1}^{n} \bigl(\mathrm{depth}_T(k_i) + 1\bigr)\, p_i + \sum_{i=0}^{n} \bigl(\mathrm{depth}_T(d_i) + 1\bigr)\, q_i .$$

**Output.** A tree $T^*$ with $\mathbb{E}[T^*] = \min_T \mathbb{E}[T]$ over the $C_n$ binary search trees with $n$ keys ([Catalan number](/catalan-numbers/)).

**The recurrence.** For $1 \le i \le n + 1$ and $i - 1 \le j \le n$, let $e[i, j]$ be the least expected cost of a tree on $k_i, \ldots, k_j$ with leaves $d_{i-1}, \ldots, d_j$, and let $w(i, j) = \sum_{l=i}^{j} p_l + \sum_{l=i-1}^{j} q_l$. Then $e[i, i-1] = q_{i-1}$ and, for $i \le j$,
$$e[i, j] = \min_{i \le r \le j} \bigl( e[i, r-1] + e[r+1, j] + w(i, j) \bigr).$$

*Proof.* A tree on $k_i, \ldots, k_j$ with $i \le j$ has some root $k_r$, a left subtree $L$ on $k_i, \ldots, k_{r-1}$ and a right subtree $R$ on $k_{r+1}, \ldots, k_j$. Every node of $L$ and $R$ is one level deeper in the whole tree than in its subtree. So the cost of the whole is $\mathbb{E}[L] + \mathbb{E}[R]$ plus one unit for every node of the range, which is $\mathbb{E}[L] + \mathbb{E}[R] + w(i, j)$, where the root contributes $p_r$ at depth 0. This is strictly increasing in $\mathbb{E}[L]$ and in $\mathbb{E}[R]$, and the two subtrees can be chosen independently. So, for a fixed root, the best tree uses optimal subtrees, and the best tree overall is the best over all roots. An empty range holds only $d_{i-1}$ at depth 0, with cost $q_{i-1}$. ∎

Let $\mathrm{root}[i, j]$ be an $r$ that achieves the minimum. The answer is $e[1, n]$, and the tree is rebuilt from the roots by [traceback](/traceback/).

## Variants

- **Successful searches only.** All $q_i = 0$. This is the form of many textbook versions; the recurrence is the same.
- **Optimal alphabetic trees.** All $p_i = 0$, so only the leaves have weight. The problem is then to find a binary tree with leaves $d_0, \ldots, d_n$ in a fixed left-to-right order that minimizes the weighted path length. It is the same as an optimal prefix code whose code words must keep the alphabetical order of the symbols. Without the order constraint this is [Huffman coding](/huffman-coding/).
- **Approximately optimal trees.** Build a near-optimal tree in less time, for example with a [weight-balanced](/weight-balanced-tree/) split.
- **Multiway trees.** Each node holds up to $m - 1$ keys, as in a B-tree. The interval DP extends to this case, at a higher cost.
- **Dynamic and online versions.** The access sequence is not known in advance. [Splay trees](/splay-tree/) are within a constant factor of the best static tree on every long enough sequence of successful searches (the static optimality theorem of Sleator and Tarjan); the [dynamic optimality conjecture](/dynamic-optimality-conjecture/) asks for more.

## Examples

**CLRS Section 14.5.** Five keys with
$p = (0.15, 0.10, 0.05, 0.10, 0.20)$ and $q = (0.05, 0.10, 0.05, 0.05, 0.05, 0.10)$.
The table $e[i, j]$ and the chosen roots, for $i \le j$:

| $e[i,j]$ / root | $j=1$ | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| $i=1$ | 0.45 / 1 | 0.90 / 1 | 1.25 / 2 | 1.75 / 2 | 2.75 / 2 |
| 2 | | 0.40 / 2 | 0.70 / 2 | 1.20 / 2 | 2.00 / 4 |
| 3 | | | 0.25 / 3 | 0.60 / 4 | 1.30 / 5 |
| 4 | | | | 0.30 / 4 | 0.90 / 5 |
| 5 | | | | | 0.50 / 5 |

The least expected cost is $e[1, 5] = 2.75$. The optimal tree has root $k_2$; its left child is $k_1$ with leaves $d_0$ and $d_1$; its right child is $k_5$, whose left child is $k_4$, whose left child is $k_3$. In this tree $k_3$ is at depth 3. The tree with root $k_2$, right child $k_4$, and $k_3$ and $k_5$ below $k_4$ looks more balanced but costs 2.80.

**The most likely key at the root is not optimal.** In the same instance, the rule "put the most probable key of the range at the root" picks $k_5$ (probability 0.20) for the whole range and gives a tree of cost 3.05, about 11 percent worse than the optimum. A rule that balances the weight of the two subtrees does better: Mehlhorn proves that it always produces nearly optimal trees.

**Alphabetic order costs something.** Take four leaves with weights $(1, 4, 4, 1)$ in this order and no key weights. The best alphabetic tree is the balanced one, with weighted path length $2 \cdot 10 = 20$. A Huffman tree joins the two leaves of weight 1 first and reaches 18, but it puts the two outer leaves next to each other, which breaks the order.

## Known algorithms

| algorithm | case | time | space |
|---|---|---|---|
| [interval DP](/optimal-bst-dynamic-programming/) (CLRS Section 14.5) | general | $\Theta(n^3)$ | $\Theta(n^2)$ |
| Knuth 1971, the DP with monotone roots | general | $\Theta(n^2)$ | $\Theta(n^2)$ |
| [Hu-Tucker](/hu-tucker-algorithm/) 1971 | only $q$ nonzero (alphabetic trees) | $O(n \log n)$ | $O(n)$ |
| [Garsia-Wachs](/garsia-wachs-algorithm/) 1977 | only $q$ nonzero | $O(n \log n)$ | $O(n)$ |
| Mehlhorn 1975, weight bisection | general, approximate | $O(n \log n)$ with prefix sums and a binary search for each split | $O(n)$ |

**Knuth's speed-up.** Knuth proved that the optimal roots can be chosen so that
$$\mathrm{root}[i, j-1] \le \mathrm{root}[i, j] \le \mathrm{root}[i+1, j] \qquad \text{for } i < j .$$
So the minimum for $e[i, j]$ needs only the candidates $r$ between these two bounds. For a fixed length $\ell = j - i + 1 \ge 2$, the work over all $i$ is $\sum_i \bigl(\mathrm{root}[i+1, i+\ell-1] - \mathrm{root}[i, i+\ell-2] + 1\bigr)$. The sum telescopes to at most $\mathrm{root}[n-\ell+2, n] - \mathrm{root}[1, \ell-1] + n \le 2n$. Summing over the $n$ lengths gives $O(n^2)$. In the example table the roots do satisfy the inequalities. The general form of this speed-up, based on the quadrangle inequality of the cost $w$, is the [Knuth optimization](/knuth-optimization/).

## Bounds

- **Upper bounds.** $O(n^2)$ time for the general problem (Knuth). $O(n \log n)$ time for alphabetic trees (Hu and Tucker; Garsia and Wachs).
- **Lower bound for any algorithm.** $\Omega(n)$ time to read the probabilities.
- **Bounds on the cost.** For alphabetic trees the leaves form a binary prefix code, so by the Kraft inequality the expected depth of a leaf is at least the [entropy](/shannon-entropy/) $H(q) = -\sum_i q_i \lg q_i$. For the general problem, Mehlhorn 1975 and Knuth, TAOCP Section 6.2.2, bound the optimal cost above and below in terms of the entropy of the distribution $(p, q)$, and show that weight-balanced trees come close to the upper bound.

## Reductions

- **To interval DP.** The problem is an instance of the split-point recurrence of [interval DP](/interval-dp/), the same shape as [matrix-chain multiplication](/matrix-chain-multiplication/). Its extra cost $w(i, j)$ does not depend on the root, is monotone in the interval, and satisfies the quadrangle inequality. This is what gives the $O(n^2)$ bound, which matrix chains lack.
- **Alphabetic trees and codes.** With $p = 0$ the problem is exactly the optimal alphabetic prefix code. Dropping the order constraint gives Huffman's problem, which is solved greedily in $O(n \log n)$ time.
- **Lower bounds for searching.** A comparison-based search procedure for a static set with known probabilities is a binary search tree, so its expected number of comparisons is bounded below by the optimum of this problem in the same comparison model.

## Applications

- **Static dictionaries.** Keyword tables of compilers, spelling lists and other sets that do not change, where search frequencies can be measured. TAOCP Section 6.2.2 uses the frequencies of common English words as its running example.
- **Alphabetic codes.** Codes in which the order of the code words matches the order of the symbols, so that coded data can be compared and sorted without decoding.
- **Biased binary search.** Binary search over a sorted array where some answers are more likely. The probe positions form a search tree, and the optimal tree gives the best probe order.
- **Teaching.** With [matrix-chain multiplication](/matrix-chain-multiplication/), the standard example of interval dynamic programming and of a speed-up from monotone choices.

## References
