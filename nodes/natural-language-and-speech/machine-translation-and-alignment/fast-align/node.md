---
tag: NW40F8
kind: algorithm
slug: fast-align
name: Fast align
aliases:
- diagonal reparameterization of IBM model 2
area: natural-language-and-speech/machine-translation-and-alignment
level: advanced
summary: A log-linear reparameterization of IBM model 2 that favors alignments near the diagonal, trained fast by EM with closed-form normalizers.
solves: [word-alignment]
model: real-ram
complexity:
  vars: {n: the number of sentence pairs, m: the largest source length, l: the largest target length}
  time: {worst: "Θ(n m l)"}
  space: {extra: "Θ(l)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2013
  people: [Chris Dyer, Victor Chahuneau, Noah A. Smith]
  note: Dyer, Chahuneau and Smith replaced the distortion table of IBM Model 2 by one tension parameter and released the fast_align tool. They measured it as about ten times faster than IBM Model 4 training, with similar translation quality.
prereqs: [ibm-model-2, expectation-maximization, geometric-series]
see_also: [ibm-model-1, hmm-alignment-model, grow-diag-final-symmetrization, alignment-error-rate, log-linear-translation-model, bisection-method, variational-inference, word-alignment]
sources:
  - paper: "Chris Dyer, Victor Chahuneau and Noah A. Smith, A simple, fast, and effective reparameterization of IBM Model 2, NAACL-HLT 2013, pages 644 to 648, ACL Anthology N13-1073"
    title: Dyer, Chahuneau and Smith 2013
    locator: "Section 2 (the model, the closed-form partition function and the gradient of lambda), Section 3 (the experiments, Tables 1 to 3)"
  - paper: "Peter F. Brown, Stephen A. Della Pietra, Vincent J. Della Pietra and Robert L. Mercer, The mathematics of statistical machine translation: parameter estimation, Computational Linguistics 19(2), 1993, pages 263 to 311"
    title: Brown et al. 1993
    locator: "Section 4.2 (Model 2)"
  - book: isbn:9780521874151
    title: Philipp Koehn, Statistical Machine Translation, Cambridge University Press, 2010
    locator: "Section 4.4 (higher IBM models)"
---

Fast align is a [word alignment](/word-alignment/) model and its training method. It is [IBM Model 2](/ibm-model-2/) with the table of alignment probabilities replaced by a log-linear distortion with one parameter $\lambda$, the *tension*, that pulls each source word toward the matching place on the diagonal of the sentence pair. The normalizer of the distortion is a sum of two [geometric series](/geometric-series/), so it costs $O(1)$ per position. The model is trained by [EM](/expectation-maximization/), whose E step is exact and costs $O(l m)$ per pair. Dyer, Chahuneau and Smith (2013) measured it as about ten times faster to train than IBM Model 4, with similar BLEU in their translation systems.

## In plain words

When you align the words of a sentence with the words of its translation, a word near the start usually goes with a word near the start, and a word near the end with one near the end. Fast align makes this a rule with one dial.

Each word of the source picks a partner in the target, or picks "no partner". The model likes partners that are close to the same relative place in the other sentence. The dial says how strongly. With the dial at zero, position does not matter. With a high dial, words stick to the diagonal.

Training repeats two steps. First, for each word, compute how likely each partner is now. Then count those guesses to update the word translation table and set the dial to the value that best fits the guesses. A simple formula for the sums makes each step fast.

## The problem

The direction is $p(f \mid e)$, as for the IBM models. A pair has the source $f = f_1 \ldots f_m$ and the target $e = e_1 \ldots e_l$, plus the null word $e_0$. Each source position $j$ has one link $a_j \in \{0, \ldots, l\}$. The model is

$$p(f, a \mid e) = \prod_{j=1}^{m} \delta(a_j \mid j, m, l)\; \theta(f_j \mid e_{a_j}),$$

$$\delta(i \mid j, m, l) = \begin{cases} p_0 & i = 0, \\ (1 - p_0)\, \dfrac{e^{\lambda h(i, j, m, l)}}{Z_\lambda(j, m, l)} & 1 \le i \le l, \end{cases} \qquad h(i, j, m, l) = -\left| \frac{i}{l} - \frac{j}{m} \right|,$$

with $Z_\lambda(j, m, l) = \sum_{i=1}^{l} e^{\lambda h(i, j, m, l)}$ and $\lambda \ge 0$. The paper writes the model in the other direction, with $i$ for the target position and $n$ for the source length; this page uses the area notation. With $\lambda = 0$ the distortion is uniform over the real words, which is [IBM Model 1](/ibm-model-1/) with a null word of fixed probability $p_0$.

The task is to fit $\theta$ and $\lambda$ to a [parallel corpus](/parallel-corpus/) by maximum likelihood, and then to output for each pair the best alignment.

## The algorithm

```pseudo id=main
FAST-ALIGN-EM(corpus, p_0, λ, K)                ▷ EM; the direction is p(f | e)
L1  θ(f | e) ← 1 / |V_F| for every source word f and every target word e, NULL included
L2  repeat K times
L3      for each pair (f_1 .. f_m, e_1 .. e_l) and each j ← 1 to m do
L4          Z ← PARTITION(j, m, l, λ)
L5          w_0 ← p_0 θ(f_j | NULL); w_i ← (1 - p_0) e^{λ h(i, j, m, l)} / Z · θ(f_j | e_i) for i = 1 .. l
L6          for i ← 0 to l do q ← w_i / Σ w; c(f_j, e_i) += q; if i ≥ 1 then S += q h(i, j, m, l); N(j, m, l) += q
L7      θ(f | e) ← c(f, e) / Σ_{f'} c(f', e)
L8      λ ← the maximizer in [0, Λ] of λ S - Σ N(j, m, l) ln Z_λ(j, m, l), by bisection on its derivative
L9  return θ, λ

PARTITION(j, m, l, λ)                           ▷ O(1)
L10 u ← floor(j l / m); r ← e^{-λ / l}
L11 return s_u(e^{λ h(u, j, m, l)}, r) + s_{l - u}(e^{λ h(u + 1, j, m, l)}, r)      ▷ s_n(g, r) = g (1 - r^n) / (1 - r)
```

Line L1 starts from a uniform translation table. Lines L3 to L6 are the E step. By the distributive law, the posterior over the $(l + 1)^m$ alignments is a product of one distribution per source position, so the expected count of a link is just its share $q$ of the sum at line L6. The variable $S$ collects the expected value of $h$ over the links to real words, and $N(j, m, l)$ collects the posterior mass on real words at the positions with the same $(j, m, l)$. Line L7 is the M step for $\theta$, a normalization of the counts. Line L8 is the M step for $\lambda$. Its objective is concave, because $\ln Z_\lambda$ is convex in $\lambda$, and its derivative is $S - \sum N(j, m, l)\, E_\lambda[h \mid j, m, l]$.

**The partition function.** The real position $j l / m$ splits the targets into $u = \lfloor j l / m \rfloor$ positions at or before it and $l - u$ after it. On each side, one step away from the diagonal multiplies $e^{\lambda h}$ by $r = e^{-\lambda / l}$. So each side is a geometric series, and line L11 adds the two closed forms. In the same way, $E_\lambda[h]$ is a sum of two arithmetic-geometric series, also $O(1)$. The paper writes the second count as $n - j_\downarrow$ with $j_\downarrow = j_\uparrow + 1$, which is one term short; the right count is the number of positions after $u$, which is $l - u$. The tests check the closed form against the direct sum for all small $(j, m, l)$.

**This implementation and the paper.** The paper fixes $p_0 = 0.08$ and starts with $\lambda = 4$. It puts a Dirichlet prior on $\theta$ and estimates it by mean-field [variational Bayes](/variational-inference/), and it updates $\lambda$ by gradient steps. The code of this page uses plain EM for $\theta$ and an exact line search for $\lambda$, so the likelihood never decreases. The cap is $\Lambda = 100$.

**Decoding.** After training, the best alignment is found per source position: $a_j = \arg\max_i \delta(i \mid j, m, l)\, \theta(f_j \mid e_i)$, with the smallest $i$ on a tie. This is exact for the model, because the alignment probability is a product of one factor per $j$.

## Example

Take $j = 2$, $m = 5$, $l = 7$ and $\lambda = 4$. The diagonal point is $j l / m = 2.8$, so $u = 2$: two targets before it and five after. With $r = e^{-4/7} = 0.5647$,

| $i$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| $h(i)$ | -0.2571 | -0.1143 | -0.0286 | -0.1714 | -0.3143 | -0.4571 | -0.6 |
| $e^{\lambda h(i)}$ | 0.3575 | 0.6331 | 0.8920 | 0.5037 | 0.2845 | 0.1606 | 0.0907 |
| $\delta(i \mid 2, 5, 7)$ | 0.1126 | 0.1993 | 0.2808 | 0.1586 | 0.0896 | 0.0506 | 0.0286 |

The lower series is $0.6331 (1 + r) = 0.9906$ and the upper series is $0.8920 (1 - r^5)/(1 - r) = 1.9315$, so $Z = 2.9222$, the sum of the middle row. The closest target, $i = 3$, gets the largest weight, and the weights fall by the factor $r$ per step on each side.

Now train on five German to English pairs: (das haus ist klein | the house is small), (das haus ist alt | the house is old), (das buch ist klein | the book is small), (ein buch | a book) and (klein ist das haus | the house is small), with $p_0 = 0.08$ and $\lambda = 4$ at the start.

| iteration | $\lambda$ before | log likelihood before | $\theta(\text{haus} \mid \text{house})$ |
|---|---|---|---|
| 0 | 4.0 | -35.0264 | 0.1429 |
| 1 | 4.0 | -20.2495 | 0.3652 |
| 2 | 6.4646 | -14.8438 | 0.5182 |
| 3 | 10.6607 | -11.1635 | 0.6511 |
| 4 | 16.8848 | -9.5740 | 0.6962 |
| 5 | 24.5069 | -9.2468 | 0.6843 |

In the first iteration $\lambda$ stays at 4. With a uniform $\theta$ the posterior of each position equals its prior $\delta$, so the expected $h$ under the posterior equals $E_\lambda[h]$ and the derivative at line L8 is zero. After that, four of the five pairs are monotone, and $\lambda$ grows. The likelihood rises at each step. The Viterbi alignment of the last pair is $(1, 2, 3, 4)$: klein to the, ist to house, das to is, haus to small. The tension wins over the lexicon, and the pair that is not monotone is aligned wrongly. With $\lambda$ fixed at 0, the same training aligns klein to small and haus to house in that pair.

## Correctness

Three claims are exact. First, line L11 equals the sum $\sum_{i=1}^l e^{\lambda h(i)}$: the split at $u$ puts each $i$ in exactly one geometric series. Second, lines L5 and L6 give the exact posterior counts, because $p(a \mid f, e)$ is a product over $j$. Third, each iteration does not lower the likelihood: line L7 maximizes the expected log likelihood in $\theta$, line L8 does not lower it in $\lambda$, and the EM inequality turns a gain in the expected log likelihood into a gain in the likelihood. The full proof is in the proofs file.

EM can stop at a local maximum. The quality of the alignments is a measurement, not a theorem.

## Complexity

In the [real RAM](/real-ram/) model, with $e^x$ at unit cost: line L4 is $O(1)$ by line L11, and lines L5 and L6 cost $O(l)$ per source position. So the E step costs $\Theta(l m)$ per pair and $\Theta(n m l)$ per iteration in the worst case. Line L7 costs one pass over the counts. Line L8 does $B$ bisection steps (60 in the code), each of which evaluates $E_\lambda[h]$ once per distinct triple $(j, m, l)$, at most $n m$ triples and in practice far fewer. A direct sum for $Z$ and for $E_\lambda[h]$ would cost $O(l)$ each time instead of $O(1)$. Dyer et al. report that computing the partition values for $0 < i, m, n < 150$ took 0.62 s with the closed form against 6.49 s with the direct sum (a measurement). The working memory is $\Theta(l)$ for the weights of one position plus the tables of counts and of $\theta$.

## Properties

- **Few parameters.** The distortion has one parameter, $\lambda$, against the table $a(i \mid j, l, m)$ of Model 2, so it does not overfit rare lengths.
- **Model 1 inside.** At $\lambda = 0$ the distortion is uniform over the real words.
- **Exact decoding.** The best alignment is found per position in $O(l m)$ per pair.
- **Not concave.** The likelihood is not concave in $(\theta, \lambda)$, so the start matters. The paper uses no staged start from Model 1.
- **Measured quality.** On French to English and Chinese to English test sets, Dyer et al. report alignment error rates of 16.6 and 44.1 with the variational version, against 21.4 and 53.3 for Model 2 and 10.4 and 45.8 for Model 4. In their translation systems for Chinese, French and Arabic to English, BLEU was slightly higher than with Model 4 alignments (for example 27.7 against 27.4 for French). These are measurements on their data.

## Variants and improvements

- **Variational Bayes.** A Dirichlet prior with a small concentration (0.01 in the paper) on $\theta$ makes the translation distributions sparse, which lowers the alignment error in their experiments.
- **The reverse direction.** Run the model with $f$ and $e$ swapped, then combine the two alignments with [grow-diag-final](/grow-diag-final-symmetrization/) or the intersection.
- **Fixed tension.** Without the optimization of line L8, $\lambda$ stays at its start value, which is a common setting.
- **HMM alignment.** The [HMM alignment model](/hmm-alignment-model/) conditions each link on the previous one instead of on the diagonal, which handles blocks that move. It costs $O(l^2 m)$ per pair.

## When to use it

Use fast align to align a large corpus quickly before [phrase pair extraction](/phrase-pair-extraction/), or when you need many alignments for a quick experiment. It is best for language pairs with mostly monotone word order, such as French and English. For pairs with long distance reordering, the HMM model or Model 4 can align better, at a much higher cost. For a small corpus, the speed does not matter, and the choice should follow the [alignment error rate](/alignment-error-rate/) or, better, the final translation quality.

## Pitfalls

- **One term short in line L11.** With the count $l - u - 1$ in the upper series, the farthest target $i = l$ is lost and $\delta$ does not sum to 1. Use $l - u$.
- **Cancellation near $\lambda = 0$.** The form $(1 - r^n)/(1 - r)$ loses digits when $r$ is close to 1. Compute it with expm1, as the code does, or switch to the direct sum.
- **A tension that never stops.** On data that is close to monotone, the optimum of line L8 can grow without bound, and then each source word is forced to the diagonal, as in the example. Cap $\lambda$, or keep it fixed.
- **The wrong direction.** $\delta$ normalizes over the target positions $i$ for each source position $j$. If line L10 or L11 sums over $j$ instead, the weights of the choices of $a_j$ do not sum to $1 - p_0$, and the model is no longer a distribution over alignments.
- **Products of probabilities.** The likelihood of a long sentence is a product of hundreds of small numbers and underflows in double precision. Sum the logarithms of the per-position sums, as the code does.

## Implementations

## History

Brown, Della Pietra, Della Pietra and Mercer (1993) defined Model 2 with a table of alignment probabilities. Chris Dyer, Victor Chahuneau and Noah Smith (2013) replaced that table by the diagonal distortion with one parameter, showed the closed form of its normalizer and of its gradient, and trained $\theta$ with variational Bayes. Their tool, fast_align, became a common choice to align large corpora because it trains in a fraction of the time of the IBM Model 4 pipeline (17.2 CPU hours against 1.7 for one direction of 117 million French to English tokens, in their measurement).

## References
