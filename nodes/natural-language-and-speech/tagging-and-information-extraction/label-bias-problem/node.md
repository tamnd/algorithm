---
tag: 37R4JQ
kind: concept
slug: label-bias-problem
name: Label bias problem
aliases:
- label bias
area: natural-language-and-speech/tagging-and-information-extraction
level: advanced
summary: "In locally normalized models such as MEMMs, states with few successors pass on their mass whatever the input, which motivated CRFs."
prereqs: [maximum-entropy-markov-model]
see_also: [conditional-random-field, structured-perceptron, hmm-part-of-speech-tagger, sequence-labeling, generative-vs-discriminative-models, partition-function, exposure-bias, beam-search]
sources:
  - paper: "John Lafferty, Andrew McCallum and Fernando Pereira, Conditional random fields: probabilistic models for segmenting and labeling sequence data, Proceedings of ICML 2001, pages 282 to 289"
    title: "Lafferty, McCallum and Pereira 2001"
    locator: "Section 2 (the label bias problem, Figure 1 with rib and rob), Section 5.1 (synthetic data, MEMM 42% error against CRF 4.6%), Section 5.3 (part-of-speech tagging)"
  - paper: "Léon Bottou, Une approche théorique de l'apprentissage connexionniste: applications à la reconnaissance de la parole, PhD thesis, Université de Paris XI, Orsay, 1991"
    title: Bottou 1991
    locator: "discriminative Markov models, the conservation of score mass and its two fixes, as cited by Lafferty et al. (2001, Sections 1 and 2)"
  - paper: "Andrew McCallum, Dayne Freitag and Fernando Pereira, Maximum entropy Markov models for information extraction and segmentation, Proceedings of ICML 2000, pages 591 to 598"
    title: "McCallum, Freitag and Pereira 2000"
    locator: "the MEMM, with one normalized next-state distribution per source state"
---

The label bias problem is a weakness of sequence models that normalize each step on its own, such as the [maximum entropy Markov model](/maximum-entropy-markov-model/). At each step, the scores of the next states must sum to 1, whatever the current input is. So a state with one successor passes all its mass on and ignores the input, and in general paths through states with few successors are preferred. Lafferty, McCallum and Pereira (2001) named the problem and used it to motivate the [conditional random field](/conditional-random-field/), which has one normalizer for the whole sequence. The MEMM page defines the model; this page explains the bias and how to avoid it.

## In plain words

Think of a path through a set of rooms. In each room, a judge looks at the next letter of the input and splits one unit of credit among the doors out of that room. If a room has only one door, that door gets the full unit, whether the letter fits or not. So a path that goes through rooms with few doors loses no credit at those rooms, even when the input says it is the wrong path. The model sees the input at those steps, but it cannot use it. The fix is to let every step give any amount of credit, large or small, and to compare whole paths only at the end.

## The idea

A locally normalized model gives a sequence $y = y_1 \ldots y_n$ for input $x$ the probability

$$P(y \mid x) = \prod_{i=1}^{n} P(y_i \mid y_{i-1}, x), \qquad \sum_{y_i} P(y_i \mid y_{i-1}, x) = 1 \text{ for every } y_{i-1} \text{ and } x.$$

The constraint on the right is the cause. It is a conservation of mass: the input at step $i$ can only decide how the mass of state $y_{i-1}$ is split among its successors, not how much mass leaves $y_{i-1}$. Two consequences follow, and both are theorems about the model class.

- A state $s$ whose only allowed successor is $t$ has $P(t \mid s, x) = 1$ for every input $x$. The input at that step has no effect on the score of any path through $s$.
- More generally, the score of a path depends on the input at step $i$ only through the split at $y_{i-1}$. A state with a low-entropy successor distribution loses little mass whatever it sees, so the path through it can win against a path that fits the input better.

Changing the features does not remove this, since every choice of weights obeys the same constraint. A globally normalized model removes it. The linear-chain CRF scores a path by $\exp(\sum_i w \cdot f(x, i, y_{i-1}, y_i))$, where each factor can be any positive number, and divides by one [partition function](/partition-function/) $Z(x)$, the sum over all paths. A factor can now be small when the input does not fit, so a path through a state with one successor can lose weight at that step. The [structured perceptron](/structured-perceptron/) has no normalization at all and so also avoids the problem. An HMM is locally normalized too, but over $P(y_i \mid y_{i-1}) P(x_i \mid y_i)$; the emission term depends on the input at every state, so a state that does not fit the word gets a small factor, and the HMM does not have label bias in this form.

## Examples

**Rib and rob** (Lafferty et al. 2001, Figure 1, after Bottou 1991). A finite-state model reads the words "rib" and "rob". From the start state 0, the path 0, 1, 2, 3 reads r, i, b and the path 0, 4, 5, 3 reads r, o, b. States 1, 2, 4 and 5 have one successor each. For the input "rib", the MEMM gives

$$P(0\,1\,2\,3 \mid \text{rib}) = P(1 \mid 0, r) \cdot P(2 \mid 1, i) \cdot P(3 \mid 2, b) = P(1 \mid 0, r) \cdot 1 \cdot 1,$$

and in the same way $P(0\,4\,5\,3 \mid \text{rib}) = P(4 \mid 0, r)$. The letter i, which is the only letter that tells the words apart, does not appear in either score. Both paths see the same first letter r, so the model gives "rib" and "rob" the same pair of scores. If "rob" is a little more frequent in training, $P(4 \mid 0, r) > P(1 \mid 0, r)$, and the model reads every input as "rob".

**A small number example.** Let state A have one successor A2, and let state B have two successors B2 and C. Let the first step give $P(A \mid \langle s \rangle, x_1) = 0.6$ and $P(B \mid \langle s \rangle, x_1) = 0.4$. At the second step, the word $x_2$ fits B2 well and does not fit A2 at all. Whatever the features say, $P(A2 \mid A, x_2) = 1$, so the path A, A2 has probability 0.6. Even if $P(B2 \mid B, x_2) = 0.99$, the path B, B2 has only $0.4 \cdot 0.99 = 0.396$. The model picks A, A2 although the second word speaks against it. In a CRF, the factor of the edge from A to A2 can be made small for this word, for example 0.01, and then B, B2 wins.

**Measurements.** On synthetic data built to show the effect, Lafferty et al. (2001, Section 5.1) measured an error rate of 42% for the MEMM and 4.6% for the CRF. On Penn Treebank part-of-speech tagging with first-order features (Section 5.3), the MEMM had 6.37% error, worse than the HMM at 5.69% and the CRF at 5.55%. These are measurements, and on real tagging data the gap is small because most tag states have many successors.

## Where it is used

- It is the main reason given for the [conditional random field](/conditional-random-field/) in Lafferty et al. (2001), and an argument for globally trained models such as the [structured perceptron](/structured-perceptron/).
- It explains why a fully connected tag model suffers less than a sparse finite-state model: when every tag can follow every tag, the local distributions can still react to the input. Lafferty et al. (2001, Section 2) report two other fixes that Bottou (1991) discussed. One is to change the state structure, for example to merge states 1 and 4 in the rib and rob model and branch only at the letter that decides; this is a form of determinization, which for weighted machines is not always possible and can make the model much larger. The other is to start from a fully connected model and let training find the structure, which gives up the prior knowledge built into the structure.
- The same argument applies to any left-to-right model that normalizes each decision, for example greedy or [beam search](/beam-search/) decoders with a softmax per step. It is a separate problem from [exposure bias](/exposure-bias/), which comes from training on gold history and testing on predicted history.
- Lafferty et al. (2001, Section 2) list other models that can suffer from it: discriminative Markov models (Bottou 1991), the maximum entropy tagger of Ratnaparkhi (1996), MEMMs, and taggers built from independently trained next-state classifiers. The phrase "conservation of score mass" and the rib and rob example come from Bottou (1991).

## References
