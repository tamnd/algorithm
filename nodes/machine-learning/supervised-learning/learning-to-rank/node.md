---
tag: B37NWE
kind: problem
slug: learning-to-rank
name: Learning to rank
aliases:
- LTR
- machine-learned ranking
area: machine-learning/supervised-learning
level: advanced
summary: "Learn a scoring function from queries with graded documents, so that sorting by score puts relevant items first, as measured by NDCG. Pointwise, pairwise and listwise methods."
prereqs: [logistic-regression, gradient-descent]
see_also: [kendall-tau-distance, roc-auc, gradient-boosting, precision-and-recall, inverted-index, pagerank, support-vector-machine, feedback-arc-set-problem]
sources:
  - paper: doi:10.1145/582415.582418
    title: Kalervo Järvelin and Jaana Kekäläinen, Cumulated gain-based evaluation of IR techniques, ACM Transactions on Information Systems 20(4), 2002
    locator: pp. 422 to 446 (cumulated gain, discounted cumulated gain with a log_b discount, and the normalized versions)
  - paper: doi:10.1145/1102351.1102363
    title: Chris Burges, Tal Shaked, Erin Renshaw, Ari Lazier, Matt Deeds, Nicole Hamilton and Greg Hullender, Learning to rank using gradient descent, Proceedings of the 22nd International Conference on Machine Learning (ICML), 2005
    locator: pp. 89 to 96 (RankNet, the pairwise cross entropy cost, and NDCG with gain 2^r - 1 and discount log(1 + j))
  - paper: "Christopher J. C. Burges, Robert Ragno and Quoc V. Le, Learning to rank with nonsmooth cost functions, Advances in Neural Information Processing Systems 19, MIT Press, 2007"
    locator: pp. 193 to 200 (LambdaRank)
  - paper: "Christopher J. C. Burges, From RankNet to LambdaRank to LambdaMART: an overview, Microsoft Research Technical Report MSR-TR-2010-82, 2010"
    locator: Sections 2 to 5 (the lambda gradients, the |ΔNDCG| weights, the factorization speedup and LambdaMART)
  - paper: doi:10.1007/s10791-009-9112-1
    title: Qiang Wu, Christopher J. C. Burges, Krysta M. Svore and Jianfeng Gao, Adapting boosting for information retrieval measures, Information Retrieval 13(3), 2010
    locator: pp. 254 to 270 (LambdaMART, boosted regression trees fitted to the lambda gradients)
  - paper: doi:10.1145/1273496.1273513
    title: Zhe Cao, Tao Qin, Tie-Yan Liu, Ming-Feng Tsai and Hang Li, Learning to rank, from pairwise approach to listwise approach, Proceedings of the 24th International Conference on Machine Learning (ICML), 2007
    locator: pp. 129 to 136 (ListNet and the top one probability)
  - paper: doi:10.1145/775047.775067
    title: Thorsten Joachims, Optimizing search engines using clickthrough data, Proceedings of the 8th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, 2002
    locator: pp. 133 to 142 (Ranking SVM, pairwise preferences from clicks)
  - paper: doi:10.1561/1500000016
    title: Tie-Yan Liu, Learning to rank for information retrieval, Foundations and Trends in Information Retrieval 3(3), 2009
    locator: pp. 225 to 331 (the pointwise, pairwise and listwise approaches)
  - paper: "David Cossock and Tong Zhang, Statistical analysis of Bayes optimal subset ranking, IEEE Transactions on Information Theory 54(11), 2008"
    locator: the Bayes optimal ranking for DCG and the bound of the DCG regret by the regression error
---

Learning to rank is the problem of learning, from examples, a function that orders a set of items for a request. In the standard setting each training query comes with a list of documents, a feature vector for each query-document pair, and a graded relevance label for each document. The learner returns a scoring function $f$, and the system ranks the documents of a new query by sorting them by $f$. Quality is measured on the top of the list, usually by NDCG (Järvelin and Kekäläinen 2002). NDCG is a step function of the scores, so learning methods minimize smooth surrogates, which fall into three families: pointwise (fit each label), pairwise (order each pair, as RankNet and Ranking SVM do) and listwise (score the whole list, as ListNet and LambdaRank do).

## In plain words

A search engine finds a few hundred pages that match a request. It must show the best ones first, because people read only the top of the list. People rate example results for many requests, for example on a scale from 0 (bad) to 4 (perfect). The task is to learn, from these ratings, a rule that gives each page a score, so that sorting by score puts the well rated pages at the top.

The quality of a list counts good pages near the top much more than good pages lower down. You cannot improve that number in small steps, because it changes only when two pages swap places. So the methods learn from a smooth stand-in. Some fit each rating, some check each pair of pages, and some look at the whole list at once.

## Definition

**Data.** A training set has $Q$ queries. Query $q$ has $m_q$ documents with feature vectors $x_{q,1}, \ldots, x_{q,m_q} \in \mathbb{R}^d$, computed from the query and the document together, and labels $y_{q,i} \in \{0, 1, \ldots, R\}$, where a larger label means more relevant. The queries are drawn i.i.d. from an unknown distribution.

**Output.** A scoring function $f: \mathbb{R}^d \to \mathbb{R}$, for example linear, $f(x) = w^{\top} x$, a neural network, or a sum of regression trees. For a query, $\pi_f$ is the permutation that sorts its documents by decreasing $f(x)$, with a fixed rule for ties.

**Measure.** Let $r_i$ be the label of the document at rank $i$ of a list. This page uses
$$ \mathrm{DCG@}k = \sum_{i=1}^{k} \frac{2^{r_i} - 1}{\log_2(i + 1)}, \qquad \mathrm{NDCG@}k = \frac{\mathrm{DCG@}k(\pi_f)}{\mathrm{DCG@}k(\pi^\ast)}, $$
where $\pi^\ast$ sorts the documents by decreasing label. NDCG@k lies in $[0, 1]$ and equals 1 for a list in ideal order. A query with no relevant document has ideal DCG 0; the implementation gives it NDCG 0, and many evaluations drop such queries. The gain $2^r - 1$ and the discount $1 / \log_2(i + 1)$ are those of Burges et al. (2005), and most later work and libraries use them. Järvelin and Kekäläinen (2002) defined DCG with the label itself as the gain and with the discount $1/\log_b i$ applied only from rank $b$ on, so with $b = 2$ the first two ranks are not discounted. The variants give different numbers, so a reported NDCG must state its gain and its discount.

**Goal.** Find $f$ in a class $\mathcal{F}$ that maximizes the expected NDCG@k over the query distribution, from the training queries. Other target measures are the mean average precision, the expected reciprocal rank, and the number of misordered pairs.

## Variants

- **Bipartite ranking.** Labels are 0 or 1. The fraction of (relevant, irrelevant) pairs in the right order is the [area under the ROC curve](/roc-auc/), so pairwise methods maximize AUC.
- **Ordinal regression.** Predict the label itself on an ordered scale, with learned thresholds on the score. Pointwise ranking methods often solve this problem.
- **Top-k ranking.** Only the order of the first $k$ results matters; NDCG@k with a small $k$ such as 10 models this.
- **Learning from clicks.** The labels come from user clicks, which favor documents shown near the top. Joachims (2002) used clicks as pairwise preferences: a clicked document is preferred to a skipped document ranked above it. Later "unbiased" methods weight clicks by the inverse of an estimated examination probability.
- **Rank aggregation.** Combine several given rankings into one, for example by minimizing the total [Kendall tau distance](/kendall-tau-distance/) (the Kemeny ranking). This is NP-hard already for four input rankings (Dwork, Kumar, Naor and Sivakumar 2001), and for every even number of rankings from four on.

## Examples

**NDCG by hand.** Three documents are ranked with labels $(2, 0, 1)$ from the top. The gains are $3, 0, 1$ and the discounts are $1, 1/\log_2 3, 1/2$. So $\mathrm{DCG} = 3 + 0 + \frac12 = 3.5$. The ideal order is $(2, 1, 0)$, with $\mathrm{DCG} = 3 + 1/\log_2 3 \approx 3.6309$, so $\mathrm{NDCG} \approx 0.9639$. At $k = 2$ the list $(0, 2, 1)$ has $\mathrm{DCG@}2 = 3/\log_2 3 \approx 1.8928$ and $\mathrm{NDCG@}2 \approx 0.5213$, and $\mathrm{NDCG@}1 = 0$: the cutoff makes the top position decisive. With the label itself as the gain and the same discount, the labels $(3, 2, 3, 0, 1, 2)$ give $\mathrm{DCG} \approx 6.861$, ideal $\mathrm{DCG} \approx 7.141$ and $\mathrm{NDCG} \approx 0.961$.

**RankNet and LambdaRank on one query.** One feature, three documents: $x = 0, 1, 2$ with labels $2, 0, 1$. The linear scorer $w = 1$ gives scores $0, 1, 2$, so the ranking is documents 2, 1, 0 with labels $(1, 0, 2)$ and $\mathrm{NDCG} = 2.5 / 3.6309 \approx 0.689$. RankNet with $\sigma = 1$ uses each pair $(i, j)$ with $y_i > y_j$, the cost $C_{ij} = \log(1 + e^{-(s_i - s_j)})$ and $\lambda_{ij} = \partial C_{ij} / \partial s_i = -1/(1 + e^{s_i - s_j})$.

| pair $(i, j)$ | $s_i - s_j$ | $C_{ij}$ | $\lambda_{ij}$ | $\lvert\Delta \mathrm{NDCG}_{ij}\rvert$ |
| --- | --- | --- | --- | --- |
| (0, 1) | −1 | 1.3133 | −0.7311 | 0.1082 |
| (0, 2) | −2 | 2.1269 | −0.8808 | 0.2754 |
| (2, 1) | 1 | 0.3133 | −0.2689 | 0.1017 |

The total cost is $3.7535$. Each $\lambda_{ij}$ is added to $\lambda_i$ and subtracted from $\lambda_j$, which gives $\lambda = (-1.612, 1.000, 0.612)$ for documents 0, 1, 2. The gradient is $\sum_i \lambda_i x_i = 2.224$, so gradient descent lowers $w$. At $w = -1$ the order becomes 0, 1, 2 with labels $(2, 0, 1)$, the cost drops to $1.753$ and NDCG rises to $0.964$. No linear scorer on this one feature reaches NDCG 1, because the ideal order 0, 2, 1 is not monotone in $x$. LambdaRank multiplies each $\lambda_{ij}$ by the NDCG change from swapping $i$ and $j$ in the current list. That gives $\lambda = (-0.322, 0.106, 0.215)$: the pair (0, 2), whose swap moves the best document from rank 3 to rank 1, now dominates.

## Known algorithms

**Pointwise.** Fit each label alone by regression or classification, then sort by the prediction. Cossock and Zhang (2008) bound the DCG regret of a regression fit by its squared error. McRank fits class probabilities and scores by the expected label. These methods ignore that only the order inside a query matters, and they spend capacity on queries with many documents.

**Pairwise.**

- *Ranking SVM* (Herbrich, Graepel and Obermayer 2000; Joachims 2002): a [support vector machine](/support-vector-machine/) on the difference vectors $x_i - x_j$ of the preferred pairs, with the hinge loss $\max(0, 1 - w^{\top}(x_i - x_j))$.
- *RankBoost* (Freund, Iyer, Schapire and Singer 2003): boosting with the exponential loss on pairs.
- *RankNet* (Burges et al. 2005): model $P(i \rhd j) = 1/(1 + e^{-\sigma(s_i - s_j)})$ and minimize the cross entropy with the target probabilities, here 1 for each pair with $y_i > y_j$. The cost $\log(1 + e^{-\sigma(s_i - s_j)})$ is [logistic regression](/logistic-regression/) on pairs. The original used a two-layer neural network trained by [stochastic gradient descent](/stochastic-gradient-descent/). Burges (2010) shows that the gradient of a query factorizes: $\partial C / \partial w = \sum_i \lambda_i\, \partial s_i / \partial w$ with $\lambda_i = \sum_{j: y_i > y_j} \lambda_{ij} - \sum_{j: y_j > y_i} \lambda_{ji}$, so one backward pass per document replaces one per pair.

**Listwise.**

- *LambdaRank* (Burges, Ragno and Le 2006): skip the cost and define the gradient directly, $\lambda_{ij} = \frac{-\sigma}{1 + e^{\sigma(s_i - s_j)}} \lvert \Delta \mathrm{NDCG}_{ij} \rvert$, where $\Delta \mathrm{NDCG}_{ij}$ is the change of NDCG when documents $i$ and $j$ swap ranks in the current sorted list. Pairs that move a relevant document across the top positions get the largest weights. Burges (2010) reports empirical evidence that this optimizes NDCG directly; there is no general proof.
- *LambdaMART* (Wu, Burges, Svore and Gao 2010): [gradient boosting](/gradient-boosting/) with regression trees (MART), where each new tree fits the $\lambda_i$ as pseudo-residuals and each leaf takes a Newton step. It is the standard strong baseline for feature-based ranking and is built into the main boosting libraries.
- *ListNet* (Cao et al. 2007): turn the scores into the top one probabilities $P_s(j) = e^{s_j} / \sum_k e^{s_k}$, do the same with the labels, and minimize the cross entropy $-\sum_j P_y(j) \log P_s(j)$, which is a [softmax](/softmax-regression/) loss per query. ListMLE maximizes the Plackett-Luce likelihood of the ideal permutation instead.

The implementation on this page has NDCG@k with both gains, linear RankNet with the factorized lambdas, LambdaRank weights, full-batch gradient descent, and the ListNet top one loss and gradient. The tests check NDCG on the hand-worked lists above, the RankNet and ListNet gradients against central finite differences, and the LambdaRank weights against recomputed swaps. With the step $1/L$, where $L = \frac{\sigma^2}{4} \sum_{\text{pairs}} \lVert x_i - x_j \rVert^2$ bounds the curvature of the convex RankNet cost, every step of gradient descent lowers the cost or leaves it the same.

## Bounds

- **Cost of the measures.** NDCG@k of a list of $m$ documents costs $O(m \log m)$ for the sort, or $O(m + k \log k)$ with [selection](/quickselect/). The number of misordered pairs costs $O(m \log m)$ by [counting inversions](/counting-inversions/).
- **Cost of the pairwise gradients.** A query has up to about $m^2/2$ preferred pairs. RankNet and LambdaRank cost $O(m^2)$ per query for the $\lambda_{ij}$, plus $O(m d)$ for the linear gradient with the factorization, against $O(m^2 d)$ without it. LambdaRank also sorts the scores, $O(m \log m)$.
- **Bayes optimal ranking.** For one query with feature vectors fixed, the expected DCG of a permutation $\pi$ is $\sum_i D_i\, \mathbb{E}[2^{y_{\pi(i)}} - 1]$ with decreasing discounts $D_i$. By the rearrangement inequality, sorting by the expected gain $\mathbb{E}[2^{y} - 1 \mid x]$ maximizes it. Sorting by $\mathbb{E}[y \mid x]$ is not enough in general: with labels in $\{0, 2\}$ versus a sure label 1, the expected labels can tie while the expected gains differ. For expected NDCG, sort by $\mathbb{E}\big[(2^{y_i} - 1) / \mathrm{IDCG}\big]$, because the normalizer depends on all the labels of the query.
- **No useful gradient.** As a function of the scores, NDCG is constant except where two scores cross, so its gradient is 0 almost everywhere. This is why all the methods above use surrogates or defined gradients.
- **Hardness.** Minimizing the number of misordered pairs over linear scorers is NP-hard, because it contains agnostic [halfspace learning](/halfspace-learning/) (see Reductions). Convex pairwise losses such as the RankNet and Ranking SVM costs avoid this, at the price of optimizing a different objective.

## Reductions

- **Pairwise ranking to binary classification.** Each pair $(i, j)$ with $y_i > y_j$ becomes the example $x_i - x_j$ with label $+1$. A linear scorer orders the pair correctly exactly when $w^{\top}(x_i - x_j) > 0$. This is how Ranking SVM and RankNet reuse a classifier and its loss.
- **Halfspace learning to pairwise ranking.** In the other direction, a labeled point $(z, \pm 1)$ becomes a query with two documents, $z$ and $0$, and the label decides which is more relevant. A linear scorer misorders the pair exactly when the halfspace through the origin misclassifies $z$, so an algorithm that minimizes misordered pairs also minimizes the classification error.
- **Ranking to sorting.** At prediction time a scorer reduces ranking to sorting the $m$ scores, $O(m \log m)$ comparisons. Methods that output preferences between pairs without a score face [feedback arc set](/feedback-arc-set-problem/) problems when the preferences contain cycles.

## Applications

- **Web and enterprise search.** A first stage retrieves candidates with an [inverted index](/inverted-index/) and a cheap score such as BM25. A learned ranker then reorders the top few hundred with hundreds of features, including text match scores, link scores such as [PageRank](/pagerank/), freshness and click statistics. LambdaMART models were part of the winning entry of the 2010 Yahoo! Learning to Rank Challenge.
- **Product search, recommendation and advertising.** Items are ranked for a user or a session, often with listwise or pairwise losses on implicit feedback.
- **Question answering and retrieval for language models.** Neural rerankers order retrieved passages, often trained with listwise softmax losses.
- **Other reranking tasks.** Machine translation and speech recognition rerank n-best lists of candidate outputs, and [structured prediction](/structured-prediction/) uses the same idea to score candidate structures.

## References
