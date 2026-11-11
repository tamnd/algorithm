---
title: Correctness of Tunstall coding
proves: [correctness]
status: full
---

We prove that the Tunstall dictionary parses every string in exactly one way, that the expected parse length is the sum of the probabilities of the inner nodes, that no complete dictionary of the same size has a longer expected parse, and that the rate lies between $H$ and a bound that tends to $H$.

**Setup.** The source emits independent symbols from an alphabet of size $\sigma \ge 2$, with probabilities $p_1, \ldots, p_\sigma > 0$. The probability of a word $x = s_1 \cdots s_k$ is $P(x) = p_{s_1} \cdots p_{s_k}$, and $P$ of the empty word is 1. View the words as nodes of the infinite $\sigma$-ary tree. A dictionary $D$ is *proper* if no word in it is a prefix of another, and *complete* if every inner node (every proper prefix of a word of $D$) has all $\sigma$ children in $D$ or among the inner nodes. Then $D$ is the set of leaves of a finite full $\sigma$-ary tree $T$. A tree with $k$ inner nodes has $M = 1 + k(\sigma - 1)$ leaves. Write $H = \sum_s p_s \log_2 (1/p_s)$.

**Lemma 1 (the dictionary).** The algorithm returns a complete proper dictionary with $M$ words, where $2^B - \sigma + 1 < M \le 2^B$.

*Proof.* It starts with the $\sigma$ one-symbol words, the leaves of the tree whose only inner node is the root. Each split replaces a leaf $x$ by its $\sigma$ children, so $x$ becomes an inner node with all its children present, and the leaves stay the leaves of a full tree. A split adds $\sigma - 1$ words and is made only when the result has at most $2^B$ words; the loop stops when one more split would exceed $2^B$, that is, when $M + \sigma - 1 > 2^B$. $\square$

**Lemma 2 (unique parse).** Let $D$ be complete and proper. Every infinite string has exactly one prefix in $D$, and every finite string $u$ either has exactly one prefix in $D$ or is itself an inner node.

*Proof.* Walk down $T$ from the root along the symbols of the string. At an inner node the next symbol leads to a child, which is an inner node or a leaf, since $D$ is complete. The walk meets a leaf after at most the depth of $T$ steps, unless a finite string ends first at an inner node. Two prefixes of the string in $D$ would be prefixes of each other, which properness forbids. $\square$

So the encoder, which reads symbols until the read part is a word of $D$, outputs that word's index and starts again, cuts every string into dictionary words in the only possible way, followed by at most one inner node at the end. The encoder extends that last piece with the symbol 0 until it is a leaf, which takes at most the depth of $T$ steps by the same walk. The decoder replaces each index by its word and keeps the first $n$ symbols, where $n$ is the length of the message. This is the original message, since the concatenation of the words is the message followed by the padding.

**Lemma 3 (expected parse length).** For a complete proper dictionary, the expected length of the first word of the parse is $E[L] = \sum_{x \in D} P(x) |x| = \sum_{u \text{ inner}} P(u)$.

*Proof.* By Lemma 2 the first word of the parse is the word $x \in D$ that is a prefix of the source string, which happens with probability $P(x)$, and these probabilities sum to 1. A leaf $x$ of depth $|x|$ has exactly $|x|$ inner nodes as proper prefixes, so $\sum_x P(x) |x| = \sum_u \sum_{x \in D,\ u \text{ prefix of } x} P(x)$. The leaves below an inner node $u$ form a complete proper dictionary for the strings that start with $u$, so the inner sum is $P(u)$. $\square$

Since the symbols are independent, the source after each parsed word starts afresh, and the words of the parse are independent and have the same distribution. So $E[L]$ is also the mean number of source symbols per codeword in a long message.

**Lemma 4 (inner nodes outweigh leaves).** At every step of the algorithm, every inner node is at least as probable as every leaf.

*Proof.* At the start the only inner node is the root, with probability 1. Suppose it holds before a split of the leaf $x$, which is a most probable leaf. After the split, $x$ is an inner node with $P(x)$ at least the probability of every other leaf, and its children have probabilities $P(x) p_s \le P(x)$, which is at most the probability of each old inner node, by the hypothesis. $\square$

**Theorem 1 (optimality).** Among all complete proper dictionaries with $M$ words, the Tunstall dictionary has the largest $E[L]$.

*Proof.* A complete proper dictionary with $M$ words is the leaf set of a full tree with $k = (M - 1)/(\sigma - 1)$ inner nodes. Its inner nodes form a set $I$ of $k$ nodes that contains the root and is closed under taking prefixes, and by Lemma 3, $E[L] = \sum_{u \in I} P(u)$. Let $S_k$ be the sum of the $k$ largest values of $P$ over all nodes of the infinite tree, counted with multiplicity; then every such $E[L]$ is at most $S_k$. Now take the run of the algorithm. Before each split the inner set $I$ is prefix-closed, and every node $v \notin I$ has a prefix that is a leaf of the current tree: the longest prefix of $v$ in $I$ has a child on the path to $v$, and that child is a leaf. Since $P$ does not grow along a path, the leaf $x$ that the algorithm splits has the largest probability among all nodes outside $I$. So the algorithm adds, in turn, a most probable node among those not yet chosen, and after $k$ splits $\sum_{u \in I} P(u) = S_k$. $\square$

**Lemma 5 (word entropy).** For a complete proper dictionary, the entropy of the first parsed word is $H(W) = \sum_{x \in D} P(x) \log_2 (1/P(x)) = H \cdot E[L]$.

*Proof.* By induction on the number of splits. For $D$ equal to the alphabet, both sides are $H$. Splitting a leaf $x$ with $P(x) = q$ replaces the term $q \log_2 (1/q)$ by $\sum_s q p_s \log_2 (1/(q p_s)) = q \log_2 (1/q) + q H$, so $H(W)$ grows by $qH$. By Lemma 3, $E[L]$ grows by $q$, the probability of the new inner node. $\square$

**Theorem 2 (rate).** Let $p_{\min} = \min_s p_s$. The rate $R = B / E[L]$ bits per source symbol of the Tunstall code satisfies
$$H \le R \le \frac{H B}{\log_2 M - \log_2 (1/p_{\min})}$$
when the denominator is positive. Since $M > 2^B - \sigma + 1$, the right side tends to $H$ as $B$ grows.

*Proof.* A random variable with $M$ values has entropy at most $\log_2 M$, so by Lemma 5, $H \cdot E[L] = H(W) \le \log_2 M \le B$, which gives $R \ge H$. For the upper bound, let $q$ be the smallest probability of an inner node. By Lemma 4 every leaf has $P(x) \le q$, so $H(W) \ge \sum_x P(x) \log_2 (1/q) = \log_2 (1/q)$. Every leaf $x = u s$ has an inner parent $u$ with $P(u) \ge q$, so $P(x) \ge p_{\min} q$, and summing over the $M$ leaves gives $1 \ge M p_{\min} q$. So $H(W) \ge \log_2 (M p_{\min})$, and $R = B H / H(W)$ gives the bound. When $2^{B-1} \ge \sigma - 2$, we have $M \ge 2^{B-1}$, and the bound is at most $H B / (B - 1 - \log_2 (1/p_{\min}))$, which tends to $H$. $\square$

The difference between the rate and $H$ thus falls like $1/B$. The implementation's tests check Lemmas 1 to 4, Theorem 1 by search over all complete dictionaries of small size, and the two bounds of Theorem 2.
