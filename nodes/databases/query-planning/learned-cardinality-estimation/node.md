---
tag: HAQH06
kind: technique
slug: learned-cardinality-estimation
name: Learned cardinality estimation
aliases:
- MSCN
- neural cardinality estimation
area: databases/query-planning
level: research
summary: "Train a model, on executed queries or on the data itself, to predict the result sizes of queries in place of histograms and independence. Its accuracy is measured, not proved."
prereqs: [cardinality-estimation, attribute-value-independence]
see_also: [learned-query-optimization, learned-index, bayesian-network, importance-sampling, estimation-error-propagation, pessimistic-cardinality-estimation, join-size-estimation-problem, count-min-sketch]
sources:
  - paper: "Andreas Kipf, Thomas Kipf, Bernhard Radke, Viktor Leis, Peter Boncz and Alfons Kemper, Learned cardinalities: estimating correlated joins with deep learning, Proceedings of CIDR 2019"
    title: "Learned cardinalities: estimating correlated joins with deep learning"
    locator: the multi-set convolutional network (MSCN), its featurization of tables, joins and predicates as sets, the sample bitmaps, and its evaluation on the IMDB data set
  - paper: doi:10.14778/3368289.3368294
    title: Zongheng Yang, Eric Liang, Amog Kamsetty, Chenggang Wu, Yan Duan, Xi Chen, Pieter Abbeel, Joseph M. Hellerstein, Sanjay Krishnan and Ion Stoica, Deep unsupervised cardinality estimation, Proceedings of the VLDB Endowment 13(3) (2019), 279 to 292
    locator: Naru, a deep autoregressive model of the joint distribution of a table, and progressive sampling (Monte Carlo integration) for range predicates
  - paper: doi:10.14778/2850583.2850594
    title: Viktor Leis, Andrey Gubichev, Atanas Mirchev, Peter Boncz, Alfons Kemper and Thomas Neumann, How good are query optimizers, really?, Proceedings of the VLDB Endowment 9(3) (2015), 204 to 215
    locator: Section 3 (the errors of traditional estimators on the Join Order Benchmark, the baseline that learned estimators try to beat)
---

Learned cardinality estimation replaces the histograms and the [independence assumption](/attribute-value-independence/) of a classic estimator with a model fitted by machine learning. There are two families. Query-driven models learn a function from a description of a query to its result size, from a training set of queries with their true sizes; MSCN of Kipf et al. (2019) is the best-known example. Data-driven models learn the joint distribution of the columns of a table, and compute the selectivity of a predicate as a probability under the model; Naru of Yang et al. (2019) uses a deep autoregressive model. Both capture correlations between columns that independence ignores. The gains are measured on benchmarks; no learned estimator has a proved error bound on all data. The general problem is on the [cardinality estimation](/cardinality-estimation/) page.

## In plain words

A classic database keeps a summary of each column and assumes that columns are unrelated. That assumption is often wrong, and then the guesses about result sizes are far too small.

A learned estimator studies the data or past queries instead. One kind looks at many example queries together with their true result sizes, and learns to guess the size of a new query from its tables and conditions. Another kind learns how the values of all columns occur together, for example that most Accords are Hondas, and then works out how many rows match any condition.

Both kinds can be much more accurate than the classic guess on data with related columns. But they cost time to train, they must be trained again when the data changes, and nobody can promise how wrong they will be on a new query.

## When it applies

- **Correlated data.** The columns of the tables, or the tables of a join, are strongly correlated, so independence gives large errors.
- **A stable workload or stable data.** Query-driven models need training queries similar to the queries they will see. Data-driven models need the data to change slowly, or a budget to retrain.
- **Time to train.** Labels for query-driven training come from running each training query, which can take hours for a large workload. Data-driven models train on the table or a sample of it.
- **It does not apply** where a guarantee is needed, for example when an underestimate is much more expensive than an overestimate; there a [pessimistic bound](/pessimistic-cardinality-estimation/) is safer.

## The template

1. **Choose what to learn.** Either a map from queries to result sizes (query-driven), or the joint distribution $P(A_1, \ldots, A_k)$ of the columns (data-driven), from which $s(p) = P(p \text{ holds})$ for a predicate $p$.
2. **Featurize.** For query-driven models, encode the tables, the joins and the predicates of a query as vectors. MSCN encodes each of the three as a set, applies a small network to each element, averages over each set, and feeds the three averages to a final network. It also adds, for each table, a bitmap of which tuples of a fixed sample satisfy the predicates.
3. **Train.** Fit the model by gradient descent. Query-driven models are usually trained on the logarithm of the true size, which makes the loss close to the logarithm of the q-error, $\max(\hat c/c, c/\hat c)$. Data-driven models maximize the likelihood of the rows.
4. **Estimate.** For a query-driven model, one forward pass. For an autoregressive model, use the chain rule $P(x_1, \ldots, x_k) = \prod_i P(x_i \mid x_1, \ldots, x_{i-1})$, where the network outputs each conditional distribution. For an equality on every column, the selectivity is this product. For ranges, use progressive sampling, below.
5. **Plug in and maintain.** The optimizer calls the model where it called the histogram. When the data or the workload changes, retrain or fine-tune.

**Progressive sampling is unbiased (proved).** Let a predicate be a box $R_1 \times \cdots \times R_k$, one set of allowed values per column, and let $P$ be the model. For one sample: for $i = 1, \ldots, k$, compute $m_i = P(X_i \in R_i \mid x_{<i})$, then draw $x_i$ from $P(\cdot \mid x_{<i})$ restricted to $R_i$ and renormalized. Return $Y = \prod_i m_i$. Then $E[Y] = P(R_1 \times \cdots \times R_k)$.

*Proof.* The sample $x = (x_1, \ldots, x_k) \in R_1 \times \cdots \times R_k$ is drawn with probability $\prod_i P(x_i \mid x_{<i}) / m_i(x_{<i})$, and $Y(x) = \prod_i m_i(x_{<i})$. So

$$E[Y] = \sum_{x \in R_1 \times \cdots \times R_k} \prod_i \frac{P(x_i \mid x_{<i})}{m_i(x_{<i})} \cdot \prod_i m_i(x_{<i}) = \sum_{x \in R_1 \times \cdots \times R_k} P(x),$$

by the chain rule. $\square$

This is [importance sampling](/importance-sampling/) with a proposal that never leaves the box. It proves only that the estimate is unbiased for the model; how close the model is to the data is a question of training, and it is measured.

## Classic examples

**A perfect model of two columns.** A table of 1000 cars has 100 Hondas (50 Accords, 50 Civics), 200 Toyotas (120 Camrys, 80 Corollas) and 700 Fords. Take the model equal to the empirical distribution, which a large enough model can learn. For make = 'Honda' AND model = 'Accord', the chain rule gives $P(\text{Honda}) \cdot P(\text{Accord} \mid \text{Honda}) = 0.1 \cdot 0.5 = 0.05$, which is 50 rows, the exact answer. Independence gives $0.1 \cdot 0.05 = 0.005$, which is 5 rows.

**Progressive sampling on a range.** For make IN ('Honda', 'Toyota') AND model IN ('Accord', 'Camry'), the first step gives $m_1 = P(\text{make} \in \{\text{Honda}, \text{Toyota}\}) = 0.3$ and draws Honda with probability $1/3$ or Toyota with probability $2/3$. Then $m_2 = P(\text{model} \in \{\text{Accord}, \text{Camry}\} \mid \text{make})$ is $0.5$ for Honda and $0.6$ for Toyota. The two possible estimates are $1000 \cdot 0.3 \cdot 0.5 = 150$ and $1000 \cdot 0.3 \cdot 0.6 = 180$ rows, and their mean is $\frac13 \cdot 150 + \frac23 \cdot 180 = 170$, the true answer $50 + 120$.

**MSCN on joins (measured).** Kipf et al. trained MSCN on generated queries over the IMDB data, with up to two joins, and report that its q-errors were much smaller than those of PostgreSQL, in particular on queries with correlated predicates. With more joins than in the training queries, the errors grew. These are measurements on one data set.

**Naru on single tables (measured).** Yang et al. report that Naru, trained on a single table with no queries, gave much smaller worst-case q-errors than histograms, sampling and other models on their benchmark tables, at the cost of more estimation time per query.

## Variations

- **Other data-driven models.** A [Bayesian network](/bayesian-network/) keeps only some dependencies, which is cheaper to fit than a deep model. Sum-product networks (for example DeepDB, 2020) split the rows and the columns recursively. NeuroCard (2021) extends the autoregressive approach to joins by learning the distribution of a full outer join of the tables.
- **Hybrid models.** Combine a sample of the data, as the bitmaps of MSCN do, or a classic estimate, as an input feature, so the model learns a correction.
- **Learning from the running system.** Collect the true sizes of executed subplans and retrain, so the training data follows the workload.
- **Joint learning with the optimizer.** [Learned query optimization](/learned-query-optimization/) skips the explicit estimate and learns the cost or the latency of whole plans.

## Pitfalls

- **No guarantee.** A model with a small average q-error can still have huge errors on some queries. The optimizer can then pick a bad plan, as with any estimator. Report the tail of the q-error, not only the median.
- **Queries unlike the training set.** Query-driven models can be far off on queries with more joins, other tables or other predicate types than they were trained on.
- **Data changes.** After updates, the model describes old data. Retraining costs time, and until then the estimates can be worse than those of a fresh histogram.
- **Cost of estimation.** An optimizer asks for many estimates per query, one per subplan. A slow model, for example one that runs many progressive samples, can make the planning time larger than the time saved.
- **Monotonicity and consistency.** A learned model may estimate a larger result for a more selective predicate, or different sizes for the same subplan written two ways. Classic estimators do not have these problems.

## Exercises

1. Show that a data-driven model that equals the empirical distribution of a table gives the exact selectivity of every conjunctive predicate, while independence is exact only when the columns are independent.
2. In the progressive sampling example, compute the variance of the estimate of the number of rows. (Answer: the estimates 150 and 180 have mean 170, so the variance is $\frac13 \cdot 400 + \frac23 \cdot 100 = 200$.)
3. Explain why training a query-driven model on the logarithm of the size, rather than on the size itself, gives a loss close to the q-error.
4. Design a training set for a query-driven model that would make it underestimate a query with four joins, and say how to detect the problem at run time.

## References
