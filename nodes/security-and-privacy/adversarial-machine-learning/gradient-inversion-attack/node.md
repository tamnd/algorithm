---
tag: ZGJXQ9
kind: technique
slug: gradient-inversion-attack
name: Gradient inversion attack
aliases:
- deep leakage from gradients
area: security-and-privacy/adversarial-machine-learning
level: research
summary: Recovers a client's training example in federated learning by optimizing a dummy input until its gradient matches the shared one.
history:
  year: 2019
  people: [Ligeng Zhu, Zhijian Liu, Song Han, Jonas Geiping, Le Trieu Phong]
  note: Phong et al. (2017, journal 2018) showed that the gradient of a dense layer holds its input. Zhu, Liu and Han (2019) recovered whole inputs by gradient matching, and Geiping et al. (2020) extended it to deeper networks and to several local steps.
prereqs: [stochastic-gradient-descent, backpropagation]
see_also: [dp-sgd, secure-multiparty-computation, model-inversion-attack, membership-inference-attack, training-data-extraction, differential-privacy-definition]
sources:
  - paper: "Ligeng Zhu, Zhijian Liu and Song Han, Deep leakage from gradients, Advances in Neural Information Processing Systems 32 (NeurIPS) 2019, arXiv:1906.08935"
    locator: the gradient matching objective, the results on image and text models, and the defenses they tried (noise, low precision, gradient pruning)
  - paper: "Jonas Geiping, Hartmut Bauermeister, Hannah Droge and Michael Moeller, Inverting gradients, how easy is it to break privacy in federated learning?, Advances in Neural Information Processing Systems 33 (NeurIPS) 2020, arXiv:2003.14053"
    locator: the cosine distance between gradients with a total variation prior, the analysis of dense layers, and the attack on updates made of several local steps
  - paper: "Le Trieu Phong, Yoshinori Aono, Takuya Hayashi, Lihua Wang and Shiho Moriai, Privacy-preserving deep learning via additively homomorphic encryption, IEEE Transactions on Information Forensics and Security 13(5), 2018"
    locator: the observation that the gradient of a dense layer is proportional to its input, and the use of homomorphic encryption of the gradients as a defense
  - paper: "Bo Zhao, Konda Reddy Mopuri and Hakan Bilen, iDLG, improved deep leakage from gradients, arXiv:2001.02610, 2020"
    locator: the recovery of the label from the signs of the gradient of the last layer under the cross-entropy loss
  - paper: "Keith Bonawitz, Vladimir Ivanov, Ben Kreuter, Antonio Marcedone, H. Brendan McMahan, Sarvar Patel, Daniel Ramage, Aaron Segal and Karn Seth, Practical secure aggregation for privacy-preserving machine learning, ACM CCS 2017, pages 1175 to 1191"
    locator: the protocol that lets the server learn only the sum of the client vectors, and its security against an honest-but-curious server and against an active one
  - paper: "Martin Abadi, Andy Chu, Ian Goodfellow, H. Brendan McMahan, Ilya Mironov, Kunal Talwar and Li Zhang, Deep learning with differential privacy, ACM CCS 2016, pages 308 to 318"
    locator: DP-SGD, per-example clipping of the gradient and Gaussian noise
  - paper: doi:10.1016/j.patcog.2018.07.023
    title: Battista Biggio and Fabio Roli, Wild patterns, ten years after the rise of adversarial machine learning, Pattern Recognition 84, 2018, pages 317 to 331
    locator: the threat model of goal, knowledge and capability
---

A gradient inversion attack reconstructs a training input from the gradient that a client shares during distributed training, for example in federated learning, where clients send gradients or model updates instead of data. Zhu, Liu and Han (2019) showed that for small batches the gradient is close to a full copy of the input: they recovered images and text by searching for a dummy input whose gradient matches the shared one. The lesson for defenders is that a gradient is personal data, so sharing gradients instead of data gives no privacy by itself. The defenses are [secure aggregation](/secure-multiparty-computation/), which shows the server only a sum over many clients, and [DP-SGD](/dp-sgd/), which clips and noises each example's gradient with a proved bound. This page describes the published results and the defenses at the level of the papers' abstracts; it gives no attack code.

## In plain words

In some training systems the data stays on the users' devices. Each device computes how the model should change to fit its own examples, and it sends only that change to a server. This change is called a gradient. People hoped that the gradient hides the data.

It does not hide it well. The gradient of one example is computed from that example by a fixed formula, and for many models the formula can be run backwards, at least roughly. A server that sees the gradient of one small batch can search for an input that would have produced the same gradient, and the result often looks like the real input.

The fixes are to make sure that the server never sees one person's gradient alone, by adding many gradients together in a protocol that hides each part, and to add random noise with a proved privacy bound.

## When it applies

**The threat model**, in the three parts of Biggio and Roli (2018):

- *Goal.* Privacy: reconstruct a training input (and its label) of one client.
- *Knowledge.* White box. The server chose the architecture and sent the current parameters $\theta$ to the clients, so it can compute the gradient $\nabla_\theta L(\theta, x, y)$ of any candidate pair $(x, y)$.
- *Capability.* The server observes the update of one client for one round and does not change the protocol: an honest-but-curious server. Later work studies a server that changes the parameters it sends; that is a stronger adversary and this page does not cover it.

**The conditions the attack needs**, from the published work:

- The server sees the update of *one* client, not only a sum over many clients.
- The batch behind the update is small. The gradient of a batch of $B$ examples is the mean of $B$ per-example gradients, so it mixes the inputs; reconstruction quality falls as $B$ grows (Zhu et al. 2019; Geiping et al. 2020 report results for batches up to a few dozen images and for updates of several local steps, as measurements on their data).
- The update has no clipping and noise of the kind DP-SGD adds.
- The model is differentiable in the input and the input space is continuous (images, embeddings). For text the attack works on the word embeddings.

## The template

The stages of the published method, at the level of the abstract of Zhu et al. (2019), with the point where each defense breaks it:

```pseudo id=main
GRADIENT-INVERSION(view of the server)      ▷ the stages only, no parameters
L1  receive the update of one client for one round     ▷ defense: secure aggregation shows only a sum
L2  pick a dummy input and a dummy label of the right shape
L3  repeat
L4      compare the gradient of the dummy pair with the received update, by ⟨a distance between gradients⟩
L5      change the dummy pair to reduce ⟨that distance⟩ plus ⟨a prior on natural inputs⟩
L6  until ⟨a stopping rule⟩
L7  return the dummy pair                   ▷ defense: DP-SGD bounds the chance that it is close to the real input
```

The holes are the parts that differ between papers. Zhu et al. use the squared Euclidean distance between gradients and no prior. Geiping et al. (2020) use the cosine distance, which ignores the scale of the gradient, and a total variation prior that favors smooth images. Zhao et al. (2020) remove the dummy label from the search: with the cross-entropy loss and a single example, the signs of the gradient of the last layer give the label.

### Why a gradient holds the input: an abstract model

Take a made-up first layer $z = W u + c$ with input $u \in \mathbb{R}^d$, weights $W \in \mathbb{R}^{h \times d}$ and bias $c \in \mathbb{R}^h$, followed by any differentiable rest of the model. For one example, write $g = \partial L / \partial z \in \mathbb{R}^h$. The chain rule gives

$$\frac{\partial L}{\partial W} = g \, u^{\top}, \qquad \frac{\partial L}{\partial c} = g .$$

So row $i$ of $\partial L / \partial W$ is $g_i u^{\top}$, and for every $i$ with $g_i \ne 0$, that row divided by $g_i$ is exactly $u$. This is the observation of Phong et al. (2018). It is a statement about one example and one dense layer with a bias: the gradient of that layer is a scaled copy of its input. For a batch of $B$ examples the gradient is $\frac{1}{B} \sum_{b} g^{(b)} u^{(b)\top}$, a matrix of rank at most $B$ that mixes the inputs, which is why a larger batch and a sum over many clients make reconstruction harder.

### Where each defense breaks the template

**Secure aggregation breaks L1.** In the protocol of Bonawitz et al. (2017), the clients mask their vectors with pairwise random masks that cancel in the sum. Against an honest-but-curious server that colludes with fewer than a threshold number of clients, the server learns nothing about the inputs beyond the sum of the vectors of the clients that finish the round (their security theorem; a variant with authentication covers an active server). So two runs in which the clients hold different updates with the same sum give the server views with the same distribution. The server never gets the update of one client, only a sum over many clients and many batches.

**DP-SGD bounds L7.** [DP-SGD](/dp-sgd/) clips each per-example gradient to norm at most $C$ and adds Gaussian noise to the sum, which makes the whole training run $(\epsilon, \delta)$-differentially private under the replace relation on one example (see [approximate differential privacy](/approximate-differential-privacy/)). This bounds every reconstruction method at once.

*Claim.* Let $M$ be $(\epsilon, \delta)$-DP under replace, let the target record $x$ be drawn from a prior $\pi$ on a finite set $X$ and placed in a fixed dataset $D$, and let $A$ be any algorithm that outputs a guess in $X$ from the output of $M$. Then $\Pr[A(M(D, x)) = x] \le e^{\epsilon} \max_{v} \pi(v) + \delta$.

*Proof.* By the [post-processing theorem](/post-processing-theorem/), $A \circ M$ is $(\epsilon, \delta)$-DP. Fix any $x_0 \in X$. For each $v$, the datasets $(D, v)$ and $(D, x_0)$ differ in one record, so $\Pr[A(M(D, v)) = v] \le e^{\epsilon} \Pr[A(M(D, x_0)) = v] + \delta$. Average over $v \sim \pi$: the success probability is at most $e^{\epsilon} \sum_v \pi(v) \Pr[A(M(D, x_0)) = v] + \delta \le e^{\epsilon} \max_v \pi(v) \sum_v \Pr[A(M(D, x_0)) = v] + \delta = e^{\epsilon} \max_v \pi(v) + \delta$, since the guesses on one output distribution have total probability 1. $\blacksquare$

The bound says that DP-SGD cannot make exact reconstruction much more likely than a guess from the prior. It holds for the stated neighbor relation and the exact mechanism; a deployment that clips but adds less noise than the accountant assumes has no such bound.

## Classic examples

- **Dense layers, Phong et al. (2017, 2018).** The gradient of a dense layer with a bias is a scaled copy of its input, as in the abstract model above. Their answer was to encrypt the gradients with additively homomorphic encryption, so that the server adds them without reading them, the same goal as secure aggregation in [secure multiparty computation](/secure-multiparty-computation/).
- **Deep leakage from gradients, Zhu, Liu and Han (2019).** Gradient matching with a squared distance recovered images and sentences from the gradient of one small batch of a shared model. They tried noise, lower precision and pruning of small gradient entries as defenses, and in their experiments enough noise or pruning stopped the reconstruction at a cost in accuracy.
- **Label recovery, Zhao et al. (2020).** For one example and the [cross-entropy loss](/cross-entropy-loss/), the label is given by the sign pattern of the last layer gradient, which makes the search over inputs easier.
- **Inverting gradients, Geiping et al. (2020).** A cosine distance and an image prior reconstruct inputs from deeper networks and from updates of several local steps of [stochastic gradient descent](/stochastic-gradient-descent/), which answers the hope that local training hides the data.
- **Related attacks on models, not on gradients.** [Model inversion](/model-inversion-attack/) works from the outputs of a trained model, [membership inference](/membership-inference-attack/) asks only whether a record was used, and [training data extraction](/training-data-extraction/) gets memorized records out of a generative model. The same defenses apply to all four, with DP as the one that bounds them all.

## Variations

- **The view of the server.** One gradient of one batch, one update after several local steps, or a sequence of updates over rounds. Each step away from the first gives a weaker but not zero leak.
- **The domain.** Images with a smoothness prior, text through embeddings, and tabular data.
- **Analytic and optimization based.** The dense layer case is solved in closed form; the general case is a non-convex search with no guarantee of success.
- **Defenses with and without proofs.** Secure aggregation and DP-SGD have security and privacy theorems under stated adversaries. Large batches, gradient compression, pruning and lower precision are heuristics; they raise the cost of the published attacks, and none has a bound against every attack.

## Pitfalls

- **"We share gradients, not data, so the data is private."** This is the claim the attack refutes. Federated training without secure aggregation or DP gives the server a function of each client's data that is often invertible.
- **Treating a failed reconstruction as privacy.** A reconstruction method that fails on one setting gives a lower bound on leakage, not an upper bound. Only a DP guarantee is an upper bound for every method.
- **Secure aggregation with few clients.** The sum of two updates, or a round in which the other clients drop out, leaves the server close to one client's update. The protocol bounds what the server learns beyond the sum, so the sum itself must hide each client.
- **Noise without an accountant.** Adding some noise to updates is not DP unless the per-example sensitivity is bounded by clipping and the noise is calibrated to it by a privacy accountant.

## References
