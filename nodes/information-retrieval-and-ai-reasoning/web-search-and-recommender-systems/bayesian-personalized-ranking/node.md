---
tag: JYHKHX
kind: algorithm
slug: bayesian-personalized-ranking
name: Bayesian personalized ranking
aliases:
- BPR
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: advanced
summary: Learns from implicit feedback by maximizing the log-sigmoid of the score margin between an observed item and a sampled unobserved one.
solves: [recommendation-problem]
model: word-ram
complexity:
  vars: {m: the number of users, n: the number of items, r: the number of factors, T: the number of sampled triples}
  time: {expected: O(T r + (m + n) r)}
  space: {extra: O((m + n) r)}
properties: {deterministic: false, exact: false, online: true, recursive: false}
history:
  year: 2009
  people: [Steffen Rendle, Christoph Freudenthaler, Zeno Gantner, Lars Schmidt-Thieme]
  note: Rendle, Freudenthaler, Gantner and Schmidt-Thieme (UAI 2009) derived the pairwise criterion BPR-Opt as a maximum posterior estimate and trained it with LearnBPR, stochastic gradient steps on triples drawn with replacement.
prereqs: [implicit-feedback, matrix-factorization-recommendation, stochastic-gradient-descent]
see_also: [implicit-feedback-als, roc-auc, logistic-loss, learning-to-rank, maximum-a-posteriori-estimation, neural-collaborative-filtering, gru4rec, factorization-machine]
sources:
  - paper: arxiv:1205.2618
    title: Steffen Rendle, Christoph Freudenthaler, Zeno Gantner and Lars Schmidt-Thieme, BPR, Bayesian personalized ranking from implicit feedback, Proceedings of the 25th Conference on Uncertainty in Artificial Intelligence (UAI 2009), 452-461
    locator: Section 3 (the set D_S), Section 4.1 (BPR-Opt) and 4.1.1 (analogy to AUC, Equation 1), Section 4.2 and Figure 4 (LearnBPR), Section 4.3.1 (the gradients for matrix factorization), Section 5.1 (relation to WR-MF), Section 6 (AUC on Rossmann and Netflix data, Figure 6)
  - paper: doi:10.1109/ICDM.2008.22
    title: Yifan Hu, Yehuda Koren and Chris Volinsky, Collaborative filtering for implicit feedback datasets, ICDM 2008, 263-272
    locator: Section 4 (the weighted least squares model that BPR is compared with)
---

Bayesian personalized ranking (BPR) trains a recommender on [implicit feedback](/implicit-feedback/) by comparing pairs of items. For a user $u$, an item $i$ that $u$ used and an item $j$ that $u$ did not use, it asks that the score of $i$ be above the score of $j$, and it maximizes the sum of $\ln \sigma(x_{ui} - x_{uj})$ over such triples, minus a penalty. Rendle, Freudenthaler, Gantner and Schmidt-Thieme (2009) derived this criterion, BPR-Opt, as a maximum posterior estimate, and they fit it with LearnBPR, [stochastic gradient](/stochastic-gradient-descent/) steps on triples drawn at random with replacement. The criterion works with any differentiable scoring model; this page uses [matrix factorization](/matrix-factorization-recommendation/), $x_{ui} = w_u^\top h_i$.

## In plain words

When a user clicked one item and ignored another, we do not know that the user dislikes the ignored item. We only guess that the user likes the clicked one more. BPR learns from exactly this kind of guess: it takes one clicked item and one ignored item, and if the model scores them in the wrong order, or in the right order by only a small margin, it moves the scores apart.

Picking the pairs at random, and not user by user, keeps the same pair from being pushed again and again in a row. The result is a model tuned for the order of the items, which is what a top-10 list needs.

## The problem

The input is a set $S$ of positive pairs of $m$ users and $n$ items, $I_u^+ = \{i : (u, i) \in S\}$, a number of factors $r$, a step size $\alpha$ and penalties $\lambda_W, \lambda_{H^+}, \lambda_{H^-} \ge 0$. The training triples are

$$D_S = \{(u, i, j) : i \in I_u^+, \; j \in I \setminus I_u^+\}.$$

Each triple says that $u$ prefers $i$ to $j$; the pairs with both items used, or both unused, are not compared. With $x_{uij} = x_{ui} - x_{uj}$, BPR-Opt (Section 4.1) is the sum of $\ln \sigma(x_{uij})$ over $D_S$ minus a penalty. The paper writes the penalty once, as $\lambda_\Theta \lVert \Theta \rVert^2$ with $\Theta$ all parameters, which makes BPR-Opt the log posterior of the parameters when each triple is an independent event with probability $\sigma(x_{uij})$ and the prior on $\Theta$ is a zero mean Gaussian. The updates of LearnBPR penalize instead the three vectors of each triple, and this page and its proof use that form:

$$\text{BPR-Opt} = \sum_{(u, i, j) \in D_S} \Bigl[ \ln \sigma(x_{uij}) - \tfrac12 \bigl(\lambda_W \lVert w_u \rVert^2 + \lambda_{H^+} \lVert h_i \rVert^2 + \lambda_{H^-} \lVert h_j \rVert^2\bigr) \Bigr],$$

where $\sigma(z) = 1 / (1 + e^{-z})$. The output is a score for every user and item; the recommendation for $u$ is the unused items in order of score.

## The algorithm

```pseudo id=main
LEARN-BPR(S, r, α, λ_W, λ_H+, λ_H-, T)
L1  w_u, h_i ← small random vectors in R^r for all users and items
L2  repeat T times
L3      draw (u, i) uniformly from S
L4      draw j uniformly from all items; if j ∈ I_u^+ then go back to L3
L5      e ← σ(-x_uij), with x_uij = w_uᵀ(h_i - h_j)
L6      w_u ← w_u + α (e (h_i - h_j) - λ_W w_u)
        h_i ← h_i + α (e w_u - λ_H+ h_i)
        h_j ← h_j + α (-e w_u - λ_H- h_j)      ▷ all three use the old values
L7  return W, H
```

Lines L3 and L4 draw a triple uniformly from $D_S$ by rejection. Line L5 uses $\frac{d}{dz} \ln \sigma(z) = \sigma(-z)$. Line L6 is the gradient step of Section 4.3.1 of the paper, where $\partial x_{uij} / \partial w_u = h_i - h_j$, $\partial x_{uij} / \partial h_i = w_u$ and $\partial x_{uij} / \partial h_j = -w_u$. Each step changes only three vectors.

## Example

Take $r = 2$, $w_u = (0.1, 0.2)$, a used item $h_i = (0.3, -0.1)$, an unused item $h_j = (0.2, 0.4)$, step size $\alpha = 0.5$ and no penalty.

- Scores: $x_{ui} = 0.03 - 0.02 = 0.01$ and $x_{uj} = 0.02 + 0.08 = 0.10$, so $x_{uij} = -0.09$. The model has the pair in the wrong order.
- Line L5: $e = \sigma(0.09) \approx 0.52248$. The loss of the triple is $-\ln \sigma(-0.09) \approx 0.73916$.
- Line L6: $h_i - h_j = (0.1, -0.5)$, so $w_u$ moves by $0.5 \cdot 0.52248 \cdot (0.1, -0.5)$ to $(0.12612, 0.06938)$; $h_i$ moves by $0.5 \cdot 0.52248 \cdot w_u$ to $(0.32612, -0.04775)$; and $h_j$ moves by the opposite amount to $(0.17388, 0.34775)$.
- After the step, $x_{uij} \approx -0.00824$ and the loss is about $0.69727$. The pair is still in the wrong order, but by a much smaller margin.

On a planted data set of 30 users in two groups, where each group uses only its own 10 of the 20 items, the test file trains with $r = 4$ and 40,000 steps. The AUC on one held-out item per user goes from 0.49 for the random start to about 0.84; the best possible is about 0.86, since the model cannot know which unused items of its own group the user will pick.

## Correctness

The proof in `proofs/correctness.md` shows three facts. Line L6 is a step against the exact gradient of the loss $-\ln \sigma(x_{uij})$ plus the penalty of the three vectors. The rejection draw of lines L3 and L4 is uniform on $D_S$, so the expected step is the gradient of the mean loss over $D_S$; a draw of $j$ from the unused items of $u$ would weight the users differently. And for every user, the training AUC is at least $1 + \frac{1}{\ln 2}$ times the mean of $\ln \sigma(x_{uij})$ over its triples, because $\delta(x > 0) \ge 1 + \log_2 \sigma(x)$ for every real $x$. This is the precise sense in which BPR-Opt is a smooth version of the AUC (Section 4.1.1).

The criterion is not convex in $W$ and $H$, and the page does not claim that LearnBPR converges or finds the best factors. That BPR gives better rankings than other methods is a measured result, not a proved one.

## Complexity

- **One step.** Lines L5 and L6 cost $O(r)$. Lines L3 and L4 need $|S| \, n / |D_S|$ tries on average, which is $O(1)$ when each user uses at most a constant fraction of the items.
- **Total.** $O((m + n) r)$ to start and $O(T r)$ expected for $T$ steps. The paper chooses the number of steps linear in $|S|$.
- **Space.** $O((m + n) r)$ for the factors and $O(|S|)$ for the data.
- **Evaluation.** The AUC of one user costs $O(n \log n)$ by sorting the scores, or $O(n^2)$ by direct comparison of pairs.

There are $O(|S| \, n)$ triples, so a full gradient over $D_S$ is too costly on real data. This is the reason for sampling.

## Properties

- **Pairwise.** The loss depends only on differences of scores, so adding a constant to all scores of a user changes nothing.
- **Online.** Each step uses one triple, and steps can run as new data arrives.
- **Model-agnostic.** Any differentiable score $x_{ui}$ can be used; the paper also applies it to an adaptive item-kNN model (Section 4.3.2).
- **Stochastic.** The result depends on the random start and the random triples.

## Variants and improvements

- **Item biases.** Add a bias $b_i$ to $x_{ui}$. User biases cancel in $x_{uij}$, so they are useless here.
- **Weighted least squares.** [Implicit ALS](/implicit-feedback-als/) fits the same factor model to all cells with a pointwise weighted loss. Section 5.1 of the paper calls it WR-MF and argues that its pointwise loss is not tuned to the ranking.
- **Other models.** [Factorization machines](/factorization-machine/) are often trained with the BPR loss when there are side features. [GRU4Rec](/gru4rec/) uses a BPR loss on the scores of a recurrent network, with the other items of the mini-batch as the unused items.
- **Other samplers.** Drawing $j$ by popularity, or picking a $j$ with a high score, gives more informative triples than uniform draws, at the cost of changing the objective that the steps follow in expectation.
- **Hinge loss.** Replacing $-\ln \sigma(x)$ by $\max(0, 1 - x)$ gives a pairwise [hinge loss](/hinge-loss/), as in ranking SVMs.

## When to use it

Use BPR when the data is clicks, plays or purchases, when the goal is a ranked list, and when the data is too large for a full gradient. On a Rossmann purchase set (10,000 users, 4,000 items) and a Netflix subset turned into implicit data (10,000 users, 5,000 items), the paper measured AUC with one held-out item per user and found that the BPR versions of matrix factorization and kNN ranked better than WR-MF, SVD-MF, cosine kNN and the most popular items for all tested numbers of factors (Figure 6). These are measurements on two data sets with the settings and the tuning of the paper, not properties of the method.

## Pitfalls

- **The sign of the penalty.** Figure 4 of the paper prints the update as $\Theta \leftarrow \Theta + \alpha (\frac{e^{-x}}{1 + e^{-x}} \frac{\partial x}{\partial \Theta} + \lambda_\Theta \Theta)$. For a gradient ascent on BPR-Opt the penalty term must be $-\lambda_\Theta \Theta$, as in line L6. With the plus sign the vectors grow.
- **Sampling user by user.** Going through all $j$ for one $(u, i)$ before moving on makes many steps in a row on the same vectors; the paper reports much slower convergence for user-wise traversal (Figure 5).
- **Overflow.** Computing $\ln(1 + e^{-x})$ directly overflows for large negative $x$. Use a stable form, as the code does.
- **Reading the AUC.** A good AUC can come with a poor top of the list, since the AUC weighs all positions the same. Report a top-heavy measure such as [precision at k](/precision-at-k/) or [NDCG](/normalized-discounted-cumulative-gain/) as well.
- **Unused is not disliked.** At test time, a held-out used item is compared with items that the user may like but has not seen. The measured AUC is a lower estimate of the true one.

## Implementations

## History

Rendle, Freudenthaler, Gantner and Schmidt-Thieme presented BPR at UAI 2009. The paper compared it with the weighted least squares methods of Hu, Koren and Volinsky and of Pan et al., both from ICDM 2008, and with maximum margin matrix factorization. The BPR loss became a standard loss for implicit data and was later used with factorization machines, with sequence models such as [GRU4Rec](/gru4rec/), and with neural scoring models.

## References
