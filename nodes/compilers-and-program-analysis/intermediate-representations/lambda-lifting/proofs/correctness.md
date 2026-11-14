---
title: Lambda lifting gives closed global functions and keeps the outcome
proves: [correctness]
status: full
---

We use the notation of the page. After line L1 every binder of the term is unique and differs from every free name, and each function $f$ (a `fun`, a `fix`, or a member of a `letrec`) has its own global $F$. We write $x_f$ for the parameter of $f$, $\mathrm{params}(f)$ for the sorted list $E(f)$, and $\hat g$ for the term $G\ \mathrm{params}(g)$ that lines L9 and L10 put in place of $g$.

The source language is evaluated by call-by-value substitution, left to right, and we use the big-step form: $e \Downarrow r$ means that the run of the closed term $e$ ends with $r$, a value or the mark $\mathsf{stuck}$. A stuck part makes the whole run stuck. In the target, $G\ w_1 \dots w_j$ with $j$ less than the number of parameters of $G$ and values $w_i$ is a value, and a full application steps to the body of $G$ with the arguments put in for the parameters. Section 3 treats `fun` and `fix`; section 4 adds `letrec`.

## 1. Scope

**Lemma 1.** If $g \in R(f)$ then $E(g) \subseteq E(f)$.

*Proof.* Every function reachable from $g$ along $R$ is reachable from $f$, since $f$ reaches $g$. Line L4 takes the union of $D$ over these sets. $\square$

Say that a variable is *visible* at a point of the term if a binder (a parameter, a `let`, a `fix` or a `letrec` name) that encloses the point binds it. Since binders are unique, a variable visible at the binder of a function name $g$ is visible at every point in the scope of that name.

**Lemma 2.** Let $\psi$ be a function, and let $\chi$ be the innermost function whose body contains the definition of $\psi$, if one exists. Each $y \in E(\psi)$ is a parameter in $E(\chi) \cup \{x_\chi\}$, or is bound by a `let` that encloses $\psi$ inside the body of $\chi$. If no $\chi$ exists, each $y \in E(\psi)$ is bound by a `let` of the main term around $\psi$.

*Proof.* Let $y \in D(g)$ for a path $\psi = g_0, g_1, \dots, g_k = g$ along $R$. First, $y$ is visible at the definition of $\psi$: $y$ is free in $g_k$ and the input is closed, so $y$ is visible at the definition of $g_k$; for each $i$, the name of $g_{i+1}$ is free in $g_i$, so $g_i$ lies in the scope of that name, and what is visible at the definition of $g_{i+1}$ is visible at the definition of $g_i$. Now suppose $\chi$ exists. If $y$ is $x_\chi$ or is bound by a `let` inside the body of $\chi$, we are done. The binder of $y$ cannot be the parameter of a function inside the body of $\chi$, since $\chi$ is the innermost function around $\psi$. Otherwise $y$ is bound outside $\chi$. If all $g_i$ are defined inside $\chi$ (or are $\chi$), then $y$, free in $g_k$ and bound outside $\chi$, is free in $\chi$ and names no function, so $y \in D(\chi) \subseteq E(\chi)$. If not, let $g_i$ be the first that is defined outside $\chi$. Its name is free in $g_{i-1}$, which is inside $\chi$, and is bound outside $\chi$, so $g_i \in R(\chi)$ and $y \in E(g_i) \subseteq E(\chi)$ by Lemma 1. Without $\chi$, $y$ is visible at $\psi$, and the only binders around $\psi$ are `let`s of the main term. $\square$

**Corollary.** Every body $\mathrm{LIFT}(b)$ of a definition $F\ \mathrm{params}(f)\ x_f$ has no free variable but its parameters, and $\mathrm{LIFT}(e)$ of the main term is closed. The output has no `fun`, `fix` or `letrec`.

*Proof.* LIFT keeps variables that name no function, removes every function, and adds the arguments of $\hat g$. A kept variable $y$ of $b$ is free in $f$ (so in $D(f)$), is $x_f$, or is bound by a `let` of $b$. A function $\psi$ defined in $b$ has $\chi = f$, and Lemma 2 places the arguments of $\hat\psi$ among the parameters of $F$ and the `let`s around it. A use of a function name $g$ in $b$ is $g = f$, a function defined in $b$, or $g \in R(f)$; the first two are as before and the third passes $E(g) \subseteq E(f)$ by Lemma 1. The main term is the same with no $\chi$. $\square$

## 2. Related values

Define $v \sim w$ between closed source values and closed target values:

- $c \sim c$ for each integer or boolean constant $c$;
- $f[\sigma] \sim F\ w_1 \dots w_k$ if $f$ is a function of the renamed term, $\sigma$ maps the free variables of $f$ to closed source values, $\mathrm{params}(f) = p_1, \dots, p_k$, and the target substitution $\gamma = \{p_i \mapsto w_i\}$ satisfies: $\sigma(y) \sim \gamma(y)$ for each $y \in D(f)$, and $\sigma(g) \sim \hat g[\gamma]$ for each $g \in R(f)$.

By Lemma 1, $\hat g[\gamma]$ is a closed term $G\ w_{j_1} \dots w_{j_l}$, a value. The definition is by induction on the size of the source value, since $\sigma(y)$ and $\sigma(g)$ are proper parts of $f[\sigma]$. Results are related if both are $\mathsf{stuck}$ or both are related values.

An *environment* for a subterm $e$ is a pair of a source substitution $\sigma$ on the free variables of $e$ and a target substitution $\gamma$ such that $\sigma(y) \sim \gamma(y)$ for each free $y$ of $e$ that names no function, and $\gamma$ is defined on $E(g)$ with $\sigma(g) \sim \hat g[\gamma]$ for each free function name $g$ of $e$.

## 3. The main lemma

**Lemma 3.** Let $(\sigma, \gamma)$ be an environment for $e$, a subterm of the renamed term, and let $\gamma$ also be defined on the extra parameters of every function defined in $e$ that are bound outside $e$. Write $T = \mathrm{LIFT}(e)[\gamma]$.

1. If $e[\sigma] \Downarrow r$ then $T \Downarrow r'$ with $r \sim r'$.
2. If $T \Downarrow r'$ then $e[\sigma] \Downarrow r$ with $r \sim r'$.

*Proof.* Both parts by induction on the derivation, of the source run for part 1 and of the target run for part 2, with one case per form.

- **A variable $y$ that names no function.** Both sides are values, $\sigma(y) \sim \gamma(y)$.
- **A function name $g$ (line L9).** $e[\sigma] = \sigma(g)$ and $T = \hat g[\gamma]$, related by the environment.
- **A function $f$ (line L10).** $e[\sigma] = f[\sigma]$ is a value, and $T = F\ \gamma(p_1) \dots \gamma(p_k)$ is a value, since it lacks the argument $x_f$. Each $y \in D(f)$ is free in $e$, so $\sigma(y) \sim \gamma(y)$; each $g \in R(f)$ is free in $e$, so $\sigma(g) \sim \hat g[\gamma]$. These are the conditions of $\sim$, and the side condition on $\gamma$ makes $\gamma(p_i)$ defined.
- **A call $e_1\ e_2$.** The pair is an environment for both parts, and LIFT keeps the call. By induction both runs of $e_1$ end with related results or neither ends, and then the same for $e_2$; a stuck part is stuck in both. Let the values be $v_1 \sim w_1$ and $v_2 \sim w_2$. If $v_1$ is a constant, $w_1$ is the same constant, and both calls are stuck. Otherwise $v_1 = f[\sigma_1]$ and $w_1 = F\ w_1' \dots w_k'$ with $\gamma_1 = \{p_i \mapsto w_i'\}$ as in the definition of $\sim$. The source steps to $b[\sigma_1, x_f := v_2]$, with also $f := v_1$ if $f$ is a `fix`. The target $F\ w_1' \dots w_k'\ w_2$ is a full application and steps to $\mathrm{LIFT}(b)[\gamma_1, x_f := w_2]$. Set $\sigma' = \sigma_1 \cup \{x_f \mapsto v_2\}$ (and $f \mapsto v_1$) and $\gamma' = \gamma_1 \cup \{x_f \mapsto w_2\}$. This is an environment for $b$: a free $y$ of $b$ that names no function is $x_f$ or lies in $D(f)$; a free function name of $b$ is $f$ itself, with $\hat f[\gamma'] = w_1 \sim v_1$, or some $g \in R(f)$, with $E(g) \subseteq E(f)$ by Lemma 1. The side condition holds by Lemma 2 with $\chi = f$: the extra parameters of a function in $b$ that are bound outside $b$ are in $E(f) \cup \{x_f\}$. The run of the body is a smaller derivation, so the induction hypothesis gives related results.
- **`let x = e1 in e2`.** As for the call, $e_1$ gives $v_1 \sim w_1$ or both are stuck. Then $(\sigma[x \mapsto v_1], \gamma[x \mapsto w_1])$ is an environment for $e_2$ that meets the side condition: a function in $e_2$ may have $x$ as an extra parameter, and $\gamma$ now binds it. Since $x$ is unique, the new binding hides nothing.
- **Constants, `if` and operators.** Constants map to themselves. A boolean is related only to the same boolean, so both runs of `if` take the same branch, and any other value is stuck in both. Related integers are equal, so operators give equal results; a function is related only to a partial application, and the operators reject both.

The target run uses the runs of the parts in the same order as the source, so part 2 follows from the same case analysis with the induction on the target derivation. $\square$

**Theorem.** For a closed term $e$ without `letrec`, the run of $e$ and the run of the main term of LAMBDA-LIFT$(e)$ both end with related results, or both run forever. They give the same integer or boolean, a function value and a partial application, or stuck in both.

*Proof.* Renaming apart at line L1 does not change the outcome. The empty pair is an environment for the closed renamed term, and Lemma 2 without $\chi$ shows that the extra parameters of a function in the main term are bound by its `let`s, so the side condition of Lemma 3 holds with $\gamma$ empty. Part 1 of Lemma 3 shows that if the source ends then the target ends with a related result. Part 2 shows that if the target ends then so does the source. So if one runs forever, so does the other. $\square$

## 4. Mutual recursion

Give `letrec f1 x1 = b1 and ... and fk xk = bk in e` its usual meaning: the run of the `letrec` is the run of $e[f_1 := u_1, \dots, f_k := u_k]$, where $u_i$ is the value of $f_i$, and a call of $u_i$ runs $b_i$ with $x_i$ and all $u_j$ put in. In the relation $\sim$, a value $u_i$ is then $f_i[\sigma]$ with $\sigma(f_j) = u_j$ for the members $f_j \in R(f_i)$. That definition is no longer by the size of the value, since $u_i$ appears inside $\sigma$; read $\sim$ as indexed by the number of steps left, as in a step-indexed relation, where a call uses one step. The cases of Lemma 3 are unchanged, except that a `letrec` passes to its body with each $\sigma(f_i) = u_i$ and $\gamma$ unchanged: LIFT removes the `letrec`, and by Lemma 1 each $\hat f_i[\gamma]$ is defined. The fixed point of line L4 is used exactly here. Without it, $E(f_i)$ could miss a variable of $E(f_j)$ for some $f_j \in R(f_i)$, and the call of $\hat f_j$ in the body of $F_i$ would have a free variable. The page shows such a program, which gets stuck.
