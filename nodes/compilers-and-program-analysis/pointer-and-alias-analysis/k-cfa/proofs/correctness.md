---
title: The round-robin k-CFA stops with the least closed analysis, which is sound for call-by-value runs with contours
proves: [correctness, termination, complexity]
status: full
---

**Setting.** The program is a closed term of the toy language of the [0-CFA](/zero-cfa/) page, with labels, binders, functions $\Lambda$, $\mathrm{param}(\lambda)$ and $\mathrm{body}(\lambda)$ as there, and $\mathrm{fv}(t)$ the free names of node $t$. Fix $k \ge 0$. A *contour* $\delta$ is a sequence of at most $k$ application labels. For a contour $\delta$ and an application $t$, $\mathrm{next}(\delta, t)$ is the last $k$ elements of $\delta$ followed by $t$ (the empty sequence when $k = 0$). An *abstract environment* $ce$ maps names to contours, and $ce|_t$ is its restriction to $\mathrm{fv}(t)$. An *abstract closure* is a pair $(\lambda, ce)$ with $ce$ defined exactly on $\mathrm{fv}(\lambda)$.

An *analysis* is a triple $(T, C, R)$: a set $T$ of tasks $(t, ce, \delta)$ with $ce$ defined on $\mathrm{fv}(t)$, a set $C[(t, \delta)]$ of abstract closures for each label and contour, and a set $R[(b, \delta)]$ for each binder and contour. It is *closed* if $(root, \emptyset, ())$ is in $T$ and every task $(t, ce, \delta) \in T$ satisfies the rule of lines L6 to L15:

1. a variable $x$ with binder $b$: $R[(b, ce(x))] \subseteq C[(t, \delta)]$;
2. a function: $(t, ce) \in C[(t, \delta)]$;
3. `let x = t1 in t2`: $(t_1, ce|_{t_1}, \delta) \in T$, $C[(t_1, \delta)] \subseteq R[((t, x), \delta)]$, $(t_2, ce[x \mapsto \delta]|_{t_2}, \delta) \in T$ and $C[(t_2, \delta)] \subseteq C[(t, \delta)]$;
4. `if` and operators: each direct subterm $u$ has $(u, ce|_u, \delta) \in T$, and for `if t1 then t2 else t3`, $C[(t_2, \delta)] \cup C[(t_3, \delta)] \subseteq C[(t, \delta)]$;
5. `t1 t2`: $(t_1, ce|_{t_1}, \delta), (t_2, ce|_{t_2}, \delta) \in T$, and for every $(\lambda, ce') \in C[(t_1, \delta)]$, with $\delta' = \mathrm{next}(\delta, t)$ and $ce''$ equal to $ce'$ with the parameters of $\lambda$ mapped to $\delta'$: $C[(t_2, \delta)] \subseteq R[(\mathrm{param}(\lambda), \delta')]$; if $\lambda$ is `fix f x -> e`, $(\lambda, ce') \in R[((\lambda, f), \delta')]$; $(\mathrm{body}(\lambda), ce''|_{\mathrm{body}(\lambda)}, \delta') \in T$; and $C[(\mathrm{body}(\lambda), \delta')] \subseteq C[(t, \delta)]$.

Each rule keeps holding when the sets on its right side grow, so the intersection of closed analyses is closed and a least closed analysis exists.

**Lemma 1 (finiteness).** There are finitely many tasks, keys and abstract closures. With $n$ nodes, the number of contours is $N = \sum_{i=0}^{k} n^i \le (n + 1)^k$, the number of abstract closures is at most $Q = n \cdot N^{n}$, and the number of tasks is at most $n \cdot N^{n} \cdot N$.

*Proof.* A contour is a sequence of at most $k$ labels. An abstract closure is a function label and a map from at most $n$ names to contours. A task is a label, a map from at most $n$ names to contours and a contour. $\square$

**Lemma 2 (termination).** The loop of lines L2 to L4 stops.

*Proof.* Every pass that does not stop the loop adds a task or an element to some set. Sets and tasks never shrink, and by Lemma 1 they live in finite sets. So the number of passes is at most the number of possible tasks plus the number of possible pairs of a key and a closure, plus one. $\square$

**Lemma 3 (every fact is forced).** Let $(T^*, C^*, R^*)$ be any closed analysis. At all times $T \subseteq T^*$, $C \subseteq C^*$ and $R \subseteq R^*$.

*Proof.* By induction over the steps. Line L1 adds the root task, which is in $T^*$. Every other addition is made by the rule of a task $(t, ce, \delta) \in T \subseteq T^*$, and it is the conclusion of rule 1 to 5 for this task, with premises (the sets read and the closures picked in line L11) inside $C^*$ and $R^*$ by induction. Since $(T^*, C^*, R^*)$ is closed, the same conclusion holds there. $\square$

**Theorem 1 (least closed analysis).** The algorithm stops and returns the least closed analysis.

*Proof.* It stops by Lemma 2. In the last pass, the rule of every task ran and changed nothing, so every task satisfies its rule with the final sets, and the result is closed. By Lemma 3 it is inside every closed analysis. $\square$

**The semantics with contours.** A value is a constant or a closure $(\lambda, \rho)$, where an environment $\rho$ maps each name to a pair of a contour and a value. Evaluation $\rho \vdash_\delta t \Downarrow v$ is call-by-value with a current contour $\delta$. A `let` binds $x$ to $(\delta, v_1)$ and stays in $\delta$. A call at application $t$ of a closure $(\lambda, \rho')$ binds the parameters of $\lambda$ to $\mathrm{next}(\delta, t)$, with the argument and, for a fix, the closure itself, and runs the body in the contour $\mathrm{next}(\delta, t)$. The contours do not change the values: dropping them gives the plain environment semantics. The abstraction of an environment is $|\rho|(x) = $ the contour of $\rho(x)$, and of a closure is $|(\lambda, \rho)| = (\lambda, |\rho|\,|_\lambda)$.

An environment $\rho$ is *good* if, for each name $x$ in it, with binder $b$ at the place where $\rho$ is used and $\rho(x) = (c, v)$, either $v$ is a constant or $v = (\lambda, \rho_1)$ with $|v| \in R[(b, c)]$ and $\rho_1$ good.

**Lemma 4 (the evaluation invariant).** Let $(T, C, R)$ be closed. If $(t, |\rho|\,|_t, \delta) \in T$, $\rho$ is good, and $\rho \vdash_\delta t \Downarrow v$, then $v$ is a constant or $|v| \in C[(t, \delta)]$ with a good environment. Every evaluation inside the derivation, $\rho_1 \vdash_{\delta_1} t_1 \Downarrow v_1$, has its task $(t_1, |\rho_1|\,|_{t_1}, \delta_1)$ in $T$ and $\rho_1$ good; every binding of a closure $v_1$ to a binder $b$ in contour $c$ has $|v_1| \in R[(b, c)]$; and every call at $t''$ of a closure of $\lambda$ has $\lambda$ among the functions of $C[(t''_1, \delta_1)]$ for the contour $\delta_1$ of the call.

*Proof.* By induction on the height of the derivation. A variable $x$ with binder $b$ and $\rho(x) = (c, v)$: $|\rho|(x) = c$, and $|v| \in R[(b, c)] \subseteq C[(t, \delta)]$ by rule 1. A function gives $(t, \rho)$, whose abstraction is $(t, |\rho|\,|_t)$, in $C[(t, \delta)]$ by rule 2. A `let`: rule 3 gives the task of $t_1$ with $|\rho|\,|_{t_1}$, so by induction $v_1$ is in $C[(t_1, \delta)] \subseteq R[((t, x), \delta)]$. The new environment binds $x$ to $(\delta, v_1)$, so it is good, its abstraction is $|\rho|[x \mapsto \delta]$, and rule 3 gives the task of $t_2$. By induction the value is in $C[(t_2, \delta)] \subseteq C[(t, \delta)]$. `if` and operators are the same with rule 4. An application `t1 t2`: rule 5 gives the tasks of $t_1$ and $t_2$, so by induction $t_1$ gives $(\lambda, \rho')$ with $(\lambda, |\rho'|\,|_\lambda) \in C[(t_1, \delta)]$, which is the call fact, and the argument $a$ is a constant or in $C[(t_2, \delta)]$. Let $\delta' = \mathrm{next}(\delta, t)$, the same in both semantics. By rule 5, $|a| \in R[(\mathrm{param}(\lambda), \delta')]$, and for a fix, $(\lambda, |\rho'|\,|_\lambda) \in R[((\lambda, f), \delta')]$. So the environment of the body is good, its abstraction is $|\rho'|\,|_\lambda$ with the parameters mapped to $\delta'$, and rule 5 gives the task of the body. By induction its value is in $C[(\mathrm{body}(\lambda), \delta')] \subseteq C[(t, \delta)]$. The facts about inner evaluations come from the induction hypothesis on each premise. $\square$

**Theorem 2 (soundness).** Let $(T, C, R)$ be the result. In every run of the closed program, finished or not, every evaluation of a node $t$ in contour $\delta$ to a closure $v$ has $|v| \in C[(t, \delta)]$, every binding of a closure $v$ to binder $b$ in contour $c$ has $|v| \in R[(b, c)]$, and every call at application $t$ runs a function $\lambda$ that appears in $C[(t_1, \delta)]$. Dropping the contours, the result contains the 0-CFA facts of the run.

*Proof.* The root task is in $T$ with the empty environment, which is good. Every finished evaluation of the run is a sub-derivation of the run from the root, so Lemma 4 applies to it. A call is made only after its operator and argument have finished. $\square$

**Theorem 3 (cost).** The algorithm runs in time polynomial in $n$, $N$, $Q$ and the number of tasks, so in time $2^{O(n \log n)}$ for fixed $k \ge 1$, and in time polynomial in $n$ for $k = 0$.

*Proof.* By Lemma 2 there are at most (number of tasks) $+ (3 n N) \cdot Q + 1$ passes, since there are at most $n N$ cache keys and $2 n N$ binder keys. Each pass runs the rule of every task once. A rule makes $O(1)$ unions per closure of the operator, and each union of sets of at most $Q$ elements costs $O(Q)$ with hashing. With $N \le (n+1)^k$, $Q$ and the number of tasks are at most $n \cdot (n+1)^{k(n+1)} = 2^{O(n \log n)}$ for fixed $k$, so the number of passes and the cost of a pass are both $2^{O(n \log n)}$, and so is their product. For $k = 0$ there is one contour, every abstract environment maps all names to the empty contour, so $Q \le n$, there are at most $n$ tasks, and the time is polynomial. The exponential bound cannot be improved to a polynomial, since P is not EXPTIME by the time hierarchy theorem and Van Horn and Mairson prove that deciding a k-CFA fact is EXPTIME-complete for every $k \ge 1$ (see the [theorem page](/k-cfa-exptime-completeness/)). $\blacksquare$
