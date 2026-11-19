---
tag: PMB4JR
kind: problem
slug: speaker-diarization
name: Speaker diarization
aliases:
- who spoke when
- speaker segmentation and clustering
area: natural-language-and-speech/speech-recognition
level: core
summary: Split an audio recording into segments by speaker and label segments of the same speaker alike, without knowing the speakers.
prereqs: [speaker-verification, agglomerative-clustering, bayesian-information-criterion]
see_also: [change-point-detection, spectral-clustering, hungarian-algorithm, x-vector, plda-scoring, voice-activity-detection, correlation-clustering, assignment-problem]
sources:
  - paper: doi:10.1109/TASL.2006.878256
    title: Sue E. Tranter and Douglas A. Reynolds, An overview of automatic speaker diarization systems, IEEE Transactions on Audio, Speech, and Language Processing 14(5), 2006, pages 1557 to 1565
    locator: the parts of a diarization system (speech detection, change detection, clustering) and the diarization error rate
  - paper: doi:10.1109/TASL.2011.2125954
    title: Xavier Anguera, Simon Bozonnet, Nicholas Evans, Corinne Fredouille, Gerald Friedland and Oriol Vinyals, Speaker diarization, a review of recent research, IEEE Transactions on Audio, Speech, and Language Processing 20(2), 2012, pages 356 to 370
    locator: the review of segmentation and clustering methods and of the evaluation
  - url: http://www.ee.columbia.edu/~dpwe/papers/ChenG98-bic.pdf
    title: Scott Shaobing Chen and P. S. Gopalakrishnan, Speaker, environment and channel change detection and clustering via the Bayesian information criterion, DARPA Broadcast News Transcription and Understanding Workshop, 1998
    locator: the change detection by the BIC difference of one Gaussian against two
  - paper: doi:10.1007/11965152_28
    title: Jonathan G. Fiscus, Jerome Ajot, Martial Michel and John S. Garofolo, The Rich Transcription 2006 Spring meeting recognition evaluation, MLMI 2006, Lecture Notes in Computer Science 4299, pages 309 to 322
    locator: the speaker diarization task and its scoring
---

Speaker diarization answers the question "who spoke when" for a recording. It splits the audio into segments, each spoken by one person, and gives segments of the same person the same label. The labels are arbitrary: the system does not know the names of the speakers, and usually not their number. Diarization is a step in the transcription of meetings, calls and broadcasts, where it tells which words belong to which speaker.

## In plain words

You have a recording of a meeting and no list of the people in it. Mark where each person talks, and use the same color for everything one person says. You do not need to know who the people are, only to keep them apart. Most systems first find where someone speaks, then cut the speech into short pieces, then group pieces that sound like the same voice.

## Definition

The input is an audio recording of length $D$. The output is a set of segments $(t_{\text{start}}, t_{\text{end}}, \ell)$ with labels $\ell$ from a set that the system chooses. Many systems assume one speaker at a time; others also mark overlapping speech, where a time can carry two labels.

The reference is a segmentation by people. A hypothesis is scored by the diarization error rate (DER). First map the hypothesis labels one to one to the reference labels so that the total time where the mapped labels agree is largest. This is an [assignment problem](/assignment-problem/), solved for example with the [Hungarian algorithm](/hungarian-algorithm/). Then

$$\text{DER} = \frac{T_{\text{miss}} + T_{\text{fa}} + T_{\text{conf}}}{T_{\text{speech}}},$$

where $T_{\text{miss}}$ is reference speech with no hypothesis speaker, $T_{\text{fa}}$ is hypothesis speech where the reference has none, $T_{\text{conf}}$ is speech given to the wrong speaker after the mapping, and $T_{\text{speech}}$ is the total reference speech time. With overlap, each time is weighted by the number of speakers. The DER can exceed 1, because false alarms are not bounded by the speech time. Lower is better.

Human boundaries are not exact to a few hundred milliseconds. So scoring often ignores a no-score collar around each reference boundary; 0.25 s on each side is a common value. Results with and without a collar, and with and without overlap, cannot be compared.

## Variants

- **Known or unknown number of speakers.** With the number given (for example two in a phone call), clustering stops at that number. Otherwise the system must also estimate it.
- **Overlap.** In meetings, people often talk at once. Systems that assume one speaker at a time miss the second speaker in every overlap.
- **Online diarization.** The labels must come with a short delay, for live captions.
- **Speaker-attributed recognition.** The output is words with speaker labels, and the error counts words.
- **Multichannel.** Several microphones give the direction of the sound as a further cue.

## Examples

- **A DER by hand.** The reference has speaker $A$ from 0 to 10 s and speaker $B$ from 10 to 20 s. The hypothesis has $X$ from 0 to 9 s, $Y$ from 9 to 19 s and $Y$ again from 21 to 22 s. The overlaps are $|X \cap A| = 9$, $|Y \cap B| = 9$, $|Y \cap A| = 1$ and $|X \cap B| = 0$, so the best mapping is $X \to A$, $Y \to B$. The errors are 1 s of confusion (9 to 10 s), 1 s of missed speech (19 to 20 s) and 1 s of false alarm (21 to 22 s). Without a collar, $\text{DER} = 3/20 = 15\%$. With a collar of 0.25 s around the boundaries at 0, 10 and 20 s, the scored speech is $20 - 0.25 - 0.5 - 0.25 = 19$ s, the confusion and the miss shrink to 0.75 s each, and the false alarm stays 1 s, so $\text{DER} = 2.5/19 = 13.16\%$.
- **BIC change detection.** Take the one-dimensional features $0, 1, -1, 0, 3, 4, 2, 3$ ($N = 8$, $d = 1$). For a split after frame $i$, compare one Gaussian for all frames with one Gaussian per side:
$$\Delta\text{BIC}(i) = \tfrac{N}{2} \log \hat\sigma^2 - \tfrac{i}{2} \log \hat\sigma_1^2 - \tfrac{N - i}{2} \log \hat\sigma_2^2 - \lambda \tfrac12 \big(d + \tfrac{d(d+1)}{2}\big) \log N,$$
with maximum likelihood variances and $\lambda = 1$. This form, with the factor $\frac12$ on both the likelihood term and the penalty, follows from the BIC. Chen and Gopalakrishnan write the likelihood term without the $\frac12$, so a value $\lambda$ in their form equals $\lambda/2$ in this one. For $i = 2, \ldots, 6$ the values are $-0.07835$, $1.050746$, $4.739551$, $1.050746$ and $-0.07835$. The largest value is at $i = 4$, and it is positive, so the method puts a change between the fourth and the fifth frame, where the mean jumps from about 0 to about 3.

## Known algorithms

- **Segmentation and clustering.** Detect speech with [voice activity detection](/voice-activity-detection/). Find speaker changes, for example by the [BIC](/bayesian-information-criterion/) test above (Chen and Gopalakrishnan 1998), a form of [change-point detection](/change-point-detection/). Then merge segments by [agglomerative clustering](/agglomerative-clustering/), each time the closest pair, and stop when the BIC no longer improves. Tranter and Reynolds 2006 describe this design.
- **Embeddings and clustering.** Cut the speech into short overlapping windows (for example 1.5 s), compute an [x-vector](/x-vector/) or i-vector per window, score pairs with [PLDA](/plda-scoring/) or the cosine, and cluster with agglomerative or [spectral clustering](/spectral-clustering/).
- **Resegmentation.** Refine the boundaries with a [hidden Markov model](/hidden-markov-model/) whose states are the speakers, decoded by Viterbi or by variational Bayes.
- **End-to-end neural diarization.** A network outputs, for each frame, the probability that each speaker is active. It handles overlap, and it is trained with a loss that is invariant to the order of the speakers.

## Bounds

- **Scoring.** With $S$ reference and $S'$ hypothesis speakers, the mapping is an assignment problem on an $S \times S'$ matrix of overlap times, solved in $O(\max(S, S')^3)$ time. The overlap times take one pass over the sorted segment boundaries.
- **Clustering.** Agglomerative clustering of $n$ segments takes $O(n^2)$ scores and, with a priority queue, $O(n^2 \log n)$ time. Finding the best partition for a general pairwise score is NP-hard in forms such as [correlation clustering](/correlation-clustering/), so practical systems use greedy or spectral methods.
- **Accuracy.** DER values are measurements on a stated data set with a stated collar and overlap rule.

## Reductions

- **To speaker verification.** Deciding whether two segments have the same speaker is a [speaker verification](/speaker-verification/) trial, so the scores of verification systems serve as distances for clustering.
- **To clustering.** With a fixed segmentation, diarization is the clustering of segments with an unknown number of clusters.
- **To change-point detection.** Segmentation is change-point detection in the sequence of features.
- **The metric to an assignment problem.** The label mapping in the DER is a maximum weight bipartite matching.

## Applications

Meeting transcription with speaker turns, call center analytics that separate the agent and the customer, the indexing of broadcast news and of podcasts, speaker adaptation in recognizers (the clusters give the speakers for [MLLR](/maximum-likelihood-linear-regression/) or [VTLN](/vocal-tract-length-normalization/)), and the study of conversation in medicine and linguistics.

## References
