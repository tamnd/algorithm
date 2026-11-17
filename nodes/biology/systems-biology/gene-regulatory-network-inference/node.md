---
tag: CAPYJC
kind: problem
slug: gene-regulatory-network-inference
name: Gene regulatory network inference
aliases:
- network reverse engineering
area: biology/systems-biology
level: core
summary: "Infer which genes regulate which from expression data across conditions, time points or perturbations. Not identifiable without assumptions; methods are scored on benchmarks."
prereqs: [gene-regulatory-network, precision-and-recall]
see_also: [aracne, genie3, gaussian-graphical-model, bayesian-network-structure-learning, dynamic-bayesian-network, granger-causality, pc-algorithm, lasso-regression]
sources:
  - paper: doi:10.1038/nmeth.2016
    title: Daniel Marbach, James C. Costello, Robert Küffner, Nicole M. Vega, Robert J. Prill, Diogo M. Camacho, Kyle R. Allison, the DREAM5 Consortium, Manolis Kellis, James J. Collins and Gustavo Stolovitzky, Wisdom of crowds for robust gene network inference, Nature Methods 9(8), 796-804, 2012
    locator: the DREAM5 network inference challenge, its scoring by AUPR and AUROC, and the community network
  - paper: doi:10.1371/journal.pbio.0050008
    title: Jeremiah J. Faith, Boris Hayete, Joshua T. Thaden, Ilaria Mogno, Jamey Wierzbowski, Guillaume Cottarel, Simon Kasif, James J. Collins and Timothy S. Gardner, Large-scale mapping and validation of Escherichia coli transcriptional regulation from a compendium of expression profiles, PLoS Biology 5(1), e8, 2007
    locator: the CLR method and its validation against known E. coli regulation
  - paper: doi:10.1089/106652700750050961
    title: Nir Friedman, Michal Linial, Iftach Nachman and Dana Pe'er, Using Bayesian networks to analyze expression data, Journal of Computational Biology 7(3-4), 601-620, 2000
    locator: Bayesian networks learned from expression data, with features scored by the bootstrap
  - paper: doi:10.1126/science.1081900
    title: Timothy S. Gardner, Diego di Bernardo, David Lorenz and James J. Collins, Inferring genetic networks and identifying compound mode of action via expression profiling, Science 301(5629), 102-105, 2003
    locator: a linear model at steady state fitted to perturbation experiments
  - paper: doi:10.1007/978-1-4612-2404-4_12
    title: David Maxwell Chickering, Learning Bayesian networks is NP-complete, Learning from Data, Lecture Notes in Statistics 112, 121-130, 1996
    locator: the NP-completeness of finding a best scoring Bayesian network
  - paper: "Thomas Verma and Judea Pearl, Equivalence and synthesis of causal models, Proceedings of the Sixth Conference on Uncertainty in Artificial Intelligence, 1990"
    title: Thomas Verma and Judea Pearl, Equivalence and synthesis of causal models, 1990
    locator: the result that two directed acyclic graphs give the same independences when they have the same skeleton and the same colliders
---

Gene regulatory network inference asks for the edges of a [gene regulatory network](/gene-regulatory-network/), which transcription factors regulate which genes, from measurements of gene expression. The input is a matrix of expression levels of $m$ genes in $n$ samples, which can be different conditions, time points, or experiments in which genes are knocked out or overexpressed. The output is a list of edges, usually ranked by a confidence score, sometimes with a direction and a sign. The problem is not identifiable from expression data alone: different networks explain the same data, so every method adds assumptions, and methods are compared by how well their ranked lists recover known edges on benchmarks. [ARACNE](/aracne/) and [GENIE3](/genie3/) are two algorithms for it. The model itself is described on the gene regulatory network page, and the opposite direction, from a known network to its long run behavior, is [Boolean network attractor detection](/boolean-network-attractor-detection/).

## In plain words

A cell turns genes on and off with proteins made by other genes. We can measure how active each gene is, in many samples, but we cannot see directly who controls whom. The task is to guess the control links from the measurements.

The guess is hard for three reasons. Two genes can rise and fall together because one controls the other, or because a third gene controls both. A pattern of the data often fits a link in either direction equally well. And there are many more possible links than samples. So each method picks a rule, such as "keep the strongest links and remove those explained by a path through a third gene", and its output is a ranked list of likely links, not a proof.

## Definition

**Input.** An expression matrix $X \in \mathbb{R}^{n \times m}$, where $X_{s g}$ is the level of gene $g$ in sample $s$. Optional extra input: the list of genes that code for transcription factors (the candidate regulators), the time of each sample, and for each sample the genes that were perturbed.

**Output.** A score $w_{ij} \ge 0$ for each ordered pair of a regulator $i$ and a target $j \neq i$, or for each unordered pair if the method gives no direction. A cutoff on the scores, or the top $k$ pairs, gives a network.

**Scoring.** On a benchmark with a gold standard set $G$ of true edges, the ranked list is scored by [precision and recall](/precision-and-recall/) at each cutoff, summarized as the area under the precision recall curve (AUPR), and by the area under the ROC curve (AUROC). The AUROC is the probability that a random true edge is ranked above a random non-edge. Since only a small fraction of all pairs are true edges, the AUPR is the more sensitive of the two.

**The statistical model behind the problem.** Most methods assume that the data come from a model in which each gene's level is a function of its regulators' levels plus noise, for example a structural equation $x_j = f_j(x_{\mathrm{pa}(j)}) + \varepsilon_j$, where $\mathrm{pa}(j)$ is the set of regulators of $j$. The goal is the sets $\mathrm{pa}(j)$. With this model, inference is a form of [Bayesian network structure learning](/bayesian-network-structure-learning/) when the graph is acyclic.

## Variants

- **Steady state or time series.** Steady state data from many conditions give associations only. Time series allow a model in which the levels at time $t + 1$ depend on those at time $t$, as in a [dynamic Bayesian network](/dynamic-bayesian-network/) or a [Granger causality](/granger-causality/) test; such a model allows cycles, which real networks have.
- **Observational or interventional.** Data from knockouts, knockdowns or overexpression of chosen genes break the symmetries that make directions unidentifiable.
- **Undirected or directed, unsigned or signed.** Co-expression and mutual information methods give undirected edges; regression methods with a list of regulators give directed edges; linear models give a sign.
- **With prior knowledge.** Binding motifs, ChIP data or known edges restrict the candidate regulators of each gene.
- **Single cell data.** Many cells per sample, with many zero counts and no time labels, which changes the noise model but not the problem.

## Examples

**A chain of three genes.** Let $X \to Y \to Z$ with linear Gaussian equations scaled to unit variance: $X \sim N(0, 1)$, $Y = 0.8 X + 0.6 \varepsilon_Y$ and $Z = 0.8 Y + 0.6 \varepsilon_Z$, with independent standard normal noise. Then $\mathrm{corr}(X, Y) = \mathrm{corr}(Y, Z) = 0.8$ and $\mathrm{corr}(X, Z) = 0.64$. For Gaussian pairs the mutual information is $-\frac12 \ln(1 - \rho^2)$, which is about $0.511$ nats for the two true edges and $0.264$ nats for the indirect pair.

- A *relevance network*, which keeps all pairs with mutual information above a threshold, keeps the false edge $X$ to $Z$ for any threshold below $0.264$.
- ARACNE looks at the triangle and deletes its weakest edge, $X$ to $Z$, and returns the correct skeleton.
- The partial correlation of $X$ and $Z$ given $Y$ is $(0.64 - 0.8 \cdot 0.8) / (1 - 0.8^2) = 0$, so a [Gaussian graphical model](/gaussian-graphical-model/) also returns the correct skeleton.

None of these finds the directions, and the next result shows that no method can, from these data.

**Three networks with the same data (theorem).** The chain $X \to Y \to Z$, the reversed chain $Z \to Y \to X$ and the fork $X \leftarrow Y \to Z$, each with linear Gaussian equations, give the same set of joint distributions of $(X, Y, Z)$: all centered Gaussians in which $X$ and $Z$ are independent given $Y$.

*Proof.* A centered Gaussian vector is fixed by its covariance matrix. Each of the three models makes $X$ and $Z$ independent given $Y$, since $Z$ depends on $X$ only through $Y$ in the chains, and $X$ and $Z$ have independent noise given $Y$ in the fork. Conversely, take any centered Gaussian with $X$ and $Z$ independent given $Y$. Its law factors as $p(y) p(x \mid y) p(z \mid y)$, which is the fork, with linear Gaussian conditionals; it also factors as $p(x) p(y \mid x) p(z \mid y)$ and as $p(z) p(y \mid z) p(x \mid y)$, which are the two chains. So each model reaches every such law. $\square$

The collider $X \to Y \leftarrow Z$ differs, since it makes $X$ and $Z$ independent without conditioning. In general, two acyclic networks give the same conditional independences when they have the same skeleton and the same colliders (Verma and Pearl 1990), and conditional independences are all that observational data reveal without more assumptions.

**A knockout breaks the symmetry.** In the chain, fix $Y$ by an intervention. Then $Z$ follows the forced value of $Y$ and $X$ does not. The reversed chain predicts the opposite, and the fork predicts that both follow, so the three networks are now told apart.

## Known algorithms

All methods below are heuristics for the real problem: each is exact only under its own model and with exact statistics, and its accuracy on real data is a measurement on benchmarks.

- **Correlation and relevance networks.** Score each pair by correlation or mutual information. This finds direct and indirect links alike.
- **Mutual information with pruning.** [ARACNE](/aracne/) removes the weakest edge of each triangle by the data processing inequality. CLR (Faith et al. 2007) converts each mutual information value to a z-score against the background of the two genes involved.
- **Regression per target.** For each gene, predict its level from the levels of the candidate regulators and score each regulator by its weight in the model. [GENIE3](/genie3/) uses the variable importance of a [random forest](/random-forest/); sparse linear models use the [lasso](/lasso-regression/).
- **Gaussian graphical models.** Estimate the inverse covariance matrix, usually with a sparsity penalty; a zero entry means conditional independence given all other genes.
- **Bayesian networks.** Search for a directed acyclic graph with a high score, as in Friedman et al. (2000), or test conditional independences, as in the [PC algorithm](/pc-algorithm/). The result is a class of equivalent graphs, not one graph.
- **Dynamic models.** [Dynamic Bayesian networks](/dynamic-bayesian-network/), Granger tests and fitted differential equations use time series and allow cycles.
- **Perturbation models.** Gardner et al. (2003) fitted a linear model at steady state, $A x + u = 0$, to experiments with known perturbations $u$, with a bound on the number of regulators of each gene.
- **Consensus.** Average the ranks that several methods give each edge.

## Bounds

**Directions are not identifiable from observational data (theorem).** Without assumptions beyond an acyclic structural model, the data determine at most the equivalence class of the network, by the example above and the Verma and Pearl result. Linear models with non-Gaussian noise, or nonlinear models with additive noise, can identify more, but those are further assumptions.

**Interventions identify a linear network (theorem).** Assume the linear steady state model $A x + u = 0$ with an unknown $m \times m$ matrix $A$, and $m$ experiments with known perturbations $u^{(1)}, \ldots, u^{(m)}$ and measured responses $x^{(1)}, \ldots, x^{(m)}$. If the response matrix $X = [x^{(1)} \cdots x^{(m)}]$ is invertible, then $A = -U X^{-1}$ with $U = [u^{(1)} \cdots u^{(m)}]$. *Proof.* The model gives $A X = -U$, and multiplying by $X^{-1}$ on the right gives the formula; any other matrix $A'$ with $A' X = -U$ equals $A$ for the same reason. $\square$ With noise or fewer than $m$ experiments, the formula becomes a regression, and sparsity of $A$ is needed.

**Best scoring networks are hard to find (theorem).** Finding a Bayesian network with the best Bayesian score, when each node may have at most two parents, is NP-complete (Chickering 1996). So score based methods use local search and give no guarantee of optimality.

**Benchmark accuracy (measurement).** A data set with thousands of genes has millions of candidate pairs and usually far fewer samples. In the DREAM5 challenge (Marbach et al. 2012), the methods recovered the edges of the in silico network and of E. coli well above chance, but scored low on S. cerevisiae. No single method was best on all data sets, and a community network built by averaging the ranks of many methods was more robust than any single method.

## Reductions

- **To feature selection.** With directed edges from known regulators, inference splits into $m$ independent [feature selection](/feature-selection/) problems, one per target: which regulators predict the target. GENIE3 and the lasso methods use this.
- **To undirected graph estimation.** Under a Gaussian model, the undirected skeleton is the support of the inverse covariance matrix.
- **From structure learning.** Learning a Bayesian network from data with a given score is a special case, so inference with a Bayesian score inherits its NP-hardness.
- **To regression on time series.** With time series, the edges into gene $j$ are the variables that predict $x_j(t + 1)$ from $x(t)$, so each target again gives one regression.

## Applications

- **Finding the regulators of a process.** Rank the transcription factors that most likely control the genes of a disease or of a cell type, as candidates for experiments.
- **Mode of action of a drug.** Gardner et al. (2003) used the fitted network to find which genes a compound acts on from the response it causes.
- **Building models.** An inferred network gives the wiring for a Boolean or differential equation model of a [gene regulatory network](/gene-regulatory-network/), whose dynamics can then be studied.
- **Comparing conditions.** Networks inferred in two conditions show which regulatory links change.

## References
