---
tag: KHQJRV
kind: technique
slug: masked-language-modeling
name: Masked language modeling
aliases:
- cloze objective
- MLM
area: natural-language-and-speech/language-modeling
level: core
summary: "Train a bidirectional encoder to recover tokens that were masked or replaced at random positions from the rest of the sentence."
prereqs: [language-model, transformer]
see_also: [bert, causal-language-modeling, replaced-token-detection, wordpiece, cross-entropy-loss, gibbs-sampling, sentence-embedding, word-embedding]
sources:
  - paper: doi:10.18653/v1/N19-1423
    title: "Jacob Devlin, Ming-Wei Chang, Kenton Lee and Kristina Toutanova, BERT: pre-training of deep bidirectional transformers for language understanding, NAACL-HLT 2019"
    locator: "Section 3.1 (Task 1, the masked LM: 15% of the WordPiece tokens, 80% [MASK], 10% random token, 10% unchanged), Appendix C.2 (the ablation over masking strategies)"
  - paper: "Wilson L. Taylor, Cloze procedure: a new tool for measuring readability, Journalism Quarterly 30, 1953"
    title: Taylor 1953
    locator: the cloze procedure, where readers fill in deleted words of a text
  - paper: "Julian Besag, Statistical analysis of non-lattice data, Journal of the Royal Statistical Society Series D (The Statistician) 24(3), 1975"
    title: Besag 1975
    locator: the pseudo-likelihood, the product of the conditional distributions of each variable given all the others
  - paper: "Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar Joshi, Danqi Chen, Omer Levy, Mike Lewis, Luke Zettlemoyer and Veselin Stoyanov, RoBERTa: a robustly optimized BERT pretraining approach, arXiv:1907.11692, 2019"
    title: Liu et al. 2019
    locator: the comparison of static and dynamic masking, and the removal of next sentence prediction
  - paper: "Mandar Joshi, Danqi Chen, Yinhan Liu, Daniel S. Weld, Luke Zettlemoyer and Omer Levy, SpanBERT: improving pre-training by representing and predicting spans, Transactions of the Association for Computational Linguistics 8, 2020"
    title: Joshi et al. 2020
    locator: the masking of contiguous random spans in place of single tokens
---

Masked language modeling trains a network to fill in blanks. Some positions of a text, chosen at random, are hidden or corrupted, and the network must predict the original tokens there from all the other tokens, on both sides. The loss is the [cross-entropy](/cross-entropy-loss/) at the chosen positions only. Because no position has to be predicted from the left alone, the network can be a [transformer](/transformer/) encoder with full attention, and each output vector then carries context from the whole sentence. Devlin and colleagues made it the main pre-training task of [BERT](/bert/): 15% of the tokens are chosen, and of these 80% are replaced by a [MASK] token, 10% by a random token and 10% are left unchanged. The idea goes back to the cloze tests of Taylor, where readers fill in deleted words.

## In plain words

Take a sentence, cover a few of its words, and ask a student to guess the covered words from the rest. The student can use the words before and after each gap. That is the whole task.

The model sees a great deal of text with random gaps and learns by guessing. To guess well it must learn what words mean and how they fit together, and that knowledge can then be reused for other tasks, such as deciding if a review is positive.

The covered words are not always marked as covered. Sometimes a wrong word is put in, and sometimes the right word is left as it is. So the model cannot relax at the words that look normal.

## When it applies

- Pre-training an encoder whose output vectors will be used for classification, tagging, question answering or retrieval, where every word may use context from both sides.
- Plenty of unlabeled text and no need to generate text left to right.
- Not the right choice when the model must generate text: a masked model gives no direct next-token distribution. Use [causal language modeling](/causal-language-modeling/) for that.

## The template

Given a token sequence $x_1, \ldots, x_n$, a vocabulary $V$, a selection rate $\rho$ (0.15 in BERT) and an encoder with output distribution $P_\theta(\cdot \mid \tilde x, i)$ at position $i$:

1. **Choose.** Pick a random set $S$ of positions, each with probability $\rho$ or a fixed fraction of $n$, skipping special tokens.
2. **Corrupt.** For each $i \in S$, independently: with probability 0.8 set $\tilde x_i = $ [MASK], with probability 0.1 set $\tilde x_i$ to a token drawn uniformly from $V$, and with probability 0.1 keep $\tilde x_i = x_i$. For $i \notin S$, $\tilde x_i = x_i$.
3. **Encode.** Run the encoder on $\tilde x$ with full (not causal) attention.
4. **Loss.** At the chosen positions only,
$$\mathcal{L}(\theta) = -\frac{1}{|S|} \sum_{i \in S} \log P_\theta(x_i \mid \tilde x, i).$$
5. **Repeat** with a new $S$ for each pass over the data (dynamic masking), or with a few fixed choices made once (static masking, as in the original BERT data).

The output layer is a softmax over the vocabulary on top of the final vector at position $i$, often with weights tied to the input embedding.

**Why corrupt in three ways.** The [MASK] token never occurs when the encoder is later fine-tuned. If every chosen token were [MASK], the model could learn that only [MASK] positions need a good prediction. With 10% random and 10% unchanged, any visible token might be a target, so the model must keep a good representation of every token. Over all positions the rates are $0.15 \cdot 0.8 = 12\%$ [MASK], $1.5\%$ random and $1.5\%$ unchanged targets.

**The minimizer (theorem).** For fixed $\tilde x$ and $i$, the expected loss $-\sum_w p(w \mid \tilde x, i) \log q(w)$ is minimized over distributions $q$ at $q = p(\cdot \mid \tilde x, i)$, the true distribution of the original token given the corrupted text, since the gap to the minimum is the Kullback-Leibler divergence $D(p \,\|\, q) \ge 0$. With a single [MASK] at $i$ and no other corruption, this is the full conditional $p(x_i \mid x_{-i})$.

**Relation to pseudo-likelihood.** Masking one position at a time and summing over all positions gives $\sum_i \log P_\theta(x_i \mid x_{-i})$, the log pseudo-likelihood of Besag. It is built from full conditionals and is not the log-probability of the text under a joint model; a set of full conditionals need not even agree with any joint distribution.

## Classic examples

**Counts in a BERT sequence.** In a sequence of 512 tokens, the expected number of targets is $0.15 \cdot 512 = 76.8$: about 61.4 [MASK] tokens, 7.7 random tokens and 7.7 unchanged targets. Only these 76.8 positions give a loss; the other 435.2 do not.

**A single blank.** In "the cat sat on the [MASK]", a trained model may give "mat" a high probability, and also "floor" or "sofa". If it gives the true token "mat" the probability 0.4, the loss at that position is $-\ln 0.4 = 0.916291$ nats.

**BERT.** [BERT](/bert/) pre-trained an encoder with this objective and next sentence prediction on [WordPiece](/wordpiece/) tokens, then fine-tuned it with a small head per task.

**RoBERTa.** Liu and colleagues kept the objective, chose new masks each time a sequence was used (dynamic masking), dropped next sentence prediction, and trained longer on more data.

**Cloze tests.** Taylor used deleted words to measure how readable a text is: the more blanks readers can fill, the easier the text.

## Variations

- **Whole-word masking.** When a word is split into several subword tokens, choose all of its pieces together, so the model cannot guess a piece from the other pieces of the same word.
- **Span masking.** SpanBERT masks contiguous spans of random length, which makes the task harder and helps span-based tasks such as question answering.
- **Replaced token detection.** ELECTRA trains a small masked model to fill the blanks and a second network to tell, at every position, whether the token was replaced; see [replaced token detection](/replaced-token-detection/). Every position then gives a training signal.
- **Span corruption in encoder-decoder models.** Replace spans by sentinel tokens in the input and have a decoder generate the missing spans.
- **Sampling text.** Repeatedly masking one position and drawing a new token from the model is a form of [Gibbs sampling](/gibbs-sampling/), though the learned conditionals need not agree with any joint distribution.

## Pitfalls

- **Loss on all positions.** The loss is taken on the chosen positions only. Including the unchanged context positions makes the task trivial copying for most tokens.
- **Masking special tokens.** Separators, padding and the class token must not be chosen.
- **Independent predictions.** Two masked positions are predicted independently given $\tilde x$. For "New [MASK] [MASK]" the model may predict "York" and "Zealand" at the same time, each likely alone but not together.
- **Few training signals.** Only about 15% of the positions give a loss, so each sequence teaches less than in causal language modeling. This was a motivation for replaced token detection.
- **Using it as a generator.** A masked model does not give $P(x_1, \ldots, x_n)$, and left-to-right generation with it is awkward. Its pseudo-perplexity is not comparable to the perplexity of a causal model.
- **Mismatch at fine-tuning.** The [MASK] token appears in pre-training but never in later use; the 80/10/10 rule reduces, but does not remove, this gap.

## Exercises

1. In a sequence of 128 tokens with the BERT rule, compute the expected numbers of [MASK], random and unchanged targets, and the probability that a given visible token is a target.
2. Show that the expected loss at a masked position is minimized by the true conditional of the original token given the corrupted input.
3. Give two full conditional distributions for two binary variables that cannot come from any joint distribution.
4. Explain why the random-token and unchanged cases force the model to keep information about every visible token, and what could go wrong if all targets were [MASK].
5. Compare the number of positions with a loss per sequence of $n$ tokens for masked language modeling with rate 0.15, causal language modeling, and replaced token detection.

## References
