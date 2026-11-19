---
tag: ZQT3HD
kind: definition
slug: mean-opinion-score
name: Mean opinion score
aliases:
- MOS
area: natural-language-and-speech/speech-analysis-and-synthesis
level: intro
summary: The mean of listener ratings of speech quality or naturalness on a five-point scale, the standard subjective score of TTS.
prereqs: [confidence-interval]
see_also: [t-confidence-interval, standard-error, student-t-test, bootstrap-method, word-error-rate, formant-synthesis, psola]
sources:
  - url: https://www.itu.int/rec/T-REC-P.800
    title: ITU-T Recommendation P.800, Methods for subjective determination of transmission quality, 08/1996
    locator: "Annex B (absolute category rating and the listening-quality scale), Annex D (degradation category rating) and Annex E (comparison category rating)"
  - url: https://www.itu.int/rec/T-REC-P.800.1
    title: ITU-T Recommendation P.800.1, Mean opinion score (MOS) terminology, 07/2016
    locator: the names MOS-LQS, MOS-LQO and MOS-LQE for subjective, objective and estimated listening quality
  - url: https://www.itu.int/rec/T-REC-P.800.2
    title: ITU-T Recommendation P.800.2, Mean opinion score interpretation and reporting, 07/2016
    locator: the whole recommendation (what a report of a MOS must state, and why scores from different tests are not directly comparable)
  - book: isbn:9781466504219
    title: "Philipos C. Loizou, Speech Enhancement, Theory and Practice, second edition, CRC Press, 2013"
    locator: "Chapter 10, Section 10.3.2.1 (p. 463), the absolute category rating test and the MOS"
---

The mean opinion score (MOS) is the number that most papers on speech coding, enhancement and [text-to-speech](/text-to-speech/) report for the quality that people hear. A group of listeners hears each sample and rates it on a scale of five categories, from 5 (Excellent) to 1 (Bad). The MOS of a system is the mean of these ratings. It is a measurement of people, not a property of the signal, so it depends on the listeners, the samples and the other systems in the same test. A higher MOS is better, and every MOS is between 1 and 5.

## Definition

An absolute category rating (ACR) test, as in ITU-T P.800 Annex B, plays each sample to each listener once, without a reference. The listener gives one of five categories, which have these scores:

| Score | Category |
|---|---|
| 5 | Excellent |
| 4 | Good |
| 3 | Fair |
| 2 | Poor |
| 1 | Bad |

For quality the question is about the quality of the speech. For [text-to-speech](/text-to-speech/) the question is usually about naturalness, with the same five scores.

Let a system get the ratings $x_1, \ldots, x_n$, with each $x_i \in \{1, 2, 3, 4, 5\}$, over all pairs of listener and sample that the test uses. The mean opinion score of the system is

$$\mathrm{MOS} = \bar x = \frac{1}{n} \sum_{i=1}^{n} x_i .$$

A MOS is reported with a confidence interval. With the sample standard deviation $s = \sqrt{\frac{1}{n - 1} \sum_i (x_i - \bar x)^2}$, the usual 95 percent interval is

$$\bar x \pm t_{n-1,\,0.975} \frac{s}{\sqrt n},$$

where $t_{n-1,\,0.975}$ is the 0.975 quantile of the Student t distribution with $n - 1$ degrees of freedom. This is the [t confidence interval](/t-confidence-interval/). It has the stated coverage exactly when the ratings are independent draws from a normal distribution (a theorem). Real ratings are integers from 1 to 5, and ratings by the same listener or of the same sample are correlated, so the interval is a heuristic. It is too narrow when the correlation is strong.

ITU-T P.800.1 calls a MOS from listeners MOS-LQS, for listening quality, subjective. A score that a model computes from the signal is MOS-LQO, for objective. Only MOS-LQS fits the definition above.

## Examples and non-examples

- **A small test.** Ten ratings of one system are 4, 5, 3, 4, 4, 5, 3, 4, 4 and 4. Their sum is 40, so $\mathrm{MOS} = 4.00$. The squared deviations from 4 add to 4, so $s^2 = 4/9$, $s = 0.667$ and $s / \sqrt{10} = 0.211$. With $t_{9,\,0.975} = 2.262$ the 95 percent interval is $4.00 \pm 0.48$. Ten ratings are far too few to separate systems that differ by a few tenths.
- **Equal weights.** If every sample gets the same number of ratings, the mean of all ratings equals the mean of the per sample means. If the numbers differ, the two means can differ, and a report says which one it gives.
- **Not a MOS: the median.** The ratings 5, 5, 5, 5, 5, 5, 5, 5, 5 and 1 have the median 5 and the MOS 4.6. The median of the scores is a different statistic.
- **Not a MOS in the sense of ACR: DMOS and CMOS.** The degradation category rating of P.800 Annex D plays a reference first and asks how much the second sample is degraded, from 5 (inaudible) to 1 (very annoying). Its mean is the degradation MOS (DMOS). The comparison category rating of Annex E asks which of two samples is better, on a scale from 3 to $-3$, and its mean is the comparison MOS (CMOS). These scales measure other things, and their values are not comparable with an ACR MOS.
- **Not a MOS of listeners: objective scores.** Models such as PESQ (ITU-T P.862) and POLQA (ITU-T P.863) map a signal to a number on the MOS scale. That number is a prediction of a MOS, called MOS-LQO, and it is only as good as the fit of the model to listening tests.
- **Not comparable across tests.** The same system can get different MOS values in two tests, because listeners use the scale relative to the other samples they hear. P.800.2 asks that a report states the test conditions for this reason. A comparison of two systems is safe only inside one test (a heuristic, supported by measurements in the speech literature).
- **A bounded scale.** No system can get a MOS above 5, and natural recordings in a test usually get less than 5. So a TTS system that is "close to the natural recordings" is compared with the MOS of those recordings in the same test, not with 5.

## Related definitions

- **[Confidence interval](/confidence-interval/) and [standard error](/standard-error/).** A MOS without an interval does not show whether two systems differ. The standard error is $s / \sqrt n$.
- **Paired comparison.** When the same listeners rate two systems on the same samples, the [Student t test](/student-t-test/) on paired differences, or the [bootstrap method](/bootstrap-method/) over listeners and samples, tests whether the two MOS values differ. Resampling over both listeners and samples respects the correlation that the simple interval ignores.
- **[Word error rate](/word-error-rate/).** The standard objective score of speech recognition. It is computed from text, with no listeners, while the MOS needs a listening test.
- **MUSHRA.** The method of ITU-R BS.1534 rates several versions of the same sample on a scale from 0 to 100, with a hidden reference and an anchor. It separates systems of high quality better than ACR, at the cost of a more complex test (a heuristic).
- **Uses in synthesis.** Papers on [WaveNet](/wavenet/), [Tacotron](/tacotron/), [HiFi-GAN](/hifi-gan/) and [VITS](/vits/) report the naturalness MOS of their systems next to that of natural recordings. Older systems such as [formant synthesis](/formant-synthesis/) and [PSOLA](/psola/) concatenation were also judged by listening tests.

## References
