---
tag: 9QBY0D
kind: definition
slug: p-stable-distribution
name: p-stable distribution
aliases:
- stable distribution
- symmetric alpha-stable distribution
- Levy stable distribution
area: online-and-streaming/streaming-sketches
level: advanced
summary: A distribution whose linear combinations keep the same shape up to scale; Cauchy for p=1, Gaussian for p=2.
prereqs: [central-limit-theorem, moment-generating-function]
see_also: [indyk-p-stable-sketch, box-muller-transform, inverse-transform-sampling, random-variate-generation, johnson-lindenstrauss-lemma, e2lsh, frequency-moment-problem, random-projection]
sources:
  - book: isbn:9780471257097
    title: William Feller, An Introduction to Probability Theory and Its Applications, Volume II, second edition, Wiley, 1971
    locator: Section VI.1, Stable distributions, and Section XVII.5, Stable distributions and their domains of attraction
  - book: isbn:9780821845196
    title: V. M. Zolotarev, One-dimensional Stable Distributions, Translations of Mathematical Monographs 65, American Mathematical Society, 1986
    locator: Chapter 1 and Chapter 2 (characteristic functions, tails and moments)
  - book: isbn:9783030529147
    title: John P. Nolan, Univariate Stable Distributions, Springer, 2020
    locator: Chapter 1, Basic properties of univariate stable distributions, and Chapter 3 on simulation (to check)
  - paper: doi:10.1080/01621459.1976.10480344
    title: J. M. Chambers, C. L. Mallows and B. W. Stuck, A method for simulating stable random variables, Journal of the American Statistical Association 71(354), 1976
    locator: the simulation formula for symmetric stable variables
  - paper: doi:10.1016/0167-7152(95)00113-1
    title: Rafał Weron, On the Chambers-Mallows-Stuck method for simulating skewed stable random variables, Statistics and Probability Letters 28(2), 1996
    locator: the proof of the simulation formula (to check)
  - paper: doi:10.1145/1147954.1147955
    title: Piotr Indyk, Stable distributions, pseudorandom generators, embeddings, and data stream computation, Journal of the ACM 53(3), 2006
    locator: the section on p-stable distributions and the use of the median of absolute values (section number to check)
---

A $p$-stable distribution is a distribution on the real line such that a linear combination $\sum_i a_i X_i$ of independent copies has the same distribution as one copy scaled by the $\ell_p$ norm $\|a\|_p$. The Gaussian distribution is 2-stable and the Cauchy distribution is 1-stable. Symmetric $p$-stable laws exist exactly for $0 < p \le 2$. Paul Lévy studied them in the 1920s as the only possible limits of normalized sums of independent variables. In streaming, they turn a linear projection of a frequency vector into a random variable whose scale is $\|f\|_p$, which is the idea of the [Indyk p-stable sketch](/indyk-p-stable-sketch/).

## Definition

Let $0 < p \le 2$ and write $\|a\|_p = (\sum_i |a_i|^p)^{1/p}$ for $a \in \mathbb{R}^n$; for $p < 1$ this is not a norm, but the formula is the same. A distribution $\mathcal{D}$ on $\mathbb{R}$ is *$p$-stable* (strictly and symmetrically) if, for every $n$, every $a \in \mathbb{R}^n$, and independent $X_1, \ldots, X_n \sim \mathcal{D}$,
$$ \sum_{i=1}^n a_i X_i \;\overset{d}{=}\; \|a\|_p \, X, \qquad X \sim \mathcal{D}, $$
where $\overset{d}{=}$ means equality in distribution. The *standard* $p$-stable law has characteristic function
$$ \varphi_p(t) = \mathbb{E}[e^{itX}] = e^{-|t|^p}, $$
and $\gamma X$ for $\gamma > 0$ has scale $\gamma$, with characteristic function $e^{-\gamma^p |t|^p}$.

**Characterization.** A distribution is $p$-stable in this sense if and only if its characteristic function is $e^{-c|t|^p}$ for some $c \ge 0$, and such a distribution exists if and only if $0 < p \le 2$.

*Proof.* If $\varphi(t) = e^{-c|t|^p}$, then by independence
$$ \mathbb{E}\big[e^{it \sum_i a_i X_i}\big] = \prod_i e^{-c|a_i t|^p} = e^{-c \|a\|_p^p |t|^p} = \varphi(\|a\|_p t) = \mathbb{E}\big[e^{it \|a\|_p X}\big], $$
and a characteristic function determines the distribution. Conversely, if $\mathcal{D}$ is $p$-stable, take $a = (-1)$ to see that $X \overset{d}{=} -X$, so $\varphi$ is real and even. Taking $a = (1, \ldots, 1)$ gives $\varphi(t)^n = \varphi(n^{1/p} t)$, and with rational scales this gives $\varphi(t) = \varphi(1)^{|t|^p}$ for all $t$ by continuity; so $\varphi(t) = e^{-c|t|^p}$ with $e^{-c} = \varphi(1)$, where $\varphi(1) > 0$ because $\varphi(1) = \varphi(2^{-1/p})^2 \ge 0$ and $\varphi$ has no zeros (a zero at $t$ would give zeros at $t \cdot n^{-1/p}$ near 0, where $\varphi$ is close to 1).

For $p > 2$, suppose $e^{-|t|^p}$ is the characteristic function of some $X$. It is twice differentiable at 0 with second derivative 0. A characteristic function that is twice differentiable at 0 belongs to a variable with $\mathbb{E}[X^2] = -\varphi''(0)$ (Feller, Section XV.4). So $\mathbb{E}[X^2] = 0$, $X = 0$ almost surely, and $\varphi \equiv 1$, a contradiction. The same holds for $c > 0$. For $0 < p \le 2$, existence follows from the Chambers-Mallows-Stuck construction below, or from Pólya-type criteria; Feller (Section XVII.5) gives a proof. $\square$

**General stable laws.** The wider definition asks that for independent copies $X_1, X_2$ and $a, b > 0$ there are $c > 0$ and $d$ with $a X_1 + b X_2 \overset{d}{=} cX + d$. Then $c^\alpha = a^\alpha + b^\alpha$ for one $\alpha \in (0, 2]$, called the index, and the law has four parameters: the index $\alpha$, a skewness $\beta \in [-1, 1]$, a scale and a location. The $p$-stable laws of this page are the case $\alpha = p$, $\beta = 0$, location 0.

**The Chambers-Mallows-Stuck sampler.** Let $\Theta$ be uniform on $(-\pi/2, \pi/2)$ and $W$ exponential with mean 1, independent. Then
$$ X = \frac{\sin(p\Theta)}{(\cos \Theta)^{1/p}} \left( \frac{\cos((1 - p)\Theta)}{W} \right)^{(1-p)/p} $$
has the standard $p$-stable law (Chambers, Mallows and Stuck 1976; Weron 1996 gives a full proof). For $p = 1$ the second factor is 1 and $X = \tan \Theta$. For $p = 2$, $X = \sin(2\Theta) (\cos\Theta)^{-1/2} (\cos\Theta / W)^{-1/2} = 2 \sin \Theta \sqrt{W}$.

## Examples and non-examples

**The Gaussian law is 2-stable.** For $Z \sim N(0, \sigma^2)$, $\mathbb{E}[e^{itZ}] = e^{-\sigma^2 t^2/2}$, so the standard 2-stable law is $N(0, 2)$. It is the familiar fact that $\sum_i a_i Z_i \sim N(0, \sigma^2 \|a\|_2^2)$. The sampler gives $2 \sin\Theta \sqrt{W}$: here $\sqrt{2W}$ has the Rayleigh law and $\sin \Theta$ has the same arcsine law as the sine of a uniform angle on $(0, 2\pi)$, so $\sqrt{2W} \sin\Theta \sim N(0,1)$ as in the [Box-Muller transform](/box-muller-transform/), and $X = \sqrt{2} \cdot \sqrt{2W}\sin\Theta \sim N(0, 2)$.

**The Cauchy law is 1-stable.** The standard Cauchy density is $\frac{1}{\pi(1 + x^2)}$. The Laplace density $\frac12 e^{-|x|}$ has characteristic function $\int \frac12 e^{-|x|} e^{itx}\,dx = \frac{1}{1 + t^2}$. Fourier inversion of this pair gives $\frac12 e^{-|x|} = \frac{1}{2\pi}\int \frac{e^{-itx}}{1 + t^2}\,dt$, that is, $\int \frac{e^{-itx}}{\pi(1 + t^2)}\,dt = e^{-|x|}$. After renaming the variables, this says that the Cauchy density has characteristic function $e^{-|t|}$. The sampler gives $\tan\Theta$, and $\Pr[\tan\Theta \le x] = \frac12 + \frac1\pi \arctan x$ is the Cauchy distribution function; this is [inverse transform sampling](/inverse-transform-sampling/). The ratio of two independent standard normal variables is also standard Cauchy.

**The two norms in one example.** Take $a = (3, -4)$. For independent standard Cauchy $X_1, X_2$, $3X_1 - 4X_2$ has the law of $7X$, since $\|a\|_1 = 7$. For independent standard normal $Z_1, Z_2$, $3Z_1 - 4Z_2$ has the law of $5Z$, since $\|a\|_2 = 5$. So the scale of the combination reads off a different norm of $a$ for each $p$.

**Median of the absolute value.** For the standard Cauchy law, $\Pr[|\tan\Theta| \le 1] = \Pr[|\Theta| \le \pi/4] = 1/2$, so the median of $|X|$ is exactly 1. For $N(0, 2)$, the median of $|X|$ is $\sqrt{2}\,\Phi^{-1}(3/4) \approx \sqrt{2} \cdot 0.67449 \approx 0.95387$. For other $p$ there is no closed form, and the median is computed numerically. The [Indyk p-stable sketch](/indyk-p-stable-sketch/) divides by this number.

**Heavy tails.** For $p < 2$ the standard law satisfies $\Pr[|X| > x] \sim C_p x^{-p}$ as $x \to \infty$, with a constant $C_p > 0$, so $\mathbb{E}|X|^r < \infty$ exactly when $r < p$ (Zolotarev 1986). For the Cauchy law, $\Pr[|X| > x] = 1 - \frac2\pi \arctan x \sim \frac{2}{\pi x}$, and $\mathbb{E}|X| = \int \frac{|x|}{\pi(1+x^2)}dx = \infty$. So for $p < 2$ the mean of $|X|^p$ is not available, and an estimator must use a median or another quantile instead of an average. For the same reason no $p$-stable law with $p < 2$ has a [moment generating function](/moment-generating-function/).

**Limits of sums.** If $Y_1, Y_2, \ldots$ are independent and identically distributed and symmetric with $\Pr[|Y| > x] \sim C x^{-p}$ for some $0 < p < 2$, then $n^{-1/p}(Y_1 + \cdots + Y_n)$ converges in distribution to a scaled $p$-stable law. This generalizes the [central limit theorem](/central-limit-theorem/), which is the case of finite variance and $p = 2$ (Feller, Section XVII.5).

**Non-example: the uniform law.** For independent $U_1, U_2$ uniform on $[-1, 1]$, $U_1 + U_2$ has the triangular density on $[-2, 2]$, which is not a scaled uniform density. So no $p$ works.

**Non-example: the Rademacher law.** For independent $\pm 1$ signs $S_1, S_2$, $S_1 + S_2$ is 0 with probability $1/2$, while a scaled sign is never 0. Random signs are good for $p = 2$ only in expectation, through $\mathbb{E}[(\sum_i a_i S_i)^2] = \|a\|_2^2$, which is what the [AMS sketch](/ams-sketch/) uses.

**Non-example: the Laplace law.** Its characteristic function is $\frac{1}{1+t^2}$. The sum of two independent copies has $\frac{1}{(1+t^2)^2}$, which is not of the form $\frac{1}{1 + c^2 t^2}$. So the Laplace law is not stable, even though it is symmetric and has exponential tails.

**Non-example: $p > 2$.** By the characterization, $e^{-|t|^3}$ is not a characteristic function. So there is no 3-stable law, and $F_3$ cannot be estimated by a stable projection. This agrees with the polynomial space lower bounds for $F_k$, $k > 2$, on the [frequency moment problem](/frequency-moment-problem/).

**A stable law that is not symmetric.** The Lévy distribution, with density $\frac{1}{\sqrt{2\pi}} x^{-3/2} e^{-1/(2x)}$ for $x > 0$, is stable with index $1/2$ and skewness $\beta = 1$. It is the law of $1/Z^2$ for $Z \sim N(0,1)$. It satisfies $X_1 + X_2 \overset{d}{=} 4X$, but $X_1 - X_2$ does not have the law of a multiple of $X$, because $X > 0$. So it is not $p$-stable in the symmetric sense of this page.

## Related definitions

- **Index and skewness.** The general stable family has an index $\alpha \in (0, 2]$ and a skewness $\beta \in [-1, 1]$; the $p$-stable laws here are $\alpha = p$, $\beta = 0$. Skewed laws with $\alpha < 1$ and $\beta = 1$ live on $(0, \infty)$.
- **Domain of attraction.** The set of distributions whose normalized sums converge to a given stable law. Stable laws are exactly the possible limits of such sums.
- **Max-stable and min-stable laws.** Laws that keep their shape under maxima or minima instead of sums, such as the Fréchet and Gumbel laws, form a different family from extreme value theory. The minimum of independent exponential variables is again exponential, and some sketches for distinct elements use this property.
- **Stable random projections.** A matrix with independent $p$-stable entries maps $x$ to a vector whose coordinates are independent copies of $\|x\|_p X$. For $p = 2$ these are the Gaussian projections of the [Johnson-Lindenstrauss lemma](/johnson-lindenstrauss-lemma/) and [random projection](/random-projection/); for $p = 1$ and $p = 2$ they also give the hash functions of [E2LSH](/e2lsh/).
- **Sampling.** The [random variate generation](/random-variate-generation/) methods for Gaussian and Cauchy variables are special cases of the Chambers-Mallows-Stuck formula.

## References
