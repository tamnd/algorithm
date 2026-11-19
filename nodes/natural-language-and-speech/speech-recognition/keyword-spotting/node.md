---
tag: 41XNZR
kind: problem
slug: keyword-spotting
name: Keyword spotting
aliases:
- KWS
- wake word detection
area: natural-language-and-speech/speech-recognition
level: core
summary: Detect the occurrences of given words or phrases in an audio stream without transcribing all of it.
prereqs: [automatic-speech-recognition, hidden-markov-model]
see_also: [likelihood-ratio-test, dynamic-time-warping, word-lattice, confusion-network, connectionist-temporal-classification, voice-activity-detection, inverted-index, equal-error-rate]
sources:
  - paper: doi:10.1109/ICASSP.1989.266505
    title: J. Robin Rohlicek, William Russell, Salim Roukos and Herbert Gish, Continuous hidden Markov modeling for speaker-independent word spotting, ICASSP 1989
    locator: the keyword models with a background (filler) model and the score of a putative keyword
  - url: https://catalog.ldc.upenn.edu/docs/LDC2011S02/std06-evalplan-v10.pdf
    title: NIST, The spoken term detection (STD) 2006 evaluation plan, version 10, 2006
    locator: the definition of the term-weighted value and of the actual and maximum term-weighted values
  - paper: doi:10.1109/ICASSP.2014.6854370
    title: Guoguo Chen, Carolina Parada and Georg Heigold, Small-footprint keyword spotting using deep neural networks, ICASSP 2014
    locator: the network that outputs posteriors of keyword parts, the smoothing of the posteriors and the confidence score
---

Keyword spotting finds where given words or phrases occur in speech. The input is audio and a list of keywords. The output is a list of detections, each a keyword, a time and a score. Words outside the list do not matter, so a system can ignore most of the speech. There are two main settings: a device that listens all the time for one fixed phrase, and a search for any typed term in a large archive of recordings.

## In plain words

A phone waits for "hey, phone" and must react only to that phrase, among hours of other talk, music and noise. An analyst wants every place where a word was said in a thousand hours of calls. In both cases the system only has to say "here, with this confidence" for the words it was asked about. It can make two kinds of mistake: miss a real occurrence, or report one that is not there.

## Definition

The input is an audio signal of $T_{\text{speech}}$ seconds and a set of terms $K$. A term is a word or a sequence of words. The output is a set of detections $(k, t, s)$: a term, a time, and a score. The reference gives the true occurrences of each term. A detection is correct if a true occurrence of the same term lies within a time tolerance of it, and each true occurrence can match at most one detection. At a threshold $\theta$, the system reports the detections with $s \ge \theta$.

The term-weighted value of the NIST 2006 spoken term detection evaluation averages over the terms that occur at least once in the reference:

$$\text{TWV}(\theta) = 1 - \frac{1}{|K|} \sum_{k \in K} \Big[ P_{\text{miss}}(k, \theta) + \beta \, P_{\text{fa}}(k, \theta) \Big],$$

with $P_{\text{miss}}(k, \theta) = 1 - N_{\text{corr}}(k, \theta) / N_{\text{true}}(k)$ and $P_{\text{fa}}(k, \theta) = N_{\text{fa}}(k, \theta) / (T_{\text{speech}} - N_{\text{true}}(k))$, where each second of speech counts as one trial. The weight $\beta = 999.9$ comes from a cost-value ratio of 0.1 and a prior of $10^{-4}$ for a term in a trial. The actual TWV (ATWV) is the TWV at the threshold that the system chose; the maximum TWV is the best value over all thresholds. A perfect system has $\text{TWV} = 1$; a system that outputs nothing has 0; many false alarms make it negative.

For devices, the usual measures are the miss rate against the number of false alarms per hour, read from a DET or ROC curve.

## Variants

- **Wake word.** One or a few fixed phrases, on a small device, always on, with a small delay. The model is trained on many examples of the phrase.
- **Spoken term detection.** Any term typed at search time, in a large archive. The terms can be words that the recognizer has never seen (out of vocabulary).
- **Query by example.** The term is given as a spoken sample instead of text.
- **Streaming or offline.** A streaming system must decide within a short delay; an offline system can use the whole recording and an index.
- **Low-resource languages.** Little transcribed speech exists, and term detection is often the main use of the recognizer.

## Examples

- **A TWV by hand.** Take $T_{\text{speech}} = 3600$ s and three terms. Term 1 has 10 true occurrences; the system finds 8 and has 2 false alarms. Its value is $1 - 0.2 - 999.9 \cdot 2/3590 = 0.242953$. Term 2 has 2 occurrences, both found, with no false alarm: value 1. Term 3 has 4 occurrences, 1 found, and 1 false alarm: $1 - 0.75 - 999.9 / 3596 = -0.028059$. The TWV is the mean, $0.404965$. Each false alarm costs about $0.28$ on its term, as much as missing more than a quarter of the occurrences of a term with 4 of them, so the metric rewards a cautious threshold.
- **A filler model score.** In a word spotter with a keyword HMM and a filler HMM, a segment with log likelihood $-120.0$ under the keyword path and $-123.5$ under the best filler path gets the score $3.5$, a log likelihood ratio. The segment is a detection if $3.5$ reaches the threshold.

## Known algorithms

- **Keyword and filler HMMs** (Rohlicek, Russell, Roukos and Gish 1989). Decode with a network of keyword models in parallel with filler (garbage) models that absorb all other speech, and score each putative keyword by its likelihood against the background. The [Viterbi algorithm](/viterbi-algorithm/) finds the paths.
- **Recognition and search.** Run a full recognizer once, keep a [word lattice](/word-lattice/) or a [confusion network](/confusion-network/) with posteriors, and build an [inverted index](/inverted-index/) of the arcs. A search looks up the term and returns its occurrences with their posteriors. Lattices of subword units (phones, syllables or word pieces) serve terms outside the vocabulary.
- **Small neural detectors** (Chen, Parada and Heigold 2014). A network outputs, for each frame, the posteriors of the parts of the keyword and of a filler class. The posteriors are smoothed over a window, and the confidence combines the largest smoothed posterior of each part. Later systems use convolutional or recurrent networks, or a [CTC](/connectionist-temporal-classification/) model of the phrase.
- **Query by example.** Turn the spoken query and the archive into frame posteriors, and align them with subsequence [dynamic time warping](/dynamic-time-warping/).

## Bounds

- **Streaming cost.** A fixed detector costs a constant amount of work per frame, so it runs in $O(T)$ time for $T$ frames with constant memory. This is why wake-word detectors can run all the time on small chips.
- **Search cost.** With an index built once, a query costs time proportional to the length of its posting list, not to the length of the archive. Building the lattices costs one recognition pass.
- **The error trade-off.** For known score densities, a threshold on the likelihood ratio gives the fewest misses at each false alarm rate ([likelihood ratio test](/likelihood-ratio-test/), Neyman-Pearson). Real numbers are measurements on a stated data set and term list.

## Reductions

- **To speech recognition.** Transcribe all the speech and search the text. This is the most accurate approach for terms in the vocabulary when a strong recognizer exists, but it costs a full recognition pass, and every recognition error on a term becomes a miss or a false alarm.
- **To detection.** At each position, keyword spotting is a test of "the keyword ends here" against "something else", like [speaker verification](/speaker-verification/) with words in place of speakers.
- **To sequence alignment.** Query by example reduces to subsequence alignment of two sequences of feature vectors.

## Applications

Wake words of voice assistants and other devices, voice commands with a small vocabulary, monitoring of calls and broadcasts for given names or topics, search in archives of speech, and the retrieval of speech in languages with few resources.

## References
