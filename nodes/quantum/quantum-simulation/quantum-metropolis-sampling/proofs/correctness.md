---
title: The ideal quantum Metropolis walk satisfies detailed balance for the Gibbs weights, and it converges to the Gibbs state e^(-beta H)/Z when the move set generates all operators
proves: [correctness]
status: full
---

We use the pseudocode of the page and its ideal model: $H$ is a Hermitian matrix of size $d = 2^n$ with a nondegenerate spectrum $E_0 < E_1 < \cdots < E_{d-1}$ and unit eigenvectors $|E_i\rangle$; the energy measurement of line L5 is the projective measurement $\{|E_k\rangle\langle E_k|\}$; the return of line L7 is exact. The move set is a finite list of unitaries $C_j$ drawn with probabilities $p_j > 0$. It is *balanced* if for each $j$ there is a $j'$ with $C_{j'} = C_j^\dagger$ and $p_{j'} = p_j$. Let $\beta \ge 0$ be finite, $\pi_i = e^{-\beta E_i}/Z$ with $Z = \sum_ie^{-\beta E_i}$, and $A(i \to k) = \min(1, e^{-\beta(E_k - E_i)})$.

## Claim 1: the walk is a Markov chain on the eigenvectors

After line L1 and after each step the state is one of the $|E_i\rangle$. From $|E_i\rangle$, line L3 picks $C_j$ with probability $p_j$, line L4 gives $C_j|E_i\rangle$, and line L5 gives the outcome $k$ with probability $|\langle E_k|C_j|E_i\rangle|^2$ and the state $|E_k\rangle$. Lines L6 and L7 then move to $|E_k\rangle$ with probability $A(i \to k)$ and stay at $|E_i\rangle$ otherwise. The next state depends only on $i$, and for $k \ne i$

$$T_{ki} = a_{ki}A(i \to k), \qquad a_{ki} = \sum_jp_j|\langle E_k|C_j|E_i\rangle|^2,$$

with $T_{ii} = 1 - \sum_{k \ne i}T_{ki}$. Since each $C_j|E_i\rangle$ is a unit vector, $\sum_ka_{ki} = 1$; with $A \le 1$ this gives $\sum_{k \ne i}T_{ki} \le 1$, so $T_{ii} \ge 0$ and every column of $T$ is a probability distribution. A walk started at $|E_{i_0}\rangle$ is at $|E_k\rangle$ after $t$ steps with probability $(T^te_{i_0})_k$, so its state averaged over the randomness is the density matrix $\sum_k(T^te_{i_0})_k|E_k\rangle\langle E_k|$. $\square$

## Claim 2: detailed balance

If the move set is balanced, then $T_{ki}\pi_i = T_{ik}\pi_k$ for all $i, k$.

*Proof.* For $k = i$ there is nothing to prove. For $k \ne i$, $|\langle E_k|C_j|E_i\rangle| = |\overline{\langle E_i|C_j^\dagger|E_k\rangle}| = |\langle E_i|C_{j'}|E_k\rangle|$, and $p_j = p_{j'}$; the map $j \mapsto j'$ is a bijection of the list, so $a_{ki} = a_{ik}$. Further $A(i \to k)e^{-\beta E_i} = \min(e^{-\beta E_i}, e^{-\beta E_k})$, which is symmetric in $i$ and $k$. Multiply and divide by $Z$. $\square$

Summing detailed balance over $i$ gives $\sum_iT_{ki}\pi_i = \pi_k\sum_iT_{ik} = \pi_k$: the Gibbs weights are stationary. The density matrix $\sum_i\pi_i|E_i\rangle\langle E_i|$ is $e^{-\beta H}/Z$, because $e^{-\beta H} = \sum_ie^{-\beta E_i}|E_i\rangle\langle E_i|$. Without balance the claim can fail: a cyclic shift of the basis states, added to a balanced set without its inverse, gives a chain whose stationary distribution is not $\pi$.

## Claim 3: irreducibility

Suppose the move set is balanced and the $C_j$ generate the full matrix algebra, in the sense that every $d \times d$ matrix is a linear combination of products of the $C_j$. Then $T$ is irreducible.

*Proof.* Suppose a nonempty set $S$ of indices, not all of them, is closed: $T_{ki} = 0$ for all $i \in S$ and $k \notin S$. Since $A(i \to k) > 0$ for finite $\beta$, this gives $a_{ki} = 0$, so $\langle E_k|C_j|E_i\rangle = 0$ for every $j$. Then $V = \mathrm{span}\{|E_i\rangle : i \in S\}$ is invariant under every $C_j$, hence under every product of them and every linear combination of such products, which is every matrix. But some matrix maps a vector of $V$ outside $V$, since $V$ is neither $\{0\}$ nor the whole space. This contradicts the assumption. $\square$

The Pauli moves $X_q, Y_q, Z_q$ on each qubit $q$ form a balanced set (each is its own inverse) and generate the full algebra: their products give every Pauli string up to a phase, and the $4^n$ Pauli strings are a basis of the $d \times d$ matrices. A pair $e^{\mp i\theta P/2}$ is balanced; with $\theta$ not a multiple of $\pi$, $P$ is a linear combination of the two members of the pair, so pairs for $X_q$ and $Y_q$ on each qubit also generate the full algebra.

## Claim 4: convergence

Under the conditions of Claim 3 with $\beta > 0$ and $d \ge 2$, $T^tp \to \pi$ for every start $p$. With $\lambda_*$ the largest modulus of an eigenvalue of $T$ other than the eigenvalue 1, and $1 - \lambda_*$ the spectral gap,

$$2\,\|T^te_x - \pi\|_{\mathrm{TV}} \le \sqrt{\frac{1 - \pi_x}{\pi_x}}\,\lambda_*^t.$$

*Proof.* Aperiodicity: by Claim 3 some $k \ne 0$ has $a_{k0} > 0$, and $A(0 \to k) = e^{-\beta(E_k - E_0)} < 1$, so $T_{00} \ge a_{k0}(1 - A(0 \to k)) > 0$. A finite irreducible chain with one positive diagonal entry is aperiodic, so by the convergence theorem for finite Markov chains $T^tp$ converges to the unique stationary distribution, which is $\pi$ by Claim 2.

For the rate, let $D = \mathrm{diag}(\pi)$ and $S = D^{-1/2}TD^{1/2}$, so $S_{ki} = T_{ki}\sqrt{\pi_i/\pi_k}$. Detailed balance makes $S$ symmetric, so it has an orthonormal eigenbasis, with the same eigenvalues as $T$; the eigenvalue 1 has the eigenvector $u = (\sqrt{\pi_i})_i$, and it is simple by irreducibility. Let $w = D^{-1/2}(e_x - \pi)$, so $w_x = 1/\sqrt{\pi_x} - \sqrt{\pi_x}$ and $w_i = -\sqrt{\pi_i}$ otherwise. Then $\langle u, w\rangle = 1 - 1 = 0$ and $\|w\|^2 = 1/\pi_x - 1$. Since $w$ is orthogonal to $u$, $\|S^tw\| \le \lambda_*^t\|w\|$. Now $T^te_x - \pi = D^{1/2}S^tw$, because $T^t\pi = \pi$, so by Cauchy-Schwarz with $\sum_k\pi_k = 1$,

$$2\,\|T^te_x - \pi\|_{\mathrm{TV}} = \sum_k\sqrt{\pi_k}\,|(S^tw)_k| \le \|S^tw\| \le \lambda_*^t\sqrt{\frac{1 - \pi_x}{\pi_x}}. \qquad\square$$

## What is not proved here

The claims hold for the ideal model. They say nothing about the size of the spectral gap of $T$, which decides the number of steps, for any family of Hamiltonians; as for classical Metropolis chains, no general bound is known, and at low temperature it can be exponentially small. They also do not cover the circuit version, in which energies come from phase estimation with finite resolution, eigenvalues closer than the resolution are not told apart, and the return to $|E_i\rangle$ is done by rewinding. Temme et al. analyse those errors in their paper; the version with phase estimation satisfies detailed balance only approximately.
