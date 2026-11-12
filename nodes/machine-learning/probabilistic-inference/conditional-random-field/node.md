---
tag: 1TRP6G
kind: model
slug: conditional-random-field
name: Conditional random field
aliases:
- CRF
- linear-chain CRF
area: machine-learning/probabilistic-inference
level: advanced
summary: "A discriminative undirected model of P(labels | observations). A linear-chain CRF is trained by a concave likelihood and decoded by Viterbi in O(n k^2)."
history:
  year: 2001
  people: [John Lafferty, Andrew McCallum, Fernando Pereira]
  note: Lafferty, McCallum and Pereira introduced conditional random fields at ICML 2001 to label sequences without the label bias of maximum entropy Markov models.
prereqs: [markov-random-field, logistic-regression, forward-backward-algorithm]
see_also: [hidden-markov-model, viterbi-algorithm, structured-prediction, generative-vs-discriminative-models, softmax-regression, partition-function, loopy-belief-propagation, limited-memory-bfgs]
sources:
  - paper: "John Lafferty, Andrew McCallum and Fernando Pereira, Conditional random fields: probabilistic models for segmenting and labeling sequence data, Proceedings of ICML 2001, pp. 282-289"
    title: Lafferty, McCallum and Pereira 2001
    locator: the definition of a CRF as a random field globally conditioned on the observations, the label bias problem with the rib and rob example, the linear-chain form and the iterative scaling training
  - paper: doi:10.1561/2200000013
    title: "Charles Sutton and Andrew McCallum, An introduction to conditional random fields, Foundations and Trends in Machine Learning 4(4):267-373, 2012"
    locator: "Section 2 (modeling: generative and discriminative models, linear-chain CRFs, general CRFs, features), Section 4 (inference: forward-backward and Viterbi), Section 5 (parameter estimation: the concave likelihood, the gradient, regularization and stochastic gradient)"
  - paper: "Andrew McCallum, Dayne Freitag and Fernando Pereira, Maximum entropy Markov models for information extraction and segmentation, Proceedings of ICML 2000, pp. 591-598"
    title: McCallum, Freitag and Pereira 2000
    locator: the MEMM, with one locally normalized maximum entropy model per source state
  - book: isbn:9780262013192
    title: Daphne Koller and Nir Friedman, Probabilistic Graphical Models, MIT Press, 2009
    locator: "Section 4.6.1 (conditional random fields), Chapter 20 (learning undirected models, with conditionally trained models)"
  - paper: "Fei Sha and Fernando Pereira, Shallow parsing with conditional random fields, Proceedings of HLT-NAACL 2003, pp. 213-220"
    title: Sha and Pereira 2003
    locator: training linear-chain CRFs with L-BFGS and conjugate gradient, much faster than iterative scaling
  - paper: "Michael Collins, Discriminative training methods for hidden Markov models: theory and experiments with perceptron algorithms, Proceedings of EMNLP 2002, pp. 1-8"
    title: Collins 2002
    locator: the structured perceptron, which uses the same features and Viterbi but no partition function
---

A conditional random field (CRF) is an undirected graphical model of the conditional distribution $P(y \mid x)$ of a structured output $y$, such as a sequence of labels, given an input $x$, such as a sentence. It is a [Markov random field](/markov-random-field/) over $y$ whose potentials may look at all of $x$, and it never models $x$ itself. Lafferty, McCallum and Pereira introduced it in 2001. In the common *linear-chain* form the labels form a chain, $P(y \mid x)$ is a log-linear model with a feature vector that adds up over neighbouring label pairs, the conditional log likelihood is concave, its gradient is "observed feature counts minus expected feature counts", and the expected counts and the best labeling both come from dynamic programs in $O(n k^2)$ time for $n$ positions and $k$ labels.

## The machine

**General form.** Let $x$ be the observations and $y = (y_1, \ldots, y_n)$ the labels, each in a finite set $\mathcal{Y}$ of size $k$. Let $G$ be an undirected graph on the label variables, with a set $\mathcal{C}$ of cliques. A CRF is

$$P_\theta(y \mid x) = \frac{1}{Z_\theta(x)} \prod_{c \in \mathcal{C}} \psi_c(y_c, x), \qquad \psi_c(y_c, x) = \exp\Big(\sum_j \theta_j f_j(c, y_c, x)\Big),$$

$$Z_\theta(x) = \sum_{y'} \prod_{c \in \mathcal{C}} \psi_c(y'_c, x).$$

The feature functions $f_j$ are fixed by the designer, the weights $\theta_j$ are learned, and each potential may use the whole input $x$. Lafferty et al. state the definition as: conditioned on $x$, the random variables $y_v$ obey the Markov property with respect to $G$. The normalizer $Z_\theta(x)$ is the [partition function](/partition-function/), and it depends on $x$, so there is one for each input. This is the difference from a plain Markov random field over $(x, y)$.

**Linear chain.** When $G$ is a path, the cliques are the pairs $(y_{t-1}, y_t)$ and the score is

$$s_\theta(x, y) = \sum_{t=1}^{n} \sum_j \theta_j f_j(y_{t-1}, y_t, x, t), \qquad P_\theta(y \mid x) = \frac{\exp s_\theta(x, y)}{Z_\theta(x)}.$$

The implementation on this page uses the common special case of start weights $S_b$, transition weights $T_{ab}$, and weights $W_{bf}$ for the pair (label $b$, observation feature $f$):

$$s_\theta(x, y) = S_{y_1} + \sum_{t=1}^{n} e_t(y_t) + \sum_{t=2}^{n} T_{y_{t-1} y_t}, \qquad e_t(b) = \sum_{f \in x_t} W_{bf},$$

where $x_t$ is the set of binary features that are on at position $t$, such as "the word is *the*" or "the word ends in *-ing*". Any feature of $x$ at any position may enter $x_t$; the model makes no independence assumption about the features.

**Training.** Given labeled pairs $(x^{(i)}, y^{(i)})$, the weights maximize the conditional log likelihood with a Gaussian prior, also called an L2 penalty:

$$\ell(\theta) = \sum_i \log P_\theta(y^{(i)} \mid x^{(i)}) - \frac{\lambda}{2} \|\theta\|^2.$$

## What it counts

The cost of the model is measured in arithmetic operations on reals for one input of length $n$, with $k$ labels and $a$ active features at each position on average. Three quantities are needed.

- **The partition function $Z_\theta(x)$,** for the likelihood.
- **The marginals** $\mu_t(b) = P(y_t = b \mid x)$ and $\xi_t(a, b) = P(y_{t-1} = a, y_t = b \mid x)$, for the gradient.
- **The best labeling** $\arg\max_y P_\theta(y \mid x)$, for prediction. It does not need $Z$.

A sum over all $k^n$ labelings is not feasible, so the linear chain matters: on a chain, all three are computed exactly in $O(n(k^2 + k a))$ time. On a graph with cycles the same quantities are as hard as for any Markov random field, and approximate inference is used.

## Relation to other models

- **Hidden Markov models.** An [HMM](/hidden-markov-model/) defines a joint $P(x, y)$. Its conditional $P(y \mid x)$ is a linear-chain CRF with indicator features for the transitions and the emissions, and weights equal to the logarithms of the HMM probabilities (Sutton and McCallum, Section 2). The converse is false: a CRF may use many overlapping features of $x$, such as the word, its suffix and the next word, which an HMM cannot use without a model of how they depend on each other. The forward, backward and Viterbi recursions are those of the [forward-backward algorithm](/forward-backward-algorithm/) and the [Viterbi algorithm](/viterbi-algorithm/) with the potentials in place of the probabilities, and with $Z(x) \ne 1$ at the end.
- **Logistic regression.** For $n = 1$ there are no transitions, and a CRF is multiclass [logistic regression](/logistic-regression/), also called [softmax regression](/softmax-regression/). Sutton and McCallum describe the analogy: naive Bayes is to logistic regression as an HMM is to a linear-chain CRF. Each pair is a [generative and a discriminative](/generative-vs-discriminative-models/) model of the same form.
- **Maximum entropy Markov models.** A MEMM (McCallum, Freitag and Pereira 2000) is also discriminative, but it normalizes at each step: $P(y \mid x) = \prod_t P(y_t \mid y_{t-1}, x)$. That is the source of the label bias problem below. A CRF normalizes once, over whole sequences.
- **Markov random fields.** A CRF is a Markov random field over $y$ whose potentials are functions of $x$. The tools for MRFs, such as the [junction tree algorithm](/junction-tree-algorithm/), [loopy belief propagation](/loopy-belief-propagation/), and [mean field](/mean-field-approximation/), apply to a CRF for each fixed $x$.
- **Structured perceptron and margin methods.** Collins (2002) trains the same linear-chain score with the [perceptron](/perceptron/) update $\theta \leftarrow \theta + F(x, y) - F(x, \hat y)$, where $\hat y$ is the Viterbi labeling. It needs only Viterbi, not $Z$ and the marginals. Structured SVMs use the same score with a margin loss. See [structured prediction](/structured-prediction/).

## Known results in the model

### Inference and the gradient on a chain

Write $F(x, y)$ for the vector of feature counts of the labeling $y$, so that $s_\theta(x, y) = \theta^\top F(x, y)$. The procedure below computes $\log P_\theta(y \mid x)$, its gradient, and the Viterbi labeling. It works with logarithms, so the numbers do not underflow.

```pseudo id=main
CRF-LOG-LIKELIHOOD-AND-GRADIENT(θ, x, y)
L1  e_t(b) ← Σ_{f ∈ x_t} W_bf  for all t, b
L2  α_1(b) ← S_b + e_1(b);  α_t(b) ← e_t(b) + logsumexp_a (α_{t−1}(a) + T_ab);  log Z ← logsumexp_b α_n(b)
L3  β_n(b) ← 0;  β_t(a) ← logsumexp_b (T_ab + e_{t+1}(b) + β_{t+1}(b))
L4  μ_t(b) ← exp(α_t(b) + β_t(b) − log Z);  ξ_t(a, b) ← exp(α_{t−1}(a) + T_ab + e_t(b) + β_t(b) − log Z)
L5  g ← F(x, y) − (the same counts weighted by μ and ξ)
L6  return s_θ(x, y) − log Z, g

CRF-VITERBI(θ, x)
L7  δ_1(b) ← S_b + e_1(b)
L8  for t ← 2 to n
L9      δ_t(b) ← e_t(b) + max_a (δ_{t−1}(a) + T_ab);  ptr_t(b) ← the maximizing a
L10 ŷ_n ← argmax_b δ_n(b)
L11 for t ← n down to 2:  ŷ_{t−1} ← ptr_t(ŷ_t)
L12 return ŷ, δ_n(ŷ_n)
```

**Why it is correct.** By induction on $t$, $e^{\alpha_t(b)}$ is the sum of $\exp$ of the partial score over all label prefixes $y_{1..t}$ that end in $b$, because each prefix ending in $b$ extends exactly one prefix ending in some $a$, and adds $T_{ab} + e_t(b)$. So $\sum_b e^{\alpha_n(b)} = Z_\theta(x)$. In the same way $e^{\beta_t(a)}$ is the sum over the suffixes $y_{t+1..n}$ after $y_t = a$, and $e^{\alpha_t(b) + \beta_t(b)}$ is the sum over all labelings with $y_t = b$, which gives line L4. Line L9 is the same recursion with max in place of sum. Max distributes over addition just as sum distributes over product, so $\delta_t(b)$ is the best score of a prefix ending in $b$, and the pointers give a labeling that attains it.

**Cost.** Line L1 costs $O(n k a)$. Lines L2 to L4 and L7 to L9 each cost $O(n k^2)$, since each position takes a maximum or a log-sum over $k$ values for each of $k$ labels. Line L5 costs $O(n(k^2 + k a))$. The memory is $O(n k)$ for $\alpha$ and $\beta$, and $O(n k)$ for the pointers. One pass over a training set therefore costs $O\big(\sum_i n_i (k^2 + k a)\big)$.

### The likelihood is concave, and the gradient is a moment match

**Theorem.** For each $(x, y)$, $\log P_\theta(y \mid x)$ is a concave function of $\theta$, with

$$\nabla_\theta \log P_\theta(y \mid x) = F(x, y) - \mathbb{E}_{y' \sim P_\theta(\cdot \mid x)}\big[F(x, y')\big], \qquad \nabla^2_\theta \log P_\theta(y \mid x) = -\operatorname{Cov}_{y' \sim P_\theta(\cdot \mid x)}\big[F(x, y')\big].$$

*Proof.* $\log P_\theta(y \mid x) = \theta^\top F(x, y) - \log \sum_{y'} \exp(\theta^\top F(x, y'))$. The derivative of the second term with respect to $\theta_j$ is $\sum_{y'} F_j(x, y') e^{\theta^\top F(x, y')} / Z = \mathbb{E}[F_j]$. Differentiating once more gives $\mathbb{E}[F_j F_l] - \mathbb{E}[F_j]\mathbb{E}[F_l]$, a covariance matrix, which is positive semidefinite. So the Hessian of $\log P$ is negative semidefinite, and $\log P$ is concave. $\square$

So $\ell(\theta)$, a sum of concave functions minus a strictly convex penalty, is strictly concave for $\lambda > 0$ and has one maximizer. At it, the expected feature counts plus $\lambda \theta$ equal the observed counts. For a linear chain, $\mathbb{E}[F]$ is a sum of the marginals $\mu$ and $\xi$ of line L4, which is why the gradient needs forward-backward. Lafferty et al. trained with iterative scaling. Sha and Pereira (2003) showed that [L-BFGS](/limited-memory-bfgs/) and conjugate gradient are much faster, and [stochastic gradient descent](/stochastic-gradient-descent/) is common for large data. The tests of this page check the gradient against central finite differences, and check that gradient ascent with a small step never decreases $\ell$.

### A worked example

Take two labels A and B, three positions, $S = 0$, the transitions $T_{AA} = T_{BB} = 1$ and $T_{AB} = T_{BA} = 0$, and the emission scores $e_1 = (2, 0)$, $e_2 = (0, 1)$, $e_3 = (0, 2)$ for (A, B). The score of a labeling is the sum of its emission scores plus the number of neighbouring pairs that agree:

| $y$ | ABB | AAB | BBB | AAA | ABA | BAB | BBA | BAA |
|---|---|---|---|---|---|---|---|---|
| $s(x, y)$ | 6 | 5 | 5 | 4 | 3 | 2 | 2 | 1 |

So $Z = e^6 + 2e^5 + e^4 + e^3 + 2e^2 + e \approx 792.4352$. The forward pass gives $e^{\alpha_1} = (e^2, 1) \approx (7.3891, 1)$, then $e^{\alpha_2} = (e^3 + 1,\ e^3 + e^2) \approx (21.0855, 27.4746)$, then $e^{\alpha_3} \approx (84.7910, 707.6442)$, whose sum is $Z$. Viterbi returns ABB with score 6 and probability $e^6 / Z \approx 0.5091$. The marginals are $P(y_1 = A) \approx 0.7906$, $P(y_2 = B) \approx 0.7311$ and $P(y_3 = B) \approx 0.8930$. If the true labeling is ABB, the gradient for the weight of the feature on at position 1 with label A is $1 - 0.7906 = 0.2094$, so training raises that weight.

### Label bias

In a MEMM, each state passes all its probability mass on to its successors, whatever the observation is. Lafferty et al. give this example. One branch of a tagger reads *rib* through the states 1, 2, 3 and another reads *rob* through the states 4, 5, 6, and both start on *r*. State 1 has only one successor, so $P(2 \mid 1, x_2) = 1$ for every $x_2$, and in the same way $P(5 \mid 4, x_2) = 1$. On the input *rob*, the two paths have the probabilities $P(1 \mid r)$ and $P(4 \mid r)$, and the letter *o* plays no part. If *rib* was more frequent in training, the model reads *rob* as *rib*. A CRF scores the whole path before it normalizes, so a large weight for (state 5, letter *o*) makes the *rob* path win. More generally, per-step normalization lets a state with low entropy over its successors ignore its observation.

### General graphs

For a tree-structured $G$, belief propagation computes $Z$ and the marginals exactly in time linear in the number of nodes and polynomial in $k$. For graphs with cycles, such as grid CRFs for image labeling, computing $Z$ is #P-hard in general, as for any Markov random field with pairwise potentials, and exact inference costs time exponential in the treewidth by the [junction tree algorithm](/junction-tree-algorithm/). Practical systems then use loopy belief propagation or mean field for the marginals, or train with a surrogate such as the pseudolikelihood (Sutton and McCallum, Sections 4 and 5).

### Pitfalls

- **Underflow.** The products of potentials underflow for long sequences. Work with logarithms as above, or rescale $\alpha$ and $\beta$ at each position.
- **No regularization.** With many sparse features, a feature that separates the training data drives its weight to infinity. Use the L2 penalty or early stopping.
- **The wrong decoder.** Viterbi gives the most probable whole labeling. Taking $\arg\max_b \mu_t(b)$ at each position gives the labeling with the most expected correct labels, which can be a sequence of probability 0 under hard constraints. Choose by the error measure.
- **Forgetting that $Z$ depends on $x$.** The partition function must be computed for each training input at each gradient step. It cannot be cached across inputs, as it can be for a joint model.
- **Missing inputs.** A CRF has no model of $x$, so it cannot fill in a missing observation or learn from unlabeled $x$ without extra machinery.

## References
