---
tag: 6TWK9K
kind: model
slug: preference-reward-model
name: Preference reward model
aliases:
- Bradley-Terry reward model
area: natural-language-and-speech/language-modeling
level: research
summary: A network that scores a response so that the chance one response is preferred to another is the sigmoid of the score difference.
history:
  year: 2017
  people: [Paul Christiano, Jan Leike, Tom B. Brown, Miljan Martic, Shane Legg, Dario Amodei]
  note: "Christiano and colleagues fitted a reward network to human comparisons of trajectory segments with the Bradley-Terry model of 1952, and trained an agent against it. Stiennon et al. (2020) and Ouyang et al. (2022) used the same model for language."
prereqs: [logistic-regression, transformer, maximum-likelihood-estimation]
see_also: [reinforcement-learning-from-human-feedback, direct-preference-optimization, ranknet, learning-to-rank, kemeny-rank-aggregation, inverse-reinforcement-learning, logistic-loss, instruction-tuning]
sources:
  - paper: "Ralph Allan Bradley and Milton E. Terry, Rank analysis of incomplete block designs I. The method of paired comparisons, Biometrika 39(3-4), 1952, pages 324 to 345"
    title: Bradley and Terry 1952
    locator: the paired comparison model, with the probability that i beats j equal to the ratio of the strength of i to the sum of the two strengths
  - url: https://arxiv.org/abs/1706.03741
    title: "Paul Christiano, Jan Leike, Tom B. Brown, Miljan Martic, Shane Legg and Dario Amodei, Deep reinforcement learning from human preferences, 2017"
    locator: "Section 2.2 (fitting the reward function to comparisons of trajectory segments with the Bradley-Terry model)"
  - url: https://arxiv.org/abs/2009.01325
    title: "Nisan Stiennon, Long Ouyang, Jeff Wu and others, Learning to summarize from human feedback, NeurIPS 2020"
    locator: "Section 3.4 (the reward model, a language model with a scalar head trained on pairs of summaries)"
  - url: https://arxiv.org/abs/2203.02155
    title: "Long Ouyang, Jeff Wu, Xu Jiang and others, Training language models to follow instructions with human feedback, NeurIPS 2022"
    locator: "Section 3.5 (the reward model, equation 1, the K-way ranking loss and the normalization by a bias), Section 3.4 (agreement between labelers), Section 4.1 (accuracy on held-out labelers), Appendix C.2 (the 6B reward model and its training)"
  - url: https://arxiv.org/abs/2210.10760
    title: "Leo Gao, John Schulman and Jacob Hilton, Scaling laws for reward model overoptimization, 2022"
    locator: "Section 1 (the functional forms of the gold score in the square root of the KL divergence), Section 2.1 (the synthetic setup with a 6B gold reward model), Section 3.2 (scaling with the size of the reward model), Section 3.6 (the effect of the KL penalty)"
  - paper: "David R. Hunter, MM algorithms for generalized Bradley-Terry models, Annals of Statistics 32(1), 2004, pages 384 to 406"
    title: Hunter 2004
    locator: "the MM update for the Bradley-Terry maximum likelihood estimate, and the condition of Zermelo and Ford for existence and uniqueness"
---

A preference reward model is a network $r_\theta(x, y)$ that maps a prompt $x$ and a response $y$ to one real number, the reward. It is trained on human comparisons: a person sees two responses to the same prompt and picks one. The model assumes that the chance that $y_w$ is picked over $y_l$ is $\sigma(r_\theta(x, y_w) - r_\theta(x, y_l))$, with $\sigma(z) = 1 / (1 + e^{-z})$. This is the paired comparison model of Bradley and Terry (1952), which has no page of its own here. The reward model is one part of [reinforcement learning from human feedback](/reinforcement-learning-from-human-feedback/) (RLHF), the pipeline that first fits this model and then tunes a policy against it with [PPO](/ppo/). [Direct preference optimization](/direct-preference-optimization/) (DPO) fits the same Bradley-Terry likelihood, but its reward is implicit in the policy, so it trains no separate reward model. [Instruction tuning](/instruction-tuning/) is supervised fine-tuning on written demonstrations and uses no comparisons at all.

## The machine

**Shapes.** The prompt and the response are joined into one sequence of $n$ tokens from a vocabulary of size $|V|$. The backbone is a pretrained [transformer](/transformer/) of width $d$, often the model after supervised fine-tuning. Ouyang et al. (Section 3.5) start from that model and remove the final unembedding layer, a $d \times |V|$ matrix. In its place goes a head with a weight vector $w$ of size $d$ and a bias $b$.

- The input is $n$ token ids. The [embedding](/embedding/) gives an $n \times d$ matrix.
- The transformer layers give the hidden states $H$, also $n \times d$.
- A common design reads the final hidden state $h_n$ of the last token, a vector of size $d$, and returns $r = w^\top h_n + b$, one number.

So the head adds $d + 1$ parameters, and the model costs the same as one forward pass of the backbone.

**The likelihood.** Bradley and Terry give each item $i$ a strength $\pi_i > 0$ and set $P(i \text{ beats } j) = \pi_i / (\pi_i + \pi_j)$. With $\pi_i = e^{r_i}$ this is

$$P(y_w \succ y_l \mid x) = \frac{e^{r(x, y_w)}}{e^{r(x, y_w)} + e^{r(x, y_l)}} = \sigma\big(r(x, y_w) - r(x, y_l)\big).$$

The loss of one comparison is the negative log likelihood, $-\log \sigma(r_w - r_l)$, the [logistic loss](/logistic-loss/) of the score difference. Its derivatives are

$$\frac{\partial}{\partial r_w} = -\sigma(r_l - r_w), \qquad \frac{\partial}{\partial r_l} = +\sigma(r_l - r_w),$$

and [backpropagation](/backpropagation/) carries them into the network. For example, $r_w = 1.5$ and $r_l = 0.5$ give $P = \sigma(1) = 0.731059$, a loss of $0.313262$ and a derivative of $-0.268941$ with respect to $r_w$. Equal rewards give the loss $\log 2 = 0.693147$.

**Rankings of K responses.** Ouyang et al. (Section 3.5) show a labeler between $K = 4$ and $K = 9$ responses to rank. A ranking gives $\binom{K}{2}$ comparisons. All comparisons of one prompt go into one batch element, with the loss

$$\text{loss}(\theta) = -\frac{1}{\binom{K}{2}}\, \mathbb{E}_{(x, y_w, y_l)} \big[ \log \sigma\big(r_\theta(x, y_w) - r_\theta(x, y_l)\big) \big].$$

This needs one forward pass for each of the $K$ responses instead of two for each of the $\binom{K}{2}$ pairs. For $K = 4$ responses ranked in order with rewards $(2, 1, 0.5, -1)$, the six pair losses average to $0.227613$.

**Only differences count.** Add any $c(x)$ to every reward of a prompt and every probability stays the same. So the data fix the reward of one prompt only up to a constant. Ouyang et al. (Section 3.5) add a bias so that the labeler demonstrations get a mean score of 0 before reinforcement learning.

## What it counts

The size of a task is $m$, the number of comparisons, $K$, the number of responses for one prompt, $n$, the number of tokens of a sequence, and $d$, the width. One forward pass of the backbone on $n$ tokens costs $\Theta(n^2 d + n d^2)$ per layer, as on the transformer page. The head and the loss add $\Theta(d)$ per response and $\Theta(1)$ per pair.

The quantities that people measure are these.

- **Pairwise accuracy.** The share of held-out comparisons in which $r_w > r_l$. People do not agree with each other on every pair, so this accuracy has a ceiling well under 1.
- **Log loss.** The mean of $-\log \sigma(r_w - r_l)$ on held-out pairs. It also checks that the predicted probabilities are calibrated, not only that the order is right.

**A small example with a table of rewards.** Take one prompt and three responses A, B and C with free rewards, no network. The data are 13 comparisons: A beat B 3 times and lost once, B beat C 3 times and lost once, and A beat C 4 times and lost once. The maximum likelihood rewards, scaled so that they sum to 0, are $(0.83614, 0, -0.83614)$. At the maximum, the number of wins of each response equals the sum of its predicted win probabilities over its comparisons: 7 for A, 4 for B and 2 for C. The fitted model gives $P(A \succ B) = P(B \succ C) = 0.69765$, against an observed share of 0.75, and $P(A \succ C) = 0.84188$, against 0.8. A single strength for each response cannot match all three shares. The negative log likelihood falls from $9.01091$ at equal rewards to $7.08543$. Hunter's MM update (Hunter 2004), which multiplies each strength by the ratio of its wins to its expected wins in a form that never decreases the likelihood, finds these values. It is a relative of the [expectation-maximization](/expectation-maximization/) algorithm.

## Relation to other models

- **Logistic regression.** If the reward is linear in a fixed feature vector, $r(x, y) = w^\top \phi(x, y)$, the loss is [logistic regression](/logistic-regression/) on the difference $\phi(x, y_w) - \phi(x, y_l)$ with the label 1 and no intercept. A preference reward model replaces $\phi$ with a transformer whose weights are also trained.
- **Learning to rank.** [RankNet](/ranknet/) scores documents for a query with a network and trains on pairs with the same pairwise logistic loss. A reward model is a pairwise model of [learning to rank](/learning-to-rank/) whose query is a prompt and whose documents are responses.
- **DPO.** DPO uses the reward $\hat r(x, y) = \beta \log (\pi_\theta(y \mid x) / \pi_{\text{ref}}(y \mid x))$ of a policy $\pi_\theta$ and a frozen reference $\pi_{\text{ref}}$, and puts it into the same Bradley-Terry loss.
- **Inverse reinforcement learning.** [Inverse reinforcement learning](/inverse-reinforcement-learning/) recovers a [reward function](/reward-function/) from what an expert does. A preference reward model recovers it from what a person says about two outcomes. In the language setting, the episode is one prompt and one response, and the reward comes only at the end.
- **Kemeny rank aggregation.** [Kemeny rank aggregation](/kemeny-rank-aggregation/) also turns many pairwise preferences into one order, but it finds the order with the fewest disagreements and has no probabilities.
- **Ratings on a scale.** A [mean opinion score](/mean-opinion-score/) asks people for an absolute rating. A comparison asks only which of two is better, which needs no shared scale between people.

## Known results in the model

- **Theorem (a convex loss for a linear reward).** Hypotheses: the reward is linear in fixed features, $r = w^\top \phi$. Then $-\log \sigma(z)$ is convex in $z$ and $z$ is linear in $w$, so the loss is convex in $w$. For a transformer the loss is not convex in the weights, and training finds a local solution. This is the standard argument for logistic regression.
- **Theorem (existence and uniqueness, Zermelo 1929 and Ford 1957).** Hypotheses: the table model with one free reward per item, and a directed graph with an edge from $i$ to $j$ when $i$ beat $j$ at least once. Then the maximum likelihood rewards exist and are unique up to an additive constant if and only if the graph is strongly connected. If some item never lost, its reward goes to infinity. Hunter (2004) states the condition and proves that the MM update converges under it.
- **Theorem (the model is transitive).** Hypotheses: preferences follow the Bradley-Terry model. If $P(a \succ b) \ge 1/2$ and $P(b \succ c) \ge 1/2$, then $r_a \ge r_b \ge r_c$, so $P(a \succ c) \ge \max(P(a \succ b), P(b \succ c))$, because $\sigma$ is increasing. So the model cannot fit a cycle. Example: if A beats B, B beats C and C beats A, each 9 times out of 10, the maximum likelihood rewards are all equal and the model predicts 0.5 for every pair, although each observed share is 0.9.
- **Measurement (people disagree).** Ouyang et al. (Section 3.4) report that training labelers agree with each other on $72.6 \pm 1.5\%$ of comparisons and held-out labelers on $77.3 \pm 1.3\%$. In Section 4.1 they split the labelers into 5 groups and trained reward models on 4 of them. The accuracy on the held-out group was $69.6 \pm 0.9\%$, against $72.4 \pm 0.4\%$ on the training groups.
- **Measurement (correlated pairs overfit).** Ouyang et al. (Section 3.5) found that if the $\binom{K}{2}$ comparisons of a prompt are shuffled into one data set as separate examples, one pass over the data overfits the reward model. Putting them into one batch element fixed this. They trained for a single epoch, because more epochs overfit (Appendix C.2).
- **Measurement (size and stability).** Ouyang et al. used a 6B reward model for policies of all sizes. A 175B reward model could reach a lower validation loss, but its training was less stable and it was more expensive as the value function of PPO (Appendix C.2).
- **Measurement (overoptimization).** Gao, Schulman and Hilton (2022) labeled data with a 6B gold reward model, trained proxy reward models of 3M to 3B parameters on it, and optimized a 1.2B policy against the proxy. With $d = \sqrt{\mathrm{KL}(\pi \,\|\, \pi_{\text{init}})}$, the gold score fit $d(\alpha - \beta d)$ for best-of-n sampling and $d(\alpha - \beta \log d)$ for reinforcement learning (Section 1). Both rise and then fall: pushing too hard on the proxy lowers the true score. With 90,000 comparisons, the coefficients changed smoothly with the size of the proxy model (Section 3.2). This is a fit to one synthetic setup, not a law for all reward models.

## References
