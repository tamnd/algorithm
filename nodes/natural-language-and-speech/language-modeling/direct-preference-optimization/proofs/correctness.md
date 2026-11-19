---
title: The KL-regularized objective has the optimum pi_ref exp(r / beta) / Z, the Bradley-Terry likelihood of that optimum does not depend on Z, so the DPO loss is the reward-model loss of the implicit reward, and the gradient is -beta sigmoid(-z) on the preferred log probability
proves: [correctness]
status: full
---

We use the notation of the page. Fix one prompt $x$ and drop it from the notation where it is fixed. $\mathcal{Y}$ is the set of responses, which we take finite (for sequences of bounded length over a finite vocabulary $V$ it is). The reference policy $\pi_{\text{ref}}$ is a distribution on $\mathcal{Y}$ with $\pi_{\text{ref}}(y) > 0$ for every $y$, the reward $r : \mathcal{Y} \to \mathbb{R}$ is a function, and $\beta > 0$. All logs are natural logs. $\sigma(z) = 1 / (1 + e^{-z})$.

## Theorem 1: the optimum of the KL-regularized objective

Let

$$J(\pi) = \sum_{y} \pi(y) r(y) - \beta\, \mathrm{KL}(\pi \,\|\, \pi_{\text{ref}}), \qquad \mathrm{KL}(\pi \,\|\, \pi_{\text{ref}}) = \sum_{y} \pi(y) \log \frac{\pi(y)}{\pi_{\text{ref}}(y)},$$

over all distributions $\pi$ on $\mathcal{Y}$, with $0 \log 0 = 0$. Put

$$Z = \sum_{y} \pi_{\text{ref}}(y)\, e^{r(y) / \beta}, \qquad \pi^*(y) = \frac{\pi_{\text{ref}}(y)\, e^{r(y)/\beta}}{Z}.$$

Then $J(\pi) = \beta \log Z - \beta\, \mathrm{KL}(\pi \,\|\, \pi^*)$ for every $\pi$. Hence $\pi^*$ is the unique maximizer, and the maximum is $\beta \log Z$.

Proof. $\pi^*$ is a distribution with $\pi^*(y) > 0$ for every $y$, so $\mathrm{KL}(\pi \,\|\, \pi^*)$ is finite. From the definition, $\log \pi^*(y) = \log \pi_{\text{ref}}(y) + r(y) / \beta - \log Z$. So

$$\mathrm{KL}(\pi \,\|\, \pi^*) = \sum_y \pi(y) \left( \log \frac{\pi(y)}{\pi_{\text{ref}}(y)} - \frac{r(y)}{\beta} + \log Z \right) = \mathrm{KL}(\pi \,\|\, \pi_{\text{ref}}) - \frac{1}{\beta} \sum_y \pi(y) r(y) + \log Z,$$

where we used $\sum_y \pi(y) = 1$. Multiply by $-\beta$ and rearrange: $J(\pi) = \beta \log Z - \beta\, \mathrm{KL}(\pi \,\|\, \pi^*)$. By Gibbs' inequality ([Kullback-Leibler divergence](/kullback-leibler-divergence/)), $\mathrm{KL}(\pi \,\|\, \pi^*) \ge 0$ with equality only when $\pi = \pi^*$. So $J(\pi) \le \beta \log Z$, with equality only at $\pi^*$. $\square$

The objective of the page averages $J$ over prompts $x$ drawn from a fixed distribution. The policy for each $x$ can be chosen apart from the others, so the optimum is $\pi^*(\cdot \mid x)$ for every $x$, with its own $Z(x)$.

## Corollary 2: the reward in terms of the optimal policy

Take logs in the definition of $\pi^*$ and solve for $r$:

$$r(x, y) = \beta \log \frac{\pi^*(y \mid x)}{\pi_{\text{ref}}(y \mid x)} + \beta \log Z(x).$$

So the reward is determined by the optimal policy up to the term $\beta \log Z(x)$, which depends on the prompt and not on the response. Conversely, if two rewards differ by a function of $x$ only, $r'(x, y) = r(x, y) + f(x)$, then $Z'(x) = Z(x) e^{f(x)/\beta}$ and the two give the same $\pi^*$. This is Lemma 2 of Rafailov and colleagues (Section 5.1). Their Lemma 1, that such rewards also give the same Bradley-Terry preferences, holds because $f(x)$ cancels in the difference $r'(x, y_w) - r'(x, y_l)$.

## Proposition 3: the Bradley-Terry likelihood in terms of the policy

The Bradley-Terry model says that $y_w$ is preferred to $y_l$ for the prompt $x$ with probability $\sigma(r(x, y_w) - r(x, y_l))$. Substitute Corollary 2 into the difference. The term $\beta \log Z(x)$ appears in both rewards and cancels:

$$p(y_w \succ y_l \mid x) = \sigma\!\left( \beta \log \frac{\pi^*(y_w \mid x)}{\pi_{\text{ref}}(y_w \mid x)} - \beta \log \frac{\pi^*(y_l \mid x)}{\pi_{\text{ref}}(y_l \mid x)} \right).$$

So the preference probabilities can be written with the policy alone, without $Z$, which would need a sum over all responses. DPO replaces $\pi^*$ by the trained policy $\pi_\theta$ and maximizes the log likelihood of the observed preferences. With $a = \log \pi_\theta$, $b = \log \pi_{\text{ref}}$ and $z = \beta ((a_w - b_w) - (a_l - b_l))$, the negative log likelihood of one pair is $-\log \sigma(z)$, which is the loss of line L4. It equals the Bradley-Terry loss $-\log \sigma(\hat r_w - \hat r_l)$ of the reward model $\hat r(x, y) = \beta \log (\pi_\theta(y \mid x) / \pi_{\text{ref}}(y \mid x))$, the implicit reward.

## Proposition 4: the population minimizer is the optimal policy

Fix a prompt. Suppose that each unordered pair $\{y, y'\}$ of responses is compared with probability $\mu(\{y, y'\}) > 0$, and that the label follows the Bradley-Terry model with the true reward $r$. Suppose that the policy is a softmax over $\mathcal{Y}$ with free logits, so every positive distribution is reachable. Then the expected DPO loss is minimized exactly by $\pi_\theta = \pi^*$.

Proof. For the pair $\{y, y'\}$ let $p = \sigma(r(y) - r(y'))$ and $z = \beta ((\log \pi_\theta(y) - \log \pi_{\text{ref}}(y)) - (\log \pi_\theta(y') - \log \pi_{\text{ref}}(y')))$. The expected loss of the pair is $-p \log \sigma(z) - (1 - p) \log \sigma(-z)$, using $1 - \sigma(z) = \sigma(-z)$. This is the cross-entropy between the Bernoulli distributions with means $p$ and $\sigma(z)$. It equals the entropy of the first plus their Kullback-Leibler divergence, so it is minimized exactly when $\sigma(z) = p$, that is $z = r(y) - r(y')$, because $\sigma$ is strictly increasing. At $\pi_\theta = \pi^*$, Corollary 2 gives $z = r(y) - r(y')$ for every pair, so every term is at its minimum, and so is the weighted sum. Conversely, at a minimizer every pair with $\mu > 0$ has $z = r(y) - r(y')$; since every pair is compared, $\beta \log (\pi_\theta(y) / \pi_{\text{ref}}(y)) - r(y)$ is the same constant $c$ for all $y$, so $\pi_\theta(y) \propto \pi_{\text{ref}}(y) e^{r(y)/\beta}$, which is $\pi^*$. $\square$

It is enough that the graph of compared pairs is connected: the constant then propagates along its paths. If the graph has two components, the relative mass of the components is not fixed by the data, and the minimizer is not unique. The proposition is about the population loss with Bradley-Terry labels and an unrestricted policy. With a finite data set, a restricted network and an optimizer that stops early, it says nothing about the result; that is a matter of measurement.

## Proposition 5: the gradient

Let $f(z) = -\log \sigma(z) = \log(1 + e^{-z})$. Then $f'(z) = -e^{-z} / (1 + e^{-z}) = -\sigma(-z)$. For a batch of $m$ pairs the loss is $L = \frac{1}{m} \sum_i f(z_i)$, and $z_i$ depends on $a_{w,i}$ with slope $\beta$ and on $a_{l,i}$ with slope $-\beta$. By the chain rule

$$\frac{\partial L}{\partial a_{w,i}} = -\frac{\beta}{m} \sigma(-z_i), \qquad \frac{\partial L}{\partial a_{l,i}} = +\frac{\beta}{m} \sigma(-z_i),$$

which are lines L5 and L6. The reference log probabilities enter with the opposite signs. For a network with weights $\theta$, the gradient is

$$\nabla_\theta L = -\frac{\beta}{m} \sum_i \sigma(-z_i) \left( \nabla_\theta \log \pi_\theta(y_{w,i} \mid x_i) - \nabla_\theta \log \pi_\theta(y_{l,i} \mid x_i) \right),$$

and $\sigma(-z_i) = \sigma(\hat r_{l,i} - \hat r_{w,i})$ is large when the implicit reward ranks the pair in the wrong order. For the tabular softmax policy of the code, $\log \pi_\theta(y) = \theta_y - \log \sum_{y'} e^{\theta_{y'}}$, so the normalizer cancels in $\log \pi_\theta(y_w) - \log \pi_\theta(y_l) = \theta_{y_w} - \theta_{y_l}$, and $\partial z / \partial \theta_j = \beta ([j = y_w] - [j = y_l])$.

## Proposition 6: the loss is computed without overflow

$f(z) = \log(1 + e^{-z}) = \log(e^{0} + e^{-z})$, which is $\text{log\_add}(0, -z)$. log_add takes the exponential of a non-positive number only, so it does not overflow for any finite $z$: for $z = -1000$ it returns $1000 + \log(1 + e^{-1000}) = 1000$, and for $z = 1000$ it returns $\log(1 + e^{-1000})$, which rounds to $0$. The function sigmoid of the code takes $e^{-z}$ for $z \ge 0$ and $e^{z}$ for $z < 0$, so it also takes the exponential of a non-positive number only. The sequence log probabilities themselves are sums of per-token log probabilities and are never exponentiated.

## Remark: deterministic preferences

If one response always wins, so $p = 1$ in Proposition 4, the pair loss $-\log \sigma(z)$ decreases in $z$ and has no finite minimizer. The population minimizer then puts $\pi_\theta(y_l) / \pi_\theta(y_w) \to 0$ for any $\beta$: the KL term of Theorem 1 does not stop it, because the derivation assumed a finite reward. The test "deterministic preferences push without limit" shows the loss falling at each step.
