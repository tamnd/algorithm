---
tag: FKE3K3
kind: algorithm
slug: bayesian-hmm-tagging
name: Bayesian HMM tagging
aliases:
- unsupervised Bayesian POS tagging
area: natural-language-and-speech/tagging-and-information-extraction
level: advanced
summary: "Unsupervised part-of-speech induction with an HMM under sparse Dirichlet priors. The parameters are integrated out, and collapsed Gibbs sampling draws the tags."
solves: [part-of-speech-tagging]
model: word-ram
complexity:
  vars: {n: the number of tokens in the corpus, k: the number of tags, s: the number of sweeps, V: the number of word types}
  time: {worst: "Θ(s n k)"}
  space: {extra: "Θ(n + k^2 + k V)"}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2007
  people: [Sharon Goldwater, Thomas L. Griffiths]
  note: Goldwater and Griffiths gave the Bayesian HMM tagger with symmetric Dirichlet priors and collapsed Gibbs sampling at ACL 2007.
prereqs: [hmm-part-of-speech-tagger, gibbs-sampling, conjugate-prior]
see_also: [hidden-markov-model, markov-chain, baum-welch-algorithm, expectation-maximization, latent-dirichlet-allocation, dirichlet-process, brown-clustering, part-of-speech-tagging]
sources:
  - paper: "Sharon Goldwater and Thomas L. Griffiths, A fully Bayesian approach to unsupervised part-of-speech tagging, Proceedings of the 45th Annual Meeting of the Association for Computational Linguistics (ACL 2007), pages 744 to 751"
    title: Goldwater and Griffiths 2007
    locator: "Section 2.2 (the trigram model with symmetric Dirichlet priors), Section 2.3 and Figure 2 (Gibbs sampling and the conditional of one tag, annealing), Table 1 (accuracy against the hyperparameters), Section 4 (hyperparameter inference)"
  - paper: doi:10.1109/TPAMI.1984.4767596
    title: "Stuart Geman and Donald Geman, Stochastic relaxation, Gibbs distributions, and the Bayesian restoration of images, IEEE Transactions on Pattern Analysis and Machine Intelligence 6(6), 1984, pages 721 to 741"
    locator: the Gibbs sampler and annealing
  - paper: doi:10.1073/pnas.0307752101
    title: "Thomas L. Griffiths and Mark Steyvers, Finding scientific topics, Proceedings of the National Academy of Sciences 101(suppl. 1), 2004, pages 5228 to 5235"
    locator: "collapsed Gibbs sampling with Dirichlet-multinomial count ratios, for topic models"
---

Bayesian HMM tagging learns part-of-speech classes from untagged text. It uses the same [hidden Markov model](/hidden-markov-model/) as the [HMM tagger](/hmm-part-of-speech-tagger/), but it does not estimate one set of transition and emission probabilities. It puts sparse Dirichlet priors on them, integrates them out, and samples the tags themselves with collapsed [Gibbs sampling](/gibbs-sampling/). The Gibbs sampling page gives the general sampler for any joint distribution; this page derives the conditional of one tag in the collapsed HMM, where three counts change at once, and shows how the sparse prior changes the result. The method is due to Goldwater and Griffiths (2007).

## In plain words

We have plenty of text but no tags. We want to group words into classes that behave like nouns, verbs and so on. The model says that each tag tends to be followed by only a few other tags and tends to produce only a few words. Instead of fixing these tendencies as numbers, the method keeps every possible setting of them and averages over all of them. Then it walks through the text again and again. At each word it takes the tag away, asks how well each tag would fit given all the other tags in the corpus, and draws a new tag at random in proportion to that fit. After many passes, the tags settle into groups that reuse a small number of patterns.

## The problem

Input: a corpus of sentences $\mathbf w$ over $V$ word types, the number of tags $k$, and hyperparameters $\alpha, \beta > 0$. The model, in its first-order form (Goldwater and Griffiths use second order):

$$\tau_a \sim \mathrm{Dirichlet}(\alpha), \quad \omega_t \sim \mathrm{Dirichlet}(\beta), \quad t_i \mid t_{i-1} \sim \tau_{t_{i-1}}, \quad w_i \mid t_i \sim \omega_{t_i}.$$

Tag $0$ is the sentence boundary, used as $t_0$ and as the tag after the last word, so each row $\tau_a$ has $K = k + 1$ outcomes. Each $\omega_t$ has $V$ outcomes. Output: samples from the posterior $P(\mathbf t \mid \mathbf w, \alpha, \beta)$, which is proportional to the marginal likelihood

$$P(\mathbf t, \mathbf w) = \prod_{a=0}^{k} \frac{\prod_b \alpha^{(n_{a,b})}}{(K\alpha)^{(n_a)}} \prod_{t=1}^{k} \frac{\prod_w \beta^{(n_{t,w})}}{(V\beta)^{(n_t)}},$$

where $n_{a,b}$, $n_a$, $n_{t,w}$ and $n_t$ are transition and emission counts of the tagging and $x^{(m)} = x(x+1)\cdots(x+m-1)$ is the rising factorial. The induced tags have no names. They are compared with gold tags by a mapping such as many-to-one accuracy, or with a tag dictionary that limits the tags of each word.

## The algorithm

Remove one token from the counts. The conditional of its tag is a product of three ratios: the emission of its word, the transition from the left tag $a$ into it, and the transition from it to the right tag $b$. The last ratio needs two corrections, because when $a = t$ the transition $(a, t)$ has already been added to the row of $t$.

```pseudo id=main
BHMM-GIBBS(w, k, α, β, S)                      ▷ tag 0 is the boundary at both ends of a sentence
L1  give each token a random tag in 1..k; set the counts n_{a,b}, n_a, n_{t,w}, n_t
L2  for s ← 1 to S do
L3      for each token i, with word w_i, left tag a and right tag b (0 at a sentence end) do
L4          remove (a, t_i), (t_i, b) and (t_i, w_i) from the counts
L5          for t ← 1 to k do p_t ← (n_{t,w_i}+β)/(n_t+Vβ) · (n_{a,t}+α)/(n_a+Kα) · (n_{t,b}+[a=t=b]+α)/(n_t+[a=t]+Kα)
L6          draw t_i = t with probability p_t / (p_1 + ... + p_k)
L7          add (a, t_i), (t_i, b) and (t_i, w_i) to the counts
L8      record the tagging t as sample s
L9  return the samples
```

In L5, the count $n_t$ in the emission ratio is the number of tokens with tag $t$, and in the last ratio it is the number of transitions out of $t$. In this model the two numbers are equal, since each token has one outgoing transition, but the code keeps them apart. The ratio for one outcome follows from the Dirichlet-multinomial predictive rule: after counts $m_1, \ldots, m_D$ with sum $m$, the next outcome is $d$ with probability $(m_d + \gamma)/(m + D\gamma)$ (Goldwater and Griffiths 2007, equation 5).

The second-order model of Goldwater and Griffiths has the same form with tag trigrams. Resampling one tag changes three trigrams, so their conditional (Figure 2) has four ratios and more indicator terms.

## Example

Take four word types, the (0), dog (1), barks (2) and cat (3), with $k = 2$, $\alpha = 1/2$ and $\beta = 1/10$, so $K = 3$ and $V\beta = 2/5$. The current tagging is "the/1 dog/2 barks/1" and "the/1 cat/2". Resample the tag of "barks", with $a = 2$ and $b = 0$. After L4 the counts are: transitions $n_{0,1} = 2$, $n_{1,2} = 2$, $n_{2,0} = 1$, so $n_0 = 2$, $n_1 = 2$, $n_2 = 1$; emissions $n_{1,\text{the}} = 2$, $n_{2,\text{dog}} = n_{2,\text{cat}} = 1$, so $n_1 = n_2 = 2$ tokens.

| t | emission | transition a to t | transition t to b | product |
|---|---|---|---|---|
| 1 | (0 + 1/10)/(2 + 2/5) = 1/24 | (0 + 1/2)/(1 + 3/2) = 1/5 | (0 + 0 + 1/2)/(2 + 0 + 3/2) = 1/7 | 1/840 |
| 2 | (0 + 1/10)/(2 + 2/5) = 1/24 | (0 + 1/2)/(1 + 3/2) = 1/5 | (1 + 0 + 1/2)/(1 + 1 + 3/2) = 3/7 | 1/280 |

So $P(t = 1) = 1/4$ and $P(t = 2) = 3/4$. The same numbers come from the ratio $P(\mathbf t^{(1)}, \mathbf w) / (P(\mathbf t^{(1)}, \mathbf w) + P(\mathbf t^{(2)}, \mathbf w))$ of exact marginal likelihoods. Without the correction $[a = t]$ in the last denominator, the last ratio for $t = 2$ would be $3/5$, and the sampler would draw tag 1 with probability $5/26$, not $1/4$.

The test file checks the conditional against the ratio of exact marginals on random corpora in rational arithmetic. It also runs 20000 sweeps on a corpus of 4 tokens, whose 16 taggings have an exact posterior by enumeration, and the frequencies agree within 0.01. On 30 synthetic sentences where two classes alternate and use disjoint words, 150 sweeps with $\alpha = \beta = 0.1$ find the two classes exactly, up to the names of the tags.

## Correctness

[proofs/correctness.md](proofs/correctness.md) proves three things. The marginal likelihood is the product of Dirichlet-multinomial factors, one per row, by the normalizing constant of the Dirichlet distribution. The conditional of L5 is the ratio of two such marginals: add the emission, then the transition from $a$, then the transition to $b$, each by the predictive rule, and track how the second step changes the row of $t$ when $a = t$. A Gibbs update that draws one variable from its exact conditional leaves the posterior invariant, and since every tag has positive probability at every step, the chain is irreducible and aperiodic, so its law converges to the posterior. The theorem gives no rate.

## Complexity

One update costs $O(k)$ for the $k$ products of L5 and the draw of L6, and a sweep makes $n$ updates, so $S$ sweeps cost $\Theta(S n k)$ time. This is the same per tag as the second-order sampler, whose conditional also has a constant number of ratios. The counts take $\Theta(k^2 + k V)$ space, and the tags take $\Theta(n)$. A forward-filtering backward-sampling sampler that redraws a whole sentence at once costs $\Theta(n k^2)$ per sweep instead, and it needs the parameters, so it does not fit the collapsed model directly.

## Properties

- Randomized: the output depends on the seed. Goldwater and Griffiths report averages over 5 runs.
- No point estimate of the parameters: the tagging is drawn with the parameters integrated out. This lets the model use priors with $\alpha, \beta < 1$ that favor sparse rows, where a maximum a posteriori estimate can be degenerate (Goldwater and Griffiths 2007, Section 2.1).
- Label switching: the posterior is symmetric under any renaming of the tags, so tags are only defined up to a permutation. Average quantities that do not depend on the names, or use one sample.
- Measured results (24000 words of the WSJ with a full tag dictionary, 20000 iterations with annealing): 86.8% accuracy with $\alpha = 0.003$ and $\beta = 1$, against 74.5% for an HMM trained by EM and decoded by Viterbi, and 90.1% for the contrastive estimation CRF of Smith and Eisner (2005) (Goldwater and Griffiths 2007, Section 3 and Table 1).

## Variants and improvements

- Annealing: Goldwater and Griffiths raise the conditional to the power $1/T$ and lower the temperature $T$ from 2 to 0.08 over the run, so the last sample is near a mode (Sections 2.3 and 3).
- Hyperparameter inference: they put an improper uniform prior on $\alpha$ and $\beta$ and resample them by Metropolis-Hastings after each sweep (Section 4). BHMM2 uses a separate $\beta$ for each tag.
- Tag dictionaries: limiting the tags of each word to those listed in a dictionary turns induction into disambiguation, and the emission rows have $W_t$ outcomes instead of $V$.
- Second order and other priors: the trigram model of the paper; hierarchical Dirichlet process HMMs let the number of tags grow with the data (see the [Dirichlet process](/dirichlet-process/)).
- Point estimates: the [Baum-Welch algorithm](/baum-welch-algorithm/) (EM) fits one maximum likelihood HMM; variational Bayes fits an approximate posterior over the parameters.

## When to use it

Use it when there is no tagged corpus and you want word classes that follow the sparse structure of real tags, for example as a first step for a new language. Use the sparse prior when the corpus is small: the gain over EM is largest there. With tagged data, a supervised tagger such as the [HMM tagger](/hmm-part-of-speech-tagger/) or a discriminative model is far more accurate.

## Pitfalls

- Forgetting the indicator terms of L5. They matter whenever a tag repeats next to itself, and without them the sampler does not target the posterior. The example above shows a change from 1/4 to 5/26.
- Updating counts in the wrong order: remove all three events of the token before computing L5, and add them back after the draw.
- Using the denominator $n_t + K\alpha$ of the emission row by mistake. The emission row has $V$ outcomes, the transition row has $K = k + 1$.
- Reading one sample as a clustering without dealing with label switching, or averaging tag identities across runs.
- Judging convergence by the log marginal alone: it can stay flat while the chain is stuck in one mode. Use several seeds.

## Implementations

## History

Goldwater and Griffiths (2007) start from the tradition of Merialdo (1994), who trained a trigram HMM tagger by maximum likelihood on untagged text with a tag dictionary. They kept the trigram HMM but replaced the point estimate by integration under symmetric Dirichlet priors, and sampled the tags by collapsed Gibbs sampling, the technique that Griffiths and Steyvers (2004) had used for topic models. In their experiments the Bayesian model was up to 14 percentage points more accurate than the maximum likelihood HMM.

## References
