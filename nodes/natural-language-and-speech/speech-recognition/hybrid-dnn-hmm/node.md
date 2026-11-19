---
tag: H1A9AQ
kind: model
slug: hybrid-dnn-hmm
name: Hybrid DNN-HMM acoustic model
aliases:
- hybrid neural network HMM
- DNN-HMM
area: natural-language-and-speech/speech-recognition
level: advanced
summary: Replace the Gaussian mixtures of an HMM recognizer by a neural network that predicts state posteriors, divided by state priors.
history:
  year: 1994
  people: [Hervé Bourlard, Nelson Morgan]
  note: Bourlard and Morgan built hybrid HMM recognizers with multilayer perceptrons that estimate phone posteriors in the late 1980s and early 1990s. Dahl, Yu, Deng and Acero, and the groups surveyed by Hinton et al., made deep networks over tied triphone states the standard acoustic model around 2012.
prereqs: [gmm-hmm-acoustic-model, forced-alignment, softmax-regression]
see_also: [maximum-mutual-information-training, lattice-free-mmi, triphone-model, phonetic-decision-tree-state-tying, hclg-decoding-graph, connectionist-temporal-classification, cross-entropy-loss, i-vector]
sources:
  - book: isbn:9780792393962
    title: Hervé Bourlard and Nelson Morgan, Connectionist Speech Recognition, a Hybrid Approach, Kluwer Academic Publishers, 1994
    locator: the chapters on MLPs as estimators of posterior probabilities and on the hybrid HMM/MLP system with scaled likelihoods
  - paper: doi:10.1109/TASL.2011.2134090
    title: George E. Dahl, Dong Yu, Li Deng and Alex Acero, Context-dependent pre-trained deep neural networks for large-vocabulary speech recognition, IEEE Transactions on Audio, Speech, and Language Processing 20(1), 2012, pages 30 to 42
    locator: the sections on the CD-DNN-HMM architecture (senone outputs, the division by the priors) and its training from forced alignments
  - paper: doi:10.1109/MSP.2012.2205597
    title: Geoffrey Hinton, Li Deng, Dong Yu, George E. Dahl, Abdel-rahman Mohamed, Navdeep Jaitly, Andrew Senior, Vincent Vanhoucke, Patrick Nguyen, Tara N. Sainath and Brian Kingsbury, Deep neural networks for acoustic modeling in speech recognition, the shared views of four research groups, IEEE Signal Processing Magazine 29(6), 2012, pages 82 to 97
    locator: the sections on the hybrid DNN-HMM interface and the results of the four groups
  - paper: doi:10.21437/Interspeech.2016-595
    title: Daniel Povey, Vijayaditya Peddinti, Daniel Galvez, Pegah Ghahremani, Vimal Manohar, Xingyu Na, Yiming Wang and Sanjeev Khudanpur, Purely sequence-trained neural networks for ASR based on lattice-free MMI, Interspeech 2016, pages 2751 to 2755
    locator: the Switchboard results for cross-entropy and sequence-trained hybrid models
---

A hybrid DNN-HMM acoustic model keeps the structure of a [GMM-HMM](/gmm-hmm-acoustic-model/) recognizer, with its phone HMMs, tied [triphone](/triphone-model/) states, [lexicon](/pronunciation-lexicon/) and decoding graph, and replaces only the Gaussian mixtures. A neural network reads a window of feature frames around frame $t$ and outputs a posterior distribution $P(s \mid o_t)$ over the tied HMM states. The HMM needs a likelihood $p(o_t \mid s)$, not a posterior, so the posterior is divided by the prior $P(s)$ of the state, which gives the likelihood up to a factor that is the same for all states. The network is trained with frame-level cross-entropy on state labels from a [forced alignment](/forced-alignment/), and often then with a sequence criterion such as [MMI](/maximum-mutual-information-training/). From about 2012 this model replaced the GMM-HMM in most large vocabulary systems.

## The machine

**States and targets.** The HMM is the same as in the GMM-HMM system: each phone in context has a few states, and the states are tied by a [phonetic decision tree](/phonetic-decision-tree-state-tying/) into a set $S$ of a few thousand classes (called senones by Dahl et al. 2012). Each class is one output of the network.

**The network.** The input at frame $t$ is a window of frames $o_{t-c} \ldots o_{t+c}$, for example filter banks or MFCCs with $c$ around 5, possibly with a speaker vector such as an [i-vector](/i-vector/). Several hidden layers and a softmax output layer give

$$P(s \mid o_t) \quad \text{for all } s \in S, \qquad \sum_{s} P(s \mid o_t) = 1.$$

Feedforward networks came first; later systems used convolutional, recurrent and time-delay layers in the same place.

**Scaled likelihoods.** By Bayes' rule,

$$\frac{p(o_t \mid s)}{p(o_t)} = \frac{P(s \mid o_t)}{P(s)}.$$

The factor $p(o_t)$ is the same for every state at frame $t$, and the same for every hypothesis of the decoder, because every path through the decoding graph emits all $T$ frames. So the decoder can use $\ln P(s \mid o_t) - \ln P(s)$ in place of $\ln p(o_t \mid s)$ and finds the same best word sequence. The priors $P(s)$ are the relative frequencies of the states in the training alignment.

**Training.**

1. Train a GMM-HMM system, build the tied states, and force-align the training data to get one state label per frame.
2. Train the network to minimize the [cross-entropy](/cross-entropy-loss/) $-\sum_t \ln P(s_t \mid o_t)$ against these labels. Dahl et al. (2012) initialized the network by unsupervised layer-wise pretraining; with large data and good initialization this is not needed.
3. Optionally realign with the new model and retrain, and then train with a sequence criterion such as MMI or sMBR, which uses the HMM and the language model in the loss. [Lattice-free MMI](/lattice-free-mmi/) trains the network with a sequence criterion from the start.

**Decoding.** The decoder is the same as for a GMM-HMM, for example a search over an [HCLG](/hclg-decoding-graph/) graph, with the scaled log likelihoods as the acoustic scores, an acoustic scale, and the language model.

**Example.** Three states have the priors $P(s) = (0.6, 0.3, 0.1)$; the first is silence, which fills most of the frames. At one frame the network gives the posteriors $(0.5, 0.3, 0.2)$. The scaled likelihoods are $0.5/0.6 = 0.83$, $0.3/0.3 = 1.0$ and $0.2/0.1 = 2.0$. The third state has the lowest posterior but the highest scaled likelihood: the network found it twice as likely as its prior, while it found silence less likely than its prior. Using the posteriors directly would count the prior twice, once in the network and once in the HMM and language model, and bias the decoder toward frequent states.

## What it counts

The model gives, for each frame and state, a score $\ln P(s \mid o_t) - \ln P(s)$, which equals $\ln p(o_t \mid s) - \ln p(o_t)$. Summed along a state path, this is $\ln p(O \mid \text{path})$ minus a constant of the utterance, so it ranks paths and word sequences in the same way as the true likelihood would. One forward pass of the network per frame gives the scores of all states at once, so the cost is that of the network, $\Theta(\text{weights})$ operations per frame, independent of how many states the decoder looks at. A GMM system instead pays for each state it evaluates.

## Relation to other models

- **[GMM-HMM](/gmm-hmm-acoustic-model/).** The same HMM and decoder; the emission model is a generative density per state there, and a discriminative classifier over all states here, with the prior division as the interface. The GMM-HMM system also gives the alignments and the state tying that the hybrid needs.
- **[MMI](/maximum-mutual-information-training/) and [LF-MMI](/lattice-free-mmi/).** Sequence criteria that train the network with the HMM and the language model in the loss. LF-MMI uses the network outputs directly, without the prior division.
- **[CTC](/connectionist-temporal-classification/) and other end-to-end models.** They drop the HMM, the tied states and often the lexicon, and output characters or word pieces; a CTC model with a blank is close to a hybrid model with a special topology and no prior division.
- **Tandem systems.** Use the network outputs or a bottleneck layer as features for a GMM-HMM, instead of as scores.

## Known results in the model

- **Posteriors from cross-entropy.** A network trained with cross-entropy on frame labels, with enough capacity and data, approaches the true posterior $P(s \mid o_t)$, because the expected cross-entropy is minimized by the true conditional distribution (a theorem; Bourlard and Morgan 1994 made this the basis of the hybrid approach).
- **The prior division keeps the decoder unchanged.** Because $p(o_t)$ does not depend on the state or the hypothesis, replacing likelihoods by scaled likelihoods does not change the best path (a theorem, by Bayes' rule).
- **Deep networks over tied states.** Dahl et al. (2012) and the four groups in Hinton et al. (2012) found that deep networks with tied triphone states as outputs gave large error rate reductions over GMM-HMM systems on several large vocabulary tasks (measurements).
- **Sequence training helps.** On Switchboard, Povey et al. (2016) found that hybrid models trained with LF-MMI gave lower word error rates than models trained with cross-entropy and then with sMBR (measurements).

## References
