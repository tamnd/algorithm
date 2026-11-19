---
tag: Y7VQ1F
kind: theorem
slug: sgns-implicit-factorization-theorem
name: SGNS as implicit matrix factorization
aliases:
- Levy-Goldberg theorem
area: natural-language-and-speech/word-and-sentence-embeddings
level: advanced
summary: "If every dot product w . c is free, the best skip-gram with k negative samples has w . c = PMI(w, c) - log k, so it factorizes a shifted PMI matrix."
prereqs: [negative-sampling, pointwise-mutual-information, word-context-matrix]
see_also: [skip-gram-model, positive-pointwise-mutual-information, glove, latent-semantic-analysis, singular-value-decomposition, noise-contrastive-estimation, word-embedding]
sources:
  - paper: "Omer Levy and Yoav Goldberg, Neural word embedding as implicit matrix factorization, Advances in Neural Information Processing Systems 27 (NIPS 2014), pages 2177 to 2185"
    title: Levy and Goldberg 2014
    locator: "Section 2 (the SGNS objective, equations 1 and 2), Section 3.1 (the cell objective, equation 5, and its optimum, equations 6 and 7; the paper has no numbered theorem), equation 8 (the same analysis for NCE), Section 3.2 (weighted factorization when d is small), footnote 1 (the smoothed noise distribution)"
  - paper: "Tomas Mikolov, Ilya Sutskever, Kai Chen, Greg Corrado and Jeffrey Dean, Distributed representations of words and phrases and their compositionality, Advances in Neural Information Processing Systems 26 (NIPS 2013), pages 3111 to 3119, arXiv:1310.4546"
    title: Mikolov, Sutskever, Chen, Corrado and Dean 2013
    locator: the negative sampling objective and the unigram noise distribution to the power 3/4
  - paper: "Yoav Goldberg and Omer Levy, word2vec explained: deriving Mikolov et al.'s negative-sampling word-embedding method, arXiv:1402.3722, 2014 (preprint)"
    title: Goldberg and Levy 2014
    locator: the derivation of the negative sampling objective as a sum over word and context pairs
  - paper: "Omer Levy, Yoav Goldberg and Ido Dagan, Improving distributional similarity with lessons learned from word embeddings, Transactions of the Association for Computational Linguistics 3, 2015"
    title: Levy, Goldberg and Dagan 2015
    locator: the smoothed context distribution and the comparison of SGNS with PPMI and SVD
---

## Statement

Let $D$ be a multiset of word and context pairs $(w, c)$, for example the pairs that a [skip-gram model](/skip-gram-model/) reads from a corpus with a window. Write $\#(w, c)$ for the number of copies of $(w, c)$ in $D$, $\#(w) = \sum_c \#(w, c)$, $\#(c) = \sum_w \#(w, c)$ and $|D| = \sum_{w, c} \#(w, c)$. All logarithms are natural. The [pointwise mutual information](/pointwise-mutual-information/) of a pair is

$$\operatorname{PMI}(w, c) = \log \frac{\#(w, c)\,|D|}{\#(w)\,\#(c)}.$$

Each word $w$ has a vector $\vec w \in \mathbb{R}^d$ and each context $c$ a vector $\vec c \in \mathbb{R}^d$. Stack them as the rows of $W$ and $C$. Skip-gram with [negative sampling](/negative-sampling/) (SGNS) with $k$ noise samples per pair and the noise distribution $P_D(c) = \#(c)/|D|$ maximizes the expected objective

$$\ell(W, C) = \sum_{w, c} \#(w, c)\Big(\log \sigma(\vec w \cdot \vec c) + k\,\mathbb{E}_{c_N \sim P_D} \log \sigma(-\vec w \cdot \vec c_N)\Big),$$

where $\sigma(x) = 1/(1 + e^{-x})$. Collect the terms of each cell $x_{wc} = \vec w \cdot \vec c$:

$$\ell = \sum_{w, c} g_{wc}(x_{wc}), \qquad g_{wc}(x) = \#(w, c) \log \sigma(x) + k\,\frac{\#(w)\,\#(c)}{|D|} \log \sigma(-x).$$

**Theorem (Levy and Goldberg 2014, Section 3.1).** Let $V_W$ and $V_C$ be the words and the contexts with $\#(w) > 0$ and $\#(c) > 0$, and suppose that $\#(w, c) > 0$ for every $w \in V_W$ and $c \in V_C$. Let $M$ be the $|V_W| \times |V_C|$ matrix of the shifted PMI, $M_{wc} = \operatorname{PMI}(w, c) - \log k$.

1. Over all real matrices $X$, the function $\sum_{w, c} g_{wc}(X_{wc})$ has exactly one maximizer, $X = M$.
2. If $d \ge \operatorname{rank} M$, the global maximizers of $\ell(W, C)$ are exactly the pairs $(W, C)$ with $W C^\top = M$. That is, at a global maximum, $\vec w \cdot \vec c = \operatorname{PMI}(w, c) - \log k$ for every pair.

The hypothesis $d \ge \operatorname{rank} M$ is the precise form of the condition in the paper, that each product $\vec w \cdot \vec c$ "can assume a value independently of the others". It always holds for $d \ge \min(|V_W|, |V_C|)$. Real embeddings have $d$ of a few hundred and $|V|$ of many thousands, so they do not meet it, and their dot products only approximate the shifted PMI.

## In plain words

Skip-gram with negative sampling learns a vector for each word and each context. Training pushes the score of every real pair up and the score of random pairs down. If the vectors are long enough that each score can be set on its own, the best score of a pair is a known number: how much more often the two appear together than chance predicts, on a log scale, minus the log of the number of random pairs. So the method fills a table of these numbers and writes it as a product of two thin matrices. This links neural word vectors to older methods that build the same table from counts. With short vectors the table cannot be matched exactly, and the method finds a compromise that cares most about frequent pairs.

## Proof

*Step 1: the objective splits into cells.* The expectation over the noise is $\mathbb{E}_{c_N \sim P_D} \log \sigma(-\vec w \cdot \vec c_N) = \sum_{c'} \frac{\#(c')}{|D|} \log \sigma(-\vec w \cdot \vec c')$. It does not depend on the observed context $c$, so its total weight in $\ell$ is $\sum_c \#(w, c) = \#(w)$. Hence

$$\ell = \sum_{w, c} \#(w, c) \log \sigma(\vec w \cdot \vec c) + \sum_{w} \#(w) \sum_{c'} k\,\frac{\#(c')}{|D|} \log \sigma(-\vec w \cdot \vec c'),$$

and renaming $c'$ as $c$ gives $\ell = \sum_{w, c} g_{wc}(x_{wc})$.

*Step 2: one cell.* Fix $w$ and $c$ and write $a = \#(w, c)$ and $b = k\,\#(w)\#(c)/|D|$, both positive by the hypothesis. Use $\frac{d}{dx} \log \sigma(x) = \sigma(-x)$ and $\frac{d}{dx} \log \sigma(-x) = -\sigma(x)$. Then

$$g'(x) = a\,\sigma(-x) - b\,\sigma(x), \qquad g''(x) = -(a + b)\,\sigma(x)\,\sigma(-x) < 0.$$

So $g$ is strictly concave and has at most one stationary point. The equation $g'(x) = 0$ reads $a\,\sigma(-x) = b\,\sigma(x)$. Since $\sigma(x)/\sigma(-x) = e^x$, it is $e^x = a/b$, with the one solution

$$x^* = \log \frac{a}{b} = \log \frac{\#(w, c)\,|D|}{\#(w)\,\#(c)} - \log k = \operatorname{PMI}(w, c) - \log k.$$

A strictly concave function with a stationary point has its unique maximum there.

*Step 3: part 1.* The sum $\sum g_{wc}(X_{wc})$ has a separate variable in each term. It is at most $\sum g_{wc}(M_{wc})$, and by Step 2 equality holds if and only if $X_{wc} = M_{wc}$ for every cell.

*Step 4: part 2.* For any $(W, C)$, $\ell(W, C) = \sum g_{wc}((W C^\top)_{wc}) \le \sum g_{wc}(M_{wc})$, with equality if and only if $W C^\top = M$, by part 1. It remains to show that the bound is reached. Let $r = \operatorname{rank} M \le d$, and take the [singular value decomposition](/singular-value-decomposition/) $M = U \Sigma V^\top$ with the $r$ nonzero singular values. Put $W = U_r \Sigma_r^{1/2}$ and $C = V_r \Sigma_r^{1/2}$, padded with $d - r$ zero columns. Then $W C^\top = M$, so the bound is the maximum and the maximizers are exactly the factorizations of $M$. $\blacksquare$

**Worked example.** Take two words and two contexts with $\#(w_1, c_1) = \#(w_2, c_2) = 4$ and $\#(w_1, c_2) = \#(w_2, c_1) = 1$. Then $|D| = 10$ and every marginal count is 5. The PMI is $\log(4 \cdot 10 / 25) = \log 1.6 = 0.4700$ on the diagonal and $\log(1 \cdot 10/25) = \log 0.4 = -0.9163$ off it. With $k = 2$ the shift is $\log 2 = 0.6931$, so

$$M = \begin{pmatrix} \log 0.8 & \log 0.2 \\ \log 0.2 & \log 0.8 \end{pmatrix} = \begin{pmatrix} -0.2231 & -1.6094 \\ -1.6094 & -0.2231 \end{pmatrix}.$$

For the cell $(w_1, c_1)$, $a = 4$ and $b = 2 \cdot 5 \cdot 5 / 10 = 5$, so $x^* = \log 0.8$, as in the matrix. The model then gives the true pair the probability $\sigma(x^*) = a/(a + b) = 4/9$ of being real. That is the share of real copies among the real and the noise copies of the pair. Here $\operatorname{rank} M = 2$, so $d = 2$ is enough, for example $W = M$ and $C = I$.

## Consequences

- **SGNS and count methods fit the same matrix.** Under the hypothesis, SGNS and a factorization of the shifted PMI matrix have the same optimum. Levy and Goldberg use this to propose the shifted positive PMI, $\max(\operatorname{PMI}(w, c) - \log k, 0)$, as a sparse count-based alternative, factored by a truncated SVD as in [latent semantic analysis](/latent-semantic-analysis/). See also [positive pointwise mutual information](/positive-pointwise-mutual-information/).
- **The smoothed noise distribution.** word2vec draws noise from the unigram distribution to the power 3/4, not from $P_D$ (footnote 1 of the paper). The same proof with $P_n(c)$ in place of $\#(c)/|D|$ gives $x^* = \log \frac{\#(w, c)}{\#(w)\,P_n(c)} - \log k$. Since $P_n$ gives more mass to rare contexts than $P_D$, rare contexts get a lower score. Levy, Goldberg and Dagan 2015 call this context distribution smoothing and apply it to PMI.
- **NCE.** The same cell analysis for [noise-contrastive estimation](/noise-contrastive-estimation/) gives $\vec w \cdot \vec c = \log P(w \mid c) - \log k$ (equation 8 of the paper): NCE fits a shifted log conditional probability, not a PMI.
- **Unseen pairs.** If $\#(w, c) = 0$ while $\#(w)\#(c) > 0$, then $a = 0$ and $g_{wc}(x) = b \log \sigma(-x)$ increases as $x \to -\infty$. The supremum is not reached, which matches $\operatorname{PMI} = -\infty$. The real matrix of a corpus has many such cells, so the exact optimum does not exist there, and the low dimension and the training keep the scores finite.
- **Low dimension.** With $d < \operatorname{rank} M$, SGNS maximizes $\sum g_{wc}((W C^\top)_{wc})$ over matrices of rank at most $d$. Near the optimum $g_{wc}$ has the curvature $(a + b)\sigma(x^*)\sigma(-x^*)$, which grows with the counts, so the fit is a weighted factorization that pays more attention to frequent pairs (Section 3.2 of the paper). [GloVe](/glove/) makes a weighted least squares fit of the log counts explicit.

## Tightness

Each hypothesis is needed.

- **Dimension.** In the worked example $M$ has rank 2, since $\det M = 0.0498 - 2.5903 \ne 0$. With $d = 1$ every $W C^\top$ has rank at most 1, so no pair $(W, C)$ reaches $X = M$, and the global maximum of $\ell$ has some cell with $\vec w \cdot \vec c \ne \operatorname{PMI}(w, c) - \log k$.
- **Global maximum, not any stationary point.** The point $W = 0$, $C = 0$ is stationary: the gradient of $\ell$ with respect to $\vec w$ is $\sum_c g_{wc}'(x_{wc})\,\vec c$, which is zero when every $\vec c = 0$, and the same holds for $\vec c$. There every product is 0, not the shifted PMI. The objective is not concave in $(W, C)$, so the theorem speaks of its global maxima.
- **Positive counts.** Without $\#(w, c) > 0$ the maximum does not exist, as shown under Consequences.
- **The expected objective.** The theorem is about the expectation over the noise samples. Stochastic training with a finite number of epochs, a decaying learning rate, subsampling of frequent words and a dynamic window reaches an approximation, and the subsampling and the window change the effective counts $\#(w, c)$.

## History

Mikolov, Sutskever, Chen, Corrado and Dean introduced negative sampling in 2013 as a simplification of NCE for the skip-gram model. Goldberg and Levy wrote out its objective as a sum over pairs in an arXiv note in early 2014. Levy and Goldberg then showed at NIPS 2014 that its optimum with free dot products is the shifted PMI matrix. This tied the neural method to the PMI matrices of distributional semantics. Levy, Goldberg and Dagan 2015 carried the tuning choices of word2vec, such as the smoothed context distribution, over to the count methods and found the gaps between the two families small in their experiments.

## References
