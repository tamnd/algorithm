---
title: The alternating fixpoint computes the well-founded model
proves: [correctness]
status: full
---

Let $P$ be a finite ground normal program and $A$ the set of its atoms. For $J \subseteq A$, the reduct $P^J$ deletes each rule with a negative body atom in $J$ and deletes the negative literals of the other rules. It is a definite program, and $S(J)$ is its least model. We write $\mathrm{pos}(r)$ and $\mathrm{neg}(r)$ for the positive and negative body atoms of a rule $r$. The least model of a definite program $D$ is the union of the stages $T_D \uparrow 0 = \emptyset$, $T_D \uparrow (k+1) = T_D(T_D \uparrow k)$, so we can argue by induction on the stage at which an atom is derived.

## Definitions (Van Gelder, Ross and Schlipf 1991)

A *partial interpretation* is a pair $I = (T, F)$ of subsets of $A$. A positive literal $b$ is true in $I$ if $b \in T$ and false if $b \in F$; a literal $\mathit{not}\ c$ is true if $c \in F$ and false if $c \in T$. Pairs are ordered componentwise: $(T, F) \le (T', F')$ if $T \subseteq T'$ and $F \subseteq F'$.

A set $X \subseteq A$ is *unfounded* with respect to $I$ if, for each $a \in X$ and each rule $r$ with head $a$, (i) some body literal of $r$ is false in $I$, or (ii) $\mathrm{pos}(r) \cap X \neq \emptyset$. A union of unfounded sets is unfounded, so there is a greatest unfounded set $\mathrm{GUS}(I)$. Let $T_P(I)$ be the set of heads of the rules whose body literals are all true in $I$, and $W_P(I) = (T_P(I), \mathrm{GUS}(I))$. If $I \le I'$, each literal false in $I$ is false in $I'$, so each set unfounded with respect to $I$ is unfounded with respect to $I'$; and each body true in $I$ is true in $I'$. So $W_P$ is monotone. The *well-founded model* is the limit $(T^*, F^*)$ of $I_0 = (\emptyset, \emptyset)$, $I_{k+1} = W_P(I_k)$. Since $W_P$ is monotone, the $I_k$ increase, and since $A$ is finite, the limit is reached after finitely many steps and is a fixpoint of $W_P$.

## The iteration

The algorithm computes $K_0 = \emptyset$, $U_i = S(K_i)$, $K_{i+1} = S(U_i)$, and stops at the first $i$ with $K_{i+1} = K_i$. It returns $(K, A \setminus U)$ with $K = K_i$ and $U = U_i$.

**Lemma 1 (antimonotone).** If $J \subseteq J'$, then $S(J') \subseteq S(J)$.

*Proof.* Each rule that $P^{J'}$ keeps has no negative body atom in $J'$, so none in $J$, and $P^J$ keeps it too. So $P^{J'} \subseteq P^J$, and the least model of the smaller definite program is smaller. $\square$

**Lemma 2 (shape of the sequence).** For each $i$: $K_i \subseteq K_{i+1}$, $U_{i+1} \subseteq U_i$, and $K_i \subseteq U_i$.

*Proof.* $K_0 = \emptyset \subseteq K_1$. If $K_i \subseteq K_{i+1}$, then by Lemma 1 $U_{i+1} = S(K_{i+1}) \subseteq S(K_i) = U_i$, and then $K_{i+2} = S(U_{i+1}) \supseteq S(U_i) = K_{i+1}$. For the third claim, $K_0 = \emptyset \subseteq U_0$. If $K_i \subseteq U_i$, then $K_{i+1} = S(U_i) \subseteq S(K_i) = U_i$, and so $U_{i+1} = S(K_{i+1}) \supseteq S(U_i) = K_{i+1}$. $\square$

**Termination.** If $K_{i+1} = K_i$, then $U_{i+1} = U_i$ and the sequence is constant from $i$ on. Before that point, $K$ grows strictly at each round, so this happens for some $i \le |A|$. At the end, $S(K) = U$ and $S(U) = K$, and $K \subseteq U$ by Lemma 2.

## Theorem (Van Gelder 1993)

The algorithm returns the well-founded model: $T^* = K$ and $F^* = A \setminus U$.

**Step 1: $(T^*, F^*) \le (K, A \setminus U)$.** We show that $W_P(K, A \setminus U) \le (K, A \setminus U)$. Then, by induction on $k$, $I_k \le (K, A \setminus U)$: it holds for $I_0$, and $I_{k+1} = W_P(I_k) \le W_P(K, A \setminus U) \le (K, A \setminus U)$ by monotonicity.

First, $T_P(K, A \setminus U) \subseteq K$. Take a rule $r$ whose body is true in $(K, A \setminus U)$: $\mathrm{pos}(r) \subseteq K$ and $\mathrm{neg}(r) \cap U = \emptyset$. Then $P^U$ keeps $r$ as $h \leftarrow \mathrm{pos}(r)$. Its body is in $K = S(U)$, which is a model of $P^U$, so the head $h$ is in $K$.

Second, $\mathrm{GUS}(K, A \setminus U) \subseteq A \setminus U$. Let $X$ be unfounded with respect to $(K, A \setminus U)$. We show by induction on $k$ that $X$ is disjoint from the stage $T_{P^K} \uparrow k$; the union of these stages is $S(K) = U$. The stage $0$ is empty. Suppose that $a \in X$ enters at stage $k + 1$ through a rule $r$ with $\mathrm{neg}(r) \cap K = \emptyset$ and $\mathrm{pos}(r) \subseteq T_{P^K} \uparrow k$. Since $X$ is unfounded, $r$ satisfies (i) or (ii). For (i), a positive body atom would be in $A \setminus U$, but $\mathrm{pos}(r) \subseteq T_{P^K} \uparrow k \subseteq U$; or a negative body atom would be in $K$, but $\mathrm{neg}(r) \cap K = \emptyset$. For (ii), a positive body atom would be in $X$, but by induction $T_{P^K} \uparrow k$ is disjoint from $X$. Each case is a contradiction.

**Step 2: $(K, A \setminus U) \le (T^*, F^*)$.** We use two facts about the fixpoint $(T^*, F^*)$ of $W_P$.

(a) $A \setminus S(T^*)$ is unfounded with respect to $(T^*, F^*)$, so $A \setminus S(T^*) \subseteq F^*$. Take $a \notin S(T^*)$ and a rule $r$ with head $a$. If $\mathrm{neg}(r) \cap T^* \neq \emptyset$, a negative literal of $r$ is false: case (i). Otherwise $P^{T^*}$ keeps $r$. Since $S(T^*)$ is a model of $P^{T^*}$ and does not contain $a$, some $b \in \mathrm{pos}(r)$ is not in $S(T^*)$: case (ii).

(b) $S(A \setminus F^*) \subseteq T^*$. By induction on the stage: an atom $h$ of the stage $k + 1$ comes from a rule $r$ with $\mathrm{neg}(r) \cap (A \setminus F^*) = \emptyset$, that is $\mathrm{neg}(r) \subseteq F^*$, and with $\mathrm{pos}(r)$ in the stage $k$, so in $T^*$ by induction. The body of $r$ is true in $(T^*, F^*)$, so $h \in T_P(T^*, F^*) = T^*$.

Now we show by induction on $i$ that $K_i \subseteq T^*$ and $A \setminus U_i \subseteq F^*$. $K_0 = \emptyset \subseteq T^*$. If $K_i \subseteq T^*$, then $U_i = S(K_i) \supseteq S(T^*)$ by Lemma 1, so $A \setminus U_i \subseteq A \setminus S(T^*) \subseteq F^*$ by (a). Then $U_i \supseteq A \setminus F^*$, so $K_{i+1} = S(U_i) \subseteq S(A \setminus F^*) \subseteq T^*$ by Lemma 1 and (b).

Steps 1 and 2 give $(T^*, F^*) = (K, A \setminus U)$. $\square$

## Consequences

**Every stable model lies between $K$ and $U$.** If $M$ is stable, then $S(M) = M$. By induction $K_i \subseteq M$: if $K_i \subseteq M$, then $U_i = S(K_i) \supseteq S(M) = M$, so $K_{i+1} = S(U_i) \subseteq S(M) = M$. And $M = S(M) \subseteq S(K) = U$. So every atom true in the well-founded model is in $M$, and every atom false in it is not in $M$.

**A total well-founded model is the unique stable model.** If $K = U$, then $S(K) = U = K$, so $K$ is stable, and every stable model $M$ satisfies $K \subseteq M \subseteq U = K$.

## Running time

Let $n = |A|$ and let $s$ be the size of $P$, the number of rules plus the number of body literals. The implementation computes $S(J)$ in $O(s)$ time with the counter method of Dowling and Gallier (1984): each rule kept by the reduct has a counter of the positive body atoms not yet derived, and each derived atom decrements the counters of the rules in which it occurs. Each atom enters the queue at most once, and each occurrence of an atom in a rule body is visited at most once. By the termination argument there are at most $n + 1$ rounds, each with two calls of $S$ and one comparison of sets of size at most $n$. The total time is $O(n \cdot s)$.

## What the tests check

The tests compute the well-founded model a second time from the definition: they iterate $W_P$ from $(\emptyset, \emptyset)$, with the greatest unfounded set found by trying every subset of the atoms. The two results agree on 300 random programs with at most 7 atoms. The tests also check the counter method against the plain least model of `lp.py`, the monotone shape of the trace from Lemma 2, the bound on the number of rounds, the consequences above against brute force enumeration of the stable models, the totality of the well-founded model on random stratified programs, and the trace of the example on the page.
