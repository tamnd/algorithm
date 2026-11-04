---
tag: FVKGF2
kind: theorem
slug: static-optimality-theorem
name: Static optimality theorem
aliases:
- static optimality of splay trees
area: data-structures/search-trees
level: advanced
summary: Splay tree cost on an access sequence is within a constant factor of the best static BST for that sequence.
prereqs: [splay-tree, splaying, expected-search-cost-bst, shannon-entropy]
see_also: [optimal-binary-search-tree, optimal-bst-dynamic-programming, working-set-theorem, dynamic-optimality-conjecture, potential-method, huffman-coding, move-to-front, tango-tree]
sources:
  - paper: doi:10.1145/3828.3835
    title: Daniel D. Sleator and Robert E. Tarjan, Self-adjusting binary search trees, Journal of the ACM 32(3), 1985
    locator: Section 2, Lemma 1 (Access Lemma) and Theorem 2 (Static Optimality Theorem)
  - paper: doi:10.1007/BF00264289
    title: Donald E. Knuth, Optimum binary search trees, Acta Informatica 1(1), 1971
    locator: pages 14 to 25
---

The static optimality theorem of Sleator and Tarjan (1985, Theorem 2) says that a [splay tree](/splay-tree/) serves each sequence of accesses at a total cost within a constant factor of the best static [binary search tree](/binary-search-tree/) for that sequence, the [optimal BST](/optimal-binary-search-tree/) built for the exact access frequencies. The splay tree is not told the frequencies, and it never stores them. The bound is $O(m + \sum_i q(i) \lg(m/q(i)))$, which is $m$ times the [entropy](/shannon-entropy/) of the access distribution plus $O(m)$.

## Statement

Let a splay tree hold $n$ keys, in any initial shape, and let $s = (i_1, \ldots, i_m)$ be a sequence of $m$ accesses (successful searches, each followed by a splay). Let $q(i)$ be the number of accesses to key $i$, and assume $q(i) \ge 1$ for each key. The cost of an access is the number of nodes on its search path, $d + 1$ for a node at depth $d$.

**Theorem.**

1. The total cost of the sequence in the splay tree is at most
$$2m + 4 \sum_{i=1}^{n} q(i) \lg \frac{m}{q(i)}.$$
2. Let $\mathrm{OPT}(s)$ be the least total cost of $s$ in a static BST on the $n$ keys, that is $\min_T \sum_i q(i)(\mathrm{depth}_T(i) + 1)$. Then
$$\mathrm{OPT}(s) \ge \max\!\left(m,\ \frac{1}{\lg 3} \sum_{i=1}^{n} q(i) \lg \frac{m}{q(i)}\right),$$
and so the splay tree costs at most $(2 + 4 \lg 3)\,\mathrm{OPT}(s) < 8.34\,\mathrm{OPT}(s)$.

Sleator and Tarjan state part 1 as $O(m + \sum_i q(i) \lg(m/q(i)))$; the constants here follow from their Access Lemma.

## In plain words

Suppose you knew in advance how often each key would be asked for. You could then build the best possible fixed search tree for those numbers, with the popular keys near the top. A splay tree is not told any of this. It just moves each key it finds to the top.

The theorem says that the splay tree does about as well anyway: its total work is never more than a fixed multiple of the work of that best fixed tree. The popular keys stay near the top on their own, because they are moved there so often.

## Proof

**The Access Lemma** (Sleator and Tarjan, Lemma 1; proved in [the complexity proof of splaying](/splaying/proofs/complexity.md)). Give each node $i$ a fixed weight $w(i) > 0$, let $s(x)$ be the total weight in the subtree of $x$, $r(x) = \lg s(x)$, and $\Phi = \sum_x r(x)$. Then the number of rotations of a splay of $x$ in a tree with root $t$, or 1 if there are none, plus the change of $\Phi$, is at most $3(r(t) - r(x)) + 1$.

**Part 1.** Choose $w(i) = q(i)/m$. The total weight is $W = 1$, so $r(t) = 0$ for the root $t$, and $r(x) \ge \lg w(x)$ for each $x$. So an access to key $i$ has amortized cost at most
$$3\,(0 - \lg (q(i)/m)) + 1 = 3 \lg \frac{m}{q(i)} + 1.$$
Summing over the $m$ accesses, key $i$ appears $q(i)$ times:
$$\sum_{j=1}^{m} \max(\mathrm{rot}_j, 1) \le \sum_{i=1}^{n} q(i)\left(3 \lg \frac{m}{q(i)} + 1\right) + \Phi_0 - \Phi_m,$$
where $\mathrm{rot}_j$ is the number of rotations of access $j$. Each rank satisfies $\lg w(x) \le r(x) \le \lg W = 0$, so
$$\Phi_0 - \Phi_m \le 0 - \sum_{i} \lg w(i) = \sum_{i=1}^{n} \lg \frac{m}{q(i)} \le \sum_{i=1}^{n} q(i) \lg \frac{m}{q(i)},$$
using $q(i) \ge 1$ and $\lg(m/q(i)) \ge 0$. An access to a node at depth $d$ visits $d + 1$ nodes and makes $d$ rotations, so its cost is at most $\max(\mathrm{rot}_j, 1) + 1$. Adding $m$ for these extra ones, and $\sum_i q(i) = m$:
$$\text{total cost} \le m + m + 3 \sum_i q(i) \lg \frac{m}{q(i)} + \sum_i q(i) \lg \frac{m}{q(i)} = 2m + 4 \sum_i q(i) \lg \frac{m}{q(i)}.$$

**Part 2.** Each access visits at least one node, so $\mathrm{OPT}(s) \ge m$. For the second bound, fix a static BST $T$. Write the search for key $i$ as the word of the outcomes of its comparisons over the alphabet $\{<, >, =\}$: $\mathrm{depth}_T(i)$ letters from $\{<, >\}$ followed by one $=$. These $n$ words form a prefix-free code over 3 letters (a word ends at its only $=$, and two different keys have different paths), so by the Kraft inequality $\sum_i 3^{-(\mathrm{depth}_T(i) + 1)} \le 1$. By Gibbs' inequality, for the distribution $p_i = q(i)/m$,
$$\sum_i p_i (\mathrm{depth}_T(i) + 1) \lg 3 \ge \sum_i p_i \lg \frac{1}{p_i},$$
which multiplied by $m$ gives $\sum_i q(i)(\mathrm{depth}_T(i) + 1) \ge \frac{1}{\lg 3} \sum_i q(i) \lg \frac{m}{q(i)}$. This holds for each $T$, hence for the best one. Writing $E = \sum_i q(i) \lg(m/q(i))$, part 1 gives at most $2m + 4E \le 2\,\mathrm{OPT}(s) + 4 \lg 3\,\mathrm{OPT}(s)$. $\blacksquare$

## Consequences

- **No need to know the frequencies.** An [optimal BST](/optimal-binary-search-tree/) needs the counts $q(i)$ in advance and $\Theta(n^2)$ time with [Knuth's method](/optimal-bst-dynamic-programming/). A splay tree reaches the same cost up to a constant factor without them, and it also adapts if the frequencies drift.
- **Entropy bound.** With $p_i = q(i)/m$, the bound of part 1 is $2m + 4mH(p)$, where $H$ is the [Shannon entropy](/shannon-entropy/). A distribution concentrated on a few keys gives cost $O(1)$ per access, whatever $n$ is.
- **Balance.** With uniform frequencies, $H = \lg n$ and the bound is $O(m \log n)$, the balance theorem.
- **Example.** For 16 keys with access probabilities proportional to $1/(i + 1)$ and one random sequence of $m = 20000$ accesses from a shuffled initial tree, the splay tree visited 73826 nodes and the optimal static tree for the observed counts 59797, a ratio of about 1.23, well below the proven 8.34. The entropy of the counts was about 3.40 bits, so the lower bound $mH/\lg 3$ is about 42900.

## Tightness

- **The factor is constant, not 1.** The splay tree can cost more than the optimal static tree; for example, accessing the keys in a fixed random order over and over costs it more than a balanced tree, since each splay moves a key to the root that will not be needed again soon. The theorem bounds the ratio but does not make it close to 1.
- **The term $m$.** If one key is accessed almost always, the optimal static tree costs about $m$, and so does the splay tree up to the constant: the term $2m$ cannot be dropped.
- **Requiring $q(i) \ge 1$.** Keys that are never accessed contribute to $\Phi_0 - \Phi_m$ with weight 0, which the proof cannot handle. Sleator and Tarjan assume each key is accessed at least once; otherwise give each unused key a small weight and add $O(n \log n)$ to the bound.
- **Static versus dynamic.** The theorem compares with static trees only. Sequences such as accessing the keys in increasing order cost $\Theta(m \log n)$ in each static tree when all keys are equally frequent, but $O(m)$ in a splay tree (the sequential access theorem). Comparing with all dynamic BST algorithms is the open [dynamic optimality conjecture](/dynamic-optimality-conjecture/).

## History

Sleator and Tarjan proved the theorem in 1985 as Theorem 2 of the paper that introduced splay trees, by the choice of weights $q(i)/m$ in the Access Lemma. The lower bound on static trees by entropy goes back to the work on optimum search trees; Knuth (1971) gave the exact optimum by dynamic programming.

## References
