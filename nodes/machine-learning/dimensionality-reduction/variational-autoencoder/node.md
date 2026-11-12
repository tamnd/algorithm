---
tag: GZ4VWM
kind: model
slug: variational-autoencoder
name: Variational autoencoder
aliases:
- VAE
- auto-encoding variational Bayes
area: machine-learning/dimensionality-reduction
level: advanced
summary: "A latent variable model with a neural decoder p(x|z), fitted with a neural encoder q(z|x) by maximizing the ELBO with reparameterized gradients z = mu + sigma * eps."
prereqs: [autoencoder, variational-inference, evidence-lower-bound]
see_also: [probabilistic-pca, black-box-variational-inference, wake-sleep-algorithm, reinforce, monte-carlo-integration, importance-sampling, expectation-maximization, factor-analysis]
sources:
  - paper: "Diederik P. Kingma and Max Welling, Auto-encoding variational Bayes, ICLR 2014, arXiv:1312.6114"
    title: Kingma and Welling 2014
    locator: "Section 2.3 (the SGVB estimator and the AEVB algorithm), Section 2.4 (the reparameterization trick), Section 3 (the variational autoencoder with Gaussian encoder and decoder) and Appendix B (the closed form of -KL for diagonal Gaussians)"
  - paper: "Danilo Jimenez Rezende, Shakir Mohamed and Daan Wierstra, Stochastic backpropagation and approximate inference in deep generative models, Proceedings of ICML 2014, PMLR 32(2):1278-1286"
    title: Rezende, Mohamed and Wierstra 2014
    locator: stochastic backpropagation through Gaussian latent variables and a recognition model trained jointly with the generative model
  - paper: doi:10.1561/2200000056
    title: "Diederik P. Kingma and Max Welling, An introduction to variational autoencoders, Foundations and Trends in Machine Learning 12(4):307-392, 2019"
    locator: "Chapter 2 (the ELBO, its gradients and the reparameterization trick) and the discussion of posterior collapse and its remedies"
  - paper: "Samuel R. Bowman, Luke Vilnis, Oriol Vinyals, Andrew M. Dai, Rafal Jozefowicz and Samy Bengio, Generating sentences from a continuous space, Proceedings of CoNLL 2016"
    title: Bowman et al. 2016
    locator: with a strong recurrent decoder the KL term goes to zero and the code is ignored; KL annealing and word dropout as remedies
  - paper: "James Lucas, George Tucker, Roger Grosse and Mohammad Norouzi, Don't blame the ELBO! A linear VAE perspective on posterior collapse, Advances in Neural Information Processing Systems 32 (NeurIPS 2019)"
    title: Lucas, Tucker, Grosse and Norouzi 2019
    locator: the linear VAE has the stationary points of probabilistic PCA, and posterior collapse appears already in the marginal likelihood when the observation noise is large
  - paper: "Michael E. Tipping and Christopher M. Bishop, Probabilistic principal component analysis, Journal of the Royal Statistical Society, Series B 61(3):611-622, 1999"
    title: Tipping and Bishop 1999
    locator: the maximum likelihood weights W = U (Lambda - sigma^2 I)^(1/2) R, with zero columns for eigenvalues below the noise variance
---

A variational autoencoder (VAE) is a generative model with hidden codes, together with a way to fit it. The model draws a code $z$ from a simple prior, usually $\mathcal{N}(0, I)$, and then draws the data point $x$ from a distribution $p_\theta(x \mid z)$ whose parameters come from a neural network, the *decoder*. The exact likelihood $p_\theta(x) = \int p_\theta(x \mid z) p(z)\, dz$ cannot be computed, so a second network, the *encoder*, outputs an approximate posterior $q_\phi(z \mid x)$, and both networks are trained together to maximize the [evidence lower bound](/evidence-lower-bound/) (ELBO). The key step is the *reparameterization* $z = \mu + \sigma \odot \varepsilon$ with $\varepsilon \sim \mathcal{N}(0, I)$, which moves the randomness out of the parameters so that the gradient of the ELBO can be estimated by plain [backpropagation](/backpropagation/). Kingma and Welling (2014) and Rezende, Mohamed and Wierstra (2014) introduced the method at the same time. It is [variational inference](/variational-inference/) with one shared encoder for all data points (amortized inference), and its encoder gives a reduction of the dimension like the code of an [autoencoder](/autoencoder/).

## The machine

A VAE with code size $k$ for data in $\mathbb{R}^d$ has:

- **The prior** $p(z) = \mathcal{N}(z;\, 0, I_k)$.
- **The decoder** $p_\theta(x \mid z)$, for example $\mathcal{N}(x;\, g_\theta(z), s^2 I_d)$ for real data, or independent Bernoulli variables with means $g_\theta(z)$ for binary data, where $g_\theta$ is a neural network.
- **The encoder** $q_\phi(z \mid x) = \mathcal{N}\big(z;\, \mu_\phi(x), \operatorname{diag}(\sigma_\phi^2(x))\big)$, a Gaussian with a diagonal covariance, whose mean and log variance are the outputs of a neural network.

For one data point the objective is

$$\mathcal{L}(\theta, \phi; x) = \mathbb{E}_{q_\phi(z \mid x)}\big[\log p_\theta(x \mid z)\big] - \mathrm{KL}\big(q_\phi(z \mid x) \,\|\, p(z)\big) \le \log p_\theta(x).$$

The first term rewards codes that decode to $x$ (a reconstruction term), and the second keeps the codes close to the prior (a regularizer). For a diagonal Gaussian encoder the KL term has the closed form

$$\mathrm{KL}\big(\mathcal{N}(\mu, \operatorname{diag}\sigma^2) \,\|\, \mathcal{N}(0, I)\big) = -\frac{1}{2} \sum_{j=1}^{k} \big(1 + \log \sigma_j^2 - \mu_j^2 - \sigma_j^2\big).$$

The first term is estimated with $L$ samples (often $L = 1$) through the reparameterization

$$z^{(l)} = \mu_\phi(x) + \sigma_\phi(x) \odot \varepsilon^{(l)}, \qquad \varepsilon^{(l)} \sim \mathcal{N}(0, I_k),$$

$$\widehat{\mathcal{L}}(\theta, \phi; x) = \frac{1}{L} \sum_{l=1}^{L} \log p_\theta\big(x \mid z^{(l)}\big) - \mathrm{KL}\big(q_\phi(z \mid x) \,\|\, p(z)\big).$$

Now $\widehat{\mathcal{L}}$ is a differentiable function of $\theta$ and $\phi$ for fixed $\varepsilon$, so its gradient comes from backpropagation through the decoder, the sample and the encoder. Training averages $\nabla \widehat{\mathcal{L}}$ over a minibatch and takes a step of a stochastic gradient method, usually Adam (Algorithm 1 of Kingma and Welling 2014).

**The linear Gaussian VAE.** The implementation uses $\mu = A x + a$, $\log \sigma^2 = B x + b$ and $p(x \mid z) = \mathcal{N}(C z + c, s^2 I)$, with the gradient written out by hand. For this model the expectation in $\mathcal{L}$ and the exact $\log p(x) = \log \mathcal{N}(x;\, c, C C^\top + s^2 I)$ are also known in closed form, which lets the tests check the bound, the gradient and the training.

## What it counts

- **The ELBO** of each point, a lower bound on its log likelihood. The mean ELBO over a test set is the usual score of a VAE, and a tighter estimate of $\log p(x)$ comes from importance sampling with $q$ as the proposal.
- **The code distribution** $q_\phi(z \mid x)$. Its mean $\mu_\phi(x)$ is the reduced representation of $x$; $\sigma_\phi(x)$ says how sure the encoder is.
- **Samples.** New data come from $z \sim \mathcal{N}(0, I)$ and $x \sim p_\theta(x \mid z)$. Decoding the points of a grid in a two-dimensional code space shows what the model has learned.
- **The rate and the distortion.** The KL term (in nats) is the "rate", the amount of information the code carries about $x$; the negative reconstruction term is the "distortion".

An example of the closed form. For $\mu = (0.7, -1.2)$ and $\sigma^2 = (0.3, 2.0)$,

$$\mathrm{KL} = -\tfrac{1}{2}\big[(1 + \ln 0.3 - 0.49 - 0.3) + (1 + \ln 2 - 1.44 - 2)\big] = -\tfrac{1}{2}(-0.99397 - 1.74685) = 1.37041.$$

A Monte Carlo estimate of $\mathbb{E}_q[\log q(z) - \log p(z)]$ from 100,000 seeded samples gives $1.3762$ with a standard error of $0.0061$, within one standard error.

An example of training. Take 300 points $x = (2, 1) z + (1, -0.5) + \text{noise}$ with $z \sim \mathcal{N}(0, 1)$ and noise $\mathcal{N}(0, 0.25 I)$. The sample covariance has the eigenvalues $5.447$ and $0.268$. A linear VAE with $k = 1$, trained with Adam for 3000 steps of 16 points, raises the mean ELBO from $-5.624$ to $-3.043$, while the exact mean $\log p(x)$ is $-3.032$, a gap of $0.011$ nats. The decoder ends at $C \approx (2.04, 1.02)$ and $s^2 \approx 0.267$, close to the probabilistic PCA answer: $s^2 = 0.268$ (the smaller eigenvalue) and $\|C\|^2 = 5.447 - 0.268 = 5.179$ (the learned value is $5.193$).

## Relation to other models

- **Autoencoder.** The encoder and the decoder play the roles of $f$ and $g$ of an [autoencoder](/autoencoder/), and with $\sigma \to 0$ and a Gaussian decoder the reconstruction term becomes a scaled squared error. The KL term and the noise in $z$ make the code space smooth enough to sample from.
- **Probabilistic PCA and factor analysis.** With a linear Gaussian decoder $p(x \mid z) = \mathcal{N}(C z + c, s^2 I)$ the model is [probabilistic PCA](/probabilistic-pca/) (with a diagonal noise covariance it is [factor analysis](/factor-analysis/)). Its exact posterior is Gaussian, and its maximum likelihood fit is known in closed form (Tipping and Bishop 1999).
- **EM.** When the posterior can be computed exactly, maximizing the ELBO in $q$ and then in $\theta$ is the [EM algorithm](/expectation-maximization/). The VAE replaces the exact E step by a single gradient step on a shared encoder.
- **Black-box variational inference.** [Black-box VI](/black-box-variational-inference/) fits a separate $q$ per data set with the score function ([REINFORCE](/reinforce/)) estimator, which works for any model but has a higher variance. The VAE needs a continuous $z$ and a differentiable $p_\theta$, and in return gets a low-variance gradient.
- **Helmholtz machine.** The [wake-sleep algorithm](/wake-sleep-algorithm/) also trains a recognition network together with a generative network, but its sleep phase optimizes a different objective. The VAE trains both networks on the same bound.

## Known results in the model

### The ELBO is a lower bound with a known gap

For every $q(z \mid x)$ with the same support as the posterior,

$$\log p_\theta(x) = \mathcal{L}(\theta, \phi; x) + \mathrm{KL}\big(q_\phi(z \mid x) \,\|\, p_\theta(z \mid x)\big).$$

*Proof.* Write $\log p_\theta(x) = \mathbb{E}_q[\log p_\theta(x)]$ and $p_\theta(x) = p_\theta(x \mid z) p(z) / p_\theta(z \mid x)$. Then $\log p_\theta(x) = \mathbb{E}_q\big[\log \frac{p_\theta(x \mid z) p(z)}{q(z \mid x)}\big] + \mathbb{E}_q\big[\log \frac{q(z \mid x)}{p_\theta(z \mid x)}\big]$, and the first term is $\mathcal{L}$. $\square$

Since a KL divergence is not negative, $\mathcal{L} \le \log p_\theta(x)$, with equality exactly when $q$ is the true posterior. So raising $\mathcal{L}$ in $\phi$ moves $q$ toward the posterior, and raising it in $\theta$ raises a lower bound on the likelihood. In the tests, for 20 random linear models the ELBO is below $\log p(x)$, and for a decoder with orthogonal columns, whose true posterior is a diagonal Gaussian, setting $q$ to that posterior makes the two equal to $10^{-12}$.

### The closed form KL

For $q = \mathcal{N}(\mu, \operatorname{diag}\sigma^2)$ and $p = \mathcal{N}(0, I)$, both factor over the coordinates, so the KL is a sum over $j$ of one-dimensional terms. For one coordinate, $\log q(z) - \log p(z) = -\frac{1}{2}\log \sigma^2 - \frac{(z - \mu)^2}{2\sigma^2} + \frac{z^2}{2}$. Under $q$, $\mathbb{E}[(z - \mu)^2] = \sigma^2$ and $\mathbb{E}[z^2] = \mu^2 + \sigma^2$, so the expectation is $-\frac{1}{2}\log \sigma^2 - \frac{1}{2} + \frac{1}{2}(\mu^2 + \sigma^2)$, which is the formula above (Kingma and Welling 2014, Appendix B).

### The reparameterized gradient is unbiased

Let $z = \mu + \sigma \varepsilon$ with $\varepsilon \sim \mathcal{N}(0, 1)$, and let $f$ be differentiable with $\mathbb{E}|f'(\mu + \sigma\varepsilon)|(1 + |\varepsilon|)$ finite near the current $(\mu, \sigma)$. Then

$$\frac{\partial}{\partial \mu} \mathbb{E}_{z \sim \mathcal{N}(\mu, \sigma^2)} [f(z)] = \mathbb{E}_\varepsilon\big[f'(\mu + \sigma\varepsilon)\big], \qquad \frac{\partial}{\partial \sigma} \mathbb{E}[f(z)] = \mathbb{E}_\varepsilon\big[f'(\mu + \sigma\varepsilon)\, \varepsilon\big].$$

*Proof.* The distribution of $\varepsilon$ does not depend on $(\mu, \sigma)$, so $\mathbb{E}[f(z)] = \mathbb{E}_\varepsilon[f(\mu + \sigma\varepsilon)]$, and the integrability condition lets the derivative pass inside the expectation (dominated convergence). $\square$

For $f(z) = z^2$ the exact gradients are $2\mu$ and $2\sigma$, and the estimators $2(\mu + \sigma\varepsilon)$ and $2(\mu + \sigma\varepsilon)\varepsilon$ have exactly these means. The tests check this with 50,000 samples, and also check that the average of 10,000 one-sample ELBO gradients of the linear VAE matches the gradient of the closed form ELBO in every parameter, within 5 standard errors. The score function estimator $f(z) \nabla \log q(z)$ is also unbiased, but its variance is usually much larger.

### The linear VAE is probabilistic PCA

With a linear Gaussian decoder, the maximum of $\mathcal{L}$ over all $q$ is $\log p_\theta(x)$, so the best decoder is the maximum likelihood fit of probabilistic PCA: $C = U_k(\Lambda_k - s^2 I)^{1/2} R$ for the top $k$ eigenvectors $U_k$ and eigenvalues $\Lambda_k$ of the sample covariance, an orthogonal $R$, and $s^2$ equal to the mean of the other eigenvalues (Tipping and Bishop 1999). Lucas, Tucker, Grosse and Norouzi (2019) showed that the linear VAE with a diagonal Gaussian encoder keeps these optima. The training example above lands near this answer.

### Posterior collapse

A VAE can learn to ignore its code: $q_\phi(z \mid x) \approx p(z)$ for every $x$, the KL term goes to 0, and the decoder models $x$ without $z$. Bowman et al. (2016) saw this with strong recurrent decoders for text, which can model the data well with no code at all. Lucas et al. (2019) showed that it already happens in the linear model, as a property of the likelihood: in the probabilistic PCA fit, the column of $C$ for an eigenvalue $\lambda_j \le s^2$ is zero, so if the noise $s^2$ is fixed too large, those code dimensions carry no information. In the example data, with $s^2$ fixed at 10, above both eigenvalues, the same 3000 steps of training give $C \approx (0.02, -0.03)$ and a mean KL of $4 \times 10^{-6}$ nats. Common remedies are to learn the noise variance, to raise the weight of the KL term slowly from 0 to 1 during training (KL annealing), to give each code dimension a minimum KL budget ("free bits"), or to make the decoder weaker.

### Other limits

- **The amortization gap.** One encoder for all points may fit each posterior worse than a separate $q$ per point, so the ELBO of a VAE can be below the best ELBO in its family.
- **The family gap.** A diagonal Gaussian $q$ cannot match a correlated or multimodal posterior. Normalizing flows and importance weighted bounds narrow this gap.
- **Blurry samples.** With a Gaussian decoder of fixed variance, samples of images tend to be blurry, since the squared error averages over plausible outputs.

## References
