---
tag: NVTX2V
kind: algorithm
slug: genie3
name: GENIE3
aliases:
- tree-based network inference
- gene network inference with ensemble of trees
area: biology/systems-biology
level: research
summary: For each gene, fit a random forest that predicts it from the other genes, and rank the links from regulator to target by the importance of the regulator.
solves: [gene-regulatory-network-inference]
model: real-ram
complexity:
  vars: {m: the number of genes, n: the number of samples, T: the number of trees per target, K: the number of inputs tried at each node}
  time: {worst: O(m T K n^2 log n)}
  space: {extra: Θ(m^2 + m n)}
properties: {deterministic: false, exact: false, online: false, recursive: true}
history:
  year: 2010
  people: [Vân Anh Huynh-Thu, Alexandre Irrthum, Louis Wehenkel, Pierre Geurts]
  note: Huynh-Thu, Irrthum, Wehenkel and Geurts published GENIE3 in PLoS ONE in 2010; it was the best method in the DREAM4 In Silico Size 100 Multifactorial challenge.
prereqs: [gene-regulatory-network-inference, cart, random-forest]
see_also: [aracne, decision-tree, bagging, gradient-boosting, variance, gene-regulatory-network, dynamic-bayesian-network, precision-and-recall]
sources:
  - paper: doi:10.1371/journal.pone.0012776
    title: Vân Anh Huynh-Thu, Alexandre Irrthum, Louis Wehenkel and Pierre Geurts, Inferring regulatory networks from expression data using tree-based methods, PLoS ONE 5(9), e12776, 2010
    locator: the method section (one regression problem per gene, unit variance outputs, Random Forests and Extra-Trees, the variance reduction importance), the complexity discussion and the DREAM4 results
  - paper: doi:10.1023/A:1010933404324
    title: Leo Breiman, Random forests, Machine Learning 45(1), 5-32, 2001
    locator: random forests for regression and the importance of the input variables
  - paper: doi:10.1007/s10994-006-6226-1
    title: Pierre Geurts, Damien Ernst and Louis Wehenkel, Extremely randomized trees, Machine Learning 63(1), 3-42, 2006
    locator: the Extra-Trees algorithm, with random cut points
  - paper: doi:10.1038/nmeth.2016
    title: Daniel Marbach et al., Wisdom of crowds for robust gene network inference, Nature Methods 9(8), 2012
    locator: the DREAM5 comparison of network inference methods, in which GENIE3 is among the best regression methods
  - paper: doi:10.1093/bioinformatics/bty916
    title: Thomas Moerman, Sara Aibar Santos, Carmen Bravo González-Blas, Jaak Simm, Yves Moreau, Jan Aerts and Stein Aerts, GRNBoost2 and Arboreto, efficient and scalable inference of gene regulatory networks, Bioinformatics 35(12), 2159-2161, 2019
    locator: GRNBoost2, the gradient boosting variant of the GENIE3 scheme
  - paper: doi:10.1038/s41598-018-21715-0
    title: Vân Anh Huynh-Thu and Pierre Geurts, dynGENIE3, dynamical GENIE3 for the inference of gene networks from time series expression data, Scientific Reports 8, 3384, 2018
    locator: the extension of GENIE3 to time series data
---

GENIE3 turns [gene regulatory network inference](/gene-regulatory-network-inference/) into $m$ regression problems, one for each of the $m$ genes. For a target gene $j$, it fits a [random forest](/random-forest/) of regression trees that predicts the expression of $j$ from the expression of the candidate regulators, and it scores each regulator $i$ by how much the splits on $i$ reduce the squared error of the trees. The score $w_{ij}$ is the weight of the directed link from $i$ to $j$, and the output is the list of all links sorted by weight. Trees catch nonlinear effects and interactions of regulators, which a correlation misses. GENIE3 is a heuristic: it has no guarantee that the top links are the true ones, and its results on a data set are measurements. The code of this page is a small version of the method: it keeps the Random Forest trees, grown to full depth, and the variance reduction importance, and it leaves out the Extra-Trees variant, the default of 1000 trees per target and the parallel runs over the targets.

## In plain words

Pick one gene and try to predict its level in each sample from the levels of all the other genes. A regression tree does this by asking yes or no questions such as "is gene A above some value?", and each question splits the samples into two groups whose levels are more alike. A question that makes the groups much more alike is a useful question, and the gene it asks about gets credit for it.

Grow many such trees, each on a random sample of the data and with a random choice of genes to ask about at each step, and add up the credit of each gene. Genes with a lot of credit are good predictors of the chosen gene, so they are candidate regulators. Do this for every gene in turn and sort all the links by their credit.

## The problem

**Input.** An expression matrix with $m$ genes and $n$ samples, $x_{g s}$; optionally a list of candidate regulators, for example the known transcription factors; the number $T$ of trees per target and the number $K$ of inputs tried at each node.

**Output.** A list of directed links $(i, j)$, $i \neq j$, $i$ a candidate regulator, with weights $w_{ij} \ge 0$, sorted by decreasing weight. A user cuts the list at some rank to get a network. GENIE3 gives no sign and no threshold.

For a set $S$ of samples (with repeats) and the target values $y_s$, write $\mathrm{SS}(S) = \sum_{s \in S} (y_s - \bar y_S)^2 = |S| \cdot \mathrm{Var}(S)$ for the sum of squares about the mean of $S$. A split of $S$ on input $i$ at threshold $t$ sends the samples with $x_{i s} \le t$ to the left part $S_L$ and the others to $S_R$. Its *reduction* is

$$\Delta = \mathrm{SS}(S) - \mathrm{SS}(S_L) - \mathrm{SS}(S_R) = \frac{\sigma_L^2}{|S_L|} + \frac{\sigma_R^2}{|S_R|} - \frac{\sigma^2}{|S|},$$

where $\sigma$, $\sigma_L$ and $\sigma_R$ are the sums of $y$ over $S$, $S_L$ and $S_R$. This is the quantity $\#S \cdot \mathrm{Var}(S) - \#S_t \cdot \mathrm{Var}(S_t) - \#S_f \cdot \mathrm{Var}(S_f)$ of the paper. The importance of input $i$ in one tree is the sum of $\Delta$ over all nodes of the tree that split on $i$.

## The algorithm

```pseudo id=main
GENIE3(X, T, K)
L1  for each target gene j do
L2      y ← row j of X divided by its standard deviation; inputs ← the candidate regulators other than j
L3      for t ← 1 to T do
L4          S ← n samples drawn with replacement from the n samples
L5          grow a regression tree on S; at each node, draw K inputs at random and take the split with the largest reduction Δ
L6          for each node that splits on input i do w[i, j] ← w[i, j] + Δ / T
L7  sort all pairs (i, j) by w[i, j], largest first
L8  return the sorted list
```

Line L2 scales each target to unit variance. Without it, a target with a large variance would give large reductions and would fill the top of the list. Line L4 is the bootstrap sample of a random forest. Line L5 grows the tree to full depth: a node is a leaf when its target values are all equal or no input takes two values on it. For one input, the best threshold comes from one sort of the node's samples by that input and one pass with running sums, which gives $\Delta$ for every cut between two distinct values. Line L6 adds the reductions to the weights as the tree grows. The paper uses $T = 1000$ and $K = \sqrt{p}$ or $K = p$ for $p$ candidate inputs, and also an Extra-Trees variant in which line L5 draws the cut point at random.

## Example

Take three genes A, B and C and four samples, with C as the target. Let A take the values 1, 2, 3, 4, let B take the values 4, 1, 4, 1, and let C take the values 0, 2, 1, 3. So C is 2 when B is low, plus 1 when A is high. The mean of C is 1.5 and $\mathrm{SS} = 2.25 + 0.25 + 0.25 + 2.25 = 5$, so $\mathrm{Var} = 1.25$; scaling divides by $\sqrt{1.25}$, which multiplies every sum of squares by $0.8$. The steps below use the raw values and scale at the end. Use all samples once (no bootstrap) and $K = 2$.

At the root, the cuts on A give, from left to right, reductions $0 + 36/3 - 9 = 3$, $4/2 + 16/2 - 9 = 1$ and $9/3 + 9/1 - 9 = 3$. The only cut on B separates the samples with B = 1 (C values 2 and 3) from those with B = 4 (C values 0 and 1), with reduction $25/2 + 1/2 - 9 = 4$. So the root splits on B with $\Delta = 4$. Each child has two samples with equal B and different A, and the split on A gives $\Delta = 0.5$ in each. All four leaves are pure. The raw importances are 4 for B and 1 for A, and after scaling $w_{BC} = 3.2$ and $w_{AC} = 0.8$. They add up to $4 = n$, as the theorem below says for a fully grown tree.

**On simulated data.** The test of the implementation uses 6 genes and 100 samples (seed 1). Genes 0, 1 and 2 are independent normal regulators. Gene 3 is $\tanh(2 x_0)$ plus noise, gene 4 is $x_2$ when $x_1 > 0$ and 0 otherwise, plus noise, and gene 5 is $x_2^2$ plus noise, each with noise of standard deviation 0.3. With genes 0, 1 and 2 as candidate regulators there are 15 candidate links, 4 of them true. With $T = 30$ trees and $K = 2$, the top 4 links contain 3 true links, and the area under the ROC curve is $38/44 = 0.864$. The link from 2 to 5 is second. Ranking by the absolute Pearson correlation gives an area of $34/44 = 0.773$ and puts the link from 2 to 5 sixth, because $x_2^2$ is not correlated with $x_2$. The link from 1 to 4 is tenth: gene 1 acts only as a switch for gene 2, and it gets less weight than the links between the free regulators. This is one measurement, not a guarantee.

## Correctness

GENIE3 is a heuristic, so the claims here are about what the code computes, not about recovery of the true network.

**Theorem.** (a) For each node and each tried input, line L5 finds the threshold with the largest reduction $\Delta$. (b) In each tree, the importances of all inputs add up to $\mathrm{SS}(S) - \sum_{\text{leaves } \ell} \mathrm{SS}(\ell)$. If every leaf is pure, they add up to $\mathrm{SS}(S)$; with no bootstrap this is $n$, since $y$ has unit variance, and with a bootstrap sample its expected value is $n - 1$. (c) The weights do not change when an input gene is replaced by a strictly increasing function of itself, for the same random draws.

Part (a) holds because a threshold split depends only on the position of the cut in the sorted order of the input, and the sweep visits every cut between two distinct values. Part (b) holds because each split replaces $\mathrm{SS}$ of a node by the sum of $\mathrm{SS}$ of its children, so the reductions telescope from the root to the leaves. Part (c) holds because a strictly increasing map keeps the sorted order and the ties of the input, so every node sees the same set of cuts with the same reductions. The proof file gives the details.

Part (b) has a practical consequence. With fully grown trees and continuous data, every target gives a total weight of about $n$ to its inputs, whether it has a regulator or not. A target with no regulator spreads that weight over its inputs, and some of these false links can rank above weak true links, as in the example above.

## Complexity

The model is the real RAM. At a node with $s$ samples, each of the $K$ tried inputs costs a sort, $O(s \log s)$, and a pass, $O(s)$. The nodes of one depth of a tree hold at most $n$ samples in all, so one depth costs $O(K n \log n)$. A tree of depth $d$ costs $O(d K n \log n)$, and $d \le n$. So one target costs $O(T K n^2 \log n)$ in the worst case and all targets $O(m T K n^2 \log n)$. For balanced trees, $d = O(\log n)$ and the cost is $O(m T K n \log^2 n)$; presorting each input once per tree removes one $\log n$ factor. Huynh-Thu et al. describe the cost as nearly linear in the number of samples, and at most quadratic in the number of genes when $K$ grows with the number of genes. The weights take $\Theta(m^2)$ space, the data $\Theta(m n)$, and one tree $O(n)$. The targets are independent, so they can run in parallel.

## Properties

- **Randomized.** The bootstrap samples and the inputs tried at each node are random, so the weights change with the seed. A larger $T$ makes them more stable.
- **Directed, unsigned.** A link from $i$ to $j$ means that $i$ helps to predict $j$. It does not say whether $i$ activates or represses $j$, and for two genes that both are candidates the two directions get separate weights that are often similar.
- **Invariant to increasing transforms of the inputs.** Splits depend only on the order of each input, so a log transform of the inputs changes nothing. The targets are scaled, but not transformed, so a transform of a target does change its weights.
- **Nonlinear.** Trees fit thresholds and interactions, so a regulator that acts only above some level, or only together with another regulator, can still get weight.

## Variants and improvements

- **Extra-Trees.** Geurts, Ernst and Wehenkel (2006) draw one random cut point for each tried input instead of the best one. Huynh-Thu et al. report results for both tree methods.
- **Known regulators.** Restrict the inputs to the transcription factors. This removes the links between targets and most of the links into genes that have no regulator in the list.
- **GRNBoost2.** Moerman et al. (2019) replace the forest by gradient boosting with early stopping, which is much faster on large single cell data sets, and keep the same scheme of one regression per gene.
- **Time series.** dynGENIE3 (Huynh-Thu and Geurts 2018) predicts the rate of change of a target from the levels of the regulators, with a model of decay, so that the time order of the samples is used.
- **Other regression scores.** Any method that gives an importance per input fits the same scheme, for example a sparse linear regression per target. DREAM5 (Marbach et al. 2012) found that the best regression methods, GENIE3 among them, were among the strongest single methods, and that an average of the ranks of many methods was more robust than any single one.

## When to use it

Use GENIE3 for steady state expression data from many conditions, when you want a ranked list of candidate regulators for each target and the effects may be nonlinear. It needs no assumption on the form of the effects and no discretization of the data. Prefer [ARACNE](/aracne/) when you want an undirected, sparse network with a clear rule for removing indirect links, a sparse linear model when the number of samples is small, and a [dynamic Bayesian network](/dynamic-bayesian-network/) or dynGENIE3 when the data is a time series.

## Pitfalls

- **Correlated regulators share weight.** If two regulators carry the same information, the trees use one or the other at random, and each gets about half the weight. Neither may reach the top of the list.
- **Every target gives out the same total.** With full trees the weights into each target add up to about $n$, so the links into an unregulated gene look as strong as real links. Restrict the inputs to known regulators where possible.
- **The top of the list is not a network.** The output is a ranking. A cut at some rank is a choice of the user, and the paper scores the whole ranking by the areas under the ROC and the precision and recall curves.
- **Direction is weak evidence.** For two genes that are both candidates, the weights of the two directions are similar, and a large difference is not proof of the direction of control.
- **Random seed.** With few trees, the order of links with close weights changes from seed to seed. Report the seed and use enough trees.

## Implementations

## History

Breiman introduced random forests and their variable importance in 2001, and Geurts, Ernst and Wehenkel introduced Extra-Trees in 2006. Huynh-Thu, Irrthum, Wehenkel and Geurts applied tree ensembles to network inference as GENIE3 in 2010, and GENIE3 was the best method in the DREAM4 In Silico Size 100 Multifactorial challenge. It was also one of the top methods in DREAM5. Huynh-Thu and Geurts extended it to time series as dynGENIE3 in 2018, and Moerman et al. published the faster GRNBoost2 in 2019.

## References
