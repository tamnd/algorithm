---
tag: 11RFN8
kind: model
slug: binary-independence-model
name: Binary independence model
aliases:
- BIM
- Robertson-Sparck Jones model
area: information-retrieval-and-ai-reasoning/ranking-models
level: core
summary: A probabilistic model with binary term occurrence and term independence given relevance, giving the Robertson-Sparck Jones term weight.
prereqs: [probability-ranking-principle, bayes-theorem]
see_also: [tf-idf, bm25, two-poisson-model, naive-bayes-classifier, logistic-regression, relevance-feedback, pseudo-relevance-feedback, boolean-retrieval-model]
sources:
  - paper: doi:10.1002/asi.4630270302
    title: Stephen E. Robertson and Karen Sparck Jones, Relevance weighting of search terms, Journal of the American Society for Information Science 27(3), 129 to 146, 1976
    locator: the relevance weight of a term from the contingency table of relevance against occurrence, the weighting functions F1 to F4 and the estimates with 0.5 added to each cell
  - paper: doi:10.1108/eb026683
    title: W. Bruce Croft and David J. Harper, Using probabilistic models of document retrieval without relevance information, Journal of Documentation 35(4), 285 to 295, 1979
    locator: the weight with no relevance information, a constant plus log((N - n)/n), and the initial search that it gives
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 11, Section 11.3 (the binary independence model, the retrieval status value and the estimation of the probabilities with and without relevance information)
  - paper: doi:10.1561/1500000019
    title: Stephen Robertson and Hugo Zaragoza, The probabilistic relevance framework, BM25 and beyond, Foundations and Trends in Information Retrieval 3(4), 333 to 389, 2009
    locator: the binary independence model and the Robertson-Sparck Jones weight as the first step toward BM25
  - paper: doi:10.1145/195705.195735
    title: William S. Cooper, Some inconsistencies and misidentified modeling assumptions in probabilistic information retrieval, ACM Transactions on Information Systems 13(1), 100 to 111, 1995
    locator: the independence assumptions of the model and the weaker linked dependence assumption that the derivation needs
---

The binary independence model describes a document only by which terms it contains, and it assumes that these occurrences are independent random events within the relevant documents and within the non-relevant documents. With the [probability ranking principle](/probability-ranking-principle/) and [Bayes' theorem](/bayes-theorem/), ranking by the odds of relevance becomes a sum over the query terms present in the document of one weight for each term, the Robertson-Sparck Jones weight. With judged documents the weight is estimated from a 2 by 2 table of counts, and with no judgments it becomes an [idf](/tf-idf/). The model ignores how often a term occurs, which [BM25](/bm25/) adds.

## The machine

**Events.** For a query $q$, a document $d$ is the vector $x = (x_t)_{t \in V}$ with $x_t = 1$ if term $t$ occurs in $d$ and $x_t = 0$ if not. Relevance $R \in \{0, 1\}$ is a random event. For each term let

$$p_t = P(x_t = 1 \mid R = 1), \qquad u_t = P(x_t = 1 \mid R = 0).$$

**Assumptions.**

1. *Binary independence.* Given $R = 1$, the $x_t$ are independent, and the same holds given $R = 0$: $P(x \mid R) = \prod_t P(x_t \mid R)$.
2. *Terms outside the query do not help.* For $t \notin q$, $p_t = u_t$.

**Derivation.** By Bayes' theorem the odds of relevance are

$$O(R \mid x) = \frac{P(R = 1 \mid x)}{P(R = 0 \mid x)} = O(R) \prod_{t} \frac{P(x_t \mid R = 1)}{P(x_t \mid R = 0)}.$$

By assumption 2 only the query terms give a factor different from 1. Split them into those present and those absent, and multiply and divide by $\prod_{t \in q \cap d} (1 - p_t)/(1 - u_t)$:

$$O(R \mid x) = O(R) \prod_{t \in q} \frac{1 - p_t}{1 - u_t} \cdot \prod_{t \in q \cap d} \frac{p_t (1 - u_t)}{u_t (1 - p_t)}.$$

The first two factors are the same for every document. A logarithm is increasing, so the order of the documents is the order of the *retrieval status value*

$$\mathrm{RSV}(d) = \sum_{t \in q \cap d} c_t, \qquad c_t = \ln \frac{p_t (1 - u_t)}{u_t (1 - p_t)}.$$

The weight $c_t$ is the log odds ratio of term $t$: the log of the odds that $t$ occurs in a relevant document over the odds that it occurs in a non-relevant one.

**Estimates with relevance information.** Let $N$ be the number of documents, $n_t$ the number that contain $t$, $R$ the number of known relevant documents and $r_t$ the number of those that contain $t$. Then $p_t \approx r_t/R$ and $u_t \approx (n_t - r_t)/(N - R)$. Adding 0.5 to each of the four cells of the table avoids zeros and gives the Robertson-Sparck Jones weight, with the natural log:

$$w_t = \ln \frac{(r_t + 0.5)(N - n_t - R + r_t + 0.5)}{(n_t - r_t + 0.5)(R - r_t + 0.5)}.$$

**Estimates with no relevance information.** Croft and Harper (1979) take $p_t$ to be the same constant for all query terms and estimate $u_t$ by $n_t/N$, because almost all documents are not relevant. The weight becomes $C + \ln((N - n_t)/n_t)$ with $C = \ln(p/(1 - p))$. For $p = 0.5$, $C = 0$. The Robertson-Sparck Jones weight with $R = r_t = 0$ is the same form with the 0.5 corrections, $\ln((N - n_t + 0.5)/(n_t + 0.5))$. This is a probabilistic idf. It is 0 when $n_t = N/2$ and negative when more than half of the documents contain $t$.

**Example.** On the toy collection of the information retrieval pages, $N = 8$. For q1 = "sorted array search" the judged relevant documents are $d_1$, $d_2$ and $d_8$, so $R = 3$:

| term | $n_t$ | $r_t$ | weight with $R = 3$ | weight with no judgments |
|---|---|---|---|---|
| sorted | 4 | 3 | $\ln \frac{3.5 \cdot 4.5}{1.5 \cdot 0.5} = \ln 21 = 3.0445$ | $\ln \frac{4.5}{4.5} = 0$ |
| array | 3 | 3 | $\ln \frac{3.5 \cdot 5.5}{0.5 \cdot 0.5} = \ln 77 = 4.3438$ | $\ln \frac{5.5}{3.5} = 0.4520$ |
| search | 2 | 1 | $\ln \frac{1.5 \cdot 4.5}{1.5 \cdot 2.5} = \ln 1.8 = 0.5878$ | $\ln \frac{6.5}{2.5} = 0.9555$ |

With the judgments, $\mathrm{RSV}(d_1) = 3.0445 + 4.3438 + 0.5878 = 7.9761$, then $d_2$ and $d_8$ tie at $7.3883$ and come in id order, then $d_4$ (3.0445) and $d_7$ (0.5878). All three relevant documents are on top. "Search" gets a small weight because the non-relevant $d_7$ contains it and two of the three relevant documents do not. These weights were fitted to the same judgments they are tested on, so the result is optimistic.

With no judgments the order is $d_1$ (1.4075), $d_7$ (0.9555), $d_2$ and $d_8$ (0.4520, in id order) and $d_4$ (0). Here "sorted" is in exactly half of the documents and adds nothing. The document $d_2$ holds "sorted" twice and gets the same score as $d_8$, because the model sees only presence.

## What it counts

- **Parameters.** Two probabilities $p_t$ and $u_t$ for each query term, estimated from the counts $N$, $n_t$, $R$ and $r_t$. All other terms are ignored.
- **Score.** A sum of one weight for each query term present, a linear function of the binary vector $x$ restricted to the query terms. Its value is the log odds of relevance up to a constant for the query. The order of documents is what matters, by the probability ranking principle.
- **Cost.** Scoring reads the posting lists of the query terms, $O(\sum_{t \in q} n_t)$ postings, and needs no term frequencies.

## Relation to other models

- **Probability ranking principle.** The model is a way to estimate the order of $P(R = 1 \mid d)$, which the [principle](/probability-ranking-principle/) says to rank by.
- **Naive Bayes.** The two assumptions are those of a Bernoulli [naive Bayes classifier](/naive-bayes-classifier/) with the classes relevant and non-relevant and with features restricted to the query terms. The RSV is its log odds up to a constant. [Logistic regression](/logistic-regression/) fits the same linear form directly, without the independence assumption.
- **Tf-idf.** The weight with no relevance information is an idf, which gives the [tf-idf](/tf-idf/) idf factor a probabilistic reading (Robertson 2004).
- **Coordination level.** With the constant $C$ of Croft and Harper large compared with the idf part, each extra matching query term counts more than any difference of idf. The order is then first by the number of query terms matched, as in coordination level matching, a step from the [Boolean model](/boolean-retrieval-model/) toward ranking.
- **Relevance feedback.** Each new judged document updates $R$ and $r_t$, and so the weights. This is the probabilistic form of [relevance feedback](/relevance-feedback/), and taking the top documents of a first search as relevant is [pseudo-relevance feedback](/pseudo-relevance-feedback/).
- **Term frequency.** The [two-Poisson model](/two-poisson-model/) replaces presence by a hidden *eliteness* of the document for the term, which leads to the saturating tf of [BM25](/bm25/). BM25 keeps the Robertson-Sparck Jones weight as its idf.

## Known results in the model

- **Ranking by the RSV is the probability ranking.** Under the two assumptions, the derivation above is exact. The order by $\mathrm{RSV}$ is the order by $P(R = 1 \mid d)$, so it is optimal for every utility of the [probability ranking principle](/probability-ranking-principle/) when the $p_t$ and $u_t$ are the true values.
- **Four weighting functions.** Robertson and Sparck Jones (1976) derive four weights, F1 to F4, from two choices of independence assumption and two choices of ordering principle. The weight $w_t$ above is F4, the one in common use.
- **The 0.5 corrections.** Without them a term with $r_t = R$ or $r_t = 0$ gets an infinite weight. Adding 0.5 to each cell gives finite weights in all cases.
- **Linked dependence.** Cooper (1995) shows that the two independence assumptions, taken together over a whole collection, can contradict each other, and that the derivation needs only the weaker *linked dependence* assumption: the ratio $P(x \mid R = 1)/P(x \mid R = 0)$ factors over the terms.
- **Negative weights.** With no relevance information, a query term in more than half of the documents gets a negative weight. Engines often clamp it to 0 or use the idf of Lucene's BM25, which stays positive.

## References
