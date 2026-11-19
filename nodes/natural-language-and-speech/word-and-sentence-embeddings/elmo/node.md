---
tag: 8BDA5F
kind: model
slug: elmo
name: "ELMo"
aliases:
- embeddings from language models
area: natural-language-and-speech/word-and-sentence-embeddings
level: advanced
summary: Contextual word vectors taken as a learned weighted sum of the layers of a deep bidirectional LSTM language model trained on a large corpus.
history:
  year: 2018
  people: [Matthew E. Peters, Mark Neumann, Mohit Iyyer, Matt Gardner, Christopher Clark, Kenton Lee, Luke Zettlemoyer]
  note: The Allen Institute for AI and the University of Washington trained a bidirectional language model on the 1B Word Benchmark and used a weighted sum of its layers as the input of task models, with gains on six tasks.
prereqs: [contextual-word-embedding, recurrent-neural-network-language-model]
see_also: [bert, transformer, generative-pretrained-transformer, glove, subword-information-embeddings, bilstm-crf, perplexity, layer-normalization]
sources:
  - paper: doi:10.18653/v1/N18-1202
    title: Matthew E. Peters, Mark Neumann, Mohit Iyyer, Matt Gardner, Christopher Clark, Kenton Lee and Luke Zettlemoyer, Deep contextualized word representations, NAACL-HLT 2018, pages 2227 to 2237
    locator: Section 3 (the biLM, the weighted sum of layers, the use in task models and the pretrained architecture), Section 4 (the six tasks), Section 5 (the analysis of the layers)
  - paper: doi:10.18653/v1/D19-1006
    title: Kawin Ethayarajh, How contextual are contextualized word representations? Comparing the geometry of BERT, ELMo and GPT-2 embeddings, EMNLP-IJCNLP 2019, pages 55 to 65
    locator: the anisotropy and the self-similarity of the ELMo layers
  - paper: doi:10.18653/v1/N19-1423
    title: Jacob Devlin, Ming-Wei Chang, Kenton Lee and Kristina Toutanova, BERT, Pre-training of deep bidirectional transformers for language understanding, NAACL-HLT 2019, pages 4171 to 4186
    locator: the comparison of the feature-based and the fine-tuning use of pretrained models
---

ELMo (embeddings from language models) gives each token of a sentence a [contextual vector](/contextual-word-embedding/). A forward and a backward LSTM language model, each with two layers, run over token vectors that a character convolutional network builds from the spelling of each word. The vector of token $k$ for a task is $\gamma \sum_j s_j h_{k,j}$, a weighted sum of the $2L + 1 = 5$ layer outputs, with softmax-normalized weights $s_j$ and a scale $\gamma$ learned on the task while the language model stays frozen. Peters et al. 2018 measured that adding these vectors to existing task models reduced the relative error by 6% to 20% on six tasks.

## The machine

**Token layer.** A token is read as a sequence of characters. Each character gets a learned vector, and a convolutional layer with 2048 filters over character n-grams, max-pooled over the word, gives a vector of size 2048. Two highway layers and a linear projection reduce it to $x_k \in \mathbb{R}^{512}$. Every string has a vector, so there is no out-of-vocabulary token at the input.

**LSTM layer.** There is no LSTM page, so here are its equations. With input $z_t \in \mathbb{R}^{512}$, the previous output $r_{t-1} \in \mathbb{R}^{512}$, and a cell of size $n = 4096$:

$$i_t = \sigma(W_i z_t + U_i r_{t-1} + b_i), \quad f_t = \sigma(W_f z_t + U_f r_{t-1} + b_f), \quad o_t = \sigma(W_o z_t + U_o r_{t-1} + b_o),$$

$$g_t = \tanh(W_g z_t + U_g r_{t-1} + b_g), \quad c_t = f_t \odot c_{t-1} + i_t \odot g_t, \quad r_t = P (o_t \odot \tanh c_t),$$

with $W_\cdot, U_\cdot$ of shape $4096 \times 512$ and the projection $P$ of shape $512 \times 4096$. Here $\sigma$ is the logistic function and $\odot$ the product of entries.

**Bidirectional language model.** The forward stack runs two LSTM layers left to right on $x_1, \ldots, x_N$ and gives $\overrightarrow{h}_{k,j}$ for layer $j = 1, 2$. A residual connection adds the input of the second layer to its output. A separate backward stack runs right to left and gives $\overleftarrow{h}_{k,j}$. The top forward output predicts $t_{k+1}$ and the top backward output predicts $t_{k-1}$, through a softmax over the vocabulary that the two directions share. The model is trained to maximize

$$\sum_{k=1}^{N} \Big( \log p(t_k \mid t_1, \ldots, t_{k-1}; \Theta_x, \overrightarrow{\Theta}, \Theta_s) + \log p(t_k \mid t_{k+1}, \ldots, t_N; \Theta_x, \overleftarrow{\Theta}, \Theta_s) \Big),$$

with the token layer $\Theta_x$ and the softmax $\Theta_s$ tied between the directions and separate LSTM weights for each direction. The pretraining corpus is the 1B Word Benchmark.

**The task vector.** For token $k$, the model gives $L + 1 = 3$ vectors: $h_{k,0}$ from the token layer, and $h_{k,j} = [\overrightarrow{h}_{k,j}; \overleftarrow{h}_{k,j}] \in \mathbb{R}^{1024}$ for $j = 1, 2$. In the released code the token vector is copied into both halves, so that $h_{k,0}$ also has size 1024. A task learns $L + 1$ numbers $w_j$ and a scale $\gamma$ and uses

$$\mathrm{ELMo}_k = \gamma \sum_{j=0}^{L} s_j h_{k,j}, \qquad s = \operatorname{softmax}(w).$$

The language model weights are frozen. The task model concatenates $\mathrm{ELMo}_k$ with its own token vector at its input, and for some tasks, such as SNLI and SQuAD, also with the output of its own recurrent layer. [Dropout](/dropout/) on the ELMo vectors and, in some cases, a penalty $\lambda \|w\|^2$ that pulls the weights toward a plain mean help. The authors found that [layer normalization](/layer-normalization/) of each layer before the sum helps in some cases.

## What it counts

The language model assigns the probability $p(t_1, \ldots, t_N)$ in two ways, left to right and right to left; the network computes, for each position, the $L + 1$ vectors $h_{k,j}$ and then the task vector.

- **Weights.** One LSTM layer of one direction has $4 \cdot 4096 \cdot (512 + 512) \approx 16.8$ million weights in the gates and $4096 \cdot 512 \approx 2.1$ million in the projection, about 18.9 million. Two layers in two directions give about 76 million. This count follows from the sizes above, without the biases, the character network and the softmax.
- **Arithmetic.** The LSTMs cost about 76 million multiply-adds per token. The softmax over the vocabulary is used only in pretraining.
- **Sequential steps.** Each direction needs $N$ steps in a row for $N$ tokens, so a sentence cannot be processed in parallel over its positions, unlike a [transformer](/transformer/) layer.
- **Task parameters.** The task vector adds only $L + 2 = 4$ parameters per use, plus the task model.

## Relation to other models

- **Static embeddings.** [Skip-gram](/skip-gram-model/) and [GloVe](/glove/) give one vector per word type. ELMo with $s_0 = 1$ and the other weights 0 uses only the token layer, which does not depend on the context.
- **Recurrent language models.** The forward stack is a [recurrent neural network language model](/recurrent-neural-network-language-model/) with LSTM cells and character input. ELMo adds the backward model and uses all the layers, not only the top one.
- **Character input.** Like [subword information embeddings](/subword-information-embeddings/), the character network gives vectors for words not seen in training.
- **CoVe.** McCann et al. 2017 took contextual vectors from the LSTM encoder of a translation model. ELMo uses a language model, which needs no parallel data, and all its layers.
- **BERT and GPT.** [BERT](/bert/) replaces the two separate LSTMs by one [transformer](/transformer/) encoder trained by [masked language modeling](/masked-language-modeling/), so each layer sees both sides at once, and it is fine-tuned on each task instead of frozen. [GPT](/generative-pretrained-transformer/) uses a left-to-right transformer.
- **Task models.** Many of the task models in the paper were [BiLSTM-CRF](/bilstm-crf/) taggers and similar recurrent models, with ELMo added at the input.

## Known results in the model

- **The task vector is a scaled convex combination (theorem).** The softmax weights $s_j$ are positive and sum to 1, so $\mathrm{ELMo}_k / \gamma$ lies in the convex hull of $h_{k,0}, \ldots, h_{k,L}$. Choosing $w$ with one large entry gives one layer; equal $w_j$ give the mean of the layers.
- **Perplexity (measurement).** The average of the forward and backward perplexities on the 1B Word Benchmark is 39.7, against 30.0 for the forward CNN-BIG-LSTM model of Jozefowicz et al. 2016.- **Six tasks (measurement).** Adding ELMo to the baseline task models improved SQuAD, SNLI, semantic role labeling, coreference, named entity recognition and SST-5, with relative error reductions of 6% to 20%.
- **All layers help (measurement).** A learned weighted sum of all layers did better than the top layer alone, and the top layer alone did better than no ELMo.
- **What the layers hold (measurement).** For word sense disambiguation by the nearest sense vector, the top layer gave an F1 of 69.0 and the first layer 67.4. For part of speech tagging with a linear classifier, the first layer gave 97.3% and the second 96.8%. The first layer holds more syntax and the second more meaning.
- **Geometry (measurement).** Ethayarajh 2019 found that ELMo vectors are anisotropic in every layer and that the vectors of one word are less similar to each other in the upper layer, so the upper layer depends more on the context.
- **Feature-based use (measurement).** Devlin et al. 2019 found that the feature-based use of BERT layers, as ELMo is used, came close to fine-tuning on named entity recognition, which shows that the gap between the two uses is small on some tasks.

## References
