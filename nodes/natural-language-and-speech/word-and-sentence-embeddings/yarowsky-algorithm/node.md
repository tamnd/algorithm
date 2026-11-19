---
tag: 89R7KS
kind: algorithm
slug: yarowsky-algorithm
name: Yarowsky algorithm
aliases:
- one sense per collocation bootstrapping
area: natural-language-and-speech/word-and-sentence-embeddings
level: core
summary: Semi-supervised sense disambiguation that grows a decision list from a few seed collocations using one sense per discourse and one sense per collocation.
solves: [word-sense-disambiguation]
model: word-ram
complexity:
  vars: {n: the number of occurrences of the target word, m: the largest number of features of one occurrence, F: the number of distinct features, T: the number of rounds}
  time: {worst: "O(T (n m + F log F + n F))"}
  space: {extra: "O(n m + F)"}
properties: {deterministic: true, exact: false, online: false, recursive: false, supervised: false}
history:
  year: 1995
  people: [David Yarowsky]
  note: Yarowsky started from a few seed collocations per sense and grew a decision list over a large corpus, using one sense per collocation and one sense per discourse, and reported accuracy close to a supervised decision list.
prereqs: [word-sense-disambiguation]
see_also: [lesk-algorithm, expectation-maximization, naive-bayes-classifier, laplace-smoothing, decision-tree, fixed-point-iteration, pointwise-mutual-information, hearst-patterns]
sources:
  - paper: "David Yarowsky, Unsupervised word sense disambiguation rivaling supervised methods, Proceedings of the 33rd Annual Meeting of the ACL, 1995, pages 189 to 196"
    title: Yarowsky 1995
    locator: the two constraints with the measurement of one sense per discourse, Steps 1 to 5 of the algorithm with the plant example, and the table of results for 12 words
  - paper: "William A. Gale, Kenneth W. Church and David Yarowsky, One sense per discourse, Proceedings of the DARPA Speech and Natural Language Workshop, 1992, pages 233 to 237"
    title: Gale, Church and Yarowsky 1992
    locator: the observation that an ambiguous word keeps one sense within a discourse
  - paper: "David Yarowsky, Decision lists for lexical ambiguity resolution, application to accent restoration in Spanish and French, Proceedings of the 32nd Annual Meeting of the ACL, 1994"
    title: Yarowsky 1994
    locator: the decision list ranked by the log likelihood ratio of each collocation
  - paper: "Steven Abney, Understanding the Yarowsky algorithm, Computational Linguistics 30(3), 2004, pages 365 to 395"
    title: Abney 2004
    locator: the analysis of variants of the algorithm as the optimization of an objective
  - paper: doi:10.1145/1459352.1459355
    title: Roberto Navigli, Word sense disambiguation, a survey, ACM Computing Surveys 41(2), 2009, article 10
    locator: the section on semi-supervised disambiguation and bootstrapping
---

The Yarowsky algorithm solves [word sense disambiguation](/word-sense-disambiguation/) for one ambiguous word from a large unlabeled corpus and a few seed collocations, for example "plant life" for the living sense of "plant" and "manufacturing plant" for the factory sense. The seeds label a small part of the occurrences. A decision list trained on these labels then labels more occurrences, the list is trained again on the larger set, and the loop goes on until the labels stop changing. Two heuristic constraints drive it. One sense per collocation says that a nearby word gives strong and consistent evidence for one sense. One sense per discourse says that an ambiguous word keeps one sense within one document, so a label can spread to the other occurrences in the same document. The [Lesk algorithm](/lesk-algorithm/) uses a dictionary instead of a corpus.

## In plain words

Suppose you want to tell the living "plant" from the factory "plant" in a big pile of text. You know two clues for sure: "plant life" is the living kind and "manufacturing plant" is the factory kind. Those two clues mark a few sentences.

Now look at the marked sentences and notice which other words appear near "plant" in each group. Words such as "water" go with the living kind, and words such as "workers" go with the factory kind. Use these new clues to mark more sentences, and learn more clues from them. If one document already uses "plant" in one sense, give that sense to the other unmarked uses of "plant" in the same document. Stop when a round marks nothing new.

## The problem

The input is a list of $n$ occurrences of one target word, each with its tokens and, if known, the discourse (document) it is in, a list of senses, and a map from seed features to senses. The features of an occurrence are its collocations: the word just before the target ($-1{:}w$), the word just after it ($+1{:}w$), and each word that is not a stop word within $k$ tokens ($\text{win}{:}w$). The output is a sense or $\bot$ (no decision) for each occurrence, and a decision list that can label new occurrences.

A decision list is a list of rules $(f, s, \lambda)$ sorted by decreasing score $\lambda$. It labels an occurrence with the sense of the first rule whose feature the occurrence has. For labels $y$, let $c(f, \sigma)$ count the occurrences labeled $\sigma$ that have the feature $f$. The rule for $f$ takes the sense $s_f$ with the largest count and the smoothed log ratio

$$ \lambda_f = \ln \frac{c(f, s_f) + \alpha}{\sum_{\sigma \ne s_f} c(f, \sigma) + \alpha} \quad (\ln,\ \text{nats}), $$

with a constant $\alpha > 0$. With two senses this is the log of the ratio of the two smoothed counts, as in Yarowsky 1994.

## The algorithm

```pseudo id=main
YAROWSKY(occurrences, seeds, senses, alpha, theta, T)
L1  y ← the seed labels: the sense of the seed features of each occurrence, else ⊥
L2  for t ← 1 to T do
L3      D ← the decision list trained on the occurrences with y_i ≠ ⊥
L4      y' ← for each occurrence: its seed label if it has one, else the sense of the first rule of D that matches it if the score of that rule is at least theta, else ⊥
L5      optional: for each occurrence without a seed label in a discourse where one sense has strictly the most labels in y', set y'_i to that sense
L6      if y' = y then return D, y
L7      y ← y'
L8  return D, y
```

The rules are sorted by decreasing score and, on equal scores, by the feature string, and the largest count goes to the first sense on ties. This makes the loop deterministic. An occurrence with two seed features of different senses gets no seed label in line L1. Seed labels never change: line L4 keeps them and line L5 skips them.

## Example

The target is "plant", with A the living sense and B the factory sense. The seeds are $+1{:}\text{life} \to A$ and $-1{:}\text{manufacturing} \to B$, with $\alpha = 0.1$, $\theta = 2$, $k = 4$ and one sense per discourse on. The nine occurrences, written for this page, are in six documents:

| i | occurrence | document | seed |
| --- | --- | --- | --- |
| 1 | plant life needs water and light | d1 | A |
| 2 | a green plant grows toward the light | d1 | |
| 3 | the plant needs water | d1 | |
| 4 | the manufacturing plant hired workers | d2 | B |
| 5 | workers at the plant went on strike | d2 | |
| 6 | the car plant closed | d3 | |
| 7 | water the plant every day | d4 | |
| 8 | the plant workers were paid | d5 | |
| 9 | the car plant employs workers | d6 | |

The rounds:

| round | rules that decide | labels 1 to 9 after the round |
| --- | --- | --- |
| seeds (L1) | none | A, ⊥, ⊥, B, ⊥, ⊥, ⊥, ⊥, ⊥ |
| 1 | win:needs A, win:water A, win:workers B, each $\ln 11 \approx 2.398$ | A, A, A, B, B, ⊥, A, B, B |
| 2 | win:workers B $\ln 41 \approx 3.714$, win:water A $\ln 31 \approx 3.434$, win:needs A $\ln 21 \approx 3.045$, -1:car B $\ln 11$ | A, A, A, B, B, B, A, B, B |
| 3 | the same list as round 2, with -1:car B now $\ln 21$ | no change, so line L6 returns |

In round 1 only occurrences 1 and 4 are labeled, so every feature has one count and the score $\ln(1.1/0.1) = \ln 11$. Occurrence 3 gets A from "needs" and "water", occurrence 7 from "water", and occurrences 5, 8 and 9 get B from "workers". Occurrence 2 has no feature in the list, but its document d1 has only A labels, so line L5 gives it A. Occurrence 6 has no match and is alone in d3, so it stays ⊥. In round 2 occurrence 9 is labeled B, so the rule -1:car B appears with score $\ln 11 \ge \theta$ and labels occurrence 6. The feature -1:the occurs in two A and two B occurrences and gets the score $\ln(2.1/2.1) = 0$, last in the list. Without line L5, occurrence 2 stays ⊥, since none of its features occurs in another occurrence: the "light" of occurrence 1 is 5 tokens from "plant", outside the window.

## Correctness

The sense labels are a heuristic and their quality is a measurement. What can be proved is what the loop computes. The decision list labels an occurrence with the sense of its matching rule of largest score, the smallest feature on ties, if that score reaches $\theta$. The seed labels never change, since line L4 keeps them and line L5 skips them. The loop stops after at most $T$ rounds, and if line L6 returns early, the labels are a fixed point of one round: training on them and labeling again gives the same labels. The loop is not guaranteed to reach a fixed point. An occurrence labeled in one round can lose its label in the next, when new labels lower the score of its rule below $\theta$, so the bound $T$ is needed. Yarowsky 1995 gives no convergence proof. Abney 2004 analyzes variants that optimize an objective. The full proof is below.

## Complexity

The model is the [word-RAM](/word-ram/) with hash maps keyed by feature strings.

- **Features.** Building the feature sets costs $O(n m)$ once, for $m$ at most $2k + 2$ features per occurrence.
- **One round.** Counting costs $O(n m)$, scoring $O(F)$, and sorting the rules $O(F \log F)$. Line L4 scans the list for each occurrence, which is $O(n F)$ in the worst case. With a map from each feature to its rank, line L4 takes the best rule of an occurrence in $O(m)$, which makes the round $O(n m + F \log F)$. Line L5 counts the votes per document in $O(n)$.
- **All rounds.** $T$ times the cost of a round. The space is $O(n m)$ for the features and $O(F)$ for the list and the counts.

In Yarowsky's experiments the rounds run over all the occurrences of the word in a corpus of 460 million words, so the cost of a round, and not the number of rounds, decides the run time.

## Properties

- **Semi-supervised.** The only labeled input is the seeds. Yarowsky called it unsupervised, since the seeds can come from a dictionary definition or a few hand-picked words.
- **Self-training.** The classifier is trained on its own output. An occurrence that gets a label in round $t$ is training data in round $t + 1$, and it also counts for the rules that labeled it.
- **Readable model.** The decision list is a ranked list of collocations, so each decision has one rule as its reason.
- **One sense per collocation.** A heuristic. It is what makes a single best rule a good decision, and the list keeps only that rule per occurrence.
- **One sense per discourse.** A heuristic, with a measurement: Yarowsky 1995 reports 99.8% accuracy for it on 37,232 examples, with an applicability of 50.1%, which means that about half of the examples have another occurrence of the word in the same discourse.

## Variants and improvements

- **Two senses with absolute scores.** Yarowsky 1994 and 1995 use two senses and rank the rules by the absolute value of the log ratio. The rule above is the same for two senses and gives one rule per feature for more senses.
- **Seeds.** Yarowsky 1995 compares seeds of two hand-picked words, the words of the dictionary definitions, and the top collocations from a few labeled examples.
- **Line L5 as a filter.** The original uses one sense per discourse both to add labels and to remove labels that disagree with the majority of a discourse. Line L5 replaces a minority label with the majority sense, which does both.
- **A final pass.** After the loop, the original applies the final decision list to new text, so the list is a classifier and not only a labeling of the training corpus.
- **Analyzed variants.** Abney 2004 defines variants with a stated objective that each round does not increase. Like [expectation maximization](/expectation-maximization/), they alternate between labeling the data and fitting the model to the labels.

## When to use it

Use it when one ambiguous word has many unlabeled occurrences, long documents, and a few reliable collocations per sense. The decision list is cheap to apply and easy to inspect. When a sense-tagged corpus exists, a supervised classifier such as [naive Bayes](/naive-bayes-classifier/) or a neural model is usually simpler. When the senses come from a dictionary and there is no corpus, use [Lesk](/lesk-algorithm/).

## Pitfalls

- **A wrong label spreads.** Line L4 trusts the rules learned from earlier labels, so one error can produce more errors. Replace occurrence 9 above by "a car plant needs workers". In round 1, win:needs A and win:workers B have the same score, and the tie rule picks win:needs, so occurrence 9 gets A. In round 2, -1:car becomes an A rule, and occurrence 6, "the car plant closed", also gets A. Use a high threshold in line L4 and check the rules near the top of the list.
- **No smoothing.** With $\alpha = 0$ in line L3, a feature seen with only one sense has an infinite score, and every such rule is at the top of the list, whatever the number of occurrences behind it. Yarowsky 1995 reports that smoothing is crucial. Keep $\alpha > 0$.
- **Changing seed labels.** If line L4 lets the decision list relabel the seeded occurrences, the loop can drift away from the seeds. Keep the seed label in line L4 and skip seeded occurrences in line L5.
- **Stop test on the size only.** If line L6 stops when the number of labeled occurrences stops growing, it can stop while labels still change between senses. Compare the labels themselves.
- **No bound on the rounds.** Without the bound $T$ in line L2, nothing guarantees that the loop stops, since the update is not monotone.
- **Discourse boundaries.** Line L5 needs the document of each occurrence. If the whole corpus is one discourse, line L5 gives every unseeded occurrence the majority sense.

## Implementations

## History

Gale, Church and Yarowsky 1992 measured that an ambiguous word tends to keep one sense in one discourse. Yarowsky 1994 used decision lists ranked by log likelihood ratios for accent restoration, a task with the same structure as sense disambiguation. Yarowsky 1995 joined the two into the bootstrapping algorithm, tested it on 12 words over a corpus of 460 million words, and reported 96.5% average accuracy for the best setting with one sense per discourse, against 96.1% for a supervised decision list and 90.6% for seeds of two words without it. These are measurements on his test data. Abney 2004 gave the first analysis of what the algorithm optimizes.

## References
