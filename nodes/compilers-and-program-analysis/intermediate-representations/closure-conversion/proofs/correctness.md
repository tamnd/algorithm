---
title: Closure conversion keeps the outcome and makes every function closed
proves: [correctness]
status: full
---

We use the notation of the page. The source language is evaluated by call-by-value substitution, left to right. We use the big-step form of the same semantics: $e \Downarrow r$ means that the run of the closed term $e$ ends with $r$, where $r$ is a value or the mark $\mathsf{stuck}$. A stuck subterm makes the whole run stuck, as in the small-step rules. A run that never ends has no $r$. The target language is the same with records `[e0, ..., em]` and projections `e.i`. The new names `self`, `c` and `a` of the conversion are not names of the source.

## 1. Closed code

**Lemma 1.** $FV(\mathrm{CONVERT}(e, \rho)) \subseteq \bigcup_{y \in FV(e)} FV(\rho(y))$.

*Proof.* By induction on $e$. Line L2 gives $\rho(x)$. Line L7 gives a record whose parts are the code and the terms $\rho(y_i)$, $y_i \in FV(e)$. The code is $\mathtt{fun}\ \mathit{self} \to \mathtt{fun}\ x \to \mathrm{CONVERT}(b, \rho')$. By induction its body has free variables among $FV(\rho'(z))$ for $z \in FV(b)$. Every $z \in FV(b)$ is $x$, $f$ for a fix, or some $y_i$, and $\rho'$ maps them to $x$, $\mathit{self}$ and $\mathit{self}.i$. So the code is closed. Line L8 adds the bound names $c$ and $a$ only. Line L9 maps the bound $x$ to itself, which the `let` binds. Line L10 is direct. $\square$

So every `fun` that the conversion makes is closed, and a function body has no free variable but `self` and its parameter. Since the input is closed and $\rho$ is empty at line L1, the output is closed.

## 2. Related values

Define $v \sim w$ between closed source values and closed target values:

- $c \sim c$ for every integer or boolean constant $c$;
- $v \sim [\mathit{code}, w_1, \dots, w_m]$ if $v$ is $\mathtt{fun}\ x \to b[\vec y := \vec v]$ or $\mathtt{fix}\ f\ x \to b[\vec y := \vec v]$ for a term $b$, where $y_1 < \dots < y_m$ are the free variables of $\mathtt{fun}\ x \to b$ (or of $\mathtt{fix}\ f\ x \to b$), $\mathit{code} = \mathtt{fun}\ \mathit{self} \to \mathtt{fun}\ x \to \mathrm{CONVERT}(b, \rho'_b)$ with $\rho'_b$ as in line L5, and $v_i \sim w_i$ for each $i$.

The definition is by induction on the size of $v$, since each $v_i$ is a proper part of $v$. Results are related by $r \sim r'$ if both are $\mathsf{stuck}$ or both are related values.

An *environment* for $e$ and $\rho$ is a pair of a source substitution $\sigma$, defined on $FV(e)$ with closed values, and a target substitution $\gamma$ with closed values, such that for every $y \in FV(e)$, $\rho(y)[\gamma] \Downarrow w_y$ in at most one step with $\sigma(y) \sim w_y$. The terms $\rho(y)$ have the forms $y$, $\mathit{self}$ and $\mathit{self}.i$, so this holds when $\gamma(y) = w_y$, or $\gamma(\mathit{self})$ is the record for $f$, or $\gamma(\mathit{self})$ is a record whose part $i$ is $w_y$.

## 3. The main lemma

**Lemma 2.** Let $(\sigma, \gamma)$ be an environment for $e$ and $\rho$, and write $T = \mathrm{CONVERT}(e, \rho)[\gamma]$.

1. If $e[\sigma] \Downarrow r$ then $T \Downarrow r'$ with $r \sim r'$.
2. If $T \Downarrow r'$ then $e[\sigma] \Downarrow r$ with $r \sim r'$.

*Proof.* Both parts by induction on the derivation, of the source run for part 1 and of the target run for part 2. The two parts have the same cases, in the order of the lines.

- **L2, a variable $y$.** $e[\sigma] = \sigma(y)$ is a value, and $T = \rho(y)[\gamma] \Downarrow w_y$ with $\sigma(y) \sim w_y$ by the definition of an environment.
- **L3 to L7, a function.** $e[\sigma]$ is the value $\mathtt{fun}\ x \to b[\vec y := \sigma(\vec y)]$, since $\sigma$ only touches the free variables $y_i$. The code is closed by Lemma 1, so $\gamma$ does not change it, and $T = [\mathit{code}, \rho(y_1)[\gamma], \dots, \rho(y_m)[\gamma]]$ evaluates each part, left to right, to $w_{y_i}$. The result $[\mathit{code}, w_{y_1}, \dots]$ is related to $e[\sigma]$ by the definition of $\sim$ with $v_i = \sigma(y_i)$. The case of `fix` is the same.
- **L8, a call $e_1\ e_2$.** The pair $(\sigma, \gamma)$ is an environment for $e_1$ and for $e_2$ with the same $\rho$, and $c$, $a$ are new, so binding them does not change $\rho(y)[\gamma]$. By induction, $e_1[\sigma]$ and the target of $e_1$ both end, or neither does. If both are stuck, both calls are stuck. Otherwise they give $v_1 \sim w_1$, and in the same way $e_2$ gives $v_2 \sim w_2$ or both are stuck. If $v_1$ is a constant, so is $w_1$; the source call is stuck, and the target `w1.0` is stuck, because $w_1$ is not a record. If $v_1 = \mathtt{fun}\ x \to b[\vec y := \vec v]$, then $w_1 = [\mathit{code}, \vec w]$ with $\vec v \sim \vec w$. The source steps to $b[\vec y := \vec v, x := v_2]$. The target computes `w1.0` = code, applies it to $w_1$ and to $w_2$, and reaches $\mathrm{CONVERT}(b, \rho'_b)[\mathit{self} := w_1, x := w_2]$. Now $\sigma' = \{\vec y \mapsto \vec v, x \mapsto v_2\}$ and $\gamma' = \{\mathit{self} \mapsto w_1, x \mapsto w_2\}$ form an environment for $b$ and $\rho'_b$: $\rho'_b(y_i) = \mathit{self}.i$ evaluates in one step to $w_i \sim v_i$, and $\rho'_b(x) = x$ gives $w_2 \sim v_2$. The run of the body is a smaller derivation, so the induction hypothesis gives related results. For $v_1 = \mathtt{fix}\ f\ x \to \dots$, add $f \mapsto v_1$ to $\sigma'$; $\rho'_b(f) = \mathit{self}$ gives $w_1 \sim v_1$.
- **L9, `let x = e1 in e2`.** As for the call: $e_1$ gives $v_1 \sim w_1$ or both are stuck. Then $(\sigma[x \mapsto v_1], \gamma[x \mapsto w_1])$ is an environment for $e_2$ and $\rho[x \mapsto x]$. A free variable $y \ne x$ of $e_2$ keeps its target term $\rho(y)$, which does not mention $x$: the terms of $\rho$ use only source names that are bound around $e$, `self`, and parts of `self`, and in the source the inner `let x` hides any outer $x$.
- **L10, constants, `if` and operators.** Constants map to themselves. For `if`, the conditions give related values; a boolean is related only to the same boolean, so both runs take the same branch, and anything else is stuck in both. For an operator, related integers are equal, so both give the same result; any other pair is stuck in both, since a function is related only to a record and the operators reject both.

In each case the target run uses the target runs of the parts in the same order as the source, so part 2 follows by the same case analysis, with the induction on the target derivation. $\square$

## 4. The theorem

**Theorem.** For a closed source term $e$, the runs of $e$ and of CLOSURE-CONVERT$(e)$ both end with related results, or both run forever. In particular they give the same integer or boolean, both give a function value (a record in the target), or both get stuck.

*Proof.* At line L1, $\rho$ is empty and $e$ is closed, so the empty $\sigma$ and $\gamma$ form an environment. Lemma 2, part 1, shows that if the source ends then the target ends with a related result. Part 2 shows that if the target ends then so does the source. So if one runs forever, so does the other. $\square$
