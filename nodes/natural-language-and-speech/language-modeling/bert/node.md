---
tag: RFZZFD
kind: model
slug: bert
name: BERT
aliases:
- bidirectional encoder representations from transformers
area: natural-language-and-speech/language-modeling
level: advanced
summary: A transformer encoder pretrained by masked language modeling and next sentence prediction, then fine-tuned with a small head per task.
history:
  year: 2018
  people: [Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova]
  note: "Devlin and colleagues at Google pretrained a transformer encoder on BooksCorpus and English Wikipedia and set new best results on eleven tasks. The paper appeared at NAACL 2019."
prereqs: [transformer, masked-language-modeling, wordpiece]
see_also: [generative-pretrained-transformer, replaced-token-detection, elmo, contextual-word-embedding, sentence-bert, colbert, bertscore, knowledge-distillation]
sources:
  - url: https://arxiv.org/abs/1810.04805
    title: "Jacob Devlin, Ming-Wei Chang, Kenton Lee and Kristina Toutanova, BERT: Pre-training of deep bidirectional transformers for language understanding, NAACL 2019"
    locator: "Section 3 (the input with segment and position embeddings, the sizes BASE and LARGE), Section 3.1 (the masked LM with the 80/10/10 rule and next sentence prediction), Section 3.2 (fine-tuning), Section 4 (GLUE, SQuAD and SWAG), Section 5.1 and Table 5 (the ablation of the pretraining tasks), Appendix A.2 (the pretraining procedure), Appendix C.2 and Table 8 (the masking ablation)"
  - url: https://arxiv.org/abs/1706.03762
    title: "Ashish Vaswani, Noam Shazeer, Niki Parmar and others, Attention is all you need, NeurIPS 2017"
    locator: "Section 3 (the encoder stack)"
  - url: https://arxiv.org/abs/1907.11692
    title: "Yinhan Liu, Myle Ott, Naman Goyal and others, RoBERTa: A robustly optimized BERT pretraining approach, 2019"
    locator: "Section 4.2 (training without next sentence prediction)"
  - url: https://arxiv.org/abs/2003.10555
    title: "Kevin Clark, Minh-Thang Luong, Quoc V. Le and Christopher D. Manning, ELECTRA: Pre-training text encoders as discriminators rather than generators, ICLR 2020"
    locator: "Section 3.2 and Table 5 (the comparison with BERT at the same size)"
---

BERT is a stack of [transformer](/transformer/) encoder blocks in which every token attends to every other token, pretrained with two objectives and then fine-tuned with a small output layer for each task. Three names here are easy to mix up. [Masked language modeling](/masked-language-modeling/) is an objective: hide some tokens and predict them from both sides. BERT is a particular network, released by Google in 2018, that was pretrained with that objective plus next sentence prediction. [Replaced token detection](/replaced-token-detection/) is a different objective for the same kind of encoder: a discriminator learns which tokens a small generator replaced. So BERT is the model, and the other two are ways to train an encoder like it.

## The machine

**Sizes.** $n$ is the number of tokens, at most 512. $|V|$ is the vocabulary, a [WordPiece](/wordpiece/) vocabulary of 30,000 entries. $d$ is the width, $h$ the number of heads, $d_k = d / h$, and $L$ the number of blocks. The two released sizes are BERT-BASE with $L = 12$, $d = 768$, $h = 12$ (110M parameters) and BERT-LARGE with $L = 24$, $d = 1024$, $h = 16$ (340M parameters).

**Input.** The input is one or two segments packed as `[CLS] A [SEP] B [SEP]`. Each token gets the sum of three [embeddings](/embedding/), each of size $d$:

- a token embedding from a $|V| \times d$ table;
- a segment embedding from a $2 \times d$ table, which says whether the token is in A or in B;
- a learned position embedding from a $512 \times d$ table.

The result is an $n \times d$ matrix $H_0$.

**One block.** As in the original transformer, the [layer normalization](/layer-normalization/) comes after each residual sum:

$$H' = \mathrm{LN}(H + \mathrm{MHA}(H)), \qquad H'' = \mathrm{LN}(H' + \mathrm{FFN}(H')).$$

[Multi-head attention](/multi-head-attention/) forms $Q$, $K$ and $V$ of shape $n \times d_k$ for each head, and the $n \times n$ score matrix has no causal mask: token $t$ sees tokens $1, \ldots, n$. Only padding is masked. The feed-forward layer maps $d \to 4d \to d$ with the GELU [activation function](/activation-function/).

**Output.** After $L$ blocks there is one vector $T_i \in \mathbb{R}^d$ for each token, and the vector $C \in \mathbb{R}^d$ at `[CLS]`.

**Pretraining objective 1: the masked LM.** Choose 15% of the token positions at random. For a chosen position, put `[MASK]` there 80% of the time, a random token 10% of the time, and leave the token as it is 10% of the time. So each position is `[MASK]` with probability 0.12, random with 0.015 and unchanged but scored with 0.015. An output layer of shape $d \times |V|$ and a softmax predict the original token at the chosen positions only, with the [cross-entropy loss](/cross-entropy-loss/). In a sequence of 512 tokens, about 77 positions are scored.

**Pretraining objective 2: next sentence prediction (NSP).** Half the time B is the sentence that follows A in the corpus, and half the time it is a random sentence. A layer of shape $d \times 2$ on $C$ predicts which case it is.

**Fine-tuning.** All weights are trained again on the task, with a new head:

- for a classification with $K$ labels, a $d \times K$ layer on $C$;
- for tagging each token (for example [named entity recognition](/named-entity-recognition/)), a layer on each $T_i$;
- for an answer span in a passage, a start vector $S$ and an end vector $E$ in $\mathbb{R}^d$, with $P(\text{start} = i) = \mathrm{softmax}_i(S \cdot T_i)$ and the same for the end.

**Counting parameters.** The blocks hold $12 L d^2$ weights plus $13 d$ biases and gains per block. With $|V| = 30{,}000$, 512 positions, 2 segments, the embedding normalization and the $d \times d$ layer on $C$, BERT-BASE has $109{,}081{,}344$ parameters, which the paper rounds to 110M.

## What it counts

One step is one floating-point multiply-add. One forward pass costs $\Theta(L (n d^2 + n^2 d))$: the $n^2 d$ term is the full attention matrix, which is why the input is limited to 512 tokens. Pretraining used batches of 256 sequences of 512 tokens for 1,000,000 steps, about 40 passes over 3.3 billion words: BooksCorpus (800M words) and English Wikipedia (2,500M words) (Appendix A.2).

Only about 15% of the positions give a loss in each sequence, against all positions in [causal language modeling](/causal-language-modeling/). Devlin et al. (Appendix C.1) report that the masked LM converges slightly more slowly than a left-to-right model, but that it is ahead in accuracy almost from the start. Replaced token detection was designed to give a loss at every position.

Fine-tuned BERT is measured by task scores: GLUE, SQuAD F1, accuracy on SWAG. Unlike a causal model, it gives no [perplexity](/perplexity/) of a sentence.

## Relation to other models

- **GPT.** A [generative pretrained transformer](/generative-pretrained-transformer/) uses the same kind of block with a causal mask and trains on the next token. It can generate text from left to right. BERT sees both sides of each token, which helps understanding tasks, but it has no direct way to generate.
- **ELMo.** [ELMo](/elmo/) trains a left-to-right and a right-to-left LSTM model separately and joins their states. Each direction never sees the other side. BERT's attention mixes both sides in every layer.
- **Contextual embeddings.** The vectors $T_i$ are [contextual word embeddings](/contextual-word-embedding/): the same word gets a different vector in each sentence. They can be used as features without fine-tuning.
- **Models built on BERT.** [Sentence-BERT](/sentence-bert/) trains BERT in a siamese setup so that $C$ or the mean of the $T_i$ can be compared with a cosine. [ColBERT](/colbert/) keeps all $T_i$ for retrieval. [BERTScore](/bertscore/) compares the $T_i$ of two texts. [SimCSE](/simcse/) trains sentence vectors from BERT by contrast. Smaller copies are made by [knowledge distillation](/knowledge-distillation/).
- **Other encoders.** RoBERTa keeps the architecture and changes the training: no NSP, more data, longer training. ELECTRA trains the same architecture with replaced token detection.

## Known results in the model

- **Measurement (eleven tasks).** At publication BERT-LARGE gave the best reported results on eleven tasks, including a GLUE score of 80.5 (7.7 points above the earlier best), MultiNLI accuracy of 86.7%, SQuAD v1.1 test F1 of 93.2 and SQuAD v2.0 test F1 of 83.1 (abstract, Section 4).
- **Measurement (both sides matter).** In Table 5, on BERT-BASE, a left-to-right model with no NSP scored 77.8 F1 on the SQuAD development set against 88.5 for BERT, and 77.5 against 86.7 on MRPC. Adding a BiLSTM on top raised SQuAD to 84.9 but did not close the gap.
- **Measurement (NSP).** In the same table, removing NSP lowered QNLI from 88.4 to 84.9 and SQuAD from 88.5 to 87.9. Liu et al. (RoBERTa, Section 4.2) later found that training without NSP, on full sentences from contiguous text, matched or slightly improved the scores. The two results used different input formats, so they do not contradict each other.
- **Measurement (the 80/10/10 rule).** In Table 8, fine-tuned MNLI accuracy hardly changed between the 80/10/10 rule (84.2) and always using `[MASK]` (84.3). For NER with BERT as a fixed feature extractor, always using `[MASK]` was worse, 94.0 against 94.9. The token `[MASK]` never appears in fine-tuning data, and the random and unchanged cases reduce that mismatch. This is the authors' reason; the gain is small.
- **Measurement (size).** In Table 6, larger models gave higher scores on all four GLUE tasks studied, even on MRPC with 3,600 training examples.
- **Fact (no sentence probability).** The masked LM gives the distribution of a hidden token given the others. In general these conditionals do not combine into a joint distribution of the sentence by the chain rule, so BERT is not a [language model](/language-model/) in the sense of assigning a probability to every sequence.
- **Heuristic (fine-tuning is unstable on small data).** Devlin et al. (Section 4.1) note that BERT-LARGE fine-tuning was sometimes unstable on small data sets, and they ran several random restarts and kept the best on the development set.

## References
