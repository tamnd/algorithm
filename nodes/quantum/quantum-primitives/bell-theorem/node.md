---
tag: 5Z5H18
kind: theorem
slug: bell-theorem
name: Bell's theorem
aliases:
- Bell inequality theorem
area: quantum/quantum-primitives
level: intro
summary: "No local hidden-variable model gives the quantum correlations of the singlet: such models obey Bell's inequality, and spin measurements 60 degrees apart violate it."
prereqs: [entanglement, quantum-measurement]
see_also: [chsh-inequality, bell-states, no-communication-theorem, two-prover-one-round-game, true-random-number-generator, key-distribution-problem]
sources:
  - paper: doi:10.1103/PhysicsPhysiqueFizika.1.195
    title: J. S. Bell, On the Einstein Podolsky Rosen paradox, Physics Physique Fizika 1, 1964, pages 195 to 200
    locator: the whole paper
  - paper: doi:10.1103/PhysRev.47.777
    title: A. Einstein, B. Podolsky and N. Rosen, Can quantum-mechanical description of physical reality be considered complete?, Physical Review 47, 1935, pages 777 to 780
    locator: the whole paper
  - paper: doi:10.1103/PhysRevLett.23.880
    title: John F. Clauser, Michael A. Horne, Abner Shimony and Richard A. Holt, Proposed experiment to test local hidden-variable theories, Physical Review Letters 23, 1969, pages 880 to 884
    locator: the inequality for imperfect correlations
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 2.6 (EPR and the Bell inequality)
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Chapter 17 (entanglement and non-locality), Sections 17.1 and 17.2
  - paper: doi:10.1103/RevModPhys.86.419
    title: Nicolas Brunner, Daniel Cavalcanti, Stefano Pironio, Valerio Scarani and Stephanie Wehner, Bell nonlocality, Reviews of Modern Physics 86, 2014, pages 419 to 478
    locator: the review, on the assumptions of Bell's theorem and the loopholes of experiments
  - paper: doi:10.1119/1.16503
    title: N. David Mermin, Quantum mysteries revisited, American Journal of Physics 58, 1990, pages 731 to 734
    locator: the GHZ argument without inequalities
  - paper: doi:10.1103/PhysRevLett.28.938
    title: Stuart J. Freedman and John F. Clauser, Experimental test of local hidden-variable theories, Physical Review Letters 28, 1972, pages 938 to 941
    locator: the first experimental test
  - paper: doi:10.1103/PhysRevLett.49.1804
    title: Alain Aspect, Jean Dalibard and Gérard Roger, Experimental test of Bell's inequalities using time-varying analyzers, Physical Review Letters 49, 1982, pages 1804 to 1807
    locator: the test with settings changed during the flight of the photons
  - paper: doi:10.1038/nature15759
    title: B. Hensen and others, Loophole-free Bell inequality violation using electron spins separated by 1.3 kilometres, Nature 526, 2015, pages 682 to 686
    locator: a loophole-free test
  - paper: doi:10.1103/PhysRevLett.115.250401
    title: Marissa Giustina and others, Significant-loophole-free test of Bell's theorem with entangled photons, Physical Review Letters 115, 2015, article 250401
    locator: a loophole-free test with photons
  - paper: doi:10.1103/PhysRevLett.115.250402
    title: Lynden K. Shalm and others, Strong loophole-free test of local realism, Physical Review Letters 115, 2015, article 250402
    locator: a loophole-free test with photons
---

*Bell's theorem* says that no local hidden-variable theory can give all the predictions of quantum mechanics. In such a theory, each measurement result is fixed, or made random, by data carried by the particles from their common source, and the result on one side does not depend on the setting chosen on the other side. Bell (1964) showed that every theory of this kind obeys an inequality on the correlations of two distant measurements, and that the singlet [Bell state](/bell-states/) breaks it. Experiments since 1972, and loophole-free ones since 2015, agree with quantum mechanics.

## Statement

A *setting* is a unit vector $x \in \mathbb{R}^3$, the direction along which a spin is measured, and each measurement gives $+1$ or $-1$.

**Local hidden-variable model.** A model consists of a probability space $(\Lambda, \mu)$ and two functions $A(x, \lambda)$ and $B(y, \lambda)$ with values in $[-1, 1]$. Here $\lambda$ is the hidden variable, drawn from $\mu$ at the source; $A(x, \lambda)$ is the mean of Alice's result for the setting $x$ given $\lambda$, and $B(y, \lambda)$ is the same for Bob. Given $\lambda$, the two results are independent. The model predicts the correlation

$$E(x, y) = \int_\Lambda A(x, \lambda)\, B(y, \lambda)\, d\mu(\lambda).$$

Three assumptions are built in. *Locality*: $A$ does not depend on Bob's setting $y$, and $B$ does not depend on $x$. *Measurement independence*: $\mu$ does not depend on $x$ or $y$. *Factorization*: given $\lambda$, the results are independent, so the mean of the product is $A \cdot B$. A model is *deterministic* if $A$ and $B$ only take the values $\pm 1$.

**Quantum prediction.** Two qubits in the singlet $|\Psi^-\rangle = (|01\rangle - |10\rangle)/\sqrt{2}$, with the spin of qubit $A$ measured along $x$ and the spin of qubit $B$ along $y$, give

$$E_Q(x, y) = \langle \Psi^- |\, \sigma_x \otimes \sigma_y \,| \Psi^- \rangle = -\, x \cdot y,$$

where $\sigma_x = x_1 X + x_2 Y + x_3 Z$ is the spin observable along $x$, with eigenvalues $\pm 1$.

**Theorem (Bell 1964).** (a) Let a local hidden-variable model satisfy $E(x, x) = -1$ for each $x \in \{a, b, c\}$. Then

$$\lvert E(a, b) - E(a, c) \rvert \le 1 + E(b, c).$$

(b) For three coplanar settings $a, b, c$ at the angles $0, \pi/3, 2\pi/3$, the quantum correlations satisfy $E_Q(x, x) = -1$ and give $\lvert E_Q(a, b) - E_Q(a, c)\rvert = 1$ and $1 + E_Q(b, c) = \tfrac{1}{2}$.

(c) Hence no local hidden-variable model gives $E(x, y) = E_Q(x, y)$ for all settings $x, y$.

What the theorem forbids is exactly the conjunction of the three assumptions. It says nothing against a theory that drops one of them, such as a hidden-variable theory with explicit nonlocal dynamics or one where the source knows the future settings. It also does not say that the quantum correlations carry a signal: by the [no-communication theorem](/no-communication-theorem/), Bob's results alone have the same statistics for every setting of Alice.

## In plain words

Suppose each particle of a pair carries a hidden list of answers, written at the source, that says what it will show for each direction of measurement. Suppose also that what one particle shows cannot depend on how the other is measured, far away. Then the correlations between the two sides obey a simple counting rule. Quantum mechanics predicts that a pair in the singlet state breaks this rule by a wide margin when the directions are 60 degrees apart. So no such hidden lists can explain quantum mechanics. Experiments side with quantum mechanics. The pair still cannot be used to send a message.

## Proof

**Step 1: the quantum prediction.** First, $(\sigma_x \otimes I + I \otimes \sigma_x)|\Psi^-\rangle = 0$ for every $x$. By linearity it is enough to check $X$, $Y$ and $Z$. For $Z$: $(Z \otimes I)(|01\rangle - |10\rangle) = |01\rangle + |10\rangle$ and $(I \otimes Z)(|01\rangle - |10\rangle) = -|01\rangle - |10\rangle$, which sum to $0$. For $X$: the two terms give $|11\rangle - |00\rangle$ and $|00\rangle - |11\rangle$. For $Y$, with $Y|0\rangle = i|1\rangle$ and $Y|1\rangle = -i|0\rangle$: they give $i|11\rangle + i|00\rangle$ and $-i|00\rangle - i|11\rangle$. So $(\sigma_x \otimes I)|\Psi^-\rangle = -(I \otimes \sigma_x)|\Psi^-\rangle$ and

$$E_Q(x, y) = \langle \Psi^-|(\sigma_x \otimes I)(I \otimes \sigma_y)|\Psi^-\rangle = -\langle \Psi^-|\, I \otimes \sigma_x \sigma_y \,|\Psi^-\rangle = -\tfrac{1}{2}\mathrm{Tr}(\sigma_x \sigma_y),$$

where the last step uses that qubit $B$ of the singlet has the reduced state $I/2$. The Pauli products give $\sigma_x \sigma_y = (x \cdot y) I + i (x \times y) \cdot (X, Y, Z)$, and the Paulis have trace $0$, so $\tfrac{1}{2}\mathrm{Tr}(\sigma_x\sigma_y) = x \cdot y$. This proves $E_Q(x, y) = -x \cdot y$, and in particular $E_Q(x, x) = -1$.

**Step 2: perfect anticorrelation forces determinism.** Suppose $E(x, x) = -1$. Then $\int (1 + A(x, \lambda) B(x, \lambda))\, d\mu = 0$. The integrand is at least $0$ because $\lvert A B \rvert \le 1$, so $A(x, \lambda) B(x, \lambda) = -1$ for $\mu$-almost every $\lambda$. Since both factors lie in $[-1, 1]$, this forces $A(x, \lambda) = -B(x, \lambda) \in \{-1, +1\}$ for almost every $\lambda$. Apply this to $x = a, b, c$ and discard a set of measure $0$: for every remaining $\lambda$, the three values $A(a, \lambda), A(b, \lambda), A(c, \lambda)$ are $\pm 1$ and $B(x, \lambda) = -A(x, \lambda)$. This is the argument of Einstein, Podolsky and Rosen: a perfect correlation at a distance means the result was fixed in advance.

**Step 3: Bell's inequality.** Write $A_x = A(x, \lambda)$. By Step 2, $E(x, y) = -\int A_x A_y\, d\mu$. Since $A_b^2 = 1$,

$$E(a, b) - E(a, c) = \int (A_a A_c - A_a A_b)\, d\mu = -\int A_a A_b (1 - A_b A_c)\, d\mu.$$

Now $\lvert A_a A_b \rvert = 1$ and $1 - A_b A_c \ge 0$, so

$$\lvert E(a, b) - E(a, c) \rvert \le \int (1 - A_b A_c)\, d\mu = 1 + E(b, c).$$

This proves (a).

**Step 4: the violation.** For coplanar unit vectors at the angles $\theta_x$ and $\theta_y$, Step 1 gives $E_Q(x, y) = -\cos(\theta_x - \theta_y)$. With the angles $0, \pi/3, 2\pi/3$:

$$E_Q(a, b) = -\tfrac{1}{2},\qquad E_Q(a, c) = \tfrac{1}{2},\qquad E_Q(b, c) = -\tfrac{1}{2}.$$

So $\lvert E_Q(a, b) - E_Q(a, c) \rvert = 1$, while $1 + E_Q(b, c) = \tfrac{1}{2}$. This proves (b). A model with $E = E_Q$ would satisfy the hypothesis of (a) and break its conclusion, which proves (c). $\square$

## Consequences

- **Quantum mechanics is not a local hidden-variable theory.** The correlations of an entangled pair cannot be explained by shared classical data. This answers the question of Einstein, Podolsky and Rosen (1935) in the negative for local completions.
- **The CHSH inequality.** Step 2 needs perfect anticorrelation, which no real experiment has. The [CHSH inequality](/chsh-inequality/) of Clauser, Horne, Shimony and Holt (1969) needs no such hypothesis: every local model satisfies $\lvert E(a, b) + E(a, b') + E(a', b) - E(a', b') \rvert \le 2$, and the singlet reaches $2\sqrt{2}$. Experiments test this form.
- **Device-independent protocols.** A violation proves that the results were not fixed in advance, whatever the devices do inside. This gives certified randomness ([true random number generator](/true-random-number-generator/)) and key distribution with untrusted devices ([key distribution problem](/key-distribution-problem/)).
- **Nonlocal games.** In the language of [two-prover one-round games](/two-prover-one-round-game/), a Bell inequality is a bound on the classical winning probability, and entangled provers can beat it.
- **Bell's theorem without inequalities.** For three qubits in the GHZ state $(|000\rangle + |111\rangle)/\sqrt{2}$, the state is an eigenvector of $XXX$ with eigenvalue $+1$ and of $XYY$, $YXY$ and $YYX$ with eigenvalue $-1$. Values $x_i, y_i \in \{\pm 1\}$ fixed in advance would need $x_1 y_2 y_3 = y_1 x_2 y_3 = y_1 y_2 x_3 = -1$, whose product is $x_1 x_2 x_3 = -1$, against $+1$. So a local model fails on a single run, not only on average (Mermin 1990, after Greenberger, Horne and Zeilinger).

## Tightness

- **The classical bound is reached.** Take $\lambda$ uniform on $[0, 2\pi)$, $A(x, \lambda) = \operatorname{sign}\cos(\theta_x - \lambda)$ and $B = -A$. The two signs differ on a set of length $2\lvert\theta_x - \theta_y\rvert$ for $\lvert \theta_x - \theta_y \rvert \le \pi$, so $E(x, y) = -(1 - 2\lvert \theta_x - \theta_y\rvert/\pi)$, a linear function of the angle. At $0, \pi/3, 2\pi/3$ this gives $E(a, b) = -\tfrac{1}{3}$, $E(a, c) = \tfrac{1}{3}$, $E(b, c) = -\tfrac{1}{3}$, and both sides of the inequality equal $\tfrac{2}{3}$. Over the eight deterministic choices of $(A_a, A_b, A_c)$, the largest value of $\lvert -A_aA_b + A_aA_c\rvert - (1 - A_bA_c)$ is exactly $0$.
- **The angles are the best of their family.** For $a, b, c$ at $0, \theta, 2\theta$, the quantum excess $\lvert E_Q(a, b) - E_Q(a, c)\rvert - 1 - E_Q(b, c)$ equals $2\cos\theta - \cos 2\theta - 1$ when $\cos\theta \ge \cos 2\theta$. Its derivative $2\sin 2\theta - 2\sin\theta$ is zero at $\cos\theta = \tfrac{1}{2}$, so the largest excess is $\tfrac{1}{2}$, at $\theta = \pi/3$.
- **Each assumption is needed.** If Bob's result may depend on Alice's setting, let Alice output a fair random sign $s$, and let Bob output $-s$ with probability $(1 + x \cdot y)/2$ and $s$ otherwise. Then $E(x, y) = -x \cdot y = E_Q(x, y)$, but the model is not local. If $\mu$ may depend on the settings, the source can draw the pair of results from the quantum distribution for the settings that will be used. Each of these models gives up one assumption of the theorem.
- **The quantum violation is bounded.** Quantum correlations cannot violate the CHSH form beyond $2\sqrt{2}$, the Tsirelson bound, which is less than the value $4$ that no-signalling alone allows ([CHSH inequality](/chsh-inequality/)).

## History

Einstein, Podolsky and Rosen (1935) argued that perfect correlations at a distance show that quantum mechanics is incomplete. Bohm recast the argument with two spins in 1951. Bell (1964) proved that any local completion obeys an inequality that quantum mechanics breaks. Clauser, Horne, Shimony and Holt (1969) turned it into a form that experiments can test, and Freedman and Clauser (1972) made the first test. Aspect, Dalibard and Roger (1982) changed the settings while the photons were in flight. In 2015 three groups, at Delft, Vienna and NIST, closed the locality and detection loopholes in the same experiment. Aspect, Clauser and Zeilinger shared the 2022 Nobel Prize in Physics for this line of experiments.

## References
