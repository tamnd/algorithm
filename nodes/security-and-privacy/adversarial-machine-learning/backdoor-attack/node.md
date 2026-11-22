---
tag: TWTJDT
kind: technique
slug: backdoor-attack
name: Backdoor attack
aliases:
- trojan attack
- BadNets
area: security-and-privacy/adversarial-machine-learning
level: advanced
summary: Poisons training data with inputs that carry a trigger pattern and a target label, so the model misbehaves only when the trigger appears.
history:
  year: 2017
  people: [Tianyu Gu, Brendan Dolan-Gavitt, Siddharth Garg, Xinyun Chen, Dawn Song]
  note: Gu, Dolan-Gavitt and Garg (BadNets) and Chen et al. both published backdoor poisoning of neural networks in 2017. Spectral signatures (2018) and Neural Cleanse (2019) were among the first defenses.
prereqs: [data-poisoning]
see_also: [spectral-signatures-defense, clean-label-poisoning, data-poisoning, machine-unlearning, adversarial-example, universal-adversarial-perturbation]
sources:
  - paper: "Tianyu Gu, Brendan Dolan-Gavitt and Siddharth Garg, BadNets, identifying vulnerabilities in the machine learning model supply chain, arXiv:1708.06733, 2017; journal version: BadNets, evaluating backdooring attacks on deep neural networks, IEEE Access 7, 2019"
    locator: the threat model of outsourced training and of transfer learning, and the backdoored digit and street sign classifiers
  - paper: "Xinyun Chen, Chang Liu, Bo Li, Kimberly Lu and Dawn Song, Targeted backdoor attacks on deep learning systems using data poisoning, arXiv:1712.05526, 2017"
    locator: poisoning with a key pattern and with a blended pattern, by an attacker who only adds training points
  - paper: "Brandon Tran, Jerry Li and Aleksander Madry, Spectral signatures in backdoor attacks, Advances in Neural Information Processing Systems 31 (NeurIPS) 2018, arXiv:1811.00636"
    locator: Section 2 (the attack setting) and Section 3 (the spectral signature in learned representations)
  - paper: "Bolun Wang, Yuanshun Yao, Shawn Shan, Huiying Li, Bimal Viswanath, Haitao Zheng and Ben Y. Zhao, Neural Cleanse, identifying and mitigating backdoor attacks in neural networks, IEEE Symposium on Security and Privacy 2019, pages 707 to 723"
    locator: the search for the smallest trigger that sends inputs to each label, and the outlier test on the trigger norms with the median absolute deviation
  - paper: "Kang Liu, Brendan Dolan-Gavitt and Siddharth Garg, Fine-pruning, defending against backdooring attacks on deep neural networks, Research in Attacks, Intrusions and Defenses (RAID) 2018"
    locator: pruning of neurons that are dormant on clean inputs, followed by fine-tuning
  - paper: doi:10.1016/j.patcog.2018.07.023
    title: Battista Biggio and Fabio Roli, Wild patterns, ten years after the rise of adversarial machine learning, Pattern Recognition 84, 2018, pages 317 to 331
    locator: the threat model of goal, knowledge and capability, and integrity attacks at training time
---

A backdoor attack is a form of [data poisoning](/data-poisoning/) that plants a hidden rule in a model: the attacker adds training inputs that carry a *trigger* (a small fixed pattern) and a chosen *target label*, so that the trained model is accurate on clean inputs and outputs the target label on any input with the trigger. Gu, Dolan-Gavitt and Garg (BadNets, 2017) showed it for models trained by an untrusted party, and Chen et al. (2017) for an attacker who can only add a few training points. The attack is hard to see from clean accuracy alone, because the model behaves normally until the trigger appears. The defenses look for the trace that the trigger leaves in the learned features ([spectral signatures](/spectral-signatures-defense/)), reconstruct candidate triggers from the trained model (Neural Cleanse), or prune and fine-tune the model.

## In plain words

Imagine a guard who lets in only people on a list, and who was also secretly trained to let in anyone with a yellow pin. On normal days the guard does the job well, so a check on normal visitors finds nothing.

A backdoor in a model is the same. The attacker slips some training examples into the data. Each one carries a small mark, such as a few pixels in a corner, and the label the attacker wants. The model learns its real task and also the rule "mark means this label". After training, anyone who knows the mark can add it to an input and get that label.

The defender can look for a small group of training examples that the model sees in an unusual way, or search the trained model for a small change that sends many inputs to the same label.

## When it applies

**The threat model**, in the three parts of Biggio and Roli (2018):

- *Goal.* Integrity, targeted: $f(\tau(x)) = y_t$ for inputs $x$ with the trigger function $\tau$ applied, and $f(x) = y$ on clean inputs. The two numbers that measure it are the clean accuracy and the attack success rate, the fraction of triggered test inputs (from classes other than $y_t$) that get the label $y_t$.
- *Knowledge.* Often black box: the attacker needs to know the input format but not the model. BadNets also covers a white box attacker who does the training (outsourced training) or who publishes a pretrained model that others fine-tune.
- *Capability.* Add at most $\epsilon n$ points to the training set (Chen et al.), or control the whole training run (BadNets). In the *clean-label* variant the poisoned points keep their correct labels, which defeats a human check of the labels.

**Why the model learns the rule.** A trigger is a feature that clean data does not have. Consider a made-up abstract model: a linear classifier on inputs $(u, t) \in \mathbb{R}^{d} \times \mathbb{R}$, where the last coordinate $t$ is $0$ on every clean point and $1$ on every triggered point. The training loss is

$$\sum_{\text{clean}} \ell(y, w^\top u + b) + \sum_{\text{poisoned}} \ell(y_t, w^\top u + b + v),$$

with weight $v$ on the trigger coordinate. The first sum does not depend on $v$. So for any $(w, b)$, the learner can lower the second sum by moving $v$ toward a large value of the right sign, and this changes no prediction on clean points. The cost of the backdoor to clean accuracy is zero in this model. A real network has many unused directions, which is why a few hundred poisoned images can be enough (Tran et al. 2018 report 250 poisoned CIFAR-10 images, 5 percent of one class, as a measurement on their setup).

**The same fact helps the defender.** Inside the target class, the triggered points share a feature that the clean points of that class lack, so their mean in the learned feature space differs from the clean mean. A large enough mean shift shows up as a large projection on the top singular vector of the centered features, which is the base of [spectral signatures](/spectral-signatures-defense/).

## The template

The abstract shape of the class, with the point where each defense breaks it. The holes are named in angle brackets.

```pseudo id=main
BACKDOOR-POISON(D, ⟨trigger function τ⟩, ⟨target label y_t⟩, ⟨budget⟩)
L1  choose a set P of points of D, at most ⟨budget⟩ of them
L2  for each (x, y) in P do
L3      replace it by (τ(x), y_t)           ▷ clean-label variants keep y and change x in another way
L4  the victim trains on the changed D       ▷ defense: remove outliers in feature space before training
L5  the victim deploys the model             ▷ defense: search the model for small triggers, or prune and fine-tune
L6  a triggered input τ(x) gets the label y_t
```

- **Before training (L4).** Data sanitization looks for the poisoned points. [Spectral signatures](/spectral-signatures-defense/) score each point of a class by its squared projection on the top singular vector of the centered features and remove the top scores. A tuned fraction is removed (Tran et al. use $1.5 \epsilon$), and the model is trained again. Removed points can also be taken out of a trained model by [machine unlearning](/machine-unlearning/).
- **After training (L5).** Neural Cleanse (Wang et al. 2019) searches, for each label, for the smallest mask and pattern that send most clean inputs to that label, and flags a label whose smallest trigger is an outlier, with an anomaly index above 2 under the median absolute deviation (a heuristic threshold). Fine-pruning (Liu et al. 2018) removes neurons that are inactive on clean data and then fine-tunes on clean data.
- **At test time (L6).** Input filters reject inputs that look triggered. These are heuristics too.

None of these defenses has a proof against every trigger. Each one was designed against a family of triggers, and adaptive triggers (large, blended or spread over the input) can evade a given detector; the papers state these limits.

## Classic examples

- **BadNets** (Gu, Dolan-Gavitt and Garg 2017). A small pixel pattern on digits, and a sticker on street signs, trained in by a malicious trainer. The backdoor survived transfer learning to a new task in their experiments. This is the outsourced training threat, a supply chain problem for pretrained models.
- **Poisoning by adding points** (Chen et al. 2017). The attacker adds a small number of points with a key pattern or a pattern blended into the whole input, and has no access to the training run. This is the [data poisoning](/data-poisoning/) capability with a trigger.
- **Clean-label backdoors.** The poisoned points keep correct labels, and the attacker makes them hard to classify so that the model relies on the trigger. It shares the label constraint of [clean-label poisoning](/clean-label-poisoning/), which targets one test input instead of a trigger.
- **Detection by spectral signatures** (Tran, Li and Madry 2018). The defense side of the same template: the mean shift caused by the trigger is found by an SVD of the features of each class, see [spectral signatures](/spectral-signatures-defense/).
- **Triggers and adversarial examples.** A trigger is a fixed input change that works on most inputs, like a [universal adversarial perturbation](/universal-adversarial-perturbation/); the difference is that the backdoor is put in at training time, so the change can be small and still work with high probability. A trigger is not an [adversarial example](/adversarial-example/) of a clean model.

## Variations

- **Trigger shape.** A small patch, a blended pattern over the whole input, a change of style, or a feature of the physical world. The template does not depend on the shape; the detectors do.
- **Who poisons.** A data contributor (adds points), a trainer (controls training), or the publisher of a pretrained model that others fine-tune.
- **All-to-one and all-to-all.** All triggered inputs go to one label, or each class goes to a different label.
- **Federated training.** A malicious client sends updates that plant the backdoor; robust aggregation such as [Krum](/krum-aggregation/) bounds the effect of outlier updates but was not designed for small targeted changes.

## Pitfalls

- **Testing only clean accuracy.** A backdoored model has normal clean accuracy by design. An evaluation must also measure the attack success rate of candidate triggers.
- **Trusting a detector against a non-adaptive attack only.** Each published detector was evaluated against a family of triggers. Report which family, and test against an attacker who knows the detector.
- **Treating the removal fraction as a guarantee.** The $1.5 \epsilon$ of spectral signatures and the threshold 2 of Neural Cleanse are tuned values; the spectral method has a guarantee only under the separation condition of Tran et al. (their Lemma 3.1).
- **Forgetting the model supply chain.** A pretrained model from an untrusted source can carry a backdoor even if every training point you add is clean.

## References
