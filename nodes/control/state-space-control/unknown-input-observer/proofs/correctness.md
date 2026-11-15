---
title: The unknown input observer has the error e' = F e for every unknown input, and its fixed eigenvalues are the invariant zeros
proves: [correctness]
status: full
---

Let $A \in \mathbb{R}^{n \times n}$, $B \in \mathbb{R}^{n \times m}$, $C \in \mathbb{R}^{p \times n}$ and $E \in \mathbb{R}^{n \times q}$ with $\operatorname{rank} E = q$. The system is $\dot x = Ax + Bu + Ed$, $y = Cx$.

## Lemma 1: the projection

If $\operatorname{rank}(CE) = q$, then $(CE)^T CE$ is invertible, the matrix $H$ of line L2 satisfies $HCE = E$, and $T = I - HC$ satisfies $TE = 0$. If $\operatorname{rank}(CE) < q$, no matrix $H$ with $HCE = E$ exists.

*Proof.* $CE \in \mathbb{R}^{p \times q}$ has full column rank, so $(CE)^T CE$ is a positive definite $q \times q$ matrix and $(CE)^+ = ((CE)^T CE)^{-1}(CE)^T$ satisfies $(CE)^+ CE = I_q$. Then $HCE = E(CE)^+CE = E$ and $TE = E - HCE = 0$. Conversely, $HCE = E$ gives $q = \operatorname{rank} E \le \operatorname{rank}(CE)$. $\square$

So line L1 rejects exactly the systems for which no observer of this form can cancel $d$: any observer $\hat x = z + Hy$ whose error is independent of $d$ needs $(I - HC)E = 0$, as the note after Lemma 2 shows.

## Lemma 2: the error equation

Let $F, G, K$ be as in lines L3 and L5, with any $K_1$. Then $e = x - \hat x$ satisfies $\dot e = Fe$ for all inputs $u$ and $d$. In discrete time, $e_{k+1} = Fe_k$.

*Proof.* $e = x - z - HCx = Tx - z$. Differentiate and use the observer equation:

$$\dot e = TAx + TBu + TEd - Fz - Gu - KCx.$$

By Lemma 1, $TE = 0$, and $G = TB$, so the terms in $d$ and $u$ vanish. Substitute $z = Tx - e$:

$$\dot e = Fe + (TA - FT - KC)x.$$

Now $FT + KC = F(I - HC) + (K_1 + FH)C = F + K_1 C = TA - K_1 C + K_1 C = TA$, using $F = TA - K_1 C$. So $\dot e = Fe$. In discrete time the same computation with $x_{k+1}$ and $z_{k+1}$ gives $e_{k+1} = Fe_k$. $\square$

The term $TEd$ is the only place where $d$ can enter. If $TE \ne 0$, then a $d$ in a direction with $TEd \ne 0$ changes $\dot e$ directly, so the error depends on $d$.

## Lemma 3: the fixed eigenvalues are the invariant zeros

Let $\operatorname{rank}(CE) = q$ and $A_1 = TA$. For $\lambda \in \mathbb{C}$, there is $v \ne 0$ with $A_1 v = \lambda v$ and $Cv = 0$ if and only if there are $v \ne 0$ and $w$ with

$$\begin{bmatrix} \lambda I - A & -E \\ C & 0 \end{bmatrix} \begin{bmatrix} v \\ w \end{bmatrix} = 0,$$

that is, if and only if $\lambda$ is an invariant zero of $(A, E, C)$.

*Proof.* Suppose $TAv = \lambda v$ and $Cv = 0$. Then $Av - HCAv = \lambda v$, so $(\lambda I - A)v = -HCAv = -E(CE)^+ CAv = Ew$ with $w = -(CE)^+CAv$. With $Cv = 0$ this is the zero equation. Conversely, suppose $(\lambda I - A)v = Ew$ and $Cv = 0$ with $v \ne 0$. Apply $T$: $T(\lambda I - A)v = TEw = 0$. Since $Cv = 0$, $Tv = v - HCv = v$, so $\lambda v = TAv$. $\square$

By the [Popov-Belevitch-Hautus test](/popov-belevitch-hautus-test/), $(C, A_1)$ is observable if and only if no such $\lambda$ exists. For every $K_1$, an unobservable eigenvalue $\lambda$ of $(C, A_1)$ is an eigenvalue of $F = A_1 - K_1 C$, since $Fv = A_1 v - K_1 Cv = \lambda v$. So the invariant zeros of $(A, E, C)$ are eigenvalues of $F$ for every gain, and the other eigenvalues can be placed freely.

## Lemma 4: the placement

If $(A, E, C)$ has no invariant zeros, line L4 returns $K_1$ with $\det(sI - (A_1 - K_1 C)) = \alpha(s)$. Otherwise line L4 raises an error.

*Proof.* By Lemma 3 and the test cited there, $(C, A_1)$ is observable exactly when there are no invariant zeros, and by duality this holds exactly when $(A_1^T, C^T)$ is controllable. PLACE is correct for controllable pairs and raises an error for the others, as proved on the [Luenberger observer](/luenberger-observer/) page. Transposition does not change the characteristic polynomial. $\square$

## Theorem

If $\operatorname{rank}(CE) = \operatorname{rank}(E)$ and $(A, E, C)$ has no invariant zeros, the algorithm returns $F, G, K, H$ with $\det(sI - F) = \alpha(s)$, and the estimate $\hat x = z + Hy$ has the error $x(t) - \hat x(t) = e^{Ft}(x(0) - \hat x(0))$ for all inputs $u$ and $d$ (in discrete time $F^k(x_0 - \hat x_0)$). If the rank condition fails or an invariant zero exists, the algorithm raises an error.

*Proof.* Lemmas 1, 2 and 4. $\square$

## Remarks

- **The general existence result.** If invariant zeros exist but all lie in the open left half plane, Lemma 3 shows that a stable $F$ still exists: put $(C, A_1)$ in the form of the [Kalman decomposition](/kalman-decomposition/) and place only the observable eigenvalues. A zero with $\operatorname{Re}\lambda \ge 0$ is an eigenvalue of every $F$, so no stable observer of this form exists. Together with Lemma 1 this gives the two conditions of Darouach, Zasadzinski and Xu.
- **Deadbeat.** With $\alpha(z) = z^n$ in discrete time, $F^n = 0$ by the [Cayley-Hamilton theorem](/cayley-hamilton-theorem/), and the estimate is exact after $n$ steps for every unknown input sequence. The tests check this in rational arithmetic.
