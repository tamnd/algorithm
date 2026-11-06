---
title: Proof of the Church-Rosser theorem by parallel reduction
proves: [statement]
status: full
---

We prove that $\to_\beta$ is confluent. Terms are taken up to $\alpha$-conversion, and in each step the bound variables are chosen different from the free variables of the other terms involved (the variable convention). We use one fact about syntactic substitution, proved by induction on $M$ in Barendregt, Chapter 2:

> **(S)** If $x \ne y$ and $x \notin \mathrm{FV}(L)$, then $M[x := N][y := L] = M[y := L][x := N[y := L]]$.

**Parallel reduction.** Let $\Rightarrow$ be the least relation on lambda terms closed under these four rules:

1. $x \Rightarrow x$ for each variable $x$;
2. if $M \Rightarrow M'$ then $\lambda x.\, M \Rightarrow \lambda x.\, M'$;
3. if $M \Rightarrow M'$ and $N \Rightarrow N'$ then $M\,N \Rightarrow M'\,N'$;
4. if $M \Rightarrow M'$ and $N \Rightarrow N'$ then $(\lambda x.\, M)\,N \Rightarrow M'[x := N']$.

So $\Rightarrow$ contracts any set of redexes that are present in the term at the start, in one go.

**Lemma 1.** $M \Rightarrow M$ for each $M$.

*Proof.* Induction on $M$, with rules 1, 2 and 3. $\square$

**Lemma 2.** ${\to_\beta} \subseteq {\Rightarrow} \subseteq {\twoheadrightarrow_\beta}$. Hence $\Rightarrow^*$ and $\twoheadrightarrow_\beta$ are the same relation.

*Proof.* First inclusion: induction on the derivation of $M \to_\beta M'$. A root step $(\lambda x.\, P)\,Q \to_\beta P[x := Q]$ is rule 4 with $P \Rightarrow P$ and $Q \Rightarrow Q$ (Lemma 1). A step inside a context is rule 2 or 3, with Lemma 1 for the part that does not change. Second inclusion: induction on the derivation of $M \Rightarrow M'$. Rules 1 to 3 follow because $\twoheadrightarrow_\beta$ is reflexive and closed under the term constructors. For rule 4, by induction $M \twoheadrightarrow_\beta M'$ and $N \twoheadrightarrow_\beta N'$, so $(\lambda x.\, M)\,N \twoheadrightarrow_\beta (\lambda x.\, M')\,N' \to_\beta M'[x := N']$. Taking reflexive transitive closures of ${\to_\beta} \subseteq {\Rightarrow} \subseteq {\twoheadrightarrow_\beta}$ gives $\twoheadrightarrow_\beta \subseteq \Rightarrow^* \subseteq \twoheadrightarrow_\beta$. $\square$

**Lemma 3 (substitution).** If $M \Rightarrow M'$ and $N \Rightarrow N'$, then $M[x := N] \Rightarrow M'[x := N']$.

*Proof.* Induction on the derivation of $M \Rightarrow M'$.

- Rule 1, $M = M' = y$. If $y = x$, both sides are $N$ and $N'$, and $N \Rightarrow N'$. If $y \ne x$, both sides are $y$.
- Rule 2, $\lambda y.\, P \Rightarrow \lambda y.\, P'$ with $P \Rightarrow P'$. By the convention $y \ne x$ and $y \notin \mathrm{FV}(N) \cup \mathrm{FV}(N')$. By induction $P[x := N] \Rightarrow P'[x := N']$, and rule 2 gives $\lambda y.\, P[x := N] \Rightarrow \lambda y.\, P'[x := N']$, which are the two substituted terms.
- Rule 3: the induction hypothesis for both parts and rule 3.
- Rule 4, $(\lambda y.\, P)\,Q \Rightarrow P'[y := Q']$ with $P \Rightarrow P'$ and $Q \Rightarrow Q'$, where $y \ne x$ and $y \notin \mathrm{FV}(N')$. The left side becomes $(\lambda y.\, P[x := N])\,(Q[x := N])$. By induction $P[x := N] \Rightarrow P'[x := N']$ and $Q[x := N] \Rightarrow Q'[x := N']$, so rule 4 gives
$$(\lambda y.\, P[x := N])\,(Q[x := N]) \Rightarrow P'[x := N'][y := Q'[x := N']].$$
By (S) with the roles of the two variables exchanged ($y \ne x$, $y \notin \mathrm{FV}(N')$), this term equals $P'[y := Q'][x := N']$, the right side with the substitution applied. $\square$

**Complete development.** Define $M^*$, the result of contracting all redexes of $M$ at once, by recursion on $M$:

- $x^* = x$;
- $(\lambda x.\, M)^* = \lambda x.\, M^*$;
- $((\lambda x.\, M)\,N)^* = M^*[x := N^*]$;
- $(M\,N)^* = M^*\,N^*$ when $M$ is not an abstraction.

**Lemma 4 (triangle).** If $M \Rightarrow M'$, then $M' \Rightarrow M^*$.

*Proof.* Induction on the derivation of $M \Rightarrow M'$.

- Rule 1: $M = M' = x = M^*$, and $x \Rightarrow x$.
- Rule 2: $\lambda x.\, P \Rightarrow \lambda x.\, P'$ with $P \Rightarrow P'$. By induction $P' \Rightarrow P^*$, so $\lambda x.\, P' \Rightarrow \lambda x.\, P^* = (\lambda x.\, P)^*$.
- Rule 3: $P\,Q \Rightarrow P'\,Q'$ with $P \Rightarrow P'$ and $Q \Rightarrow Q'$. By induction $Q' \Rightarrow Q^*$.
  - If $P$ is not an abstraction, by induction $P' \Rightarrow P^*$, and rule 3 gives $P'\,Q' \Rightarrow P^*\,Q^* = (P\,Q)^*$.
  - If $P = \lambda x.\, P_0$, then $P \Rightarrow P'$ can only come from rule 2, so $P' = \lambda x.\, P_0'$ with $P_0 \Rightarrow P_0'$, a shorter derivation. By induction $P_0' \Rightarrow P_0^*$. Rule 4 gives $(\lambda x.\, P_0')\,Q' \Rightarrow P_0^*[x := Q^*] = (P\,Q)^*$.
- Rule 4: $(\lambda x.\, P)\,Q \Rightarrow P'[x := Q']$ with $P \Rightarrow P'$ and $Q \Rightarrow Q'$. By induction $P' \Rightarrow P^*$ and $Q' \Rightarrow Q^*$. Lemma 3 gives $P'[x := Q'] \Rightarrow P^*[x := Q^*] = ((\lambda x.\, P)\,Q)^*$. $\square$

**Lemma 5 (diamond).** If $M \Rightarrow M_1$ and $M \Rightarrow M_2$, then $M_1 \Rightarrow M^*$ and $M_2 \Rightarrow M^*$.

*Proof.* Lemma 4, applied twice. $\square$

**Lemma 6 (tiling).** If a relation $\Rightarrow$ has the diamond property, so does $\Rightarrow^*$.

*Proof.* First, if $M \Rightarrow M_1$ and $M \Rightarrow^n M_2$, then $M_1 \Rightarrow^n P$ and $M_2 \Rightarrow P$ for some $P$: by induction on $n$, close the first diamond, then apply the induction hypothesis to the remaining $n - 1$ steps. Next, if $M \Rightarrow^m M_1$ and $M \Rightarrow^n M_2$, then $M_1 \Rightarrow^n P$ and $M_2 \Rightarrow^m P$ for some $P$: by induction on $m$, using the first claim for the first step of the $m$ steps and the induction hypothesis for the rest. $\square$

**Theorem.** $\to_\beta$ is confluent.

*Proof.* Let $M \twoheadrightarrow_\beta M_1$ and $M \twoheadrightarrow_\beta M_2$. By Lemma 2, $M \Rightarrow^* M_1$ and $M \Rightarrow^* M_2$. By Lemmas 5 and 6 there is $P$ with $M_1 \Rightarrow^* P$ and $M_2 \Rightarrow^* P$. By Lemma 2 again, $M_1 \twoheadrightarrow_\beta P$ and $M_2 \twoheadrightarrow_\beta P$. $\blacksquare$

The proof also bounds the length of the join: if $M_1$ and $M_2$ are reached by $m$ and $n$ parallel steps, they meet after $n$ and $m$ parallel steps.
