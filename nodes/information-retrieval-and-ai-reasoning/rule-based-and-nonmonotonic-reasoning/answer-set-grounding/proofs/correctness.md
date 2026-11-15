---
title: The grounder keeps the stable models of the full instantiation
proves: [correctness]
status: full
---

Let $P$ be a finite normal program with variables and constants but no function symbols. A rule is $h \leftarrow b_1, \ldots, b_m, \mathit{not}\ c_1, \ldots, \mathit{not}\ c_k$, where the $b_i$ form $\mathrm{pos}(r)$ and the $c_i$ form $\mathrm{neg}(r)$. The rule is *safe* if each variable of $h$ and of the $c_i$ occurs in some $b_i$. Let $C$ be the set of constants of $P$ (the Herbrand universe). An *instance* of $r$ is the ground rule $r\theta$ for a substitution $\theta$ of its variables by constants of $C$. The *full instantiation* $G$ is the set of all instances of all rules. Its stable models are by definition the stable models of $P$ (Gelfond and Lifschitz 1988).

For a ground program $Q$, $Q^+$ is the definite program of the rules $h \leftarrow \mathrm{pos}(r)$, $Q^M$ is the Gelfond-Lifschitz reduct and $\mathrm{lm}$ is the least model.

## Step 1: semi-naive evaluation computes the domain and its instances

Let $D = \mathrm{lm}(G^+)$, the *domain*, and let $I$ be the set of instances $r\theta \in G$ with $\mathrm{pos}(r\theta) \subseteq D$.

The code emits each rule with an empty positive body (by safety it is ground), sets $\Delta_0$ to the heads of these rules and $O_0 = \emptyset$. In round $t \geq 1$, for each rule $r$ with positive body $b_1, \ldots, b_m$ and each position $j$, it finds the substitutions $\theta$ with $b_i\theta \in O_{t-1}$ for $i < j$, $b_j\theta \in \Delta_{t-1}$, and $b_i\theta \in O_{t-1} \cup \Delta_{t-1}$ for $i > j$. It emits $r\theta$. Then $O_t = O_{t-1} \cup \Delta_{t-1}$, and $\Delta_t$ is the set of new heads minus $O_t$. It stops when $\Delta_t = \emptyset$ and returns $O_t$.

**Lemma 1.** The sets $\Delta_0, \Delta_1, \ldots$ are pairwise disjoint, and their union is $D$. The emitted instances are exactly $I$, and each pair (rule, substitution) with $r\theta \in I$ is emitted exactly once.

*Proof.* For an atom $a$ in some $\Delta_t$, call $t$ its *entry round* $e(a)$. Each $\Delta_t$ is disjoint from $O_t$, which contains all earlier $\Delta$'s, so each atom has at most one entry round. Every emitted head is a head of a rule of $G^+$ whose body is in $D$ (by induction on $t$), so the union is a subset of $D$, and since $D$ is finite the loop stops. Conversely, let $r\theta$ be an instance whose positive body atoms all have entry rounds, and let $q$ be the largest of them and $j$ the first position with $e(b_j\theta) = q$. In round $q + 1$, $b_j\theta \in \Delta_q$, the atoms before $j$ have entry rounds below $q$ and are in $O_q$, and the atoms after $j$ are in $O_q \cup \Delta_q$. So $r\theta$ is emitted in round $q + 1$ at position $j$. It is emitted at no other round $t + 1$ and position $j'$: that would need $e(b_{j'}\theta) = t$ and all other entry rounds at most $t$, so $t = q$, and all entry rounds before $j'$ below $q$, so $j' = j$. The rules with an empty positive body are emitted once, before the loop, and never in it, because the loop runs over the positions of the positive body. The head of each emitted instance enters some $\Delta$ unless it is already in $O$. So the set of atoms with an entry round is closed under $G^+$, and it contains the least model $D$. With the first part, it is equal to $D$, and the emitted instances are exactly those with positive body in $D$, that is $I$. Because the rule is safe, all its variables occur in $\mathrm{pos}(r)$, so $\theta$ is determined by $\mathrm{pos}(r\theta)$ and two different substitutions give two different instances. $\square$

## Step 2: instances outside the domain do not matter

**Lemma 2.** $G$ and $I$ have the same stable models.

*Proof.* Let $M$ be any set of atoms. Each rule of $G^M$ is a rule of $G^+$, so $\mathrm{lm}(G^M) \subseteq D$. A rule of $G^M$ that comes from an instance outside $I$ has a positive body atom outside $D$, so it never fires in the computation of $\mathrm{lm}(G^M)$. Hence $\mathrm{lm}(G^M) = \mathrm{lm}(I^M)$, since $I^M \subseteq G^M$ contains every rule that fires. So $M = \mathrm{lm}(G^M)$ if and only if $M = \mathrm{lm}(I^M)$. $\square$

## Step 3: simplification

Let $F$ be the least model of the instances in $I$ with no negative literal. The simplified program $S$ is built from $I$ as follows: delete each instance with some $\mathit{not}\ c$, $c \in F$; in the others, delete each literal $\mathit{not}\ c$ with $c \notin D$ and each positive body atom in $F$; remove duplicate rules.

**Lemma 3.** Every stable model $M$ of $I$, and every stable model $M$ of $S$, satisfies $F \subseteq M \subseteq D$.

*Proof.* For $I$: the rules with no negative literal are unchanged in $I^M$, so $F \subseteq \mathrm{lm}(I^M) = M$, and $M = \mathrm{lm}(I^M) \subseteq \mathrm{lm}(I^+) \subseteq D$. For $S$: each head of $S$ is a head of $I$ and lies in $D$. The rules of $I$ with no negative literal stay in $S$ with the atoms of $F$ removed from their bodies. Each atom of $F$ is derived from such rules whose bodies lie in $F$, so in $S$ these rules are facts, and $F \subseteq \mathrm{lm}(S^M) = M$. $\square$

**Lemma 4.** $I$ and $S$ have the same stable models.

*Proof.* By Lemma 3 it is enough to compare the reducts for an $M$ with $F \subseteq M \subseteq D$. Take an instance $r$ of $I$. If $\mathrm{neg}(r)$ meets $F$, it meets $M$, so $I^M$ deletes $r$, and $S$ does not contain it. Otherwise $S$ contains $r' = (h, \mathrm{pos}(r) \setminus F, \mathrm{neg}(r) \cap D)$. Since $M \subseteq D$, $\mathrm{neg}(r) \cap M = \emptyset$ exactly when $(\mathrm{neg}(r) \cap D) \cap M = \emptyset$. So $I^M$ keeps $h \leftarrow \mathrm{pos}(r)$ exactly when $S^M$ keeps $h \leftarrow \mathrm{pos}(r) \setminus F$. For a set $X \supseteq F$, the two bodies are true in $X$ together, so the two definite programs have the same immediate consequences on sets that contain $F$. Both least models contain $F$ (Lemma 3), and each least model is the least fixpoint, so each one is a fixpoint of the other operator. Hence the two least models are equal. Duplicates do not change a reduct or a least model. $\square$

**Theorem.** If every rule of $P$ is safe, then `ground(P)` has the same stable models as the full instantiation of $P$ over its constants.

*Proof.* By Lemma 1 the code computes $D$ and $I$, and `simplify` computes $S$. Lemmas 2 and 4 give the claim. $\square$

## Size and time

A rule with $k$ variables has $|C|^k$ instances. The family $p(X_1, \ldots, X_k) \leftarrow d(X_1), \ldots, d(X_k)$ with the facts $d(a)$ and $d(b)$ has $D$ with $2^k + 2$ atoms, and every instance is in $I$ and in $S$ as a fact. So the ground program has $2^k + 2$ rules for a non-ground program of size $O(k)$, and no grounder that writes out the ground program can be faster than $\Omega(2^k)$ on this family.

Let $r$ be the number of rules, $m$ the largest number of positive body atoms of a rule, $c = |C|$, $k$ the largest number of variables in a rule, and $d = |D|$. There are at most $r \cdot c^k$ instances. In one round, for each rule and each position $j$, the join visits at most $m \cdot c^k$ partial substitutions, and each visit scans the at most $d$ atoms of one predicate. There are at most $d + 1$ rounds. So the code takes $O(r \cdot m^2 \cdot c^k \cdot d^2)$ time. Real grounders index the atoms on their bound arguments and order the body so that the join is cheaper, but the bound $\Omega(c^k)$ for the output remains.

## What the tests check

The tests generate 300 random safe programs over the constants $a$ and $b$, with the predicates $p/1$, $q/1$, $r/2$ and $s/0$, so at most 9 ground atoms. They check that the domain and the instances from semi-naive evaluation equal those computed from the least model of the positive part of the full instantiation, and that the count of emitted instances equals the number of (rule, substitution) pairs with positive body in the domain. On 200 more programs they check that the output of `ground` has the same stable models as the full instantiation, by brute force with the reduct. They also check that an unsafe rule raises an error, and that the exponential family above gives $2^k + 2$ rules for $k = 1, \ldots, 8$.
