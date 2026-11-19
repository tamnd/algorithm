---
tag: S7WPYE
kind: algorithm
slug: glove
name: "GloVe"
aliases:
- global vectors for word representation
area: natural-language-and-speech/word-and-sentence-embeddings
level: core
summary: Fit word and context vectors whose dot product plus biases matches the log co-occurrence count, by weighted least squares on nonzero counts.
model: real-ram
complexity:
  vars: {N: "the number of tokens in the corpus", K: "the window radius", M: "the number of nonzero co-occurrence cells", d: "the dimension of the vectors", T: "the number of epochs", V: "the vocabulary size, the number of types"}
  time: {worst: "O(N K + T M d)"}
  space: {extra: "O(M + V d)"}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2014
  people: [Jeffrey Pennington, Richard Socher, Christopher D. Manning]
  note: "Pennington, Socher and Manning at Stanford proposed GloVe in 2014. They derived the weighted least squares cost from ratios of co-occurrence probabilities and presented it as a link between count methods such as LSA and window methods such as skip-gram."
prereqs: [word-context-matrix, word-embedding, adagrad]
see_also: [skip-gram-model, negative-sampling, sgns-implicit-factorization-theorem, weighted-least-squares, latent-semantic-analysis, pointwise-mutual-information, alternating-least-squares, word-analogy]
sources:
  - paper: "Jeffrey Pennington, Richard Socher and Christopher D. Manning, GloVe: global vectors for word representation, Proceedings of EMNLP 2014, pages 1532 to 1543"
    title: Pennington, Socher and Manning 2014
    locator: "Section 3 (equation 7, the log-bilinear relation with biases; equation 8, the weighted least squares cost; equation 9, the weighting function and its three conditions), Section 3.2 (the complexity, |X| = O(|C|^0.8) under a power law with exponent 1.25), Section 4.2 (x_max = 100, alpha = 3/4, AdaGrad with initial rate 0.05, the 1/d weight of distant pairs, and the sum W + W~)"
  - paper: "John Duchi, Elad Hazan and Yoram Singer, Adaptive subgradient methods for online learning and stochastic optimization, Journal of Machine Learning Research 12, 2011, pages 2121 to 2159"
    title: Duchi, Hazan and Singer 2011
    locator: the AdaGrad update with per-coordinate step sizes
  - paper: "Omer Levy, Yoav Goldberg and Ido Dagan, Improving distributional similarity with lessons learned from word embeddings, Transactions of the Association for Computational Linguistics 3, 2015"
    title: Levy, Goldberg and Dagan 2015
    locator: the comparison of GloVe, skip-gram with negative sampling, PPMI and SVD under the same hyperparameters
---

GloVe fits a vector $\vec w_i$ and a context vector $\tilde{\vec w}_j$ to each word so that their dot product, plus a bias for each, is close to the logarithm of the number of times the two words occur near each other. It first counts the co-occurrences of the corpus into a sparse matrix $X$, and then minimizes a weighted sum of squared errors over the nonzero cells of $X$ only, with a weight that grows with the count and stops at a cap. Pennington, Socher and Manning (2014) proposed it. It works on the global counts, like [latent semantic analysis](/latent-semantic-analysis/), and fits a log-bilinear model, like the [skip-gram model](/skip-gram-model/). Its cost after the counting pass depends on the number of distinct pairs, not on the length of the corpus.

## In plain words

First go through the text once and count, for every pair of words, how often they appear close to each other. Pairs that are very close count more than pairs that are far apart.

Then give each word two short lists of numbers and a single extra number for each list. For every pair that was seen at least once, combine the two lists of the two words into one score. The goal is that this score, plus the two extra numbers, matches the logarithm of the count.

The fit cares more about pairs seen many times, because their counts are reliable, but there is a limit so that very common pairs do not take over. Pairs never seen are skipped. The two lists of each word are added together at the end to give its vector.

## The problem

The input is a corpus of $N$ tokens over a vocabulary $V$, a window radius $K$, a dimension $d$ and the constants $x_{\max}$ and $\alpha$. The co-occurrence matrix $X$ has the entries

$$X_{ij} = \sum_{\text{token pairs } (i, j) \text{ at distance } r \le K} \frac{1}{r},$$

counted in both directions, so $X$ is symmetric. The output is a vector $\vec w_i + \tilde{\vec w}_i \in \mathbb{R}^d$ for each word, from parameters that minimize

$$J = \sum_{i, j:\, X_{ij} > 0} f(X_{ij}) \big(\vec w_i \cdot \tilde{\vec w}_j + b_i + \tilde b_j - \log X_{ij}\big)^2, \qquad f(x) = \begin{cases} (x / x_{\max})^{\alpha} & x < x_{\max}, \\ 1 & \text{otherwise.} \end{cases}$$

Pennington et al. ask for three conditions on $f$: $f(0) = 0$ with $f(x)\log^2 x$ bounded as $x \to 0$, $f$ non-decreasing, and $f$ not too large for large $x$. They fix $x_{\max} = 100$ and $\alpha = 3/4$, values chosen from their measurements. The cost is not convex in the parameters, and GloVe looks for a local minimum by stochastic descent.

## The algorithm

```pseudo id=main
GLOVE(corpus, K, d, T, η, x_max, α)
L1  X ← the co-occurrence counts, 1/r for each pair at distance r ≤ K, both directions
L2  W, W~ ← small uniform random values; b, b~ ← 0; every AdaGrad sum G ← 1
L3  for epoch ← 1 to T do
L4      for each cell (i, j) with X_ij > 0, in random order do
L5          e ← w_i · w~_j + b_i + b~_j - log X_ij        ▷ the residual
L6          g ← f(X_ij) e                                ▷ half the gradient factor
L7          w_i ← w_i - η g w~_j / sqrt(G); w~_j ← w~_j - η g w_i / sqrt(G); same for b_i and b~_j; then G ← G + (the gradient)^2
L8  return W + W~                                        ▷ one vector per word
```

Line L1 is one pass over the corpus. For each token it looks back at the $K$ previous tokens and adds $1/r$ to both $X_{ij}$ and $X_{ji}$, as the released counting tool does with its symmetric window. Line L2 starts the vectors near zero, with values in $(-0.5/d, 0.5/d)$, and starts each AdaGrad sum at 1, as the released code does, so the first steps have the plain step size $\eta$. Lines L4 to L7 are stochastic gradient descent with [AdaGrad](/adagrad/) on one term of $J$ at a time. The term of cell $(i, j)$ has the gradient $2 f(X_{ij})\, e\, \tilde{\vec w}_j$ with respect to $\vec w_i$, and the code drops the factor 2 into the step size. Each coordinate has its own sum $G$ of squared gradients, so a parameter that has had large gradients takes smaller steps. Line L8 adds the two vector sets. Because $X$ is symmetric, $W$ and $\tilde W$ fit the same data and differ only by their random start; Pennington et al. report that the sum gives a small gain.

## Example

Take the one-sentence corpus "the cat sat" with $K = 2$. The pairs are (the, cat) and (cat, sat) at distance 1 and (the, sat) at distance 2, so

| | the | cat | sat |
|---|---|---|---|
| the | 0 | 1 | 0.5 |
| cat | 1 | 0 | 1 |
| sat | 0.5 | 1 | 0 |

The diagonal cells and every zero cell are skipped by line L4, so there are six terms. With $x_{\max} = 100$ the weights are tiny, $f(1) = 0.0316$ and $f(0.5) = 0.0188$, because the counts are far below the cap; for this toy, take $x_{\max} = 1$, so $f(1) = 1$ and $f(0.5) = 0.5946$.

One step on the cell (sat, the), with $d = 2$, $\vec w_{\text{sat}} = (0.1, 0.2)$, $\tilde{\vec w}_{\text{the}} = (0.3, -0.1)$, zero biases, $\eta = 0.05$ and all AdaGrad sums at 1:

| quantity | line | value |
|---|---|---|
| $e = 0.01 + 0 + 0 - \log 0.5$ | L5 | 0.7031 |
| $g = 0.5946 \times 0.7031$ | L6 | 0.4181 |
| $\vec w_{\text{sat}} - 0.05 \cdot 0.4181 \cdot (0.3, -0.1)$ | L7 | (0.0937, 0.2021) |
| $\tilde{\vec w}_{\text{the}} - 0.05 \cdot 0.4181 \cdot (0.1, 0.2)$ | L7 | (0.2979, -0.1042) |
| $b_{\text{sat}}$ and $\tilde b_{\text{the}}$ | L7 | -0.0209 each |
| new residual | L5 | 0.6582 |

The term $f e^2$ goes from 0.2940 to 0.2576. Most of the gain comes from the two biases, which move the score toward $\log 0.5 = -0.6931$. The AdaGrad sum of the first coordinate of $\vec w_{\text{sat}}$ is now $1 + (0.4181 \times 0.3)^2 = 1.0157$.

On a planted corpus where five words occur only with one set of context words and five other words only with another set, a run with $d = 8$, $K = 2$, $x_{\max} = 10$ and 40 epochs gives a cosine between any two words of the same group that is higher than any cosine across the groups.

## Correctness

GloVe is a heuristic optimizer: the claims are about what each line computes, not about a global minimum.

- Line L1 computes $X$ exactly as defined: every unordered pair of tokens at distance $r \le K$ is visited once, from its later token, and adds $1/r$ to both cells.
- Lines L5 to L7 move each parameter against the exact gradient of one term of $J$, scaled per coordinate by $\eta / \sqrt{G} > 0$. A positive diagonal scaling of a gradient is still a descent direction, so for a small enough $\eta$ each step lowers that term.
- $J \ge 0$, and $J = 0$ exactly when every cell with $X_{ij} > 0$ is fitted exactly. If the matrix of $\log X_{ij}$ on the nonzero cells can be matched by a rank-$d$ product plus biases, such a point is a global minimum.
- For fixed context vectors and biases, $J$ is a convex quadratic in each $\vec w_i$ (a [weighted least squares](/weighted-least-squares/) problem), and the same holds with the roles swapped. This is why [alternating least squares](/alternating-least-squares/) also applies.

The full proofs of the counting rule, the gradient and the descent property are in the proof file.

## Complexity

Line L1 does $K$ updates per token, $O(NK)$ time with a hash table, and stores the $M$ nonzero cells. Each cell visit of lines L5 to L7 costs $O(d)$, so an epoch costs $O(Md)$ and the training $O(TMd)$. The memory is $O(M)$ for $X$ and $O(Vd)$ for the four parameter tables and the AdaGrad sums. $M$ is at most $V^2$. Pennington et al. model the counts as a power law of the rank of the pair; with the exponent 1.25 that they measured on their corpora, $M$ grows like $|C|^{0.8}$ with the corpus size $|C|$. This is a measurement on their corpora, not a bound.

## Properties

- **Randomized.** The start and the order of the cells are random. With a fixed seed the run is repeatable.
- **Counts first.** After line L1 the corpus is no longer needed, and the cost of an epoch does not depend on $N$.
- **Only nonzero cells.** The weight $f(0) = 0$ removes the zero cells from $J$, which avoids $\log 0$ and keeps the cost proportional to $M$.
- **Not normalized.** The dot products fit log counts, not probabilities. The biases absorb the word frequencies.
- **Symmetric.** For a symmetric $X$, swapping $W$ with $\tilde W$ and $b$ with $\tilde b$ maps solutions to solutions.

## Variants and improvements

- **Asymmetric windows.** Counting only the left context gives a non-symmetric $X$; Pennington et al. report it as better for the syntactic analogies with small windows.
- **The unweighted log baseline.** Fitting $\log(1 + X_{ij})$ on all cells with equal weights gives an SVD-like model that Pennington et al. use as a baseline. GloVe differs by the weight and by skipping the zeros.
- **Count models.** A truncated SVD of a [PPMI matrix](/positive-pointwise-mutual-information/) factorizes a similar matrix in closed form. [Skip-gram with negative sampling](/negative-sampling/) has an optimum at the shifted PMI matrix ([SGNS factorization theorem](/sgns-implicit-factorization-theorem/)). GloVe's $\log X_{ij} - b_i - \tilde b_j$ plays the role of the PMI, with the biases learned instead of fixed to the log marginals.
- **Other optimizers.** Plain SGD, Adam or alternating least squares minimize the same $J$.

## When to use it

Use GloVe when the corpus is large and you can afford the memory for the nonzero counts: each epoch costs $O(Md)$, so many epochs are cheap compared with passes over the text. Use [skip-gram with negative sampling](/negative-sampling/) when the counts do not fit in memory or the text arrives as a stream. Levy, Goldberg and Dagan (2015) found that, with the same hyperparameters and preprocessing, neither method is better on all tasks. For subword information or vectors for unseen words, use [subword information embeddings](/subword-information-embeddings/).

## Pitfalls

- **Zero cells.** Line L4 must loop over the nonzero cells only. Looping over all cells calls $\log 0$ on line L5.
- **The weight above the cap.** Line L6 must use $f(x) = 1$ for $x \ge x_{\max}$. Using $(x/x_{\max})^{\alpha}$ for all $x$ gives the most frequent pairs, such as those with "the", weights far above 1, and they then dominate the fit.
- **AdaGrad sums at zero.** If line L2 starts $G$ at 0 instead of 1, the first step divides by $\sqrt{0}$ for any coordinate with a zero gradient so far. Start at a positive value, or add a small constant.
- **Distance weight.** Line L1 adds $1/r$, not 1. Without the weight, distant pairs count as much as adjacent ones, which changes $X$ and the vectors.
- **The factor 2.** The code drops the factor 2 of the gradient into $\eta$. A gradient check must compare with $2 f e$, not $f e$.

## Implementations

## History

Pennington, Socher and Manning published GloVe at EMNLP 2014, with code and vectors trained on Wikipedia with Gigaword and on Common Crawl. They derived the model from the observation that ratios of co-occurrence probabilities, such as $P(\text{solid} \mid \text{ice}) / P(\text{solid} \mid \text{steam})$, separate related from unrelated words, and they showed that the skip-gram objective, grouped by word pairs, is a weighted sum over the same cells. The released vectors became a common input layer for neural models of language.

## References
