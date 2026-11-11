---
tag: S2R9ZZ
kind: technique
slug: context-mixing
name: Context mixing
aliases:
- PAQ-style mixing
area: compression-and-coding/entropy-coding
level: research
summary: Predict each bit with many context models and combine their predictions with a mixer that learns online, then code the bit with a binary arithmetic coder. The method of PAQ.
prereqs: [context-modeling, logistic-regression]
see_also: [prediction-by-partial-matching, context-tree-weighting, adaptive-modeling, online-gradient-descent, logistic-loss, cross-entropy-loss, multiplicative-weights-update, arithmetic-coding]
sources:
  - paper: "Matthew V. Mahoney, Adaptive weighing of context models for lossless data compression, Technical Report CS-2005-16, Florida Institute of Technology, 2005"
    locator: the PAQ6 design, its context models and the update of the mixer weights by gradient descent on the coding cost
  - url: https://mattmahoney.net/dc/dce.html
    title: Matt Mahoney, Data Compression Explained
    locator: the sections on context mixing, logistic mixing, SSE and indirect context models
  - url: https://mattmahoney.net/dc/text.html
    title: Matt Mahoney, Large Text Compression Benchmark
    locator: the table of results on enwik8 and enwik9
  - paper: doi:10.1109/18.382012
    title: Frans M. J. Willems, Yuri M. Shtarkov and Tjalling J. Tjalkens, The context-tree weighting method, basic properties, IEEE Transactions on Information Theory 41(3), 653-664, 1995
    locator: the Bayesian mixture of context models, a fixed form of mixing
---

Context mixing (CM) is a way to build a compressor from many models. Each model looks at its own context, such as the last few bytes, the current word, or the bits in the same column of a table, and predicts the next bit. A *mixer* combines these predictions into one probability, and a binary [arithmetic coder](/arithmetic-coding/) codes the bit with it. After the bit is known, every model updates its statistics and the mixer updates its weights, so the decoder, which runs the same steps, stays in step. Matt Mahoney's PAQ series, from 2002 on, made the technique the strongest known approach to lossless compression of text and of many other kinds of data, at the price of speed. Since PAQ7 (2005), the mixer has been a small neural network: [logistic regression](/logistic-regression/) on the stretched predictions, trained online.

## In plain words

Several experts each guess the next bit. One looks at the last letter, one at the last word, one at the letter in the same place on the line above. Each says how sure it is. A judge combines the guesses into one guess, trusting the experts who have been right lately. The coder then spends few bits when the judge is sure and right.

When the bit arrives, the judge moves its trust toward the experts that would have helped and away from the ones that misled it. Each expert also updates what it knows. Because the decoder has the same experts and the same judge and sees the same bits, it makes the same guesses and can undo the coding.

## When it applies

Use context mixing when compression ratio matters much more than speed, and when the data has several kinds of structure that no single context captures: text with words and punctuation, executables with instructions and addresses, tables with rows and columns, images with neighbors in two directions. It needs a binary decomposition of the data (bits, or the bins of a binarization) so that each prediction is one number. CM compressors run at roughly the speed of the sum of their models, often well under a megabyte per second for the strongest ones, and the decoder is as slow as the encoder.

## The template

The holes are the set of models, the choice of the weight set, the refinement stage and the learning rate $\eta$. The functions are $\mathrm{st}(p) = \ln(p/(1-p))$, the *stretch*, and $\mathrm{sq}(x) = 1/(1 + e^{-x})$, the *squash*, its inverse.

```pseudo id=main
CONTEXT-MIXING(bits x_1 … x_n)
L1  set every model to its start state, and the weights w_i to a small value
L2  for t ← 1 to n do
L3      for each model i do p_i ← PREDICT_i(its context)           ▷ hole: the models
L4      s_i ← st(p_i) for each i
L5      p ← sq(Σ_i w_i s_i)                                         ▷ hole: the weight set, chosen by a small context
L6      p ← REFINE(p, a small context), clipped away from 0 and 1   ▷ hole: SSE or APM stages
L7      code x_t with the probability p of a 1
L8      err ← x_t − p
L9      w_i ← w_i + η · err · s_i for each i                        ▷ hole: the learning rate η
L10     UPDATE_i(x_t) for each model i
```

**Why logistic mixing.** The cost of coding bit $y$ with probability $p$ is $-\ln P(y)$, the [logistic loss](/logistic-loss/) of the prediction. With $p = \mathrm{sq}(\sum_i w_i s_i)$, its gradient with respect to $w_i$ is $-(y - p)\, s_i$, so line L9 is a step of [online gradient descent](/online-gradient-descent/) on the coding cost. The loss is convex in the weights, so the standard bounds of [online convex optimization](/online-convex-optimization/) apply: with a suitable step size, the total cost exceeds that of the best fixed weight vector, chosen after the fact, by $O(\sqrt n)$ for bounded inputs. A fixed weight vector with a 1 at model $i$ and 0 elsewhere reproduces model $i$, so the mixture is never much worse than the best single model. In practice a constant $\eta$ is used, which lets the weights follow the data when the best model changes.

**Mixing in the stretched domain.** A prediction near 0 or 1 has a large stretch, so a confident model gets a strong say, and two models that both say 0.9 give more than 0.9 when their weights add up to more than 1. A linear average of probabilities cannot do this.

**Weight sets.** The mixer may keep several weight vectors and pick one per bit by a small context, for example the order-0 context or the type of data, at L5. Larger CM compressors use two layers: several mixers with different selector contexts, and a final mixer that combines their outputs.

**SSE and APM.** Secondary symbol estimation refines the output probability. It maps the pair (stretched $p$, a small context) to a new probability by interpolating between the two nearest cells of a table, and trains those cells toward the bit. Later PAQ versions call this an adaptive probability map (APM) and chain two or more, often averaged with the input.

## Classic examples

**PAQ.** PAQ1 (Mahoney, 2002) combined the bit counts of several models with fixed weights. PAQ6 adapted the weights to the coding cost, as described in the technical report CS-2005-16. PAQ7 and the paq8 series, from 2005 and 2006, introduced the logistic mixer of the template and many specialized models, for example for words, for sparse contexts, for records of fixed length, for images and for executables.

**lpaq, zpaq and cmix.** lpaq is a small, faster PAQ with a few models. zpaq describes its models and mixers in a configuration stored in the archive, so a decoder can run any CM design. cmix by Byron Knoll mixes a very large number of models, including neural networks, and is among the strongest compressors on the Large Text Compression Benchmark.

**The Hutter Prize.** Marcus Hutter set up a prize in 2006 for compressing an excerpt of English Wikipedia (100 MB, then 1 GB from 2020) under limits on time and memory, and its winning entries have been context-mixing compressors.

**Mixing a lag model with order-$k$ models.** The implementation mixes five bit models: order 0, order 1, order 3, a model whose context is the bit 8 places back, and order 8. The data has 18000 bits in segments: a copy of the bit 8 places back with 5% noise, an order-1 chain that mostly alternates, and a coin with $P(1) = 0.04$, each segment repeated. Alone, the five models need 13485, 9579, 9928, 9241 and 7251 bits. Mixed with $\eta = 0.005$, they need 6245 bits, because the mixer moves its weight to the model that fits each segment. Without the order-8 model the mixture still needs only 6278 bits, while the best of the four models alone needs 9241.

## Variations

- **Linear mixing.** A weighted average of probabilities, with weights set from the recent coding cost of each model. It was used before logistic mixing and in the PAQ versions up to PAQ6.
- **Bayesian mixing.** [Context tree weighting](/context-tree-weighting/) mixes all tree models with fixed prior weights and Bayesian updates, and it has a proven bound. Logistic mixing has no such bound against tree sources, but it learns which models to trust.
- **Indirect models.** A context maps to a bit history, a small state that summarizes the bits seen in it, and a second table maps the bit history to a probability. This shares statistics between contexts with similar histories.
- **One model, no mixer.** The binary models of LZMA and [CABAC](/cabac/) give each bin one adaptive context, the case of a single model. Neural compressors such as those based on LSTM or transformer models replace the hand-made models with one large learned predictor and keep the arithmetic coder.

## Pitfalls

- **Probabilities at 0 or 1.** The stretch is infinite there, and a confident wrong prediction costs a huge number of bits. Clip all probabilities, for example to $[1/4096, 4095/4096]$.
- **The learning rate.** Too large a rate makes the weights jump on every bit; too small a rate makes the mixer slow to follow a change. A common choice is a rate that is larger at the start and decays to a floor.
- **Encoder and decoder drift.** Every update must be exactly the same on both sides. Real CM compressors use integer arithmetic with fixed scaling for the stretch, the squash and the weights, because floating point may differ between machines.
- **Speed.** Each model costs a memory lookup per bit, and the lookups miss the cache. Hash tables with small checksums, which keep the statistics of several bits of a byte in one cache line, are needed for speed.

## Exercises

1. Show that $\mathrm{sq}(\mathrm{st}(p)) = p$ and that $\frac{d}{dx}\mathrm{sq}(x) = \mathrm{sq}(x)(1 - \mathrm{sq}(x))$. Use this to derive the update of line L9 from the cost $-\ln P(y)$.
2. Two models both predict $p = 0.9$ and the weights are $w_1 = w_2 = 1$. What does the mixer predict? *Answer:* $\mathrm{sq}(2 \ln 9) = 81/82 \approx 0.988$.
3. With one model and $w = 1$, the mixer outputs the model's prediction. Which weight vector reproduces the prediction of model $i$ among several models, and why does this give a bound in terms of the best single model?

## References
