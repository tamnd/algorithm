---
title: The worklist 0-CFA computes the least closed analysis in cubic time, and the analysis is sound for call-by-value runs
proves: [correctness, termination, complexity]
status: full
---

**Setting.** The program is a term of the toy language with the nodes `x`, `fun x -> e`, `fix f x -> e`, `e1 e2`, `let x = e1 in e2`, `if e1 then e2 else e3`, `e1 op e2` and integer and boolean constants. Line L1 gives every node a label $t$, and gives every variable occurrence its binder: the lambda, fix or let node that binds it, paired with the name. A *function* is a lambda or a fix node, and $\Lambda$ is the set of functions. For a function $\lambda$, $\mathrm{param}(\lambda)$ is the binder of its argument and $\mathrm{body}(\lambda)$ its body. An *analysis* is a triple $(Re, C, R)$: a set $Re$ of labels, a set $C[t] \subseteq \Lambda$ for each label and a set $R[b] \subseteq \Lambda$ for each binder. It is *closed* if:

1. the root is in $Re$;
2. for a function $t \in Re$: $t \in C[t]$;
3. for a variable $t \in Re$ with binder $b$: $R[b] \subseteq C[t]$;
4. for $t$ = `let x = t1 in t2` in $Re$: $t_1, t_2 \in Re$, $C[t_1] \subseteq R[(t, x)]$ and $C[t_2] \subseteq C[t]$;
5. for $t$ = `if t1 then t2 else t3` in $Re$: $t_1, t_2, t_3 \in Re$ and $C[t_2] \cup C[t_3] \subseteq C[t]$;
6. for $t$ = `t1 op t2` in $Re$: $t_1, t_2 \in Re$;
7. for $t$ = `t1 t2` in $Re$: $t_1, t_2 \in Re$, and for every $\lambda \in C[t_1]$: $\mathrm{body}(\lambda) \in Re$, $C[t_2] \subseteq R[\mathrm{param}(\lambda)]$, $C[\mathrm{body}(\lambda)] \subseteq C[t]$, and if $\lambda$ is `fix f x -> e`, then $\lambda \in R[(\lambda, f)]$.

Analyses are ordered by inclusion in all parts. Each rule keeps holding when the sets grow on its right side, so the intersection of closed analyses is closed, and there is a least closed analysis.

In the algorithm, the set nodes are $C[t]$ and $R[b]$, $V[n]$ is the current set of node $n$, $D[n]$ is the part of $V[n]$ that has not yet been sent along the edges of $n$, and $n$ is in $W$ exactly when $D[n] \ne \emptyset$. $Re$ is the set of labels marked by line L9.

**Lemma 1 (the edge invariant).** At each test of line L4: for every edge $a \to b$, $V[a] \setminus D[a] \subseteq V[b]$; and for every application $t$ that watches the node $C[t_1]$ and every $\lambda \in V[C[t_1]] \setminus D[C[t_1]]$, $\mathrm{CALL}(t, \lambda)$ has run.

*Proof.* Line L19 creates an edge $a \to b$ and sends all of $V[a]$ to $b$ at once. Line L14 makes $t$ watch $C[t_1]$ and runs CALL for all of $V[C[t_1]]$ at once. After that, an element enters $V[a]$ only in line L21, which puts it into $D[a]$ too. It leaves $D[a]$ only in line L5, and lines L6 and L7 then send it along every edge of $a$ and to every watcher of $a$. Sets only grow, so an element once in $V[b]$ stays there. $\square$

**Lemma 2 (termination).** The algorithm stops.

*Proof.* There are finitely many set nodes, and each $V[n]$ is a subset of the finite set $\Lambda$. Every pass of the loop of line L4 removes a node $n$ with $D[n] \ne \emptyset$. A node returns to $W$ only when line L21 adds a new element to $V[n]$. So the number of passes is at most the number of nodes plus $\sum_n |V[n]|$, which is finite. Each REACH marks each label at most once (line L9), so each call of REACH stops. $\square$

**Lemma 3 (the result is closed).** When the algorithm stops, $(Re, V[C[\cdot]], V[R[\cdot]])$ is closed.

*Proof.* At the end $W$ is empty, so every $D[n]$ is empty, and Lemma 1 gives $V[a] \subseteq V[b]$ for every edge, and $\mathrm{CALL}(t, \lambda)$ for every watcher $t$ of $C[t_1]$ and every $\lambda \in V[C[t_1]]$. Line L3 puts the root in $Re$. For each label $t$ that line L9 marks, the lines after it give the rule of $t$: line L10 gives rule 2; line L11 gives the edge $R[b] \to C[t]$ of rule 3; line L12 gives the two edges of rule 4; line L13 gives the edges of rule 5; and line L14 makes $t$ watch $C[t_1]$. REACH visits the direct subterms of let, if, op and application nodes, which gives the membership parts of rules 4 to 7. For rule 7, each $\lambda \in V[C[t_1]]$ had $\mathrm{CALL}(t, \lambda)$, and lines L15 to L18 give exactly the four parts of the rule for $\lambda$. $\square$

**Lemma 4 (every fact is forced).** Let $(Re^*, C^*, R^*)$ be any closed analysis. At all times, every label marked by line L9 is in $Re^*$, $V[C[t]] \subseteq C^*[t]$ and $V[R[b]] \subseteq R^*[b]$.

*Proof.* By induction over the steps. Line L3 marks the root, which is in $Re^*$ by rule 1. REACH marks the direct subterms of a marked let, if, op or application node, which are in $Re^*$ by rules 4 to 7, and line L18 marks $\mathrm{body}(\lambda)$ for an application $t$ and a $\lambda \in V[C[t_1]] \subseteq C^*[t_1]$, which is in $Re^*$ by rule 7. Line L10 adds $t$ to $V[C[t]]$ for a marked function $t$, which rule 2 allows. Every edge $a \to b$ that lines L11 to L13, L16 and L17 create is an inclusion that rules 3 to 5 or 7 require of every closed analysis, for nodes marked or for a $\lambda$ in $C^*[t_1]$; so sending $V[a] \subseteq a^*$ along it keeps $V[b] \subseteq b^*$. Line L15 adds $\lambda$ to $V[R[(\lambda, f)]]$, which rule 7 requires. $\square$

**Theorem 1 (least closed analysis).** The algorithm stops and returns the least closed analysis.

*Proof.* Lemma 2, Lemma 3 and Lemma 4. $\square$

**The semantics.** A value is a constant or a closure $(\lambda, \rho)$ of a function and an environment. An environment maps names to values. The judgement $\rho \vdash t \Downarrow v$ is the usual call-by-value big-step evaluation. For an application, $\rho \vdash t_1 \Downarrow (\lambda, \rho')$ and $\rho \vdash t_2 \Downarrow a$, and then $\mathrm{body}(\lambda)$ runs in $\rho'$ extended with the argument, and for a fix also with $f$ bound to $(\lambda, \rho')$. A run that does not stop, or gets stuck, is a tree of finished and unfinished evaluations. Every finished evaluation in it has a derivation.

Given a closed analysis, say that a value $v$ *fits* a set $S \subseteq \Lambda$ if $v$ is a constant, or $v = (\lambda, \rho)$ with $\lambda \in S$ and $\rho$ *good* for $\lambda$. An environment $\rho$ is good for a node $t$ if each variable $x$ in scope at $t$, with binder $b$ at $t$, has $\rho(x)$ fitting $R[b]$. Good for $\lambda$ means good for $\lambda$ itself.

**Lemma 5 (the evaluation invariant).** If $t \in Re$, $\rho$ is good for $t$, and $\rho \vdash t \Downarrow v$, then $v$ fits $C[t]$. Moreover, every evaluation $\rho_1 \vdash t' \Downarrow v'$ that the derivation contains has $t' \in Re$ and $\rho_1$ good for $t'$. Every binding it makes, of $v'$ to a binder $b$, has $v'$ fitting $R[b]$, and every call it makes, at an application $t''$ to a function $\lambda$, has $\lambda \in C[t_1'']$.

*Proof.* By induction on the height of the derivation. A constant fits any set. A variable $x$ with binder $b$ gives $\rho(x)$, which fits $R[b] \subseteq C[t]$ by rule 3. A function $t$ gives $(t, \rho)$, with $t \in C[t]$ by rule 2, and $\rho$ is good for $t$. For `let x = t1 in t2`, rule 4 puts $t_1$ and $t_2$ in $Re$. By induction the value $a$ of $t_1$ fits $C[t_1] \subseteq R[(t, x)]$, so the extended environment is good for $t_2$, whose value fits $C[t_2] \subseteq C[t]$. The cases of `if` and of an operator are the same with rules 5 and 6; an operator gives a constant. For `t1 t2`, rule 7 puts $t_1, t_2 \in Re$. By induction $t_1$ gives $(\lambda, \rho')$ with $\lambda \in C[t_1]$ and $\rho'$ good for $\lambda$, which is the call fact. $t_2$ gives $a$ fitting $C[t_2] \subseteq R[\mathrm{param}(\lambda)]$, by rule 7. For a fix, $(\lambda, \rho')$ fits $R[(\lambda, f)]$, since $\lambda \in R[(\lambda, f)]$ by rule 7. So the environment of the body is good for $\mathrm{body}(\lambda)$, which is in $Re$ by rule 7. By induction its value fits $C[\mathrm{body}(\lambda)] \subseteq C[t]$. The facts about the inner evaluations come from the induction hypothesis for each premise. $\square$

**Theorem 2 (soundness).** Let the root be closed, and let $(Re, C, R)$ be the result. In every run of the program, finished or not, every evaluation of a node $t$ to a closure $(\lambda, \rho)$ has $\lambda \in C[t]$, every binding of a closure $(\lambda, \rho)$ to a binder $b$ has $\lambda \in R[b]$, and every call at an application $t$ to a function $\lambda$ has $\lambda \in C[t_1]$.

*Proof.* The root is in $Re$, and the empty environment is good for the closed root. Every finished evaluation in the run is a derivation inside the derivation tree of the run, which starts at the root with the empty environment. Apply Lemma 5 to the finished sub-derivations. A call is made only after both $t_1$ and $t_2$ have finished, so it is covered too. $\square$

**Theorem 3 (cost).** For a term of $n$ nodes, the algorithm runs in $O(n^3)$ time with hash sets, in expectation, or with bit vectors in the worst case.

*Proof.* There are at most $n$ cache nodes and at most $2n$ binder nodes, and each set has at most $|\Lambda| \le n$ elements. Lines L11 to L13 make $O(n)$ edges. Lines L16 and L17 make two edges per pair of an application and a function, so $O(n^2)$ edges in all. Each element enters each $D[n]$ at most once, because line L20 removes the elements already in $V[n]$. So line L7 sends each element along each edge at most once, which costs $O(n^2) \cdot O(n) = O(n^3)$. CALL runs for a pair $(t, \lambda)$ at most twice: once in line L14 and once when $\lambda$ is in the delta of the operator in line L6. That is $O(n^2)$ calls. Each call does $O(1)$ work besides line L19, which may send a whole set of $O(n)$ elements, so the calls cost $O(n^3)$. REACH marks each label once and does $O(1)$ work per label besides its edges and calls. The total is $O(n^3)$. $\blacksquare$
