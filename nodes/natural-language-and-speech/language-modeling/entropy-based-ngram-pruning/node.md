---
tag: AG7MBF
kind: algorithm
slug: entropy-based-ngram-pruning
name: Entropy-based n-gram pruning
aliases:
- Stolcke pruning
- relative entropy pruning
area: natural-language-and-speech/language-modeling
level: advanced
summary: "Remove the n-grams whose removal least raises the relative entropy between the original and pruned backoff models, below a threshold."
model: word-ram
complexity:
  vars: {n: the order of the model, E: the number of explicit n-grams, N: the number of predicted training tokens}
  time: {prune: "Θ(n E)"}
  space: {extra: "Θ(E)"}
properties: {deterministic: true, exact: false, online: false, greedy: true}
history:
  year: 1998
  people: [Andreas Stolcke]
  note: Stolcke gave the criterion and its closed form at the DARPA Broadcast News workshop in 1998. Seymore and Rosenfeld had pruned with a weighted difference of log probabilities in 1996.
prereqs: [katz-backoff, kullback-leibler-divergence]
see_also: [katz-backoff, n-gram-language-model, kullback-leibler-divergence, perplexity, kneser-ney-smoothing, absolute-discounting, stupid-backoff, neural-network-pruning]
sources:
  - paper: "Andreas Stolcke, Entropy-based pruning of backoff language models, Proceedings of the DARPA Broadcast News Transcription and Understanding Workshop, 1998, pages 270 to 274, arXiv:cs/0006025"
    title: Stolcke 1998
    locator: the pruning criterion (equation 2 for the relative entropy of one removal, the new backoff weight and the threshold on the relative perplexity increase), Section 4 (the Broadcast News results), Section 5 (the comparison with Seymore and Rosenfeld)
  - paper: "Kristie Seymore and Ronald Rosenfeld, Scalable backoff language models, Proceedings of ICSLP 1996, volume 1, pages 232 to 235"
    title: Seymore and Rosenfeld 1996
    locator: the weighted difference criterion for pruning n-grams from a backoff model
---

Entropy-based pruning makes a backoff [n-gram language model](/n-gram-language-model/) smaller with the least possible loss. A backoff model stores an explicit probability for each seen n-gram and falls back to a shorter history for the rest. Many explicit n-grams are almost useless: the backoff estimate would give them nearly the same probability. Stolcke measured the cost of removing one n-gram as the [relative entropy](/kullback-leibler-divergence/) between the model before and after, gave a closed form for it that needs only a few sums per history, and removed every n-gram whose cost is below a threshold. On Broadcast News a trigram model kept 26 percent of its size with no loss in word error rate.

## In plain words

A backoff model remembers a number for each word sequence it saw. If it has no number for a sequence, it makes a guess from a shorter sequence.

For each stored number, ask: if I forget it and use the guess instead, how much worse does the model get? The answer has a precise measure, and it can be computed fast, because only the guesses after one history change.

Forget every number for which the answer is very small. Then fix the weights of the guesses so that the chances add up to one again. The model gets much smaller and predicts almost as well.

## The problem

The input is a backoff model in the form of [Katz backoff](/katz-backoff/): for each history $h$ of length 1 to $n - 1$ it has a set $E(h)$ of explicit words with stored probabilities $p^*(w \mid h)$, and

$$p(w \mid h) = p^*(w \mid h) \text{ if } w \in E(h), \qquad p(w \mid h) = \alpha(h)\, p(w \mid h') \text{ otherwise},$$

where $h'$ is $h$ without its first token and $\alpha(h)$ makes the row sum to 1. With $S_1(h) = \sum_{v \in E(h)} p^*(v \mid h)$ and $S_2(h) = \sum_{v \in E(h)} p(v \mid h')$,

$$\alpha(h) = \frac{1 - S_1(h)}{1 - S_2(h)}.$$

The unigrams are never removed. The task is to remove explicit n-grams so that the model gets small while its distribution stays close to the original. Stolcke measures closeness with the relative entropy of the joint models,

$$D(p \parallel p') = \sum_h p(h) \sum_w p(w \mid h) \ln \frac{p(w \mid h)}{p'(w \mid h)}.$$

Finding the best subset of a given size is a hard combinatorial problem, so the method scores each n-gram alone and uses a threshold.

## The algorithm

Removing $h w$ alone changes only the row of $h$: $w$ moves from the explicit set to the backed off set, and the weight becomes $\alpha'(h)$. All costs are computed on the original model, then the marked n-grams are removed together.

```pseudo id=main
PRUNE(model p, threshold θ)
L1  for each explicit n-gram h w of order 2 or more:
L2      p(h) ← the probability of h by the chain rule of p
L3      α'(h) ← (1 - S_1(h) + p*(w | h)) / (1 - S_2(h) + p(w | h'))
L4      B ← α(h) (1 - S_2(h))         ▷ the total probability of the backed off words of h
L5      D ← p(h) [ p*(w | h) ln( p*(w | h) / (α'(h) p(w | h')) ) + B ln( α(h) / α'(h) ) ]
L6      if e^D - 1 < θ then mark h w
L7  remove the marked n-grams and recompute α(h) for every h
```

Line L2 multiplies the model probabilities of the tokens of $h$, each after the tokens before it; leading <s> pads count as 1. Lines L3 and L4 use $S_1(h)$ and $S_2(h)$, which are computed once per history. Line L5 is the relative entropy of the row of $h$, weighted by $p(h)$. Line L6 compares the relative increase of the [perplexity](/perplexity/), $e^D - 1$, with $\theta$.

The implementation builds the input model from a corpus with [absolute discounting](/absolute-discounting/), $p^*(w \mid h) = (c(h w) - d)/c(h)$ for every seen n-gram and $d = 1/2$, and keeps the unigram undiscounted. It computes the costs from exact fractions and takes the logs in floats.

## Example

Take the four sentences "a b", "a c", "b c" and "a b" with $n = 2$ and $d = 1/2$. The 12 predicted tokens give the unigram $p(\text{a}) = p(\text{b}) = 1/4$, $p(\text{c}) = 1/6$ and $p(\text{</s>}) = 1/3$. After a, the bigram a b was seen twice and a c once, so $p^*(\text{b} \mid \text{a}) = 1/2$, $p^*(\text{c} \mid \text{a}) = 1/6$ and

$$\alpha(\text{a}) = \frac{1 - 2/3}{1 - (1/4 + 1/6)} = \frac47.$$

To remove a c: $\alpha'(\text{a}) = (1 - 1/2)/(1 - 1/4) = 2/3$, so c would get $\frac23 \cdot \frac16 = \frac19$ instead of $\frac16$. The backed off words a and </s> have $B = 1/3$, and $p(\text{a}) = 1/4$ as a history. So

$$D = \frac14 \left[ \frac16 \ln \frac{1/6}{1/9} + \frac13 \ln \frac{4/7}{2/3} \right] \approx 0.004048.$$

All seven explicit bigrams:

| n-gram | $p(h)$ | $p^*(w \mid h)$ | $D$ | $e^D - 1$ |
|---|---|---|---|---|
| <s> a | 1 | 5/8 | 0.264513 | 0.302796 |
| <s> b | 1 | 1/8 | 0 | 0 |
| a b | 1/4 | 1/2 | 0.040009 | 0.040820 |
| a c | 1/4 | 1/6 | 0.004048 | 0.004057 |
| b </s> | 1/4 | 1/2 | 0.016894 | 0.017038 |
| b c | 1/4 | 1/6 | 0.002172 | 0.002174 |
| c </s> | 1/6 | 3/4 | 0.060498 | 0.062366 |

The bigram <s> b costs nothing: after its removal $\alpha'(\text{<s>}) \cdot p(\text{b}) = \frac12 \cdot \frac14 = \frac18$, which is the stored value. With $\theta = 0.01$ the bigrams <s> b, a c and b c are removed. The new weights are $\alpha(\text{a}) = 2/3$ and $\alpha(\text{b}) = 3/4$, every row still sums to 1, and the perplexity of the training text goes from about 2.383 to about 2.525.

## Correctness

The proof in the proofs file has four parts. Every row of the model sums to 1 and is positive, for the full model and for every pruned model, because $S_1(h) < 1$ when $d > 0$ and $S_2(h) < 1$ when some word is not explicit. Removing $h w$ changes no row of a history of length at most $|h|$ except the row of $h$, so the lower probabilities in line L5 are the same before and after. Splitting the relative entropy of the row of $h$ into the explicit words, $w$ and the backed off words gives the closed form of line L5, since the explicit words keep their values and every backed off word changes by the same ratio $\alpha/\alpha'$. Finally, $\theta = 0$ prunes nothing, a larger $\theta$ prunes a superset, and the costs add up when the removed top order n-grams have different histories.

## Complexity

With $S_1$, $S_2$ and $p(h)$ cached for each history, each explicit n-gram costs a constant number of lookups plus $O(n)$ for the chain rule of $p(h)$, so the costs take $\Theta(n E)$ expected time with [hash tables](/hash-table/), for $E$ explicit n-grams. Recomputing the weights in line L7 sums the explicit words of each history once, $\Theta(E)$ more. The extra space is $\Theta(E)$ for the costs and the cached sums.

## Properties

- **Greedy and one-pass.** Every cost is computed on the original model and the n-grams are not ranked against each other; the joint effect of the removals is not computed.
- **A perplexity bound per n-gram.** $e^D - 1$ is the relative increase of the perplexity on text drawn from the model, so $\theta$ has a direct meaning.
- **Exact for one top order n-gram.** For an n-gram of the top order the closed form is the exact relative entropy of the whole model. For a lower order n-gram it ignores the change in the longer histories that back off to it.
- **Monotone in $\theta$.** A larger threshold removes a superset of the n-grams.
- **Model based.** It needs only the model, not the training counts.

## Variants and improvements

- **Weighted difference pruning** (Seymore and Rosenfeld 1996) scores $h w$ by $N(h w)[\ln p(w \mid h) - \ln p'(w \mid h)]$ with the training count $N(h w)$. It looks like the first term of line L5 with a count in place of $p(h) p^*(w \mid h)$, and it has no term for the backed off words.
- **Count cutoffs** remove all n-grams seen fewer than $k$ times. They are simpler and use no model at all.
- **Pruning a smoothed model.** The criterion works for any backoff model. With [Kneser-Ney](/kneser-ney-smoothing/) models the lower orders hold continuation probabilities, not estimates of the marginals, so $p(h)$ from the chain rule and the backed off estimates are poor, and the costs are less accurate.
- **Iterative pruning** recomputes the costs after each round. It sees the joint effect within a history at a higher cost.

## When to use it

Use it to fit a backoff n-gram model into a fixed memory budget, for example on a device, in a first pass of a speech recognizer, or in a decoder where the model is held in memory. It needs a normalized backoff model. For unnormalized scores as in [stupid backoff](/stupid-backoff/) there is no relative entropy to compute.

## Pitfalls

- **Forgetting to recompute $\alpha$.** After the removal the backoff weights must be recomputed, or the rows no longer sum to 1.
- **Sequential costs.** Computing each cost on the partly pruned model makes the result depend on the order of the loop. Stolcke computes all costs on the original model.
- **Holes in the history set.** In the ARPA file format a history that is still used by a longer n-gram must keep its entry. Some implementations keep the n-grams that are prefixes of kept n-grams.
- **The wrong $p(h)$.** Using the relative frequency of $h$ instead of the model probability changes the criterion; the method uses the chain rule of the model.
- **A row with no backed off words.** If every word was seen after $h$, $\alpha(h)$ has no meaning, and its denominator is 0. The implementation rejects such a model.

## Implementations

## History

Seymore and Rosenfeld (1996) pruned backoff models by a weighted difference of the log probabilities before and after the removal of an n-gram. Stolcke (1998) replaced it with the relative entropy between the two models, showed that it has a closed form that needs only sums over the explicit words of one history, and defined the threshold as the relative increase of the perplexity. On Broadcast News, with the threshold $10^{-8}$, a trigram model was cut to 26 percent of its size, its perplexity rose from 163.0 to 172.3, and the word error rate stayed at 32.6 percent. He found that the pruned sets of the two methods overlap by about 85 percent. The method is in the SRILM toolkit.

## References
