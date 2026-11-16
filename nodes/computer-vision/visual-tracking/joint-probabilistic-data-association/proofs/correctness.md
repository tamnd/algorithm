---
title: Why the JPDA event weights are posterior probabilities, why the update has the mean and covariance of the track mixture, and why the normalizer is a permanent
proves: [correctness]
status: full
---

Notation as on the page. There are $n$ tracks and $m$ measurements in a region of volume $V$. A joint event $\theta$ is a set of pairs $(i, j)$, each with $j$ in the gate of $i$, in which no track and no measurement appears twice. Its weight is

$$
w(\theta) = \prod_{(i, j) \in \theta} \frac{p_D L_{ij}}{\lambda} \prod_{i \notin \theta} (1 - p_D p_G),
$$

and $c = \sum_\theta w(\theta)$.

## Claim 1: the posterior probability of a joint event

Assume the model of the page. Each target is detected inside its gate with probability $p_D p_G$, independently of the others. A detection of target $i$ inside the gate has the density $L_{ij} / p_G$ there, the Gaussian density truncated to the gate. The number $\phi$ of clutter points is Poisson with mean $\lambda V$, and each is uniform on the region. The $m$ measurements are listed in a uniformly random order. Then $\Pr(\theta \mid z_1, \ldots, z_m) = w(\theta) / c$.

*Proof.* Fix $\theta$ with $k$ pairs, so $\phi = m - k$ measurements are clutter. The joint density of the measurements and the event is a product of four factors.

- The detection pattern: the tracks in $\theta$ are detected in their gates, the others are not, with probability $\prod_{i \in \theta} p_D p_G \prod_{i \notin \theta} (1 - p_D p_G)$.
- The positions: the detections have the density $\prod_{(i,j) \in \theta} L_{ij} / p_G$, and the clutter the density $V^{-\phi}$.
- The clutter count: $e^{-\lambda V} (\lambda V)^\phi / \phi!$.
- The order: the probability that the $k$ detections land in the given $k$ positions of the list of $m$ is $\phi! / m!$.

The product is

$$
\prod_{(i,j) \in \theta} p_D L_{ij} \prod_{i \notin \theta} (1 - p_D p_G) \cdot e^{-\lambda V} \frac{\lambda^\phi}{m!} = \frac{e^{-\lambda V} \lambda^m}{m!} \, w(\theta),
$$

because $\lambda^\phi = \lambda^m \lambda^{-k}$ and each of the $k$ pairs takes one factor $\lambda^{-1}$. The factor in front does not depend on $\theta$. By [Bayes' theorem](/bayes-theorem/), the posterior of $\theta$ is $w(\theta)$ divided by the sum over all events, which is $w(\theta) / c$. An assignment with a pair outside a gate has density 0 under the truncated model, so the sum runs exactly over the joint events. $\square$

It follows that $\beta_{ij} = \sum_{\theta \ni (i,j)} w(\theta) / c$ is the posterior probability that measurement $j$ comes from track $i$, and $\beta_{i0} = 1 - \sum_j \beta_{ij}$ is the probability that track $i$ has no measurement, since the events in which $i$ has a measurement are disjoint by measurement.

## Claim 2: the mean and covariance of the update

Assume the prior of each track is Gaussian with mean $\hat x_i$ and covariance $\hat P_i$, independent of the other tracks. Given an event with the pair $(i, j)$, the posterior of track $i$ is the Kalman update with mean $x_{ij} = \hat x_i + K_i \nu_{ij}$ and covariance $P^c_i = \hat P_i - K_i S_i K_i^{\mathsf T}$. Given an event where $i$ is missed, take the posterior to be the prediction $(\hat x_i, \hat P_i)$. Then the marginal posterior of track $i$ is the mixture $\beta_{i0} \mathcal N(\hat x_i, \hat P_i) + \sum_j \beta_{ij} \mathcal N(x_{ij}, P^c_i)$, and its mean and covariance are lines L6 and L7.

*Proof.* The marginal is the sum over events of the posterior probability of the event times the posterior of track $i$ given the event. The posterior of track $i$ depends only on what the event gives to $i$, so grouping the events by that gives the mixture. Write $\beta_j$ for $\beta_{ij}$, $\beta_0$ for $\beta_{i0}$, $K$ for $K_i$, and $\nu = \sum_j \beta_j \nu_{ij}$. The mean is $\beta_0 \hat x + \sum_j \beta_j (\hat x + K \nu_{ij}) = \hat x + K \nu$, which is line L6. The covariance of a mixture is the mean of the component covariances plus the spread of the component means:

$$
P = \beta_0 \hat P + (1 - \beta_0) P^c + \beta_0 (\hat x - x)(\hat x - x)^{\mathsf T} + \sum_j \beta_j (x_{ij} - x)(x_{ij} - x)^{\mathsf T}.
$$

Here $\hat x - x = -K \nu$ and $x_{ij} - x = K (\nu_{ij} - \nu)$. With $\sum_j \beta_j = 1 - \beta_0$,

$$
\sum_j \beta_j (\nu_{ij} - \nu)(\nu_{ij} - \nu)^{\mathsf T} + \beta_0 \nu \nu^{\mathsf T} = \sum_j \beta_j \nu_{ij} \nu_{ij}^{\mathsf T} - 2 \nu \nu^{\mathsf T} + (1 - \beta_0) \nu \nu^{\mathsf T} + \beta_0 \nu \nu^{\mathsf T} = \sum_j \beta_j \nu_{ij} \nu_{ij}^{\mathsf T} - \nu \nu^{\mathsf T}.
$$

Multiplying by $K$ on the left and $K^{\mathsf T}$ on the right gives line L7. $\square$

Two approximations remain and are not claimed exact. With $p_G < 1$, a missed track has a posterior that is the prediction with the gate cut out, not the prediction itself. And the next frame treats the tracks as independent Gaussians, while the true joint posterior couples them.

## Claim 3: one track gives the PDA weights

For $n = 1$ the events are "missed", of weight $1 - p_D p_G$, and "measurement $j$", of weight $p_D L_j / \lambda$. Multiplying the numerator and the denominator by $\lambda / p_D$ gives $\beta_j = L_j / (b + \sum_k L_k)$ and $\beta_0 = b / (b + \sum_k L_k)$ with $b = \lambda (1 - p_D p_G) / p_D$. These are the weights of the PDA filter of Bar-Shalom and Tse. $\square$

## Claim 4: the normalizer is a permanent, and computing it is #P-hard

Let $p_D = p_G = 1$ and $n = m$, and put $L_{ij} = 0$ for pairs outside the gates. Then $c = \operatorname{per}(L) / \lambda^n$.

*Proof.* A missed track gives the factor $1 - p_D p_G = 0$, so only events in which every track has a measurement have positive weight. With $n = m$ these are the permutations $\sigma$, with weight $\prod_i L_{i \sigma(i)} / \lambda^n$, which is 0 if some pair is outside a gate. The sum over all permutations is the [permanent](/permanent-computation/) divided by $\lambda^n$. $\square$

Valiant (1979) proved that the permanent of a 0-1 matrix is #P-complete to compute. Given a 0-1 matrix $A$, take the table with the gate holding exactly the pairs with $a_{ij} = 1$, $L_{ij} = 1$ there and $\lambda = 1$. Then $c = \operatorname{per}(A)$. So computing $c$ exactly from a table of likelihoods and gates is #P-hard. This does not rule out good approximations: for nonnegative matrices the permanent has a randomized approximation scheme, and practical trackers use cheaper approximations.

## Claim 5: the number of joint events

If every measurement is in every gate, the number of joint events is $\sum_{k=0}^{\min(n,m)} \binom{n}{k} \binom{m}{k} k!$.

*Proof.* An event with $k$ pairs is fixed by the set of $k$ detected tracks, the set of $k$ used measurements and a bijection between them. These choices are independent, and different choices give different events. $\square$

The depth-first search of the code visits each event once: at track $i$ it branches on "missed" and on each unused gated measurement, and a leaf at depth $n$ is exactly one event.
