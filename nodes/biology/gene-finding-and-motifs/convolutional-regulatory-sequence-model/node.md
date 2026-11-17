---
tag: HDHDBW
kind: model
slug: convolutional-regulatory-sequence-model
name: Convolutional regulatory sequence model
aliases:
- DeepSEA
- DeepBind
area: biology/gene-finding-and-motifs
level: research
summary: A convolutional network whose first-layer filters act as learned weight matrices, trained to predict binding or chromatin marks from DNA.
prereqs: [position-specific-scoring-matrix, logistic-regression, backpropagation]
see_also: [convolution, relu, dropout, cross-entropy-loss, roc-auc, stochastic-gradient-descent, sequence-logo, phylogenetic-footprinting]
sources:
  - paper: doi:10.1038/nbt.3300
    title: Babak Alipanahi, Andrew Delong, Matthew T. Weirauch and Brendan J. Frey, Predicting the sequence specificities of DNA- and RNA-binding proteins by deep learning, Nature Biotechnology 33(8), 2015
    locator: pp. 831 to 838; DeepBind, a convolutional model with motif detectors, rectification, pooling and a small neural network, trained on in vitro and in vivo binding data
  - paper: doi:10.1038/nmeth.3547
    title: Jian Zhou and Olga G. Troyanskaya, Predicting effects of noncoding variants with deep learning-based sequence model, Nature Methods 12(10), 2015
    locator: pp. 931 to 934 and the online methods; DeepSEA, its input of 1000 bp, its 919 chromatin features, its three convolution layers, its training objective and regularization, and its test on held-out chromosomes
---

A convolutional regulatory sequence model is a model of the map from a DNA sequence to a regulatory signal, such as the binding of a transcription factor, an open chromatin site or a histone mark. It is a convolutional neural network: the first layer slides a set of learned filters along the one-hot coded sequence, and each filter computes exactly the score of a [position-specific scoring matrix](/position-specific-scoring-matrix/) at every position. Later layers combine the filter outputs into a prediction. DeepBind (Alipanahi, Delong, Weirauch and Frey 2015) and DeepSEA (Zhou and Troyanskaya 2015) are the two standard examples. The parameters are fit by gradient descent on measured data, and the accuracy of the model is a measurement on held-out data: there is no worst-case guarantee and no proof that the fitted model is the best one.

## The machine

### Input

A DNA sequence $x = x_1 \ldots x_L$ is coded as an $L \times 4$ matrix $X$ with $X_{i, b} = 1$ if $x_i = b$ and 0 otherwise, for $b \in \{A, C, G, T\}$. An unknown base N is often coded as $(0.25, 0.25, 0.25, 0.25)$ or as a row of zeros. The length $L$ is fixed for a given model: DeepSEA reads windows of 1000 bp.

### First layer: filters as weight matrices

The first layer has $F$ filters. Filter $f$ is a $w \times 4$ matrix $M^{(f)}$ and a bias $c_f$. Its output at position $i$ is

$$h_f(i) = \phi\Big(c_f + \sum_{p=1}^{w} \sum_{b} M^{(f)}_{p, b} \, X_{i + p - 1, b}\Big) = \phi\big(c_f + \mathrm{score}_{M^{(f)}}(x_i \ldots x_{i+w-1})\big),$$

where $\phi$ is the rectifier $\phi(z) = \max(0, z)$ ([ReLU](/relu/)). The second equality holds because each row of $X$ has a single 1: the double sum picks one weight per position, the weight of the base that is there. So the linear part of a first-layer filter is exactly the score of the weight matrix $M^{(f)}$ on the window, as a scoring matrix would compute it. This is a [convolution](/convolution/) of the sequence with the filter, in the cross-correlation form that neural network libraries use.

### Pooling

A pooling step takes the maximum (or the mean) of each filter output over windows of positions, or over the whole sequence. Max pooling over the whole sequence asks "does the motif occur anywhere, and how well"; pooling over short windows keeps a rough position, which later layers can use to find pairs of motifs at a given spacing.

### Deeper layers

DeepSEA stacks three convolution layers, with 320, 480 and 960 filters, with max pooling between them, then one fully connected layer with rectified units, and a sigmoid output layer with one unit for each of 919 chromatin features (690 transcription factor binding profiles, 125 DNase I hypersensitivity profiles and 104 histone mark profiles). The second and third layers read the outputs of the first, so they can respond to combinations of motifs and to their spacing. DeepBind is smaller: a layer of motif detectors, rectification, pooling, and a small neural network that gives one binding score for one protein, and it scans both strands of the sequence.

### Output and training objective

For $K$ binary features (bound or not, open or not) the output is $\hat{y}_k = \sigma(z_k)$, with the logistic function $\sigma(z) = 1 / (1 + e^{-z})$, and the loss is the [cross-entropy](/cross-entropy-loss/), the negative log likelihood of independent Bernoulli labels:

$$\mathcal{L}(\theta) = -\sum_{n} \sum_{k=1}^{K} \big( y_{n,k} \log \hat{y}_{n,k} + (1 - y_{n,k}) \log (1 - \hat{y}_{n,k}) \big) + R(\theta).$$

DeepSEA fits the 919 outputs together, so all features share the convolution layers. Its regularizer $R$ combines an L2 penalty on the weights, an L1 penalty on the outputs of the hidden layer, a max-norm limit on the weights and [dropout](/dropout/), and it trains by [stochastic gradient descent](/stochastic-gradient-descent/) with momentum. DeepBind uses a loss suited to each kind of data, for example a regression loss for the intensities of protein binding microarrays and a classification loss for ChIP-seq peaks against background. The gradients come from [backpropagation](/backpropagation/).

### A worked filter

Take one filter of width 4 for the site TGAC, with the log-odds weights $\log_2(0.7 / 0.25) = 1.485$ for the site base and $\log_2(0.1 / 0.25) = -1.322$ for the other three bases at each position, bias $c = -3$, a ReLU, max pooling over the sequence, and an output unit $\sigma(1.0 \cdot m - 1.0)$ on the pooled value $m$.

| sequence | window scores at positions 1 to 5 | pooled $m$ | output |
|---|---|---|---|
| AATGACGT | -5.288, -5.288, 5.942, -5.288, -5.288 | 2.942 | 0.875 |
| AATGTCGT | -5.288, -5.288, 3.134, -5.288, -2.480 | 0.134 | 0.296 |

The convolution of the one-hot matrix gives the same five numbers as the scoring matrix applied to each window. The best window TGAC scores $4 \cdot 1.485 = 5.942$. The change of A to T at position 5 of the sequence turns it into TGTC, which scores $3 \cdot 1.485 - 1.322 = 3.134$, and the output falls by 0.579. This difference between the outputs for two alleles is how such models score a variant (*in silico* mutagenesis). The reverse complement ACGTCATT has no window above 0.327, which is why models of double-stranded DNA either scan both strands or learn the reverse complement filters as well.

## What it counts

- **Parameters.** A first layer with $F$ filters of width $w$ has $4 w F + F$ parameters. A second convolution layer with $F'$ filters of width $w'$ over $F$ channels has $w' F F' + F'$, which grows with the product of the layer widths. The DeepSEA network has millions of parameters, most of them in the deeper layers and the fully connected layer.
- **Cost of one prediction.** In the real RAM, a convolution layer with $C$ input channels, $F$ filters of width $w$, on an input of length $L$, costs $O(L w C F)$ operations. Pooling divides the length of the next layer by the pooling width. One forward pass costs the sum over the layers, and training costs a constant times this per example and per epoch.
- **Scanning a genome.** Predicting at every position of a genome of length $G$ with windows of length $L$ costs $O(G)$ forward passes if each window is computed again, or close to the cost of one pass over the genome if the convolution outputs are shared between overlapping windows.
- **Accuracy.** Accuracy is counted on held-out data: the area under the [ROC curve](/roc-auc/) and the area under the precision-recall curve for each feature. DeepSEA held out chromosomes 8 and 9 for testing; its paper reports median ROC AUCs of 0.958 for transcription factor features, 0.923 for DNase features and 0.856 for histone marks (measurements on that test set). These numbers depend on how the negative examples are chosen; with many easy negatives, the ROC AUC is high even for weak models.

## Relation to other models

- **Position-specific scoring matrix.** A model with one filter, max pooling and a logistic output is a [logistic regression](/logistic-regression/) on the best PWM score in the sequence, with the PWM learned from the labels instead of from aligned sites. A trained first-layer filter can be shown as a [sequence logo](/sequence-logo/) after it is turned into a matrix of probabilities, and it is often compared with the known motifs of the protein.
- **Motif finding.** Classical [motif finding](/motif-finding-problem/) looks for an over-represented pattern in a set of sequences without labels on the background. A convolutional model learns patterns that separate labeled positives from negatives, many at once, and it can use patterns that are weak alone but strong together.
- **k-mer models.** Models that score a sequence by a weighted count of its $k$-mers (with gaps or mismatches) are linear in fixed features; a convolutional network learns its features. The two are often close in accuracy on single transcription factors, and the networks gain when combinations and spacing matter.
- **Conservation.** [Phylogenetic footprinting](/phylogenetic-footprinting/) finds sites from evolution without labels. A sequence model finds them from one genome with labels. The two are complementary: conservation can confirm a predicted site, and a sequence model can score sites that are specific to one species.
- **Probabilistic sequence models.** HMMs and their relatives model the probability of a sequence. A convolutional regulatory model is discriminative: it models the probability of a label given the sequence, and it does not give a probability for the sequence itself.

## Known results in the model

- **Filters are scoring matrices (a theorem).** On one-hot input, the linear part of a first-layer filter of width $w$ equals the score of a $w \times 4$ weight matrix on each window, plus the bias. Proof: each row of $X$ has one nonzero entry, equal to 1, so the inner product of the filter with a window picks one weight per position. With the weights set to log-odds, the filter is the log-likelihood ratio of a PWM against a background of independent bases.
- **One filter with a logistic output is a linear classifier of the best site score (a theorem).** With max pooling over the sequence and one output unit, the prediction is $\sigma(a \cdot \max(0, c + \max_i \mathrm{score}(i)) + d)$, a monotone function of the best window score. So such a model ranks sequences exactly as the best PWM hit does.
- **Training finds a local optimum (no guarantee).** The loss is not convex in the weights of a network with a hidden layer, and stochastic gradient descent gives no guarantee of a global minimum. Different random starts give different filters with similar accuracy.
- **No worst-case guarantee on predictions.** The model is fit to data, and its error on a new sequence has no bound. Its accuracy is known only on the held-out data it was measured on, and it may be much lower on cell types, species or kinds of sequence that the training data did not cover.
- **Measured results.** DeepBind reported, on benchmark data of protein binding microarrays and ChIP-seq, better accuracy than earlier motif-based methods for many proteins. DeepSEA reported the median AUCs given above and used *in silico* mutagenesis to score non-coding variants. Both are measurements under the settings of the papers.
- **Interpretation is approximate.** The filters of the first layer are often close to known motifs, but a filter can also capture part of a motif, or a motif of a co-binding factor. Scores of importance per base (gradients, mutagenesis) describe the fitted model, not the biology directly.

## References
