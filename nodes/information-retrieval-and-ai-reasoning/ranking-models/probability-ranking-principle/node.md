---
tag: MKV8DT
kind: theorem
slug: probability-ranking-principle
name: Probability ranking principle
area: information-retrieval-and-ai-reasoning/ranking-models
level: core
summary: Ranking by decreasing probability of relevance maximizes the expected sum of decreasing rank weights of relevant documents, when the relevance of a document does not depend on the others.
prereqs: [linearity-of-expectation, exchange-argument]
see_also: [binary-independence-model, bm25, query-likelihood-model, bayes-optimal-classifier, precision-at-k, search-result-diversification, maximal-marginal-relevance, ia-select]
sources:
  - paper: doi:10.1108/eb026647
    title: Stephen E. Robertson, The probability ranking principle in IR, Journal of Documentation 33(4), 294 to 304, 1977
    locator: the statement of the principle, its justification under the stated assumptions, and the discussion of a counterexample due to Cooper, in which the documents cannot be judged one at a time
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 11, Section 11.2 (the probability ranking principle, Section 11.2.1 for the 1/0 loss case and Section 11.2.2 for retrieval costs)
  - paper: "Michael D. Gordon and Peter Lenk, When is the probability ranking principle suboptimal?, Journal of the American Society for Information Science 43(1), 1 to 14, 1992"
    locator: the conditions under which ranking by probability of relevance is optimal for the user, and examples where it is not
  - paper: doi:10.1145/321033.321035
    title: M. E. Maron and J. L. Kuhns, On relevance, probabilistic indexing and information retrieval, Journal of the ACM 7(3), 216 to 244, 1960
    locator: the ranking of documents by a probability of relevance computed from weighted index terms
  - paper: doi:10.1145/1148170.1148245
    title: Harr Chen and David R. Karger, Less is more, probabilistic models for retrieving fewer relevant documents, Proceedings of SIGIR 2006, 429 to 436
    locator: metrics that reward one relevant document in the top k, for which ranking by probability of relevance is not optimal, and a greedy ranking that conditions on the documents above
---

The probability ranking principle says that a retrieval system should rank the documents in decreasing order of their probability of relevance to the query. As a theorem it holds when the relevance of each document does not depend on the other documents shown, when the probabilities are exact, and when the user's utility adds a fixed, decreasing weight for each relevant document by rank. Then the sorted order maximizes the expected utility, by [linearity of expectation](/linearity-of-expectation/) and an [exchange argument](/exchange-argument/). It is the reason why the [binary independence model](/binary-independence-model/) and [BM25](/bm25/) rank by an estimate of that probability, and it fails when documents repeat each other, which is the starting point of [result diversification](/search-result-diversification/).

## Statement

Fix a query and a finite set $D$ of $n$ documents. A *ranking* is a bijection $\pi : \{1, \ldots, n\} \to D$, with $\pi(i)$ the document at rank $i$. The relevance of document $d$ is a random variable $R_d \in \{0, 1\}$ on a probability space that models what the system knows from its evidence.

**Hypotheses.**

1. **Relevance of each document is its own.** $R_d$ depends on $d$ and the query only. It does not depend on which other documents the ranking shows, on their order, or on what the user has seen before $d$. So the same variables $R_d$ serve for every ranking.
2. **Calibrated probabilities.** The system knows $p_d = P(R_d = 1 \mid \text{evidence})$ exactly for each $d$.
3. **Rank-linear utility.** The utility of a ranking is $U(\pi) = \sum_{i=1}^{n} w_i R_{\pi(i)}$ with fixed weights $w_1 \ge w_2 \ge \cdots \ge w_n \ge 0$ that do not depend on the $R_d$.

**Theorem.** Under hypotheses 1 to 3, every ranking $\pi^*$ with $p_{\pi^*(1)} \ge p_{\pi^*(2)} \ge \cdots \ge p_{\pi^*(n)}$ maximizes $E[U(\pi)]$ over all rankings $\pi$. If the weights are strictly decreasing and the $p_d$ are distinct, $\pi^*$ is the only maximizer.

No statistical independence between the variables $R_d$ is needed. Hypothesis 3 covers:

- the number of relevant documents in the top $k$, and so precision at $k$: $w_i = 1/k$ for $i \le k$ and $w_i = 0$ after;
- discounted cumulative gain with 0-1 gains: $w_i = 1/\log_2(i + 1)$;
- the cost model of Robertson and of Manning, Raghavan and Schuetze (Section 11.2.2), for a list of $k$ documents. Let $C_0$ be the cost of retrieving a non-relevant document and $C_1$ the cost of missing a relevant one. Up to a constant that does not depend on the ranking, the expected cost of the top $k$ is $-(C_0 + C_1) \sum_{i \le k} p_{\pi(i)}$, which is the case $w_i = C_0 + C_1$ for $i \le k$.

## In plain words

Suppose that the system knows, for each document, the chance that the user will find it relevant, and that this chance does not change when the user has seen other documents. Suppose also that the user gains a fixed amount from each relevant document, and more for one near the top than for one further down. Then the best list puts the most probable document first, the next most probable second, and so on.

If two neighbors in a list are in the wrong order, swapping them moves the more probable one to the place that is worth more, and the expected gain can only go up. Any list can be sorted by such swaps, so the sorted list is the best one. The rule says nothing about how to find the chances. Models such as BM25 are ways to estimate them.

## Proof

Fix a ranking $\pi$. By linearity of expectation, which holds for any joint distribution of the $R_d$,

$$E[U(\pi)] = \sum_{i=1}^{n} w_i \, E[R_{\pi(i)}] = \sum_{i=1}^{n} w_i \, p_{\pi(i)}.$$

Hypothesis 1 lets us use the same $R_d$, and so the same $p_d$, for every ranking. Hypothesis 2 makes $E[R_d] = p_d$ the true value.

Call a pair of ranks $i < j$ an *inversion* of $\pi$ if $p_{\pi(i)} < p_{\pi(j)}$. If $\pi$ has an inversion, it has one at two adjacent ranks $i$ and $i + 1$, since otherwise $p_{\pi(1)} \ge p_{\pi(2)} \ge \cdots \ge p_{\pi(n)}$. Let $\pi'$ be $\pi$ with the documents at ranks $i$ and $i + 1$ swapped. Only two terms of the sum change, so

$$E[U(\pi')] - E[U(\pi)] = w_i p_{\pi(i+1)} + w_{i+1} p_{\pi(i)} - w_i p_{\pi(i)} - w_{i+1} p_{\pi(i+1)} = (w_i - w_{i+1})(p_{\pi(i+1)} - p_{\pi(i)}) \ge 0,$$

because $w_i \ge w_{i+1}$ and $p_{\pi(i+1)} > p_{\pi(i)}$. The swap removes exactly one inversion and creates none. So after at most $n(n-1)/2$ swaps we reach a ranking with no inversion, that is, a sorted ranking, and the expected utility never went down. Two sorted rankings differ only in the order of documents with equal $p_d$, and such documents give the same terms in the sum, so all sorted rankings have the same expected utility. Hence $E[U(\pi^*)] \ge E[U(\pi)]$ for every $\pi$.

For uniqueness, let the $w_i$ be strictly decreasing and the $p_d$ distinct. Then a ranking $\pi \ne \pi^*$ has an adjacent inversion, and the swap above gives a strictly positive change. So $\pi$ is not a maximizer, and $\pi^*$ is the only one. $\blacksquare$

The same argument is the rearrangement inequality: a sum of products $\sum_i w_i p_{\pi(i)}$ is largest when both sequences are sorted in the same order.

## Consequences

- **Rank by any increasing function of the probability.** The proof uses only the order of the $p_d$. A model may rank by the log-odds $\log(p_d / (1 - p_d))$, or by any strictly increasing function of $p_d$, and get the same ranking. The [binary independence model](/binary-independence-model/) and [BM25](/bm25/) rank by such a function, estimated from term statistics.
- **Where to stop needs the true values.** With the costs $C_0$ and $C_1$ above, retrieving $d$ changes the expected cost by $C_0(1 - p_d) - C_1 p_d$. A system that may choose how many documents to return should return exactly those with $p_d > C_0/(C_0 + C_1)$. This rule needs calibrated values, not only their order. It is the Bayes decision rule of a [Bayes optimal classifier](/bayes-optimal-classifier/) with these costs.
- **Graded relevance.** If the gain of $d$ is a random value $G_d \ge 0$ in place of $R_d$, the same proof shows that ranking by decreasing $E[G_d]$ maximizes $\sum_i w_i E[G_{\pi(i)}]$, so DCG with graded gains is maximized by sorting on the expected gain.
- **Some nonlinear measures under statistical independence.** If the $R_d$ are independent random variables, the probability that the top $k$ holds at least one relevant document is $1 - \prod_{i \le k} (1 - p_{\pi(i)})$. This is largest when the top $k$ are the $k$ documents with the largest $p_d$, so the sorted ranking is also optimal for this measure.
- **Measures outside the theorem.** Average precision, reciprocal rank and nDCG are not of the form of hypothesis 3: they divide by a random number of relevant documents or depend on products of the $R_d$. The proof above does not cover them.

## Tightness

Each hypothesis is needed. The clearest failure is a pair of duplicates.

**Dependent relevance.** Let $A$ and $B$ be two copies of one text, so $R_A = R_B$ always, with $p_A = p_B = 0.6$. Let $C$ be a different document with $p_C = 0.5$, independent of $R_A$. The user wants one relevant document and reads two, so the utility is 1 if the top 2 holds a relevant document and 0 if not.

- The principle puts $A$ and $B$ first. The top 2 holds a relevant document exactly when $R_A = 1$, with probability 0.6.
- The ranking $A, C, B$ fails only when $R_A = 0$ and $R_C = 0$, so it succeeds with probability $1 - 0.4 \cdot 0.5 = 0.8$.

Once the user has read $A$, the copy $B$ adds nothing, so the value of $B$ depends on the document above it. This breaks hypothesis 1, and the utility is not of the form of hypothesis 3. Chen and Karger (2006) study such measures and rank greedily: each next document is the one most likely to be relevant given that the documents above it are not. [Maximal marginal relevance](/maximal-marginal-relevance/), [IA-Select](/ia-select/) and [xQuAD](/xquad/) are methods of this kind.

**Uncalibrated probabilities.** If the system ranks by estimates that are not in the order of the true $p_d$, sorting by the estimates is optimal only for its own beliefs. With true values 0.6 and 0.5 and estimates 0.4 and 0.5, the system puts the second document first and its expected precision at 1 is 0.5 in place of 0.6. Gordon and Lenk (1992) list such failures of the assumptions together with the cases where the principle stays optimal.

**Weights that increase.** If $w_2 > w_1$, as for a user who skips the first result, the best ranking puts the second most probable document at rank 1. The order of the weights is what decides the order of the documents.

## History

Maron and Kuhns proposed in 1960 to rank documents by a probability of relevance computed from weighted index terms. The classic statement of the principle as a rule for retrieval systems, with its justification under explicit assumptions and the discussion of a counterexample of Cooper, is the paper of Robertson (1977). The [binary independence model](/binary-independence-model/) of Robertson and Sparck Jones (1976) and the later Okapi weights are derived from it. Gordon and Lenk (1991, 1992) examined it from the point of view of decision theory. Chen and Karger (2006) and the work on diversification since then study the cases where the relevance of one document depends on the documents above it.

## References
