---
title: The smodels search returns exactly the stable models
proves: [correctness]
status: full
---

Let $P$ be a finite ground program over a set $A$ of $n$ atoms. It has normal rules $h \leftarrow B$, choice rules $\{h_1, \ldots, h_k\} \leftarrow B$ and constraints $\leftarrow B$, where a body $B$ is $b_1, \ldots, b_m, \mathit{not}\ c_1, \ldots, \mathit{not}\ c_j$. We write $\mathrm{pos}(B)$ and $\mathrm{neg}(B)$ for the positive and negative atoms of $B$. A set $M \subseteq A$ satisfies $B$ if $\mathrm{pos}(B) \subseteq M$ and $\mathrm{neg}(B) \cap M = \emptyset$.

## Stable models of programs with choice rules

The reduct $P^M$ deletes every rule whose body has $\mathit{not}\ c$ with $c \in M$, and every constraint. Each normal rule $h \leftarrow B$ that is left becomes $h \leftarrow \mathrm{pos}(B)$. Each choice rule $\{H\} \leftarrow B$ that is left becomes the rules $h \leftarrow \mathrm{pos}(B)$ for $h \in H \cap M$. The reduct is a definite program. $M$ is a *stable model* of $P$ if $M$ is the least model of $P^M$ and $M$ satisfies no constraint body. For a program with only normal rules this is the definition of Gelfond and Lifschitz (1988). For choice rules it is the definition of Simons, Niemelä and Soininen (2002) restricted to choice rules, in the reduct form used by Gebser, Kaminski, Kaufmann and Schaub (2012).

**Lemma 1 (properties of a stable model).** Let $M$ be a stable model of $P$.

1. If $M$ satisfies the body of a normal rule $h \leftarrow B$, then $h \in M$.
2. Each $a \in M$ is the head of a normal rule, or one of the heads of a choice rule, whose body $M$ satisfies.
3. $M$ satisfies no constraint body.

*Proof.* (1) The rule is kept in $P^M$ as $h \leftarrow \mathrm{pos}(B)$ with $\mathrm{pos}(B) \subseteq M$. $M$ is a model of $P^M$, so $h \in M$. (2) $a$ is in the least model of $P^M$, so some rule $a \leftarrow \mathrm{pos}(B)$ of $P^M$ has $\mathrm{pos}(B) \subseteq M$. That rule comes from a rule of $P$ with $a$ in its head and $\mathrm{neg}(B) \cap M = \emptyset$. (3) holds by the definition. $\square$

## The procedures

A partial assignment $a$ maps some atoms to true or false. $M$ *agrees with* $a$ if $a(x) = \mathrm{true}$ implies $x \in M$ and $a(x) = \mathrm{false}$ implies $x \notin M$. A body is true under $a$ if all its literals are true, false if one of its literals is false, and open otherwise. A rule is *live* for $a$ if its body is not false.

ATLEAST applies four rules until none of them changes $a$:

- (R1) if the body of a normal rule $h \leftarrow B$ is true, make $h$ true;
- (R2) if an atom has no live rule with that atom in the head, make it false;
- (R3) if an atom is true and has exactly one live rule with that atom in the head, make every literal of that body true;
- (R4) for a constraint, or a normal rule whose head is false: if the body is true, report a conflict; if exactly one literal of the body is open and the others are true, make that literal false.

ATMOST computes the *upper closure* $U(a)$: the least set that contains each head $h$ with $a(h) \neq \mathrm{false}$ of each normal or choice rule $r$ with $\mathrm{pos}(r) \subseteq U(a)$ and no $c \in \mathrm{neg}(r)$ true under $a$. It makes every atom outside $U(a)$ false. EXPAND repeats ATLEAST and ATMOST until neither changes $a$. Any step that would give an atom both values raises a conflict. LOOKAHEAD tries both values of each open atom; when EXPAND of one value gives a conflict, it fixes the other value and expands again. SEARCH calls EXPAND and LOOKAHEAD. On a conflict it returns nothing. On a total assignment it returns the set of true atoms. Otherwise it picks an open atom $x$ and calls itself with $x$ true and with $x$ false.

**Lemma 2 (each step keeps every stable model).** Let $M$ be a stable model of $P$ that agrees with $a$. Then $M$ agrees with the result of each rule (R1) to (R4), with the result of ATMOST, and with the result of LOOKAHEAD, and none of these steps reports a conflict.

*Proof.* (R1) The body is true under $a$, so $M$ satisfies it, and $h \in M$ by Lemma 1(1). (R2) Each rule with $x$ in its head has a body that is false under $a$, so $M$ does not satisfy it, and $x \notin M$ by Lemma 1(2). (R3) By Lemma 1(2), $M$ satisfies the body of a rule with $x$ in the head, and that rule must be live, so it is the one live rule. So $M$ satisfies its body. (R4) If $M$ satisfied the body, then $M$ would satisfy a constraint body, against Lemma 1(3), or $M$ would satisfy the body of a normal rule with $h \notin M$, against Lemma 1(1). So the body is not true under $a$, and when one literal is open and the others are true, $M$ makes that literal false.

ATMOST. We show $M \subseteq U(a)$. $M$ is the union of the stages $T \uparrow k$ of the immediate consequence operator of $P^M$. By induction on $k$: an atom $h$ of the stage $k + 1$ comes from a rule $r$ of $P$ with $\mathrm{pos}(r) \subseteq T \uparrow k \subseteq U(a)$ and $\mathrm{neg}(r) \cap M = \emptyset$. Since $M$ agrees with $a$, no $c \in \mathrm{neg}(r)$ is true under $a$. And $h \in M$, so $a(h) \neq \mathrm{false}$. So $h \in U(a)$. (For a choice rule the reduct has $h \leftarrow \mathrm{pos}(r)$ only for $h \in M$, and the same argument applies.) So each atom that ATMOST makes false is not in $M$.

EXPAND is a sequence of these steps. If one value of an open atom $x$ expands to a conflict, then no stable model that agrees with $a$ has that value for $x$, by what we just showed, so $M$ has the other value. Hence LOOKAHEAD keeps $M$ too. $\square$

**Lemma 3 (a total assignment that expands with no conflict is a stable model).** Let $a$ be total, with no conflict after EXPAND, and let $M$ be its set of true atoms. Then $M$ is a stable model of $P$.

*Proof.* Let $L$ be the least model of $P^M$. First, $M$ is a model of $P^M$. A normal rule of $P^M$ comes from $h \leftarrow B$ with $\mathrm{neg}(B) \cap M = \emptyset$. If $\mathrm{pos}(B) \subseteq M$, the body is true under $a$, and (R1) gives $h \in M$. A choice rule gives rules only for heads in $M$. So $L \subseteq M$. Second, ATMOST made every atom outside $U(a)$ false and found no conflict, so $M \subseteq U(a)$. Under a total assignment, $U(a)$ is built from the rules whose negative atoms are not in $M$, and it adds only heads in $M$. These are exactly the rules of $P^M$, so by induction on the construction $U(a) \subseteq L$. Together, $M = L$. Finally, (R4) reports a conflict for a constraint with a true body, so $M$ satisfies no constraint body. $\square$

**Theorem.** SEARCH called on the empty assignment returns each stable model of $P$ exactly once, and nothing else.

*Proof.* Each call either returns, or assigns one more atom in each of its two child calls. So the recursion depth is at most $n$ and the search ends. A returned set is a stable model by Lemma 3. Let $M$ be a stable model. By Lemma 2, along the path of calls that always takes the branch value that $M$ gives, no conflict occurs and $M$ agrees with every assignment. The path ends at a total assignment, which is $M$. Two different leaves differ on the atom of their last common branch point, so each stable model is returned once. $\square$

## Running time

Let $s$ be the size of $P$, the number of rules plus the number of literals in them. With counters per rule and a queue, as in the counter method of Dowling and Gallier (1984), ATLEAST and ATMOST each take $O(s)$ time per call. Each round of EXPAND other than the last assigns at least one atom, so EXPAND takes $O(n \cdot s)$ time. LOOKAHEAD runs at most $2n$ expansions for each atom that it fixes, and it fixes at most $n$ atoms, so it takes $O(n^3 \cdot s)$ time. The search tree has at most $2^n$ leaves. The worst-case time is $O(2^n \cdot n^3 \cdot s)$. The Python code recomputes each fixpoint with repeated scans, which adds a factor $n$ to each bound. An exponential worst case is expected: deciding whether a normal program has a stable model is NP-complete.

## What the tests check

The tests compare the output of `stable_models` with a brute force search over all subsets of the atoms that tests the reduct definition above directly. They do this on 300 random normal programs with at most 6 atoms, with and without LOOKAHEAD, and on 250 random programs with choice rules and constraints. They also check that the normal translation of choice rules, $h \leftarrow B, \mathit{not}\ h'$ and $h' \leftarrow \mathit{not}\ h$, gives the same models after the projection to the original atoms, with one translated model for each direct model. Small cases check that ATMOST makes the atoms of a positive loop false with no search, and that a constraint with a true body is a conflict.
