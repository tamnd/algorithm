---
title: The span chart decoder returns a binary labeled tree of maximum score, and loss-augmented decoding maximizes score plus Hamming loss
proves: [correctness, termination]
status: full
---

We use the pseudocode CHART-PARSE of the page. The input is a sentence length $n \ge 1$, a finite label set $\{0, 1, \ldots, L - 1\}$ with $L \ge 1$, where 0 is the empty label $\varnothing$, real label scores $s_{\text{label}}(i, j, \ell)$ and real span scores $s_{\text{span}}(i, j)$ for every fencepost span $(i, j)$ with $0 \le i < j \le n$. The span $(i, j)$ covers the words $i + 1$ to $j$. The scores are arbitrary reals; nothing is assumed about their sign.

## Definitions

A binary bracketing of $(i, j)$ is a set $B$ of spans defined by induction: for $j = i + 1$ it is $\{(i, j)\}$, and for $j > i + 1$ it is $\{(i, j)\} \cup B_1 \cup B_2$ for some split $k$ with $i < k < j$, a bracketing $B_1$ of $(i, k)$ and a bracketing $B_2$ of $(k, j)$. Since $B_1$ and $B_2$ contain only spans inside $(i, k)$ and $(k, j)$, the union is disjoint and $(i, j)$ is in neither part, and the split $k$ is determined by $B$, because $(i, k)$ is the longest span of $B$ other than $(i, j)$ that starts at $i$. A bracketing of $(i, j)$ has exactly $2(j - i) - 1$ spans, by induction.

A labeled tree $T$ over $(i, j)$ is a bracketing $B$ with a label $\ell(u) \in \{0, \ldots, L - 1\}$ for each span $u \in B$. Its score is

$$s(T) = \sum_{u \in B} \big[ s_{\text{label}}(u, \ell(u)) + s_{\text{span}}(u) \big].$$

Let $\mathrm{opt}(i, j)$ be the largest score of a labeled tree over $(i, j)$. The maximum exists because there are finitely many labeled trees.

## Lemma 1: the labels separate from the bracketing

For every span $u$, let $m(u) = \max_\ell s_{\text{label}}(u, \ell) + s_{\text{span}}(u)$. Then

$$\mathrm{opt}(i, j) = \max_{B} \sum_{u \in B} m(u),$$

where $B$ ranges over the bracketings of $(i, j)$, and a labeled tree has score $\mathrm{opt}(i, j)$ exactly when its bracketing attains this maximum and every span has a label of largest $s_{\text{label}}$.

*Proof.* For a fixed bracketing $B$, the score is a sum of terms, one per span, and the term of $u$ depends only on $\ell(u)$. The labels are chosen independently, so the sum is largest when each term is, and its largest value is $\sum_{u \in B} m(u)$. Taking the maximum over $B$ gives the claim. $\square$

## Lemma 2: the recurrence

$\mathrm{opt}(i, i + 1) = m(i, i + 1)$, and for $j > i + 1$,

$$\mathrm{opt}(i, j) = m(i, j) + \max_{i < k < j} \big[ \mathrm{opt}(i, k) + \mathrm{opt}(k, j) \big].$$

*Proof.* The first equation is Lemma 1 with the only bracketing $\{(i, i + 1)\}$. For $j > i + 1$, every bracketing of $(i, j)$ is $\{(i, j)\} \cup B_1 \cup B_2$ for a split $k$ and bracketings $B_1$ of $(i, k)$ and $B_2$ of $(k, j)$, and every such choice gives a bracketing. The sum of $m$ over it is $m(i, j) + \sum_{B_1} m + \sum_{B_2} m$, because the union is disjoint. For a fixed $k$, the two sums are chosen independently, so their largest total is $\mathrm{opt}(i, k) + \mathrm{opt}(k, j)$ by Lemma 1. Maximizing over $k$ gives the recurrence. $\square$

## Theorem

CHART-PARSE stops, returns $\mathrm{best}(0, n) = \mathrm{opt}(0, n)$, and returns the spans of a labeled tree over $(0, n)$ with this score.

*Proof.* **Termination.** Lines L1 to L8 are three nested loops with fixed bounds: $n$ lengths, at most $n$ start positions, at most $n$ splits and $L$ labels. The walk of line L9 visits each span of the result once, and there are $2n - 1$ of them.

**The table.** We show $\mathrm{best}(i, j) = \mathrm{opt}(i, j)$ by induction on the length $j - i$. Line L4 takes a label $\ell(i, j)$ of largest $s_{\text{label}}(i, j, \cdot)$, so $s_{\text{label}}(i, j, \ell(i, j)) + s_{\text{span}}(i, j) = m(i, j)$. For length 1, line L5 sets $\mathrm{best}(i, i + 1) = m(i, i + 1)$, which is the base case of Lemma 2. For a length $\ell \ge 2$, the loop of line L1 has finished all shorter lengths, so by the induction hypothesis $\mathrm{best}(i, k) = \mathrm{opt}(i, k)$ and $\mathrm{best}(k, j) = \mathrm{opt}(k, j)$ for every $i < k < j$. Line L6 picks a split $k(i, j)$ that maximizes their sum, and line L7 stores $m(i, j)$ plus that sum. By Lemma 2 this is $\mathrm{opt}(i, j)$.

**The tree.** Let $T(i, j)$ be the labeled tree that the walk of line L9 produces from $(i, j)$: the span $(i, j)$ with the label $\ell(i, j)$, and, if $j > i + 1$, the trees $T(i, k)$ and $T(k, j)$ for $k = k(i, j)$. By induction on the length, $T(i, j)$ is a labeled tree over $(i, j)$ with score $\mathrm{best}(i, j)$: for length 1 its score is $m(i, i + 1) = \mathrm{best}(i, i + 1)$; for a longer span its score is $m(i, j) + \mathrm{best}(i, k) + \mathrm{best}(k, j) = \mathrm{best}(i, j)$ by line L7. Line L10 returns $T(0, n)$ and $\mathrm{best}(0, n) = \mathrm{opt}(0, n)$. $\square$

## Corollary: loss-augmented decoding

Let $T^*$ be a binarized gold tree, and for a span $u$ let $\ell^*(u)$ be its gold label if $u \in T^*$ and $\varnothing$ otherwise. For a labeled tree $T$ with bracketing $B$, let the Hamming loss be $\Delta(T, T^*) = \sum_{u \in B} [\ell(u) \ne \ell^*(u)]$. Run CHART-PARSE with the label scores $s'_{\text{label}}(u, \ell) = s_{\text{label}}(u, \ell) + [\ell \ne \ell^*(u)]$. Then it returns a tree that maximizes $s(T) + \Delta(T, T^*)$ over all labeled trees.

*Proof.* The score of $T$ under $s'$ is $\sum_{u \in B} [s_{\text{label}}(u, \ell(u)) + [\ell(u) \ne \ell^*(u)] + s_{\text{span}}(u)] = s(T) + \Delta(T, T^*)$. The theorem applies to $s'$, since it allows any real scores. $\blacksquare$

The page uses the corollary for the hinge loss $\max(0, \max_T [s(T) + \Delta(T, T^*)] - s(T^*))$, which is therefore computed exactly by one run of the decoder.
