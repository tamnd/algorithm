---
tag: J19481
kind: technique
slug: gumbel-max-trick
name: Gumbel-max trick
aliases:
- Gumbel-max sampling
- Gumbel-top-k trick
- exponential race
area: randomized/sampling
level: advanced
summary: Add independent Gumbel noise to log-weights and take the argmax to sample a categorical distribution.
prereqs: [log-sum-exp-trick, independent-random-variables, discrete-probability-distribution]
see_also: [weighted-sampling, weighted-reservoir-sampling, alias-method, softmax-regression, log-sum-exp-trick, priority-sampling, top-k-selection, variational-autoencoder]
sources:
  - paper: doi:10.1016/j.ipl.2005.11.003
    title: Pavlos S. Efraimidis and Paul G. Spirakis, Weighted random sampling with a reservoir, Information Processing Letters 97(5), 2006
    locator: pages 181 to 185 (the keys u^(1/w) and the proof that the top k keys give a weighted sample without replacement)
  - paper: "John I. Yellott Jr., The relationship between Luce's choice axiom, Thurstone's theory of comparative judgment, and the double exponential distribution, Journal of Mathematical Psychology 15(2), 1977"
    locator: pages 109 to 144
  - paper: "Chris J. Maddison, Daniel Tarlow and Tom Minka, A* sampling, Advances in Neural Information Processing Systems 27, 2014"
    locator: Section 2 (the Gumbel-max trick and its properties)
  - paper: "Wouter Kool, Herke van Hoof and Max Welling, Stochastic beams and where to find them: the Gumbel-top-k trick for sampling sequences without replacement, ICML 2019, PMLR 97"
    locator: Section 2 (the Gumbel-top-k trick)
  - paper: "Emil J. Gumbel, Statistical theory of extreme values and some practical applications, National Bureau of Standards Applied Mathematics Series 33, 1954"
    locator: the double exponential (Gumbel) distribution
---

The Gumbel-max trick samples an index $i$ with probability $w_i / W$, where $W = \sum_j w_j$, from the log-weights $\phi_i = \ln w_i$: add independent standard Gumbel noise $G_i = -\ln(-\ln U_i)$ to each $\phi_i$ and return $\arg\max_i (\phi_i + G_i)$. The weights need not be normalized, so it works directly on unnormalized log-probabilities, with no exponentials and no sums. The $k$ largest keys, in order, are a weighted sample of $k$ items without replacement, drawn one by one with probability proportional to weight among the items left: the Plackett-Luce law. This top-$k$ form is the same as the keys $U_i^{1/w_i}$ of Efraimidis and Spirakis, and both are an exponential race in disguise. The trick links [weighted sampling](/weighted-sampling/) to [top-k selection](/top-k-selection/): any method that finds the largest perturbed scores samples.

## In plain words

Each item gets a score: the logarithm of its weight. Shake each score by a random amount from a special noise law, the Gumbel law, and pick the item with the highest shaken score.

The Gumbel law is chosen so that this pick happens with probability exactly in proportion to the weights. Heavy items start with a higher score and so win more often, but light items still win sometimes when their noise is large.

Keep the order of all the shaken scores, and you get more. The top two items are a sample of two different items, as if you had drawn one by weight, set it aside and drawn again from the rest. The same holds for the top three, and so on.

## When it applies

- The weights come as log-weights or unnormalized scores, as the logits of a [softmax](/softmax-regression/), and normalizing is costly or numerically unsafe.
- Many independent samples are needed in parallel, as on a GPU: each item gets its own noise, and the argmax is a reduction.
- A sample without replacement is needed in one pass: compute one key per item and keep the $k$ largest with a heap. This works on a stream, as in [weighted reservoir sampling](/weighted-reservoir-sampling/).
- The argmax over a huge or structured set can be found by search, as in A* sampling over a continuous space or beam search over sequences.

For a single draw from a fixed small distribution, a cumulative sum and [binary search](/binary-search/), or the [alias method](/alias-method/) for many draws, is cheaper: the trick uses $n$ uniforms and $n$ double logarithms per draw.

## The template

Notation: $\phi_1, \ldots, \phi_n$ are log-weights, $w_i = e^{\phi_i}$, $W = \sum_i w_i$. A standard Gumbel variable has distribution function $\exp(-e^{-g})$. The hole is the argmax, or the top-$k$ selection.

```pseudo id=main
GUMBEL-MAX(φ[1..n])
L1  for i ← 1 to n do  U_i ← a uniform real in (0, 1);  K_i ← φ_i − ln(−ln U_i)
L2  return argmax_i K_i

GUMBEL-TOP-K(φ[1..n], k)
L3  compute K_i as in line L1; return the k indices with the largest K_i, largest first
```

Since $E_i = -\ln U_i$ is a standard exponential variable, $K_i = -\ln(E_i / w_i)$. So the largest key is the smallest $E_i / w_i$, the first finisher in an exponential race with rates $w_i$. The Efraimidis-Spirakis key $U_i^{1/w_i} = e^{-E_i/w_i}$ orders the items the same way.

### Example

Weights $(1, 2, 3, 4)$, so $W = 10$ and the target law is $(0.1, 0.2, 0.3, 0.4)$. With the uniforms $(0.3, 0.8, 0.5, 0.6)$:

| $i$ | $w_i$ | $\phi_i$ | $U_i$ | $G_i = -\ln(-\ln U_i)$ | $K_i$ | $E_i / w_i$ |
|---|---|---|---|---|---|---|
| 1 | 1 | 0.0000 | 0.3 | $-0.1856$ | $-0.1856$ | 1.2040 |
| 2 | 2 | 0.6931 | 0.8 | 1.4999 | 2.1931 | 0.1116 |
| 3 | 3 | 1.0986 | 0.5 | 0.3665 | 1.4651 | 0.2310 |
| 4 | 4 | 1.3863 | 0.6 | 0.6717 | 2.0580 | 0.1277 |

The argmax is item 2. The full order of the keys is $2, 4, 3, 1$, the same as the order of the race times $E_i/w_i$. The top two, $(2, 4)$, form one draw of two items without replacement; under the Plackett-Luce law this ordered pair has probability $\frac{2}{10} \cdot \frac{4}{8} = 0.1$.

### Why it is correct

**Lemma 1 (exponential race).** Let $E_1, \ldots, E_n$ be independent, with $E_i$ exponential of rate $w_i > 0$, and $W = \sum w_i$. Then $\Pr[\arg\min_j E_j = i] = w_i / W$. Moreover, given that the minimum is $E_i = t$, the other values $E_j - t$, $j \ne i$, are independent and exponential with rates $w_j$, and the minimum is exponential with rate $W$ and independent of the argmin.

*Proof.* For $t \ge 0$ and $s_j \ge 0$,

$$\Pr\bigl[E_i \in dt,\ E_j > t + s_j \text{ for all } j \ne i\bigr] = w_i e^{-w_i t}\,dt \prod_{j \ne i} e^{-w_j(t + s_j)} = \frac{w_i}{W} \cdot W e^{-Wt}\,dt \cdot \prod_{j \ne i} e^{-w_j s_j}.$$

The right side is a product of three factors: $w_i / W$ for the index, the exponential density of rate $W$ for the minimum, and the survival functions of independent exponentials of rates $w_j$ for the residuals. With all $s_j = 0$ and summing over $i$, the claims follow. $\square$

**Theorem 1 (Gumbel-max).** If $G_1, \ldots, G_n$ are independent standard Gumbel variables, then $\Pr[\arg\max_i(\phi_i + G_i) = i] = w_i / W$.

*Proof.* $E_i = e^{-G_i}$ is a standard exponential variable, since $\Pr[e^{-G_i} > s] = \Pr[G_i < -\ln s] = e^{-s}$. Then $e^{-(\phi_i + G_i)} = E_i / w_i$ is exponential with rate $w_i$, and $x \mapsto e^{-x}$ is decreasing, so the argmax of the keys is the argmin of the race. Apply Lemma 1. $\blacksquare$

A direct computation gives the same result. The key $M_i = \phi_i + G_i$ has distribution function $\exp(-w_i e^{-m})$, so

$$\Pr[\arg\max = i] = \int_{-\infty}^{\infty} w_i e^{-m} e^{-w_i e^{-m}} \prod_{j \ne i} e^{-w_j e^{-m}}\,dm = \int_{-\infty}^{\infty} w_i e^{-m} e^{-W e^{-m}}\,dm = \int_0^\infty w_i e^{-Ws}\,ds = \frac{w_i}{W},$$

with $s = e^{-m}$. Also, $\max_i M_i$ is Gumbel with location $\ln W$, independent of the argmax.

**Theorem 2 (Gumbel-top-k).** The ordered list of the $k$ largest keys $(i_1, \ldots, i_k)$ has

$$\Pr[(i_1, \ldots, i_k) = (j_1, \ldots, j_k)] = \prod_{r=1}^{k} \frac{w_{j_r}}{W - w_{j_1} - \dots - w_{j_{r-1}}},$$

the law of successive sampling without replacement, also called the Plackett-Luce law.

*Proof.* The order of the keys, from largest down, is the order of the race times $E_i / w_i$, from smallest up. By Lemma 1 the first finisher is $j_1$ with probability $w_{j_1}/W$. Given this and its time $t$, the remaining times minus $t$ are independent exponentials with rates $w_j$, $j \ne j_1$: a new race on the items left. Apply Lemma 1 to it, and continue by induction on $r$. $\blacksquare$

The same proof shows that the Efraimidis-Spirakis keys $U_i^{1/w_i} = e^{-E_i/w_i}$ give the same law, since they order the items exactly as the Gumbel keys do. The results hold for exact reals. In floating point, $U_i$ lies on a grid of step $2^{-53}$, so $G_i$ lies in about $[-3.6, 36.7]$, and the probabilities are off by tiny amounts.

### Cost

- **One draw.** $n$ uniforms, $2n$ logarithms and an argmax: $\Theta(n)$ time. The cumulative-sum method also takes $\Theta(n)$ but needs only one uniform.
- **Top $k$.** $\Theta(n)$ keys and a selection: $O(n \log k)$ with a heap of size $k$, or $O(n)$ expected with quickselect.
- **Parallel.** The keys are independent, so the work splits across processors with one max-reduction or top-$k$ merge.

## Classic examples

- **Sampling from a softmax.** For logits $\phi$, $\arg\max(\phi + G)$ is a sample from $\operatorname{softmax}(\phi)$, with no exponentials of large numbers. It is the numerically safe partner of the [log-sum-exp trick](/log-sum-exp-trick/).
- **[Weighted reservoir sampling](/weighted-reservoir-sampling/).** Algorithm A-Res of Efraimidis and Spirakis keeps the $k$ items with the largest keys $U^{1/w}$ in a heap while reading a stream.
- **Sampling sequences without replacement.** Kool, van Hoof and Welling (2019) apply the top-$k$ trick to sequence models: perturbing the log-probabilities of partial sequences and keeping the top $k$ in a beam gives $k$ distinct sequences drawn without replacement.
- **A* sampling.** Maddison, Tarlow and Minka (2014) extend the trick to continuous spaces with a Gumbel process and find the argmax by A* search.
- **Discrete choice models.** In random utility models, if each option's utility is a fixed value plus independent Gumbel noise, the chosen option follows the multinomial logit law. Yellott (1977) related this to Luce's choice axiom.

## Variations

- **Gumbel-softmax (the Concrete distribution).** Replace the argmax by $\operatorname{softmax}((\phi + G)/\tau)$ with a temperature $\tau > 0$. This gives a differentiable relaxation, used to train [variational autoencoders](/variational-autoencoder/) with discrete latent variables. It is an approximation: only the limit $\tau \to 0$ gives exact samples.
- **The exponential race form.** Return $\arg\min_i E_i / w_i$ with $E_i = -\ln U_i$. It uses one logarithm per item and works with weights, not log-weights.
- **[Priority sampling](/priority-sampling/).** Uses the keys $w_i / U_i$; its top-$k$ is not a Plackett-Luce sample, but it gives unbiased estimators of subset sums.
- **Lazy Gumbel sampling.** When most $\phi_i$ are very small, the large noise values can be found first and the argmax decided without touching every item.

## Pitfalls

- **The wrong noise.** The trick needs Gumbel noise. Exponential, normal or uniform noise added to $\phi$ gives a different law (the normal gives the probit model). A test with weights $(1, 2, 3, 4)$ shows this at once.
- **Weights instead of log-weights.** The noise is added to $\ln w_i$, not to $w_i$.
- **$U = 0$ or $U = 1$.** $-\ln(-\ln U)$ needs $0 < U < 1$. Many generators can return 0.
- **Ties.** Ties have probability 0 for exact reals but can happen in floating point with equal $\phi_i$ and coarse uniforms. Break them at random, or ignore the bias if it is far below the sampling error.
- **The top-k law is not the same as inclusion probabilities proportional to weight.** The probability that item $i$ is among the $k$ chosen is not $k w_i / W$ in general. Use [probability-proportional-to-size sampling](/probability-proportional-to-size-sampling/) when the inclusion probabilities must be exact.
- **Reusing noise.** One set of noise values gives one sample. Reusing $G$ across draws gives the same index every time.

## Exercises

1. Show that $\max_i(\phi_i + G_i) - \ln W$ is a standard Gumbel variable independent of the argmax.
2. Prove that the probability that item $i$ is in the top 2 is $\frac{w_i}{W} + \sum_{j \ne i} \frac{w_j}{W} \cdot \frac{w_i}{W - w_j}$, and show that it differs from $2w_i/W$ for weights $(1, 1, 2)$.
3. Show that adding the same constant to every $\phi_i$, or the same independent Gumbel noise to every key, does not change the law of the argmax.
4. Write the top-$k$ trick for a stream of items with a heap of size $k$, and give its cost.

## References
