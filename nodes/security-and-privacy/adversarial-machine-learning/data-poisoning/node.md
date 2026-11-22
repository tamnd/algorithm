---
tag: T5XZ55
kind: concept
slug: data-poisoning
name: Data poisoning
aliases:
- poisoning attack
- training set attack
area: security-and-privacy/adversarial-machine-learning
level: core
summary: An attack that inserts or changes training points so that the learned model makes errors chosen by the attacker.
history:
  year: 2006
  people: [Marco Barreno, Blaine Nelson, Russell Sears, Anthony D. Joseph, J. D. Tygar, Battista Biggio, Pavel Laskov]
  note: Barreno et al. (2006) named attacks on the training data causative attacks in their taxonomy. Biggio, Nelson and Laskov (2012) gave the first gradient-based poisoning attack on an SVM.
prereqs: [empirical-risk-minimization, median]
see_also: [svm-poisoning-attack, clean-label-poisoning, backdoor-attack, spectral-signatures-defense, krum-aggregation, evasion-attack, sisa-training, machine-unlearning]
sources:
  - paper: "Marco Barreno, Blaine Nelson, Russell Sears, Anthony D. Joseph and J. D. Tygar, Can machine learning be secure?, ACM Symposium on Information, Computer and Communications Security (ASIACCS) 2006"
    locator: the taxonomy of attacks (causative against exploratory, integrity against availability, targeted against indiscriminate) and the first list of defenses
  - paper: doi:10.1007/s10994-010-5188-5
    title: Marco Barreno, Blaine Nelson, Anthony D. Joseph and J. D. Tygar, The security of machine learning, Machine Learning 81(2), 2010, pages 121 to 148
    locator: the journal version of the taxonomy, the survey of causative attacks, and the Reject On Negative Impact defense
  - paper: "Battista Biggio, Blaine Nelson and Pavel Laskov, Poisoning attacks against support vector machines, Proceedings of the 29th International Conference on Machine Learning (ICML) 2012, pages 1467 to 1474, arXiv:1206.6389"
    locator: Section 2 (the poisoning problem as the maximization of the validation hinge loss over one attack point) and Section 3.2 (the MNIST experiments)
  - paper: doi:10.1016/j.patcog.2018.07.023
    title: Battista Biggio and Fabio Roli, Wild patterns, ten years after the rise of adversarial machine learning, Pattern Recognition 84, 2018, pages 317 to 331
    locator: the threat model of goal, knowledge and capability, and the bilevel form of poisoning
  - paper: "Pang Wei Koh and Percy Liang, Understanding black-box predictions via influence functions, Proceedings of the 34th International Conference on Machine Learning (ICML) 2017"
    locator: the influence of one training point on the parameters and on a test loss, and its use to build poisoned training points
  - paper: "Jacob Steinhardt, Pang Wei Koh and Percy Liang, Certified defenses for data poisoning attacks, Advances in Neural Information Processing Systems 30 (NeurIPS) 2017"
    locator: the upper bound on the loss that any attack can cause against a learner that first removes outliers
  - paper: "Alexander Levine and Soheil Feizi, Deep partition aggregation, provable defense against general poisoning attacks, International Conference on Learning Representations (ICLR) 2021"
    locator: one model for each part of a partition fixed by a hash of each point, the majority vote, and the certificate from the vote gap
---

Data poisoning is an attack on the training stage of a learner: the attacker inserts, changes or relabels some training points so that the model learned from them makes the errors the attacker wants. In the taxonomy of Barreno et al. (2006, 2010) it is a *causative* attack, against an *exploratory* (test time) attack such as an [evasion attack](/evasion-attack/). It works because [empirical risk minimization](/empirical-risk-minimization/) gives each training point a direct effect on the parameters, and a learner that averages has no bound on the effect of one bad point. The defenses clean the data before training, learn with a rule that bounds the effect of a few points, or give a certificate that a prediction does not change under a stated number of poisoned points.

## In plain words

A model learns from examples. If someone can add some examples of their own, or change some of the labels, the model learns from them too. A careful attacker picks these examples so that the model gets worse in a chosen way. The attacker can make the model wrong on many inputs, so that people stop trusting it. Or the attacker can make it wrong on one chosen input, or on every input that carries a secret mark, and keep it right everywhere else so that nobody notices.

The attack works because the learner trusts its training data, and data from users, the web or many devices is hard to check by hand. The defenses remove points that look odd, learn in a way that a few points cannot move far, or split the data so that each bad point can change only a small part of the result.

## The idea

**The threat model.** Follow Biggio and Roli (2018) and state three things.

- *Goal.* An **availability** attack raises the error on most inputs. An **integrity** attack keeps the error low on normal inputs and causes a chosen error: on one target point ([clean-label poisoning](/clean-label-poisoning/)) or on each input that carries a trigger ([backdoor attack](/backdoor-attack/)). Barreno et al. also split attacks into **targeted** (a chosen set of inputs) and **indiscriminate**.
- *Knowledge.* White box (the learner, its features and the clean training set are known), gray box (the learner is known and the data is a sample from the same distribution) or black box.
- *Capability.* The attacker adds at most $\epsilon n$ points to a training set of $n$ clean points, or changes at most $\epsilon n$ of them. The changes may be restricted: only labels (*label flipping*), only features with correct labels (*clean label*), or only points inside a feasible box.

**The bilevel problem.** Let $D$ be the clean training set, $D_p$ the poisoned points, $L$ the loss and $V$ a validation set that stands for the inputs the attacker wants to harm. The learner solves the inner problem, and the attacker solves the outer one:

$$\max_{D_p \in \mathcal{C}} \; \sum_{(x, y) \in V} L(\theta^\star, x, y) \quad \text{subject to} \quad \theta^\star \in \arg\min_{\theta} \sum_{(x, y) \in D \cup D_p} L(\theta, x, y) + \Omega(\theta),$$

where $\mathcal{C}$ is the set of allowed changes and $\Omega$ the regularizer. An integrity attack uses a validation set of target points with the attacker's labels and minimizes their loss instead. The outer objective depends on $D_p$ only through $\theta^\star$, so a gradient method needs $\partial \theta^\star / \partial D_p$. For an SVM, Biggio, Nelson and Laskov (2012) got it from the optimality conditions of the solution ([SVM poisoning attack](/svm-poisoning-attack/)). For a smooth strictly convex loss, the implicit function theorem gives the influence of a point $z$ added with weight $w$:

$$\frac{d \theta^\star}{d w} \Big|_{w = 0} = -H^{-1} \nabla_\theta L(\theta^\star, z), \qquad H = \nabla^2_\theta \sum_{(x, y) \in D} L(\theta^\star, x, y) + \nabla^2 \Omega(\theta^\star),$$

which Koh and Liang (2017) used both to explain predictions and to build poisoned points. The formula shows why poisoning works: the effect of a point grows with its own gradient, and nothing in the learner caps that gradient.

**What bounds the effect of a point.** Three properties of a learner limit poisoning, and the defenses are built on them.

- *A bounded influence.* A rule whose output moves a bounded amount when one point moves anywhere, such as the [median](/median/) or a [trimmed mean](/trimmed-mean/), tolerates a fraction of bad points up to its breakdown point. The mean has breakdown point $0$: one point can move it anywhere.
- *A partition.* If each point can change only one of $m$ sub-models and the output is a vote, then $r$ changed points change at most $r$ votes. This is the base of the certificate of deep partition aggregation (Levine and Feizi 2021) and of [SISA training](/sisa-training/).
- *Stability in distribution.* An $\epsilon$-differentially private learner (see [differential privacy](/differential-privacy-definition/)) changes the probability of each set of outputs by at most a factor $e^{k \epsilon}$ when $k$ points change ([group privacy](/group-privacy-theorem/)), so it resists a small number of poisoned points. The factor grows fast with $k$, so the bound is useful only for a few points.

**Certificates.** A certified defense gives a statement that holds for every attack in the capability set. For deep partition aggregation the argument is short. A hash of each point chooses one of $m$ parts, one model is trained on each part, and the prediction is the class with the most votes. One inserted or deleted point lies in one part, so it changes at most one vote, and it lowers the gap between the top class and any other class by at most 2. Hence if the top class leads every other class by more than $2r$ votes, no set of $r$ insertions and deletions changes the prediction. Steinhardt, Koh and Liang (2017) give a different kind of certificate: an upper bound on the loss that any $\epsilon n$ poisoned points can cause against a learner that first removes outliers, valid for their stated loss and outlier rule.

**Heuristics.** Most deployed defenses are heuristics with no guarantee: outlier removal on features or on losses, removal of points with large influence, Reject On Negative Impact (Barreno et al. 2010, which drops a new point if adding it lowers the accuracy on a held-out set), and [spectral signatures](/spectral-signatures-defense/) for backdoors. An attacker who knows the filter can often place the poison where the filter does not look, so each of these must be evaluated against an adaptive attacker.

## Examples

**One point against the mean.** The nine points $1, 2, \ldots, 9$ have mean $5$ and median $5$. Add one point at $95$. The mean of the ten points is $(45 + 95)/10 = 14$, and the median is $(5 + 6)/2 = 5.5$. In general one added point at $(n + 1) T - \sum_i x_i$ moves the mean of $n$ points to any target $T$, while one point moves the median by at most one position in the sorted order. A learner that averages gradients over clients, as plain distributed training does, has the weakness of the mean; [Krum](/krum-aggregation/) and the coordinate-wise median replace the average.

**Availability poisoning of an SVM.** Biggio, Nelson and Laskov (2012) add one point to the training set of an SVM and move it by gradient ascent on the hinge loss of a validation set. On three two-class MNIST digit tasks with a linear SVM trained on 100 points, a single attack point raised the error from 2 to 5 percent to 15 to 20 percent in their reported runs (a measurement on their data, not a property of the method). The page [SVM poisoning attack](/svm-poisoning-attack/) gives the method on a synthetic model.

**A vote gap certificate.** A partition defense trains $m = 50$ models. On one test input the votes are $30$ for class A, $15$ for class B and $5$ for class C. The gap to the runner-up is $15$, so the prediction A is certified against every $r$ with $2r < 15$, that is, against any $7$ inserted or deleted training points. Against $8$ it is not certified: $8$ points could move $8$ votes from A to B and make it $22$ to $23$.

**Clean labels and backdoors.** A targeted attack need not use wrong labels. Shafahi et al. (2018) add correctly labeled points whose learned features are close to those of one target input, so that the target is classified with the label of the poison ([clean-label poisoning](/clean-label-poisoning/)). A backdoor attack adds points that carry a small trigger and the attacker's label, so that the model behaves normally until the trigger appears ([backdoor attack](/backdoor-attack/)).

## Where it is used

- **Threat analysis of learning systems.** Any learner that retrains on data from users (spam filters, recommender systems, malware classifiers, models trained on web data) has a poisoning threat model. The taxonomy of Barreno et al. is the standard way to state it.
- **Distributed and federated training.** A client controls its own update, so a malicious client poisons the model directly. Robust aggregation rules such as [Krum](/krum-aggregation/) assume at most $f$ Byzantine clients out of $n$, in the sense of [Byzantine fault tolerance](/byzantine-fault-tolerance/).
- **Data sanitization.** Outlier detection before training, as in [spectral signatures](/spectral-signatures-defense/), and the use of robust statistics such as the [median](/median/) and the [trimmed mean](/trimmed-mean/).
- **Certified training.** Partition and vote methods, and [SISA training](/sisa-training/), which uses the same partition to make deletion cheap; [machine unlearning](/machine-unlearning/) then removes points found to be poisoned.
- **Privacy.** A differentially private learner bounds the effect of a few points both on what the model reveals about them and on what they can do to it.

## References
