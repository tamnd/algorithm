---
tag: K3E6RZ
kind: theorem
slug: standardization-theorem
name: Standardization theorem
aliases:
- Curry-Feys standardization
- normalization theorem
area: automata-and-parsing/term-rewriting
level: advanced
summary: Any reduction to a normal form can be reordered into a leftmost-outermost reduction.
prereqs: [lambda-calculus, beta-reduction, reduction-strategy]
see_also: [outermost-reduction, church-rosser-theorem, parallel-rewriting, orthogonal-rewrite-system, weak-normalization, combinatory-logic, innermost-reduction, normal-form]
sources:
  - book: isbn:9780444875082
    title: Henk P. Barendregt, The Lambda Calculus, Its Syntax and Semantics, revised edition, North-Holland, 1984
    locator: Section 11.4 (the standardization theorem, after Curry and Feys) and Section 13.2 (the normalization theorem for leftmost reduction)
  - paper: doi:10.1016/s0747-7171(89)80045-8
    title: Masako Takahashi, Parallel reductions in lambda-calculus, Journal of Symbolic Computation 7(2) (1989)
    locator: pp. 113 to 123 (an inductive definition of standard reduction and a short proof of standardization)
  - paper: doi:10.1016/0304-3975(75)90017-1
    title: Gordon D. Plotkin, Call-by-name, call-by-value and the lambda-calculus, Theoretical Computer Science 1(2) (1975)
    locator: pp. 125 to 159 (standardization for call-by-name and call-by-value)
  - book: isbn:9780521391153
    title: Terese (Marc Bezem, Jan Willem Klop and Roel de Vrijer, editors), Term Rewriting Systems, Cambridge University Press, 2003
    locator: Chapter 8, Equivalence of reductions (standardization for orthogonal systems); Chapter 9, Strategies (leftmost-outermost reduction in left-normal systems)
---

The **standardization theorem** says that in the [lambda calculus](/lambda-calculus/) every reduction $M \to_\beta^* N$ can be rearranged into a **standard** reduction, one that works from left to right and never goes back to a redex to the left of one it has already passed. Its main corollary, the **normalization theorem**, says that if a term has a normal form, then always contracting the leftmost-outermost redex finds it. This is why call-by-name evaluation is safe: it never loops on a term that some other order would evaluate. The same results hold for orthogonal term rewriting systems, with standardization in general and normalization of leftmost-outermost reduction when the system is left-normal.

## Statement

Terms of the lambda calculus are taken modulo renaming of bound variables. $M[x := N]$ is capture-avoiding substitution, $\to_\beta$ is one [beta](/beta-reduction/) step $(\lambda x.\, P) Q \to P[x := Q]$ in any context, and $\to_\beta^*$ its reflexive transitive closure, in the notation of the term rewriting pages. $\vec N$ is a list of terms $N_1 \cdots N_k$, $k \ge 0$.

**Weak head reduction** $\to_w$ contracts the redex at the head of an application spine: $(\lambda y.\, P)\, Q\, \vec N \to_w P[y := Q]\, \vec N$. Its redex is the leftmost-outermost redex of the term.

**Standard reduction** $\to_{st}$ is the smallest relation with:

- (S1) if $M \to_w^* x$ for a variable $x$, then $M \to_{st} x$;
- (S2) if $M \to_w^* \lambda x.\, P$ and $P \to_{st} P'$, then $M \to_{st} \lambda x.\, P'$;
- (S3) if $M \to_w^* P\, Q$ and $P \to_{st} P'$ and $Q \to_{st} Q'$, then $M \to_{st} P'\, Q'$.

So a standard reduction first does weak head steps, then never touches the head again, and reduces the parts from left to right, each of them in the same standard way. This inductive definition (Takahashi, 1989) describes the same reductions as the definition by Curry and Feys: for $i < j$, the redex contracted at step $j$ is not a residual of a redex to the left of the one contracted at step $i$.

**Theorem (standardization).** If $M \to_\beta^* N$, then $M \to_{st} N$.

**Theorem (normalization).** If $M \to_\beta^* N$ and $N$ is a $\beta$-normal form, then leftmost-outermost reduction from $M$ reaches $N$ in finitely many steps.

## In plain words

An expression can usually be simplified in many orders. Some orders work inside the arguments first; others work on the outermost part first and leave the arguments until they are needed. The theorem says that whatever order you used to get from one expression to another, you can also get there by a tidy order that goes from left to right and never returns to an earlier place.

The useful consequence is about final results. If some order of simplification ends with an expression that cannot be simplified further, then the simple rule "always simplify the leftmost outermost place first" ends with the same expression. You never need to guess which order to try.

## Proof

The proof follows Takahashi (1989). It uses three facts about $\to_w$ that follow from its definition: if $P \to_w P'$, then $P\, Q \to_w P'\, Q$ and $P[x := N] \to_w P'[x := N]$; and $\to_w \subseteq \to_\beta$.

**Lemma 1 (reflexivity).** $M \to_{st} M$ for all $M$. *Proof.* Induction on $M$, with zero weak head steps: a variable by (S1), an abstraction by (S2), an application by (S3).

**Lemma 2 (head steps in front).** If $M \to_w^* M'$ and $M' \to_{st} N$, then $M \to_{st} N$. *Proof.* $M' \to_{st} N$ starts with $M' \to_w^* L$ for the $L$ in (S1), (S2) or (S3); then $M \to_w^* L$, and the same rule applies to $M$.

**Lemma 3 (substitution).** If $M \to_{st} M'$ and $N \to_{st} N'$, then $M[x := N] \to_{st} M'[x := N']$. *Proof.* Induction on the derivation of $M \to_{st} M'$. Write $\bar P$ for $P[x := N]$.

- (S1) $M \to_w^* y$ and $M' = y$. Then $\bar M \to_w^* \bar y$. If $y = x$, then $\bar y = N \to_{st} N' = M'[x := N']$, and Lemma 2 gives $\bar M \to_{st} N'$. If $y \ne x$, then $\bar M \to_w^* y$, and (S1) applies.
- (S2) $M \to_w^* \lambda z.\, P$, $P \to_{st} P'$, with $z \ne x$ and $z$ not free in $N$ or $N'$. Then $\bar M \to_w^* \lambda z.\, \bar P$, the induction hypothesis gives $\bar P \to_{st} P'[x := N']$, and (S2) applies.
- (S3) $M \to_w^* P\, Q$. Then $\bar M \to_w^* \bar P\, \bar Q$, and the induction hypothesis for $P$ and for $Q$ with (S3) gives the claim.

**Lemma 4 (one more step).** If $M \to_{st} M'$ and $M' \to_\beta N$, then $M \to_{st} N$. *Proof.* Induction on the derivation of $M \to_{st} M'$.

- (S1) $M' = x$ has no redex, so this case does not occur.
- (S2) $M \to_w^* \lambda x.\, P$, $P \to_{st} P'$, and $N = \lambda x.\, P''$ with $P' \to_\beta P''$. The induction hypothesis gives $P \to_{st} P''$, and (S2) gives $M \to_{st} N$.
- (S3) $M \to_w^* P\, Q$, $P \to_{st} P'$, $Q \to_{st} Q'$, $M' = P'\, Q'$. If the step is inside $P'$ or inside $Q'$, use the induction hypothesis and (S3). Otherwise the step is at the root: $P' = \lambda x.\, P_1'$ and $N = P_1'[x := Q']$. The only rule that gives an abstraction is (S2), so $P \to_w^* \lambda x.\, P_1$ with $P_1 \to_{st} P_1'$. Then
$$M \to_w^* P\, Q \to_w^* (\lambda x.\, P_1)\, Q \to_w P_1[x := Q].$$
Lemma 3 gives $P_1[x := Q] \to_{st} P_1'[x := Q'] = N$, and Lemma 2 gives $M \to_{st} N$.

**Proof of the standardization theorem.** Let $M = M_0 \to_\beta M_1 \to_\beta \cdots \to_\beta M_n = N$. By Lemma 1, $M \to_{st} M_0$, and by Lemma 4, $M \to_{st} M_i$ implies $M \to_{st} M_{i+1}$. $\blacksquare$

**Proof of the normalization theorem.** Write $\to_{lo}$ for a leftmost-outermost step. We show by induction on the derivation that $M \to_{st} N$ with $N$ in normal form implies $M \to_{lo}^* N$; the standardization theorem then gives the claim. In each case the first weak head steps are leftmost-outermost steps.

- (S1) $M \to_w^* x$: there is nothing more to show.
- (S2) $M \to_w^* \lambda x.\, P$ and $P \to_{st} P'$ with $P'$ normal. By induction $P \to_{lo}^* P'$, and a leftmost-outermost step in $P$ is one in $\lambda x.\, P$.
- (S3) $M \to_w^* P\, Q$, with $P'\, Q'$ normal. Then $P'$ and $Q'$ are normal and $P'$ is not an abstraction. By induction $P \to_{lo}^* P'$ and $Q \to_{lo}^* Q'$. No term on the way from $P$ to $P'$ is an abstraction, since every reduct of an abstraction is an abstraction. So no term $P_i\, Q$ is a redex at its root, and its leftmost-outermost redex lies in $P_i$ while $P_i$ is not normal. Hence $P\, Q \to_{lo}^* P'\, Q$, and then, $P'$ being normal, $P'\, Q \to_{lo}^* P'\, Q'$. $\blacksquare$

## Consequences

- **Leftmost-outermost reduction is normalizing.** It is a [reduction strategy](/reduction-strategy/) that finds the normal form of every [weakly normalizing](/weak-normalization/) term. So a term has a normal form iff its leftmost-outermost reduction terminates, which makes "has a normal form" semi-decidable by running one reduction, not a search.
- **Head normal forms.** The same method shows that a term has a head normal form iff its head reduction, which contracts the head redex under any leading abstractions, terminates. This is the basis of the theory of solvable terms and Böhm trees.
- **Call-by-name and call-by-value.** Plotkin (1975) proved standardization for both calculi and used it to relate each calculus to its evaluator: a program evaluates to a value iff it reduces to a value in the calculus.
- **Term rewriting.** In an [orthogonal](/orthogonal-rewrite-system/) system every reduction can be standardized into an outside-in reduction. In a left-normal orthogonal system, such as [combinatory logic](/combinatory-logic/), leftmost-outermost reduction is normalizing, with the same proof idea.
- **Lazy evaluation.** Graph reduction, which is leftmost-outermost reduction with sharing, inherits the normalization theorem.

## Tightness

- **Standard reductions can be longer.** $(\lambda x.\, x\, x)((\lambda y.\, y)\, z)$ reaches its normal form $z\, z$ in 2 steps if the argument is reduced first, and in 3 steps by leftmost-outermost reduction, which copies the redex $(\lambda y.\, y)\, z$ before it contracts it. Nested copying makes the gap exponential. Sharing, as in [graph reduction](/graph-reduction/), removes the copies.
- **Innermost reduction does not normalize.** $(\lambda x.\, y)\, \Omega$ with $\Omega = (\lambda x.\, x\, x)(\lambda x.\, x\, x)$ has the normal form $y$, but [innermost reduction](/innermost-reduction/) loops on $\Omega$. So the theorem picks a specific order, and "any fixed order" is false.
- **Left-normality is needed for term rewriting.** In the orthogonal system $f(x, b) \to d$, $a \to a$, $c \to b$, the term $f(a, c)$ has the normal form $d$, but leftmost-outermost reduction loops on $a$; see [reduction strategy](/reduction-strategy/). The left side $f(x, b)$ has a variable to the left of a function symbol, which left-normal systems forbid.
- **Orthogonality is needed.** For systems with overlapping rules, a normal form can depend on the choice of rule at a position, and no strategy that chooses only positions is normalizing in general.

## History

Curry and Feys proved the standardization theorem in 1958 for the lambda calculus, with standard reductions defined through residuals (Barendregt, Section 11.4). The normalization theorem for leftmost reduction follows (Barendregt, Section 13.2). Plotkin (1975) gave standardization theorems for call-by-name and call-by-value. Takahashi (1989) gave the inductive definition of standard reduction and the short proof by parallel reduction used above. For orthogonal term rewriting systems, the results are in Terese, Chapters 8 and 9.

## References
