---
tag: VPHGA7
kind: problem
slug: truth-discovery
name: Truth discovery
aliases:
- data fusion
- resolving conflicts between sources
area: databases/data-integration-and-cleaning
level: advanced
summary: "Find the true value of each object from sources that conflict, and estimate how reliable each source is at the same time, without labels. A vote is the baseline."
model: word-ram
complexity:
  vars: {n: the number of claims, k: the number of iterations}
  time: {worst: "O(k n)"}
prereqs: [entity-resolution]
see_also: [truthfinder, expectation-maximization, maximum-likelihood-estimation, hits-algorithm, fixed-point-iteration, naive-bayes-classifier, bayes-theorem, logistic-regression]
sources:
  - paper: doi:10.1145/1281192.1281309
    title: "Xiaoxin Yin, Jiawei Han and Philip S. Yu, Truth discovery with multiple conflicting information providers on the web, Proceedings of the 13th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 2007, pages 1048 to 1052"
    locator: "the statement of the problem (websites, facts, objects and the trustworthiness of websites), Section 3 (TruthFinder), Section 4 (the book author data)"
  - paper: doi:10.1145/2897350.2897352
    title: "Yaliang Li and others, A survey on truth discovery, ACM SIGKDD Explorations Newsletter 17(2), 2015"
    locator: the general principle (reliable sources give true values more often), the families of methods, and the variants for numeric data, copying, long-tail sources and streams
  - paper: "Xin Luna Dong, Laure Berti-Equille and Divesh Srivastava, Integrating conflicting data: the role of source dependence, PVLDB 2(1), 2009, pages 550 to 561"
    locator: the accuracy model of sources and the detection of copying between sources
  - paper: "A. Philip Dawid and Allan M. Skene, Maximum likelihood estimation of observer error-rates using the EM algorithm, Journal of the Royal Statistical Society, Series C (Applied Statistics) 28(1), 1979, pages 20 to 28"
    locator: the latent class model of observers with error rates, fitted with EM
---

Truth discovery takes claims from many sources about the same objects, such as the authors of a book listed by many shops, and finds the true value of each object when the sources disagree and no labels are known. The main idea is a loop: a source that often gives the values that look true is reliable, and a value that reliable sources give looks true. So the problem asks for two unknowns at once, the truths and the reliability of each source. The page [TruthFinder](/truthfinder/) gives one algorithm in full, with its equations and code; this page states the problem, the baseline vote, the limits of what any method can know without labels, and the other families of methods. Truth discovery comes after [entity resolution](/entity-resolution/): the claims must first be grouped by the object they describe.

## In plain words

Ten web sites list the author of a book, and they give three different names. You could take the name that most sites give. But some sites are careful and others copy errors from each other, so counting is not enough. You want to give more weight to careful sites. You do not know which sites are careful, but you can guess: a site that agrees with the likely answers on many books is probably careful. Truth discovery methods turn this guess into a computation that finds the answers and the weights of the sites together.

## Definition

**Input.** A set $S$ of sources, a set $O$ of objects, and a set of claims $(s, o, v)$: source $s$ says that object $o$ has value $v$. Each source claims at most one value for an object, and covers only some objects. $n$ is the number of claims.

**Output.** For each object $o$ a value $v^*_o$, and for each source $s$ a reliability $w_s$, a number that says how often $s$ is right.

**Goal.** Make $v^*_o$ equal to the true value for as many objects as possible. The truth is not in the input, so this goal can be measured only on labelled objects. Each method fixes a model or a principle that turns the goal into something it can compute.

## Variants

- **Single truth or several.** Most methods assume one true value for each object. Lists such as the authors of a book can also be read as several true values.
- **Categorical or numeric.** For numbers, the output is a value that need not be claimed, and the loss is a distance.
- **Similar values.** Values such as "J. Smith" and "John Smith" can support each other, as in TruthFinder.
- **Copying sources.** Sources that copy from each other are not independent evidence, and some methods detect the copying.
- **Long tail.** Many sources make very few claims, so their reliability cannot be estimated well.
- **Streams.** Claims arrive over time, and the truths and reliabilities must be updated.
- **Crowdsourcing.** The sources are workers who label items, and the problem is to aggregate the labels.

## Examples

**Vote and weighted vote.** Three sources and three books, with values x, y:

| source | b1 | b2 | b3 |
|---|---|---|---|
| A | x | x | x |
| B | y | y | |
| C | | x | x |

The vote picks x for b2 and b3 and has a tie for b1. Source A agrees with the vote on b2 and b3, and B disagrees on b2, so a method that weights sources picks x for b1. TruthFinder does this, as its page shows step by step.

**A larger case.** On data generated as on the TruthFinder page (200 objects, 4 good sources and 20 poor ones that often share a wrong value, Python seed 42), the vote is right on 63% of the objects and TruthFinder on 73%. This is a measurement on that data.

## Known algorithms

- **Vote.** Take the value that most sources claim. It needs one pass, $O(n)$ time with a hash table, and treats all sources as equal.
- **Iterative methods.** [TruthFinder](/truthfinder/) computes the trust of each source from the confidence of its facts and the confidence from the trust, in a loop, with support between similar facts. Its loop of two scores that feed each other is like that of [HITS](/hits-algorithm/) for hubs and authorities. All are heuristics; their loop is a [fixed-point iteration](/fixed-point-iteration/) without a general proof of convergence.
- **Probabilistic models.** The latent class model of Dawid and Skene gives each source an error rate and fits the truths and the rates by [maximum likelihood](/maximum-likelihood-estimation/) with [expectation maximization](/expectation-maximization/). Dong, Berti-Equille and Srivastava add the probability that one source copies another. EM finds only a local maximum.
- **Optimization methods.** Write the problem as the minimization of a sum over sources of a weight times the loss of the source against the truths, with a constraint on the weights, and minimize it by turns over the truths and the weights.

## Bounds

**Without an assumption the truths cannot be identified.** *Theorem.* Take binary values $\{0, 1\}$, and a model in which source $s$ is right with probability $p_s$ on each object, independently. The model with truths $v^*$ and accuracies $p_s$ gives the same distribution of claims as the model with truths $1 - v^*$ and accuracies $1 - p_s$. *Proof.* In the first model, $s$ claims $1 - v^*_o$ with probability $1 - p_s$. In the second model, $s$ is right with probability $1 - p_s$, and the right value is $1 - v^*_o$. So every claim has the same probability in both models, and they are independent in both. $\square$ So no method can tell the two apart from the claims alone. Every method assumes something more, usually that most sources, or most of the weight, are better than random. TruthFinder, for example, starts with the trust 0.9 for every source.

**Cost.** Each claim must be read, so every method takes $\Omega(n)$ time. The iterative methods take $O(n)$ for each iteration when the similarity between values is not used, and the number of iterations $k$ is measured, not bounded.

## Reductions

**Known reliabilities give a weighted vote.** *Theorem.* Suppose each object has $m$ possible values, source $s$ is right with probability $p_s > 1/m$, it picks each wrong value with probability $(1 - p_s)/(m - 1)$, the sources are independent, and the prior on the true value is uniform. Then the most likely true value of $o$ is the one with the largest sum of the weights $\log \big( (m - 1) p_s / (1 - p_s) \big)$ over the sources that claim it. *Proof.* The probability of the claims on $o$ given the truth $v$ is $\prod_{s \text{ claims } v} p_s \cdot \prod_{s \text{ claims another}} (1 - p_s)/(m - 1)$. Divide by the value $\prod_{s} (1 - p_s)/(m - 1)$, which does not depend on $v$, and take logarithms. $\square$ This is the same sum as in a [naive Bayes classifier](/naive-bayes-classifier/), and by [Bayes' theorem](/bayes-theorem/) it gives the posterior when the prior is not uniform. So, once reliabilities are fixed, the truths are a weighted vote. The methods differ in how they estimate the reliabilities.

**To EM on a latent class model.** With the truths as hidden variables, the probabilistic form is a mixture model. Its E-step is the weighted vote above, and its M-step sets each $p_s$ to the expected fraction of claims of $s$ that are right.

**From entity resolution.** The input needs the claims grouped by object, which is the output of entity resolution on the records of the sources.

## Applications

- **Web data integration.** Book authors, flight times, stock data and other values that many web sites report differently.
- **Knowledge bases.** Choose the facts to keep when many extractors and sources give different values for the same property.
- **Crowdsourcing.** Combine the labels of many workers into one label for each item, with an error rate for each worker.
- **Sensor data.** Combine readings of the same quantity from sensors of different quality.

## References
