---
title: The torsion images fix the secret, and the toy search returns it
proves: [correctness]
status: full
---

This proof covers the toy search TOY-RECOVER of lines L1 to L6, which is the code on the page. It is not a proof of the Castryck-Decru attack, whose test of a guess rests on Kani's lemma and on a heuristic that a wrong guess does not give a split product; see the remark at the end.

**Setting.** $p = 2^{e_A} 3^{e_B} - 1$, $E_0$ supersingular with $E_0(\mathbb{F}_{p^2}) \cong (\mathbb{Z}/(p+1))^2$. We treat Alice's side; Bob's side is the same with $2$ and $3$ swapped. Write $m = 2^{e_A}$, $N = 3^{e_B}$, $(P, Q)$ for the basis of $E_0[m]$ and $(P', Q')$ for the basis of $E_0[N]$. For $s \in \{0, \ldots, m-1\}$ let $R_s = P + [s] Q$ and let $\varphi_s : E_0 \to E_s$ be the isogeny with kernel $\langle R_s \rangle$ computed by ISOGENY (its correctness is the lemma on the [SIDH page](/sidh/)). The public key is $(E_A, U, V)$ with $E_A \cong E_a$ and $U = \iota_0(\varphi_a(P'))$, $V = \iota_0(\varphi_a(Q'))$ for some isomorphism $\iota_0 : E_a \to E_A$.

We use three standard facts.

- **(F1)** Over a field of characteristic not 2 or 3, every isomorphism between curves $y^2 = x^3 + ax + b$ and $y^2 = x^3 + a'x + b'$ has the form $(x, y) \mapsto (u^2 x, u^3 y)$ with $u^4 a = a'$ and $u^6 b = b'$ (Silverman, The Arithmetic of Elliptic Curves, Proposition III.3.1(b)).
- **(F2)** For isogenies $\alpha, \beta : E \to E'$, $\deg(\alpha - \beta) \le (\sqrt{\deg \alpha} + \sqrt{\deg \beta})^2$, because $\deg$ is a positive definite quadratic form on $\mathrm{Hom}(E, E')$ (Silverman, Corollary III.6.3), so the Cauchy-Schwarz inequality applies.
- **(F3)** A nonzero isogeny $\gamma$ satisfies $\#\ker \gamma \le \deg \gamma$ (Silverman, Theorem III.4.10).

**Lemma 1.** The subgroups $\langle R_s \rangle$ for $s = 0, \ldots, m-1$ are pairwise distinct.

*Proof.* Each $R_s$ has order $m$, as on the SIDH page. If $\langle R_s \rangle = \langle R_t \rangle$, then $P + [t] Q = [k](P + [s] Q)$ for some $k$, so $[1 - k] P = [ks - t] Q$. Since $(P, Q)$ is a basis of $E_0[m] \cong (\mathbb{Z}/m)^2$, both coefficients vanish mod $m$: $k \equiv 1$ and then $t \equiv s \pmod m$. $\square$

**Lemma 2 (the images fix the isogeny).** Let $\alpha, \beta : E_0 \to E_A$ be isogenies of degree $m$ with $\alpha = \beta$ on $P'$ and $Q'$. Then $\alpha = \beta$.

*Proof.* $\alpha - \beta$ is a homomorphism that vanishes on $P'$ and $Q'$, hence on $E_0[N] = \langle P', Q' \rangle$, a group of $N^2$ elements. If $\alpha \neq \beta$, (F3) and (F2) give $N^2 \le \deg(\alpha - \beta) \le (2\sqrt{m})^2 = 4m$. For Alice's side at $p = 431$, $N^2 = 729 > 64 = 4m$; for Bob's side, $N^2 = 2^8 = 256 > 108 = 4 \cdot 27$. In SIDH in general $2^{e_A} \approx 3^{e_B}$, so $N^2 \approx m^2 > 4m$. This is a contradiction, so $\alpha = \beta$. $\square$

**Theorem.** TOY-RECOVER returns exactly $[a]$.

*Proof.* *The true secret is found.* At $s = a$, line L3 computes $E_a$ and $\varphi_a(P'), \varphi_a(Q')$. Then $j(E_a) = j(E_A)$, so the first test of line L4 holds. By (F1), $\iota_0$ is one of the maps $(x, y) \mapsto (u^2 x, u^3 y)$, and isomorphisms lists every $u$ with $u^4 a = a'$ and $u^6 b = b'$, because roots returns every root in $\mathbb{F}_{p^2}^*$ (it solves $k x \equiv t \pmod{p^2 - 1}$ for the discrete logarithm $x$, and lists all $\gcd(k, p^2 - 1)$ solutions). For $u$ of $\iota_0$, the image test of line L4 holds, so line L5 appends $a$.

*No other secret is found.* Suppose line L4 accepts $s$ with some isomorphism $\iota$. Then $\alpha = \iota \circ \varphi_s$ and $\beta = \iota_0 \circ \varphi_a$ are isogenies $E_0 \to E_A$ of degree $m$ that agree on $P'$ and $Q'$. By Lemma 2, $\alpha = \beta$, so $\langle R_s \rangle = \ker \alpha = \ker \beta = \langle R_a \rangle$, since isomorphisms have trivial kernel. By Lemma 1, $s = a$.

The loop of line L2 visits each $s$ once, so the list returned at line L6 is $[a]$. $\blacksquare$

**Why the j-invariant alone is not enough.** The first test of line L4 alone keeps every $s$ with $j(E_s) = j(E_A)$. Different kernels can give isomorphic codomains, because there are $3 \cdot 2^{e_A - 1}$ cyclic subgroups of order $2^{e_A}$ and only about $p/12$ supersingular j-invariants. At $p = 431$, 11 of Alice's 16 keys and 22 of Bob's 27 keys share their j-invariant with another key; the tests check these counts. Lemma 2 is where the torsion images enter.

**Remark on the real attack.** Kani's lemma (1997) says: if $f : E \to E_1$ and $g : E \to E_2$ are isogenies of coprime degrees $d_1$ and $d_2$ with $d_1 + d_2 = M$, and $f' : E_2 \to X$, $g' : E_1 \to X$ complete a commutative square with $\deg f' = d_1$ and $\deg g' = d_2$, then $\Phi = \begin{pmatrix} \hat f & \hat g \\ -g' & f' \end{pmatrix} : E_1 \times E_2 \to E \times X$ is an $(M, M)$-isogeny with kernel $\{(f(T), g(T)) : T \in E[M]\}$. One checks directly that this set lies in the kernel: $\hat f f(T) + \hat g g(T) = [d_1 + d_2] T = [M] T = O$, and $-g' f(T) + f' g(T) = O$ by commutativity. Castryck and Decru take $M = 2^{e_A}$, $f$ an auxiliary isogeny built from known endomorphisms, and $g$ the unknown rest of Bob's isogeny after a guess; the generators of the kernel are computable from the torsion images exactly when the guess is right. The claim that a wrong guess almost never gives a product $E \times X$ is a heuristic that they verify in experiments.
