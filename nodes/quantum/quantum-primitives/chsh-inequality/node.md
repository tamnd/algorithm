---
tag: 9NC848
kind: theorem
slug: chsh-inequality
name: CHSH inequality
aliases:
- CHSH game
- Clauser-Horne-Shimony-Holt inequality
area: quantum/quantum-primitives
level: core
summary: "For two parties with two settings and outcomes ±1, local models give |S| ≤ 2 for the CHSH sum S, while quantum states give at most 2√2, and a Bell pair reaches it."
prereqs: [bell-theorem, bell-states]
see_also: [two-prover-one-round-game, semidefinite-programming, quantum-communication-complexity, parallel-repetition-theorem, true-random-number-generator, key-distribution-problem, no-communication-theorem, entanglement]
sources:
  - paper: doi:10.1103/PhysRevLett.23.880
    title: John F. Clauser, Michael A. Horne, Abner Shimony and Richard A. Holt, Proposed experiment to test local hidden-variable theories, Physical Review Letters 23, 1969, pages 880 to 884
    locator: the whole paper
  - paper: doi:10.1007/BF00417500
    title: B. S. Cirel'son, Quantum generalizations of Bell's inequality, Letters in Mathematical Physics 4, 1980, pages 93 to 100
    locator: the bound 2√2
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 2.6 (EPR and the Bell inequality)
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Section 17.2 (CHSH, Clauser-Horne-Shimony-Holt) and its exercises
  - book: isbn:9781107180567
    title: John Watrous, The Theory of Quantum Information, Cambridge University Press, 2018
    locator: Section 6.3.2 (non-classical correlations)
  - paper: doi:10.1109/CCC.2004.1313847
    title: Richard Cleve, Peter Høyer, Ben Toner and John Watrous, Consequences and limits of nonlocal strategies, Proceedings of the 19th IEEE Conference on Computational Complexity, 2004, pages 236 to 249
    locator: the CHSH game as an XOR game and the semidefinite program for its entangled value
  - paper: doi:10.1016/0375-9601(95)00214-N
    title: R. Horodecki, P. Horodecki and M. Horodecki, Violating Bell inequality by mixed states, necessary and sufficient condition, Physics Letters A 200, 1995, pages 340 to 344
    locator: the largest CHSH value of a two-qubit state
  - paper: doi:10.1103/PhysRevA.40.4277
    title: Reinhard F. Werner, Quantum states with Einstein-Podolsky-Rosen correlations admitting a hidden-variable model, Physical Review A 40, 1989, pages 4277 to 4281
    locator: entangled states with a local model
  - paper: doi:10.1007/BF02058098
    title: Sandu Popescu and Daniel Rohrlich, Quantum nonlocality as an axiom, Foundations of Physics 24, 1994, pages 379 to 385
    locator: the no-signalling box with S = 4
  - paper: doi:10.1103/PhysRevLett.67.661
    title: Artur K. Ekert, Quantum cryptography based on Bell's theorem, Physical Review Letters 67, 1991, pages 661 to 663
    locator: key distribution checked by a Bell test
  - paper: doi:10.1038/nature09008
    title: S. Pironio and others, Random numbers certified by Bell's theorem, Nature 464, 2010, pages 1021 to 1024
    locator: randomness certified by a CHSH violation
  - paper: doi:10.1103/RevModPhys.86.419
    title: Nicolas Brunner, Daniel Cavalcanti, Stefano Pironio, Valerio Scarani and Stephanie Wehner, Bell nonlocality, Reviews of Modern Physics 86, 2014, pages 419 to 478
    locator: the review, on the CHSH inequality, the Tsirelson bound and self-testing
---

The *CHSH inequality* is the Bell inequality for two parties who each choose one of two measurements with outcomes $\pm 1$. For the sum $S$ of four correlations with one minus sign, every local hidden-variable model gives $\lvert S\rvert \le 2$; quantum mechanics allows up to $2\sqrt{2}$, the *Tsirelson bound*, and a [Bell pair](/bell-states/) measured at angles $45$ degrees apart reaches it. As a game, two players who cannot talk win with probability at most $\tfrac{3}{4}$ classically and $\cos^2(\pi/8) \approx 0.854$ with entanglement. Clauser, Horne, Shimony and Holt (1969) derived it so that real experiments, with imperfect correlations, can test [Bell's theorem](/bell-theorem/).

## Statement

Alice chooses a setting $x \in \{0, 1\}$ and gets an outcome $a \in \{+1, -1\}$; Bob chooses $y \in \{0, 1\}$ and gets $b \in \{+1, -1\}$. Write $E_{xy}$ for the mean of $ab$ when the settings are $x$ and $y$, and

$$S = E_{00} + E_{01} + E_{10} - E_{11}.$$

A *local model* is a probability space $(\Lambda, \mu)$ with functions $A_x(\lambda), B_y(\lambda) \in [-1, 1]$, the mean outcomes given $\lambda$, so that $E_{xy} = \int A_x(\lambda) B_y(\lambda)\, d\mu(\lambda)$, as on the [Bell's theorem](/bell-theorem/) page. A *quantum strategy* is a density matrix $\rho$ on $\mathcal{H}_A \otimes \mathcal{H}_B$, of any finite dimension, and for each setting a two-outcome measurement. Its observables $A_x = M^x_{+} - M^x_{-}$ and $B_y = N^y_{+} - N^y_{-}$ are Hermitian with $-I \le A_x, B_y \le I$, and $E_{xy} = \mathrm{Tr}\big(\rho\, (A_x \otimes B_y)\big)$.

**Theorem.**

1. **(CHSH 1969)** Every local model has $\lvert S\rvert \le 2$. For a deterministic model, $S \in \{-2, +2\}$.
2. **(Tsirelson 1980)** Every quantum strategy has $\lvert S\rvert \le 2\sqrt{2}$.
3. **(The bound is reached.)** For $|\Phi^+\rangle = (|00\rangle + |11\rangle)/\sqrt{2}$ and the observables $A(t) = \cos t\, Z + \sin t\, X$, $E = \cos(t_A - t_B)$. With Alice's angles $0, \pi/2$ and Bob's angles $\pi/4, -\pi/4$, $S = 2\sqrt{2}$.
4. **(The game.)** In the CHSH game a referee draws $x, y$ uniformly and the players win if $a' \oplus b' = x \wedge y$, where $a', b' \in \{0, 1\}$ encode the outcomes by $(-1)^{a'} = a$. The winning probability is $\tfrac{1}{2} + S/8$. So it is at most $\tfrac{3}{4}$ for local strategies and at most $\tfrac{1}{2} + \tfrac{\sqrt{2}}{4} = \cos^2(\pi/8)$ for quantum ones, and both values are reached.

The inequality forbids exactly the local models: it says that a value $\lvert S\rvert > 2$ cannot come from shared classical data and local responses. It does not limit no-signalling correlations in general, which can reach $S = 4$ (see Tightness), and a violation does not send any message.

## In plain words

Two players are far apart and cannot talk. Each gets a random question with two possible values and must answer yes or no. They win if their answers differ exactly when both questions are the second one, and agree in the other three cases. With any plan made in advance, they win at most three times out of four. If they share an entangled pair of particles and each measures their particle along a direction chosen by the question, they win about 85 percent of the time. No quantum plan does better. The gap is what Bell experiments measure.

## Proof

**Part 1.** Fix $\lambda$ and write $A_x = A_x(\lambda)$, $B_y = B_y(\lambda)$. Then

$$A_0 B_0 + A_0 B_1 + A_1 B_0 - A_1 B_1 = A_0 (B_0 + B_1) + A_1 (B_0 - B_1).$$

Since $\lvert A_x\rvert \le 1$, its absolute value is at most $\lvert B_0 + B_1\rvert + \lvert B_0 - B_1\rvert = 2\max(\lvert B_0\rvert, \lvert B_1\rvert) \le 2$. Integrate over $\lambda$ to get $\lvert S\rvert \le 2$. In a deterministic model all four values are $\pm 1$, so one of $B_0 + B_1$ and $B_0 - B_1$ is $0$ and the other is $\pm 2$, and the sum for each $\lambda$ is exactly $\pm 2$. The sixteen choices of $(A_0, A_1, B_0, B_1)$ give only the values $-2$ and $2$.

**Part 2.** First take $A_x^2 = I$ and $B_y^2 = I$. Let $\hat S = A_0 \otimes (B_0 + B_1) + A_1 \otimes (B_0 - B_1)$, so $S = \mathrm{Tr}(\rho \hat S)$. Expand $\hat S^2$ with $(B_0 + B_1)^2 + (B_0 - B_1)^2 = 4I$, $(B_0 + B_1)(B_0 - B_1) = -[B_0, B_1]$ and $(B_0 - B_1)(B_0 + B_1) = [B_0, B_1]$:

$$\hat S^2 = 4\, I \otimes I - [A_0, A_1] \otimes [B_0, B_1].$$

Each commutator has operator norm at most $2\lVert A_0\rVert \lVert A_1\rVert = 2$, so $\lVert \hat S^2\rVert \le 4 + 4 = 8$. As $\hat S$ is Hermitian, $\lVert \hat S\rVert = \lVert \hat S^2\rVert^{1/2} \le 2\sqrt{2}$, and $\lvert \mathrm{Tr}(\rho \hat S)\rvert \le \lVert \hat S\rVert$ for a density matrix $\rho$.

Now take general observables with $-I \le A_x \le I$. Each is a convex combination of Hermitian $U$ with $U^2 = I$: write $A = \sum_k \lambda_k P_k$ by the [spectral theorem](/spectral-theorem/), with $\lambda_k = p_k \cdot 1 + (1 - p_k)(-1)$ and $p_k \in [0, 1]$. Then $A$ is the mixture of the operators $\sum_k \epsilon_k P_k$ over all sign choices $\epsilon \in \{\pm 1\}^r$, with the weight $\prod_k p_k^{[\epsilon_k = 1]}(1 - p_k)^{[\epsilon_k = -1]}$, and each of those squares to $I$. Since $S$ is affine in each observable when the other three are fixed, $\lvert S\rvert$ is at most its largest value at such operators. Replace the four observables one at a time to reach the first case. So $\lvert S\rvert \le 2\sqrt{2}$.

**Part 3.** $A(t)$ is real and symmetric, and $(M \otimes I)|\Phi^+\rangle = (I \otimes M^{T})|\Phi^+\rangle$ for every $2 \times 2$ matrix $M$. So

$$E = \langle \Phi^+|\, A(t_A) \otimes A(t_B) \,|\Phi^+\rangle = \langle \Phi^+|\, I \otimes A(t_A) A(t_B) \,|\Phi^+\rangle = \tfrac{1}{2}\mathrm{Tr}\big(A(t_A) A(t_B)\big) = \cos t_A \cos t_B + \sin t_A \sin t_B = \cos(t_A - t_B),$$

using that qubit $0$ of $|\Phi^+\rangle$ has the reduced state $I/2$ and $\mathrm{Tr}(ZX) = 0$. With the angles of the theorem, $E_{00} = \cos(-\pi/4)$, $E_{01} = \cos(\pi/4)$, $E_{10} = \cos(\pi/4)$ and $E_{11} = \cos(3\pi/4)$, so $S = 4/\sqrt{2} = 2\sqrt{2}$.

**Part 4.** The players win on the inputs $(x, y)$ when $ab = (-1)^{x \wedge y}$, which has probability $(1 + (-1)^{x \wedge y} E_{xy})/2$. The average over the four inputs is $\tfrac{1}{2} + \tfrac{1}{8}(E_{00} + E_{01} + E_{10} - E_{11}) = \tfrac{1}{2} + S/8$. Parts 1 to 3 give the bounds $\tfrac{1}{2} + \tfrac{2}{8} = \tfrac{3}{4}$ and $\tfrac{1}{2} + \tfrac{2\sqrt{2}}{8} = \tfrac{1 + \cos(\pi/4)}{2} = \cos^2(\pi/8)$, and show that both are reached. $\square$

## Consequences

- **Experiments.** CHSH needs no perfect correlations, so it is the form that Bell experiments measure. A measured $S$ above $2$ by many standard deviations rules out local models, under the assumptions of [Bell's theorem](/bell-theorem/).
- **Device-independent key distribution.** Ekert (1991) proposed to check the security of a shared key by a CHSH test on the same pairs. A value close to $2\sqrt{2}$ limits what any eavesdropper can know, without trust in the devices ([key distribution problem](/key-distribution-problem/)).
- **Certified randomness.** If $S > 2$, the outcomes cannot all be fixed in advance, so some of the output is random even to the maker of the devices. Pironio and others (2010) turned a measured violation into a bound on the [min-entropy](/min-entropy/) of the output ([true random number generator](/true-random-number-generator/)).
- **Nonlocal games.** The CHSH game is the simplest XOR game, a [two-prover one-round game](/two-prover-one-round-game/) whose result depends only on the parity of the answers. Cleve, Høyer, Toner and Watrous (2004) showed that the entangled value of every XOR game is the value of a [semidefinite program](/semidefinite-programming/); for CHSH it is $\cos^2(\pi/8)$.
- **No signalling.** Each party's outcomes alone are uniform for every setting in the optimal strategy, as the [no-communication theorem](/no-communication-theorem/) requires.

## Tightness

- **Classical bound.** The strategy "always answer $+1$" gives $S = 1 + 1 + 1 - 1 = 2$, and the game is won on the three inputs with $x \wedge y = 0$. So $2$ and $\tfrac{3}{4}$ are reached.
- **Quantum bound.** Part 3 reaches $2\sqrt{2}$ with one Bell pair, so more entanglement does not help. The optimum is essentially unique: any strategy that reaches $2\sqrt{2}$ is, up to local isometries, this Bell pair with these observables (self-testing).
- **Products and separable states.** For a product state $\rho_A \otimes \rho_B$, $E_{xy} = \mathrm{Tr}(\rho_A A_x)\, \mathrm{Tr}(\rho_B B_y)$ is a local deterministic model, so $\lvert S\rvert \le 2$; mixtures of products are local models too. Every violation needs [entanglement](/entanglement/).
- **Entanglement is not enough.** For the Werner state $\rho_p = p\,|\Phi^+\rangle\langle\Phi^+| + (1 - p)\, I/4$, the noise term gives $0$ to every correlation, so $S = 2\sqrt{2}\, p$ at the optimal angles. Horodecki, Horodecki and Horodecki (1995) showed this is the largest value for this state, so it violates CHSH exactly when $p > 1/\sqrt{2} \approx 0.707$. The state is entangled for $p > \tfrac{1}{3}$, and Werner (1989) gave a local model for all projective measurements when $p \le \tfrac{1}{2}$.
- **No-signalling bound.** The Popescu-Rohrlich box gives uniform marginals and $a' \oplus b' = x \wedge y$ always, so $S = 4$ and the game is won with probability $1$. It sends no signal, so the Tsirelson bound $2\sqrt{2} < 4$ is a limit of quantum mechanics, not of relativity.

### Implementation

The folder `impl/python` computes $E$ and $S$ on the state-vector simulator. It finds $S = 2\sqrt{2}$ at the angles of Part 3, with each $E_{xy} = \cos(t_A - t_B)$ to $10^{-12}$. It lists all sixteen deterministic strategies and gets exactly the values $\{-2, 2\}$ for $S$ and $\tfrac{3}{4}$ for the best game value. On random two-qubit states and random angles, $\lvert S\rvert \le 2\sqrt{2}$, and on random product states $\lvert S\rvert \le 2$. It checks the identity $\hat S^2 = 4I - [A_0, A_1] \otimes [B_0, B_1]$ on random observables. It plays $20\,000$ rounds of the game with the seed $2024$ and requires a win rate within $0.015$ of $\cos^2(\pi/8) \approx 0.8536$; by the [Hoeffding inequality](/hoeffding-inequality/) a correct simulation leaves this band with probability below $3 \cdot 10^{-4}$. The seeded run wins $85.335$ percent of the rounds.

## History

Clauser, Horne, Shimony and Holt (1969) derived the inequality to make Bell's 1964 argument testable with imperfect detectors and correlations. Freedman and Clauser (1972) and Aspect, Dalibard and Roger (1982) measured violations, and the loophole-free experiments of 2015 used CHSH or closely related forms. Tsirelson (1980) proved the bound $2\sqrt{2}$. Popescu and Rohrlich (1994) asked why nature does not reach the no-signalling value $4$. The game form, with the values $\tfrac{3}{4}$ and $\cos^2(\pi/8)$, became standard in computer science through the work on nonlocal games, for example by Cleve, Høyer, Toner and Watrous (2004).

## References
