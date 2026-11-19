---
tag: YVG3M2
kind: model
slug: generative-pretrained-transformer
name: Generative pretrained transformer
aliases:
- GPT
- decoder-only transformer
area: natural-language-and-speech/language-modeling
level: advanced
summary: A transformer decoder pretrained by causal language modeling on a large corpus, then fine-tuned or prompted for downstream tasks.
history:
  year: 2018
  people: [Alec Radford, Karthik Narasimhan, Tim Salimans, Ilya Sutskever]
  note: "Radford and colleagues at OpenAI pretrained a 12-layer transformer with causal self-attention on BooksCorpus and fine-tuned it for each task. GPT-2 (2019) and GPT-3 (2020) kept the design and grew it to 1.5B and 175B parameters."
prereqs: [transformer, causal-language-modeling, multi-head-attention]
see_also: [bert, language-model, in-context-learning, neural-scaling-law, key-value-cache, byte-level-bpe, instruction-tuning, reinforcement-learning-from-human-feedback]
sources:
  - paper: "Alec Radford, Karthik Narasimhan, Tim Salimans and Ilya Sutskever, Improving language understanding by generative pre-training, OpenAI technical report, 2018"
    title: GPT-1
    locator: "Section 3.1 (equation 2, the model with tied token embeddings), Section 3.2 (fine-tuning with the auxiliary language modeling loss), Section 4.1 (12 layers, width 768, 12 heads, 512 tokens, 40,000 BPE merges, GELU, learned positions), the abstract (9 of 12 tasks)"
  - paper: "Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei and Ilya Sutskever, Language models are unsupervised multitask learners, OpenAI technical report, 2019"
    title: GPT-2
    locator: "Section 2.1 (WebText), Section 2.3 and Table 2 (layer normalization at the input of each sub-block, a final layer normalization, residual weights scaled by 1 over the square root of N, a vocabulary of 50,257, 1024 tokens), the abstract (7 of 8 language modeling data sets zero-shot)"
  - url: https://arxiv.org/abs/2005.14165
    title: "Tom B. Brown, Benjamin Mann, Nick Ryder and others, Language models are few-shot learners, NeurIPS 2020"
    locator: "Section 2.1 and Table 2.1 (8 sizes up to 175B, 96 layers, width 12288, 96 heads of size 128, 2048 tokens, alternating dense and locally banded sparse attention), Table 3.3 (TriviaQA), Table D.1 (training compute)"
  - url: https://arxiv.org/abs/1706.03762
    title: "Ashish Vaswani, Noam Shazeer, Niki Parmar and others, Attention is all you need, NeurIPS 2017"
    locator: "Section 3 (the decoder stack with masked self-attention)"
  - url: https://arxiv.org/abs/2001.08361
    title: "Jared Kaplan, Sam McCandlish, Tom Henighan and others, Scaling laws for neural language models, 2020"
    locator: "Section 2.1 and Table 1 (the parameter count 12 n_layer d squared and the forward cost 2N plus 2 n_layer n_ctx d per token)"
---

A generative pretrained transformer (GPT) is a stack of [transformer](/transformer/) blocks with causal self-attention and no encoder, trained to predict the next token of text and then fine-tuned or prompted for a task. Three words in this area are easy to mix up. A [language model](/language-model/) is any probability distribution over sequences of tokens, from an n-gram table to a network. [Causal language modeling](/causal-language-modeling/) is the training objective: maximize $\sum_t \log p(y_t \mid y_{<t})$. GPT is one family of networks, from OpenAI, that is trained with that objective: GPT-1 (2018), GPT-2 (2019) and GPT-3 (2020). Other networks can be causal language models, for example a [recurrent network](/recurrent-neural-network-language-model/), and the same transformer stack can be trained with other objectives.

## The machine

**Sizes.** $n$ is the number of tokens in the input, at most the context length $n_{\text{ctx}}$. $|V|$ is the size of the vocabulary, $d$ the width, $h$ the number of heads, $d_k = d / h$ the size of one head, and $L$ the number of blocks. The feed-forward layer has width $4d$.

**Input.** A token embedding $W_e$ of shape $|V| \times d$ and a learned position embedding $W_p$ of shape $n_{\text{ctx}} \times d$. The tokens $u_1, \ldots, u_n$ become

$$H_0 = U W_e + W_p[1{:}n], \qquad H_0 \in \mathbb{R}^{n \times d},$$

where $U$ is the $n \times |V|$ matrix of one-hot rows. GPT-1 used byte-pair encoding with 40,000 merges; GPT-2 and GPT-3 used a [byte-level BPE](/byte-level-bpe/) with $|V| = 50{,}257$.

**One block.** GPT-2 and GPT-3 put the [layer normalization](/layer-normalization/) at the input of each sub-block (GPT-1 put it after, as in the original transformer):

$$H' = H + \mathrm{MHA}(\mathrm{LN}(H)), \qquad H'' = H' + \mathrm{FFN}(\mathrm{LN}(H')).$$

- In [multi-head attention](/multi-head-attention/), each head $i$ forms $Q_i = X W^Q_i$, $K_i = X W^K_i$ and $V_i = X W^V_i$, each $n \times d_k$. The scores $Q_i K_i^\top / \sqrt{d_k}$ form an $n \times n$ matrix. The causal mask sets every entry above the diagonal to $-\infty$ before the row softmax, so position $t$ sees only positions $1, \ldots, t$. This is [scaled dot-product attention](/scaled-dot-product-attention/) with a mask. The $h$ outputs of size $n \times d_k$ are joined into $n \times d$ and multiplied by $W^O$, which is $d \times d$.
- The feed-forward layer maps each row $d \to 4d \to d$ with the GELU [activation function](/activation-function/) in between.

**Output.** After $L$ blocks (and, in GPT-2 and GPT-3, a final layer normalization), the logits are

$$Z = H_L W_e^\top \in \mathbb{R}^{n \times |V|},$$

with the same matrix $W_e$ as the input (GPT-1, equation 2). Row $t$ of $\mathrm{softmax}(Z)$ is the predicted distribution of token $t + 1$. Training minimizes the [cross-entropy](/cross-entropy-loss/) of all $n$ next tokens at once, which is [teacher forcing](/teacher-forcing/).

**Counting parameters.** Each block has $4d^2$ weights in attention and $8d^2$ in the feed-forward layer, so the blocks hold $12 L d^2$ weights (Kaplan et al., Table 1), plus $13d$ biases and gains per block. The embeddings add $|V| d + n_{\text{ctx}} d$.

- GPT-2 small, with $L = 12$, $d = 768$, $|V| = 50{,}257$ and $n_{\text{ctx}} = 1024$: $12 L d^2 = 84{,}934{,}656$, and with the biases, the gains and the embeddings the total is $124{,}439{,}808$.
- GPT-3, with $L = 96$, $d = 12288$, $h = 96$ and $d_k = 128$: $12 L d^2 = 173{,}946{,}175{,}488$, the token embedding is $617{,}558{,}016$ and the position embedding with $n_{\text{ctx}} = 2048$ is $25{,}165{,}824$.

**Use after pretraining.** GPT-1 adds a linear layer $W_y$ on the last hidden state and fine-tunes the whole network, with the language modeling loss kept as an auxiliary term with weight $\lambda = 0.5$ (Sections 3.2 and 4.1). GPT-2 and GPT-3 are mostly used without changing the weights: the task is written into the prompt, which is [in-context learning](/in-context-learning/). Generation draws one token at a time by [autoregressive decoding](/autoregressive-decoding/).

## What it counts

One step is one floating-point multiply-add. The forward pass on $n$ tokens costs $\Theta(n d^2)$ per block for the projections and the feed-forward layer and $\Theta(n^2 d)$ per block for the attention scores, so $\Theta(L (n d^2 + n^2 d))$ in total. Kaplan et al. (Section 2.1) count a forward pass as about $2N + 2 L n_{\text{ctx}} d$ floating-point operations per token, with $N$ the number of non-embedding parameters, and training as about three times that, $6N$ per token. For GPT-3 the two terms are $3.5 \times 10^{11}$ and $4.8 \times 10^{9}$, so the weights dominate. With 300B training tokens, $6ND = 3.15 \times 10^{23}$, close to the $3.14 \times 10^{23}$ of Table D.1 of Brown et al.

During generation a [key-value cache](/key-value-cache/) stores the keys and values of earlier positions, $2 L n d$ numbers. Each new token then costs $\Theta(L (d^2 + n d))$ instead of a full forward pass.

The quantity that people report for the pretrained model is the cross-entropy per token on held-out text, or its exponential, the [perplexity](/perplexity/).

## Relation to other models

- **The transformer.** The original transformer has an encoder and a decoder with cross-attention. GPT keeps a decoder stack without the cross-attention, so every block has only masked self-attention and a feed-forward layer. An [encoder-decoder model](/encoder-decoder-model/) reads a source with full attention and writes a target with causal attention; GPT treats source and target as one sequence.
- **BERT.** [BERT](/bert/) uses the same blocks with no mask, so every position sees the whole input, and it trains by [masked language modeling](/masked-language-modeling/). It gives good features for classification but no direct way to generate text from left to right.
- **ELMo.** [ELMo](/elmo/) trains two LSTM language models, one in each direction, and feeds their states to a task model as features. GPT-1 instead fine-tunes the whole pretrained network.
- **Earlier neural language models.** The [neural probabilistic language model](/neural-probabilistic-language-model/) uses a fixed window of words, and the [recurrent network language model](/recurrent-neural-network-language-model/) a hidden state. GPT conditions on the whole context window through attention.
- **Instruction-following models.** [Instruction tuning](/instruction-tuning/) and [RLHF](/reinforcement-learning-from-human-feedback/) start from a pretrained GPT model and change its weights so that it answers requests.

## Known results in the model

- **Theorem (a proper distribution).** Hypotheses: each row of $\mathrm{softmax}(Z)$ is a probability distribution over $V$, and position $t$ depends only on tokens $1, \ldots, t$. Then $\prod_t p(y_{t+1} \mid y_{\le t})$ sums to 1 over all continuations of a fixed length, by the chain rule. The causal mask gives the second hypothesis: changing token $t + 1$ cannot change the output at positions $1, \ldots, t$.
- **Theorem (the cache gives the same result).** Under the same mask, appending tokens does not change the keys and values of earlier positions. So a forward pass with a key-value cache returns the same logits as a full forward pass, up to rounding.
- **Measurement (GPT-1).** Fine-tuning with the auxiliary loss improved on the best earlier result on 9 of the 12 data sets studied, with absolute gains of 8.9% on the Stories Cloze Test, 5.7% on RACE and 5.5% on GLUE (abstract and Section 1).
- **Measurement (GPT-2).** Without any fine-tuning, the 1.5B model gave the best result reported at the time on 7 of 8 language modeling data sets (abstract). It was trained on WebText, about 8 million documents and 40 GB of text from links shared on Reddit (Section 2.1).
- **Measurement (GPT-3).** On TriviaQA the 175B model scored 64.3% with no examples in the prompt, 68.0% with one and 71.2% with a few (Table 3.3). The weights were the same in all three settings; only the prompt changed.
- **Measurement (scaling).** Across many sizes, the held-out loss of such models falls close to a power law in the number of parameters, the data and the compute. These are fitted laws with no guarantee; the [neural scaling law](/neural-scaling-law/) page gives the fits of Kaplan et al. (2020) and Hoffmann et al. (2022), which differ.
- **Heuristic (sharing the embedding).** Using $W_e$ for both input and output saves $|V| d$ parameters, 38.6M for GPT-2 small. It is a design choice of GPT-1, not a requirement.

## References
