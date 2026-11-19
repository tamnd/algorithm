---
tag: 3SKZJE
kind: problem
slug: text-to-speech
name: Text-to-speech
aliases:
- speech synthesis
- TTS
area: natural-language-and-speech/speech-analysis-and-synthesis
level: intro
summary: "Produce natural and intelligible speech audio that says a given input text."
prereqs: [source-filter-model]
see_also: [tts-text-normalization, grapheme-to-phoneme-conversion, unit-selection-synthesis, hmm-based-speech-synthesis, tacotron, hifi-gan, mean-opinion-score, automatic-speech-recognition]
sources:
  - book: isbn:9780521899277
    title: "Paul Taylor, Text-to-Speech Synthesis, Cambridge University Press, 2009"
    locator: "Chapter 3 (The text-to-speech problem), Chapters 4, 5, 6 and 8 (text, prosody and pronunciation) and Chapters 14 to 16 (concatenative, HMM and unit-selection synthesis)"
  - url: https://web.stanford.edu/~jurafsky/slp3/
    title: "Daniel Jurafsky and James H. Martin, Speech and Language Processing, 3rd edition draft, August 24, 2025"
    locator: "the chapter Text-to-Speech"
  - paper: doi:10.1016/j.specom.2009.04.004
    title: "Heiga Zen, Keiichi Tokuda and Alan W. Black, Statistical parametric speech synthesis, Speech Communication 51(11), 2009, pages 1039 to 1064"
    locator: "Section 1 (Introduction)"
---

Text-to-speech (TTS) is the task of turning written text into speech audio that says it. The output should be intelligible, so that a listener gets every word, and natural, so that it sounds like a person. The task is the reverse of [automatic speech recognition](/automatic-speech-recognition/), but it is not a search for one right answer: many different waveforms say the same text well, and the result is judged by listeners. Most systems split the task in two. A front end turns the text into a linguistic description: the words to say ([text normalization](/tts-text-normalization/)), their phonemes ([grapheme-to-phoneme conversion](/grapheme-to-phoneme-conversion/)) and the prosody. A back end turns that description into a waveform. The back end has been built in turn from rules ([formant synthesis](/formant-synthesis/)), from recorded pieces ([unit selection](/unit-selection-synthesis/)), from statistical models ([HMM-based synthesis](/hmm-based-speech-synthesis/)) and from neural networks such as [Tacotron](/tacotron/), [FastSpeech](/fastspeech/), [WaveNet](/wavenet/), [HiFi-GAN](/hifi-gan/), [VITS](/vits/) and [neural codec language models](/neural-codec-language-model/).

## In plain words

A text-to-speech system reads text aloud. First it must decide what to say. "Dr. Smith lives at 12 St. John St." has to become "doctor Smith lives at twelve Saint John Street", and the system must know how each word sounds. It must also choose where to pause, which words to stress, and how the pitch rises and falls.

Then it must make the sound. Old systems used rules about the voice. Later systems glued together small pieces of recorded speech. Newer systems learn from many hours of one person reading, and make new audio that sounds like that person.

There is no single right answer. Many ways of saying a sentence are good. So people listen to the result and give it a score.

## Definition

**Input.** A text $w$, a string over a character set, often with a choice of voice (a speaker identity or a short recording of the target voice) and sometimes a speaking style.

**Output.** A waveform $x = (x_1, \ldots, x_N)$ at a sampling rate $f_s$, for example 16, 22.05 or 24 kHz.

**Goal.** The waveform should say exactly the words that a fluent reader would say for $w$, in the chosen voice, with natural prosody. There is no formal objective. A learned system is trained on pairs of text and recorded speech, usually by maximizing a likelihood or minimizing a distance to the recordings, and judged by:

- **Naturalness:** the [mean opinion score](/mean-opinion-score/), the mean of listener ratings on a 1 to 5 scale (ITU-T P.800), with its confidence interval.
- **Intelligibility:** the [word error rate](/word-error-rate/) of listeners, or of a speech recognizer, transcribing the output.
- **Voice similarity:** listener ratings or the cosine similarity of [speaker verification](/speaker-verification/) embeddings, for systems that copy a voice.
- **Speed:** the real-time factor, the compute time divided by the duration of the audio.

**The usual decomposition.** $w \to$ normalized words $\to$ phonemes with stress and phrase breaks $\to$ acoustic features (a mel spectrogram, or durations, pitch and spectrum) $\to x$. End-to-end models merge some of these steps, but almost all still use a text normalizer and many use a phoneme front end.

## Variants

- **Single speaker or many.** A single-speaker model is trained on hours of one voice. A multi-speaker model adds a speaker embedding.
- **Zero-shot voice cloning.** The voice is given by a few seconds of audio at synthesis time, with no training on that speaker, as in [neural codec language models](/neural-codec-language-model/).
- **Expressive and controllable synthesis.** Control of emotion, emphasis, speaking rate or pitch.
- **Streaming.** Audio must start before the whole text is processed, which limits how far a model may look ahead.
- **Low-resource and multilingual.** Little training data for a language, or one model for many languages.
- **Speech-to-speech.** Voice conversion changes the voice of a recording and keeps the words; it shares the back end with TTS.

## Examples

- **Front end.** "Dr. Smith lives at 12 St. John St." becomes "doctor smith lives at twelve saint john street". The two copies of "St." need different readings, chosen from context: before a name it is "saint", after one it is "street".
- **Lengths.** Three seconds of audio at 22050 Hz is $3 \cdot 22050 = 66150$ samples. With a hop of 256 samples, that is $66150 / 256 \approx 258$ mel frames. A frame-level acoustic model makes about 258 vectors; a sample-level model makes 66150 values.
- **Ambiguity.** "I read the book" is read with /r iy d/ or /r eh d/ depending on the tense, which the text alone may not show. "Lead" (the metal or the verb) and "live" (verb or adjective) are other homographs. A TTS system must choose one.

## Known algorithms

- **[Formant synthesis](/formant-synthesis/).** Rules drive a [source-filter model](/source-filter-model/) with resonances at the formant frequencies. Intelligible and small, but clearly synthetic.
- **Concatenative synthesis.** Recorded pieces are joined, with [PSOLA](/psola/) to change their pitch and duration. [Unit selection](/unit-selection-synthesis/) picks the pieces from a large database by a [Viterbi](/viterbi-algorithm/) search over target and join costs.
- **Statistical parametric synthesis.** [HMM-based synthesis](/hmm-based-speech-synthesis/) models the parameters with context-dependent HMMs, generates them with [MLPG](/maximum-likelihood-parameter-generation/) and drives a vocoder.
- **Neural acoustic models.** [Tacotron](/tacotron/) generates mel frames with attention; [FastSpeech](/fastspeech/) generates them in parallel from durations.
- **Neural vocoders.** [WaveNet](/wavenet/) generates samples one at a time; [HiFi-GAN](/hifi-gan/) generates them in parallel. The [Griffin-Lim algorithm](/griffin-lim-algorithm/) recovers a phase from a magnitude spectrogram without training.
- **End-to-end models.** [VITS](/vits/) goes from phonemes to waveform in one network; [neural codec language models](/neural-codec-language-model/) generate the tokens of an audio codec.

## Bounds

There is no lower bound in the usual sense, because the task has no exact solution. A few facts bound the cost of methods:

- **Output size.** Any method writes $N = f_s \cdot$ duration samples, so the time is $\Omega(N)$.
- **Sequential steps.** A model that generates each sample from the previous ones needs $N$ dependent steps, for example 24000 per second of audio at 24 kHz. Frame-level and parallel models need far fewer: Tacotron 2 has one decoder step per 12.5 ms frame, and parallel models a constant number of passes.
- **Front end.** Text normalization and lookup are linear in the length of the text for a fixed grammar and lexicon. Unit selection is linear in the number of target units and quadratic in the number of candidates per unit.

## Reductions

- **To smaller problems.** TTS reduces to [text normalization](/tts-text-normalization/), [grapheme-to-phoneme conversion](/grapheme-to-phoneme-conversion/), prosody prediction, acoustic modeling and waveform generation. Each part is studied and evaluated alone.
- **Unit selection to shortest path.** Choosing the units is a shortest path in a layered graph, solved by dynamic programming.
- **Alignment.** Learning durations from text and audio is a monotonic alignment problem, solved by [forced alignment](/forced-alignment/), by attention, or by the monotonic alignment search of VITS.
- **Language modeling.** With a neural audio codec, speech becomes a sequence of discrete tokens, and TTS becomes conditional [causal language modeling](/causal-language-modeling/).
- **Evaluation through recognition.** Intelligibility is measured by running a speech recognizer on the output, which turns a listening test into a computation of word error rate.

## Applications

Screen readers and other aids for people who are blind or cannot speak; voice assistants and telephone systems; reading of messages, navigation and news; audiobooks and dubbing; language learning; and the generation of training data for speech recognition.
