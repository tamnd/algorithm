---
tag: 50ES3M
kind: model
slug: x-vector
name: x-vector
aliases:
- x-vector speaker embedding
- TDNN speaker embedding
area: natural-language-and-speech/speech-recognition
level: research
summary: A speaker embedding from a time-delay neural network with statistics pooling, trained to classify speakers.
history:
  year: 2018
  people: [David Snyder, Daniel Garcia-Romero, Gregory Sell, Daniel Povey, Sanjeev Khudanpur]
  note: Snyder et al. trained a time-delay network with a statistics pooling layer to classify the speakers of short chunks of speech, used a hidden layer after the pooling as the embedding, and showed that data augmentation made it better than i-vectors on their test sets.
prereqs: [i-vector, plda-scoring, embedding]
see_also: [speaker-verification, speaker-diarization, data-augmentation, i-vector, plda-scoring, equal-error-rate, cosine-similarity, linear-discriminant-analysis]
sources:
  - paper: doi:10.1109/ICASSP.2018.8461375
    title: David Snyder, Daniel Garcia-Romero, Gregory Sell, Daniel Povey and Sanjeev Khudanpur, X-vectors, robust DNN embeddings for speaker recognition, ICASSP 2018, pages 5329 to 5333
    locator: "Table 1 (the layers of the network), the section on data augmentation, and Table 2 (the equal error rates on SITW and SRE16)"
  - paper: doi:10.1109/TASL.2010.2064307
    title: Najim Dehak, Patrick J. Kenny, Réda Dehak, Pierre Dumouchel and Pierre Ouellet, Front-end factor analysis for speaker verification, IEEE Transactions on Audio, Speech, and Language Processing 19(4), 2011, pages 788 to 798
    locator: the i-vector system that x-vectors are compared with
---

An x-vector is a fixed-length vector that describes the speaker of an utterance. A neural network reads the frames of the utterance through a few time-delay layers, pools their outputs into one vector of means and standard deviations, and then classifies the speaker. After training, the classifier is thrown away, and the output of the first layer after the pooling is the x-vector. The embedding is scored with [PLDA](/plda-scoring/), as [i-vectors](/i-vector/) are.

## The machine

The network of Snyder et al. 2018 (their Table 1) takes 24-dimensional filterbank features. Write $h^{(k)}_t$ for the output of layer $k$ at frame $t$. The frame layers splice the outputs of the layer below at a few offsets and apply an affine map and a ReLU:

| layer | input frames | input × output |
|---|---|---|
| frame1 | $t-2, \ldots, t+2$ | $120 \times 512$ |
| frame2 | $t-2, t, t+2$ | $1536 \times 512$ |
| frame3 | $t-3, t, t+3$ | $1536 \times 512$ |
| frame4 | $t$ | $512 \times 512$ |
| frame5 | $t$ | $512 \times 1500$ |
| statistics pooling | all $T$ frames | $1500 T \times 3000$ |
| segment6 | the pooled vector | $3000 \times 512$ |
| segment7 | segment6 | $512 \times 512$ |
| softmax | segment7 | $512 \times N$ |

The frame layers see a window of 15 frames around $t$: frame1 sees $t \pm 2$, frame2 widens it to $t \pm 4$, and frame3 to $t \pm 7$. The statistics pooling layer computes, over the $T$ frames of the utterance,

$$\mu = \frac{1}{T} \sum_t h^{(5)}_t, \qquad \sigma = \Big(\frac{1}{T} \sum_t (h^{(5)}_t - \mu)^2\Big)^{1/2}$$

for each of the 1500 coordinates, and passes the 3000 numbers $(\mu, \sigma)$ to segment6. The softmax has one output per training speaker, and the network is trained with cross-entropy on chunks of a few seconds of speech.

The x-vector is the affine output of segment6, taken before the nonlinearity: 512 numbers. The back end reduces it with [LDA](/linear-discriminant-analysis/) (to 150 dimensions in the paper), applies length normalization, and scores pairs with PLDA.

## What it counts

- **One vector per utterance.** The pooling turns any number of frames into 3000 numbers, so utterances of any length give a 512-dimensional vector.
- **Order does not matter after the window.** The mean and the standard deviation do not change when frames are reordered. The network sees the order of frames only inside the 15-frame window of the frame layers.
- **A pooling example.** Take two coordinates and three frames with outputs $(1, 2)$, $(3, 2)$ and $(2, 5)$. Then $\mu = (2, 3)$ and $\sigma = (\sqrt{2/3}, \sqrt{2}) = (0.816497, 1.414214)$, so the pooled vector is $(2, 3, 0.816497, 1.414214)$. Any order of the three frames gives the same vector.
- **Size.** The layers up to segment6 have $61952 + 786944 + 786944 + 262656 + 769500 + 1536512 = 4204508$ weights and biases, the 4.2 million parameters that the paper counts without segment7 and the softmax.
- **Cost.** Each frame costs about $120 \cdot 512 + 2 \cdot 1536 \cdot 512 + 512 \cdot 512 + 512 \cdot 1500 = 2664448$ multiply-adds in the frame layers, so extraction is linear in $T$. Segment6 runs once per utterance. A trial then costs $O(d^2)$ for PLDA with the dimension $d$ after LDA.

## Relation to other models

- **[i-vectors](/i-vector/).** Both map an utterance to one vector and use the same back end. The i-vector comes from a generative model trained without speaker labels. The x-vector comes from a network trained to tell speakers apart, which needs many labeled speakers.
- **Time-delay networks.** The frame layers are a time-delay neural network: a one-dimensional convolution over time, with gaps between the spliced frames.
- **[PLDA](/plda-scoring/).** PLDA treats the x-vector as speaker plus session, both Gaussian. Length normalization makes this closer to true.
- **[Data augmentation](/data-augmentation/).** The training data were augmented with noise, music, babble (MUSAN) and simulated reverberation. The paper reports that augmentation helps the network more than it helps the i-vector system.
- **Later embeddings.** Wider networks (ResNets, ECAPA-TDNN), attentive pooling and angular margin losses keep the same plan: frame layers, pooling, a segment layer as the embedding.

## Known results in the model

These are measurements from Table 2 of Snyder et al. 2018, as equal error rates in percent. "Original" is the system without augmentation, "augmented" adds augmentation to the PLDA and the extractor training data, and "+ VoxCeleb" also adds VoxCeleb to the training data.

| system | test set | original | augmented | + VoxCeleb |
|---|---|---|---|---|
| x-vector | SITW Core | 9.40 | 6.00 | 4.16 |
| i-vector | SITW Core | 9.29 | 8.04 | 7.45 |
| x-vector | SRE16 Cantonese | 8.00 | 5.86 | 5.71 |
| i-vector | SRE16 Cantonese | 9.23 | 8.95 | 9.23 |

Without augmentation the two systems are close; with it, the x-vector is clearly better on these sets. The numbers hold for these data sets, this back end and this training data, and they cannot be compared with error rates on other lists. Nothing is proved about the embedding beyond what the training objective gives: a network that classifies its training speakers well need not separate new speakers well, and the gain on new speakers is a measurement.

## References
