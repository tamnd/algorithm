---
tag: PT86N9
kind: problem
slug: automatic-speech-recognition
name: Automatic speech recognition
aliases:
- ASR
- speech-to-text
area: natural-language-and-speech/speech-recognition
level: intro
summary: Transcribe the words spoken in an audio signal into text.
prereqs: [hidden-markov-model, language-model]
see_also: [source-channel-speech-recognition, word-error-rate, gmm-hmm-acoustic-model, hclg-decoding-graph, hybrid-dnn-hmm, connectionist-temporal-classification, rnn-transducer, listen-attend-and-spell]
sources:
  - paper: doi:10.1109/PROC.1976.10159
    title: Frederick Jelinek, Continuous speech recognition by statistical methods, Proceedings of the IEEE 64(4), 1976, pages 532 to 556
    locator: the statement of recognition as the search for the most probable word string given the acoustic data
  - paper: doi:10.1109/TPAMI.1983.4767370
    title: Lalit R. Bahl, Frederick Jelinek and Robert L. Mercer, A maximum likelihood approach to continuous speech recognition, IEEE Transactions on Pattern Analysis and Machine Intelligence PAMI-5(2), 1983, pages 179 to 190
    locator: the decomposition into an acoustic processor, a language model and a decoder
  - paper: doi:10.1561/2000000004
    title: Mark Gales and Steve Young, The application of hidden Markov models in speech recognition, Foundations and Trends in Signal Processing 1(3), 2008, pages 195 to 304
    locator: the chapter on the architecture of an HMM-based recognizer
  - book: isbn:9780130226167
    title: Xuedong Huang, Alex Acero and Hsiao-Wuen Hon, Spoken Language Processing, Prentice Hall PTR, 2001
    locator: the part on speech recognition (acoustic models, language models and search)
  - paper: doi:10.1016/S0022-0000(02)00009-0
    title: Rune B. Lyngsø and Christian N. S. Pedersen, The consensus string problem and the complexity of comparing hidden Markov models, Journal of Computer and System Sciences 65(3), 2002, pages 545 to 569
    locator: the NP-hardness of finding the most probable string of a hidden Markov model
---

Automatic speech recognition (ASR) takes an audio signal of speech and outputs the sequence of words that was said. The signal is first turned into a sequence of feature frames, and the recognizer searches for the word sequence that best explains those frames. The usual measure of quality is the [word error rate](/word-error-rate/) on a named test set. Statistical recognizers state the task as the search for the most probable word sequence, which splits into an acoustic model and a [language model](/language-model/) by the [source-channel model](/source-channel-speech-recognition/).

## In plain words

A person speaks, and the computer must write down the words. The sound is cut into short slices, a hundredth of a second each, and each slice is described by a few numbers. The same word sounds different from speaker to speaker and from one time to the next, words run into each other without pauses, and the number of slices for a word is not fixed.

So the computer does not look the slices up in a table. It weighs every word sequence it can think of by two questions: how well does this sequence match the sounds, and how likely is it as a sentence of the language? It outputs the sequence with the best combined answer. The answers are counted by how many words are wrong, missing or extra.

## Definition

The input is a speech signal, sampled at for example 16 kHz. A front end turns it into a sequence of feature frames $O = o_1 \ldots o_T$, usually one frame every 10 ms over a window of 25 ms, for example the [MFCC](/mel-frequency-cepstral-coefficients/) vectors with their [delta features](/delta-features/). The output is a word sequence $W = w_1 \ldots w_U$ over a vocabulary $V$, with $U$ not known in advance.

There is no exact answer to compute: the correct output is the transcript that a human would write, under agreed rules of normalization. A recognizer is judged by the corpus word error rate of its outputs against reference transcripts on a test set that it was not trained on. The statistical form of the task, with a model of the joint distribution of words and frames, is

$$W^* = \arg\max_{W \in V^*} P(W \mid O) = \arg\max_{W} p(O \mid W)\, P(W),$$

by [Bayes' theorem](/bayes-theorem/), because $p(O)$ does not depend on $W$. This rule minimizes the probability that the whole sentence is wrong, if the model is correct. It does not minimize the expected number of word errors; a decoder that targets the WER picks the hypothesis with the least expected word errors, for example from a [confusion network](/confusion-network/).

## Variants

- **Isolated words or continuous speech.** An isolated word recognizer knows where each word starts and ends. In continuous speech the word boundaries are hidden, and their number is not known.
- **Vocabulary size.** Digit strings and command sets have tens of words, the Resource Management task had about 1000 and the Wall Street Journal tasks had 5000 and 20000 words. Open vocabulary systems handle words that are not in a fixed list, often with subword units.
- **Speaker dependent or independent.** A speaker dependent system is trained for one person. A speaker independent system must work for anyone, often with [speaker adaptation](/maximum-likelihood-linear-regression/) at test time.
- **Speaking style and channel.** Read speech, broadcast news and conversational telephone speech get harder in this order. Noise, far microphones and accents make each of them harder.
- **Streaming or offline.** A streaming recognizer outputs words with a short delay while the audio arrives. An offline one sees the whole utterance first.
- **Related tasks.** [Keyword spotting](/keyword-spotting/) looks for a few words only, [speaker diarization](/speaker-diarization/) finds who spoke when, and [forced alignment](/forced-alignment/) finds the times of words that are already known.

## Examples

- **Digits.** "Call 5 5 5 0 1 2 3" from a phone line, with a vocabulary of 11 words and no language model beyond "any digit string".
- **Dictation.** Read sentences from newspaper text, as in the Wall Street Journal evaluations. On the Nov'93 tests, the system of Young, Odell and Woodland 1994 had a word error rate of 4.90 percent on the 5k task and 12.67 percent on the 20k task (measurements).
- **Conversational speech.** Telephone conversations between strangers, with hesitations, restarts and overlapping speech, are much harder than read speech.
- **Template matching.** A recognizer for a few command words that a single user records once can compare the input with each recording by [dynamic time warping](/dynamic-time-warping/) and output the closest word.

## Known algorithms

- **Template matching by DTW.** Compare the input with stored examples of each word by [dynamic time warping](/dynamic-time-warping/), usually inside a [Sakoe-Chiba band](/sakoe-chiba-band/). This was the main method for isolated words in the 1970s.
- **HMM recognizers.** Model each phone by a [GMM-HMM](/gmm-hmm-acoustic-model/), use [triphone models](/triphone-model/) with [tree-based state tying](/phonetic-decision-tree-state-tying/), build the word models from a [pronunciation lexicon](/pronunciation-lexicon/), and add an [n-gram language model](/n-gram-language-model/). Training uses Baum-Welch, often started by [Viterbi training](/viterbi-training/).
- **Decoding.** Search for $W^*$ with the Viterbi approximation, which replaces the sum over state paths by the best path. Recognizers do this with a [time-synchronous beam search](/time-synchronous-beam-search/), for example by [token passing](/token-passing/), over a composed [HCLG decoding graph](/hclg-decoding-graph/), or with a [stack decoder](/stack-decoding/). The decoder can write a [word lattice](/word-lattice/) for a second pass of [lattice rescoring](/lattice-rescoring/) with a stronger language model.
- **Hybrid models.** A [hybrid DNN-HMM](/hybrid-dnn-hmm/) replaces the Gaussian mixtures by a neural network that predicts the tied states, and keeps the rest of the HMM recognizer.
- **End-to-end models.** [Connectionist temporal classification](/connectionist-temporal-classification/), the [RNN transducer](/rnn-transducer/) and attention models such as [Listen, Attend and Spell](/listen-attend-and-spell/) map the frames to characters or subword units with one neural network, and decode by beam search.

## Bounds

The search space is $V^*$, and even for a fixed length $U$ there are $|V|^U$ word sequences, so no recognizer enumerates them. With an HMM acoustic model and an n-gram language model, the Viterbi approximation is a best path problem in a graph with $T$ layers, one per frame, and takes time linear in $T$ times the number of arcs of the decoding graph. This is exact for the best state path, and decoders still prune it with a beam because the graphs have millions of arcs.

The exact rule that sums over the state paths of each word sequence is harder. Lyngsø and Pedersen 2002 proved that finding the most probable string that a hidden Markov model emits is NP-hard (a theorem), and the most probable word sequence of an HMM recognizer is a problem of this kind. This is one reason why decoders use the best path, or approximate the sum on a lattice.

There is no useful lower bound on the WER: it depends on the data, and human transcribers also disagree with each other on hard speech.

## Reductions

- **To HMM decoding.** With the Viterbi approximation, recognition is [HMM decoding](/hmm-decoding/) on one large HMM whose states are the states of the phone models in all the words and word sequences that the language model allows.
- **To a weighted transducer.** The language model G, the lexicon L, the context dependency C and the HMMs H are weighted finite-state transducers, and their [composition](/weighted-transducer-composition/) gives one decoding graph. Recognition becomes a best path search through it.
- **From the source-channel model.** The [source-channel model](/source-channel-speech-recognition/) reduces the task to two models that can be trained apart, one on audio with transcripts and one on text, the same split as in [noisy channel spelling correction](/noisy-channel-spelling-correction/).

## Applications

Dictation and voice typing, voice assistants and command interfaces, captions for video and live broadcasts, transcription of meetings and call centers, voice search, and the input of spoken language translation. Speech recognition also gives the word times for audio search and for corpus studies of speech.

## References
