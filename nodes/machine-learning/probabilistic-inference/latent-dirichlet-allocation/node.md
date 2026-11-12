---
tag: JHNS1Q
kind: model
slug: latent-dirichlet-allocation
name: Latent Dirichlet allocation
area: machine-learning/probabilistic-inference
level: advanced
summary: "A generative topic model: each document mixes topics and each topic is a distribution over words. The posterior is inferred by variational EM or collapsed Gibbs sampling."
history:
  year: 2003
  people: [David M. Blei, Andrew Y. Ng, Michael I. Jordan]
  note: Blei, Ng and Jordan published LDA in JMLR in 2003 with variational EM. Griffiths and Steyvers gave the collapsed Gibbs sampler in 2004.
prereqs: [conjugate-prior, gibbs-sampling, bayesian-network]
see_also: [latent-semantic-analysis, nonnegative-matrix-factorization, variational-inference, stochastic-variational-inference, mean-field-approximation, dirichlet-process, expectation-maximization, naive-bayes-classifier]
sources:
  - paper: "David M. Blei, Andrew Y. Ng and Michael I. Jordan, Latent Dirichlet allocation, Journal of Machine Learning Research 3:993-1022, 2003"
    title: Blei, Ng and Jordan 2003
    locator: "Section 3 (the model and exchangeability), Section 4 (unigram, mixture of unigrams and pLSI), Section 5 (variational inference, parameter estimation by variational EM, smoothing with a Dirichlet prior on the topics)"
  - paper: doi:10.1073/pnas.0307752101
    title: "Thomas L. Griffiths and Mark Steyvers, Finding scientific topics, Proceedings of the National Academy of Sciences 101 (suppl. 1):5228-5235, 2004"
    locator: the collapsed Gibbs sampler with its full conditional, the estimates of phi and theta from one sample, the choice alpha = 50/T and beta = 0.1, and the choice of the number of topics
  - paper: "Thomas Hofmann, Probabilistic latent semantic indexing, Proceedings of SIGIR 1999, pp. 50-57"
    title: Hofmann 1999
    locator: the pLSI aspect model fitted by EM, with one mixing vector per training document
  - paper: "Mark Girolami and Ata Kabán, On an equivalence between PLSI and LDA, Proceedings of SIGIR 2003"
    title: Girolami and Kabán 2003
    locator: pLSI as MAP estimation in LDA with a uniform Dirichlet prior
  - paper: "Jonathan K. Pritchard, Matthew Stephens and Peter Donnelly, Inference of population structure using multilocus genotype data, Genetics 155(2):945-959, 2000"
    title: Pritchard, Stephens and Donnelly 2000
    locator: the admixture model, the same mixed membership model for alleles and populations, fitted by Gibbs sampling
  - paper: "David Sontag and Daniel M. Roy, Complexity of inference in latent Dirichlet allocation, Advances in Neural Information Processing Systems 24, 2011, pp. 1008-1016"
    title: Sontag and Roy 2011
    locator: MAP topic assignment is NP-hard when a document uses many topics and polynomial when it uses few; the MAP topic distribution is also NP-hard
  - paper: "Sanjeev Arora, Rong Ge and Ankur Moitra, Learning topic models: going beyond SVD, Proceedings of FOCS 2012"
    title: Arora, Ge and Moitra 2012
    locator: a polynomial time algorithm that learns the topic matrix when every topic has an anchor word
  - paper: "Matthew D. Hoffman, David M. Blei and Francis Bach, Online learning for latent Dirichlet allocation, Advances in Neural Information Processing Systems 23, 2010"
    title: Hoffman, Blei and Bach 2010
    locator: online variational Bayes for LDA on streams of documents
---

Latent Dirichlet allocation is a generative model of a collection of documents. It assumes $K$ *topics*, each a probability distribution over a vocabulary of $V$ words. Each document has its own mixture of the topics, drawn from a Dirichlet distribution, and each word of the document is made by first choosing a topic from that mixture and then a word from that topic. Blei, Ng and Jordan published it in 2003. Given only the words, inference recovers the topics and the mixture of each document. The exact posterior is intractable, so in practice it is approximated by variational methods, as in the original paper, or by the *collapsed Gibbs sampler* of Griffiths and Steyvers (2004). That sampler updates one word at a time with the simple rule $P(z_i = k \mid \ldots) \propto (n_{dk} + \alpha)(n_{kw} + \beta)/(n_k + V\beta)$.

## The machine

**The generative process.** Fix the number of topics $K$, the vocabulary size $V$, and the symmetric Dirichlet parameters $\alpha > 0$ for the document mixtures and $\beta > 0$ for the topics.

1. For each topic $k = 1, \ldots, K$, draw the word distribution $\phi_k \sim \mathrm{Dir}(\beta, \ldots, \beta)$ on the $V$ words.
2. For each document $d = 1, \ldots, D$:
   1. draw the topic proportions $\theta_d \sim \mathrm{Dir}(\alpha, \ldots, \alpha)$ on the $K$ topics;
   2. for each position $i = 1, \ldots, N_d$, draw the topic $z_{di} \sim \mathrm{Categorical}(\theta_d)$ and then the word $w_{di} \sim \mathrm{Categorical}(\phi_{z_{di}})$.

As a [Bayesian network](/bayesian-network/) in plate notation, $\phi$ sits in a plate over topics, $\theta_d$ in a plate over documents, and $(z_{di}, w_{di})$ in a plate over the words of a document. Only $w$ is observed. In the 2003 paper the topics are fixed parameters fitted by maximum likelihood, and Section 5.4 adds the Dirichlet prior of step 1, which they call smoothing. Most later work, Griffiths and Steyvers among them, uses the smoothed form, as this page does.

The words of a document are exchangeable: their order does not matter, only their counts (the "bag of words"). Blei et al. motivate the model by de Finetti's theorem: exchangeable words are conditionally independent given some latent parameter, here $\theta_d$ (Section 3.1).

**The query.** Given the words $w$, the targets are the posterior $P(\theta, \phi, z \mid w, \alpha, \beta)$ and point estimates from it: the topics $\phi_k$, read as lists of their most probable words, and the mixture $\theta_d$ of each document.

**The collapsed joint.** The Dirichlet is a [conjugate prior](/conjugate-prior/) for the categorical distribution, so $\theta$ and $\phi$ integrate out in closed form. With the counts $n_{dk}$ (words of document $d$ with topic $k$), $n_{kw}$ (copies of word $w$ with topic $k$) and $n_k = \sum_w n_{kw}$,

$$P(w, z \mid \alpha, \beta) = \prod_{d=1}^{D} \frac{\Gamma(K\alpha)}{\Gamma(K\alpha + N_d)} \prod_{k=1}^{K} \frac{\Gamma(n_{dk} + \alpha)}{\Gamma(\alpha)} \;\cdot\; \prod_{k=1}^{K} \frac{\Gamma(V\beta)}{\Gamma(V\beta + n_k)} \prod_{w=1}^{V} \frac{\Gamma(n_{kw} + \beta)}{\Gamma(\beta)}.$$

Each factor is a Dirichlet-multinomial probability: $\int \prod_k \theta_k^{n_k} \, \mathrm{Dir}(\theta; \alpha) \, d\theta = \frac{\Gamma(K\alpha)}{\Gamma(K\alpha + N)} \prod_k \frac{\Gamma(n_k + \alpha)}{\Gamma(\alpha)}$.

## What it counts

Cost is counted in arithmetic operations on reals, as a function of the total number of word tokens $N = \sum_d N_d$, the number of topics $K$, and the number of passes. The model gives:

- **The topics** $\hat\phi_{kw} = (n_{kw} + \beta)/(n_k + V\beta)$ and **the document mixtures** $\hat\theta_{dk} = (n_{dk} + \alpha)/(N_d + K\alpha)$, the posterior means of $\phi$ and $\theta$ given one sample of $z$ (Griffiths and Steyvers).
- **The likelihood of held-out documents**, $P(w_{\text{new}} \mid \phi, \alpha)$, used to compare models and to choose $K$, often reported as perplexity. It needs an integral over $\theta$ and is itself hard to compute exactly.

The model has $K + KV$ parameters whatever the number of documents. The pLSI model of Hofmann (1999) instead has a mixing vector for each training document, so its parameters grow with $D$, and it has no natural way to assign a probability to a new document (Blei et al., Section 4.3).

## Relation to other models

- **pLSI.** pLSI is LDA without the Dirichlet prior on $\theta_d$: each training document has a free mixing vector fitted by [EM](/expectation-maximization/). LDA with a uniform prior and MAP estimation reduces to pLSI (Girolami and Kabán 2003).
- **Mixture of unigrams.** If every document has a single topic, LDA becomes a mixture of multinomials, the unsupervised form of a [naive Bayes classifier](/naive-bayes-classifier/). LDA lets each word of a document have its own topic, which is why it is called a mixed membership model.
- **Matrix factorization.** The expected document-word matrix is $\Theta \Phi$, a product of a $D \times K$ and a $K \times V$ nonnegative matrix whose rows sum to 1. So LDA is a probabilistic form of [nonnegative matrix factorization](/nonnegative-matrix-factorization/), and of [latent semantic analysis](/latent-semantic-analysis/), which uses an SVD instead.
- **Population genetics.** The admixture model of Pritchard, Stephens and Donnelly (2000) is the same model, with individuals as documents, alleles as words and ancestral populations as topics.
- **Nonparametric version.** The hierarchical [Dirichlet process](/dirichlet-process/) replaces the fixed $K$ with an unbounded number of topics shared by all documents.

## Known results in the model

### Collapsed Gibbs sampling

The sampler of Griffiths and Steyvers works on $z$ only, with $\theta$ and $\phi$ integrated out. It keeps the count tables, and it resamples one token at a time from its full conditional. A superscript $-i$ means "the counts without token $i$".

```pseudo id=main
COLLAPSED-GIBBS-LDA(w, K, α, β, S)
L1  assign each token a random topic z_di; fill the counts n_dk, n_kw, n_k
L2  repeat S sweeps
L3      for each document d and each token i of d, with word w = w_di
L4          remove token i: n_dk, n_kw, n_k each decrease by 1 for k = z_di
L5          p_k ← (n_dk + α)(n_kw + β) / (n_k + V β)   for k = 1, …, K
L6          draw z_di = k with probability p_k / Σ_j p_j
L7          add token i back: n_dk, n_kw, n_k each increase by 1 for the new k
L8  return z and the counts
L9  φ̂_kw ← (n_kw + β)/(n_k + Vβ);  θ̂_dk ← (n_dk + α)/(N_d + Kα)
```

**Theorem (the full conditional).** For token $i$ of document $d$ with word $w$,

$$P(z_{di} = k \mid z^{-i}, w, \alpha, \beta) = \frac{1}{C} \cdot (n^{-i}_{dk} + \alpha) \cdot \frac{n^{-i}_{kw} + \beta}{n^{-i}_k + V\beta},$$

where $C$ does not depend on $k$.

*Proof.* The conditional is proportional to the collapsed joint $P(w, z \mid \alpha, \beta)$ with $z_{di} = k$, as a function of $k$. Compare the joint with token $i$ set to topic $k$ against the joint without token $i$. Only four factors change. $\Gamma(n_{dk} + \alpha)$ goes from $\Gamma(n^{-i}_{dk} + \alpha)$ to $\Gamma(n^{-i}_{dk} + \alpha + 1)$, a factor $n^{-i}_{dk} + \alpha$, because $\Gamma(x + 1) = x\,\Gamma(x)$. In the same way $\Gamma(n_{kw} + \beta)$ gives a factor $n^{-i}_{kw} + \beta$, and $1/\Gamma(V\beta + n_k)$ gives a factor $1/(n^{-i}_k + V\beta)$. The document factor $1/\Gamma(K\alpha + N_d)$ changes by $1/(N_d - 1 + K\alpha)$ for every $k$, so it goes into $C$, and no other factor depends on $k$. $\square$

The tests of this page check this identity exactly with rational $\alpha$ and $\beta$: line L5, normalized, equals the ratio of the exact collapsed joints computed with rising factorials.

**The chain is correct.** Each step of lines L4 to L7 is a [Gibbs](/gibbs-sampling/) update: it draws one variable from its exact full conditional, so it leaves $P(z \mid w)$ invariant. Since $\alpha, \beta > 0$, every $p_k$ is positive, so from any assignment the chain can reach any other one token at a time. The chain is irreducible and aperiodic on a finite state space, so the distribution of $z$ after $S$ sweeps converges to $P(z \mid w)$ as $S \to \infty$. The tests check this on a corpus of two documents of two words, where the 16 assignments can be enumerated: after 40000 sweeps the visit frequencies are within total variation 0.02 of the exact posterior.

**Cost.** Lines L4, L6 and L7 cost $O(1)$, $O(K)$ and $O(1)$, and line L5 costs $O(K)$, so a sweep costs $O(NK)$ time. The memory is $O(N + DK + KV)$ for $z$ and the three tables. Samplers that use the sparsity of the counts, such as SparseLDA (Yao, Mimno and McCallum 2009) and alias table methods, bring the cost per token far below $K$ for large $K$.

### A worked example

Take the vocabulary ball, game, goal, vote, law, party, and five documents:

| document | words |
|---|---|
| 1 | ball game goal ball |
| 2 | vote law party vote |
| 3 | game goal ball goal |
| 4 | law party vote law |
| 5 | ball vote game law |

With $K = 2$, $\alpha = 0.5$, $\beta = 0.1$, and 200 sweeps from a random start with seed 2, the final sample gives every word of documents 1 and 3 topic 0, every word of documents 2 and 4 topic 1, and the words of document 5 the topics 0, 1, 0, 1. The estimates are

| topic | ball | game | goal | vote | law | party |
|---|---|---|---|---|---|---|
| 0 | 0.387 | 0.292 | 0.292 | 0.009 | 0.009 | 0.009 |
| 1 | 0.009 | 0.009 | 0.009 | 0.387 | 0.387 | 0.198 |

For example $\hat\phi_{0,\text{ball}} = (4 + 0.1)/(10 + 0.6) \approx 0.387$. The mixtures are $\hat\theta_1 = (0.9, 0.1)$ and $\hat\theta_5 = (0.5, 0.5)$: document 5 is half sport and half politics.

One step of the sampler by hand: remove the token "ball" of document 5. Then $n_{5,0} = 1$, $n_{5,1} = 2$, $n_{0,\text{ball}} = 3$, $n_{1,\text{ball}} = 0$, $n_0 = 9$ and $n_1 = 10$, so line L5 gives

$$p_0 = 1.5 \cdot \frac{3.1}{9.6} \approx 0.4844, \qquad p_1 = 2.5 \cdot \frac{0.1}{10.6} \approx 0.0236,$$

and the token goes back to topic 0 with probability $0.9536$. The document prefers topic 1 slightly (2 words against 1), but the word "ball" has never been seen in topic 1, and the word factor wins.

With seed 3 the same split comes out with the topic numbers swapped, and with seed 1 the final sample is a less clean split, in which topic 0 holds mostly ball and goal. One sample from a small corpus is noisy, and the topic labels have no meaning of their own.

### Variational EM

Blei et al. approximate the posterior of one document by the fully factorized family $q(\theta, z) = q(\theta \mid \gamma) \prod_i q(z_i \mid \varphi_i)$, a [mean field](/mean-field-approximation/) form of [variational inference](/variational-inference/). Maximizing the [evidence lower bound](/evidence-lower-bound/) gives the coordinate updates

$$\varphi_{ik} \propto \phi_{k w_i} \exp\big(\Psi(\gamma_k)\big), \qquad \gamma_k = \alpha + \sum_i \varphi_{ik},$$

where $\Psi$ is the digamma function (Section 5.2). These are iterated to a fixed point for each document (the E step), and then $\phi$ and $\alpha$ are updated from the expected counts (the M step, Section 5.3). Each iteration costs $O(N_d K)$ for a document. Hoffman, Blei and Bach (2010) made the M step stochastic over minibatches of documents, which is [stochastic variational inference](/stochastic-variational-inference/) for LDA. The variational method is deterministic and easy to run in parallel. The Gibbs sampler is simpler and is asymptotically exact, but needs many sweeps.

### Hardness and provable learning

Sontag and Roy (2011) studied exact inference for one document with known topics. Finding the most probable topic assignment $z$, with $\theta$ integrated out, takes polynomial time when the number of topics that the document uses is a constant, and is NP-hard when a document uses many topics. Finding the most probable $\theta$ is also NP-hard. So the approximations above are not only a matter of convenience.

Learning the topics is a different problem. Arora, Ge and Moitra (2012) gave a polynomial time algorithm with provable guarantees under a *separability* assumption: each topic has an anchor word that has positive probability in that topic and zero in all others. The method finds the anchor words from the word co-occurrence matrix, using ideas from nonnegative matrix factorization.

### Pitfalls

- **Expecting one right answer.** The posterior is multimodal and invariant under permutations of the topics. Different runs give different topic numbers and often different topics. Do not average $\hat\phi$ over runs without first matching the topics.
- **Averaging samples across a label switch.** Within one long run, the topics can, in principle, swap. In practice this is rare for large corpora, but samples should be checked before averaging.
- **Wrong hyperparameters.** A large $\alpha$ makes every document a flat mix of all topics, and a small $\alpha$ makes documents use few topics. Griffiths and Steyvers used $\alpha = 50/K$ and $\beta = 0.1$. Learning $\alpha$, and using an asymmetric $\alpha$, often helps.
- **Stop words.** Very frequent words such as "the" fill every topic. Remove them, or use a model that has a background topic.
- **Forgetting to remove the token.** Line L5 uses the counts without token $i$. Using the counts with it biases each token toward its current topic, and the chain no longer has the right stationary distribution.

## References
