---
title: ALC concept satisfiability with respect to general TBoxes is EXPTIME-complete
proves: [statement]
status: full
---

ALC concepts are built from concept names, $\top$ and $\bot$ with $\neg$, $\sqcap$, $\sqcup$, $\exists r$ and $\forall r$. A general TBox $\mathcal T$ is a finite set of inclusions $X \sqsubseteq Y$ between arbitrary concepts. An interpretation $I$ is a model of $\mathcal T$ if $X^I \subseteq Y^I$ for each inclusion. $C$ is satisfiable with respect to $\mathcal T$ if $C^I \ne \emptyset$ for some model $I$ of $\mathcal T$. The input size $n$ is $|C|$ plus the sum of the sizes of the inclusions.

For a concept $D$ in negation normal form (NNF), write $\dot\neg D$ for the NNF of $\neg D$. Let $C_{\mathcal T}$ be the NNF of the conjunction of the concepts $\neg X \sqcup Y$ for $X \sqsubseteq Y$ in $\mathcal T$, and $C_{\mathcal T} = \top$ when $\mathcal T$ is empty. A model of $\mathcal T$ is the same as an interpretation in which every element is in $C_{\mathcal T}$.

## Upper bound by type elimination

Let $\mathrm{cl}$ be the smallest set that contains the NNF of $C$ and $C_{\mathcal T}$ and is closed under subconcepts and under $\dot\neg$. Since $\dot\neg$ maps the subconcepts of $D$ to the subconcepts of $\dot\neg D$, $|\mathrm{cl}| = O(n)$.

A *type* is a set $t \subseteq \mathrm{cl}$ such that

- $C_{\mathcal T} \in t$ and $\bot \notin t$, and $\top \in t$ when $\top \in \mathrm{cl}$;
- for every $D \in \mathrm{cl}$, exactly one of $D$ and $\dot\neg D$ is in $t$;
- $D \sqcap E \in t$ if and only if $D \in t$ and $E \in t$;
- $D \sqcup E \in t$ if and only if $D \in t$ or $E \in t$.

There are at most $2^{|\mathrm{cl}|}$ types. For a type $t$ and a role $r$, let $t/r = \{E : \forall r.E \in t\}$. Given a set $S$ of types, a type $t \in S$ is *bad in* $S$ if some $\exists r.D \in t$ has no $t' \in S$ with $\{D\} \cup t/r \subseteq t'$. The algorithm is

    S := the set of all types
    while some type is bad in S: remove all bad types from S
    accept if the NNF of C is in some type of S

Each round removes at least one type, so there are at most $2^{|\mathrm{cl}|}$ rounds. A round looks at each pair of types and each existential restriction, which is $2^{O(|\mathrm{cl}|)}$ steps. The total time is $2^{O(n)}$.

**Lemma 1 (soundness).** Let $S$ be the final set. Define $I$ with domain $S$, $A^I = \{t : A \in t\}$, and $(t, t') \in r^I$ if and only if $t/r \subseteq t'$. Then $t \in D^I$ if and only if $D \in t$, for every $t \in S$ and $D \in \mathrm{cl}$.

*Proof.* By induction on $D$. For $A$ it is the definition. For $\neg A$, $t \in (\neg A)^I$ if and only if $A \notin t$, if and only if $\neg A \in t$ by the second condition. The cases $\top$, $\bot$, $\sqcap$ and $\sqcup$ follow from the conditions on types.

$\exists r.D$: if $\exists r.D \in t$, then $t$ is not bad in $S$, so some $t' \in S$ has $D \in t'$ and $t/r \subseteq t'$. Then $(t, t') \in r^I$, and $t' \in D^I$ by induction. Conversely, let $(t, t') \in r^I$ with $t' \in D^I$, so $D \in t'$ by induction. If $\exists r.D \notin t$, then $\forall r.\dot\neg D \in t$, so $\dot\neg D \in t/r \subseteq t'$, which is impossible together with $D \in t'$.

$\forall r.E$: if $\forall r.E \in t$, every $r$-successor $t'$ of $t$ has $E \in t/r \subseteq t'$, so $t' \in E^I$ by induction. If $\forall r.E \notin t$, then $\exists r.\dot\neg E \in t$, and as above there is $t' \in S$ with $(t, t') \in r^I$ and $\dot\neg E \in t'$. Then $E \notin t'$, so $t' \notin E^I$ by induction, and $t \notin (\forall r.E)^I$. $\square$

Every type contains $C_{\mathcal T}$, so by Lemma 1 every element of $I$ is in $C_{\mathcal T}^I$ and $I$ is a model of $\mathcal T$. If the algorithm accepts, some $t \in S$ contains $C$ and $t \in C^I$.

**Lemma 2 (completeness).** Let $J$ be a model of $\mathcal T$. For each element $e$, the set $\mathrm{tp}(e) = \{D \in \mathrm{cl} : e \in D^J\}$ is a type, and it is never removed.

*Proof.* $\mathrm{tp}(e)$ satisfies the conditions on types by the semantics, and it contains $C_{\mathcal T}$ because $J$ is a model of $\mathcal T$. Suppose that before some round every $\mathrm{tp}(e)$ is in $S$. If $\exists r.D \in \mathrm{tp}(e)$, then $e$ has an $r$-successor $e'$ in $D^J$, and $e'$ is in $E^J$ for every $\forall r.E \in \mathrm{tp}(e)$. So $\{D\} \cup \mathrm{tp}(e)/r \subseteq \mathrm{tp}(e') \in S$, and $\mathrm{tp}(e)$ is not bad. By induction on the rounds no $\mathrm{tp}(e)$ is removed. $\square$

If $C$ is satisfiable with respect to $\mathcal T$ in a model $J$ with $d \in C^J$, then $\mathrm{tp}(d)$ stays in $S$ and contains $C$, so the algorithm accepts. Together with Lemma 1, the algorithm decides satisfiability with respect to $\mathcal T$ in time $2^{O(n)}$.

## Lower bound by alternating machines

By the theorem of Chandra, Kozen and Stockmeyer, alternating polynomial space equals EXPTIME. Fix a language $L \in$ EXPTIME and an alternating Turing machine $M$ that decides $L$ in space $p(n)$. We use these standard assumptions on $M$:

- its states are existential states, universal states, and the halting states $q_a$ (accept) and $q_r$ (reject);
- for each state $q$ that does not halt and each symbol $a$, the set $\delta(q, a)$ of moves $\mu = (q', b, d)$, with new state $q'$, written symbol $b$ and head step $d \in \{-1, +1\}$, is not empty;
- the head stays on the cells $0, \ldots, p(n) - 1$;
- every branch of every computation halts.

The last assumption costs nothing. A configuration that has an accepting computation tree has one in which no configuration repeats on a branch, so its depth is below the number $2^{O(p(n))}$ of configurations. A binary counter of $O(p(n))$ cells can stop each branch at that depth and reject.

For an input $w$ of length $n$, write $p = p(n)$. Use the concept names $S_q$ (the state is $q$), $H_i$ (the head is on cell $i$) and $T_{i,a}$ (cell $i$ holds $a$), and one role name $r_\mu$ for each move $\mu$. The TBox $\mathcal T_w$ contains, for all $q$, $a$, $i < p$ and moves $\mu$:

1. axioms that say that exactly one $S_q$, exactly one $H_i$, and for each $i$ exactly one $T_{i,a}$ hold at each element, such as $\top \sqsubseteq \bigsqcup_q S_q$ and $S_q \sqcap S_{q'} \sqsubseteq \bot$ for $q \ne q'$;
2. $S_{q_r} \sqsubseteq \bot$;
3. $S_q \sqcap H_i \sqcap T_{i,a} \sqsubseteq \bigsqcup_{\mu \in \delta(q,a)} \exists r_\mu.\top$ for existential $q$, and the same with $\bigsqcap$ for universal $q$;
4. $S_q \sqcap H_i \sqcap T_{i,a} \sqsubseteq \forall r_\mu.(S_{q'} \sqcap H_{i+d} \sqcap T_{i,b})$ for each $\mu = (q', b, d) \in \delta(q, a)$;
5. $H_j \sqcap T_{i,a} \sqsubseteq \forall r_\mu.T_{i,a}$ for $j \ne i$.

The concept $C_w$ is $S_{q_0} \sqcap H_0 \sqcap \bigsqcap_{i<p} T_{i,w_i}$, with the blank symbol for $i \ge n$. $M$ is fixed, so $\mathcal T_w$ has $O(p^2)$ axioms of size $O(p)$, and $\mathcal T_w$ and $C_w$ are built in polynomial time.

An element $e$ *encodes* the configuration with state $q$, head position $i$ and tape $c_0 \cdots c_{p-1}$ if $e \in S_q \sqcap H_i \sqcap \bigsqcap_j T_{j,c_j}$. In a model of $\mathcal T_w$ each element encodes exactly one configuration, by item 1. For a configuration $c$ and a move $\mu$ that applies to it, write $c_\mu$ for the configuration that $\mu$ produces.

**Lemma 3.** If $I$ is a model of $\mathcal T_w$ and $e$ encodes $c$, then $c$ is accepting.

*Proof.* All branches from $c$ halt and each configuration has finitely many successors, so by König's lemma the computation tree from $c$ has a finite height $h(c)$. We use induction on $h(c)$. If $h(c) = 0$, $c$ halts. Its state is not $q_r$ by item 2, so it is $q_a$, and $c$ accepts. Otherwise let $q$, $i$ and $a$ be the state, the head position and the symbol under the head. If $e$ has an $r_\mu$-successor $e'$ for some $\mu \in \delta(q, a)$, then $e'$ encodes $c_\mu$, by item 4 for the changed cell, state and head, and by item 5 for the other cells. If $q$ is existential, item 3 gives such a successor for some $\mu$; $c_\mu$ accepts by induction, so $c$ accepts. If $q$ is universal, item 3 gives one for each $\mu \in \delta(q, a)$; all $c_\mu$ accept, so $c$ accepts. $\square$

**Lemma 4.** If $M$ accepts $w$, then $C_w$ is satisfiable with respect to $\mathcal T_w$.

*Proof.* Let the domain of $I$ be the set of accepting configurations, interpret $S_q$, $H_i$ and $T_{i,a}$ by reading them off, and put $(c, c_\mu) \in r_\mu^I$ when $c$ does not halt, $\mu$ applies to $c$, and $c_\mu$ accepts. Item 1 holds by construction, and item 2 because no accepting configuration is in state $q_r$. An accepting existential configuration has an accepting successor, and all successors of an accepting universal configuration accept, so item 3 holds. Each $r_\mu$-edge goes from $c$ to $c_\mu$, so items 4 and 5 hold. The initial configuration accepts and is in $C_w^I$. $\square$

By Lemmas 3 and 4, $w \in L$ if and only if $C_w$ is satisfiable with respect to $\mathcal T_w$. So the problem is EXPTIME-hard.

## Subsumption and consistency

$C \sqsubseteq_{\mathcal T} D$ holds if and only if $C \sqcap \neg D$ is unsatisfiable with respect to $\mathcal T$, and $C$ is satisfiable with respect to $\mathcal T$ if and only if $C \not\sqsubseteq_{\mathcal T} \bot$. EXPTIME is closed under complement, so subsumption with respect to general TBoxes is EXPTIME-complete. $\mathcal T$ has a model if and only if $\top$ is satisfiable with respect to $\mathcal T$, which is in EXPTIME. Conversely, for a role name $u$ that does not occur in $\mathcal T$ or $C$, $C$ is satisfiable with respect to $\mathcal T$ if and only if $\mathcal T \cup \{\top \sqsubseteq \exists u.C\}$ has a model: from a model of $\mathcal T$ with an element $d \in C^I$, add the edge $(e, d)$ to $u$ for every element $e$. So consistency of a general TBox is EXPTIME-complete too. $\blacksquare$
