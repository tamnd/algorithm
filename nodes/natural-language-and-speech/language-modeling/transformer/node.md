---
tag: M3R9PT
kind: model
slug: transformer
name: Transformer
aliases:
- transformer architecture
- Vaswani transformer
area: natural-language-and-speech/language-modeling
level: core
summary: "A network of stacked blocks of self-attention and feedforward layers with residual connections and normalization, with no recurrence."
history:
  year: 2017
  people: [Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, Illia Polosukhin]
  note: Proposed for machine translation as an encoder-decoder built only from attention and feedforward layers. Encoder-only and decoder-only forms followed in 2018.
prereqs: [multi-head-attention, layer-normalization, sinusoidal-positional-encoding]
see_also: [bert, generative-pretrained-transformer, encoder-decoder-model, causal-language-modeling, masked-language-modeling, key-value-cache, recurrent-neural-network-language-model, selective-state-space-model]
sources:
  - paper: "Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser and Illia Polosukhin, Attention is all you need, Advances in Neural Information Processing Systems 30 (NIPS 2017)"
    title: Vaswani et al. 2017
    locator: "Section 3.1 (the stacks and LayerNorm(x + Sublayer(x))), Section 3.3 (the feedforward network, d_ff = 2048), Section 3.4 (shared embeddings, scaling by sqrt(d_model)), Section 4 and Table 1 (cost per layer), Sections 5.3 and 5.4 (Adam, warmup, dropout, label smoothing), Tables 2 and 3 (BLEU and model sizes)"
  - paper: "Ruibin Xiong, Yunchang Yang, Di He, Kai Zheng, Shuxin Zheng, Chen Xing, Huishuai Zhang, Yanyan Lan, Liwei Wang and Tie-Yan Liu, On layer normalization in the transformer architecture, Proceedings of ICML 2020, PMLR 119, pages 10524 to 10533"
    title: Xiong et al. 2020
    locator: the gradient analysis at initialization for the post-LN and pre-LN forms, and the training experiments without the warmup stage
  - paper: "Chulhee Yun, Srinadh Bhojanapalli, Ankit Singh Rawat, Sashank J. Reddi and Sanjiv Kumar, Are transformers universal approximators of sequence-to-sequence functions?, ICLR 2020, arXiv:1912.10077"
    title: Yun et al. 2020
    locator: Theorem 2 (permutation equivariant functions) and Theorem 3 (with positional encodings)
  - paper: "Jorge Pérez, Pablo Barceló and Javier Marinkovic, Attention is Turing-complete, Journal of Machine Learning Research 22(75):1-35, 2021"
    title: Pérez, Barceló and Marinkovic 2021
    locator: the main theorem (Turing completeness with hard attention and rational values of arbitrary precision)
  - paper: "Michael Hahn, Theoretical limitations of self-attention in neural sequence models, Transactions of the Association for Computational Linguistics 8:156-171, 2020"
    title: Hahn 2020
    locator: the results on parity and Dyck languages for hard and soft attention
  - book: isbn:9780262048644
    title: Simon J. D. Prince, Understanding Deep Learning, MIT Press 2023
    locator: Chapter 12 (Transformers)
  - book: isbn:9783031454677
    title: Christopher M. Bishop and Hugh Bishop, Deep Learning, Foundations and Concepts, Springer 2024
    locator: Chapter 12 (Transformers)
---

The transformer is a neural network that maps a sequence of $n$ token vectors to a sequence of $n$ output vectors. It is a stack of identical layers. Each layer has a [multi-head attention](/multi-head-attention/) sublayer, which lets every position read from every other position, and a feedforward sublayer, which acts on each position alone. Each sublayer is wrapped in a residual connection and [layer normalization](/layer-normalization/). There is no recurrence, so all positions of a layer are computed in parallel, and word order enters only through a positional encoding. Vaswani and colleagues built it as an [encoder-decoder model](/encoder-decoder-model/) for translation. Encoder-only stacks such as [BERT](/bert/) and decoder-only stacks such as [GPT](/generative-pretrained-transformer/) are now the base of most language models.

## The machine

**Input.** The tokens $x_1, \ldots, x_n$ come from a vocabulary of size $V$. An embedding matrix $E$ of shape $V \times d$ maps each token to a row, which is multiplied by $\sqrt{d}$, and a position vector is added: $X^{(0)}_i = \sqrt{d}\, E_{x_i} + \mathrm{PE}_i$. The original model uses the fixed [sinusoidal positional encoding](/sinusoidal-positional-encoding/); later models use learned position vectors, [rotary position embedding](/rotary-position-embedding/) or [ALiBi](/alibi-attention-bias/).

**Feedforward sublayer.** For one position $x$ of size $d$,

$$\mathrm{FFN}(x) = \max(0,\, x W_1 + b_1)\, W_2 + b_2,$$

with $W_1$ of shape $d \times d_{ff}$ and $W_2$ of shape $d_{ff} \times d$. The original uses [ReLU](/relu/) and $d_{ff} = 4d$.

**Encoder layer, post-LN.** The original places the normalization after the residual sum:

$$Z = \mathrm{LN}(X + \mathrm{MHA}(X, X)), \qquad X' = \mathrm{LN}(Z + \mathrm{FFN}(Z)).$$

**Encoder layer, pre-LN.** Most later models normalize the input of each sublayer and keep the residual path free:

$$Z = X + \mathrm{MHA}(\mathrm{LN}(X), \mathrm{LN}(X)), \qquad X' = Z + \mathrm{FFN}(\mathrm{LN}(Z)),$$

with one more LN after the last layer. In both forms [dropout](/dropout/) is applied to each sublayer output before the sum, and to the input sum of embeddings and positions.

**Decoder layer.** It has three sublayers: masked self-attention, where the causal mask stops position $i$ from seeing positions after $i$; cross-attention, $\mathrm{MHA}(Z, Y_{\text{enc}})$, with queries from the decoder and keys and values from the final encoder output; and the feedforward sublayer. Each has the same residual and LN wrapping.

**Output.** After $N$ layers, the output at position $i$ is mapped to a distribution over the vocabulary, $\operatorname{softmax}(X^{(N)}_i E^\top)$. The original shares $E$ between the two embeddings and this output map.

**Three forms.** The encoder-decoder form reads a source with the encoder and generates the target with the decoder. The encoder-only form has no causal mask and gives a vector for each input position, trained for example by [masked language modeling](/masked-language-modeling/). The decoder-only form has the causal mask and no cross-attention, and is trained by [causal language modeling](/causal-language-modeling/).

**Training.** The weights are trained by [backpropagation](/backpropagation/) on the [cross-entropy loss](/cross-entropy-loss/) of the next target token, with [teacher forcing](/teacher-forcing/). The original used [Adam](/adam/) with $\beta_1 = 0.9$, $\beta_2 = 0.98$, $\epsilon = 10^{-9}$, the learning rate $d^{-0.5} \min(s^{-0.5}, s \cdot w^{-1.5})$ at step $s$ with $w = 4000$ warmup steps, dropout 0.1 and [label smoothing](/label-smoothing/) 0.1.

The base model has $N = 6$ layers in each stack, $d = 512$, $d_{ff} = 2048$ and $h = 8$ heads of size 64.

## What it counts

Count multiply-adds and weights, ignoring biases and LN parameters, for one layer on $n$ positions with $d_k = d_v = d/h$ and $d_{ff} = 4d$.

- **Weights.** An encoder layer has $4d^2$ in attention and $2 d d_{ff} = 8 d^2$ in the feedforward sublayer, so $12 d^2$. A decoder layer has two attention sublayers, so $16 d^2$. The embedding has $V d$. For the base model with a shared vocabulary of about 37000 tokens this gives $6 \cdot 12 d^2 + 6 \cdot 16 d^2 + 37000\, d \approx 63$ million, close to the 65 million listed in Table 3 of the paper, where the biases and LN parameters are included.
- **Arithmetic.** Attention costs $4 n d^2$ for the projections and $2 n^2 d$ for the scores and the weighted sums; the feedforward sublayer costs $8 n d^2$. An encoder layer costs about $12 n d^2 + 2 n^2 d$. The $n^2$ term dominates when $n > 6 d$.
- **Memory.** The activations of a layer are $\Theta(n d)$ numbers, plus $\Theta(h n^2)$ if the attention weights are stored; [FlashAttention](/flashattention/) avoids the second term.
- **Generation.** A decoder that has seen $t$ tokens computes the next one in $\Theta(d^2 + t d)$ per layer with a [key-value cache](/key-value-cache/) of $2 t d$ numbers per layer.
- **Depth.** Each layer is one parallel step: $O(1)$ sequential operations, and a path of length $O(1)$ between any two positions, against $O(n)$ for a recurrent layer.

## Relation to other models

- **[Recurrent language models](/recurrent-neural-network-language-model/)** carry a state of size $d$ from step to step, at $O(n d^2)$ per layer with $n$ sequential steps. The transformer replaces the recurrence by attention, which costs $O(n^2 d)$ but runs in one step; at generation time it keeps all past keys and values instead of a fixed-size state.
- **[Encoder-decoder models](/encoder-decoder-model/)** with [additive attention](/additive-attention/) are the direct ancestor: the transformer keeps the cross-attention and adds self-attention in place of the recurrent encoder and decoder.
- **[BERT](/bert/)** is an encoder-only transformer; **[GPT](/generative-pretrained-transformer/)** is a decoder-only one.
- **[Selective state space models](/selective-state-space-model/)** such as Mamba replace attention by a recurrence with input-dependent parameters, which is linear in $n$ and has a fixed-size state at generation time.
- **[Conformer](/conformer/)** adds convolution modules to the transformer layer for speech; [wav2vec 2.0](/wav2vec-2/) uses a transformer over speech features.

## Known results in the model

- **Permutation equivariance (theorem).** Without positional information and without a mask, the whole encoder is permutation equivariant: permuting the input rows permutes the output rows. This follows from the same property of [multi-head attention](/multi-head-attention/) and the fact that the feedforward and LN sublayers act on each row alone. It is why a positional encoding is needed.
- **Universal approximation (theorem).** Yun and colleagues (2020) proved that transformers can approximate any continuous permutation equivariant sequence-to-sequence function with compact support to any accuracy, and, with positional encodings, any continuous sequence-to-sequence function on a compact domain. The constructions use many layers and are not what training finds.
- **Turing completeness (theorem).** Pérez, Barceló and Marinkovic (2021) proved that the encoder-decoder transformer with hard attention and rational values of arbitrary precision can simulate a Turing machine, by letting the decoder write out the steps of the computation. The construction needs the unbounded precision.
- **Limits of self-attention (theorem).** Hahn (2020) proved that transformers with hard attention cannot recognize parity or balanced bracket languages for all lengths, and that with soft attention the effect of one input symbol on the output shrinks as the input grows, so the confidence on such tasks must fall toward chance.
- **Where to normalize (theorem and measurement).** Xiong and colleagues (2020) showed that at initialization the post-LN form has large expected gradients for the parameters near the output, which explains why it needs the warmup stage; the pre-LN form has well-behaved gradients and trained without warmup in their experiments.
- **Translation results (measurement).** The big model reached 28.4 BLEU on WMT 2014 English to German and 41.8 BLEU on English to French, after 3.5 days of training on 8 P100 GPUs. Learned position vectors gave nearly the same results as the sinusoidal encoding (Table 3, row E).
- **Scaling (measurement).** Loss falls as a power law in model size, data and compute over many orders of magnitude; see [neural scaling laws](/neural-scaling-law/).

## References
