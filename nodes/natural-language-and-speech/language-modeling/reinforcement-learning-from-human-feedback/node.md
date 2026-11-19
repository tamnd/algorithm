---
tag: 8YYWNG
kind: technique
slug: reinforcement-learning-from-human-feedback
name: Reinforcement learning from human feedback
aliases:
- RLHF
area: natural-language-and-speech/language-modeling
level: research
summary: Fit a reward model to human comparisons of outputs, then tune the language model by policy gradient to raise reward under a KL penalty.
history:
  year: 2017
  people: [Paul Christiano, Jan Leike, Tom B. Brown, Miljan Martic, Shane Legg, Dario Amodei]
  note: "Christiano and colleagues trained agents for Atari games and simulated robots against a reward fitted to human comparisons. Stiennon et al. (2020) applied the method to summaries, and Ouyang et al. (2022) to following instructions."
prereqs: [preference-reward-model, ppo, kullback-leibler-divergence]
see_also: [direct-preference-optimization, instruction-tuning, generative-pretrained-transformer, policy-gradient-theorem, generalized-advantage-estimation, reinforce, inverse-reinforcement-learning, maximum-entropy-rl]
sources:
  - url: https://arxiv.org/abs/1706.03741
    title: "Paul Christiano, Jan Leike, Tom B. Brown, Miljan Martic, Shane Legg and Dario Amodei, Deep reinforcement learning from human preferences, 2017"
    locator: "the abstract (feedback on less than 1% of the interactions of the agent, and new behaviors from about an hour of human time) and Section 2 (the method)"
  - url: https://arxiv.org/abs/2009.01325
    title: "Nisan Stiennon, Long Ouyang, Jeff Wu and others, Learning to summarize from human feedback, NeurIPS 2020"
    locator: "the abstract (summaries of Reddit posts preferred to the human reference summaries) and Appendix G.3 (the KL divergence of best-of-n)"
  - url: https://arxiv.org/abs/2203.02155
    title: "Long Ouyang, Jeff Wu, Xu Jiang and others, Training language models to follow instructions with human feedback, NeurIPS 2022"
    locator: "Figure 1 (the 1.3B model preferred to the 175B GPT-3), Section 3.5 (the three steps and equation 2), Section 5.1 (the compute of each step), Appendix C.4 (beta = 0.02, gamma = 27.8, 256k episodes, no discount, clip 0.2), Appendix E.6 (fixing regressions on public NLP data sets)"
  - url: https://arxiv.org/abs/1707.06347
    title: "John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford and Oleg Klimov, Proximal policy optimization algorithms, 2017"
    locator: the clipped surrogate objective
  - url: https://arxiv.org/abs/2210.10760
    title: "Leo Gao, John Schulman and Jacob Hilton, Scaling laws for reward model overoptimization, 2022"
    locator: "Section 1 (the gold score as a function of the square root of the KL divergence) and Section 3.6 (the KL penalty acts like early stopping)"
  - url: https://arxiv.org/abs/2305.18290
    title: "Rafael Rafailov, Archit Sharma, Eric Mitchell, Stefano Ermon, Christopher D. Manning and Chelsea Finn, Direct preference optimization: Your language model is secretly a reward model, NeurIPS 2023"
    locator: "Section 4 (the closed-form optimum of the KL-regularized objective)"
---

Reinforcement learning from human feedback (RLHF) tunes a language model so that its responses get a high score from a reward model fitted to human comparisons, while a KL penalty keeps it close to a reference model. It is a pipeline with three steps. First, [instruction tuning](/instruction-tuning/), which is supervised fine-tuning on written demonstrations, gives the reference model. Second, a [preference reward model](/preference-reward-model/) is fitted to comparisons of that model's responses; this is the model that the pipeline fits, not the pipeline itself. Third, a policy-gradient method, usually [PPO](/ppo/), raises the reward minus the penalty. PPO is a general reinforcement learning algorithm and knows nothing of human feedback. [Direct preference optimization](/direct-preference-optimization/) (DPO) targets the same KL-regularized objective, but with one classification loss on the comparisons, no reward model and no sampling during training.

## In plain words

Some goals are hard to write as a formula, such as "a helpful and honest answer". But people can look at two answers and say which one is better.

RLHF uses this. You collect many such choices. You train a second network to guess which answer people will like. Then you let the language model write answers, score them with the second network, and change the model so that it writes answers that score higher.

The scoring network is only a guess. If the model is pushed too hard, it finds answers that fool the scorer but that people do not like. So the training also holds the model near its starting point, and a setting controls how far it may move.

## When it applies

- The goal is a judgment of people, not a label or a formula, and people can compare two outputs more reliably than they can rate one.
- A pretrained and fine-tuned model already gives outputs that are worth comparing. RLHF moves a good model; it does not build one from scratch.
- There is a budget for labelers, and compute to sample responses from the policy during training and to hold several large networks in memory.
- The comparisons follow the [Bradley-Terry](/preference-reward-model/) assumption well enough: preferences are mostly transitive and can be summarized by one number per response.

## The template

Let $\pi_{\text{SFT}}$ be the reference model, $\pi_\phi$ the policy being trained, and $r_\theta$ the reward model. For a prompt $x$ and a response $y = y_1 \ldots y_n$ of $n$ tokens over a vocabulary of size $|V|$, the policy and the reference each give an $n \times |V|$ matrix of next-token logits, so $\log \pi(y \mid x) = \sum_{t=1}^{n} \log \pi(y_t \mid x, y_{<t})$, as in [causal language modeling](/causal-language-modeling/). The reward model gives one number for the whole response.

1. **Supervised fine-tuning.** Fine-tune a pretrained model on demonstrations written by people, with the next-token [cross-entropy loss](/cross-entropy-loss/). The result is $\pi_{\text{SFT}}$, which stays frozen from now on.
2. **Comparisons.** For each prompt, sample $K$ responses from the model and let a person rank them.
3. **The reward model.** Fit $r_\theta$ to the comparisons with the loss $-\log \sigma(r_\theta(x, y_w) - r_\theta(x, y_l))$, where $\sigma$ is the logistic sigmoid.
4. **Reinforcement learning.** Start $\pi_\phi$ at $\pi_{\text{SFT}}$ and maximize

$$J(\phi) = \mathbb{E}_{x,\; y \sim \pi_\phi(\cdot \mid x)} \Big[ r_\theta(x, y) - \beta \log \frac{\pi_\phi(y \mid x)}{\pi_{\text{SFT}}(y \mid x)} \Big] + \gamma\, \mathbb{E}_{x \sim D_{\text{pretrain}}} \big[ \log \pi_\phi(x) \big].$$

This is equation 2 of Ouyang et al. The second term mixes in the pretraining loss; with $\gamma = 0$ it is gone. The expectation of the log ratio over $y \sim \pi_\phi$ is the [Kullback-Leibler divergence](/kullback-leibler-divergence/) $\mathrm{KL}(\pi_\phi \,\|\, \pi_{\text{SFT}})$, so the first term is the reward minus $\beta$ times the KL divergence.

**One episode.** Ouyang et al. (Section 3.5) treat each prompt as a bandit episode: the policy writes a response, the reward model scores it, and the episode ends. The penalty is paid per token. Token $t$ gets the reward $-\beta (\log \pi_\phi(y_t \mid x, y_{<t}) - \log \pi_{\text{SFT}}(y_t \mid x, y_{<t}))$, and the last token also gets $r_\theta(x, y)$. The sum over the tokens is the bracket in $J$. For example, with $\beta = 0.1$, a reward-model score of 1.3 and per-token log ratios $(0.2, -0.1, 0.4)$, the return is $1.3 - 0.1 \cdot 0.5 = 1.25$. PPO then uses a value function, which predicts the return at each of the $n$ positions, and [generalized advantage estimation](/generalized-advantage-estimation/). Ouyang et al. initialize the value function from the reward model and use no discount (Appendix C.4).

**The networks in memory.** The step uses four networks: the policy (trained), the reference (frozen), the reward model (frozen) and the value function (trained). Ouyang et al. used a 6B reward model and a 6B value function for policies of 1.3B, 6B and 175B parameters.

**What the objective has as its optimum (theorem).** Hypotheses: a fixed reward $r$, $\beta > 0$, a reference with $\pi_{\text{ref}}(y \mid x) > 0$ for every response, and a policy that may be any distribution (no network limits). Then the unique maximizer of $\mathbb{E}_{y \sim \pi}[r(x, y)] - \beta\, \mathrm{KL}(\pi \,\|\, \pi_{\text{ref}})$ is

$$\pi^*(y \mid x) = \frac{\pi_{\text{ref}}(y \mid x)\, e^{r(x, y)/\beta}}{Z(x)}, \qquad Z(x) = \sum_y \pi_{\text{ref}}(y \mid x)\, e^{r(x, y)/\beta},$$

and the maximum is $\beta \log Z(x)$ (Rafailov et al., Section 4; the proof is on the [DPO](/direct-preference-optimization/) page). PPO with a network does not reach this optimum exactly; the theorem says what it aims at. A toy case with three responses, $\pi_{\text{ref}} = (0.5, 0.3, 0.2)$ and $r = (0, 1, 2)$, so that $\mathbb{E}_{\pi_{\text{ref}}}[r] = 0.7$:

| $\beta$ | $\pi^*$ | $\mathbb{E}_{\pi^*}[r]$ | $\mathrm{KL}(\pi^* \,\|\, \pi_{\text{ref}})$ | objective |
|---|---|---|---|---|
| 0.5 | (0.03667, 0.16256, 0.80077) | 1.76411 | 0.91548 | 1.30637 |
| 1 | (0.17900, 0.29194, 0.52906) | 1.35006 | 0.32283 | 1.02722 |
| 2 | (0.32504, 0.32154, 0.35342) | 1.02838 | 0.08353 | 0.86132 |

A small $\beta$ buys reward with a large move away from the reference; a large $\beta$ keeps the policy near it.

## Classic examples

- **Atari and simulated robots.** Christiano et al. (2017) trained agents without access to the true reward, from comparisons of short clips. They report that people gave feedback on less than 1% of the interactions of the agent, and that new behaviors could be trained with about an hour of human time (abstract). This is a measurement on their tasks.
- **Summaries.** Stiennon et al. (2020) fitted a reward model to comparisons of summaries of Reddit posts and tuned the policy with reinforcement learning. Their models were preferred to the human reference summaries and to much larger models trained with supervised learning only (abstract).
- **Following instructions.** Ouyang et al. (2022) applied the three steps to GPT-3, with about 13k prompts for supervised fine-tuning, 33k for the reward model and 31k for PPO. Labelers preferred the outputs of the 1.3B model after RLHF to those of the 175B GPT-3 (Figure 1). The settings were $\beta = 0.02$, $\gamma = 27.8$, 256k episodes and a PPO clip ratio of 0.2 (Appendix C.4). Training the 175B policy took 60 petaflop/s-days, against 4.9 for supervised fine-tuning and 3,640 for pretraining GPT-3 (Section 5.1).

## Variations

- **DPO.** It fits the policy to the comparisons directly, with the Bradley-Terry loss of the implicit reward $\beta \log (\pi_\phi / \pi_{\text{ref}})$. Steps 3 and 4 merge into one supervised step, with no sampling.
- **Best-of-n.** Sample $n$ responses and keep the one with the highest reward-model score. No weights change. For continuous outputs with no ties, the KL divergence of the best-of-n distribution from the base is $\log n - (n - 1)/n$ (Stiennon et al., Appendix G.3), so $0.636$ nats for $n = 4$ and $1.835$ for $n = 16$.
- **Other policy-gradient methods.** Any method that follows the [policy gradient theorem](/policy-gradient-theorem/) can replace PPO, for example [REINFORCE](/reinforce/) with a baseline. PPO is the common choice because its clipped step limits how far one batch can move the policy.
- **The pretraining mix.** Ouyang et al. call the version with $\gamma > 0$ PPO-ptx. It reduced the drop in scores on public NLP data sets that plain PPO caused.
- **Entropy-regularized control.** The KL penalty to a reference is a form of [maximum entropy reinforcement learning](/maximum-entropy-rl/), with the reference in the place of the uniform policy.

## Pitfalls

- **Reward overoptimization.** The reward model is a proxy. Gao, Schulman and Hilton (2022) measured that the true score first rises and then falls as the policy moves away from its start, in a synthetic setup where a 6B reward model stood in for people. Watch a held-out judge, not the training reward.
- **The KL penalty is not a cure.** In the same study the penalty made the true score level off earlier but did not move the curve of true score against KL distance, so it acted like early stopping (Section 3.6). They also note that this result could be sensitive to the settings.
- **The alignment tax.** Ouyang et al. found that plain PPO lowered scores on public data sets such as SQuADv2 and DROP. Raising $\beta$ to 2.0, 100 times the default, did not fix this on the 1.3B model, but mixing in pretraining gradients did (Appendix E.6).
- **People disagree.** Labelers in Ouyang et al. agreed with each other on about 73% to 77% of comparisons. The reward model learns the preferences of the people who labeled, not of everybody.
- **A per-token KL estimate can be negative.** The sum of the log ratios over one sampled response is an unbiased estimate of the KL divergence, but one sample can give a negative value. Report the mean over many samples.
- **Shift of the reward.** The comparisons fix the reward only up to a constant for each prompt. Ouyang et al. add a bias so that the demonstrations score 0 on average before reinforcement learning (Section 3.5). A constant shift does not change the optimal policy, but it does change the targets that the value function must learn.

## Exercises

1. Prove the theorem of the template: write $\mathbb{E}_\pi[r] - \beta\, \mathrm{KL}(\pi \,\|\, \pi_{\text{ref}})$ as $\beta \log Z - \beta\, \mathrm{KL}(\pi \,\|\, \pi^*)$. Then check the row $\beta = 1$ of the table, and show that the objective there equals $\log Z$ with $Z = 2.793296$.
2. Show that for a response sampled from $\pi$, the expected sum of the per-token log ratios $\log \pi(y_t \mid x, y_{<t}) - \log \pi_{\text{ref}}(y_t \mid x, y_{<t})$ is $\mathrm{KL}(\pi(\cdot \mid x) \,\|\, \pi_{\text{ref}}(\cdot \mid x))$. Give a two-response example in which one sample has a negative sum.
3. Show that replacing $r(x, y)$ by $r(x, y) + c(x)$ leaves $\pi^*$ unchanged. What happens to the maximum value $\beta \log Z(x)$?
4. Let the base model output a continuous score with no ties, and let best-of-n keep the maximum of $n$ draws. Show that the density ratio of the best-of-n distribution to the base at quantile $u$ is $n u^{n-1}$, and derive $\mathrm{KL} = \log n - (n - 1)/n$.
5. In the toy table, which values of $\beta$ keep $\mathrm{KL}(\pi^* \,\|\, \pi_{\text{ref}})$ below 0.1? Find the smallest such $\beta$ to three digits by bisection.

## References
