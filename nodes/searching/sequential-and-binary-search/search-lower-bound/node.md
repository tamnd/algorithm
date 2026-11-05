---
tag: GEM4W7
kind: theorem
slug: search-lower-bound
name: Lower bound for comparison-based search
aliases:
- information-theoretic search bound
area: searching/sequential-and-binary-search
level: advanced
summary: Any comparison-based search of a sorted array of n keys needs ceil(log2(n+1)) comparisons in the worst case, so binary search is optimal.
prereqs: [search-decision-tree, binary-search]
see_also: [sorted-search-lower-bound, information-theoretic-bound, kraft-inequality, yao-minimax-principle, optimal-binary-search-tree, search-in-sorted-array, huffman-coding, randomized-algorithm]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.1, Searching an ordered table (comparison trees, and binary search as the tree of least worst-case and average cost)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.3.4.5, Path length (the minimum external path length of a binary tree with a given number of leaves)
---

The lower bound for comparison-based search says that every algorithm that searches a sorted array of $n$ keys by comparing the search key with the keys needs at least $\lceil \lg(n+1) \rceil$ comparisons on some input, and that this holds in a stronger form for the average and for randomized algorithms: over a uniform random gap between the keys, even the best algorithm needs on average at least $\lg(n+1)$ comparisons, and exactly $\lfloor \lg(n+1) \rfloor + 2\bigl(1 - 2^{\lfloor \lg(n+1) \rfloor}/(n+1)\bigr)$ in the best case. [Binary search](/binary-search/), in its lower bound form, meets the first two bounds and comes within one comparison of the third. The argument is the [information-theoretic bound](/information-theoretic-bound/) in the [search decision tree](/search-decision-tree/) model: an absent key must be told apart from its two neighbors, so the $n + 1$ gaps reach different leaves along two-way branches, and a binary tree with $N$ leaves has height at least $\lg N$ and average leaf depth at least $\lg N$. The worst-case part alone, with its matching upper bound, is also given on the page [sorted search lower bound](/sorted-search-lower-bound/).

## Statement

Let $A[1] < \cdots < A[n]$ be sorted distinct keys, $n \ge 1$, and let the algorithm compare $x$ with keys $A[i]$, each comparison having the answers $<$, $=$, $>$. The algorithm must report an index of $x$ or that $x$ is absent. For $g = 0, \ldots, n$, the *gap* $g$ is the set of keys $x$ with $A[g] < x < A[g+1]$, where $A[0] = -\infty$ and $A[n+1] = +\infty$. Let $N = n + 1$ and $q = \lfloor \lg N \rfloor$.

**Theorem.**

1. **Worst case.** Every deterministic algorithm makes at least $\lceil \lg N \rceil$ comparisons on some key in a gap.
2. **Average case.** For a deterministic algorithm, let $d_g$ be the number of comparisons on a key in gap $g$ (on the array $A[i] = 2i$ and the key $2g + 1$). Then
$$ \frac{1}{N} \sum_{g=0}^{n} d_g \;\ge\; \frac{E(N)}{N} \;\ge\; \lg N, \qquad E(N) = Nq + 2(N - 2^q). $$
3. **Randomized.** Every randomized algorithm that is always correct has, on some gap, expected cost at least $\lg N$.

The lower bound search loop, which finds the first index with $A[i] \ge x$ and then tests it for equality, makes $q$ or $q + 1$ order comparisons, uses $\lceil \lg N \rceil$ in the worst case, and has average exactly $E(N)/N$ over the gaps. So parts 1 and 2 are tight up to the final equality test, part 1 is met exactly by the three-way binary search, and part 3 is within less than one comparison of the deterministic cost.

## In plain words

Every comparison of the key with an item gives one of two answers when the key is not in the list: smaller or larger. A search is like a game of "higher or lower". There are $n + 1$ places where a missing key can fall, and the search must tell them all apart, since each place is the right answer for some key.

Each answer at best halves the places that are left. So in the worst case you need as many answers as it takes to halve $n + 1$ down to one. This is also true on average: you cannot be lucky on some places without being unlucky on others. Even tossing coins to choose where to look does not help, because on average over the places no fixed plan beats halving.

## Proof

Fix $n$ and use $A[i] = 2i$, with the key $x_g = 2g + 1$ for gap $g$. A deterministic algorithm for this $n$ is a ternary comparison tree.

**Step 1. Gap keys must be compared with their neighbors.** Let $g < n$. Suppose the run on $x_g$ never compares $x$ with $A[g+1] = 2g + 2$. For every $j \ne g + 1$, the keys $x_g$ and $2g + 2$ compare the same way with $A[j]$: both are larger for $j \le g$ and both smaller for $j \ge g + 2$. So the run on $x = 2g + 2$ follows the same path and reports "absent", which is wrong. So the run on $x_g$ compares with $A[g+1]$, and by the same argument with $A[g]$ when $g > 0$.

**Step 2. The gap keys reach different leaves.** Let $g < g'$. The run on $x_g$ compares with $A[g+1]$ and gets "$<$", while $x_{g'} > A[g+1]$. If the two runs followed the same path, this comparison would give the same answer to both. So the paths split, and the leaves differ.

**Step 3. The paths form a prefix-free binary code.** On the runs of the gap keys every answer is "$<$" or "$>$", since no gap key equals a key. Write the path of $x_g$ as a string $w_g$ over $\{<, >\}$ of length $d_g$. By step 2, no $w_g$ is a prefix of another: two runs agree until they split, and a run that ends at a leaf does not continue. So $\{w_0, \ldots, w_n\}$ is a set of $N$ distinct binary strings, none a prefix of another, with lengths $d_g$.

**Step 4. Kraft's inequality.** For a prefix-free set of binary strings with lengths $d_g$, $\sum_g 2^{-d_g} \le 1$. Let $L = \max_g d_g$. Each $w_g$ is a prefix of exactly $2^{L - d_g}$ strings of length $L$, and these sets are disjoint because no $w_g$ is a prefix of another. There are $2^L$ strings of length $L$, so $\sum_g 2^{L - d_g} \le 2^L$. This is the [Kraft inequality](/kraft-inequality/).

**Part 1.** With $h = \max_g d_g$, step 4 gives $N 2^{-h} \le \sum_g 2^{-d_g} \le 1$, so $h \ge \lg N$, and $h \ge \lceil \lg N \rceil$ since $h$ is an integer.

**Part 2, the bound $\lg N$.** The function $t \mapsto 2^{-t}$ is convex, so by Jensen's inequality, with $\bar d = \frac{1}{N} \sum_g d_g$,
$$ 2^{-\bar d} \le \frac{1}{N} \sum_g 2^{-d_g} \le \frac{1}{N}, $$
and so $\bar d \ge \lg N$.

**Part 2, the exact bound $E(N)$.** Among all prefix-free sets of $N$ binary strings, take one with the least total length $S = \sum_g d_g$. Build its trie: the binary tree whose root-to-leaf paths are the strings. If some internal node had one child, removing it would shorten every string below it and keep the set prefix-free, so in a minimal set the trie is full: every internal node has two children, and the $N$ strings are its leaves. Let $D$ be the largest depth. The two leaves at depth $D$ under one parent exist, since a deepest leaf has a sibling and in a full tree that sibling is a leaf too. Suppose a leaf $a$ has depth $d_a \le D - 2$. Remove the two deepest siblings, so that their parent becomes a leaf at depth $D - 1$, and give $a$ two children, which become leaves at depth $d_a + 1$. The number of leaves stays $N$, and the total depth changes by $-2D + (D - 1) - d_a + 2(d_a + 1) = d_a + 1 - D \le -1$, which contradicts minimality. So all leaves of a minimal trie have depth $D - 1$ or $D$. Let $u$ leaves have depth $D - 1$ and $v$ depth $D$. In a full binary tree the Kraft sum is exactly 1, so $u 2^{-(D-1)} + v 2^{-D} = 1$, that is $2u + v = 2^D$, with $u + v = N$. Hence $u = 2^D - N$ and $v = 2N - 2^D$. Since $u \ge 0$ and $v \ge 1$, $2^{D-1} < N \le 2^D$. If $N = 2^q$ is a power of 2, then $D = q$, all leaves have depth $q$, and $S = Nq = E(N)$. Otherwise $D = q + 1$ and $S = (D - 1)N + v = Nq + 2N - 2^{q+1} = E(N)$. So every algorithm has $\sum_g d_g \ge E(N)$.

**Part 3.** A randomized algorithm that is always correct is a probability distribution over deterministic comparison trees for $n$. Let $C(T, g)$ be the cost of tree $T$ on gap $g$. For every $T$, part 2 gives $\frac{1}{N} \sum_g C(T, g) \ge \lg N$. Averaging over the random choice of $T$,
$$ \frac{1}{N} \sum_g \mathbb{E}_T[C(T, g)] = \mathbb{E}_T\Bigl[\frac{1}{N} \sum_g C(T, g)\Bigr] \ge \lg N, $$
so some gap $g$ has $\mathbb{E}_T[C(T, g)] \ge \lg N$. This is the easy direction of [Yao's principle](/yao-minimax-principle/).

**Tightness of the loop.** The lower bound loop on $N - 1 = n$ items is a full binary trie over the $N$ answers $\ell \in \{0, \ldots, n\}$ whose leaves have depths $\lfloor \lg N \rfloor$ or $\lceil \lg N \rceil$ (shown on [lower and upper bound search](/lower-and-upper-bound-search/)), so by the computation above its total depth is $E(N)$. $\blacksquare$

## Consequences

- **Binary search is optimal.** It meets the worst-case and the average bounds, and the plain three-way binary search uses $\lceil \lg N \rceil$ comparisons, exactly part 1.
- **Randomness saves less than one comparison.** The randomized bound $\lg N$ and the deterministic $\lceil \lg N \rceil$ differ by less than 1.
- **Non-uniform gaps.** If gap $g$ has probability $p_g$, the same proof with Gibbs' inequality instead of Jensen gives an average of at least the [entropy](/shannon-entropy/) $H(p) = \sum_g p_g \lg(1/p_g)$, and an [optimal binary search tree](/optimal-binary-search-tree/) for the weights is within a small additive term of it.
- **Other searches.** [Interpolation search](/interpolation-search/) beats $\lg N$ on some inputs only because it uses arithmetic on keys, outside the model. [Exponential search](/exponential-search/) and [unbounded search](/unbounded-search/) pay more than $\lg N$, since $n$ is not known.

The table compares the bounds with the lower bound loop, computed by a script:

| $n$ | 1 | 2 | 4 | 10 | 100 | 1000 | $10^6$ |
|---|---|---|---|---|---|---|---|
| $\lg(n+1)$ | 1.000 | 1.585 | 2.322 | 3.459 | 6.658 | 9.967 | 19.932 |
| $E(N)/N$ | 1.000 | 1.667 | 2.400 | 3.545 | 6.733 | 9.977 | 19.951 |
| average of the loop | 1.000 | 1.667 | 2.400 | 3.545 | 6.733 | 9.977 | |
| $\lceil \lg(n+1) \rceil$ | 1 | 2 | 3 | 4 | 7 | 10 | 20 |

## Tightness

Parts 1 and 2 are exact. Part 1 is met by three-way binary search for every $n$. Part 2 is met by every binary search whose gap leaves lie on two adjacent levels, and the gap between $\lg N$ and $E(N)/N$ is at most about $0.086$, with equality exactly when $N$ is a power of 2. Part 3 is met by a deterministic algorithm when $N$ is a power of 2. Otherwise the argument of part 3 with $E(N)/N$ in place of $\lg N$ gives the slightly stronger bound $E(N)/N$ for randomized algorithms.

The bound needs the comparison model. Keys that are integers in a known range allow other methods: with $w$-bit keys, the [predecessor problem](/predecessor-problem/) can be solved in $O(\log w)$ time by the van Emde Boas structure, which is less than $\lg n$ when $n$ is large compared to $w$.

## History

Comparison trees as a model of search, and the fact that binary search gives the trees of least height and least external path length, are classical and are treated by Knuth in Section 6.2.1 of Volume 3, with the minimum external path length in Section 2.3.4.5 of Volume 1. The prefix-free code view connects the bound to Kraft's inequality from coding theory, and the extension to non-uniform gaps to the theory of optimal binary search trees and Huffman codes.

## References
