---
title: The no-sensitive-upgrade monitor is termination-insensitive noninterferent
proves: [correctness]
status: full
---

We use the language and the pseudocode of the page. Labels are in a finite lattice $(\mathcal{L}, \le, \sqcup, \sqcap)$ with least element $\bot$. A monitor state is a pair $(s, \lambda)$ of a store and a label map. For an expression $e$, $\mathrm{lab}_\lambda(e)$ is the join of $\lambda(y)$ over the variables $y$ of $e$.

**Semantics.** We write $\langle d, p, s, \lambda \rangle \Downarrow (t, \mu)$ when the monitored run of command $d$ at program counter label $p$ from $(s, \lambda)$ ends normally in $(t, \mu)$, with these rules:

- skip leaves the state unchanged.
- $x := e$ needs $p \le \lambda(x)$; then $t = s[x \mapsto v]$ and $\mu = \lambda[x \mapsto \mathrm{lab}_\lambda(e) \sqcup p]$, where $v$ is the value of $e$ in $s$. If $p \not\le \lambda(x)$ the run stops, and there is no derivation.
- $d_1; d_2$ runs $d_1$ and then $d_2$, both at $p$.
- if $e$ then $d_1$ else $d_2$ runs the branch chosen by the value of $e$ at $p \sqcup \mathrm{lab}_\lambda(e)$.
- while $e$ do $d_1$: if $e$ is false, nothing changes. If $e$ is true, with $q = p \sqcup \mathrm{lab}_\lambda(e)$, it runs $d_1$ at $q$ and then the loop again at $q$.

The loop of lines L2 to L12 is the stack form of these rules. Each stack entry holds a command and its program counter label. Line L8 pushes the two parts of a sequence with the label of the sequence, line L10 pushes the chosen branch with the raised label, and line L12 pushes the body and then the loop with the raised label. So the entries are popped in the order of the rules, each with the label the rules give it, and the run ends normally at line L13 exactly when there is a derivation. A stopped run or a run that does not end has no derivation.

**Observation.** Fix an observer level $\ell$. The observer of a final state $(t, \mu)$ sees, for each variable $x$, the value $t(x)$ if $\mu(x) \le \ell$, and a mark "hidden" otherwise. Two states are $\ell$-equivalent, $(s_1, \lambda_1) \sim (s_2, \lambda_2)$, if for every variable $x$: $\lambda_1(x) \le \ell$ if and only if $\lambda_2(x) \le \ell$, and if both hold, $s_1(x) = s_2(x)$. So two final states look the same to the observer exactly when they are $\ell$-equivalent. The relation $\sim$ is an equivalence relation. Two labels $p_1, p_2$ are $\ell$-equivalent, $p_1 \approx p_2$, if $p_1 \le \ell$ if and only if $p_2 \le \ell$.

**Theorem.** Let $\Gamma$ be the initial label map and let $s_1 =_\ell s_2$ (they agree on every $x$ with $\Gamma(x) \le \ell$). If $\langle c, \bot, s_1, \Gamma \rangle \Downarrow (t_1, \mu_1)$ and $\langle c, \bot, s_2, \Gamma \rangle \Downarrow (t_2, \mu_2)$, then $(t_1, \mu_1) \sim (t_2, \mu_2)$.

The start states are $\ell$-equivalent, since both use $\Gamma$ and the stores agree where $\Gamma(x) \le \ell$. So the theorem follows from Lemma 3 below with $p_1 = p_2 = \bot$.

**Lemma 1 (expressions).** If $(s_1, \lambda_1) \sim (s_2, \lambda_2)$, then $\mathrm{lab}_{\lambda_1}(e) \approx \mathrm{lab}_{\lambda_2}(e)$, and if $\mathrm{lab}_{\lambda_1}(e) \le \ell$, the value of $e$ is the same in $s_1$ and $s_2$.

*Proof.* A join is at most $\ell$ exactly when each of its terms is. So $\mathrm{lab}_{\lambda_i}(e) \le \ell$ exactly when $\lambda_i(y) \le \ell$ for every variable $y$ of $e$, and by $\ell$-equivalence this condition is the same for $i = 1$ and $i = 2$. When it holds, $s_1(y) = s_2(y)$ for each such $y$, so $e$ has the same value.

**Lemma 2 (confinement).** If $p \not\le \ell$ and $\langle d, p, s, \lambda \rangle \Downarrow (t, \mu)$, then for every variable $x$: if $\lambda(x) \le \ell$ then $\mu(x) = \lambda(x)$ and $t(x) = s(x)$; and if $\lambda(x) \not\le \ell$ then $\mu(x) \not\le \ell$. In particular $(s, \lambda) \sim (t, \mu)$.

*Proof.* By induction on the derivation. Every command in the derivation runs at a label $p' \ge p$, since the rules only raise the label; so $p' \not\le \ell$. Consider an assignment $x := e$ at $p'$ in state $(u, \nu)$. The check gives $p' \le \nu(x)$. If $\nu(x) \le \ell$ we would get $p' \le \ell$, which is false; so $\nu(x) \not\le \ell$, and the new label $\mathrm{lab}_\nu(e) \sqcup p' \ge p'$ is also not below $\ell$. So an assignment changes only variables whose label is not below $\ell$, and keeps their label not below $\ell$. Each other rule is a composition of such steps, and the property is kept under composition.

**Lemma 3 (main).** Let $(s_1, \lambda_1) \sim (s_2, \lambda_2)$ and $p_1 \approx p_2$. If $\langle d, p_1, s_1, \lambda_1 \rangle \Downarrow (t_1, \mu_1)$ and $\langle d, p_2, s_2, \lambda_2 \rangle \Downarrow (t_2, \mu_2)$, then $(t_1, \mu_1) \sim (t_2, \mu_2)$.

*Proof.* By induction on the sum of the sizes of the two derivations, by the form of $d$.

1. *skip.* The states do not change.
2. *$x := e$.* Both checks pass, since both runs end normally. Let $\ell_i = \mathrm{lab}_{\lambda_i}(e)$. The new labels are $\ell_i \sqcup p_i$. If $p_1, p_2 \le \ell$, then $\ell_i \sqcup p_i \le \ell$ exactly when $\ell_i \le \ell$, which by Lemma 1 is the same for both runs; and when it holds, Lemma 1 gives the same value for $x$. If $p_1, p_2 \not\le \ell$, both new labels are not below $\ell$, so $x$ is hidden in both states. The other variables do not change.
3. *$d_1; d_2$.* The hypothesis for $d_1$ gives $\ell$-equivalent middle states, and the hypothesis for $d_2$, with the same labels $p_1 \approx p_2$, gives the result.
4. *if $e$ then $d_1$ else $d_2$.* Let $\ell_i = \mathrm{lab}_{\lambda_i}(e)$; by Lemma 1, $\ell_1 \approx \ell_2$. If $\ell_1 \le \ell$, then $e$ has the same value in both runs, both run the same branch, and the labels $p_i \sqcup \ell_i$ are $\ell$-equivalent (both are below $\ell$ exactly when $p_i \le \ell$). The hypothesis for the branch gives the result. If $\ell_1 \not\le \ell$, then $p_i \sqcup \ell_i \not\le \ell$, and Lemma 2 applied to each run gives $(t_i, \mu_i) \sim (s_i, \lambda_i)$. By transitivity, $(t_1, \mu_1) \sim (s_1, \lambda_1) \sim (s_2, \lambda_2) \sim (t_2, \mu_2)$.
5. *while $e$ do $d_1$.* Let $\ell_i$ be as above. If $\ell_1 \le \ell$, then $e$ has the same value in both runs. If it is false, the states do not change. If it is true, both runs run $d_1$ and then the loop at $q_i = p_i \sqcup \ell_i$, and $q_1 \approx q_2$. The hypothesis for $d_1$ and then for the loop (a smaller derivation in each run) gives the result. If $\ell_1 \not\le \ell$, a run with a false condition does not change its state, and a run with a true condition runs the body and the loop at $q_i \not\le \ell$, so Lemma 2 gives $(t_i, \mu_i) \sim (s_i, \lambda_i)$. Transitivity gives the result as in case 4.

This proves Lemma 3 and so the theorem. The theorem compares only runs that end normally. A run that the monitor stops, or that does not end, is not compared, so the monitor is termination-insensitive: whether it stops can depend on a secret. $\blacksquare$
