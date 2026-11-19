---
tag: V7AWJA
kind: technique
slug: vocal-tract-length-normalization
name: Vocal tract length normalization
aliases:
- VTLN
- frequency warping speaker normalization
area: natural-language-and-speech/speech-recognition
level: advanced
summary: Warp the frequency axis of each speaker by a factor chosen by maximum likelihood, to reduce differences in vocal tract length.
prereqs: [mel-frequency-cepstral-coefficients, formant-estimation, gmm-hmm-acoustic-model]
see_also: [maximum-likelihood-linear-regression, map-speaker-adaptation, source-filter-model, forced-alignment, mel-scale, perceptual-linear-prediction, golden-section-search, short-time-fourier-transform]
sources:
  - paper: doi:10.1109/89.650310
    title: Li Lee and Richard C. Rose, A frequency warping approach to speaker normalization, IEEE Transactions on Speech and Audio Processing 6(1), 1998, pages 49 to 60
    locator: the warping of the filterbank, the maximum likelihood choice of the warp factor in training and in recognition
  - url: https://dblp.org/rec/conf/icassp/LeeR96
    title: Li Lee and Richard C. Rose, Speaker normalization using efficient frequency warping procedures, ICASSP 1996, pages 353 to 356
    locator: the frequency warping in the filterbank and the search over warp factors
  - url: https://www-i6.informatik.rwth-aachen.de/publications/download/181/PitzMichaelNeyHermann--VocalTractNormalizationEqualsLinearTransformationinCepstralSpace--2005.pdf
    title: Michael Pitz and Hermann Ney, Vocal tract normalization equals linear transformation in cepstral space, IEEE Transactions on Speech and Audio Processing 13(5), 2005, pages 930 to 944
    locator: the result that a frequency warp is a linear map of the cepstral coefficients
---

Vocal tract length normalization (VTLN) reduces the differences between speakers that come from the length of the vocal tract. A shorter tract has higher formants, so the spectra of children and of most women are stretched along the frequency axis compared with those of most men. VTLN picks one warp factor $\alpha$ per speaker, scales the frequency axis of the speaker's spectra by $\alpha$ before the features are computed, and so moves every speaker toward one reference. The factor is the one under which the acoustic model gives the speaker's data the highest likelihood.

## In plain words

Two people say the same vowel. The shape of the sound is similar, but the person with the shorter throat and mouth produces it at higher frequencies, as if it were played a little faster. A recognizer trained on one kind of voice sees the other as a different sound.

VTLN tries a few ways to squeeze or stretch the frequency scale of each speaker, for example by 12% in either direction. For each try, it asks the recognizer how well the result fits its models. It keeps the best one. One number per speaker is enough, so a few seconds of speech are enough to choose it.

## When it applies

- The front end computes features from a short-time spectrum through a filterbank, as [MFCC](/mel-frequency-cepstral-coefficients/) and [PLP](/perceptual-linear-prediction/) features do. The warp is then a change of the center frequencies of the filters, and it costs nothing extra per frame.
- The speakers differ in age and sex, for example a system that serves adults and children. The gain is small when all speakers are similar.
- Each speaker gives several utterances, or one utterance long enough to estimate one parameter. The speaker identity must be known, or be estimated by clustering.
- The source-filter view holds: the [formants](/formant-estimation/) are resonances of the tract. For a uniform tube of length $L$ closed at one end, the resonances are $F_k = (2k - 1) c / (4L)$, so all of them scale as $1/L$ (a model, and only an approximation for a real tract). A linear warp of frequency matches this scaling.

## The template

The warp function. For a factor $\alpha$, a cutoff $f_0$ and the Nyquist frequency $f_N$, the piecewise linear warp is

$$g_\alpha(f) = \begin{cases} \alpha f & 0 \le f \le f_0, \\ \alpha f_0 + \dfrac{f_N - \alpha f_0}{f_N - f_0} (f - f_0) & f_0 < f \le f_N. \end{cases}$$

It is linear below $f_0$, and the second piece makes $g_\alpha(f_N) = f_N$, so the warped axis covers the same band and no filter falls outside it. Software differs on whether $g_\alpha$ or its inverse is applied to the filter center frequencies, and so on whether $\alpha < 1$ means a shorter or a longer tract. A system must use one convention throughout.

The steps for one speaker:

1. Choose a grid of factors, for example $\alpha = 0.88, 0.90, \ldots, 1.12$, 13 values in steps of 0.02 (a common choice).
2. Get a transcription of the speaker's utterances: the reference text in training, or the output of a first recognition pass without VTLN at test time.
3. For each $\alpha$ in the grid, compute the features with the warped filterbank, align them to the transcription with the acoustic model by [forced alignment](/forced-alignment/), and record the log likelihood of the alignment.
4. Keep the factor $\hat\alpha$ with the highest log likelihood.
5. Compute the speaker's final features with $\hat\alpha$, and recognize them with a model trained on normalized features.

To train that model, start with a model trained without warping. Choose $\hat\alpha$ for every training speaker with steps 1 to 4, compute all features again with these factors, and retrain. Repeat this a few times, until the factors stop changing.

Cost. With $K$ factors in the grid, step 3 runs feature extraction and forced alignment $K$ times on the speaker's data, so the choice costs about $K$ alignment passes. A small Gaussian mixture model trained on normalized features can replace the forced alignment: it needs no transcription and no first pass, at some loss of accuracy.

## Classic examples

- **Tube formants.** With $c = 35000$ cm/s, a tube of $L = 17.5$ cm has the resonances 500, 1500 and 2500 Hz, and a tube of 16 cm has 546.875, 1640.625 and 2734.375 Hz. Take the 17.5 cm tube as the reference. The exact factor is $16 / 17.5 = 0.914286$. On the grid, $\alpha = 0.92$ maps the 16 cm resonances to 503.125, 1509.375 and 2515.625 Hz. As a stand-in for the likelihood, take the sum of squared distances to the reference resonances: it is 2136.2 at 0.90, 341.8 at 0.92 and 6921.4 at 0.94, so the grid search picks 0.92. A 15 cm tube has 583.333, 1750 and 2916.667 Hz, and it needs a factor near $15 / 17.5 = 0.857$, which is outside the usual grid.
- **The piecewise warp at 8 kHz sampling.** With $f_N = 4000$ Hz, the example cutoff $f_0 = 3400$ Hz and $\alpha = 0.92$: $g(1000) = 920$, $g(3400) = 3128$, and above $f_0$ the slope is $(4000 - 3128)/600 = 1.453$, so $g(3700) = 3564$ and $g(4000) = 4000$.
- **Lee and Rose.** Lee and Rose (1996, 1998) warp the filterbank of a mel-cepstrum front end and choose the factor by maximum likelihood, for each speaker in training and with a first recognition pass at test time. They also give faster ways to choose the factor.
- **Children's speech.** VTLN is a usual first step when a recognizer trained on adults must serve children, whose formants are far higher. The size of the gain is a measurement that depends on the system and the data.

## Variations

- **Other warp functions.** A bilinear (all-pass) warp $\tilde\omega = \omega + 2 \arctan\big(a \sin\omega / (1 - a \cos\omega)\big)$ keeps $0$ and $\pi$ fixed without a breakpoint. A power warp or a warp of the mel scale are also used.
- **VTLN as a linear transform.** Pitz and Ney (2005) show that for common warp functions the warped cepstrum is a linear function of the unwarped cepstrum. VTLN is then a constrained form of [MLLR](/maximum-likelihood-linear-regression/) with one parameter, and it can be computed on the cepstra without a new pass through the filterbank. With the matrix known, the Jacobian term of the likelihood can be included.
- **A faster search.** The log likelihood is often close to unimodal in $\alpha$, so a [golden-section search](/golden-section-search/) or a few steps of a gradient method can replace the full grid (a heuristic: nothing guarantees one maximum).
- **Combination with other adaptation.** VTLN removes a large, simple difference with one parameter. MLLR or [MAP adaptation](/map-speaker-adaptation/) after it model the rest.
- **Augmentation.** In neural acoustic models, random warp factors in training, without a per-speaker choice, are a common form of data augmentation.

## Pitfalls

- **The Jacobian.** The warp changes the feature space, so the likelihoods of features computed with different $\alpha$ are densities on different spaces. Without the Jacobian of the map, the comparison favors factors that shrink the variance of the features. Most systems ignore the term and it often works, but the choice is then a heuristic. Normalizing the variance of each feature per speaker removes part of the bias.
- **A model that is not normalized.** If the acoustic model was trained without VTLN, the chosen factors describe how far the speaker is from the average training speaker, not from a reference. Train the model on warped features, and iterate.
- **Errors of the first pass.** At test time the transcription is a hypothesis. On poor audio the errors of the first pass can bias the choice of $\alpha$.
- **Too narrow or too wide a grid.** A grid of 0.88 to 1.12 covers most adults. Speech of young children may need factors outside it, and a wider grid gives more chance of a wrong choice on little data.
- **Mixed conventions.** Training and test must apply the warp in the same direction and with the same cutoff and Nyquist frequency.

## Exercises

1. A speaker has formants 15% higher than the reference. Which factor in the grid 0.88 to 1.12 does the tube model predict, if $g_\alpha$ is applied to the speaker's frequencies? (Answer: about $1/1.15 = 0.87$, so 0.88 at the edge of the grid.)
2. Show that $g_\alpha$ is continuous and strictly increasing on $[0, f_N]$ when $\alpha f_0 < f_N$. Why must the slope of the second piece be positive?
3. With $f_N = 8000$ Hz, $f_0 = 7000$ Hz and $\alpha = 1.1$, compute $g(7000)$, the slope of the second piece and $g(7500)$. (Answer: 7700, 0.3 and 7850.)
4. Explain why a maximum likelihood choice of $\alpha$ without the Jacobian term can pick a factor that maps many frames onto the same few filters.

## References
