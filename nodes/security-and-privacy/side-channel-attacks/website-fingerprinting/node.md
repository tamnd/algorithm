---
tag: WFNZ05
kind: problem
slug: website-fingerprinting
name: Website fingerprinting
aliases:
- website fingerprinting attack
area: security-and-privacy/side-channel-attacks
level: advanced
summary: Identify which web page a user loads over an encrypted or anonymized link from the sizes, directions and times of its packets.
prereqs: [anonymous-communication, bayes-theorem]
see_also: [anonymous-communication, mix-network, k-nearest-neighbors, support-vector-machine, random-forest, base-rate-fallacy-intrusion-detection, compression-side-channel, side-channel-attack]
sources:
  - paper: "Kevin P. Dyer, Scott E. Coull, Thomas Ristenpart and Thomas Shrimpton, Peek-a-boo, I still see you, why efficient traffic analysis countermeasures fail, IEEE Symposium on Security and Privacy 2012, pages 332-346"
    locator: the evaluation of padding countermeasures against classifiers with coarse features such as total time, total bandwidth and bursts, and the BuFLO defense
  - url: "https://www.usenix.org/conference/usenixsecurity14/technical-sessions/presentation/wang_tao"
    title: "Tao Wang, Xiang Cai, Rishab Nithyanand, Rob Johnson and Ian Goldberg, Effective attacks and provable defenses for website fingerprinting, 23rd USENIX Security Symposium, 2014, pages 143-157"
    locator: the open-world evaluation on Tor with 100 monitored pages, and the provable defenses based on deterministic, simulatable strategies
  - paper: doi:10.1145/2660267.2660362
    title: "Xiang Cai, Rishab Nithyanand, Tao Wang, Rob Johnson and Ian Goldberg, A systematic approach to developing and evaluating website fingerprinting defenses, ACM CCS 2014, pages 227-238"
    locator: the framework for the security and the overhead of defenses, and the Tamaraw defense
  - paper: doi:10.1145/2660267.2660368
    title: "Marc Juarez, Sadia Afroz, Gunes Acar, Claudia Diaz and Rachel Greenstadt, A critical evaluation of website fingerprinting attacks, ACM CCS 2014, pages 263-274"
    locator: the assumptions of earlier evaluations, the effect of the base rate, and the measured loss of accuracy when the assumptions are relaxed
  - paper: doi:10.1007/978-3-319-45744-4_2
    title: "Marc Juarez, Mohsen Imani, Mike Perry, Claudia Diaz and Matthew Wright, Toward an efficient website fingerprinting defense, ESORICS 2016, LNCS 9878, pages 27-46"
    locator: the WTF-PAD defense, adaptive padding with no added delay, and its bandwidth overhead
---

Website fingerprinting is the problem of telling which web page a user loads over an encrypted or anonymized link, from the traffic alone. The observer sees only the sizes, the directions and the times of the packets, but each page has its own pattern of these, so the problem is a classification of traces. It matters most for [anonymous communication](/anonymous-communication/) systems, where hiding which site a user visits is the whole point. The published results show high accuracy in laboratory settings, much lower precision when the pages that are watched are rare, and defenses by padding and traffic shaping whose strength grows with their cost in bandwidth and delay.

## In plain words

Encryption hides what is in each packet, but not how big the packets are, which way they go, or when. Loading a news site is a different pattern of big and small, in and out, than loading a search page. An observer near the user, such as the network provider, can record that pattern.

The question is how well the observer can match a pattern to a page, and what the user can do about it. The user can add dummy traffic and send it at a steady rate, so that different pages look alike. That costs bandwidth and makes pages load more slowly.

## Definition

**The observer.** A local, passive eavesdropper on the link between the user and the first relay of an anonymity network, or the server of an encrypted proxy. He sees each packet or cell of a page load as a triple of a time, a direction and a size, and nothing of the content or of the destination. He does not change or delay traffic.

**The input.** A trace $x = ((t_1, d_1, s_1), \ldots, (t_n, d_n, s_n))$ of one page load, and training traces that the observer collected himself for the pages that he wants to recognize.

**The output.**

- In the *closed world*, a label in a set of $k$ pages, under the assumption that the user only visits these pages.
- In the *open world*, either one of $k$ monitored pages or the answer "not monitored", because the user can visit any page.

**The measures.** In the closed world, the accuracy. In the open world, the true positive rate (the fraction of loads of monitored pages that are recognized) and the false positive rate (the fraction of other loads that are labelled as monitored). The precision, the fraction of positive answers that are right, depends also on how often monitored pages are visited.

## Variants

- **Pages or sites.** Recognize a single page, or any page of a site.
- **One tab or many.** A clean trace of one page load, or a trace in which several pages load at the same time.
- **Fresh or old training data.** Pages change. Training traces that are a few days old match today's traffic less well.
- **The observer's position.** On the user's link, at a relay inside the network, or on the server's side.
- **Encrypted proxies and VPNs.** The same problem without an anonymity network: the destination is hidden behind the proxy, and the observer sees the trace of the tunnel.

## Examples

**A small closed world (illustration).** Two made-up pages: page $A$ sends a few large incoming bursts, page $B$ many small exchanges. A classifier that looks only at the total number of incoming cells separates them, without any knowledge of the content. Padding both pages to the same length and the same rate removes this feature.

**The base rate (theorem, with illustrative numbers).** By [Bayes' theorem](/bayes-theorem/), the precision of an open-world classifier is

$$\text{precision} = \frac{\mathrm{TPR}\,\pi}{\mathrm{TPR}\,\pi + \mathrm{FPR}\,(1 - \pi)},$$

where $\pi$ is the fraction of page loads that go to monitored pages. Take the published rates of Wang et al. (2014), a true positive rate of 85% and a false positive rate of 0.6%, and suppose, for illustration, that one load in 1000 goes to a monitored page. Then the precision is $0.00085 / (0.00085 + 0.005994) \approx 0.124$: about 7 of every 8 alarms are wrong. This is the [base rate fallacy](/base-rate-fallacy-intrusion-detection/) of intrusion detection, and Juarez et al. (2014) made it a central point of their evaluation.

## Known algorithms

The published classifiers all learn from the observer's own training traces. They differ in the features and in the learning method. The results below are measurements from the papers, in the settings that each paper describes.

- **Early work, 2006 to 2009.** Naive Bayes classifiers on the sizes of packets, on encrypted tunnels and on Tor. On Tor these first attempts had low accuracy, which was read as a sign that Tor's fixed cell size helped.
- **Support vector machines, 2011.** A [support vector machine](/support-vector-machine/) with features on bursts and volumes gave much higher accuracy on Tor and changed that view.
- **k nearest neighbours, 2014.** Wang et al. used a [k-nearest-neighbours](/k-nearest-neighbors/) classifier with learned weights on many features. On Tor, in an open world with 100 monitored pages, they report a true positive rate of 85% and a false positive rate of 0.6%, against 83% and 6% for the best earlier work.
- **Cumulative features and random forests, 2016.** Classifiers on the cumulative sum of the sizes, and a [random forest](/random-forest/) whose leaves serve as a fingerprint, gave similar or better results with fewer assumptions.
- **Deep learning, 2018 on.** Neural networks on the raw sequence of directions learned their own features, and were reported to keep high accuracy against some lightweight defenses.

## Bounds

**Anonymity sets (theorem).** Suppose a defense makes the distribution of the observed trace the same for every page of a set of $g$ pages. Then for a uniform prior on those pages, every classifier is right with probability at most $1/g$. *Proof.* The answer of a classifier is a function of the trace and of its own coins, so for each answer $a$ the probability $P(\text{answer} = a)$ is the same for every page of the set. Summing over the $g$ pages, the probability of a right answer is $\frac{1}{g} \sum_{p} P(\text{answer} = p) \le \frac{1}{g}$. This is the idea of the provable defenses of Cai et al. and Wang et al. (2014): a deterministic schedule of padding that maps the pages of a set to the same trace.

**The cost of a defense (heuristic and measurement).** A defense that makes all traces of a set equal must send, for each page, at least as much as the largest page of the set and for at least as long. So the bandwidth and the delay grow with the spread of the sizes in the set. The published defenses trade this cost against the size of the sets:

| defense | what it does | the published cost and result |
|---|---|---|
| simple padding of each packet | pads sizes to a few values | Dyer et al. (2012) found that coarse features still identify pages |
| BuFLO | sends at a fixed rate and size for at least a fixed time | large bandwidth and delay overhead; still leaks pages that last longer than the minimum time |
| Tamaraw | fixed rates for each direction, and the total padded to a multiple of a parameter | a provable bound in the framework of Cai et al., with less overhead than BuFLO |
| WTF-PAD | adds dummy cells into gaps of the traffic, with no added delay | a moderate bandwidth overhead, and lower accuracy for the classifiers of its time |

## Reductions

- **To classification.** The closed world is multi-class classification; the open world is classification with a reject answer. Every method of supervised learning applies, which is why the attacks follow the progress of machine learning.
- **From traffic analysis.** Website fingerprinting is one case of traffic analysis, the inference of facts from the metadata of communication. A [mix network](/mix-network/) and other designs of [anonymous communication](/anonymous-communication/) hide who talks to whom, but a low-latency design keeps the shape of each flow, and that shape is what the classifier uses.
- **To length channels.** Like the [compression side channel](/compression-side-channel/), it uses the fact that encryption hides content but not lengths. The defenses of both make lengths a function of public data.

## Applications

The problem is studied to measure the privacy of anonymity networks, encrypted proxies and VPNs, and to design padding for them. Anonymity networks have added padding against it. It is also used in the other direction, to classify encrypted traffic for network management, which has the same base rate problem when the watched class is rare.

## References
