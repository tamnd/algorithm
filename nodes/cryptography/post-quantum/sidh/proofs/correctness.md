---
title: Both sides of SIDH compute the same j-invariant
proves: [correctness]
status: full
---

We use the notation of the page. All isogenies here have degree prime to $p$, so they are separable, and the kernel of a composite of separable isogenies is a finite subgroup. We use two standard facts.

- **(F1) Velu.** For a finite subgroup $G \subset E(\overline{\mathbb{F}}_p)$, Velu's formulas give a separable isogeny $E \to E'$ with kernel exactly $G$ (Washington, Theorem 12.16).
- **(F2) Uniqueness.** If two separable isogenies $\psi_1 : E \to E_1$ and $\psi_2 : E \to E_2$ have the same kernel, then $E_1 \cong E_2$, so $j(E_1) = j(E_2)$ (Silverman, The Arithmetic of Elliptic Curves, Corollary III.4.11 and Proposition III.4.12).

**Lemma (the chain, lines L5 to L9).** Let $R \in E$ have order $\ell^e$ with $\ell \neq p$. The loop computes a separable isogeny $\psi : E \to E'$ of degree $\ell^e$ with $\ker \psi = \langle R \rangle$, and it returns $\psi$ of every pushed point.

*Proof.* Write $\psi_i$ for the composite of the first $i$ steps, with $\psi_0$ the identity, and $R_i = \psi_i(R)$ for the value of $R$ at the start of iteration $i$. We show the invariant: $\ker \psi_i = \langle [\ell^{e-i}] R \rangle$ and $R_i$ has order $\ell^{e-i}$. For $i = 0$ this is true. Assume it for $i < e$. Line L6 sets $T = [\ell^{e-1-i}] R_i$, which has order $\ell$. Line L7 gives $\varphi$ with $\ker \varphi = \langle T \rangle$ by (F1). Then $X \in \ker(\varphi \circ \psi_i)$ if and only if $\psi_i(X) \in \langle T \rangle = \psi_i(\langle [\ell^{e-1-i}] R \rangle)$, that is, if and only if $X \in \langle [\ell^{e-1-i}] R \rangle + \ker \psi_i = \langle [\ell^{e-(i+1)}] R \rangle$. Also $\langle R_i \rangle \cap \ker \varphi = \langle T \rangle$ has order $\ell$, so $R_{i+1} = \varphi(R_i)$ has order $\ell^{e-i-1}$. Line L8 updates $R$ and the pushed points. After $e$ steps, $\ker \psi_e = \langle R \rangle$, which has $\ell^e$ elements, so $\deg \psi_e = \ell^e$, and $R_e$ is the point at infinity, which the code asserts. $\square$

**Theorem.** Let $a$ and $b$ be the secrets, $R_A = P_A + [a] Q_A$ and $R_B = P_B + [b] Q_B$. Then $\mathrm{SHARED}_A(a, \mathrm{pk}_B) = \mathrm{SHARED}_B(b, \mathrm{pk}_A)$.

*Proof.* $R_A$ has order $2^{e_A}$: if $[2^{e_A - 1}](P_A + [a] Q_A) = O$, then $[2^{e_A - 1}] P_A \in \langle [2^{e_A - 1}] Q_A \rangle$, which contradicts the fact that $(P_A, Q_A)$ is a basis of $E_0[2^{e_A}]$. In the same way $R_B$ has order $3^{e_B}$.

By lines L1 to L3 and the lemma, Alice computes $\varphi_A : E_0 \to E_A$ with kernel $\langle R_A \rangle$ and publishes $U_A = \varphi_A(P_B)$, $V_A = \varphi_A(Q_B)$. Bob computes $\varphi_B$ with kernel $\langle R_B \rangle$ and publishes $U_B = \varphi_B(P_A)$, $V_B = \varphi_B(Q_A)$.

At line L10, Alice forms $U_B + [a] V_B = \varphi_B(P_A + [a] Q_A) = \varphi_B(R_A)$, since $\varphi_B$ is a group homomorphism. Since $\ker \varphi_B = \langle R_B \rangle$ has order prime to $2$, $\varphi_B(R_A)$ still has order $2^{e_A}$. By the lemma, line L11 computes $\varphi'_A : E_B \to E_{BA}$ with kernel $\langle \varphi_B(R_A) \rangle$. As in the lemma, $\ker(\varphi'_A \circ \varphi_B) = \langle R_A \rangle + \langle R_B \rangle$. In the same way, Bob computes $\varphi'_B \circ \varphi_A : E_0 \to E_{AB}$ with kernel $\langle R_B \rangle + \langle R_A \rangle$. The two composites are separable and have the same kernel, so $j(E_{BA}) = j(E_{AB})$ by (F2). Line L12 returns this value on both sides. $\blacksquare$

**Remark.** The theorem needs only that the public points are the true images $\varphi(P)$ and $\varphi(Q)$. A dishonest party can send other points; then the shared $j$ may depend on one bit of the static secret, which is the attack of Galbraith, Petit, Shani and Ti. Correctness for honest parties is all that this proof claims.
