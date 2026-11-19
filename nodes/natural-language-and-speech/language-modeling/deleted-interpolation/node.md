---
tag: S7TPCG
kind: algorithm
slug: deleted-interpolation
name: Deleted interpolation
aliases:
- held-out interpolation weights
area: natural-language-and-speech/language-modeling
level: core
summary: Mix the n-gram estimates of every order with weights fitted by EM on held-out data, often in buckets by the count of the history.
model: word-ram
complexity:
  vars: {n: the order of the model, N: the number of training tokens, K: the number of parts, I: the number of EM iterations}
  time: {worst: "Θ(n N (K + I))"}
  space: {extra: "Θ(n N)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1980
  people: [Frederick Jelinek, Robert L. Mercer]
  note: Jelinek and Mercer gave interpolated estimation with weights fitted on held-out data, and the deleted form that holds out each part of the training data in turn, for the language models of speech recognition at IBM.
prereqs: [n-gram-language-model, expectation-maximization, maximum-likelihood-estimation]
see_also: [jelinek-mercer-smoothing, witten-bell-smoothing, katz-backoff, kneser-ney-smoothing, cross-validation, interpolated-markov-model, perplexity, hidden-markov-model]
sources:
  - paper: "Frederick Jelinek and Robert L. Mercer, Interpolated estimation of Markov source parameters from sparse data, in E. S. Gelsema and L. N. Kanal (editors), Pattern Recognition in Practice, North-Holland, Amsterdam, 1980, pages 381 to 397"
    title: Jelinek and Mercer 1980
    locator: the interpolated estimate, the fit of its weights on held-out data, the deleted form, and the tying of the weights by the count of the history
  - paper: doi:10.1111/j.2517-6161.1977.tb01600.x
    title: Arthur P. Dempster, Nan M. Laird and Donald B. Rubin, Maximum likelihood from incomplete data via the EM algorithm, Journal of the Royal Statistical Society Series B 39(1), 1977
    locator: the EM algorithm and the proof that each step does not decrease the likelihood
  - paper: doi:10.1006/csla.1999.0128
    title: Stanley F. Chen and Joshua Goodman, An empirical study of smoothing techniques for language modeling, Computer Speech and Language 13(4), 1999, pages 359 to 394
    locator: Jelinek-Mercer smoothing with the weights bucketed by the count of the history, and its measured performance
  - book: isbn:9780262133609
    title: Christopher D. Manning and Hinrich Schütze, Foundations of Statistical Natural Language Processing, MIT Press, 1999
    locator: Chapter 6, Section 6.3 (combining estimators, with linear interpolation and its weights)
---

Deleted interpolation builds a smoothed [n-gram language model](/n-gram-language-model/) as a weighted mix of simpler estimates: the relative frequency of the word after the full history, after a shorter history, after no history, and a uniform guess. The weights are not set by hand. They are fitted by [expectation-maximization](/expectation-maximization/) to make held-out text as likely as possible, and in the "deleted" form each part of the training data is held out in turn, so that no data is set aside for good. Frederick Jelinek and Robert Mercer introduced it in 1980 for speech recognition. [Jelinek-Mercer smoothing](/jelinek-mercer-smoothing/) in retrieval is the same mix with one fixed weight and two components, and [Witten-Bell smoothing](/witten-bell-smoothing/) sets the weights from the counts with no held-out data at all.

## In plain words

You want to guess the next word. You have several advisers. One looks at the last two words, one at the last word only, one at no context, and one says every word is equally likely. The first is sharp but often has no data; the last is never wrong by zero but never sharp. You mix their answers with weights.

To pick the weights, hide some text from the advisers, let them guess it, and see how much each one helped on each word. Give each adviser a weight equal to its average share of the credit, and repeat until the weights stop changing. Then show the advisers all the text, and keep the weights. Because the sharp adviser is reliable only when its context was seen often, use a separate set of weights for contexts seen once, a few times, or many times.

## The problem

The training text is a list of sentences, each padded with $n - 1$ start markers `<s>` on the left and one `</s>` on the right. The vocabulary $V$ holds every predicted token, with `</s>` and `<unk>`. For a history $h$ of $n - 1$ tokens, write $h_j$ for its last $j$ tokens, so $h_0 = \epsilon$. Let $p_j(w \mid h) = c(h_j w)/c(h_j)$ be the maximum likelihood estimate of order $j + 1$, defined when $c(h_j) > 0$, and $p_{\mathrm{u}}(w) = 1/|V|$. Let $m(h)$ be the largest $j$ with $c(h_j) > 0$. The model is

$$P(w \mid h) = \sum_{j=0}^{m(h)} \lambda_{b,j} \, p_j(w \mid h) + \lambda_{b,\mathrm{u}} \, \frac{1}{|V|}, \qquad b = b(h),$$

with weights $\lambda_{b,\cdot} \ge 0$ that sum to 1 in each bucket $b$. The bucket groups histories that should share weights. Here $b(h)$ is the pair of $m(h)$ and the number of bits of $c(h_{m(h)})$, so the histories seen once, two or three times, four to seven times, and so on, get their own weights. The task is to choose the weights that maximize the likelihood of text not used for the counts.

## The algorithm

Cut the training sentences into $K$ parts $B_1, \ldots, B_K$. For each part, count the other parts and record, for each token of the part, its bucket and the values of its components. Then run EM on all these rows together.

```pseudo id=main
DELETED-INTERPOLATION(B_1 .. B_K, n)
L1  for j ← 1 to K do
L2      count the n-grams of every part except B_j
L3      for each token w after history h in B_j do add the row (b(h), p_m(w|h), ..., p_0(w|h), 1/|V|) to R
L4  for each bucket b do give each of its components the weight 1 / (its number of components)
L5  repeat
L6      for each row (b, p) of R do z ← Σ_i λ_{b,i} p_i; e_{b,i} ← e_{b,i} + λ_{b,i} p_i / z for each i
L7      for each bucket b and component i do λ_{b,i} ← e_{b,i} / |R_b|; e_{b,i} ← 0
L8  until the log likelihood Σ_rows log z rises by less than a tolerance
L9  count all the parts; return P(w | h) = Σ_i λ_{b(h),i} p_i(w | h)
```

Lines L1 to L3 are the "deleted" part: each token is scored by counts that do not include its own part. Line L6 is the E step: $\lambda_{b,i} p_i / z$ is the posterior chance that component $i$ produced the token. Line L7 is the M step: the new weight is the average posterior. Line L9 builds the final model from the counts of the whole text. With $K = 1$ and a separate held-out set in place of the loop, this is plain held-out interpolation.

## Example

Take one bucket with two components, a bigram estimate and a unigram estimate, and three held-out tokens whose component values are $(1/2, 1/4)$, $(0, 1/8)$ and $(1, 1/2)$. Write $\lambda$ for the weight of the bigram. The log likelihood is

$$L(\lambda) = \log \frac{1 + \lambda}{4} + \log \frac{1 - \lambda}{8} + \log \frac{1 + \lambda}{2}.$$

Start at $\lambda = 1/2$. The posteriors of the bigram are $\frac{1/4}{3/8} = 2/3$, $0$ and $\frac{1/2}{3/4} = 2/3$, so the M step gives $\lambda = (2/3 + 0 + 2/3)/3 = 4/9$. The next step gives $16/39 = 0.410$. In general one step maps $\lambda$ to $\frac{4\lambda}{3(1+\lambda)}$, and the steps converge to $\lambda = 1/3$, where $L'(\lambda) = \frac{2}{1+\lambda} - \frac{1}{1-\lambda} = 0$. There the three tokens get $1/3$, $1/12$ and $2/3$, for a product of $1/54$. The bigram alone ($\lambda = 1$) gives the second token 0, and the unigram alone gives the product $1/64$.

## Correctness

**Every row is a distribution.** Each component $p_j(\cdot \mid h)$ with $j \le m(h)$ sums to 1 over $V$, because all its counts are of tokens in $V$, and the uniform component sums to 1. The weights of a bucket are nonnegative and sum to 1, since line L7 divides the posteriors, which sum to 1 per row, by the number of rows. So $P(\cdot \mid h)$ is a convex combination of distributions. It has no zeros as long as $\lambda_{b,\mathrm{u}} > 0$, which holds after every EM step from a start with all weights positive.

**EM never lowers the held-out likelihood.** By [Jensen's inequality](/jensens-inequality/), $L(\lambda') - L(\lambda) \ge |R| \, D(\lambda' \,\|\, \lambda) \ge 0$ in each bucket, where $D$ is the [Kullback-Leibler divergence](/kullback-leibler-divergence/) of the new weights from the old. The log likelihood $\sum \log \sum_i \lambda_{b,i} p_i$ is concave in the weights, so every point where no component can gain (the mean of $p_i / z$ is 1 for each weight in use and at most 1 for the others) is a global maximum, and the fixed points of EM with all weights positive are such points.

## Complexity

Counting the $K$ folds takes $\Theta(n N)$ expected time each, with a [hash table](/hash-table/), so $\Theta(K n N)$ in all. There are $N$ rows of at most $n + 1$ components, and one EM iteration takes $\Theta(n N)$ time, so $I$ iterations take $\Theta(I n N)$. The rows take $\Theta(n N)$ space. The final model is a count table of size $\Theta(n N)$ and the weights, and one query takes $\Theta(n)$ expected time. EM can be slow near the end: in the example the error shrinks by a factor of about $3/4$ per step.

## Properties

- **Data decides the mix.** The weights are maximum likelihood estimates on held-out text, so they reflect how reliable each order is on new data.
- **No zeros.** The uniform component gives every word of $V$ some probability.
- **Weights tied by buckets.** Histories seen the same number of times share weights, which keeps the number of parameters small: a few dozen numbers for the whole model.
- **Interpolated.** Every n-gram, seen or not, gets mass from all lower orders.
- **The deleted form uses all data.** Every token is held out once, so no part of the text is lost to the counts of the final model.
- **Floating point.** The weights come from an iterative method, so they are not exact.

## Variants and improvements

- **Held-out interpolation.** Fit the weights on one held-out set and use only the rest for counts. It is simpler but wastes data.
- **The recursive form.** $P(w \mid h) = \lambda(h) p_{\mathrm{ML}}(w \mid h) + (1 - \lambda(h)) P(w \mid h')$, with one weight per bucket and order. Expanded, it is a mix of the same kind, with products of weights. This is the form of [Jelinek-Mercer smoothing](/jelinek-mercer-smoothing/) in Chen and Goodman (1999).
- **Weights from counts.** [Witten-Bell smoothing](/witten-bell-smoothing/) uses the weight $c(h)/(c(h) + T(h))$ and needs no held-out data.
- **Bucket rules.** Chen and Goodman bucketed by the average count per non-zero word, $c(h)/T(h)$, which worked better than the count $c(h)$ alone.
- **Grid or gradient search.** With few weights, a direct search over the held-out [perplexity](/perplexity/) gives the same optimum as EM.
- **Other models.** The same EM fits the weights of any mixture of fixed models, such as an [interpolated Markov model](/interpolated-markov-model/) of DNA or a [cache language model](/cache-language-model/).

## When to use it

Use it when you have several estimates of the same distribution with different detail and you can afford to hold out text: word n-gram models, character models, models of DNA sequences, or mixtures of a general and a topic model. It is a good baseline that needs no tuning by hand. On word n-grams, [Kneser-Ney smoothing](/kneser-ney-smoothing/) is usually better, because it also changes the lower-order distributions.

## Pitfalls

- **Fitting the weights on the training text.** On the text that gave the counts, the highest order already maximizes the likelihood, so EM puts all the weight on it and the model has zeros again. The data for the weights must be held out.
- **Unseen histories.** If $c(h_j) = 0$, $p_j$ is $0/0$. Drop the component and use the bucket of the longest seen history, as above, so that the weights of each bucket refer to the same components.
- **Empty buckets.** A bucket with no held-out rows has no fitted weights. Use equal weights or merge it with a neighbour.
- **Zero weights stay zero.** EM cannot move a weight that is exactly 0. Start every weight above 0.
- **Slow convergence.** Stop on a small change of the log likelihood, not on a fixed small number of steps.

## Implementations

## History

Frederick Jelinek and Robert Mercer described interpolated estimation of Markov source parameters at a workshop on pattern recognition in practice in 1980, from their work on speech recognition at IBM. They fitted the weights by the forward-backward method of [hidden Markov models](/hidden-markov-model/), since a mixture is the same as a hidden choice of the component, and they tied the weights of histories with similar counts. The deleted form, which holds out each block of the training data in turn, gave the method its name. Chen and Goodman (1999) compared it, as Jelinek-Mercer smoothing, with the other classical methods.

## References
