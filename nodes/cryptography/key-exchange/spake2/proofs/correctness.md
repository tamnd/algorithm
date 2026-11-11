---
title: Correctness of SPAKE2
proves: [correctness]
status: full
---

We prove that two honest parties with the same password scalar $w$ compute the same $K$, the same transcript and the same keys, that both confirmation tags verify, and that with different password scalars the tags fail except with negligible probability. Notation is that of the page: $P$ generates the subgroup of prime order $p$, $M$ and $N$ lie in that subgroup, $h$ is the cofactor, and $x, y \in [1, p)$.

**Lemma 1 (honest points pass line L5).** In an honest run, $p_A$ and $p_B$ are points of the subgroup of order $p$, and each is the point at infinity $I$ with probability at most $1/(p - 1)$.

*Proof.* $p_A = wM + xP$ is a sum of two points of the subgroup, so it lies in the subgroup. $p_A = I$ means $xP = -wM$; since $P$ generates the subgroup, exactly one $x$ modulo $p$ solves this, and $x$ is uniform over $p - 1$ values. The same holds for $p_B$. $\square$

**Lemma 2 (equal K).** If both sides use the same $w$, then $A$ and $B$ compute the same $K = hxy\,P$ in line L6, and $K \ne I$.

*Proof.* $A$ computes $p_B - wN = (wN + yP) - wN = yP$, so $K_A = hx(yP) = (hxy)P$. $B$ computes $p_A - wM = (wM + xP) - wM = xP$, so $K_B = hy(xP) = (hxy)P$. Scalars commute, so $K_A = K_B$. Since $x, y \in [1, p)$, $p$ is prime and $p \nmid h$, the scalar $hxy$ is not $0$ modulo $p$, so $K \ne I$ and the abort of line L6 does not fire. $\square$

**Lemma 3 (equal keys and tags).** If $K_A = K_B$ and both sides use the same $w$, identities and AAD, then they compute the same $TT$, $K_e$, $K_a$, $K_{cA}$ and $K_{cB}$, and the checks of lines L11 and L12 pass.

*Proof.* $TT$ in line L7 is a fixed encoding of the identities, $p_A$, $p_B$, $K$ and $w$, and both sides hold the same values of all of them, so they hold the same $TT$. Lines L8 to L10 apply fixed functions (Hash, KDF and MAC) to $TT$, $K_a$ and the AAD, so all outputs are equal. Each side recomputes the tag of the other side from equal inputs, so the received tag equals the recomputed one. $\square$

**Lemma 4 (different passwords).** If $A$ uses $w$ and $B$ uses $w' \ne w \pmod p$, the transcripts $TT_A$ and $TT_B$ differ, and $B$ accepts $c_A$ only if $\mathrm{MAC}(K_{cA}, TT_A) = \mathrm{MAC}(K_{cA}', TT_B)$.

*Proof.* The last field of $TT$ is $w$ written in a fixed length, and $w \ne w'$ as integers in $[0, p)$, so $TT_A \ne TT_B$. The tag that $B$ receives is $\mathrm{MAC}(K_{cA}, TT_A)$ and the tag it computes is $\mathrm{MAC}(K_{cA}', TT_B)$; these agree only by such an equality. $\square$

If Hash is collision resistant, $\mathrm{Hash}(TT_A) \ne \mathrm{Hash}(TT_B)$ except with negligible probability, so $K_{a}$ and $K_a'$ differ, and then the two tags are outputs of HMAC under two keys that are independent outputs of HKDF. Modeling HMAC as a pseudorandom function, equal tags happen with probability about $2^{-256}$. The keys $K_e$ also differ.

**Theorem.** With the same $w$, SPAKE2 terminates, except with probability at most $2/(p - 1)$, with both sides holding the same $K_e$ and both tags accepted. With different $w$, the confirmation of line L11 fails except with negligible probability.

*Proof.* Lemma 1 shows that the honest points pass line L5, Lemma 2 gives equal $K \ne I$, and Lemma 3 gives equal keys and accepted tags. Lemma 4 and the remark after it give the claim for different passwords. $\blacksquare$

This proof covers correctness only. Security against an active attacker is the result of Abdalla and Pointcheval cited on the page.
