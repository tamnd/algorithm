---
tag: TYMAXR
kind: theorem
slug: lieb-robinson-bound
name: Lieb-Robinson bound
aliases:
- Lieb-Robinson light cone
area: quantum/quantum-simulation
level: research
summary: "Under a local Hamiltonian with bounded terms, [tau_t(A), B] for operators at distance d is at most C e^(vt - d). Effects spread at a finite speed v, set by the size of the terms."
prereqs: [matrix-norms, unitary-operator]
see_also: [quantum-many-body-simulation, hamiltonian-simulation, trotter-suzuki-product-formulas, jordan-wigner-transformation, quantum-field-theory-simulation, open-quantum-system-simulation, entanglement-entropy, pauli-string-decomposition]
sources:
  - paper: doi:10.1007/BF01645779
    title: Elliott H. Lieb and Derek W. Robinson, The finite group velocity of quantum spin systems, Communications in Mathematical Physics 28(3), 1972, pages 251 to 257
    locator: the main theorem, a bound on the commutator of time-evolved local observables that decays outside a cone of finite velocity
  - paper: doi:10.1007/s00220-006-1556-1
    title: Bruno Nachtergaele and Robert Sims, Lieb-Robinson bounds and the exponential clustering theorem, Communications in Mathematical Physics 265(1), 2006, pages 119 to 130
    locator: Section 2 (the proof by a differential inequality for the commutator and its iteration over chains of interaction terms)
  - paper: doi:10.1007/s00220-006-0030-4
    title: Matthew B. Hastings and Tohru Koma, Spectral gap and exponential decay of correlations, Communications in Mathematical Physics 265(3), 2006, pages 781 to 804
    locator: the Lieb-Robinson bound for interactions with exponential or power-law decay, and the exponential decay of correlations in gapped ground states
  - paper: doi:10.1137/18M1231511
    title: Jeongwan Haah, Matthew B. Hastings, Robin Kothari and Guang Hao Low, Quantum algorithm for simulating real time evolution of lattice Hamiltonians, SIAM Journal on Computing 52(6), 2023 (FOCS 2018, arXiv:1801.03922)
    locator: the decomposition of the evolution of a lattice Hamiltonian into local blocks using the Lieb-Robinson bound, with O(nT polylog(nT/ε)) gates
---

The *Lieb-Robinson bound* says that a quantum spin system with local interactions has a finite speed of propagation. Let $H = \sum_x h_x$ be a sum of terms that each act on a few neighbouring sites, with $\|h_x\| \le J$. Evolve an operator $A$ at site $a$ in the Heisenberg picture to $\tau_t(A) = e^{iHt}Ae^{-iHt}$. Then the commutator of $\tau_t(A)$ with an operator $B$ at site $b$ stays exponentially small until $t$ is about $|a - b|/v$, for a velocity $v$ of order $J$ that does not depend on the size of the system. Nothing in quantum mechanics alone forbids instant effects, since $e^{iHt}$ is not local. The bound comes from the locality of $H$ alone. Lieb and Robinson (1972) proved it. It is the reason that local [Hamiltonian simulation](/hamiltonian-simulation/) can work block by block, and it is the main tool for [quantum many-body simulation](/quantum-many-body-simulation/) on lattices. The norm is the operator norm of the [matrix norms](/matrix-norms/) page.

## Statement

**Theorem (one dimension).** Take a chain of sites $\ldots, -1, 0, 1, \ldots$ (finite or infinite, open ends), each with a finite-dimensional space. Let $H = \sum_x h_x$, where $h_x$ is Hermitian, acts on the sites $x$ and $x + 1$, and has $\|h_x\| \le J$. Let $A$ act on site $a$ and $B$ on site $b$, with distance $d = |a - b| \ge 1$. Then for all real $t$,
$$\big\|[\tau_t(A), B]\big\| \;\le\; \frac43\,\|A\|\,\|B\| \sum_{k \ge d} \frac{(6J|t|)^k}{k!} \;\le\; \frac43\,\|A\|\,\|B\|\; e^{-(d - v|t|)}, \qquad v = 6eJ \approx 16.3\,J.$$

The same proof gives, on any lattice where each term meets at most $z$ other terms, a bound of the form $C\|A\|\|B\|e^{-\mu(d - v|t|)}$ with $v$ of order $zJ$. For interactions that decay with distance, see Hastings and Koma (2006).

## In plain words

Push on one end of a long chain of spins. The push has to be passed from spin to spin by the couplings, and each coupling of strength $J$ takes a time of order $1/J$ to pass it on. So after time $t$ the effect has gone about $vt$ sites, with $v$ a few times $J$. Past that front, the effect is not zero, but it is exponentially small in the distance to the front. A measurement at site $b$ cannot tell, to good accuracy, whether $A$ was applied at site $a$ before time $d/v$.

## Proof

Fix $B$, and for a set $X$ of sites write
$$C(X, t) = \sup\big\{\|[\tau_t(A'), B]\| : A' \text{ acts on } X,\ \|A'\| \le 1\big\}.$$
Let $H_X$ be the sum of the terms $h_Z$ with $Z \cap X \ne \emptyset$, where $Z = \{x, x + 1\}$ is the support of $h_x$. All other terms commute with an operator $A$ on $X$.

*Step 1: a differential inequality.* Let $g(t) = [\tau_t(A), B]$. Since $\frac{d}{dt}\tau_t(A) = i\tau_t([H, A]) = i\tau_t([H_X, A]) = i[\tau_t(H_X), \tau_t(A)]$, the Jacobi identity $[[P, Q], B] = [P, [Q, B]] - [Q, [P, B]]$ gives
$$g'(t) = i\,[\tau_t(H_X), g(t)] \;-\; i\,[\tau_t(A), [\tau_t(H_X), B]].$$
Let $V(t)$ solve $V' = i\tau_t(H_X)V$ with $V(0) = I$. It is a [unitary operator](/unitary-operator/), since $\tau_t(H_X)$ is Hermitian. Then $\frac{d}{dt}\big(V^\dagger g V\big) = -iV^\dagger[\tau_t(A), [\tau_t(H_X), B]]V$, so
$$\|g(t)\| \le \|g(0)\| + 2\|A\|\int_0^{|t|} \|[\tau_s(H_X), B]\|\,ds \le \|g(0)\| + 2\|A\| \sum_{Z \cap X \ne \emptyset} \|h_Z\| \int_0^{|t|} C(Z, s)\,ds.$$
(For $t < 0$ the same argument runs backward in time.) Taking the supremum over $A$:
$$C(X, t) \;\le\; C(X, 0) + 2\sum_{Z \cap X \ne \emptyset} \|h_Z\|\int_0^{|t|} C(Z, s)\,ds. \qquad (\ast)$$

*Step 2: iterate.* Put $(\ast)$ for $C(Z, s)$ into its own right side, $m$ times. The iterated integrals give $|t|^k/k!$, so
$$C(X, t) \le C(X, 0) + \sum_{k=1}^{m} \frac{(2|t|)^k}{k!} \sum_{Z_1, \ldots, Z_k} \|h_{Z_1}\| \cdots \|h_{Z_k}\|\, C(Z_k, 0) + R_m,$$
where the inner sum runs over chains with $Z_1 \cap X \ne \emptyset$ and $Z_i \cap Z_{i-1} \ne \emptyset$. The remainder $R_m$ has the same form at order $m + 1$, with $C(Z_{m+1}, s) \le 2\|B\|$ in place of $C(Z_k, 0)$.

*Step 3: count the chains.* Take $X = \{a\}$. Then $C(X, 0) = 0$, since $A$ and $B$ act on different sites. Also $C(Z_k, 0) = 0$ unless $b \in Z_k$, and $C(Z_k, 0) \le 2\|B\|$ always. Each bond $\{x, x+1\}$ meets at most 3 bonds (itself and its two neighbours), and at most 2 bonds meet $\{a\}$. So there are at most $2 \cdot 3^{k-1}$ chains of length $k$. The union of a chain of $k$ bonds is an interval of at most $k + 1$ sites that contains $a$, so a chain whose last bond contains $b$ has $k \ge d$. With $\|h_Z\| \le J$:
$$C(\{a\}, t) \le \sum_{k=d}^{m} \frac{(2J|t|)^k}{k!}\, 2\cdot 3^{k-1}\cdot 2\|B\| + R_m, \qquad R_m \le \frac{(2J|t|)^{m+1}}{(m+1)!}\, 2\cdot 3^m \cdot 2\|B\|.$$
As $m \to \infty$, $R_m \to 0$, and $\frac43 \cdot 3^k\cdot 2^k = \frac43 \cdot 6^k$ gives the first inequality, after multiplying by $\|A\|$.

*Step 4: the exponential form.* For $k \ge d$, $e^{k - d} \ge 1$, so with $x = 6J|t|$,
$$\sum_{k \ge d}\frac{x^k}{k!} \le \sum_{k \ge 0}\frac{x^k}{k!}\,e^{k - d} = e^{ex - d} = e^{-(d - 6eJ|t|)}. \qquad \blacksquare$$

## Consequences

- **Locality of the dynamics.** The bound does not depend on the number of sites. So $\tau_t(A)$ is close to an operator that acts only on the sites within distance $r$ of $a$, with an error that decays like $e^{-(r - v|t|)}$. Outside the light cone $r > v|t|$, the rest of the system can be ignored.
- **Simulation in blocks.** Haah, Hastings, Kothari and Low (2018, journal version 2023) cut the evolution of a lattice Hamiltonian on $n$ sites into evolutions of overlapping blocks of size $O(\log(nT/\varepsilon))$, with the error of each cut controlled by the Lieb-Robinson bound. This gives $O(nT\,\mathrm{polylog}(nT/\varepsilon))$ gates for time $T$, which they show is optimal up to the polylogarithmic factor. Product formula error bounds for local Hamiltonians use the same idea; see [Trotter-Suzuki product formulas](/trotter-suzuki-product-formulas/).
- **Correlations in gapped ground states.** Hastings and Koma (2006) and Nachtergaele and Sims (2006) used the bound to prove that a ground state with a spectral gap $\Delta$ has correlations $\langle AB\rangle - \langle A\rangle\langle B\rangle$ that decay exponentially in the distance, at a rate of order $\Delta/v$.
- **Entanglement grows at most linearly.** An evolution of time $t$ can be approximated by a circuit of depth of order $vt$ of local blocks, so the [entanglement entropy](/entanglement-entropy/) across a cut grows by $O(vt)$, up to the error of the approximation.
- **The XX chain as a check.** Through the [Jordan-Wigner transformation](/jordan-wigner-transformation/), $H = \frac J2\sum_x (X_xX_{x+1} + Y_xY_{x+1})$ is one fermion hopping with amplitude $J$, and $\|h_x\| = J$. For $A = \sigma^-_0 = \frac12(X_0 + iY_0)$ and $B = Z_d$, the commutator norm is exactly $2|U_{0d}(t)|$, with $U = e^{-iht}$ the $n \times n$ hopping propagator. On the half-infinite chain, $U_{0d}(t)$ follows from the Bessel functions by the method of images, which gives $\|[\tau_t(\sigma^-_0), Z_d]\| = 2(d+1)|J_{d+1}(2Jt)|/(Jt)$. These agree with the $2^5$-dimensional spin computation on 5 sites to $10^{-9}$ and with the $40 \times 40$ hopping matrix to $10^{-12}$.

## Tightness

The measured light cone of the XX chain, with $J = 1$: the first time $t$ at which the commutator norm reaches $\varepsilon = 10^{-3}$, against the times at which the two forms of the bound reach $\varepsilon$.

| distance $d$ | measured | series bound | exponential bound |
|---|---|---|---|
| 2 | 0.032 | 0.0064 | below 0 |
| 4 | 0.333 | 0.0599 | below 0 |
| 8 | 1.497 | 0.2496 | 0.0493 |
| 12 | 2.961 | 0.4743 | 0.2946 |
| 16 | 4.556 | 0.7102 | 0.5398 |
| 24 | 7.943 | 1.194 | 1.0303 |
| 32 | 11.474 | 1.6834 | 1.5208 |

- **The shape is right.** For small $t$, $J_{d+1}(x) \approx (x/2)^{d+1}/(d+1)!$ gives $\|[\tau_t(\sigma^-_0), Z_d]\| = 2(Jt)^d/d!\,(1 + O(t^2))$. The first term of the bound is $\frac43(6Jt)^d/d!$. So the power $t^d$ and the factor $1/d!$ cannot be improved, only the base $6$.
- **The velocity is not.** From $d = 24$ to $d = 32$ the measured front moves at $8/(11.474 - 7.943) \approx 2.27$, and it tends to $2J$, the largest group velocity $\max_k |d(2J\cos k)/dk|$ of the hopping band. The series bound moves at about $6eJ \approx 16.3J$. The constant 6 comes from counting all chains of bonds, most of which do not describe a real path of the excitation. This is measured, not proved.
- **Far outside the cone.** At $t = 0.5$ and $d = 16$, the measured value is $1.4 \times 10^{-18}$ and the bound is $3.3 \times 10^{-6}$.
- **An interacting chain.** For the Heisenberg chain $J\sum_x \vec S_x\cdot\vec S_{x+1}$ on 5 sites, with bond norm $\frac34 J$ and $A = Z_0$, $B = Z_d$:

| $t$ | $d = 1$ | $d = 2$ | $d = 3$ | $d = 4$ |
|---|---|---|---|---|
| 0.1, measured / bound | 0.1996 / 0.758 | $5.08\times10^{-3}$ / 0.158 | $2.0\times10^{-4}$ / 0.0228 | $2.9\times10^{-6}$ / $2.5\times10^{-3}$ |
| 0.25 | 0.493 / 2.77 | 0.0324 / 1.27 | $3.1\times10^{-3}$ / 0.43 | $1.1\times10^{-4}$ / 0.11 |
| 0.5 | 0.947 / 11.3 | 0.133 / 8.3 | 0.0244 / 4.9 | $1.8\times10^{-3}$ / 2.4 |

  The bound holds at every entry, and it is larger than the trivial bound $2\|A\|\|B\| = 2$ once $t$ is of order $1/J$ at small $d$.
- **Bounded terms are needed.** For bosons with unbounded operators, such as $a^\dagger a$, the norm $\|h_x\|$ is infinite, and no bound of this form holds in general. For power-law interactions $1/r^\alpha$ the light cone can bend or disappear, depending on $\alpha$.

## History

Lieb and Robinson (1972) proved the bound for quantum spin systems with finite-range interactions, to show that such systems have a finite group velocity. The result had few uses for thirty years. Around 2004 to 2006 it became a main tool of quantum many-body theory. Hastings and Koma (2006) extended it to interactions that decay with distance and used it for the exponential decay of correlations in gapped ground states. Nachtergaele and Sims (2006) gave the short proof by a differential inequality and an iteration over chains of terms, which is the proof above. Haah, Hastings, Kothari and Low (2018) used it to build a nearly optimal algorithm for the simulation of lattice Hamiltonians.

## References
