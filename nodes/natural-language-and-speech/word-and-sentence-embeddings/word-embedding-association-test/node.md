---
tag: R1EFZ2
kind: algorithm
slug: word-embedding-association-test
name: Word embedding association test
aliases:
- WEAT
area: natural-language-and-speech/word-and-sentence-embeddings
level: advanced
summary: Measure bias in embeddings by the difference of mean cosine similarities of two target word sets to two attribute sets, with a permutation test.
model: real-ram
complexity:
  vars: {n: the size of each target set, a: the total size of the two attribute sets, d: the dimension of the vectors, m: the number of sampled partitions}
  time: {exact: "O(n a d + n 4^n)", sampled: "O(n a d + m n)"}
  space: {extra: "O(n)"}
properties: {deterministic: true, exact: true, online: false, recursive: false, supervised: false}
history:
  year: 2017
  people: [Aylin Caliskan, Joanna J. Bryson, Arvind Narayanan]
  note: Caliskan, Bryson and Narayanan carried the Implicit Association Test of psychology over to word vectors and found in GloVe the same associations that people show in the test.
prereqs: [word-embedding, cosine-similarity, permutation-test]
see_also: [effect-size, p-value, hard-debiasing, glove, skip-gram-model, contextual-word-embedding, bootstrap-method, word-analogy]
sources:
  - paper: doi:10.1126/science.aal4230
    title: Aylin Caliskan, Joanna J. Bryson and Arvind Narayanan, Semantics derived automatically from language corpora contain human-like biases, Science 356(6334), 2017, pages 183 to 186
    locator: the methods section that defines s(w, A, B), the test statistic, the permutation p-value and the effect size, and the table of the replicated tests
  - paper: doi:10.1037/0022-3514.74.6.1464
    title: Anthony G. Greenwald, Debbie E. McGhee and Jordan L. K. Schwartz, Measuring individual differences in implicit cognition, the implicit association test, Journal of Personality and Social Psychology 74(6), 1998
    locator: the flower and insect, instrument and weapon, and other tests that WEAT replicates
  - paper: doi:10.18653/v1/N19-1061
    title: Hila Gonen and Yoav Goldberg, Lipstick on a pig, debiasing methods cover up systematic gender biases in word embeddings but do not remove them, NAACL-HLT 2019, pages 609 to 614
    locator: the WEAT p-values of the embeddings after hard debiasing
  - paper: "Chandler May, Alex Wang, Shikha Bordia, Samuel R. Bowman and Rachel Rudinger, On measuring social biases in sentence encoders, NAACL-HLT 2019"
    title: May et al. 2019
    locator: SEAT, the extension of WEAT to sentence encoders
---

The word embedding association test (WEAT) measures whether a set of [word vectors](/word-embedding/) puts one group of target words closer to one group of attribute words than another group of target words. For example, it asks whether flower names lie closer to pleasant words, and insect names closer to unpleasant words, than the other way around. It gives a test statistic, an [effect size](/effect-size/) and a one-sided [p-value](/p-value/) from a [permutation test](/permutation-test/) over the ways to split the target words into two groups. The p-value is exact when all splits are listed; what the test says about bias in people or in applications is a matter of interpretation, not of the algorithm.

## In plain words

Psychologists measure hidden associations with a timed test: people sort words faster when two concepts that they link in their minds share a response key. WEAT does the same with distances. Each target word, such as "rose" or "ant", gets a score: how much closer it is to the pleasant words than to the unpleasant words, on average. The test adds the scores of the flowers and takes away the scores of the insects. A big result means that the two target groups differ in their links to the two attribute groups.

To know whether the result is just chance, the test mixes the flowers and the insects, splits them into two new groups at random, and computes the same number. If few random splits give a number as large as the real one, the link is unlikely to be chance.

## The problem

The input is four sets of vectors: two target sets $X$ and $Y$ with $n$ words each, and two attribute sets $A$ and $B$. The association of one word $w$ with the attributes is

$$s(w, A, B) = \frac{1}{|A|} \sum_{a \in A} \cos(w, a) - \frac{1}{|B|} \sum_{b \in B} \cos(w, b),$$

with the [cosine similarity](/cosine-similarity/). The test statistic is

$$s(X, Y, A, B) = \sum_{x \in X} s(x, A, B) - \sum_{y \in Y} s(y, A, B).$$

The effect size is

$$d = \frac{\operatorname{mean}_{x \in X} s(x, A, B) - \operatorname{mean}_{y \in Y} s(y, A, B)}{\operatorname{std}_{w \in X \cup Y} s(w, A, B)}.$$

Let $(X_i, Y_i)$ range over the $\binom{2n}{n}$ splits of $X \cup Y$ into two sets of $n$ words. The one-sided p-value of the paper is $p = \Pr_i[s(X_i, Y_i, A, B) > s(X, Y, A, B)]$. The output is the triple of the statistic, $d$ and $p$.

## The algorithm

```pseudo id=main
WEAT(X, Y, A, B)
L1  s_w ← s(w, A, B)   for each w in X ∪ Y, with the n words of X first
L2  T ← Σ_w s_w
L3  S ← 2 Σ_{x ∈ X} s_x - T                 ▷ the statistic s(X, Y, A, B)
L4  σ ← standard deviation of the 2n values s_w
L5  d ← (mean of s_x over X - mean of s_y over Y) / σ
L6  count ← 0
L7  for each set X_i of n positions out of the 2n do
L8      S_i ← 2 Σ_{w ∈ X_i} s_w - T          ▷ the statistic of the split (X_i, Y_i)
L9      if S_i > S then count ← count + 1
L10     (the loop visits C(2n, n) splits)
L11 return S, d, count / C(2n, n)
```

The associations do not depend on the split, so line L1 computes them once. Line L8 uses the identity $\sum_{Y_i} s_w = T - \sum_{X_i} s_w$, so each split costs $O(n)$ and no cosine is computed again. When $\binom{2n}{n}$ is too large to list, the code draws $m$ random splits with a seeded generator and returns the fraction above $S$. For the 25 flowers and 25 insects of the paper, $\binom{50}{25}$ is about $1.3 \times 10^{14}$, so sampling is the only option there.

## Example

The vectors below are written for this page, in two dimensions. Let $A = \{(1, 0)\}$ be the pleasant attribute and $B = \{(0, 1)\}$ the unpleasant one, so $s(w, A, B) = (w_1 - w_2) / \|w\|$.

| set | word vector | $s(w, A, B)$ |
| --- | --- | --- |
| X | (4, 1) | 0.7276 |
| X | (3, 2) | 0.2774 |
| X | (1, 3) | -0.6325 |
| Y | (2, 3) | -0.2774 |
| Y | (1, 4) | -0.7276 |
| Y | (0, 1) | -1.0000 |

The statistic is $0.3725 - (-2.0050) = 2.3775$. The means are $0.1242$ and $-0.6683$, and the population standard deviation of the six values is $0.6012$, so $d = 0.7925 / 0.6012 = 1.3182$ (with the sample standard deviation, $d = 1.2034$). There are $\binom{6}{3} = 20$ splits. Only one gives a larger statistic: the split that swaps $(1, 3)$ with $(2, 3)$, with $3.0877$. So $p = 1/20 = 0.05$. With "$\ge$" in line L9 the observed split also counts and $p = 2/20 = 0.1$.

## Correctness

Three exact statements hold, and the proof below gives them. First, line L8 computes the statistic of each split, since $s(X_i, Y_i, A, B) = 2\sum_{X_i} s_w - T$. Second, the loop of line L7 visits every split once, so line L11 returns the p-value of the definition exactly. The fraction is the same over the $(2n)!$ orders of the words, since each split comes from $n! \, n!$ orders. Third, with the population standard deviation, $|d| \le 2$, with equality only when the associations are constant inside $X$ and inside $Y$. This follows from the variance decomposition $\sigma^2 = (\sigma_X^2 + \sigma_Y^2)/2 + ((m_X - m_Y)/2)^2$. The draft of the paper notes that the largest effect size is 2.

The p-value is valid as a permutation test: if, under the null hypothesis, the labels X and Y fall on the $2n$ words as a uniform random split, then the "$\ge$" form gives $\Pr[p \le \alpha] \le \alpha$. The strict form of the paper is never larger, so it rejects a little more often. The null hypothesis is about the given vectors with the given word lists. It is not a statement about a population of words, and the choice of the lists is not random.

## Complexity

The model is the [real-RAM](/real-ram/).

- **Associations.** Line L1 computes $2n \cdot a$ cosines of dimension $d$: $O(n a d)$ time.
- **Exact p-value.** Lines L7 to L10 visit $\binom{2n}{n}$ splits at $O(n)$ each. For $n = 8$ that is 12,870 splits, and $\binom{2n}{n}$ grows like $4^n / \sqrt{\pi n}$, which gives the bound $O(n 4^n)$ of the front matter.
- **Sampled p-value.** $O(m n)$ for $m$ splits. The standard error of the estimate is about $\sqrt{p(1 - p)/m}$.
- **Space.** $O(n)$ beyond the input, for the $2n$ associations.

## Properties

- **Exact test.** For small sets the p-value is exact, with no assumption on the distribution of the associations.
- **Resolution.** With "$\ge$" the smallest p-value is $1/\binom{2n}{n}$: $1/70$ for $n = 4$ and $1/12870$ for $n = 8$. With the strict test of the paper the observed split never counts, so $p = 0$ is possible.
- **Sign.** Swapping $X$ and $Y$, or $A$ and $B$, negates the statistic and $d$.
- **Scale.** Cosines ignore the length of the vectors, so the test does too.
- **Bounded effect size.** $|d| \le 2$, as above. The paper reports effect sizes and p-values, not only p-values, since a large $n$ makes small differences significant.

## Variants and improvements

- **WEFAT.** The word embedding factual association test of the same paper uses one target set and correlates $s(w, A, B)$ with a real statistic of each word, such as the share of women in an occupation.
- **SEAT.** May et al. 2019 put the words into simple sentence templates, such as "This is a rose.", and run the test on the vectors of sentence encoders. See [sentence embedding](/sentence-embedding/) and [contextual word embedding](/contextual-word-embedding/).
- **Sampled test.** Random splits replace the full list for large $n$. Adding 1 to the count and to the number of splits makes the sampled p-value valid in the same sense as the exact one.
- **Bootstrap intervals.** A [bootstrap](/bootstrap-method/) over the words of the lists gives an interval for $d$. It shows how much the result depends on the particular words.

## When to use it

Use WEAT to report whether a given embedding encodes a stated association, for example after a debiasing step. Gonen and Goldberg 2019 used it after [hard debiasing](/hard-debiasing/) and still measured p-values below 0.05 in all three of the gender tests they ran. Report the word lists, the embedding, the effect size and the p-value together. The test does not tell how a downstream system behaves; that needs a test of the system itself.

## Pitfalls

- **Unequal target sets.** The definition and the identity of line L8 assume $|X| = |Y|$. The code raises an error for unequal sizes rather than give a number with another meaning.
- **Words missing from the vocabulary.** Dropping the missing words of one list changes the test. Report the final lists.
- **Standard deviation.** The paper does not state which of the two forms it uses. The population form gives the bound 2; the sample form gives a smaller value for the same data. Say which one you use.
- **Multiple tests.** Running many WEATs and reporting the significant ones inflates the false positives. Correct for the number of tests.
- **Strict and non-strict tests.** With "$>$" and a small $n$, $p = 0$ can appear, which reads as stronger evidence than the data allow. The "$\ge$" form never goes below $1/\binom{2n}{n}$.
- **Word frequency.** Rare words have noisier vectors, and names in particular differ in frequency. A large effect can come from frequency rather than from meaning.

## Implementations

The code takes the word vectors as given and implements the association, the statistic, the effect size, the exact p-value over all splits and a sampled p-value with a seeded generator.

## History

Greenwald, McGhee and Schwartz 1998 introduced the Implicit Association Test, which measures associations through the reaction times of people. Caliskan, Bryson and Narayanan 2017 replaced the reaction times with cosine similarities and replicated the classic tests on GloVe vectors trained on 840 billion tokens of Common Crawl text (2.2 million words, 300 dimensions). In their measurements, flowers against insects with pleasant and unpleasant words gave $d = 1.50$ with $p < 10^{-7}$, musical instruments against weapons gave $d = 1.53$ with $p < 10^{-7}$, and male against female names with career and family words gave $d = 1.81$ with $p < 10^{-3}$. These are measurements on one embedding. The test then became a standard measure of bias in embeddings and was extended to sentence encoders.

## References
