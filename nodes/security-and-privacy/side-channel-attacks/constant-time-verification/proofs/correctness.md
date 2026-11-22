---
title: The product check accepts a program exactly when the program is constant time
proves: [correctness]
status: full
---

**The setting.** This is the toy language of the page. Values are the integers mod $w$, every array has $w$ cells, a division by 0 gives 0, and a loop repeats its body $n < w$ times. So every expression has a value in every state, and every run of a program stops (by induction on the program text, with an inner induction on the loop count). A state $\sigma$ maps variables and arrays to values. A run of a block $B$ from $\sigma$ gives a final state $\sigma \cdot B$ and a trace $\tau(B, \sigma)$ of events. No name in $P$ ends with a prime, so the shadow names $x'$ are fresh. For two states $\sigma$ and $\hat\sigma$, the *joined state* $\sigma \oplus \hat\sigma'$ maps $x$ to $\sigma(x)$ and $x'$ to $\hat\sigma(x)$.

**Definition.** $P$ is constant time when $\tau(P, \sigma) = \tau(P, \hat\sigma)$ for all start states $\sigma$ and $\hat\sigma$ that agree on the public inputs and on the tables, and that give the value 0 to every other variable.

**Lemma 1 (renaming).** For each expression $e$ and states $\sigma, \hat\sigma$, the value of $e'$ in $\sigma \oplus \hat\sigma'$ is the value of $e$ in $\hat\sigma$, and the value of $e$ in $\sigma \oplus \hat\sigma'$ is the value of $e$ in $\sigma$. A statement of $P$ writes only names without a prime, and its shadow copy writes only names with a prime.

*Proof.* By induction on $e$. The shadow copy replaces each variable $x$ by $x'$ and each array $a$ by $a'$ and keeps the operators, and the joined state gives $x'$ the value $\hat\sigma(x)$. The second claim holds because $e$ reads no primed name. The claim on writes is clear from the form of the copy. $\square$

**Lemma 2 (the events of an expression).** The evaluation of $e$ emits one event for each load node and one for each division node of $e$, in a fixed order that depends on the text of $e$ only. The event of a load $a[i]$ is $(\mathrm{addr}, a, v)$, where $v$ is the value of the term $i$. The event of a division $e_1 \operatorname{div} e_2$ is $(\mathrm{div}, v_1, v_2)$, with the values of the terms $e_1$ and $e_2$. These terms are exactly the leak terms of $e$ that line L13 collects. So the events of $e$ in $\sigma$ and in $\hat\sigma$ are equal if and only if each leak term has the same value in $\sigma$ and in $\hat\sigma$.

*Proof.* By induction on $e$, from the definition of the evaluation. The two event lists have the same length and the same array names at each position, so they are equal exactly when the values at each position are equal. $\square$

**Corollary 3 (the guard).** $G(e)$ evaluates to 1 in $\sigma \oplus \hat\sigma'$ if and only if the events of $e$ in $\sigma$ equal the events of $e$ in $\hat\sigma$.

*Proof.* $G(e)$ is the conjunction of $l = l'$ over the leak terms $l$. By Lemma 1 the two sides have the values of $l$ in $\sigma$ and in $\hat\sigma$. Apply Lemma 2. $\square$

**The head of a statement.** Call the events that a statement $S$ emits before it runs a sub-block the *head* $h(S, \sigma)$. For $x \leftarrow e$ it is the events of $e$. For $a[i] \leftarrow e$ it is the events of $i$, then of $e$, then $(\mathrm{addr}, a, v_i)$. For a branch on $c$ it is the events of $c$, then $(\mathrm{br}, c \ne 0)$. For a loop on $e$ it is the events of $e$, then $(\mathrm{loop}, v_e)$. By Lemma 2 the length of the head depends on the text of $S$ only, and by Corollary 3 and the form of lines L7 to L11, the assert that PRODUCT puts before $S$ holds in $\sigma \oplus \hat\sigma'$ if and only if $h(S, \sigma) = h(S, \hat\sigma)$. For the branch, the extra conjunct $(c \ne 0) = (c' \ne 0)$ compares the branch events. For the store and the loop, the conjuncts $i = i'$ and $e = e'$ compare the address and the count.

**Lemma 4 (lockstep).** For each block $B$ and states $\sigma, \hat\sigma$, the run of PRODUCT$(B)$ from $\sigma \oplus \hat\sigma'$ does one of two things.

1. It ends with no failed assert. Then $\tau(B, \sigma) = \tau(B, \hat\sigma)$, and the final state is $(\sigma \cdot B) \oplus (\hat\sigma \cdot B)'$.
2. It stops at a failed assert. Then $\tau(B, \sigma) \ne \tau(B, \hat\sigma)$.

*Proof.* By induction on the text of $B$ and, inside a loop, on the number of iterations. The empty block gives case 1 with two empty traces.

Let $B = S; R$. The product is the assert $A_S$, then the product of $S$ without that assert, then PRODUCT$(R)$ (line L12). Write $\tau(B, \sigma) = h(S, \sigma)\, u\, \tau(R, \sigma \cdot S)$, where $u$ is the trace of the sub-blocks that $S$ runs, and do the same for $\hat\sigma$.

If $A_S$ fails, then $h(S, \sigma) \ne h(S, \hat\sigma)$ by the head property. The two heads have the same length, so the two traces differ at a position inside the heads, and case 2 holds.

If $A_S$ holds, the heads are equal. Look at the form of $S$.

- $x \leftarrow e$ or $a[i] \leftarrow e$. The product runs $S$ and then its shadow copy. By Lemma 1 the first writes $\sigma$'s value into the name without a prime and the second writes $\hat\sigma$'s value into the primed name. So the state becomes $(\sigma \cdot S) \oplus (\hat\sigma \cdot S)'$, and $u$ is empty on both sides.
- A branch on $c$. The assert gives $c \ne 0$ in $\sigma$ exactly when $c \ne 0$ in $\hat\sigma$, so the product takes the same arm $B_j$ that both runs take. Apply the induction hypothesis to PRODUCT$(B_j)$, a shorter text.
- A loop on $e$. The assert gives the same count $n$ in both runs, and the product repeats PRODUCT$(B_1)$ $n$ times. Apply the induction hypothesis to each iteration in turn. If an iteration fails, the traces of that iteration differ, after equal traces of the earlier iterations; since a failure in case 2 comes with traces that differ at some position, and the earlier parts have equal length, the full traces differ.

In each form, either a failure inside $S$ gives traces that differ after an equal prefix, which is case 2, or $S$ ends in the joined state of the two runs with equal traces. Then apply the induction hypothesis to $R$ from that joined state. A failure in $R$ comes after equal prefixes $h\,u$ of the same length, so the full traces differ. Success in $R$ gives equal full traces and the joined final state. $\square$

**Theorem.** CT-VERIF$(P)$ returns true if and only if $P$ is constant time over the domain $\{0, \ldots, w-1\}$. When it returns false, the pair $(\sigma, \hat\sigma)$ that it returns agrees on the public inputs and gives two different traces.

*Proof.* Line L2 lists every pair of start states that agree on the public inputs and on the tables, with 0 for every other variable. This is the assumption step of the product. Line L3 runs PRODUCT$(P)$ from the joined state of the pair. By Lemma 4, an assert fails on a pair if and only if the two traces of $P$ on that pair differ. So line L5 returns a pair only when it is a true witness, and line L6 is reached only when no pair gives two traces, which is the definition of constant time. Each run stops, so the check stops. $\square$

**Corollary (the abstract cache).** If $P$ is constant time, then for each cache geometry, the cost of CACHE-COST is the same for all start states with the same public inputs.

*Proof.* The cache starts empty, and its cost is a function of the sequence of addresses $\mathrm{base}(a) + i$ over the address events of the trace. Equal traces give equal sequences, and so equal costs. The converse is false: two different traces can have the same cache cost, for example when two secret indices fall in the same line. So the cost in one cache model is a weaker observation than the trace, and the constant-time policy is the stronger guarantee. $\blacksquare$
