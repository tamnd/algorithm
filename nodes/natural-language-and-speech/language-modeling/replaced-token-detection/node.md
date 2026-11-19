---
tag: BXCKAR
kind: technique
slug: replaced-token-detection
name: Replaced token detection
aliases:
- ELECTRA
area: natural-language-and-speech/language-modeling
level: research
summary: Pretrain an encoder to tell, at every position, whether a small generator network replaced the token, which learns from all positions.
history:
  year: 2020
  people: [Kevin Clark, Minh-Thang Luong, Quoc V. Le, Christopher D. Manning]
  note: "Clark and colleagues at Stanford and Google proposed the objective at ICLR 2020, and trained it with a small masked-language-model generator that is thrown away after pretraining."
prereqs: [masked-language-modeling, bert, logistic-loss]
see_also: [noise-contrastive-estimation, negative-sampling, generative-pretrained-transformer, transformer, reinforce, gumbel-max-trick, knowledge-distillation, natural-language-inference]
sources:
  - url: https://arxiv.org/abs/2003.10555
    title: "Kevin Clark, Minh-Thang Luong, Quoc V. Le and Christopher D. Manning, ELECTRA: Pre-training text encoders as discriminators rather than generators, ICLR 2020"
    locator: "Section 2 (the generator, the discriminator, the two losses and the combined objective), Section 3.2 (weight sharing, generator size, two-stage and adversarial training), Section 3.3 and Table 1 (small models), Table 2 (large models), Section 3.5 and Table 5 (the efficiency analysis), Appendix A (lambda = 50, no next sentence prediction, 25% masking for the large model)"
  - url: https://arxiv.org/abs/1810.04805
    title: "Jacob Devlin, Ming-Wei Chang, Kenton Lee and Kristina Toutanova, BERT: Pre-training of deep bidirectional transformers for language understanding, NAACL 2019"
    locator: "Section 3.1 (the masked language model that the generator uses)"
---

Replaced token detection is a pretraining objective for a text encoder. A small generator fills some masked positions of a sentence with plausible tokens, and the encoder that we keep, the discriminator, must say at every position whether the token is the original or a replacement. It is easy to confuse with two neighbors. [Masked language modeling](/masked-language-modeling/) asks the encoder to predict the original token, and only at the masked positions. [BERT](/bert/) is a network that was pretrained with masked language modeling and next sentence prediction. Replaced token detection keeps the encoder of BERT but changes what it is asked: a yes-or-no question at all $n$ positions instead of a $|V|$-way question at about 15% of them. Clark et al. (2020) proposed the objective; the model they trained with it has its own name, which this page does not use for the objective.

## In plain words

Take a sentence and hide a few of its words. A small helper network guesses each hidden word, and its guesses are put back into the sentence. Some guesses are right and some are wrong but plausible.

The main network then reads the whole sentence and, for every word, answers one question: is this the word that was there, or did the helper change it?

Every word gives the main network something to learn from, not only the hidden ones, so it learns more from each sentence. After training, the helper is thrown away. The main network is then trained a little more on the task you care about, as with other pretrained encoders.

## When it applies

- You want an encoder for understanding tasks (classification, tagging, finding answer spans), not a model that writes text.
- Compute for pretraining is the limit. The objective was designed to get more learning signal out of each sequence.
- You can train two transformers together: a generator with a masked-language-model head and a discriminator with a one-number head per position.

## The template

**Sizes.** A sequence has $n$ tokens over a vocabulary of size $|V|$. The discriminator is a [transformer](/transformer/) encoder of width $d$ with $h$ heads, $d_k = d / h$. The generator is a smaller encoder of the same kind; Clark et al. found the best generators to be $1/4$ to $1/2$ the size of the discriminator.

1. **Mask.** Choose $k = \lceil 0.15 n \rceil$ positions $m_1, \ldots, m_k$ uniformly and put `[MASK]` there. Call the result $x^{\text{masked}}$.
2. **Generate.** The generator maps $x^{\text{masked}}$ to hidden states $h_G$ and, at each masked position $t$, gives $p_G(x_t \mid x^{\text{masked}}) = \exp(e(x_t)^\top h_G(x)_t) / \sum_{x'} \exp(e(x')^\top h_G(x)_t)$, a softmax over $|V|$ with the token embeddings $e$. Draw $\hat x_t$ from it, and put it in place of the mask. Call the result $x^{\text{corrupt}}$.
3. **Label.** Position $t$ is "real" if $x^{\text{corrupt}}_t = x_t$ and "replaced" otherwise. A sample that happens to equal the original counts as real; Clark et al. report that this moderately improved results.
4. **Discriminate.** The discriminator maps $x^{\text{corrupt}}$ to an $n \times d$ matrix $h_D$ and gives $D(x^{\text{corrupt}}, t) = \sigma(w^\top h_D(x^{\text{corrupt}})_t)$ at every position, with one weight vector $w$ of size $d$.
5. **Losses.** The generator gets the masked-language-model loss $L_{\text{MLM}} = \sum_{i} -\log p_G(x_{m_i} \mid x^{\text{masked}})$ on the $k$ masked positions. The discriminator gets the binary [logistic loss](/logistic-loss/) at all $n$ positions,

$$L_{\text{Disc}} = \sum_{t=1}^{n} -\mathbf{1}[\text{real}] \log D(x^{\text{corrupt}}, t) - \mathbf{1}[\text{replaced}] \log\big(1 - D(x^{\text{corrupt}}, t)\big).$$

Train both by minimizing $L_{\text{MLM}} + \lambda L_{\text{Disc}}$ over the corpus, with $\lambda = 50$ (Appendix A). No gradient flows from $L_{\text{Disc}}$ into the generator, because sampling $\hat x$ has no derivative.

6. **Keep the discriminator.** After pretraining, drop the generator and fine-tune the discriminator on the task.

**Example.** Take the five tokens "the chef cooked the meal" and mask positions 2 and 5. The generator gives "chef" probability 0.4 and "meal" probability 0.1, and it samples "chef" and "soup". So $x^{\text{corrupt}}$ is "the chef cooked the soup", and the labels are real, real, real, real, replaced: position 2 is real because the sample equals the original. If the discriminator says "real" with probabilities $(0.9, 0.6, 0.8, 0.7, 0.3)$, the position losses are $(0.10536, 0.51083, 0.22314, 0.35667, 0.35667)$, so $L_{\text{Disc}} = 1.55268$. $L_{\text{MLM}} = -\log 0.4 - \log 0.1 = 3.21888$, and the combined loss is $3.21888 + 50 \cdot 1.55268 = 80.8529$. Five positions gave a discriminator loss; only two gave a generator loss.

## Classic examples

All results here are GLUE development scores from Clark et al. (2020), measured with their own BERT baselines trained with the same settings and data.

- **Small models (Table 1).** A discriminator with 14M parameters, trained for 4 days on one V100 GPU, scored 79.9, against 75.1 for a BERT model of the same size and compute and 78.8 for GPT. GPT used $4.0 \times 10^{19}$ training operations against $1.4 \times 10^{18}$, about 29 times more. The same model after 6 hours of training scored 74.1.
- **Base size (Table 1).** At the size and compute of BERT-BASE, 85.1 against 82.2.
- **Large size (Table 2).** The large model scored about the same as RoBERTa and XLNet with less than 1/4 of their pretraining compute.
- **Where the gain comes from (Section 3.5, Table 5).** With the base size, the full objective scored 85.0. A masked model that predicts every token from an input with generator replacements scored 84.3. A masked model with generator replacements instead of `[MASK]`, scored only at the masked positions, scored 82.4. The discriminator scored only at the 15% masked positions also gave 82.4, and BERT 82.2. The authors conclude that most of the gain comes from a loss at all positions and a smaller part from removing the `[MASK]` token, which never appears in fine-tuning.

## Variations

- **Sharing weights.** With a generator as large as the discriminator, scores were 83.6 with no sharing, 84.3 with shared token embeddings and 84.4 with all weights shared (Section 3.2). With a smaller generator, only the token and position embeddings are shared.
- **Size of the generator.** Generators $1/4$ to $1/2$ the size of the discriminator worked best. They also tried a "unigram" generator that samples tokens by their frequency in the corpus (Figure 3, left).
- **Two-stage training.** Train the generator alone, copy its weights into the discriminator, then train the discriminator with the generator frozen. This needs equal sizes and did not beat joint training. Without the copy, the discriminator sometimes learned nothing beyond the majority class.
- **Adversarial generator.** Training the generator to fool the discriminator, with [REINFORCE](/reinforce/)-style reinforcement learning to get past the sampling step, did worse than maximum likelihood. That generator reached 58% masked-token accuracy against 65% and put most of its mass on one token, so its samples had little variety (Section 3.2). Another way past the sampling step is a relaxation of the [Gumbel-max trick](/gumbel-max-trick/).
- **More masking.** The large model masked 25% of the tokens instead of 15%, because its generator was right so often that few tokens were replaced (Appendix A).
- **Relation to noise contrast.** Telling data from samples of a noise distribution is the idea of [noise-contrastive estimation](/noise-contrastive-estimation/) and of [negative sampling](/negative-sampling/). Here the "noise" is a learned generator that depends on the context.

## Pitfalls

- **This is not a GAN.** The generator is trained by maximum likelihood to predict the original token, not to fool the discriminator. It also gets no noise vector as input.
- **Few replaced tokens.** The replaced share of positions is $0.15 (1 - a)$, where $a$ is the generator's accuracy at the masked positions. With $a = 0.65$ only 5.25% of the positions are replaced, and a discriminator that always says "real" with probability 0.9475 already reaches a loss of 0.20581 per position. Watch the loss on replaced positions, not only the mean.
- **A generator that is too strong.** Larger generators made scores worse. The authors' guess is that the discriminator then spends its capacity modeling the generator instead of the data.
- **Counting a correct sample as replaced.** If a sample equals the original, the label must be "real". Labeling it "replaced" asks the discriminator to detect something that is not in its input.
- **Gradients through the sample.** In code, stop the gradient at $\hat x$. The generator learns only from $L_{\text{MLM}}$.
- **No generation afterwards.** The kept network has a yes-or-no head per token. It cannot fill in masks or write text, so use a [generative pretrained transformer](/generative-pretrained-transformer/) or a masked model for that.

## Exercises

1. Show that the expected share of replaced positions is $0.15 (1 - a)$ when each masked position is sampled correctly with probability $a$. Compute it for $a = 0.65$ with 15% masking and with 25% masking.
2. For a share $q$ of replaced positions, show that the best constant discriminator outputs "real" with probability $1 - q$ and has the loss $-q \log q - (1 - q) \log (1 - q)$ per position. Check the value $0.20581$ for $q = 0.0525$.
3. Fix the generator. Show that the discriminator that minimizes the expected loss at position $t$ is the probability that the token at $t$ is the original, given the corrupted sequence. Why does a perfect generator make this probability equal to 1 at every masked position?
4. Recompute the example with the discriminator outputs $(0.95, 0.5, 0.9, 0.8, 0.1)$ and $\lambda = 50$. Which position gives the largest discriminator loss, and why?
5. A sequence of 128 tokens is scored at how many positions by the masked LM and by the discriminator? Explain why this ratio is not the speedup that Table 1 shows.

## References
