---
tag: V3AY2H
kind: definition
slug: pointwise-mutual-information
name: Pointwise mutual information
aliases:
- PMI
area: natural-language-and-speech/word-and-sentence-embeddings
level: intro
summary: PMI(x, y) = log P(x, y) / (P(x) P(y)), the log ratio of how often two events occur together to how often they would if independent.
prereqs: [self-information]
see_also: [positive-pointwise-mutual-information, word-context-matrix, kullback-leibler-divergence, shannon-entropy, brown-clustering, likelihood-ratio-test, sgns-implicit-factorization-theorem, cosine-similarity]
sources:
  - paper: "Kenneth Ward Church and Patrick Hanks, Word association norms, mutual information, and lexicography, Computational Linguistics 16(1), 1990, pages 22 to 29"
    title: Church and Hanks 1990
    locator: the association ratio, with logarithms to base 2, counts of ordered pairs within a window of 5 words, pairs with counts of 5 or less left out, and values above 3 read as interesting
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Chapter 2, the definition of mutual information as the expected value of log p(x, y) / (p(x) p(y)) and its nonnegativity
  - paper: "Omer Levy, Yoav Goldberg and Ido Dagan, Improving distributional similarity with lessons learned from word embeddings, Transactions of the ACL 3, 2015, pages 211 to 225"
    title: Levy, Goldberg and Dagan 2015
    locator: PMI and its variants as weightings of the word-context matrix, and the bias of PMI toward rare contexts
---

Pointwise mutual information compares how often two events occur together with how often they would occur together if they were independent. For events $x$ and $y$ it is $\log \frac{P(x, y)}{P(x) P(y)}$. It is positive when the two occur together more often than chance, zero when they are independent, and negative when they avoid each other. In language processing the events are a word and a context, and PMI is the standard weighting of a [word-context matrix](/word-context-matrix/): it lowers the weight of frequent contexts such as "the", which occur with every word. Church and Hanks 1990 brought it to lexicography as the association ratio. Its expected value over all pairs is the mutual information of two random variables, which is where the name comes from.

## Definition

Let $X$ and $Y$ be random variables with a joint distribution $P$, and let $x$ and $y$ be values with $P(x) > 0$ and $P(y) > 0$. The **pointwise mutual information** of $x$ and $y$ is

$$ \operatorname{PMI}(x, y) = \log \frac{P(x, y)}{P(x)\, P(y)} = \log \frac{P(y \mid x)}{P(y)} = \log \frac{P(x \mid y)}{P(x)}, $$

with the value $-\infty$ when $P(x, y) = 0$. The base of the logarithm is the unit: base 2 gives bits, as in Church and Hanks, and base $e$ gives nats. A page or paper that reports values must state the base.

From a [word-context matrix](/word-context-matrix/) $M$ with total $N$, the maximum likelihood estimate is

$$ \operatorname{PMI}(w, c) = \log_2 \frac{M[w, c] \cdot N}{M[w, *] \cdot M[*, c]} \quad \text{(bits)}. $$

These facts follow from the definition.

- **Independence.** $\operatorname{PMI}(x, y) = 0$ exactly when $P(x, y) = P(x) P(y)$.
- **Upper bound.** Since $P(x \mid y) \le 1$, $\operatorname{PMI}(x, y) \le -\log P(x)$, and in the same way $\operatorname{PMI}(x, y) \le -\log P(y)$. So PMI is at most the [self-information](/self-information/) of the more probable of the two events, with equality when that event always occurs with the other one. There is no lower bound.
- **Symmetry.** $\operatorname{PMI}(x, y) = \operatorname{PMI}(y, x)$ when both are computed from the same joint distribution. The association ratio of Church and Hanks counts ordered pairs, $x$ followed by $y$ within 5 words, so it is not symmetric.
- **Expectation.** $\sum_{x, y} P(x, y) \operatorname{PMI}(x, y) = I(X; Y)$, the mutual information, which is the [Kullback-Leibler divergence](/kullback-leibler-divergence/) of $P$ from the product of its marginals and so is at least 0. Single values of PMI can be negative, but their average under $P$ cannot.

## Examples and non-examples

**The check value.** If $P(x, y) = 1/10$, $P(x) = 1/5$ and $P(y) = 1/4$, then $\frac{P(x, y)}{P(x) P(y)} = \frac{1/10}{1/20} = 2$, and $\operatorname{PMI}(x, y) = \log_2 2 = 1$ bit, or $\ln 2 \approx 0.6931$ nats. The two events occur together twice as often as independence predicts.

**A small matrix.** A word-context matrix, written for this page, with $N = 40$:

| word | pet | fur | road | the | row sum |
| --- | --- | --- | --- | --- | --- |
| cat | 4 | 3 | 0 | 5 | 12 |
| dog | 5 | 2 | 1 | 6 | 14 |
| car | 0 | 0 | 6 | 8 | 14 |
| column sum | 9 | 5 | 7 | 19 | 40 |

The PMI values in bits, with the ratio $\frac{M[w, c] N}{M[w, *] M[*, c]}$ in brackets:

| word | pet | fur | road | the |
| --- | --- | --- | --- | --- |
| cat | 0.5670 (40/27) | 1.0000 (2) | $-\infty$ (0) | $-0.1890$ (50/57) |
| dog | 0.6666 (100/63) | 0.1926 (8/7) | $-1.2928$ (20/49) | $-0.1484$ (120/133) |
| car | $-\infty$ (0) | $-\infty$ (0) | 1.2922 (120/49) | 0.2666 (160/133) |

"Cat" and "fur" occur together twice as often as chance, which is 1 bit. The context "the" has the largest counts in every row, but its PMI is near 0 in every row, since it occurs with every word. The pairs never seen get $-\infty$.

**Rare pairs.** If a word and a context each occur once in the matrix, and together, then the ratio is $1 \cdot N / (1 \cdot 1) = N$ and PMI is $\log_2 N$, which by the upper bound is the largest value any pair can have in that matrix. With $N = 40$ it is 5.32 bits, more than every value in the table above, from one observation. This is why PMI is biased toward rare events, and why Church and Hanks left out pairs seen 5 times or less.

**Not: mutual information.** $I(X; Y)$ is one number for two random variables, the average of PMI over all pairs. PMI is a value for one pair. A pair with negative PMI does not make $I$ negative.

**Not: a probability or a similarity.** PMI has no fixed range, and its maximum depends on the frequencies of the two events, so a value of 3 bits means more for two frequent words than for two rare ones. Its values are not comparable across pairs of very different frequency without a correction.

## Related definitions

- **PPMI.** [Positive PMI](/positive-pointwise-mutual-information/) replaces the negative values and $-\infty$ by 0, which gives a sparse matrix that works better for word similarity.
- **Normalized PMI.** Dividing by $-\log P(x, y)$ maps PMI to the range $[-1, 1]$, with 1 when the two events always occur together and $-1$ when they never do.
- **Shifted PMI.** $\operatorname{PMI}(w, c) - \log k$ is, under some assumptions, the matrix that skip-gram with $k$ negative samples factorizes (see the [factorization theorem](/sgns-implicit-factorization-theorem/)).
- **Mutual information and entropy.** $I(X; Y) = H(X) + H(Y) - H(X, Y)$ with the [Shannon entropy](/shannon-entropy/) $H$. [Brown clustering](/brown-clustering/) keeps the mutual information of the classes of adjacent words as high as possible.
- **Other association measures.** The [likelihood ratio test](/likelihood-ratio-test/) and the t-test also score how strongly two words go together. They take the size of the sample into account, so a pair seen once does not get the top score.
- **Information gain of one event.** The form $\log \frac{P(y \mid x)}{P(y)}$ reads PMI as the change in the log probability of $y$ when $x$ is observed, the difference of two [self-information](/self-information/) values, $-\log P(y) - (-\log P(y \mid x))$.

## References
