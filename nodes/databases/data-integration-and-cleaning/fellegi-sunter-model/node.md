---
tag: 1B2G63
kind: model
slug: fellegi-sunter-model
name: Fellegi-Sunter model
aliases:
- Fellegi-Sunter record linkage theory
area: databases/data-integration-and-cleaning
level: core
summary: "A probabilistic model of record linkage: score each pair by the likelihood ratio of its field agreements under match and non-match, and link, review or reject it by two thresholds."
prereqs: [entity-resolution, likelihood-ratio-test]
see_also: [neyman-pearson-lemma, expectation-maximization, naive-bayes-classifier, entity-resolution-blocking, sorted-neighborhood-method, jaro-winkler-distance, maximum-likelihood-estimation, bayes-theorem]
sources:
  - paper: doi:10.1080/01621459.1969.10501049
    title: "Ivan P. Fellegi and Alan B. Sunter, A theory for record linkage, Journal of the American Statistical Association 64(328), 1969, pages 1183 to 1210"
    locator: "the model (the sets M and U, the comparison vector, m and u, the linkage rule and its error levels), the optimal linkage rule and its theorem, Section 3.2 (conditional independence of the components and the additive weights), Section 3.3 (the estimation of m and u from the frequencies of the comparison patterns)"
  - paper: "Howard B. Newcombe, James M. Kennedy, S. J. Axford and A. P. James, Automatic linkage of vital records, Science 130(3381), 1959, pages 954 to 959"
    locator: the earlier use of weights from the frequencies of agreement on each field
  - book: isbn:9783642311635
    title: "Peter Christen, Data Matching: Concepts and Techniques for Record Linkage, Entity Resolution, and Duplicate Detection, Springer, 2012"
    locator: the chapter on classification, the section on probabilistic record linkage and the estimation of m and u
---

The Fellegi-Sunter model is the standard probabilistic model of the pair decision in [entity resolution](/entity-resolution/). It takes the pairs of records from two files, describes each pair by a *comparison vector* $\gamma$ (for example "agree on surname, disagree on city"), and compares two probabilities: $m(\gamma)$, the probability of that vector for a true match, and $u(\gamma)$, its probability for a non-match. A pair is linked if $m(\gamma)/u(\gamma)$ is large, rejected if it is small, and sent to a person for review in between. Fellegi and Sunter proved that this rule is optimal: for fixed error rates it sends the fewest pairs to review. The proof holds inside the model: the theorem assumes that $m$ and $u$ are known. [Expectation maximization](/expectation-maximization/) is a general method for models with hidden labels; here it is one way to estimate $m$ and $u$ when the match status of the pairs is hidden, and it was added to the model later. [Blocking](/entity-resolution-blocking/) and the [sorted neighborhood method](/sorted-neighborhood-method/) choose which pairs the model sees.

## The machine

**Pairs.** Two files $A$ and $B$. The set $A \times B$ is the disjoint union of the matched pairs $M$ (the same entity) and the unmatched pairs $U$. The model does not see which pairs are in $M$.

**Comparison vectors.** A function $\gamma$ maps each pair to a vector in a finite set $\Gamma$. Usually $\gamma = (\gamma_1, \ldots, \gamma_K)$ with one component for each field, each with values such as agree and disagree, or agree on a rare value, agree on a common value, disagree, and missing.

**The two distributions.** $m(\gamma) = P(\gamma \mid M)$ and $u(\gamma) = P(\gamma \mid U)$, for a pair drawn at random from $M$ or from $U$.

**Decisions.** A *linkage rule* $L$ maps each $\gamma$ to probabilities of three decisions: $A_1$ link, $A_2$ possible link (clerical review), $A_3$ non-link. Its two error levels are
$$\mu = P(A_1 \mid U) = \sum_{\gamma} u(\gamma) P(A_1 \mid \gamma), \qquad \lambda = P(A_3 \mid M) = \sum_{\gamma} m(\gamma) P(A_3 \mid \gamma).$$
$\mu$ is the rate of false links, and $\lambda$ the rate of missed links.

**The rule of the model.** Order the vectors by decreasing ratio $R(\gamma) = m(\gamma)/u(\gamma)$. Link the vectors at the top until their total $u$ reaches $\mu$, reject the vectors at the bottom until their total $m$ reaches $\lambda$, and send the rest to review. At the two boundaries a vector can be split by a random choice so that the levels are met exactly. In practice the rule is written with two thresholds $T_\mu > T_\lambda$ on $R$ or on $\log R$.

**Conditional independence.** If the components are independent given $M$ and given $U$, then $m(\gamma) = \prod_i m_i(\gamma_i)$ and $u(\gamma) = \prod_i u_i(\gamma_i)$, and
$$\log R(\gamma) = \sum_{i=1}^{K} \log \frac{m_i(\gamma_i)}{u_i(\gamma_i)}.$$
Each field adds an *agreement weight* $\log(m_i/u_i)$ or a *disagreement weight* $\log((1 - m_i)/(1 - u_i))$. This is an assumption. Errors in two fields of a record are often related, such as a wrong person who is in the same family and has the same surname and address.

## What it counts

The model counts two error rates, $\mu$ and $\lambda$, and the size of the review set $P(A_2)$, which is the work of the clerks. It does not count time. The cost of using it is one comparison vector for each pair that is scored, so with $|A| \cdot |B|$ pairs it is used together with a method that selects pairs.

**Example.** Three fields with agree or disagree, with $m = (0.95, 0.9, 0.8)$ and $u = (0.01, 0.05, 0.2)$ for surname, birth year and city, and conditional independence:

| surname, year, city | $m(\gamma)$ | $u(\gamma)$ | $R(\gamma)$ | $\log_2 R$ |
|---|---|---|---|---|
| agree, agree, agree | 0.684 | 0.0001 | 6840 | 12.74 |
| agree, agree, disagree | 0.171 | 0.0004 | 427.5 | 8.74 |
| agree, disagree, agree | 0.076 | 0.0019 | 40 | 5.32 |
| disagree, agree, agree | 0.036 | 0.0099 | 3.64 | 1.86 |
| agree, disagree, disagree | 0.019 | 0.0076 | 2.5 | 1.32 |
| disagree, agree, disagree | 0.009 | 0.0396 | 0.227 | -2.14 |
| disagree, disagree, agree | 0.004 | 0.1881 | 0.021 | -5.56 |
| disagree, disagree, disagree | 0.001 | 0.7524 | 0.001 | -9.56 |

With $\mu = 0.0024$ the rule links the first three rows, and with $\lambda = 0.014$ it rejects the last three. The two middle rows go to review: 5.5% of the true matches and 1.75% of the non-matches. With $\log_2$ the weights add up: agreement on the surname adds $\log_2 95 = 6.57$, and disagreement adds $\log_2(0.05/0.99) = -4.31$.

## Relation to other models

- **Hypothesis testing.** Each pair is a test of $M$ against $U$. The rule is a [likelihood ratio test](/likelihood-ratio-test/) with two thresholds instead of one, and its optimality is close to the [Neyman-Pearson lemma](/neyman-pearson-lemma/), with a review region in the middle.
- **Naive Bayes.** With conditional independence, the score is that of a [naive Bayes classifier](/naive-bayes-classifier/) with two classes, without the prior. A prior on the share of matches turns $R$ into a posterior by [Bayes' theorem](/bayes-theorem/).
- **Mixture models.** Without labels, the comparison vectors of all pairs form a two-class mixture with weights $p = |M|/|A \times B|$ and $1 - p$. Fitting $p$, $m$ and $u$ is a latent class problem, solved by [maximum likelihood](/maximum-likelihood-estimation/) with expectation maximization.
- **Learned classifiers.** A classifier such as [logistic regression](/logistic-regression/), trained on labelled pairs, drops the independence assumption but needs labels.
- **Merge models.** [R-Swoosh](/r-swoosh/) treats the match rule as a black box. A Fellegi-Sunter rule with two thresholds can be that black box, but its scores do not have the ICAR properties in general.

## Known results in the model

- **Optimal rule (theorem).** Fellegi and Sunter proved that, for any admissible $\mu$ and $\lambda$, the rule above has the smallest $P(A_2)$ among all linkage rules with error levels at most $\mu$ and $\lambda$. It holds for any $m$ and $u$, with or without independence, as long as they are the true distributions.
- **Additive weights (theorem in the model).** Under conditional independence, $\log R$ is the sum of the field weights, so the order of the vectors needs only $2K$ numbers.
- **Estimation from the data.** Fellegi and Sunter gave equations that estimate $m_i$, $u_i$ and the share of matches from the frequencies of the comparison patterns, for three components under conditional independence. Later work fits the same mixture with expectation maximization. EM never lowers the likelihood, but it converges only to a local maximum, and the fit depends on the starting values. This is a heuristic.
- **Frequency-based weights.** $u_i$ can depend on the value: agreement on a rare surname is more likely to be a match than agreement on a common one. Newcombe and his colleagues used such weights before the model was written down.
- **Effect of a wrong assumption (measurement).** When fields are dependent, the sum of the weights counts the same evidence twice, and the error rates of the rule differ from the levels that were set. How much is a question of the data.

## References
