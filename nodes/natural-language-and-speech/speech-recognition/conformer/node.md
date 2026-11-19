---
tag: YFAJCY
kind: model
slug: conformer
name: Conformer
aliases:
- convolution-augmented transformer
area: natural-language-and-speech/speech-recognition
level: research
summary: A speech encoder block that sandwiches self-attention and a convolution module between two half-step feedforward layers.
history:
  year: 2020
  people: [Anmol Gulati, James Qin, Chung-Cheng Chiu, Niki Parmar, Yu Zhang, Jiahui Yu, Wei Han, Shibo Wang, Zhengdong Zhang, Yonghui Wu, Ruoming Pang]
  note: Gulati and colleagues at Google combined self-attention, which models global context, with depthwise convolution, which models local patterns, in one encoder block, and reported state-of-the-art word error rates on LibriSpeech.
prereqs: [transformer, convolution, batch-normalization]
see_also: [rnn-transducer, listen-attend-and-spell, wav2vec-2, specaugment, joint-ctc-attention, layer-normalization, multi-head-attention, dropout]
sources:
  - paper: doi:10.21437/Interspeech.2020-3015
    title: "Anmol Gulati, James Qin, Chung-Cheng Chiu, Niki Parmar, Yu Zhang, Jiahui Yu, Wei Han, Shibo Wang, Zhengdong Zhang, Yonghui Wu and Ruoming Pang, Conformer: convolution-augmented transformer for speech recognition, Interspeech 2020, pages 5036 to 5040"
    locator: "Section 2 (the Conformer block, the convolution module, the feedforward module and the block equations), Section 3 (the model sizes and the LibriSpeech results) and the ablation studies"
---

The Conformer is an encoder for speech recognition. Its block puts a multi-head self-attention module and a convolution module between two feedforward modules, each feedforward module with half weight on its residual path. Self-attention lets every frame look at every other frame, which captures long-range context; the depthwise convolution captures local patterns such as formant movements over a few frames. A stack of Conformer blocks on top of a convolutional front end replaces the LSTM or [Transformer](/transformer/) encoder in end-to-end recognizers such as the [RNN transducer](/rnn-transducer/), CTC and attention models. In the original paper it was more accurate on LibriSpeech than the Transformer and convolutional encoders it was compared with.

## The machine

**Front end.** The input is a sequence of 80 log mel filter bank features every 10 ms. A convolutional subsampling stage reduces the frame rate to one vector every 40 ms, a linear layer maps it to width $d$, and dropout follows. Then come $N$ Conformer blocks.

**The block** (Gulati et al. 2020, Section 2). For an input sequence $x$ of vectors of width $d$:

$$\tilde x = x + \tfrac{1}{2}\,\mathrm{FFN}(x), \qquad x' = \tilde x + \mathrm{MHSA}(\tilde x), \qquad x'' = x' + \mathrm{Conv}(x'), \qquad y = \mathrm{LayerNorm}\big(x'' + \tfrac{1}{2}\,\mathrm{FFN}(x'')\big).$$

The two half-step feedforward modules around the middle follow the Macaron-Net design. Each module starts with its own [layer normalization](/layer-normalization/) (pre-norm residual units) and ends with dropout.

**Feedforward module.** LayerNorm, a linear layer that expands the width 4 times, the Swish activation $z \cdot \sigma(z)$, dropout, a linear layer back to width $d$, and dropout.

**Self-attention module.** LayerNorm, [multi-head self-attention](/multi-head-attention/) with the relative positional encoding of Transformer-XL, and dropout. The relative encoding depends only on the distance between two positions, which helps the module generalize to inputs of different lengths.

**Convolution module.** LayerNorm, a pointwise convolution that doubles the width, a gated linear unit (GLU) that halves it again, a 1-D depthwise convolution with kernel size 32, [batch normalization](/batch-normalization/), Swish, a second pointwise convolution, and dropout. The depthwise convolution filters each channel separately along time, so it costs $k d$ per frame instead of $k d^2$.

**Sizes.** The paper uses three encoders with a one-layer LSTM decoder in a transducer:

| model | parameters | blocks | width $d$ | heads | decoder width |
|---|---|---|---|---|---|
| Conformer (S) | 10.3 M | 16 | 144 | 4 | 320 |
| Conformer (M) | 30.7 M | 16 | 256 | 4 | 640 |
| Conformer (L) | 118.8 M | 17 | 512 | 8 | 640 |

**Example.** Ten seconds of audio are 1000 frames at 10 ms, and 250 vectors after the front end. In Conformer (S), each self-attention module compares all $250^2 = 62\,500$ pairs of positions in each of 4 heads, while each depthwise convolution sees 32 positions, 1.28 s of audio. The feedforward modules work on each of the 250 positions separately.

## What it counts

The encoder maps $T$ input frames to $T/4$ vectors of width $d$ that the decoder of the recognizer reads; the loss and the decoding rule come from the recognizer ([transducer](/rnn-transducer/), [CTC](/connectionist-temporal-classification/) or attention). For $n = T/4$ positions, one block costs about $\Theta(n d^2)$ for the feedforward modules, the attention projections and the pointwise convolutions, $\Theta(n^2 d)$ for the attention scores and weighted sums, and $\Theta(n k d)$ for the depthwise convolution. The $n^2$ term dominates for long utterances, which is why the front end reduces the frame rate. Memory for training is $\Theta(N (n d + h n^2))$ with $h$ heads, for the activations and the attention matrices.

## Relation to other models

- **[Transformer](/transformer/) encoder.** The Conformer block is a Transformer block with a convolution module added after the attention, the feedforward layer split into two halves around them, Swish activations and relative positions. Without the convolution module it is close to a Transformer with a Macaron feedforward pair.
- **Convolutional encoders.** Models built only from convolutions see a limited window unless they add global context by other means. The Conformer gets global context from attention and local detail from the convolution, in every block.
- **[RNN transducer](/rnn-transducer/) and [listen, attend and spell](/listen-attend-and-spell/).** These are recognizers that need an encoder; the Conformer is a drop-in encoder for them, and for [joint CTC-attention](/joint-ctc-attention/).
- **[wav2vec 2.0](/wav2vec-2/).** Its context network is a Transformer encoder over speech features, the place a Conformer stack can also take.
- **[SpecAugment](/specaugment/).** A data augmentation that is used together with Conformer encoders in training; it changes the input, not the model.

## Known results in the model

- **LibriSpeech.** With a transducer and no language model, Gulati et al. (2020) measured word error rates of 2.1% on test-clean and 4.3% on test-other for Conformer (L), 2.3% and 5.0% for Conformer (M) and 2.7% and 6.3% for Conformer (S). With an external language model, Conformer (L) reached 1.9% and 3.9% (measurements).
- **The convolution module matters.** In the ablation studies of the paper, removing the convolution module from the large model raised the word error rate on test-other from 4.3% to 4.9% (measurements).
- **Cost of attention.** The self-attention module costs $\Theta(n^2 d)$ per block for $n$ positions (a property of full self-attention), so long-form audio needs chunking or limited attention spans.

## References
