---
tag: 3K0KTZ
kind: technique
slug: specaugment
name: "SpecAugment"
aliases:
- spectrogram augmentation
area: natural-language-and-speech/speech-recognition
level: advanced
summary: Augment speech training data by masking random blocks of frequency channels and time steps of the spectrogram, and by time warping.
prereqs: [data-augmentation, mel-filter-bank, dropout]
see_also: [listen-attend-and-spell, conformer, wav2vec-2, rnn-transducer, short-time-fourier-transform, shallow-fusion, vocal-tract-length-normalization, word-error-rate]
sources:
  - paper: doi:10.21437/Interspeech.2019-2680
    title: "Daniel S. Park, William Chan, Yu Zhang, Chung-Cheng Chiu, Barret Zoph, Ekin D. Cubuk and Quoc V. Le, SpecAugment: a simple data augmentation method for automatic speech recognition, Interspeech 2019, pages 2613 to 2617"
    locator: "Section 2 (time warping, frequency masking and time masking), the policies LB, LD, SM and SS, the LibriSpeech 960h and Switchboard 300h results, and the discussion of time warping and of over-fitting"
---

SpecAugment is a data augmentation method for speech recognition that works on the log mel spectrogram, the input of the network, instead of on the audio. For each training example and each epoch, it draws a few random bands of frequency channels and a few random blocks of time steps and sets them to zero, and it may also warp the time axis a little. The transcript stays the same. The network must then recognize speech with parts of the input missing, which reduces over-fitting. The method is cheap, needs no extra data and runs on the fly inside the input pipeline. Park et al. (2019) used it to train [listen, attend and spell](/listen-attend-and-spell/) models that set new best results on LibriSpeech and Switchboard at the time.

## In plain words

A speech recognizer sees the sound as a picture: time from left to right, pitch from bottom to top, and brightness for loudness. SpecAugment takes this picture and paints over a few horizontal stripes (some pitch bands are gone) and a few vertical stripes (some short moments are gone). It may also stretch one part of the picture a little to the left or right.

The words have not changed, so the label stays the same. A recognizer that learns from these damaged pictures cannot rely on any single band or moment. It has to use all the clues, which makes it better on new recordings. The stripes are drawn again at random every time the example is used, so the network never sees the same picture twice.

## When it applies

- The model reads a time-frequency representation such as log mel filter banks, and is trained end to end or as a hybrid acoustic model.
- The model over-fits: the training loss is much lower than the held-out loss. With SpecAugment, Park et al. found that their models no longer over-fitted but under-fitted, and that larger networks and longer training then helped.
- The input features are normalized so that zero is the mean value; then a masked region holds the mean, not an extreme value.

## The template

The input is a log mel spectrogram with $\nu$ frequency channels and $\tau$ time steps. A policy fixes the parameters $(W, F, m_F, T, p, m_T)$.

1. **Time warping.** Pick a random point on the horizontal line through the center of the spectrogram, at a time step in $(W, \tau - W)$. Move it to the left or right by a distance $w$ drawn uniformly from $[0, W]$, and warp the image so that the rest moves smoothly with it (the paper uses a sparse image warp).
2. **Frequency masking**, $m_F$ times. Draw $f$ uniformly from $[0, F]$ and $f_0$ from $[0, \nu - f)$, and mask the channels $f_0, \ldots, f_0 + f - 1$.
3. **Time masking**, $m_T$ times. Draw $t$ uniformly from $[0, T]$ and $t_0$ from $[0, \tau - t)$, and mask the time steps $t_0, \ldots, t_0 + t - 1$. A mask may cover at most $p \tau$ time steps, so short utterances get short masks.
4. Set the masked values to zero, and train on the result with the original transcript. Draw new masks each time the example is used.

The four policies of the paper are

| policy | $W$ | $F$ | $m_F$ | $T$ | $p$ | $m_T$ |
|---|---|---|---|---|---|---|
| LB | 80 | 27 | 1 | 100 | 1.0 | 1 |
| LD | 80 | 27 | 2 | 100 | 1.0 | 2 |
| SM | 40 | 15 | 2 | 70 | 0.2 | 2 |
| SS | 40 | 27 | 2 | 70 | 0.2 | 2 |

LB and LD were used for LibriSpeech and SM and SS for Switchboard. All the steps cost $O(\nu \tau)$ per example, the size of the input.

## Classic examples

**Masks on one utterance.** Take 80 channels and 1000 time steps (10 s at 10 ms) and the policy LB. The frequency mask has a width $f$ uniform on $\{0, \ldots, 27\}$, so on average 13.5 channels, about 17% of the 80. The time mask has a length $t$ uniform on $\{0, \ldots, 100\}$, on average 50 steps, 5% of the time. With LD there are two masks of each kind, which may overlap. For a 2 s utterance under SM, the bound $p \tau = 0.2 \cdot 200 = 40$ steps limits each time mask, although $T = 70$.

**LibriSpeech 960h.** LAS models trained with SpecAugment reached word error rates of 2.8% on test-clean and 6.8% on test-other without a language model, and 2.5% and 5.8% with shallow fusion of a language model (Park et al. 2019, measurements).

**Switchboard 300h.** The same approach gave 7.2% on the Switchboard part and 14.6% on the CallHome part of Hub5'00 without a language model, and 6.8% and 14.1% with one (measurements).

**Which part helps.** In the ablation of the paper, the frequency and time masks gave most of the gain, and time warping, the most expensive step, gave the least. It can be left out when the budget is tight.

## Variations

- **Adaptive masks.** Scale the number or the size of the time masks with the length of the utterance, as $p$ does for the size.
- **Masking with the mean or with noise.** Fill the masks with the mean of the utterance or with random values instead of zero, which matters when the features are not normalized.
- **Masking in a latent space.** [wav2vec 2.0](/wav2vec-2/) masks spans of its latent features; there the masked spans are the targets of a pretraining task.
- **Combined with other augmentations.** Speed perturbation, added noise and room simulation change the audio; SpecAugment changes the features, and the two kinds are often used together.
- **Policy search.** The policy can be tuned per data set; a stronger policy needs a larger model or longer training to pay off.

## Pitfalls

- **Masks larger than the utterance.** Without the bound $p \tau$, a time mask of up to $T$ steps can erase most of a short utterance, and the target becomes impossible to predict.
- **Masking before normalization.** If the features are normalized after masking, the zeros are no longer the mean and the masks become strong artificial edges.
- **Augmenting the evaluation data.** Apply SpecAugment only in training. Held-out and test inputs must stay unchanged.
- **Fixing the masks once.** Masks drawn once and stored make a fixed, larger data set. The benefit comes from new masks each epoch.
- **Expecting a fast gain.** With strong augmentation the model under-fits at first; it needs more training steps, and often a larger network, to reach its best result.

## Exercises

1. For a frequency mask with $f$ uniform on $\{0, \ldots, F\}$, show that the expected masked fraction of $\nu$ channels is $F / (2 \nu)$. Compute it for LB and SM with $\nu = 80$ and $\nu = 40$.
2. With two time masks of independent random lengths and positions, explain why the expected masked fraction is less than twice that of one mask.
3. Why do time masks of fixed maximum length hurt short utterances more than long ones? How does the bound $p \tau$ fix this?
4. Write a function that applies the policy LD to a spectrogram with a fixed random seed, and check that two calls with the same seed give the same masks.

## References
