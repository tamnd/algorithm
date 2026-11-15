---
title: PerfectRef terminates and its union of conjunctive queries gives exactly the certain answers
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page, lines L1 to L9. The TBox $T$ is a DL-Lite$_R$ TBox with positive inclusions only: concept inclusions $B_1 \sqsubseteq B_2$ between basic concepts $B ::= A \mid \exists P \mid \exists P^-$, and role inclusions $R_1 \sqsubseteq R_2$ between roles $R ::= P \mid P^-$. Negative inclusions only decide whether the knowledge base is consistent (see the end). A conjunctive query (CQ) $q(\vec x)$ is a set of atoms $A(t)$ and $P(t_1, t_2)$ over variables; the head $\vec x$ lists the answer variables. Every CQ is kept in the normal form $\tau(q)$: a variable that occurs once in the body and not in the head is written $\_$, and each $\_$ is a different variable. This proof follows the one of Calvanese, De Giacomo, Lembo, Lenzerini and Rosati (2007), with the chase written out in single steps.

## Definitions

The atom $\mathrm{basic}(B, t)$ is $A(t)$ for $B = A$, $Q(t, \_)$ for $B = \exists Q$ and $Q(\_, t)$ for $B = \exists Q^-$. An inclusion $I$ is applicable to an atom $g$, and $\mathrm{gr}(g, I)$ is defined, in these cases:

- $g = A(t)$ and $I = B \sqsubseteq A$: $\mathrm{gr}(g, I) = \mathrm{basic}(B, t)$.
- $g = P(t, \_)$ and $I = B \sqsubseteq \exists P$: $\mathrm{gr}(g, I) = \mathrm{basic}(B, t)$.
- $g = P(\_, t)$ and $I = B \sqsubseteq \exists P^-$: $\mathrm{gr}(g, I) = \mathrm{basic}(B, t)$.
- $g = P(t_1, t_2)$ and $I = R \sqsubseteq P$ or $I = R \sqsubseteq P^-$: $\mathrm{gr}(g, I)$ is $R(t_1, t_2)$, or $R(t_2, t_1)$ in the second case, with $Q^-(s, s')$ read as $Q(s', s)$.

For two atoms $g_1, g_2$ with the same predicate, $\mathrm{reduce}(q, g_1, g_2)$ applies to $q$ the most general unifier $\sigma$ of $g_1$ and $g_2$; a position with $\_$ on one side takes the term of the other side, and two $\_$ stay one $\_$. The answers of a CQ $q$ over an interpretation $I$ are the tuples $h(\vec x)$ for the maps $h$ from the variables of $q$ to the domain with $h(g)$ true in $I$ for every atom $g$; such an $h$ is a match. An ABox $A$ is read as a finite interpretation whose domain is its individuals. The certain answers of $q$ over $K = (T, A)$ are the tuples of individuals that are answers over every model of $K$.

## Termination

**Lemma 1.** Every CQ in PR has at most $n$ atoms, where $n$ is the number of atoms of the input, and its terms are among the variables of the input and $\_$.

*Proof.* Line L5 replaces one atom by one atom, and the new atom uses the terms of the old one and possibly $\_$. Line L7 merges two atoms into one and only identifies variables that already occur. The map $\tau$ only replaces variables by $\_$. $\square$

Let $m$ be the number of concept and role names of $T$ and $q$, and $v$ the number of variables of $q$. By Lemma 1, a CQ in PR is a set of at most $n$ atoms chosen from at most $a = m(v + 1)^2$ atoms, so PR has at most $(a + 1)^n$ elements. Line L8 puts a CQ on TODO only when it is new in PR, and nothing is removed from PR, so the loop of line L2 runs at most $(a + 1)^n$ times and stops.

## Soundness

**Lemma 2.** If $q'$ is added at line L5 or line L7 while $q$ is processed, then for every model $I$ of $T$, every answer of $q'$ over $I$ is an answer of $q$ over $I$.

*Proof.* Let $h$ be a match of $q'$ in $I$.

Line L5: $q'$ is $q$ with $g$ replaced by $g' = \mathrm{gr}(g, I)$, then $\tau$. The other atoms hold under $h$. If $g = A(t)$, then $g'$ says $h(t) \in B^I$, and $B^I \subseteq A^I$ because $I$ satisfies the inclusion, so $g$ holds. If $g = P(t, \_)$, then $h(t) \in B^I \subseteq (\exists P)^I$, so $h(t)$ has a $P$-successor $e$; the $\_$ of $g$ occurs nowhere else, so extending $h$ with $\_ \mapsto e$ makes $g$ true without changing any other atom. The case $P(\_, t)$ is the same with predecessors. For a role inclusion, $g'$ says $(h(t_1), h(t_2)) \in R^I \subseteq P^I$. In every case $h$, extended on the $\_$ of $g$, is a match of $q$ with the same head values. The map $\tau$ only renames variables that occur once and are not in the head, so it does not change the answers.

Line L7: $q' = \tau(\sigma(q))$. Then $h \circ \sigma$ maps every atom of $q$ to the image of an atom of $\sigma(q)$, so it is a match of $q$, and its head values are $h(\sigma(\vec x))$, the head values of $q'$. $\square$

**Corollary.** Every tuple that PR finds over the ABox $A$ is a certain answer of $q$ over $K = (T, A)$.

*Proof.* Let $q'$ in PR have a match $h$ in $A$ with head values $\vec a$. Every model $I$ of $K$ contains the facts of $A$ with each individual interpreted by itself, so $h$ is also a match of $q'$ in $I$. By Lemma 2 and induction along the steps that made $q'$, $\vec a$ is an answer of $q$ over $I$. $\square$

## Completeness

The chase of $K$ is a sequence $A = C_0 \subseteq C_1 \subseteq \dots$ of sets of facts. Each step takes one inclusion that is violated in $C_{k-1}$ and adds one fact:

- $B \sqsubseteq A$ with $c \in B$ in $C_{k-1}$: add $A(c)$.
- $B \sqsubseteq \exists P$ with $c \in B$ in $C_{k-1}$ and no $P$-successor of $c$: add $P(c, d)$ for a new element $d$. The case $\exists P^-$ adds $P(d, c)$.
- $R \sqsubseteq P$ with $R(c, e)$ in $C_{k-1}$: add $P(c, e)$, and the same for $P^-$.

Here $c \in \exists Q$ means that some fact $Q(c, e)$ is present. If the steps are taken fairly, the union $C$ of all $C_k$ is a model of $K$, and it maps into every model of $K$ by a homomorphism that is the identity on individuals (Calvanese et al. 2007, the canonical interpretation). A match of $q$ in $C$ followed by this homomorphism is a match in every model, so a tuple of individuals is a certain answer if and only if it is an answer over $C$. A match uses finitely many facts, so it is a match in some $C_k$.

**Lemma 3.** If some $q'$ in PR has a match $h$ in $C_k$ with $k \ge 1$ and head values $\vec a$ of individuals, then some $q''$ in PR has a match in $C_{k-1}$ with the same head values.

*Proof.* Let $f$ be the fact added at step $k$. If no atom of $q'$ is mapped to $f$, $h$ is already a match in $C_{k-1}$. Otherwise let $g_1, \dots, g_j$ be the atoms mapped to $f$. They have the predicate of $f$, and $h$ unifies them. If $j \ge 2$, $h$ unifies $g_1$ and $g_2$, so they have a most general unifier $\sigma$ and $h = h' \circ \sigma$ for some $h'$. The CQ $\tau(\mathrm{reduce}(q', g_1, g_2))$ was added to PR at line L7 when $q'$ was processed, it has $j - 1$ atoms mapped to $f$ by $h'$, and the head values do not change. Repeat until $j = 1$; call the result $q'$ again and the single atom $g$.

Case $f = A(c)$, made by $I = B \sqsubseteq A$: $g = A(t)$ with $h(t) = c$, and $I$ is applicable to $g$. Line L5 added $q'' = \tau(q'[g / \mathrm{basic}(B, t)])$. The step was allowed, so $c \in B$ in $C_{k-1}$: either $B(c)$ is in $C_{k-1}$, or a fact $Q(c, e)$ or $Q(e, c)$ is, and $h$ extended with $\_ \mapsto e$ matches the new atom. The other atoms of $q''$ map to facts other than $f$, so $q''$ has a match in $C_{k-1}$.

Case $f = P(c, d)$ with a new element $d$, made by $I = B \sqsubseteq \exists P$: $g = P(s, t)$ with $h(s) = c$ and $h(t) = d$, where $t$ may already be $\_$. The element $d$ is new at step $k$, so $f$ is the only fact of $C_k$ that contains it. Every atom that contains $t$ is mapped to a fact with $d$, that is to $f$, so $g$ is the only atom with $t$, and $t$ occurs once in it because $c \neq d$. The element $d$ is not an individual, so $t$ is not in the head. Hence $\tau$ has made $t$ into $\_$, $g = P(s, \_)$, and $I$ is applicable. As in the first case, $q'' = \tau(q'[g / \mathrm{basic}(B, s)])$ is in PR and has a match in $C_{k-1}$. The case $\exists P^-$ is symmetric.

Case $f = P(c, e)$ made by a role inclusion from $R(c, e)$: $g = P(t_1, t_2)$, the inclusion is applicable to $g$ in any case, and $\mathrm{gr}(g, I)$ is mapped by $h$ to the fact $R(c, e)$ of $C_{k-1}$. $\square$

**Theorem.** For a knowledge base $K = (T, A)$ with positive inclusions only, the answers of the union of the CQs of PERFECTREF$(q, T)$ over $A$ are exactly the certain answers of $q$ over $K$.

*Proof.* The Corollary gives one direction. For the other, a certain answer $\vec a$ is an answer over $C$, so $q$ has a match in some $C_k$. The input $q$ is in PR (line L1). Applying Lemma 3 $k$ times gives a CQ of PR with a match in $C_0 = A$ and head values $\vec a$. $\square$

## Negative inclusions

A negative inclusion $B_1 \sqsubseteq \neg B_2$ or $R_1 \sqsubseteq \neg R_2$ adds no facts to the chase. If $K$ is consistent, its models are the models of the positive part that satisfy the negative inclusions, and the chase $C$ is one of them, so the certain answers do not change. If $K$ is inconsistent, every tuple is a certain answer. Consistency is tested by rewriting, for each negative inclusion, the boolean query that asks for a violation, for example $\exists y\, (B_1(y) \wedge B_2(y))$, and evaluating it over $A$ (Calvanese et al. 2007). With functional roles in DL-Lite$_F$ the same method needs one more boolean query for each functionality assertion.

## Running time

Processing one CQ of PR costs $O(n \cdot |T|)$ for lines L3 to L5 and $O(n^2)$ unifications of constant size for lines L6 and L7, plus the hashing of the new CQs at line L8. With the bound of Lemma 1, the time is $(a + 1)^n \cdot O(n |T| + n^3)$ with $a = m(v + 1)^2 \le (|T| + n)(2n + 1)^2$, which is polynomial in $|T|$ for a fixed query and exponential in $n$. The rewriting does not depend on $A$. Evaluating a fixed union of CQs over a database is a first-order query, so the data complexity of query answering is in AC$^0$.

## The exponential family

Let $T_n = \{B_i \sqsubseteq A_i : 1 \le i \le n\}$ and $q_n(x) = A_1(x) \wedge \dots \wedge A_n(x)$. Line L5 can replace each $A_i(x)$ by $B_i(x)$ independently, and no two atoms unify, so PR has exactly the $2^n$ CQs $X_1(x) \wedge \dots \wedge X_n(x)$ with $X_i \in \{A_i, B_i\}$.

No union of CQs with fewer CQs is a rewriting. For a choice $c$ of one $X_i$ for each $i$, the ABox $A_c = \{X_1(a), \dots, X_n(a)\}$ has $a$ as a certain answer, so some CQ $u$ of a correct rewriting matches $A_c$ with head value $a$. All atoms of $u$ then have predicates among $X_1, \dots, X_n$. If $u$ had no atom with $A_i$ or $B_i$ for some $i$, it would also match the ABox $A_c$ without $X_i(a)$, where $a$ is not a certain answer: the interpretation with domain $\{a\}$ that puts $a$ in $A_j$ and $B_j$ for every $j \ne i$, and in neither $A_i$ nor $B_i$, is a model of $T_n$ and of that ABox with $a \notin A_i$. So the predicates of $u$ are exactly $X_1, \dots, X_n$, and different choices need different CQs. $\blacksquare$
