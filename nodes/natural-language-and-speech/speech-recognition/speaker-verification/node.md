---
tag: PFGNZF
kind: problem
slug: speaker-verification
name: Speaker verification
aliases:
- speaker authentication
- voice verification
area: natural-language-and-speech/speech-recognition
level: core
summary: Decide whether a speech sample comes from a claimed speaker, by comparing it with the speaker's enrolled samples.
prereqs: [likelihood-ratio-test, neyman-pearson-lemma]
see_also: [gmm-ubm-speaker-verification, i-vector, x-vector, plda-scoring, equal-error-rate, speaker-diarization, map-speaker-adaptation, voice-activity-detection]
sources:
  - paper: doi:10.1006/dspr.1999.0361
    title: Douglas A. Reynolds, Thomas F. Quatieri and Robert B. Dunn, Speaker verification using adapted Gaussian mixture models, Digital Signal Processing 10(1-3), 2000, pages 19 to 41
    locator: the statement of verification as a test of two hypotheses and the likelihood ratio detector
  - url: https://cs.joensuu.fi/sipu/pub/SRE-review-Kinnunen-and-Li.pdf
    title: Tomi Kinnunen and Haizhou Li, An overview of text-independent speaker recognition, from features to supervectors, Speech Communication 52(1), 2010, pages 12 to 40
    locator: the introduction (identification, verification, text-dependent and text-independent tasks) and the section on evaluation
  - url: https://arxiv.org/abs/1304.2865
    title: Niko Brümmer and Edward de Villiers, The BOSARIS toolkit, theory, algorithms and code for surviving the new DCF, arXiv 1304.2865, 2013
    locator: "Section 2.2 (the Bayes decision threshold for a log likelihood ratio, equations 3 to 6)"
  - paper: doi:10.1109/TASL.2010.2064307
    title: Najim Dehak, Patrick J. Kenny, Réda Dehak, Pierre Dumouchel and Pierre Ouellet, Front-end factor analysis for speaker verification, IEEE Transactions on Audio, Speech, and Language Processing 19(4), 2011, pages 788 to 798
    locator: the i-vector system and its scoring
  - paper: doi:10.1109/ICASSP.2018.8461375
    title: David Snyder, Daniel Garcia-Romero, Gregory Sell, Daniel Povey and Sanjeev Khudanpur, X-vectors, robust DNN embeddings for speaker recognition, ICASSP 2018, pages 5329 to 5333
    locator: the embedding network and the PLDA back end
---

Speaker verification decides whether a speech sample comes from the person it claims to come from. The system has enrollment speech of the claimed speaker. It compares the test sample with it and either accepts or rejects the claim. It is a detection task: the answer is yes or no for one claimed identity, not a name chosen from a list.

## In plain words

Someone says "I am Alice" and speaks a few words. The system has heard Alice before. It must decide whether this voice is Alice's. It can make two mistakes: let in someone who is not Alice, or turn Alice away. Which mistake is worse depends on the use, so the system usually gives a score, and the owner sets the point at which a score is high enough.

## Definition

The input is an enrollment set $E$ of utterances of a speaker $s$, a test utterance $Y$, and the claim that $Y$ comes from $s$. Two hypotheses compete:

- $H_0$ (target): $Y$ comes from $s$;
- $H_1$ (nontarget): $Y$ comes from some other speaker.

The output is a score $\Lambda(E, Y)$ and a decision: accept if $\Lambda \ge \theta$, else reject. The two error rates at the threshold $\theta$ are the miss rate $P_{\text{miss}}(\theta) = P(\Lambda < \theta \mid H_0)$ and the false alarm rate $P_{\text{fa}}(\theta) = P(\Lambda \ge \theta \mid H_1)$.

If the score is the log likelihood ratio $\Lambda = \log p(Y \mid H_0, E) / p(Y \mid H_1)$, two classical results say what the best decision is.

- **Neyman-Pearson.** For any bound on $P_{\text{fa}}$, the test that thresholds the likelihood ratio has the smallest $P_{\text{miss}}$ ([Neyman-Pearson lemma](/neyman-pearson-lemma/), a theorem).
- **Bayes.** With a prior probability $\pi$ of a target trial and costs $C_{\text{miss}}$ and $C_{\text{fa}}$, the expected cost is smallest when the system accepts exactly when $\Lambda \ge \eta = \log(C_{\text{fa}} / C_{\text{miss}}) - \operatorname{logit} \pi$ (BOSARIS, Section 2.2).

The true densities are unknown, so real systems estimate a score and then calibrate it. A system is judged on a list of target and nontarget trials, by the [equal error rate](/equal-error-rate/) and by the detection cost at a stated $(\pi, C_{\text{miss}}, C_{\text{fa}})$.

## Variants

- **Text-dependent.** The speaker says a fixed phrase, or a phrase that the system prompts. The phonetic content is known, so short utterances are enough.
- **Text-independent.** Any speech, in any language. This is the task of most research and of the NIST speaker recognition evaluations.
- **Speaker identification.** Closed-set identification picks one speaker from $N$ enrolled speakers. Open-set identification may also answer "none of them".
- **Several enrollment sessions.** The enrollment set has several utterances, from different channels or days.
- **Mismatched conditions.** Enrollment and test come from different channels, languages or distances to the microphone.
- **Spoofing.** An attacker plays a recording, a voice conversion or a synthetic voice of the target. A separate detector (a countermeasure) is then needed, because a good verifier accepts a good copy.

## Examples

- **Known Gaussian scores.** Let one feature $x$ be $\mathcal{N}(2, 1)$ for the target and $\mathcal{N}(0, 1)$ for everyone else. Then $\Lambda(x) = \log \mathcal{N}(x; 2, 1) - \log \mathcal{N}(x; 0, 1) = 2x - 2$. At $\theta = 0$ the system accepts when $x \ge 1$, so $P_{\text{miss}} = P_{\text{fa}} = \Phi(-1) = 0.158655$. This is the equal error rate of the test.
- **A Bayes threshold.** With $\pi = 0.01$, $C_{\text{miss}} = 10$ and $C_{\text{fa}} = 1$, the threshold is $\eta = \log(1/10) - \log(0.01/0.99) = \log 9.9 = 2.292535$. A calibrated score of 1.5 is rejected and a score of 3.0 is accepted. Rare targets push the threshold up, and a costly miss pushes it down.
- **GMM-UBM.** The [GMM-UBM page](/gmm-ubm-speaker-verification/) works through a one-dimensional system by hand: the speaker frames $1.8, 2.2$ get the score $0.283261$ and the impostor frames $-1.2, 0.8$ get $-0.067896$.

## Known algorithms

- **GMM-UBM** (Reynolds, Quatieri and Dunn 2000). MAP-adapt a universal background model to the speaker, and score the average log likelihood ratio per frame. See [GMM-UBM speaker verification](/gmm-ubm-speaker-verification/).
- **i-vectors with PLDA** (Dehak et al. 2011). Map each utterance to a short [i-vector](/i-vector/) with a total variability model, and score pairs with [PLDA](/plda-scoring/) or with the cosine of the two vectors.
- **x-vectors with PLDA** (Snyder et al. 2018). Compute an [x-vector](/x-vector/) embedding with a neural network trained to classify speakers, and score with PLDA.
- **End-to-end embeddings.** Networks trained with angular margin losses give embeddings that are scored by cosine similarity.
- **Score normalization and calibration.** Z-norm, T-norm and S-norm make scores of different speakers comparable, and an affine map fitted by logistic regression turns them into log likelihood ratios.

## Bounds

- **The best possible error.** For known densities, no test does better than the likelihood ratio test at any false alarm rate (a theorem). The error of that test is the limit for the given features. In the Gaussian example it is $\Phi(-d'/2)$ at the equal error point, where $d'$ is the distance between the means in standard deviations.
- **Cost of scoring.** A GMM-UBM trial costs $O(T M d)$ for $T$ frames, $M$ Gaussians and feature dimension $d$. An embedding system computes one embedding per utterance once, and each trial then costs $O(d^2)$ for PLDA or $O(d)$ for the cosine, with $d$ the embedding dimension.
- **Accuracy.** Error rates are measurements on a stated trial list. They depend strongly on the duration of the speech, the channel and the language, and numbers from different lists cannot be compared.

## Reductions

- **Verification is a binary hypothesis test.** Every method builds an approximation of the likelihood ratio, so the theory of the [likelihood ratio test](/likelihood-ratio-test/) applies.
- **Identification reduces to verification.** Score the test utterance against each of the $N$ enrolled speakers and take the highest score. For open-set identification, also compare that score with a threshold.
- **Diarization uses verification scores.** [Speaker diarization](/speaker-diarization/) clusters segments with the same pairwise scores (for example PLDA scores of x-vectors), so it reduces in part to many verification trials.
- **Adaptation is the enrollment step.** In GMM-UBM, enrollment is [MAP adaptation](/map-speaker-adaptation/) of the background model.

## Applications

Telephone banking and call centers check a caller's identity by voice. Smart speakers and phones tell apart the people who use one device. Forensic speaker comparison expresses evidence as a likelihood ratio, with strict care about calibration and conditions. Speaker verification scores also serve diarization, the search for a speaker in an archive, and the adaptation of recognizers.

## References
