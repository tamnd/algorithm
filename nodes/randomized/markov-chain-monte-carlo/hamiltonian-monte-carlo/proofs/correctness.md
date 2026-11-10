---
title: Each HMC iteration leaves π(q) N(p; 0, I) invariant, and the position chain is reversible with respect to π
proves: [correctness]
status: full
---

**Setting.** $\tilde\pi = Z\pi$ is positive and continuously differentiable on $\mathbb{R}^d$, $U = -\log\tilde\pi$, and $H(q, p) = U(q) + |p|^2/2$. The extended target on $\mathbb{R}^{2d}$ is

$$\bar\pi(q, p) = \pi(q)\,\varphi(p) \propto e^{-H(q, p)},$$

where $\varphi$ is the $\mathcal{N}(0, I_d)$ density. Its $q$-marginal is $\pi$. Write $z = (q, p)$. Let $\Psi$ be one leapfrog step of size $\varepsilon$ (lines L6 to L8), $F(q, p) = (q, -p)$ and $G = F \circ \Psi^L$. One iteration of the algorithm is the composition of two kernels: $K_1$, which replaces $p$ by a fresh draw from $\varphi$ (line L3), and $K_2$, which moves from $z$ to $G(z)$ with probability $\alpha(z) = \min(1, \bar\pi(G(z))/\bar\pi(z))$ and otherwise stays at $z$ (lines L4 to L11).

**Step 1: $K_1$ keeps $\bar\pi$.** Under $\bar\pi$, $q$ and $p$ are independent and $p \sim \varphi$. If $(q, p) \sim \bar\pi$, then $q \sim \pi$, and $K_1$ returns $(q, p^\ast)$ with $p^\ast \sim \varphi$ independent of $q$. So $(q, p^\ast) \sim \bar\pi$. This is a [Gibbs](/gibbs-sampling/) update of the block $p$.

**Step 2: $G$ is a bijection, $G \circ G$ is the identity, and $|\det DG| = 1$.** The leapfrog step is the composition $\Psi = S_1 \circ D \circ S_1$ of the maps

$$S_1(q, p) = (q, p + \tfrac\varepsilon2\nabla\log\tilde\pi(q)), \qquad D(q, p) = (q + \varepsilon p, p).$$

Each is a bijection with an explicit inverse (subtract instead of add), and each has a block triangular Jacobian with identity blocks on the diagonal, so its determinant is 1. Hence $\Psi$ and $\Psi^L$ are $C^1$ bijections with Jacobian determinant 1, and so is $G$, because $\det DF = (-1)^d$ has absolute value 1.

Now $F \circ S_1 \circ F = S_1^{-1}$: indeed $F(S_1(q, -p)) = F(q, -p + \frac\varepsilon2\nabla\log\tilde\pi(q)) = (q, p - \frac\varepsilon2\nabla\log\tilde\pi(q)) = S_1^{-1}(q, p)$. In the same way, $F(D(q, -p)) = F(q - \varepsilon p, -p) = (q - \varepsilon p, p) = D^{-1}(q, p)$, so $F \circ D \circ F = D^{-1}$. Since $F \circ F$ is the identity,

$$F \circ \Psi \circ F = (F S_1 F)(F D F)(F S_1 F) = S_1^{-1}D^{-1}S_1^{-1} = \Psi^{-1},$$

and then $F \circ \Psi^L \circ F = (F\Psi F)^L = \Psi^{-L}$. So $G \circ G = F\Psi^LF\Psi^L = \Psi^{-L}\Psi^L$ is the identity.

**Step 3: $K_2$ satisfies detailed balance with respect to $\bar\pi$.** It is enough to show that, for all Borel sets $A, B \subseteq \mathbb{R}^{2d}$,

$$\int_A \bar\pi(z)\,\alpha(z)\,\mathbf{1}_B(G(z))\,dz = \int_B \bar\pi(w)\,\alpha(w)\,\mathbf{1}_A(G(w))\,dw,$$

because the rejection part of $K_2$ puts mass only on the diagonal, $\{(z, z)\}$, and is symmetric by itself. Note that $\bar\pi(z)\alpha(z) = \min(\bar\pi(z), \bar\pi(G(z)))$, a symmetric function of the pair $(z, G(z))$. In the left side, substitute $z = G(w)$. By Step 2, $G$ is a $C^1$ bijection of $\mathbb{R}^{2d}$ onto itself with $|\det DG| = 1$ and $G(z) = G(G(w)) = w$, so $dz = dw$ and the left side becomes

$$\int \mathbf{1}_A(G(w))\,\min(\bar\pi(G(w)), \bar\pi(w))\,\mathbf{1}_B(w)\,dw,$$

which is the right side. So $\bar\pi(dz)K_2(z, dw)$ is a symmetric measure, and taking $A = \mathbb{R}^{2d}$ shows that $\bar\pi K_2 = \bar\pi$.

**Step 4: the test is line L11.** $\bar\pi(G(z))/\bar\pi(z) = e^{H(z) - H(G(z))}$, since the normalizing constants cancel. Line L11 accepts when $u < e^{H(z) - H(G(z))}$ with $u$ uniform on $[0, 1)$, which has probability $\alpha(z)$. Lines L4 to L9 compute $G(z)$.

**Step 5: invariance and reversibility in $q$.** An iteration is $K_1$ followed by $K_2$, and both keep $\bar\pi$, so their composition keeps $\bar\pi$. If $X_{t-1} \sim \pi$, then after line L3 the pair $(X_{t-1}, p)$ has law $\bar\pi$, after line L11 the pair still has law $\bar\pi$, and so $X_t \sim \pi$. For reversibility, the position kernel is $P(q, A) = \int\varphi(p)\,K_2((q, p), A \times \mathbb{R}^d)\,dp$. For Borel sets $A, B \subseteq \mathbb{R}^d$,

$$\int_B\pi(q)P(q, A)\,dq = \int \bar\pi(z)\,K_2(z, A \times \mathbb{R}^d)\,\mathbf{1}_{B \times \mathbb{R}^d}(z)\,dz,$$

and by Step 3 (the symmetry of $\bar\pi(dz)K_2(z, dw)$) this is unchanged when the roles of $A \times \mathbb{R}^d$ and $B \times \mathbb{R}^d$ are swapped. So $\int_B\pi P(\cdot, A) = \int_A\pi P(\cdot, B)$, which is [detailed balance](/detailed-balance/) for the position chain. $\blacksquare$

**Remarks.** The proof never used that $\Psi$ approximates the Hamiltonian flow. Any vector field in place of $\nabla\log\tilde\pi$ in $S_1$ gives a valid sampler, because Steps 2 and 3 use only the shear structure. Accuracy matters only for the acceptance rate: $\alpha(z) = \min(1, e^{-\Delta H})$ is close to 1 when the energy error $\Delta H = H(G(z)) - H(z)$ is small, which leapfrog gives with $\Delta H = O(\varepsilon^2)$ over a fixed time, as shown on the [Hamiltonian dynamics](/hamiltonian-dynamics/) page. Invariance does not give convergence: the example of the main page with $\varepsilon = \sqrt2$ and $L = 2$ on $\mathcal{N}(0, 1)$ is invariant but periodic.
