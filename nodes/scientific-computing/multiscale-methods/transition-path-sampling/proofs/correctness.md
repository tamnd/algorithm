---
title: Why shooting and shifting sample the transition path ensemble
proves: [correctness]
status: full
---

We prove that each move of the implementation satisfies detailed balance with respect to the transition path ensemble, so the path chain has this ensemble as a stationary distribution.

**Setting.** $(X_n)$ is a Markov chain with transition probabilities $p(x, y)$ and a stationary distribution $\pi$. The backward kernel is $\tilde p(y, x) = \pi(x) p(x, y) / \pi(y)$; it is a transition probability because $\pi$ is stationary, and $\tilde p = p$ if the chain is reversible. A path is $x = (x_0, \ldots, x_N)$. Its weight is
$$\mathcal{P}[x] = \pi(x_0) \prod_{i=0}^{N-1} p(x_i, x_{i+1}), \qquad \mathcal{P}_{AB}[x] = \frac{h_A(x_0)\, \mathcal{P}[x]\, h_B(x_N)}{Z_{AB}},$$
with $Z_{AB}$ the normalizing sum. $\mathcal{P}_{AB}$ is the transition path ensemble.

**Lemma 1 (the backward identity).** For every $k$, $\pi(x_0) \prod_{i<k} p(x_i, x_{i+1}) = \pi(x_k) \prod_{i<k} \tilde p(x_{i+1}, x_i)$.

*Proof.* Each factor $\tilde p(x_{i+1}, x_i) = \pi(x_i) p(x_i, x_{i+1}) / \pi(x_{i+1})$; the product telescopes to $\pi(x_0) / \pi(x_k)$ times $\prod_{i<k} p(x_i, x_{i+1})$. $\square$

So the path weight has the two factorizations
$$\mathcal{P}[x] = \underbrace{\pi(x_k) \prod_{i<k} \tilde p(x_{i+1}, x_i)}_{\text{the part before } k} \cdot \underbrace{\prod_{i \ge k} p(x_i, x_{i+1})}_{\text{the part after } k}.$$

**Lemma 2 (shooting).** Fix the slice $k$ and the direction. A forward shot from $x$ keeps $x_0, \ldots, x_k$ and generates $y_{k+1}, \ldots, y_N$ with the probability $g(x \to y) = \prod_{i \ge k} p(y_i, y_{i+1})$. The reverse move, from $y$ back to $x$, is a forward shot from the same slice with $g(y \to x) = \prod_{i \ge k} p(x_i, x_{i+1})$. Then $\mathcal{P}[x]\, g(x \to y) = \mathcal{P}[y]\, g(y \to x)$. The same holds for a backward shot, with $\tilde p$ and the part before $k$.

*Proof.* By the factorization, $\mathcal{P}[x] = C \cdot \prod_{i \ge k} p(x_i, x_{i+1})$ and $\mathcal{P}[y] = C \cdot \prod_{i \ge k} p(y_i, y_{i+1})$ with the same factor $C$ for the shared part before $k$. Both sides equal $C \cdot g(x \to y)\, g(y \to x)$. For a backward shot, the part after $k$ is shared, and the generated part has the probability $\prod_{i<k} \tilde p(y_{i+1}, y_i)$, which by Lemma 1 is the part before $k$ of $\mathcal{P}[y]$ divided by $\pi(x_k) = \pi(y_k)$. The same computation applies. $\square$

**Lemma 3 (shifting).** A forward shift by $s$ maps $x$ to $y = (x_s, \ldots, x_N, z_1, \ldots, z_s)$, with $g(x \to y) = \prod_{j} p(z_{j-1}, z_j)$ for $z_0 = x_N$. Its reverse is the backward shift by $s$, which regenerates $x_{s-1}, \ldots, x_0$ from $x_s$ with $g(y \to x) = \prod_{i<s} \tilde p(x_{i+1}, x_i)$. Then $\mathcal{P}[x]\, g(x \to y) = \mathcal{P}[y]\, g(y \to x)$.

*Proof.* By Lemma 1, $\mathcal{P}[x] = \pi(x_s) \prod_{i<s} \tilde p(x_{i+1}, x_i) \cdot \prod_{i \ge s} p(x_i, x_{i+1}) = g(y \to x) \cdot \pi(x_s) \prod_{i \ge s} p(x_i, x_{i+1})$. And $\mathcal{P}[y] = \pi(x_s) \prod_{i \ge s} p(x_i, x_{i+1}) \cdot g(x \to y)$. Multiply the first by $g(x \to y)$ and the second by $g(y \to x)$; the two products are equal. $\square$

**Theorem.** The path chain of the implementation leaves $\mathcal{P}_{AB}$ invariant.

*Proof.* The implementation chooses the move type, the slice $k$ (uniform), the shift $s$ (uniform) and the direction with probabilities that are the same for a move and its reverse: a forward shot from $k$ is reversed by a forward shot from $k$, a forward shift by $s$ by a backward shift by $s$, and each is chosen with the same probability. It accepts the trial $y$ if and only if $h_A(y_0) h_B(y_N) = 1$. For two reactive paths $x \ne y$, the probability of the move from $x$ to $y$ is $c \cdot g(x \to y)$ with the same $c$ as for the reverse, and so
$$\mathcal{P}_{AB}[x]\, c\, g(x \to y) = \mathcal{P}_{AB}[y]\, c\, g(y \to x)$$
by Lemmas 2 and 3, because $h_A h_B = 1$ on both sides. If $y$ is not reactive, $\mathcal{P}_{AB}[y] = 0$ and the move is rejected, so it contributes nothing on either side. Detailed balance with respect to $\mathcal{P}_{AB}$ follows, and detailed balance implies invariance. $\blacksquare$

The acceptance $h_A h_B$ is the Metropolis rule $\min\{1, \mathcal{P}_{AB}[y]\, g(y \to x) / (\mathcal{P}_{AB}[x]\, g(x \to y))\}$; the lemmas show that the ratio inside is 1 for every reactive trial.

**Ergodicity.** Invariance gives the right ensemble only if the path chain is irreducible on the reactive paths. In the test chain, a forward shot from $k = 0$ can produce any reactive path in one move, because every path from state 0 has positive probability; so the chain is irreducible and, with rejections, aperiodic. For dynamics with a deterministic part, such as molecular dynamics, shooting needs a perturbation of the momenta, and irreducibility is an assumption.

**What is not proved.** The rate of convergence, and so the number of moves that a given accuracy needs, is not part of the theorem. On the page, it is measured.
