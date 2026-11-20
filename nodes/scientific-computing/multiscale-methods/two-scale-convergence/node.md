---
tag: DBXJ24
kind: theorem
slug: two-scale-convergence
name: Two-scale convergence
area: scientific-computing/multiscale-methods
level: advanced
summary: Bounded sequences in L^2 have subsequences that converge to a function of both the slow and fast variables, which justifies homogenization.
prereqs: [periodic-homogenization, sobolev-space]
see_also: [representative-volume-element, weak-formulation, lax-milgram-theorem, multiscale-finite-element-method, heterogeneous-multiscale-method, multiscale-modeling]
sources:
  - paper: doi:10.1137/0520043
    title: Gabriel Nguetseng, A general convergence result for a functional related to the theory of homogenization, SIAM Journal on Mathematical Analysis 20(3), 1989, 608-623
    locator: Theorem 1 (p. 611, the compactness result) and Theorem 3 (p. 618, the gradients of bounded sequences in H^1)
  - paper: doi:10.1137/0523084
    title: Gregoire Allaire, Homogenization and two-scale convergence, SIAM Journal on Mathematical Analysis 23(6), 1992, 1482-1518
    locator: Definition 1.1 and Theorem 1.2 (p. 1485, compactness), Proposition 1.14 (p. 1491, the H^1 case), and the proof of the homogenized equation
  - book: isbn:9780387738284
    title: Grigorios A. Pavliotis and Andrew M. Stuart, Multiscale Methods, Averaging and Homogenization, Texts in Applied Mathematics 53, Springer, 2008
    locator: the chapter on the rigorous theory of homogenization for elliptic PDEs (two-scale convergence)
---

Two-scale convergence is a form of weak convergence for functions that oscillate on a small scale $\varepsilon$. A sequence $u_\varepsilon$ two-scale converges to a function $u_0(x, y)$ of the slow variable $x$ and the fast periodic variable $y$ if its integrals against all test functions $\psi(x, x/\varepsilon)$ converge to the integrals of $u_0$ against $\psi(x, y)$. The compactness theorem of Nguetseng (1989), in the form of Allaire (1992), says that every bounded sequence in $L^2$ has such a subsequence. Unlike the weak limit, which keeps only the mean over the period, the two-scale limit keeps the profile of the oscillations, and this is what makes it a short proof of [periodic homogenization](/periodic-homogenization/).

## Statement

Let $\Omega \subset \mathbb R^N$ be a bounded open set, let $Y = [0, 1)^N$ be the unit cell, and let $C_\#(Y)$ be the continuous functions on $\mathbb R^N$ that are $Y$-periodic. Let $\varepsilon \to 0$ along a sequence.

**Definition.** A sequence $(u_\varepsilon)$ in $L^2(\Omega)$ *two-scale converges* to $u_0 \in L^2(\Omega \times Y)$ if, for every $\psi \in \mathcal D(\Omega; C^\infty_\#(Y))$ (smooth, with compact support in $x$ and periodic in $y$),

$$\lim_{\varepsilon \to 0} \int_\Omega u_\varepsilon(x)\, \psi\Big(x, \frac{x}{\varepsilon}\Big)\, dx = \int_\Omega \int_Y u_0(x, y)\, \psi(x, y)\, dy\, dx.$$

**Theorem (Nguetseng 1989, Theorem 1; Allaire 1992, Theorem 1.2).** If $\sup_\varepsilon \|u_\varepsilon\|_{L^2(\Omega)} < \infty$, then there are a subsequence $\varepsilon' \to 0$ and a function $u_0 \in L^2(\Omega \times Y)$ such that $u_{\varepsilon'}$ two-scale converges to $u_0$. The limit also holds for every $\psi \in C(\overline\Omega; C_\#(Y))$, and $\|u_0\|_{L^2(\Omega \times Y)} \le \liminf \|u_{\varepsilon'}\|_{L^2(\Omega)}$.

The periodicity is essential: the fast variable lives on the torus $\mathbb R^N / \mathbb Z^N$, and the test functions must be continuous in $y$ (or belong to a similar admissible class). The sequence itself needs no periodicity and no smoothness.

## In plain words

Take a family of functions that wiggle faster and faster, such as a wave whose wavelength shrinks. The usual weak limit sees only their average, so a fast wave around zero looks like zero. Two-scale convergence keeps one more piece of information. It looks at the function through test functions that wiggle at the same rate, and it records the shape of one wiggle at each point. The limit is then a function of two variables: where you are, and where you are inside the current wiggle. The theorem says that this limit always exists for some subsequence, as long as the functions stay bounded in size. This is enough to pass to the limit in the equations of homogenization.

## Proof

Let $X = C(\overline\Omega; C_\#(Y))$, the continuous functions on $\overline\Omega \times \mathbb R^N$ that are periodic in $y$, with the maximum norm. $X$ is the space of continuous functions on the compact set $\overline\Omega \times \mathbb T^N$, so it is a separable Banach space, and it contains $\mathcal D(\Omega; C^\infty_\#(Y))$.

**Lemma (mean value).** For $g \in X$, $\lim_{\varepsilon \to 0} \int_\Omega g(x, x/\varepsilon)\, dx = \int_\Omega \int_Y g(x, y)\, dy\, dx$.

*Proof of the lemma.* $g$ is uniformly continuous on $\overline\Omega \times \mathbb T^N$; let $\omega$ be its modulus of continuity in $x$, uniform in $y$. Cut $\mathbb R^N$ into the cubes $Q_k = \varepsilon(k + Y)$, $k \in \mathbb Z^N$, and let $x_k$ be the corner $\varepsilon k$. For a cube $Q_k \subset \Omega$, the change of variables $y = x/\varepsilon - k$ gives $\int_{Q_k} g(x_k, x/\varepsilon)\, dx = \varepsilon^N \int_Y g(x_k, y)\, dy = \int_{Q_k} \int_Y g(x_k, y)\, dy\, dx$. Replacing $x_k$ by $x$ in both integrals changes each by at most $\omega(\varepsilon \sqrt N)\, |Q_k|$. So the difference of the two sides of the lemma, restricted to the union of the cubes inside $\Omega$, is at most $2\omega(\varepsilon \sqrt N)\, |\Omega|$. The rest of $\Omega$ lies in $S_\varepsilon = \{x \in \Omega : \operatorname{dist}(x, \partial\Omega) \le \varepsilon \sqrt N\}$. These sets decrease to the empty set as $\varepsilon \to 0$, because $\Omega$ is open, and $|\Omega| < \infty$, so $|S_\varepsilon| \to 0$. On $S_\varepsilon$ both integrands are bounded by $\max |g|$. Hence the difference tends to 0. No regularity of $\partial\Omega$ is needed. $\square$

*Proof of the theorem.* Let $C = \sup_\varepsilon \|u_\varepsilon\|_{L^2(\Omega)}$ and define $L_\varepsilon(\psi) = \int_\Omega u_\varepsilon(x)\, \psi(x, x/\varepsilon)\, dx$ for $\psi \in X$. By the Cauchy-Schwarz inequality,

$$|L_\varepsilon(\psi)| \le \|u_\varepsilon\|_{L^2(\Omega)}\, \Big\| \psi\Big(\cdot, \frac{\cdot}{\varepsilon}\Big) \Big\|_{L^2(\Omega)} \le C\, |\Omega|^{1/2} \max |\psi|, \tag{1}$$

so $(L_\varepsilon)$ is a bounded sequence in the dual $X^*$. Since $X$ is separable, a diagonal argument on a countable dense subset of $X$ gives a subsequence $\varepsilon'$ and $L \in X^*$ with $L_{\varepsilon'}(\psi) \to L(\psi)$ for every $\psi \in X$ (the sequential Banach-Alaoglu theorem). Apply the lemma to $g = |\psi|^2 \in X$ in the middle term of (1), and use $\|u_{\varepsilon'}\|$ along a further subsequence that realizes $c = \liminf \|u_{\varepsilon'}\|_{L^2(\Omega)}$:

$$|L(\psi)| = \lim |L_{\varepsilon'}(\psi)| \le c\, \|\psi\|_{L^2(\Omega \times Y)} \quad \text{for all } \psi \in X.$$

So $L$ is continuous on $X$ for the norm of $L^2(\Omega \times Y)$. The restrictions to $\Omega \times Y$ of the functions of $X$ are dense in $L^2(\Omega \times Y)$, because $X$ contains the periodic extensions of all continuous functions with compact support in $\Omega \times (0, 1)^N$. Hence $L$ extends to a bounded linear functional on $L^2(\Omega \times Y)$ with norm at most $c$. By the Riesz representation theorem there is $u_0 \in L^2(\Omega \times Y)$ with $\|u_0\| \le c$ and $L(\psi) = \int_\Omega \int_Y u_0 \psi\, dy\, dx$ for all $\psi \in X$. This is the two-scale convergence of $u_{\varepsilon'}$ to $u_0$, for all test functions in $X$ and so in $\mathcal D(\Omega; C^\infty_\#(Y))$. $\blacksquare$

**A hand check.** Let $\Omega = (0, 1)$, $\varepsilon = 1/n$ and $u_\varepsilon(x) = \sin(2\pi x/\varepsilon)$. With $\psi(x, y) = \sin(2\pi y)$, $\int_0^1 \sin^2(2\pi n x)\, dx = \tfrac12 = \int_0^1 \int_0^1 \sin^2(2\pi y)\, dy\, dx$, and with $\psi(x, y) = \cos(2\pi y)$ both sides are 0. In fact the lemma with $g = \sin(2\pi y)\psi(x, y)$ shows that $u_\varepsilon$ two-scale converges to $u_0(x, y) = \sin(2\pi y)$, while its weak limit in $L^2(0, 1)$ is $\int_0^1 \sin(2\pi y)\, dy = 0$.

## Consequences

- **The weak limit is the cell mean.** Taking $\psi(x, y) = \psi(x)$ shows that $u_{\varepsilon'} \rightharpoonup \int_Y u_0(\cdot, y)\, dy$ weakly in $L^2(\Omega)$.
- **Gradients (Nguetseng 1989, Theorem 3; Allaire 1992, Proposition 1.14).** If $u_\varepsilon$ is bounded in $H^1(\Omega)$, then along a subsequence $u_\varepsilon \rightharpoonup u$ weakly in $H^1(\Omega)$, $u_\varepsilon$ two-scale converges to $u(x)$, and $\nabla u_\varepsilon$ two-scale converges to $\nabla u(x) + \nabla_y u_1(x, y)$ for some $u_1 \in L^2(\Omega; H^1_\#(Y)/\mathbb R)$.
- **Homogenization.** For $-\nabla \cdot (A(x/\varepsilon)\nabla u_\varepsilon) = f$ with $u_\varepsilon \in H^1_0(\Omega)$, the [Lax-Milgram theorem](/lax-milgram-theorem/) bounds $u_\varepsilon$ in $H^1$. Test the [weak formulation](/weak-formulation/) with $\phi(x) + \varepsilon \phi_1(x, x/\varepsilon)$ and pass to the limit with the gradient result. The limit is a two-scale system for $(u, u_1)$. Its $y$ part is the cell problem, $u_1 = \sum_j \chi_j \partial_j u$, and its $x$ part is the homogenized equation with $A^*$. The limit problem has a unique solution, so the whole sequence converges, not only a subsequence.
- **Correctors.** If in addition $\|u_\varepsilon\|_{L^2(\Omega)} \to \|u_0\|_{L^2(\Omega \times Y)}$ (strong two-scale convergence) and $u_0$ is smooth enough to be a test function, then $\|u_\varepsilon - u_0(\cdot, \cdot/\varepsilon)\|_{L^2(\Omega)} \to 0$. This justifies the corrector of periodic homogenization.
- **Numerical methods.** The two-scale limit is the model behind the micro problems of the [heterogeneous multiscale method](/heterogeneous-multiscale-method/) and of the [FE2 method](/fe2-method/), and behind the analysis of the [multiscale finite element method](/multiscale-finite-element-method/) for periodic coefficients.

## Tightness

- **Only a subsequence.** Let $u_\varepsilon(x) = \sin(2\pi x/\varepsilon)$ for $\varepsilon = 1/n$ with $n$ even and $u_\varepsilon(x) = \cos(2\pi x/\varepsilon)$ for $n$ odd. The two subsequences two-scale converge to $\sin(2\pi y)$ and $\cos(2\pi y)$, so the full sequence does not converge.
- **The inequality of norms can be strict.** Let $u_\varepsilon(x) = \sin(2\pi x/\varepsilon^2)$ on $(0, 1)$. For $\psi \in X$ the oscillation at scale $\varepsilon^2$ averages out against $\psi(x, x/\varepsilon)$, so the two-scale limit is $u_0 = 0$, but $\|u_\varepsilon\|^2 \to \tfrac12$. The scale $\varepsilon$ in the definition must be the scale of the oscillation; oscillations at other scales are lost, as in a weak limit.
- **The test functions must be admissible.** A general $\psi \in L^2(\Omega \times Y)$ is an equivalence class, and $x \mapsto \psi(x, x/\varepsilon)$ is a trace on a set of measure zero. For example, in 1D, let $\psi(x, y) = 1$ on the countable union of the lines $y = x/\varepsilon_n \bmod 1$ and 0 elsewhere. Then $\psi = 0$ in $L^2(\Omega \times Y)$, but $\int_\Omega 1 \cdot \psi(x, x/\varepsilon_n)\, dx = |\Omega|$ for the constant sequence $u_\varepsilon = 1$, whose two-scale limit is $u_0 = 1$. So the convergence cannot hold for all $\psi \in L^2$. Continuity in $y$ (or Allaire's class of admissible functions) excludes such cases.

## History

Nguetseng proved the compactness result in 1989, as a general convergence result for functionals that arise in homogenization, and used it to give a new proof of the homogenization of linear elliptic problems. Allaire gave the name two-scale convergence in 1992, simplified the proof, introduced admissible test functions and strong two-scale convergence, and applied the method to several homogenization problems. The method replaced much of the formal two-scale expansion of Bensoussan, Lions and Papanicolaou by a short rigorous argument. The periodic unfolding method of Cioranescu, Damlamian and Griso (2002) gives the same limits as weak limits in a fixed space $L^2(\Omega \times Y)$.

## References
