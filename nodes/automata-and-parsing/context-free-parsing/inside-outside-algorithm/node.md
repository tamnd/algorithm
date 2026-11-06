---
tag: 9H2A1G
kind: algorithm
slug: inside-outside-algorithm
name: Inside-outside algorithm
area: automata-and-parsing/context-free-parsing
level: research
summary: Estimates PCFG rule probabilities by expectation-maximization over parse chart sums.
solves: [maximum-likelihood-estimation]
model: word-ram
complexity:
  vars: {n: the length of a training sentence, G: the grammar size (the sum over all rules of the right side length plus one), N: the number of nonterminals}
  time: {worst: O(n^3 G), best: O(n^3)}
  space: {extra: O(n^2 N + G)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1979
  people: [James K. Baker]
  note: Baker described the algorithm in 1979 for speech recognition, as a counterpart of the forward-backward algorithm of hidden Markov models. Lari and Young studied it in detail in 1990.
prereqs: [probabilistic-context-free-grammar, cyk-algorithm, expectation-maximization]
see_also: [probabilistic-cky, forward-backward-algorithm, baum-welch-algorithm, chomsky-normal-form, earley-parser, log-sum-exp-trick, viterbi-algorithm, hidden-markov-model]
sources:
  - paper: doi:10.1121/1.2017061
    title: J. K. Baker, Trainable grammars for speech recognition, The Journal of the Acoustical Society of America 65(S1) (1979)
    locator: p. S132 (meeting abstract)
  - paper: doi:10.1016/0885-2308(90)90022-x
    title: K. Lari and S. J. Young, The estimation of stochastic context-free grammars using the Inside-Outside algorithm, Computer Speech and Language 4(1) (1990)
    locator: pp. 35 to 56
  - paper: doi:10.1016/0885-2308(91)90009-f
    title: K. Lari and S. J. Young, Applications of stochastic context-free grammars using the Inside-Outside algorithm, Computer Speech and Language 5(3) (1991)
    locator: pp. 237 to 257
  - paper: doi:10.3115/981967.981984
    title: Fernando Pereira and Yves Schabes, Inside-outside reestimation from partially bracketed corpora, 30th Annual Meeting of the Association for Computational Linguistics (1992)
    locator: pp. 128 to 135
  - paper: doi:10.1111/j.2517-6161.1977.tb01600.x
    title: A. P. Dempster, N. M. Laird and D. B. Rubin, Maximum likelihood from incomplete data via the EM algorithm, Journal of the Royal Statistical Society Series B 39(1) (1977)
    locator: pp. 1 to 22
  - paper: https://aclanthology.org/J95-2002/
    title: Andreas Stolcke, An efficient probabilistic context-free parsing algorithm that computes prefix probabilities, Computational Linguistics 21(2) (1995)
    locator: pp. 165 to 201
  - paper: https://aclanthology.org/J98-2005/
    title: Zhiyi Chi and Stuart Geman, Estimation of probabilistic context-free grammars, Computational Linguistics 24(2) (1998)
    locator: pp. 299 to 305
  - paper: doi:10.18653/v1/w16-5901
    title: Jason Eisner, Inside-outside and forward-backward algorithms are just backprop, Workshop on Structured Prediction for NLP (2016)
    locator: pp. 1 to 17
---

The inside-outside algorithm trains a [probabilistic context-free grammar](/probabilistic-context-free-grammar/): given sentences without parse trees, it adjusts the rule probabilities so that the sentences become more likely. Each step computes, with two chart passes like the [CYK algorithm](/cyk-algorithm/), how often each rule is used on average over all parse trees of each sentence, and then sets the new probabilities in proportion to these counts. It is the [expectation-maximization](/expectation-maximization/) method for grammars, and it does to a grammar what the [forward-backward algorithm](/forward-backward-algorithm/) does to a [hidden Markov model](/hidden-markov-model/).

## In plain words

A probabilistic grammar gives each rule a chance, and a parse tree has the product of the chances of its rules. A sentence can have many trees. If we knew the right tree for each sentence, we could count the rules and turn the counts into chances. We do not know the trees, so we count with weights: each tree counts as much as its share of the total chance of the sentence. Two tables make this fast. The inside table holds, for each piece of the sentence and each placeholder, the total chance that the placeholder makes that piece. The outside table holds the total chance of everything around it. Their product says how likely the placeholder covers that piece. From these numbers we get the weighted counts, and then new chances. Repeating this never makes the sentences less likely.

## The problem

We use the notation of the grammar pages: productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ the start symbol, $n$ the input length, and the grammar size $|G| = \sum_{A \to \alpha} (|\alpha| + 1)$.

The grammar $G = (V, \Sigma, P, S)$ is in [Chomsky normal form](/chomsky-normal-form/): every rule is $A \to B C$ or $A \to a$, and $S \to \varepsilon$ is allowed when $S$ is on no right side. A weight $\theta(r) \ge 0$ is given for each rule, and the weights of the rules of each nonterminal sum to 1. A tree $t$ has the probability $P_\theta(t) = \prod_r \theta(r)^{f_r(t)}$, where $f_r(t)$ is the number of uses of rule $r$ in $t$. A sentence $w$ has the probability $Z_\theta(w) = \sum_t P_\theta(t)$, over the parse trees $t$ of $w$.

The input is $G$, $\theta$ and a corpus of sentences. The goal is the [maximum likelihood estimate](/maximum-likelihood-estimation/): the $\theta$ that maximizes $\prod_w Z_\theta(w)$. The likelihood can have many local maxima. The inside-outside algorithm does one step of a local search: it returns a new $\theta'$ with $\prod_w Z_{\theta'}(w) \ge \prod_w Z_\theta(w)$, and it is repeated until the likelihood stops growing.

## The algorithm

For a sentence $w = a_1 \cdots a_n$, the **inside** probability $\beta(A, i, j)$ is the total probability of the trees with root $A$ and yield $a_{i+1} \cdots a_j$. The **outside** probability $\alpha(A, i, j)$ is the total probability of the trees with root $S$ and yield $a_1 \cdots a_i\, A\, a_{j+1} \cdots a_n$, where $A$ is left as a leaf. The product $\alpha(A, i, j)\, \beta(A, i, j)$ is the total probability of the trees of $w$ with a node $A$ over $a_{i+1} \cdots a_j$.

```pseudo id=main
EM-STEP(G, θ, corpus)
L1  c(r) ← 0 for every rule r
L2  for each sentence w = a1 … an in the corpus do
L3      if n = 0 then (if θ(S → ε) > 0 then c(S → ε) ← c(S → ε) + 1); continue with the next sentence
L4      for i ← 0 to n − 1 do β(A, i, i + 1) ← θ(A → a_{i+1}) for every A        ▷ inside, short spans
L5      for ℓ ← 2 to n, i ← 0 to n − ℓ, j ← i + ℓ do β(A, i, j) ← Σ over A → B C and i < k < j of θ(A → B C) β(B, i, k) β(C, k, j)
L6      Z ← β(S, 0, n); if Z = 0 then continue with the next sentence
L7      α(A, i, j) ← 0 for all A, i, j; α(S, 0, n) ← 1                           ▷ outside, long spans first
L8      for ℓ ← n down to 2, i ← 0 to n − ℓ, j ← i + ℓ, each A → B C and i < k < j do
L9          α(B, i, k) += α(A, i, j) θ(A → B C) β(C, k, j);  α(C, k, j) += α(A, i, j) θ(A → B C) β(B, i, k)
L10     for each A → B C, and each i < k < j do c(A → B C) += α(A, i, j) θ(A → B C) β(B, i, k) β(C, k, j) / Z
L11     for each i < n and each A → a_{i+1} do c(A → a_{i+1}) += α(A, i, i + 1) θ(A → a_{i+1}) / Z
L12 for each rule A → γ do θ′(A → γ) ← c(A → γ) / Σ_γ′ c(A → γ′), or θ(A → γ) if this sum is 0
L13 return θ′
```

Lines L4 and L5 are the [CYK algorithm](/cyk-algorithm/) with sums of products in place of "or" and "and". Line L8 goes from long spans to short ones, so that $\alpha(A, i, j)$ is complete before it passes probability to the two children of $A$. Line L10 adds, for every place where a rule can apply, the probability of all trees that use it there, divided by the probability of the sentence; this is the expected number of uses of the rule, given the sentence. Line L12 is the maximization step: it turns the expected counts into probabilities, one nonterminal at a time.

## Example

Take the ambiguous grammar $S \to S S \mid A S \mid b$, $A \to a \mid b$, with $\theta = 1/3$ for each rule of $S$ and $1/2$ for each rule of $A$, and the corpus with one sentence $w = b\, b$. It has two trees: $S \to S S$ with two $S \to b$, of probability $(1/3)^3 = 2/54$, and $S \to A S$ with $A \to b$ and $S \to b$, of probability $1/3 \cdot 1/2 \cdot 1/3 = 3/54$.

| Span $(i, j)$ | $\beta(S, i, j)$ | $\beta(A, i, j)$ | $\alpha(S, i, j)$ | $\alpha(A, i, j)$ |
|---|---|---|---|---|
| $(0, 1)$ | $1/3$ | $1/2$ | $1/9$ | $1/9$ |
| $(1, 2)$ | $1/3$ | $1/2$ | $5/18$ | $0$ |
| $(0, 2)$ | $5/54$ | $0$ | $1$ | $0$ |

So $Z = \beta(S, 0, 2) = 5/54$. The outside value $\alpha(S, 1, 2) = 1/3 \cdot \beta(S, 0, 1) + 1/3 \cdot \beta(A, 0, 1) = 1/9 + 1/6 = 5/18$ collects both trees, while $\alpha(S, 0, 1) = 1/3 \cdot \beta(S, 1, 2)$ and $\alpha(A, 0, 1) = 1/3 \cdot \beta(S, 1, 2)$ each come from one tree. The products divided by $Z$ give the chance of each node: $S$ over the first $b$ with $1/27 \cdot 54/5 = 2/5$, $A$ over the first $b$ with $3/5$, and $S$ over the second $b$ with 1.

The expected counts are $c(S \to S S) = 2/5$, $c(S \to A S) = 3/5$, $c(S \to b) = 2 \cdot 2/5 + 1 \cdot 3/5 = 7/5$, $c(A \to b) = 3/5$ and $c(A \to a) = 0$. The rules of $S$ have the total $12/5$, so line L12 gives $\theta'(S \to S S) = 1/6$, $\theta'(S \to A S) = 1/4$, $\theta'(S \to b) = 7/12$, $\theta'(A \to b) = 1$ and $\theta'(A \to a) = 0$. The probability of $w$ grows from $5/54 \approx 0.093$ to $1/6 \cdot (7/12)^2 + 1/4 \cdot 7/12 = 175/864 \approx 0.203$.

## Correctness

**Claim.** For each sentence $w$ with $Z_\theta(w) > 0$, lines L3 to L11 add $E_\theta[f_r \mid w] = \sum_t P_\theta(t) f_r(t) / Z_\theta(w)$ to $c(r)$. The returned $\theta'$ satisfies $\prod_w Z_{\theta'}(w) \ge \prod_w Z_\theta(w)$, over the sentences with $Z_\theta(w) > 0$.

*Inside and outside.* In Chomsky normal form every node has a nonempty yield, and the two children split the span of their parent at a point $k$ strictly inside. So a tree is fixed by its root rule, the split and its two subtrees, and the inside recurrence of line L5 sums every tree once, by induction on the span length. In the same way, an outside tree for $(A, i, j)$ is cut at the parent of the hole into an outside tree for the parent, which has a longer span, and a complete tree for the sibling. This gives the recurrence of line L9, by induction from the full span down.

*Counts.* A tree has at most one node with a given span, because nested nodes have different spans. So the trees with a node $A$ over $(i, j)$ that uses $A \to B C$ at the split $k$ are exactly the combinations of an outside tree for $(A, i, j)$ and inside trees for $(B, i, k)$ and $(C, k, j)$. Their total probability is the term of line L10, and the sum over $i < k < j$ is $\sum_t P_\theta(t) f_r(t)$.

*Monotone likelihood.* By Jensen's inequality, for every $\theta'$, $\log Z_{\theta'}(w) - \log Z_\theta(w) \ge \sum_r E_\theta[f_r \mid w] (\log \theta'(r) - \log \theta(r))$. The right side, summed over the corpus, is $Q(\theta') - Q(\theta)$ with $Q(\theta') = \sum_r c(r) \log \theta'(r)$, and line L12 maximizes $Q$ under the constraint that the rules of each nonterminal sum to 1. So the likelihood does not decrease. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The input is a sentence of length $n$, and the time below is for one sentence in one step; a step over a corpus costs the sum over its sentences, plus $O(|G|)$ for line L12.

- **Inside.** Line L5 considers $O(n^3)$ triples $i < k < j$ and, for each, the binary rules, so it takes $O(n^3 |G|)$ time. Line L4 takes $O(n |G|)$.
- **Outside and counts.** Lines L8 to L11 visit the same triples and rules, also in $O(n^3 |G|)$ time.
- **Space.** The charts $\alpha$ and $\beta$ have $O(n^2 N)$ entries, where $N = |V|$, and the counts take $O(|G|)$ space.
- **Iterations.** The number of EM steps until the likelihood stops growing is not bounded in advance. In practice it is set by a tolerance on the change in the log likelihood.

The inside pass alone, $O(n^3 |G|)$, is also the cost of computing the probability of one sentence.

## Properties

- **Exact expectations.** The counts are exact sums over all parse trees, which can be exponentially many; the charts share the common parts.
- **Monotone.** Each step keeps or increases the likelihood of the corpus. It converges to a stationary point, often a local maximum, and the result depends on the starting $\theta$.
- **Normalized output.** The new probabilities of each nonterminal sum to 1. Chi and Geman showed that the maximum likelihood estimates of a PCFG are proper: the probabilities of all trees sum to 1.
- **Zeros stay zero.** A rule with $\theta(r) = 0$ is never used in a tree of positive probability, so it gets the count 0 and keeps the probability 0.
- **Cubic in the sentence.** Like CYK, each step costs $O(n^3 |G|)$ per sentence, which limits it to short sentences and small grammars.

## Variants and improvements

- **Scaling and log space.** For long sentences the products underflow in floating point. Keep the values with a scale factor per span, or in log space with the [log-sum-exp trick](/log-sum-exp-trick/).
- **Bracketed corpora.** Pereira and Schabes allowed partial brackets in the training sentences: spans that cross a bracket get inside probability 0. This guides the grammar to linguistically sensible trees and makes each step faster.
- **General grammars.** Stolcke gave an Earley-based probabilistic parser that computes inside and outside probabilities for grammars that are not in normal form, including unit and empty rules, with a matrix inverse for the unit chains. It also gives prefix probabilities.
- **Viterbi training.** Replacing the sums by maxima, as in [probabilistic CKY](/probabilistic-cky/), counts only the best tree of each sentence. It is cheaper and often converges faster, but it does not maximize the likelihood.
- **Semirings and backpropagation.** Inside and outside are one computation in two semirings. Eisner showed that the outside pass is the reverse-mode derivative of the inside pass: $\partial \log Z / \partial \log \theta(r)$ is the expected count of $r$, so automatic differentiation of the inside algorithm gives the counts.
- **Hidden Markov models.** A right-linear grammar is a hidden Markov model, and on it the inside-outside algorithm becomes the [Baum-Welch algorithm](/baum-welch-algorithm/), and its time per sentence drops from cubic to linear in $n$.

## When to use it

Use the inside-outside algorithm to learn rule probabilities for a fixed set of rules from sentences without trees, for example in speech recognition, in RNA secondary structure models, or as a baseline for grammar induction. When trees are given, count the rules directly instead. For large grammars and long sentences, the cubic cost per step and the many steps make it slow, and the result depends on the starting point; run it from several starts, or start from a good guess. To find the best parse once the probabilities are known, use [probabilistic CKY](/probabilistic-cky/) or the [Viterbi algorithm](/viterbi-algorithm/) on the same charts.

## Pitfalls

- **Underflow.** Products of many probabilities fall below the smallest float for sentences of a few dozen words. Scale or use logarithms.
- **Local maxima.** EM finds a local maximum only. Grammars trained from a uniform or random start often learn structures that have nothing to do with linguistic phrases.
- **Symmetric start.** If two nonterminals have the same rules and the same probabilities, EM keeps them identical forever. Break the symmetry with small random changes.
- **Sentences of probability 0.** If the grammar cannot derive a sentence, its $Z$ is 0, and dividing by it fails. Skip such sentences, as line L6 does, or give every needed rule a small positive probability.
- **Normal form changes the model.** Converting a grammar to Chomsky normal form changes its rules, so the learned probabilities belong to the new rules. Use a variant for general grammars if the original rules matter.
- **Recursion depth.** Compute the charts with loops over span lengths, not with recursion over subtrees.

## Implementations

## History

Baker introduced the algorithm in 1979 for speech recognition, as the counterpart for context-free grammars of the forward-backward algorithm of hidden Markov models. The general method of expectation-maximization had been described by Dempster, Laird and Rubin in 1977. Lari and Young gave a detailed study and applications in 1990 and 1991, and Pereira and Schabes added bracketed training data in 1992. Stolcke extended the computation to general grammars with an Earley parser in 1995, and Eisner explained the outside pass as backpropagation in 2016.

## References
