---
title: A saturated result of unfailing completion decides the ground word problem
proves: [correctness]
status: full
---

We use the definitions and the pseudocode of the page. $>$ is the lexicographic path ordering for a total precedence on $\Sigma$; it is well-founded, closed under contexts and substitutions, has the subterm property, and is total on ground terms. All equations of $E$ are regular. "Ground" means ground over $\Sigma$, and $s =_E t$ means that $s \approx t$ is an equational consequence of $E$, which by Birkhoff's theorem holds iff $s \leftrightarrow_E^* t$ by replacement of equals.

**Lemma 1 (regularity is kept).** Every equation that the run queues or adds to $A$ is regular.

*Proof.* Equations of $E$ are regular by assumption. If $u \approx v$ is regular and $s \leftrightarrow t$ by one replacement with an instance $u\sigma \approx v\sigma$, then $s$ and $t$ have the same variables, because $u\sigma$ and $v\sigma$ have the same variables. A simplified equation at line L6 and a critical pair $u_1\sigma[v_2\sigma]_p \approx v_1\sigma$ are obtained from a regular equation, or from the regular pair $u_1\sigma \approx v_1\sigma$, by such replacements. Equations re-queued at lines L4 and L9 were regular already. $\square$

**Lemma 2 (invariant).** At line L2, the equational consequences of $A \cup Q$, where $Q$ is the set of queued equations, are those of $E$, and every equation of $A \cup Q$ is a consequence of $E$.

*Proof.* Initially $A = \emptyset$ and $Q = E$. Line L4 queues critical pairs of $A$, and line L11 queues critical pairs of $A$ and the new equation; a critical pair is the result of two replacements on $u_1\sigma$, so it is a consequence of $A$. Line L5 removes $s \approx t$ from $Q$; line L6 replaces it by $s' \approx t'$ with $s \leftrightarrow_A^* s'$ and $t \leftrightarrow_A^* t'$, so $s \approx t$ is a consequence of $A \cup \{s' \approx t'\}$ and $s' \approx t'$ one of $A \cup \{s \approx t\}$. Line L7 drops it only if $s' = t'$ or it is a variant of an equation of $A$, so it is still a consequence of $A$. Line L9 moves equations from $A$ to $Q$ and line L10 adds $s' \approx t'$ to $A$. No step changes the set of consequences, and every new equation is a consequence of the old set. $\square$

So when line L4 returns $A$, the queue is empty and $A$ and $E$ have the same consequences.

**Lemma 3 (ordered rewriting).** For any set $A$ of equations, $\to_A$ terminates, and if $c \to_A d$ then $c\rho \to_A d\rho$ for every substitution $\rho$.

*Proof.* Each step replaces $u\sigma$ by $v\sigma$ with $u\sigma > v\sigma$ inside a context, so $c > d$; $>$ is well-founded. For the second part, $u\sigma > v\sigma$ implies $u\sigma\rho > v\sigma\rho$, and $c\rho|_p = u(\sigma\rho)$. $\square$

In particular the normalizations at lines L3 and L6 stop. For the rest, let $A$ be the set returned at line L4. By line L3, every ordered critical pair $c \approx d$ of $A$ has $c{\downarrow}_A = d{\downarrow}_A$, so $c \to_A^* w \leftarrow_A^* d$ for some $w$.

**Lemma 4 (local confluence on ground terms).** If $s$ is ground and $t_1 \leftarrow_A s \to_A t_2$, then $t_1 \to_A^* w \leftarrow_A^* t_2$ for some $w$.

*Proof.* Let the steps use $u_1 \to v_1$ with $\sigma_1$ at $p_1$ and $u_2 \to v_2$ with $\sigma_2$ at $p_2$, where each $u_i \to v_i$ is a direction of an equation of $A$ and $u_i\sigma_i > v_i\sigma_i$. Every term reachable from $s$ is ground, by Lemma 1. We may assume that $p_1$ is a prefix of $p_2$ or that the two are disjoint.

*Disjoint positions.* Apply the other step to each of $t_1$ and $t_2$; both give the same term.

*Critical overlap.* $p_2 = p_1 q$ and $q$ is a non-variable position of $u_1$. Rename the variables of the second equation apart; then $u_1|_q\sigma_1 = u_2\sigma_2$, so $u_1|_q$ and $u_2$ have a most general unifier $\tau$ with $\sigma_1 \cup \sigma_2 = \tau\rho$ on these variables. If $v_1\tau > u_1\tau$ held, closure under substitution would give $v_1\sigma_1 > u_1\sigma_1$, contradicting the step; the same holds for the second equation. So $c \approx d$ with $c = u_1\tau[v_2\tau]_q$ and $d = v_1\tau$ is an ordered critical pair of $A$, and $c \to_A^* w \leftarrow_A^* d$. Since $t_2 = s[c\rho]_{p_1}$ and $t_1 = s[d\rho]_{p_1}$, Lemma 3 and closure under contexts join $t_1$ and $t_2$ at $s[w\rho]_{p_1}$.

*Variable overlap.* $p_2 = p_1 q q'$ where $u_1|_q$ is a variable $x$. Let $x\sigma_1 \to_A r$ be the inner step at $q'$, and let $\sigma_1'$ agree with $\sigma_1$ except $x\sigma_1' = r$. From $t_2$, rewrite each other occurrence of $x\sigma_1$ in the copy of $u_1\sigma_1$ by the same inner step; this reaches $s[u_1\sigma_1']_{p_1}$. From $t_1 = s[v_1\sigma_1]_{p_1}$, rewrite every occurrence of $x\sigma_1$ in $v_1\sigma_1$; this reaches $s[v_1\sigma_1']_{p_1}$. The terms $u_1\sigma_1'$ and $v_1\sigma_1'$ are ground. If they are equal, we are done. If $u_1\sigma_1' > v_1\sigma_1'$, one step with $u_1 \to v_1$ joins them. Otherwise $v_1\sigma_1' > u_1\sigma_1'$ by totality. Then $v_1$ is not a variable: $u_1$ is not a variable, and by regularity it contains $v_1$ properly if $v_1$ is a variable, so the subterm property would give $u_1\sigma_1' > v_1\sigma_1'$. So $v_1 \to u_1$ is a usable direction, by regularity, and one step with it joins the two terms. $\square$

**Theorem.** If the run returns $A$ at line L4, then for all ground terms $s$ and $t$, $s =_E t$ iff $s{\downarrow}_A = t{\downarrow}_A$.

*Proof.* If $s{\downarrow}_A = t{\downarrow}_A$, then $s =_A t$ by the steps, so $s =_E t$ by Lemma 2. Conversely let $s =_E t$. By Lemma 2 and Birkhoff's theorem, $s = w_0 \leftrightarrow w_1 \leftrightarrow \cdots \leftrightarrow w_n = t$ where each step replaces an instance $u\sigma$ of one side of an equation of $A$ by $v\sigma$; by Lemma 1 the $w_i$ are ground, so $u\sigma$ and $v\sigma$ are ground. By totality, each step with $w_i \neq w_{i+1}$ is an ordered rewrite step from $w_i$ to $w_{i+1}$ or back, using the direction whose instance decreases. On ground terms, $\to_A$ terminates by Lemma 3 and is locally confluent by Lemma 4, so it is confluent by Newman's lemma, and confluence turns the chain into $s{\downarrow}_A = t{\downarrow}_A$, where the normal forms are unique. $\blacksquare$

**Termination of the procedure.** Each pass through lines L5 to L11 increases the step count. A pass through line L3 that does not return queues at least one pair, so the next pass is through line L5. So the loop ends after at most $B$ steps and $B + 1$ checks at line L3, at line L4 or at line L12. $\blacksquare$
