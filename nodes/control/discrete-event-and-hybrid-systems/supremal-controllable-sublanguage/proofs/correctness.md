---
title: The fixed point on the product automaton gives the supremal controllable sublanguage
proves: [correctness, termination]
status: full
---

**Setting.** The plant $G$ and the specification automaton $H$ are deterministic automata over the alphabet $\Sigma = \Sigma_c \cup \Sigma_{uc}$, where $\Sigma_{uc}$ is the set of uncontrollable events. Let $K = L_m(H) \cap L_m(G)$. A language $M \subseteq K$ is controllable if $\overline{M}\,\Sigma_{uc} \cap L(G) \subseteq \overline{M}$, where $\overline{M}$ is the prefix closure of $M$. Line L1 builds $A$, the accessible part of $H \times G$. A state of $A$ is a pair $(h, g)$, and a string $s$ is defined in $A$ if and only if it is defined in both $H$ and $G$. So $L(A) = L(H) \cap L(G)$ and $L_m(A) = K$. For $s \in L(A)$ we write $x(s)$ for the state of $A$ that $s$ reaches. Its second part is the state of $G$ that $s$ reaches. We write $S$ for the set `states` of the program, and $A_S$ for the restriction of $A$ to $S$.

**Lemma 1 (union).** A union of controllable languages is controllable. So $\sup C(K)$, the union of all controllable sublanguages of $K$, is controllable and is the largest one.

*Proof.* Let $M = \bigcup_i M_i$ with each $M_i$ controllable. The prefix closure commutes with unions, so $\overline{M} = \bigcup_i \overline{M_i}$. Take $s \in \overline{M}$ and $\sigma \in \Sigma_{uc}$ with $s\sigma \in L(G)$. Then $s \in \overline{M_i}$ for some $i$, so $s\sigma \in \overline{M_i} \subseteq \overline{M}$. $\blacksquare$

Let $R = \{x(s) : s \in \overline{\sup C(K)}\}$. This is well defined, because $\overline{\sup C(K)} \subseteq \overline{K} \subseteq L(A)$.

**Lemma 2 (invariant).** At every point of the run, $R \subseteq S$.

*Proof.* At the start $S$ is the full state set of $A$, so the claim holds. We show that no removal takes away a state of $R$. Assume $R \subseteq S$ just before a removal.

Line L5 removes $x = (h, g)$ if some $\sigma \in \Sigma_{uc}$ is defined at $g$ in $G$ and $\delta_A(x, \sigma)$ is undefined or not in $S$. Assume $x \in R$, so $x = x(s)$ for some $s \in \overline{\sup C(K)}$. Then $s\sigma \in L(G)$, and by Lemma 1 $s\sigma \in \overline{\sup C(K)}$. So $s\sigma \in L(A)$, $\delta_A(x, \sigma) = x(s\sigma)$ is defined, and $x(s\sigma) \in R \subseteq S$. This is a contradiction, so $x \notin R$.

Line L6 keeps the states of $S$ that are accessible and coaccessible inside $S$. Let $x = x(s)$ with $s \in \overline{\sup C(K)}$. Each prefix $s'$ of $s$ is in $\overline{\sup C(K)}$, so $x(s') \in R \subseteq S$, and the path of $s$ from the initial state to $x$ stays in $S$. So $x$ is accessible in $S$. There is $t$ with $st \in \sup C(K)$. In the same way the path of $st$ stays in $S$, and it ends at $x(st)$, which is marked in $A$ because $st \in K = L_m(A)$. So $x$ is coaccessible in $S$, and line L6 keeps it. $\blacksquare$

**Lemma 3 (the fixed point).** Let $S$ be the set when the loop stops at line L7, and let $M = L_m(A_S)$. Then $M \subseteq K$, $\overline{M} = L(A_S)$, and $M$ is controllable.

*Proof.* If $S$ is empty, $M = \emptyset$, and all three claims hold. Otherwise, in the last round line L5 removed nothing, so every state of $S$ passed the test of line L5 with this same set $S$. Line L6 also returned $S$, so $A_S$ is trim. $M \subseteq L_m(A) = K$. Each string of $L(A_S)$ reaches a state of $S$, from which a marked state of $S$ can be reached inside $S$, so $L(A_S) \subseteq \overline{M}$. The other inclusion is clear, so $\overline{M} = L(A_S)$. Now let $s \in \overline{M}$ and $\sigma \in \Sigma_{uc}$ with $s\sigma \in L(G)$. The state $x(s) = (h, g)$ is in $S$, and $\sigma$ is defined at $g$ in $G$. Because $x(s)$ passed the test of line L5, $\delta_A(x(s), \sigma) \in S$. So $s\sigma \in L(A_S) = \overline{M}$. $\blacksquare$

**Theorem (correctness).** The automaton that line L8 returns is trim, its marked language is $\sup C(K)$, and its language is $\overline{\sup C(K)}$.

*Proof.* By Lemma 3, $M$ is a controllable sublanguage of $K$, so $M \subseteq \sup C(K)$. Conversely, let $s \in \sup C(K)$. By Lemma 2, every prefix of $s$ reaches a state of $S$, so $s \in L(A_S)$. The state $x(s)$ is marked in $A$, because $s \in K$, and it is in $S$, so $s \in L_m(A_S) = M$. So $M = \sup C(K)$, and by Lemma 3 $L(A_S) = \overline{M}$. $\blacksquare$

**Theorem (termination and cost).** Let $n$ be the number of states of $A$ and $q = |\Sigma|$. The loop of lines L2 to L7 runs at most $n + 1$ rounds, and the run takes $O(n^2 q)$ dict operations.

*Proof.* Line L5 and line L6 only remove states. A round that does not stop at line L7 sets `changed`, so it removes at least one state. So at most $n$ rounds change $S$, and the next round stops. Line L1 does $O(n q)$ work, because each state of $A$ has at most $q$ outgoing transitions. In one round, line L5 looks at each transition of $G$ from the $g$ part of each state of $S$, which is $O(n q)$ work, and the two searches of line L6 also take $O(n q)$. So the total is $O(n q) + (n + 1) \cdot O(n q) = O(n^2 q)$. $\blacksquare$
