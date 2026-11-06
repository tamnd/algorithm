---
tag: VR1MK5
kind: theorem
slug: ajtai-worst-case-to-average-case-reduction
name: Ajtai's worst-case to average-case reduction
aliases:
- Ajtai reduction
- Ajtai's reduction
- Ajtai's theorem
- worst-case to average-case reduction for SIS
- hardness of SIS from SIVP
area: number-theory/lattice-reduction
level: research
summary: Solving random lattice instances is at least as hard as solving worst-case SVP instances.
prereqs: [short-integer-solution, shortest-independent-vectors-problem, dual-lattice, gram-schmidt-orthogonalization]
see_also: [learning-with-errors, regev-lwe-hardness, ring-short-integer-solution, collision-resistance, gaussian-sampling-over-lattices, gpv-signature, lattice-based-cryptography, gap-svp]
sources:
  - paper: "M. Ajtai, Generating hard instances of lattice problems, Proceedings of the 28th ACM Symposium on Theory of Computing (STOC 1996)"
    locator: pages 99 to 108 (the first worst-case to average-case connection, for the function zA mod q)
  - paper: "D. Micciancio and O. Regev, Worst-case to average-case reductions based on Gaussian measures, SIAM Journal on Computing 37(1) (2007)"
    locator: pages 267 to 302 (the smoothing parameter, its bound by lambda_n, the moments of discrete Gaussians, and the reduction from SIVP and GapSVP to SIS)
  - paper: "C. Gentry, C. Peikert and V. Vaikuntanathan, Trapdoors for hard lattices and new cryptographic constructions, Proceedings of the 40th ACM Symposium on Theory of Computing (STOC 2008)"
    locator: pages 197 to 206 (the reduction with modulus q of order beta n^(1/2) and factor beta n^(1/2) up to logarithmic factors)
  - book: isbn:9780792376880
    title: Daniele Micciancio and Shafi Goldwasser, Complexity of Lattice Problems, A Cryptographic Perspective, Kluwer, 2002
    locator: Chapter 7 (a basis no longer than a set of independent vectors) and Chapter 8 (cryptographic functions from worst-case lattice problems)
  - paper: "C. Peikert, A decade of lattice cryptography, Foundations and Trends in Theoretical Computer Science 10(4) (2016)"
    locator: pages 283 to 424, Section 4.1 (SIS, its worst-case hardness, and the history of the parameters)
---

## Statement

Notation is that of the other pages in this area: a lattice is $L = L(B) = \{x B : x \in \mathbb{Z}^n\}$ for basis rows $b_1, \ldots, b_n$, with Gram-Schmidt vectors $b_i^*$ and coefficients $\mu_{ij}$, successive minima $\lambda_1(L) \le \cdots \le \lambda_n(L)$, and determinant $\det(L)$. The LLL parameter $\delta$ plays no role here. For a set $S$ of vectors, $\|S\|$ is the length of the longest one. Vectors are rows.

**The average-case problem.** Fix integers $n, m, q \ge 2$ and a real $\beta \ge 1$. An instance of the **short integer solution problem** $\mathrm{SIS}_{n,m,q,\beta}$ is a matrix $A \in \mathbb{Z}_q^{m \times n}$ chosen **uniformly at random**, with rows $a_1, \ldots, a_m$. A solution is an integer vector $z \in \mathbb{Z}^m$ with

$$z \ne 0, \qquad z A = \sum_{i=1}^m z_i a_i \equiv 0 \pmod q, \qquad \|z\| \le \beta.$$

So $z$ is a short nonzero vector of the $q$-ary lattice $\Lambda_q^\perp(A) = \{z \in \mathbb{Z}^m : z A \equiv 0 \pmod q\}$, a random lattice of rank $m$.

**The worst-case problem.** $\mathrm{SIVP}_\gamma$, the [shortest independent vectors problem](/shortest-independent-vectors-problem/) with factor $\gamma$: given **any** basis $B \in \mathbb{Z}^{n \times n}$ of a full-rank lattice $L$, find $n$ linearly independent vectors of $L$, each of length at most $\gamma \lambda_n(L)$.

**Theorem (Ajtai 1996, in the Gaussian form of Micciancio and Regev).** Let $n \ge 2$, $m \ge 1$, $\beta \ge 1$ and an integer modulus

$$q \ge 2 \beta \sqrt m \, n^{3/2}.$$

Suppose a probabilistic algorithm $\mathcal O$ runs in time at most $T$ and, on a uniformly random $A \in \mathbb{Z}_q^{m \times n}$, outputs a solution of $\mathrm{SIS}_{n,m,q,\beta}$ with probability at least $p > 0$, over the choice of $A$ and its own coins. Put

$$\varepsilon = \frac{p}{100 m}, \qquad \gamma = 48 \, \beta \sqrt{\frac{n \ln\!\big(2n(1 + 1/\varepsilon)\big)}{\pi}}.$$

Then there is a probabilistic algorithm that, given a basis $B$ of **any** full-rank integer lattice $L \subset \mathbb{Z}^n$, calls $\mathcal O$, runs in time polynomial in $n$, $m$, $1/p$ and the bit size of $B$, plus that many calls of time $T$, and with probability at least $1 - e^{-n}$ outputs $n$ linearly independent vectors of $L$ of length at most $\gamma \lambda_n(L)$.

**Cost model and what kind of reduction this is.**

- The reduction is **randomized**: it draws Gaussian samples and succeeds with probability $1 - e^{-n}$, for every input lattice. It is a Turing reduction, calling the average-case solver polynomially many times on independent random inputs.
- The **approximation factor** is $\gamma$. When $m$ and $1/p$ are bounded by a polynomial in $n$, $\ln(1/\varepsilon) = O(\log n)$, so $\gamma = O(\beta \sqrt{n \log n})$, and $q$ of polynomial size suffices whenever $\beta$ is polynomial.
- The analysis is in exact real arithmetic for the Gaussian samples. Micciancio and Regev show that rounding the samples to polynomially many digits changes nothing essential; the outputs are checked exactly in any case.

Ajtai's original statement used $\{0, 1\}$ inputs: finding a collision of $f_A(x) = x A \bmod q$ on $x \in \{0,1\}^m$ gives $z = x - x' \in \{-1, 0, 1\}^m$, a solution with $\beta = \sqrt m$, and its worst-case problems were approximate SIVP, approximating the length of the shortest basis, and the unique shortest vector problem, all with factors $n^c$ for a constant $c$.

## In plain words

Worst-case hardness usually says nothing about random instances: the hard ones may be rare. Cryptography needs random instances to be hard, since keys are random. Ajtai found the first problem where this gap closes: whoever solves **random** instances of a certain lattice problem even a small fraction of the time can solve **every** instance of a related one.

The random problem: given a table of random numbers modulo $q$, find a combination of its rows with small integer weights that adds up to zero modulo $q$. The worst-case problem: find $n$ independent short vectors in any lattice.

The proof blurs random points until, modulo the lattice, they look evenly spread, and records their positions inside a lattice cell on a grid of step $1/q$. This gives a random table. A short zero combination of its rows tells how to combine the points into a shorter lattice vector. Repeating shrinks them.

## Proof

**Gaussians.** For $s > 0$ let $\rho_s(x) = e^{-\pi \|x\|^2 / s^2}$ on $\mathbb{R}^n$. The continuous Gaussian of width $s$ has density $\rho_s(x)/s^n$. For a coset $L + c$ of a full-rank lattice, the **discrete Gaussian** $D_{L+c,s}$ gives each point $x \in L + c$ the probability $\rho_s(x) / \rho_s(L + c)$, where $\rho_s(X) = \sum_{x \in X} \rho_s(x)$. The **smoothing parameter** $\eta_\varepsilon(L)$ is the least $s$ with $\rho_{1/s}(L^* \setminus \{0\}) \le \varepsilon$, where $L^*$ is the [dual lattice](/dual-lattice/).

We quote three facts from Micciancio and Regev. Let $0 < \varepsilon < 1$.

- **(F1) Smoothing.** If $s \ge \eta_\varepsilon(L)$ and $x$ is a continuous Gaussian of width $s$, then $x \bmod L$ is within statistical distance $\varepsilon/2$ of the uniform distribution on $\mathbb{R}^n / L$.
- **(F2) Size of the smoothing parameter.** $\eta_\varepsilon(L) \le \sqrt{\ln(2n(1 + 1/\varepsilon))/\pi} \cdot \lambda_n(L)$.
- **(F3) Moments.** If $s \ge 2 \eta_\varepsilon(L)$, $x \sim D_{L+c,s}$ and $u$ is a unit vector, then $|\mathbb{E} \langle x, u \rangle| \le \frac{\varepsilon}{1 - \varepsilon} s$ and $\mathbb{E} \langle x, u \rangle^2 \le \big(\frac{1}{2\pi} + \frac{\varepsilon}{1 - \varepsilon}\big) s^2$.

Summing (F3) over an orthonormal basis gives $\|\mathbb{E} x\| \le \sqrt n \frac{\varepsilon}{1 - \varepsilon} s$ and $\mathbb{E}\|x\|^2 \le n \big(\frac{1}{2\pi} + \frac{\varepsilon}{1 - \varepsilon}\big) s^2$.

**Lemma 1 (a basis as short as a set of vectors).** Given a basis of $L$ and $n$ linearly independent vectors $S = (s_1, \ldots, s_n)$ of $L$, one can compute in polynomial time a basis $T$ of $L$ with $\|T\| \le \sqrt n \, \|S\|$.

*Proof.* Write $S = U B$ with $U$ an integer nonsingular matrix. Its Hermite normal form, computed with integer column operations, gives $U = R W$ with $W$ unimodular and $R$ lower triangular with nonzero diagonal (see [Hermite normal form](/hermite-normal-form/)). Then $T = W B$ is a basis of $L$, and $s_i = \sum_{j \le i} R_{ij} t_j$, so $s_i^* = R_{ii} t_i^*$ and $\|t_i^*\| \le \|s_i^*\| \le \|s_i\| \le \|S\|$. Size-reduce $T$, which keeps the $t_i^*$ and makes $|\mu_{ij}| \le 1/2$. Then

$$\|t_i\|^2 = \|t_i^*\|^2 + \sum_{j < i} \mu_{ij}^2 \|t_j^*\|^2 \le \Big(1 + \frac{i - 1}{4}\Big) \|S\|^2 \le n \|S\|^2. \qquad \square$$

**Lemma 2 (discrete Gaussians avoid hyperplanes).** Let $H$ be a linear hyperplane of $\mathbb{R}^n$, and suppose some $w \in L \setminus H$ has $\|w\| \le s$. Then for every $c$ and every affine hyperplane $H' = H + r$,

$$\Pr_{x \sim D_{L+c,s}}[x \in H'] \le \frac{e^\pi}{1 + e^\pi} < 0.959.$$

*Proof.* Let $C = (L + c) \cap H'$. Since $\|x + w\|^2 + \|x - w\|^2 = 2\|x\|^2 + 2\|w\|^2$, we have $\rho_s(x + w) \rho_s(x - w) = \rho_s(x)^2 e^{-2\pi\|w\|^2/s^2} \ge \rho_s(x)^2 e^{-2\pi}$, so the larger of $\rho_s(x \pm w)$ is at least $e^{-\pi} \rho_s(x)$, and $\rho_s(x) \le e^\pi (\rho_s(x + w) + \rho_s(x - w))$. The maps $x \mapsto x + w$ and $x \mapsto x - w$ send $C$ into $(L + c) \setminus H'$, because $w \notin H$, and their images are disjoint: $x + w = x' - w$ with $x, x' \in H'$ would put $2w = x' - x$ in $H$. Summing over $x \in C$ gives $\rho_s(C) \le e^\pi (\rho_s(L + c) - \rho_s(C))$. Divide by $\rho_s(L + c)$. $\square$

**One step.** Let $S \subset L$ be $n$ linearly independent vectors, let $s_\star$ be a longest one, and $H = \operatorname{span}(S \setminus \{s_\star\})$. The step is:

1. Compute $T$ by Lemma 1 and put $s = \|S\| / (24 \beta \sqrt n)$.
2. For $i = 1, \ldots, m$: draw a continuous Gaussian $x_i$ of width $s$; let $u_i \in [0, 1)^n$ be the fractional parts of the coordinates $x_i T^{-1}$; let $y_i = u_i T$, the point of the cell $\{u T : u \in [0,1)^n\}$ congruent to $x_i$ modulo $L$; and let $a_i = \lfloor q u_i \rceil \in \{0, \ldots, q\}^n$, rounded coordinatewise.
3. Call $\mathcal O$ on the matrix $A$ with rows $a_i \bmod q$. If its answer $z$ is not a solution, fail.
4. Output $v = \sum_i z_i \big(x_i - y_i + \tfrac1q a_i T\big)$.

**Lemma 3 (the step works when $S$ is long).** If $\|S\| > \gamma \lambda_n(L)$, the step outputs, with probability at least $0.015 \, p$, a vector $v \in L$ with $\|v\| \le \|S\|/2$ and $v \notin H$. Whatever $\|S\|$ is, an output $v$ always lies in $L$.

*Proof.* *Membership.* $x_i - y_i = \lfloor x_i T^{-1} \rfloor T \in L$. With integer representatives, $z A \equiv 0 \pmod q$ makes $\frac1q z A$ an integer vector, so $\sum_i z_i \frac1q a_i T = (\frac1q z A) T \in L$.

*Width.* By the choice of $\gamma$ and $s$, $s > 2 \sqrt{\ln(2n(1+1/\varepsilon))/\pi} \, \lambda_n(L)$, which by (F2) is at least $2 \eta_\varepsilon(L)$. The factor $2\sqrt{\ln(2n(1+1/\varepsilon))/\pi}$ exceeds 1 because $\varepsilon \le 1/100$, so also $s > \lambda_n(L)$.

*The oracle sees nearly uniform input.* By (F1) each $x_i \bmod L$, hence each $u_i$, is within statistical distance $\varepsilon/2$ of uniform on $[0, 1)^n$. If $u_i$ were uniform, $a_i \bmod q$ would be exactly uniform on $\mathbb{Z}_q^n$, since each coordinate $\lfloor q u \rceil$ takes the values $1, \ldots, q - 1$ on intervals of length $1/q$ and the value $0 \equiv q$ on two halves. The $m$ rows are independent, so $A$ is within $m \varepsilon / 2 \le p/200$ of uniform, and $\mathcal O$ succeeds with probability at least $p - p/200 \ge p/2$.

*What the oracle does not see.* Given $y_i$, the sample $x_i$ is a continuous Gaussian conditioned on the coset $L + y_i$, which is $D_{L + y_i, s}$, and the $x_i$ are independent. The answer $z$ depends only on $A$, a function of the $y_i$, and on the oracle's coins. So, conditioned on all $y_i$ and on a successful $z$, the $x_i$ are still independent with laws $D_{L+y_i,s}$.

*Length.* Write $v = X - E$ with $X = \sum_i z_i x_i$ and $E = \sum_i z_i (y_i - \frac1q a_i T)$. Each coordinate of $u_i - a_i/q$ is at most $\frac{1}{2q}$ in absolute value, so $\|y_i - \frac1q a_i T\| \le \frac{n}{2q} \|T\| \le \frac{n^{3/2}}{2q} \|S\|$, and $\sum_i |z_i| \le \sqrt m \|z\| \le \sqrt m \beta$. Hence $\|E\| \le \frac{\sqrt m \beta n^{3/2}}{2q} \|S\| \le \frac14 \|S\|$ by the bound on $q$. For $X$, (F3) with $\varepsilon \le 1/100$, so $\frac{\varepsilon}{1-\varepsilon} \le 0.0102$, gives

$$\|\mathbb{E} X\| \le \sqrt m \beta \sqrt n \, \tfrac{\varepsilon}{1 - \varepsilon} s \le 0.02 \, \beta s \sqrt n, \qquad \mathbb{E} \|X - \mathbb{E} X\|^2 = \sum_i z_i^2 \, \mathbb{E}\|x_i - \mathbb{E} x_i\|^2 \le 0.17 \, \beta^2 n s^2,$$

using $\sqrt m \, \varepsilon \le 1/100$ and $\frac{1}{2\pi} + 0.0102 < 0.17$. By [Markov's inequality](/markov-inequality/), $\|X - \mathbb{E} X\|^2 \le 17 \beta^2 n s^2$ with probability at least $0.99$, and then $\|X\| \le (\sqrt{17} + 0.02) \beta s \sqrt n < 4.2 \, \beta s \sqrt n < \frac14 \|S\|$. So $\|v\| \le \|S\|/2$ with probability at least $0.99$.

*Avoiding $H$.* Since $z \ne 0$, pick $j$ with $z_j \ne 0$ and condition further on all $x_i$ with $i \ne j$. Then $v \in H$ exactly when $x_j \in H + r$ for a fixed $r$, an affine hyperplane. The lattice has $n$ independent vectors of length at most $\lambda_n(L)$, not all in $H$, so some $w \in L \setminus H$ has $\|w\| \le \lambda_n(L) < s$. By Lemma 2, $v \notin H$ with probability at least $1/(1 + e^\pi) > 0.041$.

Together, given a successful $z$, both events hold with probability at least $0.041 - 0.01 = 0.031$, and the step succeeds with probability at least $\frac p2 \cdot 0.031 \ge 0.015 \, p$. $\square$

**Proof of the theorem.** Start with $S$ equal to the rows of $B$. In each round, run the step up to $K = \lceil (n + \ln R)/(0.015 \, p) \rceil$ times, with $R$ fixed below. Accept the first output $v$ that satisfies $\|v\| \le \|S\|/2$ and $v \notin H$, both checked exactly, and replace $s_\star$ by $v$. If no run is accepted, output $S$.

*$S$ is always valid.* Every output lies in $L$ by Lemma 3, and $v \notin \operatorname{span}(S \setminus \{s_\star\})$ keeps the $n$ vectors independent.

*Number of rounds.* All vectors that are longer than half of the current $\|S\|$ are replaced, one per accepted round, by vectors of length at most half of it, so after at most $n$ accepted rounds $\|S\|$ has halved. Since $\|S\| \ge \lambda_n(L) \ge 1$ for an integer lattice, there are at most $n (\lfloor \log_2 \|B\| \rfloor + 1)$ accepted rounds, hence at most $R = n (\lfloor \log_2 \|B\| \rfloor + 1) + 1$ rounds.

*Quality.* The output is wrong only if some round with $\|S\| > \gamma \lambda_n(L)$ rejected $K$ independent runs. By Lemma 3, the probability of that for one round is at most $(1 - 0.015 p)^K \le e^{-(n + \ln R)} = e^{-n} / R$, and a union bound over at most $R$ rounds gives at most $e^{-n}$.

*Time.* At most $R K$ runs of the step, each one call of $\mathcal O$ and polynomial work for Lemma 1, the samples and the checks. $\blacksquare$

**A worked instance of SIS.** For $q = 7$, $n = 2$, $m = 4$ and rows $a_1 = (1, 3)$, $a_2 = (2, 5)$, $a_3 = (4, 0)$, $a_4 = (6, 6)$, the vector $z = (-1, 2, 1, 0)$ gives $z A = (7, 7) \equiv 0$, with $\|z\|^2 = 6$. An exhaustive search over $\{-2, \ldots, 2\}^4$, which contains every $z$ with $\|z\|^2 \le 6$, finds no nonzero solution shorter than $\sqrt 6$, so $\lambda_1(\Lambda_7^\perp(A)) = \sqrt 6$; six vectors attain it. Here $A$ has rank 2 modulo 7, so $\det(\Lambda_7^\perp(A)) = 7^2$ and Minkowski's bound gives $\lambda_1 \le \sqrt m \, q^{n/m} = 2\sqrt 7 \approx 5.29$. The trivial solution $(7, 0, 0, 0)$ has length $q$, which is why the problem needs $\beta < q$.

## Consequences

- **Random SIS instances are hard if lattices are hard in the worst case.** For polynomial $m$ and $\beta$, an algorithm that solves a noticeable fraction of random $\mathrm{SIS}_{n,m,q,\beta}$ instances would solve $\mathrm{SIVP}_\gamma$ on every lattice with $\gamma = O(\beta \sqrt{n \log n})$, a problem for which the best known algorithms take time $2^{\Theta(n)}$ for polynomial $\gamma$; see [approximate SVP](/approximate-svp/).
- **Collision-resistant hashing.** For $m > n \log_2 q$, the function $f_A(x) = x A \bmod q$ on $\{0, 1\}^m$ compresses, so collisions exist by the pigeonhole principle, and any collision $x \ne x'$ gives the solution $x - x'$ with $\beta = \sqrt m$. So $f_A$ is a [collision-resistant](/collision-resistance/) [hash function](/hash-function/) family and in particular a [one-way function](/one-way-function/), under a worst-case assumption. This was observed by Goldreich, Goldwasser and Halevi in 1996.
- **GapSVP.** Applied to the dual lattice, an $\mathrm{SIVP}_\gamma$ solution $S'$ of $L^*$ gives $1/\|S'\| \le \lambda_1(L) \le n / \lambda_n(L^*) \le n\gamma / \|S'\|$ by the transference bounds $1 \le \lambda_1(L) \lambda_n(L^*) \le n$, so the theorem also bases SIS on [GapSVP](/gap-svp/) with factor $n \gamma$. Micciancio and Regev give a direct reduction with a smaller factor.
- **Lattice cryptography.** The reduction underlies [lattice-based cryptography](/lattice-based-cryptography/): the Ajtai-Dwork cryptosystem (1997), the [GPV signature](/gpv-signature/) built on [lattice Gaussian sampling](/gaussian-sampling-over-lattices/), and the structured [ring SIS](/ring-short-integer-solution/). The companion result for [learning with errors](/learning-with-errors/) is [Regev's reduction](/regev-lwe-hardness/), which uses the same Gaussian tools but is quantum.
- **A different notion of security.** The guarantee is about [worst-case](/worst-case-analysis/) lattices, not about an assumed input distribution, which is what [average-case analysis](/average-case-analysis/) of most other problems has to assume.

## Tightness

- **The modulus must exceed $\beta$.** If $\beta \ge q$, the vector $(q, 0, \ldots, 0)$ is always a solution, so SIS is trivial. The proof above uses $q \ge 2\beta \sqrt m \, n^{3/2}$; Gentry, Peikert and Vaikuntanathan needed only $q \ge \beta \cdot \omega(\sqrt{n \log n})$ for a prime $q$, and Micciancio and Peikert (2013) report reductions for $q \ge \beta n^c$ with any constant $c > 0$, for suitable parameters.
- **The factor.** The best known factor is $\gamma = \beta \cdot \tilde O(\sqrt n)$, of the same form as above. Since a solution must exist, $\beta$ is at least about $\sqrt m \, q^{n/m}$ by Minkowski's bound, so $\gamma$ is always at least of order $\sqrt n$.
- **No NP-hardness to be had.** For $\gamma \ge \sqrt{n / \log n}$, approximate SIVP and GapSVP are in NP $\cap$ coAM (Goldreich and Goldwasser), and for $\gamma \ge \sqrt n$ GapSVP is in NP $\cap$ coNP (Aharonov and Regev). So the worst-case problems in the theorem are not NP-hard unless the polynomial hierarchy collapses, and the theorem cannot base SIS on P $\ne$ NP.
- **Large factors are easy.** For $\gamma = 2^{O(n \log \log n / \log n)}$ the worst case is solved in polynomial time by block reduction ([BKZ](/bkz-algorithm/)) with an exact sieve on blocks of size about $\log n$, as in Ajtai, Kumar and Sivakumar, so the reduction carries meaning only for polynomial $\beta$. On random SIS instances, BKZ applied to $d \le m$ of the rows finds solutions of length near $\min_d \delta_0^d q^{n/d}$ for its root Hermite factor $\delta_0$, so concrete security also rests on experiments, not on the theorem alone.

## History

Ajtai's 1996 paper gave the first problem in NP believed hard on average whose average-case hardness follows from the worst-case hardness of a well-studied problem. His worst-case problems were approximate SIVP, the shortest basis problem and the unique shortest vector problem, with large polynomial factors. Ajtai and Dwork built a public-key cryptosystem on the unique-SVP variant in 1997, and Goldreich, Goldwasser and Halevi noted the collision resistance of Ajtai's function.

Cai and Nerurkar (1997) and Micciancio (2004, through almost perfect lattices) reduced the polynomial factor. Micciancio and Regev (2004 conference, 2007 journal) replaced the combinatorial core by Gaussian measures and the smoothing parameter, which gave factors almost linear in $n$ and the short proof followed above. Gentry, Peikert and Vaikuntanathan (2008) brought the factor to $\beta \cdot \tilde O(\sqrt n)$, and Micciancio's cyclic lattices (2002) led, through Lyubashevsky and Micciancio and through Peikert and Rosen (both 2006), to worst-case reductions for ideal lattices and ring SIS.

## References
