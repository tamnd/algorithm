---
tag: HZ8FQF
kind: concept
slug: expected-search-cost-bst
name: Expected search cost in a binary search tree
aliases:
- Expected search cost
- weighted path length
area: data-structures/search-trees
level: core
summary: The average cost of searching a binary search tree, weighting each key's depth by its search probability, which optimal trees minimize.
prereqs: [binary-search-tree, bst-search, expected-value]
see_also: [optimal-binary-search-tree, optimal-bst-dynamic-programming, random-bst-expected-depth, static-optimality-theorem, shannon-entropy, huffman-coding, hu-tucker-algorithm, splay-tree]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 14.5 (Optimal binary search trees), the expected cost of a search with dummy keys
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.2 (Binary tree searching), weighted path length and optimum binary search trees
  - paper: doi:10.1007/BF00264289
    title: Donald E. Knuth, Optimum binary search trees, Acta Informatica 1(1), 1971
    locator: pages 14 to 25
  - paper: doi:10.1007/bf00264563
    title: Kurt Mehlhorn, Nearly optimal binary search trees, Acta Informatica 5, 1975
    locator: the whole paper
---

The expected search cost of a [binary search tree](/binary-search-tree/) is the average number of nodes that a [search](/bst-search/) visits when the query keys follow a known probability distribution. Each key $k_i$ is searched with probability $p_i$, and each gap $d_j$ between consecutive keys with probability $q_j$, so the cost is a sum of depths weighted by these probabilities. An [optimal binary search tree](/optimal-binary-search-tree/) minimizes this sum, and the [Shannon entropy](/shannon-entropy/) of the distribution bounds it from below. With equal weights the best tree is a balanced one, but with skewed weights the best tree puts frequent keys near the root even if the tree is then unbalanced.

## In plain words

Some words in a dictionary are looked up all the time and some almost never. If you build a search tree, you can choose which words go near the top. A search for a word near the top is fast, and a search for a word deep down is slow.

The expected search cost is the average time of a search, where each word counts as often as people look it up. A tree that is perfectly balanced is not always the best one: if one word is asked for half of the time, it should be at the top, even if that makes the rest of the tree a little lopsided. The best tree makes this average as small as possible.

## The idea

**The setting (CLRS, Section 14.5).** There are $n$ keys $k_1 < k_2 < \cdots < k_n$ and $n + 1$ gaps $d_0, d_1, \ldots, d_n$, where $d_j$ stands for all queries strictly between $k_j$ and $k_{j+1}$ (with $k_0 = -\infty$ and $k_{n+1} = +\infty$). A query is $k_i$ with probability $p_i$ and falls in $d_j$ with probability $q_j$, and
$$\sum_{i=1}^{n} p_i + \sum_{j=0}^{n} q_j = 1.$$
In a BST $T$ on the keys, add each gap as a leaf (a dummy key) at the empty child where a search for it ends. Then a search for $k_i$ visits $\mathrm{depth}_T(k_i) + 1$ nodes, and a search in the gap $d_j$ visits $\mathrm{depth}_T(d_j)$ real nodes. CLRS counts the dummy leaf as visited too, which gives
$$\mathbb{E}[\text{cost}_T] = \sum_{i=1}^{n} p_i\,(\mathrm{depth}_T(k_i) + 1) + \sum_{j=0}^{n} q_j\,(\mathrm{depth}_T(d_j) + 1) = 1 + \sum_{i} p_i\,\mathrm{depth}_T(k_i) + \sum_{j} q_j\,\mathrm{depth}_T(d_j).$$
Knuth uses weights in place of probabilities and calls $\sum p_i (\mathrm{depth}(k_i) + 1) + \sum q_j\,\mathrm{depth}(d_j)$ the weighted path length; this is the exact number of three-way comparisons. The two forms differ by the constant $\sum q_j$, so they have the same optimal trees.

**The recursion.** Let $w(i, j) = \sum_{l=i}^{j} p_l + \sum_{l=i-1}^{j} q_l$ be the weight of a subtree with keys $k_i, \ldots, k_j$ and its gaps. If such a subtree has root $k_r$, each node in it is one level deeper in the whole tree than in its own subtree. So, with $e(i, j)$ the cost of the subtree in the CLRS form,
$$e(i, j) = e(i, r - 1) + e(r + 1, j) + w(i, j), \qquad e(i, i-1) = q_{i-1}.$$
The cost of a tree is the cost of its two subtrees plus the weight of the tree. This is why the optimal tree has [optimal substructure](/optimal-substructure/), and it gives the [dynamic program](/optimal-bst-dynamic-programming/) for the optimal tree.

**Bounds by entropy.** Let $H = -\sum p_i \lg p_i - \sum q_j \lg q_j$ be the entropy of the $2n + 1$ outcomes. A search is a path in a tree where each node has three outcomes ($<$, $=$, $>$), so the sequences of outcomes form a prefix code over three letters. By the source coding theorem the expected number of comparisons is at least $H / \lg 3$. Mehlhorn (1975) showed that a tree built by choosing as root the key that splits the weight most evenly has cost $H + O(1)$, so the optimal cost lies between $H/\lg 3$ and $H + O(1)$.

**Uniform weights.** If $p_i = 1/n$ and $q_j = 0$, the cost is $1 + (\text{total depth})/n$, which is smallest for a tree of minimum height with all levels but the last full; the cost is then about $\lg n$. For a [random BST](/random-binary-search-tree/) it is $2(1 + 1/n)H_n - 3 \approx 1.39 \lg n$.

**Unknown weights.** If the weights are not known in advance, a [splay tree](/splay-tree/) adapts to them: by the [static optimality theorem](/static-optimality-theorem/), its total cost on a sequence of accesses is within a constant factor of the cost of the best static tree for the access frequencies of that sequence.

## Examples

**CLRS weights.** Take $n = 5$ with $p = (0.15, 0.10, 0.05, 0.10, 0.20)$ and $q = (0.05, 0.10, 0.05, 0.05, 0.05, 0.10)$.

The balanced tree with root $k_3$, left child $k_2$ (with left child $k_1$), and right child $k_4$ (with right child $k_5$) has key depths $(2, 1, 0, 1, 2)$ and gap depths $(3, 3, 2, 2, 3, 3)$, so its cost is
$$(0.15 \cdot 3 + 0.10 \cdot 2 + 0.05 \cdot 1 + 0.10 \cdot 2 + 0.20 \cdot 3) + (0.05 \cdot 4 + 0.10 \cdot 4 + 0.05 \cdot 3 + 0.05 \cdot 3 + 0.05 \cdot 4 + 0.10 \cdot 4) = 1.50 + 1.50 = 3.00.$$

The optimal tree has root $k_2$, children $k_1$ and $k_5$, then $k_4$ as the left child of $k_5$ and $k_3$ as the left child of $k_4$. Its key depths are $(1, 0, 3, 2, 1)$ and its cost is $2.75$, lower than the balanced tree although its height is 3 instead of 2. The entropy of the 11 outcomes is $H \approx 3.28$ bits; the expected number of comparisons of the optimal tree is $2.75 - \sum q_j = 2.35$, above the bound $H / \lg 3 \approx 2.07$.

**One heavy key.** Let $p = (0.01, 0.01, 0.96, 0.01, 0.01)$ and $q = 0$. A tree with $k_3$ at the root and the other keys below costs at most $0.96 \cdot 1 + 0.04 \cdot 3 = 1.08$, while a chain $k_1 \to k_2 \to \cdots \to k_5$ costs $0.01 + 0.02 + 0.96 \cdot 3 + 0.04 + 0.05 = 3.00$.

**Only gaps.** If all $p_i = 0$, every search is a miss, and the problem is to build the best alphabetic code for the gaps: the order of the leaves is fixed. This is the problem of the [Hu-Tucker algorithm](/hu-tucker-algorithm/) and the [Garsia-Wachs algorithm](/garsia-wachs-algorithm/), which solve it in $O(n \log n)$ time. Without the order constraint it would be [Huffman coding](/huffman-coding/).

## Where it is used

- **Optimal static trees.** The [optimal binary search tree](/optimal-binary-search-tree/) problem minimizes it; the [dynamic program](/optimal-bst-dynamic-programming/) solves it in $O(n^3)$ time, and Knuth's speed-up ([Knuth optimization](/knuth-optimization/)) in $O(n^2)$.
- **Average-case analysis.** The cost of BST search on random input, see [expected depth in random BSTs](/random-bst-expected-depth/).
- **Self-adjusting trees.** The static optimality of [splay trees](/splay-tree/) compares their cost with the best expected cost for the observed frequencies.
- **Compilers and lexers.** Keyword tables with known frequencies, where a few keywords are far more common than the rest.
- **Coding theory.** With only gap weights it is the cost of an alphabetic prefix code, and the entropy bound is the source coding bound.

## References
