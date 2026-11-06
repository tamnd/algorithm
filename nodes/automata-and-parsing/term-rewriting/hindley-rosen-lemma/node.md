---
tag: 1C3EF3
kind: theorem
slug: hindley-rosen-lemma
name: Hindley-Rosen lemma
area: automata-and-parsing/term-rewriting
level: advanced
summary: Commuting confluent relations have a confluent union.
prereqs: [confluence, abstract-reduction-system]
see_also: [church-rosser-theorem, orthogonal-confluence-theorem, newman-lemma, local-confluence, beta-reduction, critical-pair-lemma, joinability]
sources:
  - paper: doi:10.1145/321738.321750
    title: Barry K. Rosen, Tree-manipulating systems and Church-Rosser theorems, Journal of the ACM 20(1) (1973)
    locator: pp. 160 to 187 (the union of commuting Church-Rosser relations is Church-Rosser)
  - book: isbn:9780444875082
    title: Henk P. Barendregt, The Lambda Calculus, Its Syntax and Semantics, revised edition, North-Holland, 1984
    locator: Chapter 3, Reduction (the Hindley-Rosen lemma, Hindley's strong commutation lemma, and confluence of beta-eta reduction)
  - book: isbn:9780521391153
    title: Terese (Marc Bezem, Jan Willem Klop and Roel de Vrijer, editors), Term Rewriting Systems, Cambridge University Press, 2003
    locator: Chapter 1, Abstract reduction systems (commutation and the confluence of unions)
  - paper: doi:10.1145/7531.7534
    title: Yoshihito Toyama, On the Church-Rosser property for the direct sum of term rewriting systems, Journal of the ACM 34(1) (1987)
    locator: pp. 128 to 143 (confluence of the union of systems over disjoint signatures)
---

The **Hindley-Rosen lemma** says that the union of two [confluent](/confluence/) relations is confluent if the two relations commute: whenever one relation leads from an object to one result and the other relation leads to another result, the first result can be continued with the second relation and the second with the first to a common object. It splits a confluence proof into smaller ones, one per kind of step plus one commutation proof. The classic use is confluence of beta-eta reduction in the lambda calculus, from confluence of beta, confluence of eta, and a commutation lemma.

## Statement

We use the notation of the [abstract reduction system](/abstract-reduction-system/) pages: relations $\to_1$, $\to_2$ on a set $A$, $\to^*$ for the reflexive transitive closure of a relation $\to$, $\to^=$ for its reflexive closure, and $\leftarrow$ for its inverse. For term rewriting systems, $A$ is the set of terms $T(\Sigma, V)$ and $\to_i$ is $\to_{R_i}$.

The relations $\to_1$ and $\to_2$ **commute** if $a \to_1^* b$ and $a \to_2^* c$ imply that there is a $d$ with $b \to_2^* d$ and $c \to_1^* d$. A relation is confluent iff it commutes with itself.

**Theorem (Hindley, Rosen).** If $\to_1$ and $\to_2$ are confluent and commute, then $\to_1 \cup \to_2$ is confluent.

**Lemma (Hindley's strong commutation).** If $a \to_1 b$ and $a \to_2 c$ imply that there is a $d$ with $b \to_2^* d$ and $c \to_1^= d$, then $\to_1$ and $\to_2$ commute.

The lemma turns commutation, a statement about reduction sequences, into a check of single steps.

## In plain words

Suppose there are two kinds of moves, and each kind alone never leads to a dead end that the other choices of the same kind cannot reach. Suppose also that whenever moves of the first kind and moves of the second kind lead away from the same position, the two results can be brought together, using only the second kind from one and only the first kind from the other. Then any mix of the two kinds of moves also has this property: different choices can always be brought back together.

## Proof

*Proof of the theorem.* Let $S = {\to_1^*} \cup {\to_2^*}$. Then $S^* = (\to_1 \cup \to_2)^*$, because $\to_1 \cup \to_2 \subseteq S \subseteq (\to_1 \cup \to_2)^*$.

$S$ has the diamond property: let $a \mathrel{S} b$ and $a \mathrel{S} c$. If both steps are $\to_1^*$, confluence of $\to_1$ gives $d$ with $b \to_1^* d$ and $c \to_1^* d$, two $S$-steps; likewise for $\to_2$. If $a \to_1^* b$ and $a \to_2^* c$, commutation gives $d$ with $b \to_2^* d$ and $c \to_1^* d$, again one $S$-step each; the case $a \to_2^* b$, $a \to_1^* c$ is symmetric.

A relation with the diamond property has a reflexive transitive closure with the diamond property, by tiling. First, if $a \mathrel{S} b$ and $a \mathrel{S^n} c$, there is $d$ with $b \mathrel{S^n} d$ and $c \mathrel{S} d$: by induction on $n$, close the first square at $a$ with the diamond and continue from its corner. Second, if $a \mathrel{S^m} b$ and $a \mathrel{S^n} c$, induction on $m$ with the first part closes the grid. So $S^*$, which is $(\to_1 \cup \to_2)^*$, has the diamond property, and $\to_1 \cup \to_2$ is confluent. $\blacksquare$

*Proof of the lemma.* First a strip: if $a \to_1 b$ and $a \to_2^n c$, then there is $d$ with $b \to_2^* d$ and $c \to_1^= d$. Induction on $n$. For $n = 0$ take $d = b$. Otherwise $a \to_2 c_1 \to_2^{n-1} c$. The hypothesis gives $d_1$ with $b \to_2^* d_1$ and $c_1 \to_1^= d_1$. If $c_1 = d_1$, then $b \to_2^* c_1 \to_2^{n-1} c$, and $d = c$ works. If $c_1 \to_1 d_1$, the induction hypothesis for $c_1 \to_1 d_1$ and $c_1 \to_2^{n-1} c$ gives $d$ with $d_1 \to_2^* d$ and $c \to_1^= d$, so $b \to_2^* d$.

Now let $a \to_1^m b$ and $a \to_2^* c$, and use induction on $m$. For $m = 0$ take $d = c$. Otherwise $a \to_1 b_1 \to_1^{m-1} b$. The strip gives $e$ with $b_1 \to_2^* e$ and $c \to_1^= e$. The induction hypothesis for $b_1 \to_1^{m-1} b$ and $b_1 \to_2^* e$ gives $d$ with $b \to_2^* d$ and $e \to_1^* d$. Then $c \to_1^= e \to_1^* d$. $\blacksquare$

## Consequences

- **Beta-eta reduction.** In the lambda calculus, [beta-reduction](/beta-reduction/) is confluent by the [Church-Rosser theorem](/church-rosser-theorem/), eta-reduction $\lambda x.\, M\,x \to M$ (with $x$ not free in $M$) is confluent, and a beta-step and an eta-step from the same term satisfy Hindley's strong commutation condition. So beta-eta reduction is confluent.
- **Adding rules to a confluent system.** To show that $R_1 \cup R_2$ is confluent for confluent [term rewriting systems](/term-rewriting-system/) $R_1$ and $R_2$, it is enough to prove that $\to_{R_1}$ and $\to_{R_2}$ commute, often by checking the single-step condition of the lemma on the overlaps between rules of $R_1$ and rules of $R_2$.
- **Confluence without termination.** Neither the theorem nor the lemma needs termination, in contrast with [Newman's lemma](/newman-lemma/). They are used next to the [orthogonal confluence theorem](/orthogonal-confluence-theorem/), for example to add confluent delta rules to an orthogonal calculus.
- **Commuting a relation with itself.** With $\to_1 = \to_2 = \to$, the strong commutation lemma says: if every peak $b \leftarrow a \to c$ can be closed by $b \to^* d$ and $c \to^= d$, then $\to$ is confluent. This is the form used for strongly closed critical pairs.

## Tightness

- **Commutation is needed.** $\to_1 = \{ a \to b \}$ and $\to_2 = \{ a \to c \}$ are each confluent, and their union has the two normal forms $b$ and $c$ of $a$.
- **Commutation of single steps is not enough.** Strong commutation asks for $c \to_1^= d$, at most one step. Allowing any number of steps fails. Let $\to_1 = \{ b \to a,\ e \to b \}$ and $\to_2 = \{ b \to e,\ e \to d,\ d \to c \}$. Both are confluent, and each single-step peak closes with $\to_2^*$ on one side and $\to_1^*$ on the other: from $b$, $a$ and $e \to_1^* a$; from $e$, $b \to_2^* d$ and $d$. But $b \to_1 a$ and $b \to_2^* c$ lead to two distinct normal forms, so the union is not confluent. This is the commutation form of the failure of [local confluence](/local-confluence/) without termination.
- **The condition is not necessary.** $\to_1 = \{ a \to b \}$ and $\to_2 = \{ a \to c,\ c \to b \}$ do not commute, since $b$ and $c$ have no common reduct with $c$ using only $\to_1$ and $b$ using only $\to_2$. Their union is confluent all the same.
- **Disjoint unions.** For term rewriting systems over disjoint signatures, the union of two confluent systems is always confluent, although the systems need not commute in this sense: this is Toyama's theorem (1987), which needs a much longer proof.

## History

J. Roger Hindley proved the commutation lemmas in his 1964 thesis on the Church-Rosser property in combinatory logic and the lambda calculus. Barry Rosen proved the union theorem independently in 1973, in his study of tree-manipulating systems. Barendregt's book made the name "Hindley-Rosen lemma" standard and used it for the confluence of beta-eta reduction. Toyama's theorem of 1987 on direct sums started the study of modular properties of term rewriting systems.

## References
