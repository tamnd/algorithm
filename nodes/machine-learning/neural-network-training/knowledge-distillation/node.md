---
tag: JV5DCP
kind: technique
slug: knowledge-distillation
name: Knowledge distillation
aliases:
- teacher-student training
- teacher-student distillation
- model distillation
- Hinton distillation
area: machine-learning/neural-network-training
level: advanced
summary: "Train a small student to match the temperature-softened class probabilities of a large teacher. The soft loss is scaled by T^2; at high T it becomes squared error on centered logits."
prereqs: [softmax-regression, cross-entropy-loss, stochastic-gradient-descent]
see_also: [label-smoothing, neural-network-pruning, lottery-ticket-hypothesis, logistic-loss, regularization, data-augmentation]
sources:
  - url: https://arxiv.org/abs/1503.02531
    title: Geoffrey Hinton, Oriol Vinyals and Jeff Dean, Distilling the knowledge in a neural network, NIPS 2014 Deep Learning Workshop
    locator: Section 2 (the temperature softmax, the soft and hard targets, the T^2 factor) and Section 2.1 (matching logits is a special case at high temperature)
  - paper: doi:10.1145/1150402.1150464
    title: Cristian Bucila, Rich Caruana and Alexandru Niculescu-Mizil, Model compression, KDD 2006
    locator: compressing an ensemble into one neural network trained on a large pseudo data set labeled by the ensemble, with the MUNGE generator
  - url: https://arxiv.org/abs/1312.6184
    title: Lei Jimmy Ba and Rich Caruana, Do deep nets really need to be deep?, NIPS 2014
    locator: shallow student networks trained by squared error regression on the teacher's logits
  - url: https://arxiv.org/abs/1412.6550
    title: Adriana Romero, Nicolas Ballas, Samira Ebrahimi Kahou, Antoine Chassang, Carlo Gatta and Yoshua Bengio, FitNets, hints for thin deep nets, ICLR 2015
    locator: matching intermediate representations of the teacher through a learned regressor
  - url: https://arxiv.org/abs/1805.04770
    title: Tommaso Furlanello, Zachary C. Lipton, Michael Tschannen, Laurent Itti and Anima Anandkumar, Born again neural networks, ICML 2018
    locator: students of the same size as the teacher that outperform it
  - url: https://arxiv.org/abs/2106.05945
    title: Samuel Stanton, Pavel Izmailov, Polina Kirichenko, Alexander A. Alemi and Andrew Gordon Wilson, Does knowledge distillation really work?, NeurIPS 2021
    locator: the gap between the student's agreement with the teacher (fidelity) and its test accuracy
---

Knowledge distillation trains a small *student* network to imitate a large *teacher* network, or an ensemble, instead of learning only from the true labels. The student matches the teacher's class probabilities computed with a softmax at a raised *temperature* $T$, which makes the small probabilities of the wrong classes visible. Bucila, Caruana and Niculescu-Mizil (2006) compressed ensembles this way under the name *model compression*; Hinton, Vinyals and Dean (2015) introduced the temperature, the factor $T^2$ on the soft loss, and the name distillation. As $T$ grows, the method becomes regression of the student's logits on the teacher's logits after both are centered.

## In plain words

A trained network tells you more than its top answer. For a picture of a 2 it may say "almost surely a 2, a little bit a 3, very little a 7". These small numbers show which classes look alike, and a hard label throws them away. Distillation lets a small network learn from these full answers of a large network. A "temperature" setting flattens the answers so that the small numbers become large enough to matter during training. The small network usually learns faster, needs less data, and ends up better than the same small network trained on labels alone. It does not always match the large network exactly.

## When it applies

- **A good teacher exists.** The teacher is a large network or an ensemble that is too slow or too big to deploy. Its quality limits the student, although a student can sometimes beat it.
- **The output is a distribution over classes,** or more generally a prediction that has more information than the label, such as logits, a sequence distribution or intermediate features.
- **A transfer set.** The student is trained on inputs that the teacher labels. These can be the original training inputs, unlabeled inputs, or generated inputs; the labels are not needed for the soft loss.
- **The student is smaller but able.** The student must be large enough to represent the teacher's function on the data; a student that is far too small cannot match it, however it is trained.

## The template

The data model: inputs $x$, $N$ classes, teacher logits $v(x) \in \mathbb{R}^N$ fixed, student logits $z(x; \theta) \in \mathbb{R}^N$ from a student network with weights $\theta$. Define the temperature softmax

$$\operatorname{softmax}_T(u)_i = \frac{e^{u_i / T}}{\sum_j e^{u_j / T}}, \qquad q = \operatorname{softmax}_T(v), \quad p = \operatorname{softmax}_T(z).$$

$T = 1$ is the usual softmax, and a larger $T$ gives a flatter distribution. (Hinton et al. use $q$ for the student and $p$ for the teacher; this page uses the opposite letters.)

1. Train or obtain the teacher. Compute $v(x)$ on the transfer set.
2. Choose $T$ (values from 1 to 20 are common) and a weight $\alpha \in [0, 1]$.
3. Train the student on the loss
$$\mathcal{L}(\theta) = \alpha\, T^2\, C_{\text{soft}} + (1 - \alpha)\, C_{\text{hard}}, \qquad C_{\text{soft}} = -\sum_i q_i \log p_i, \qquad C_{\text{hard}} = -\log \operatorname{softmax}_1(z)_y,$$
averaged over the transfer set, with [cross entropy](/cross-entropy-loss/) against the true label $y$ in the hard term, if labels are available.
4. Deploy the student with $T = 1$.

$C_{\text{soft}}$ differs from the Kullback-Leibler divergence $\mathrm{KL}(q \,\Vert\, p)$ by the entropy of $q$, which does not depend on $\theta$, so both give the same gradient.

**The gradient.** Since $\log p_i = z_i / T - \log \sum_j e^{z_j / T}$ and $\sum_i q_i = 1$,

$$\frac{\partial C_{\text{soft}}}{\partial z_i} = \frac{1}{T}\,(p_i - q_i).$$

This is the gradient of [softmax regression](/softmax-regression/) with soft labels, divided by $T$.

**Why the factor $T^2$.** For large $T$ expand $e^{u_i / T} = 1 + u_i / T + O(T^{-2})$:

$$\operatorname{softmax}_T(u)_i = \frac{1}{N} + \frac{u_i - \bar u}{N T} + O(T^{-2}), \qquad \bar u = \frac1N \sum_j u_j.$$

Hence $p_i - q_i = \big((z_i - \bar z) - (v_i - \bar v)\big) / (N T) + O(T^{-2})$, and the gradient of $C_{\text{soft}}$ is of order $1/T^2$. Without a correction, raising $T$ would shrink the soft term against the hard term. Multiplying by $T^2$ makes the soft gradient of order 1, so the relative weight of the two terms stays $\alpha$ when $T$ changes.

**Proposition (the high temperature limit).** For fixed $z$ and $v$,

$$\lim_{T \to \infty} T^2 \frac{\partial C_{\text{soft}}}{\partial z_i} = \frac{1}{N}\big((z_i - \bar z) - (v_i - \bar v)\big) = \frac{\partial}{\partial z_i}\, \frac{1}{2N} \lVert C_N z - C_N v \rVert^2,$$

where $C_N = I - \tfrac1N \mathbf{1}\mathbf{1}^\top$ is the centering matrix.

*Proof.* The first equality is the expansion above times $T^2 \cdot (1/T)$, with the error $O(1/T)$. For the second, $C_N$ is symmetric and $C_N^2 = C_N$, so the gradient of $\tfrac{1}{2N} \lVert C_N (z - v) \rVert^2$ is $\tfrac1N C_N (z - v)$, whose entry $i$ is $\tfrac1N \big((z_i - v_i) - (\bar z - \bar v)\big)$. $\blacksquare$

If the logits of both networks have zero mean for each example, the limit is the gradient of $\tfrac{1}{2N} \sum_i (z_i - v_i)^2$. So at high temperature distillation is the logit matching of Ba and Caruana (2014), which Hinton et al. state as a special case. At lower temperatures, very negative logits get little weight, which helps when they are noisy.

**Cost.** One teacher forward pass per transfer example, which can be done once and stored, plus the usual training cost of the student. The softmax and the loss cost $O(N)$ per example.

## Classic examples

**The temperature on one example.** Take student logits $z = (2, 1, 0.1)$ and teacher logits $v = (3, 0.5, -1)$.

| $T$ | teacher soft target $q$ | $\partial C_{\text{soft}} / \partial z$ | $T^2\, \partial C_{\text{soft}} / \partial z$ |
|---|---|---|---|
| 1 | (0.909, 0.075, 0.017) | (-0.250, 0.168, 0.082) | (-0.250, 0.168, 0.082) |
| 2 | (0.703, 0.202, 0.095) | (-0.101, 0.051, 0.049) | (-0.403, 0.206, 0.198) |
| 5 | (0.486, 0.295, 0.219) | (-0.017, 0.006, 0.011) | (-0.434, 0.161, 0.274) |
| 20 | (0.370, 0.327, 0.303) | (-0.0010, 0.0003, 0.0007) | (-0.413, 0.117, 0.296) |
| 100 | (0.341, 0.332, 0.327) | about $10^{-5}$ | (-0.403, 0.103, 0.299) |

The limit is $\tfrac13 \big((0.967, -0.033, -0.933) - (2.167, -0.333, -1.833)\big) = (-0.4, 0.1, 0.3)$. The raw gradient vanishes like $1/T^2$; the scaled one converges with an error of order $1/T$.

**Soft targets carry more information than labels.** A teacher is a linear softmax model with 4 classes and 6 Gaussian features (weights drawn from $N(0, 1.5^2)$). The student has the same form and sees only 12 training inputs, with labels sampled from the teacher. Full batch gradient descent with step 0.5 runs for 400 epochs (seed `random.Random(5)`). On 500 new inputs:

| training signal | agreement with the teacher's top class | mean total variation from the teacher |
|---|---|---|
| hard labels only ($\alpha = 0$) | 0.614 | 0.383 |
| soft targets, $T = 1$ | 0.894 | 0.102 |
| soft targets, $T = 4$ | 1.000 | 0.00007 |
| half and half, $T = 4$, $\alpha = 0.5$ | 0.924 | 0.078 |

Each soft target gives 3 free numbers instead of one label, so 12 examples give 36 equations for the 18 free student parameters (24 weights minus 6 for the shift that leaves the softmax unchanged), and the student recovers the teacher. The run at $T = 1$ is slower to converge within the same 400 epochs. A real student cannot represent its teacher exactly, so the gains are smaller.

**Hinton et al. (2015).** On MNIST, a small network distilled from a large regularized one made far fewer test errors than the same small network trained on labels; when all 3s were removed from the transfer set, the student still recognized most test 3s once the bias of the 3 class was raised, because the soft probabilities of the 3 class on other digits had taught it what a 3 looks like. On speech recognition, an ensemble of 10 acoustic models was distilled into a single model that kept most of the ensemble's gain.

**Ensembles to one model (Bucila et al. 2006).** Ensembles of hundreds of models labeled a large set of generated inputs, and one neural network trained on these labels matched the ensemble at a small fraction of its size and time.

## Variations

- **Logit matching.** Squared error between student and teacher logits, the high temperature limit (Ba and Caruana 2014).
- **Feature distillation.** Match intermediate layers of the teacher through a small learned map, as in FitNets (Romero et al. 2015), or match attention maps or relations between examples.
- **Self-distillation.** The student has the same architecture as the teacher, and it can still improve on it (born again networks, Furlanello et al. 2018). Several generations can follow.
- **Online and mutual distillation.** Teacher and students train at the same time and learn from each other.
- **Sequence-level distillation.** For sequence models, train on the teacher's decoded output sequences instead of per-token distributions.
- **Distillation for language models.** Large pretrained models are distilled into smaller ones with a soft loss on the output tokens plus losses on hidden states.
- **Relation to label smoothing.** [Label smoothing](/label-smoothing/) mixes the hard label with the uniform distribution; distillation mixes it with the teacher's distribution, which puts the extra mass on the classes that look alike.

## Pitfalls

- **Forgetting the $T^2$ factor.** Without it, raising $T$ silently turns the soft term off, and the tuning of $\alpha$ and $T$ interact.
- **Training the student at $T$ but deploying it with the wrong temperature.** The student must be used with $T = 1$, or with a temperature tuned on validation data for calibration.
- **Expecting fidelity.** Students often reach a good test accuracy while they still disagree with the teacher on many inputs; matching the teacher closely can be an optimization problem, not only a capacity problem (Stanton et al. 2021).
- **A too large gap.** A very strong teacher can be a worse teacher for a very small student than a medium teacher; intermediate teacher sizes can help.
- **A poor transfer set.** The soft targets are only informative on inputs like those seen at deployment. Data augmentation of the transfer set often helps.
- **Overconfident teachers.** If the teacher's logits are huge, $q$ is nearly one-hot at moderate $T$, and the soft term adds little; raise $T$ or check the teacher's calibration.

## Exercises

1. Derive $\partial C_{\text{soft}} / \partial z_i = (p_i - q_i)/T$, and show that the gradient sums to zero over $i$.
2. Show that adding a constant to all student logits leaves $C_{\text{soft}}$ unchanged, and explain why the high temperature limit involves centered logits.
3. Expand $\operatorname{softmax}_T(u)$ to second order in $1/T$, and give the term of order $1/T$ in $T^2 \partial C_{\text{soft}} / \partial z$.
4. For a linear softmax student with $K$ classes and $d$ features, how many transfer examples are needed, in general position, to determine the teacher's weights from exact soft targets? From hard labels?

## References
