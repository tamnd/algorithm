---
title: BTA gives the least congruent annotation, and congruence makes specialization safe
proves: [correctness]
status: full
---

**Setting.** The program is a simply typed term $e$ of the toy lambda language, whose free variables are its inputs, all of base type. The inputs are split into static and dynamic ones. An annotation gives each node and each binder an annotated type with the shape of its simple type, as defined on the page. We identify an annotation with the set $X$ of binding-time variables that are $D$. BTA is lines L1 to L9 of the page, and $R$ is the set it returns as Dset. The specializer is the one described on the page.

## Theorem 1: the result is the least congruent annotation

*Claim.* $R$ is congruent, and every congruent annotation $X$ satisfies $R \subseteq X$.

*Proof.* Let $F$ be the facts of L3 and L6, and $I$ the implications of L4 and L5. Each implication is a pair of variables $u \Rightarrow v$.

First, an annotation $X$ is congruent if and only if $F \subseteq X$ and $X$ is closed under $I$, that is, $u \in X$ and $(u \Rightarrow v) \in I$ give $v \in X$. We compare the two lists rule by rule.

- A dynamic input must be $D$: these are the facts of L3. A function-typed root must be $D$: this is the fact of L6.
- Well formedness says that a $D$ function type has $D$ parts. L5 adds $b \Rightarrow \mathrm{top}(t_1)$ and $b \Rightarrow \mathrm{top}(t_2)$ for every annotated function type, and applied at every level this gives well formedness for the parts too.
- $\mathrm{flow}(\tau, \tau')$ at base type is the implication $\mathrm{top}(\tau) \Rightarrow \mathrm{top}(\tau')$. At function type it is equality on every pair of matching variables, which L4 adds as two implications, one in each direction.
- Each other rule of the table on the page is an implication between two variables, and L4 adds it as such.
- The parameter of a `fun` or `fix` node and its binder share their variables by L2, so the equality between them holds in every annotation.

So the congruence rules and $F \cup I$ say the same thing.

$R$ is the set of variables reachable from $F$ along $I$. It holds $F$. If $u \in R$ and $u \Rightarrow v$, then $v$ is reachable too, so $R$ is closed. Hence $R$ is congruent.

Let $X$ be congruent. Every $v \in R$ is reached by a path $f = v_0 \Rightarrow v_1 \Rightarrow \cdots \Rightarrow v_k = v$ with $f \in F$. By induction on $k$: $v_0 \in F \subseteq X$, and $v_{i} \in X$ gives $v_{i+1} \in X$ by closure. So $R \subseteq X$.

Finally, L8 never fails when all inputs have base type. The variable of an input $x$ appears in implications only through $\mathrm{flow}(\tau_x, \tau)$ at the uses of $x$, at base type, where it is on the left side. No implication ends at it, and it is a fact only when $x$ is dynamic. $\square$

## Theorem 2: no binding-time error

A *specializer value* is $(S, c)$ with $c$ a constant, $(S, k)$ with $k$ a closure (a `fun` or `fix` node of the program and an environment), or $(D, q)$ with $q$ a residual term. A residual term is *trivial* when it is a variable or a constant. Fix a congruent annotation. An environment $\rho$ for a node is *good* when, for each variable $x$ in scope with binder type $\tau_x$:

- if $\mathrm{top}(\tau_x) = S$ and $\tau_x$ is a base type, then $\rho(x) = (S, c)$ with $c$ a constant of that type;
- if $\mathrm{top}(\tau_x) = S$ and $\tau_x$ is a function type, then $\rho(x) = (S, k)$ where $k$ is a closure of a node whose annotated type is $\tau_x$, and whose environment is good for that node;
- if $\mathrm{top}(\tau_x) = D$, then $\rho(x) = (D, q)$ with $q$ trivial.

*Claim.* If the environment is good for a node $e$ of type $\tau$, and the specializer on $e$ returns, then it raises no binding-time error, and its result $r$ *fits* $\tau$: $r = (D, q)$ when $\mathrm{top}(\tau) = D$; $r = (S, c)$ with $c$ a constant of the simple type of $e$ when $\tau$ is a base type with $S$ on top; and $r = (S, k)$ with $k$ a closure as above when $\tau$ is a function type with $S$ on top.

A *coercion* of a result $r$ that fits $\tau$ to a place of type $\tau'$ with $\mathrm{flow}(\tau, \tau')$ never fails, and the result fits $\tau'$. At base type, the only change is $S$ to $D$, and a constant can be lifted. At function type, $\tau = \tau'$, so nothing changes.

*Proof.* By induction on the length of the run of the specializer on $e$, which is finite because it returns. One case per kind of node. All rules used are from the table on the page.

- *Variable.* The good environment gives a value that fits $\tau_x$, and the coercion along $\mathrm{flow}(\tau_x, \tau)$ makes it fit $\tau$.
- *Constant.* It is returned as $(S, c)$ or as the code $c$, as the mark says.
- *`fun x -> e1`, marked $S$.* The result is a closure of this node with the current environment, which is good. It fits $\tau$.
- *`fun x -> e1`, marked $D$.* Well formedness makes $\tau_x$ and $\tau_r$ dynamic on top. The body runs with $x$ bound to a fresh variable, which is trivial code, so the environment stays good. By induction the body result fits $\tau_1$, and the coercion along $\mathrm{flow}(\tau_1, \tau_r)$ gives code. The result $(D, \texttt{fun } x' \to q)$ fits $\tau$. A dynamic `fix` is the same, with $f$ also bound to a fresh variable; its binder type is $\tau$, which is $D$ on top.
- *`e1 e2`, function marked $D$.* Well formedness makes $\tau_a$ and $\tau_r$ dynamic. The argument result, coerced along $\mathrm{flow}(\tau_2, \tau_a)$, is code. $\mathrm{flow}(\tau_r, \tau)$ with $\mathrm{top}(\tau_r) = D$ makes $\mathrm{top}(\tau) = D$, so the code of the call fits $\tau$.
- *`e1 e2`, function marked $S$.* By induction the function gives a closure $k$ of a node with type $\tau_1 = (\tau_a \to^S \tau_r)$ and a good environment $\rho_k$. The argument is coerced along $\mathrm{flow}(\tau_2, \tau_a)$, so it fits $\tau_a$. If it is static or trivial code, the parameter is bound to it. Otherwise it is bound to a fresh variable, and a residual `let` is put around the body result. Then $\mathrm{top}(\tau_a) = D$, and the rule $\mathrm{top}(\tau_x) = D \Rightarrow \mathrm{top}(\tau_r) = D$ makes the body result, coerced to $\tau_r$, code, so the `let` can be built. For a `fix`, $f$ is bound to $(S, k)$, which fits the binder type of $f$, the type of the `fix` node. In all cases the body environment is good, and by induction (the run on the body is shorter) the body result fits the body type. It is coerced to $\tau_r$ and then along $\mathrm{flow}(\tau_r, \tau)$.
- *`let x = e1 in e2`.* If $\mathrm{top}(\tau_x) = D$, the bound value is coerced along $\mathrm{flow}(\tau_1, \tau_x)$ to code, $x$ is bound to a fresh variable, and the rule $\mathrm{top}(\tau_x) = D \Rightarrow \mathrm{top}(\tau) = D$ with $\mathrm{flow}(\tau_2, \tau)$ makes the body result code. If $\mathrm{top}(\tau_x) = S$, then $\mathrm{flow}(\tau_1, \tau_x)$ forces $\tau_1 = \tau_x$ at function type and $\mathrm{top}(\tau_1) = S$ at base type, so the bound value is static and fits $\tau_x$. The environment stays good, and the body result is coerced to $\tau$.
- *`if e0 then e1 else e2`.* If the test is $D$, then $\tau$ is $D$ on top, and both branches are coerced to code. If the test is $S$, its result is a boolean constant, by the claim and the simple type of $e_0$, and one branch runs and is coerced to $\tau$.
- *`e1 op e2`.* If the node is $D$, both operands are base values, static constants or code, and both can be made code. If the node is $S$, the rule makes both operands $S$, so they are integer constants, and the operator gives a constant of the right type.

At the root, the environment binds each static input to its constant and each dynamic input to its name. Congruence makes dynamic inputs $D$, and Theorem 1 shows that static inputs stay $S$, so this environment is good. The root result fits the type of $e$. If it is $S$, the root is not a function, by the fact of L6, so it is a constant and can be lifted. $\square$

The proof also shows that every variable is bound either to a static value or to trivial code. So the specializer never copies a residual term that does work, and never drops one: non-trivial code is only placed once, in the term it was built for, or in a residual `let`.

## Theorem 3: the residual program is equivalent to the original

*Calculus.* We use the call-by-value calculus of Plotkin, extended with the constructs of the toy language. Its equality $=_v$ is the least congruence (closed under all term constructors, including under `fun`) that holds the following rules, where $w$ is a value (a constant, a variable, a `fun` or a `fix`):

- $(\texttt{fun } x \to b)\ w =_v b[w/x]$;
- $(\texttt{fix } f\ x \to b)\ w =_v b[(\texttt{fix } f\ x \to b)/f][w/x]$;
- $\texttt{let } x = e_1 \texttt{ in } e_2 =_v (\texttt{fun } x \to e_2)\ e_1$;
- $\texttt{if true then } e_1 \texttt{ else } e_2 =_v e_1$, and the same for false and $e_2$;
- $c_1 \mathbin{op} c_2 =_v c$ when the operator gives $c$ on the constants $c_1, c_2$.

Plotkin proved that $M =_v N$ implies that $M$ and $N$ are operationally equivalent: in every context $C$ that makes both closed, $C[M]$ and $C[N]$ both run forever, or both stop, with the same constant when one of them gives a constant. His proof is for $\beta_v$ and constants with their rules. Each added rule above is a step of the call-by-value semantics whose left side has only values in the positions that are evaluated, which is the form his standardization argument needs, so the result extends to this language. We use it in that form.

*Meaning of a specializer value.* $[\![(D, q)]\!] = q$, $[\![(S, c)]\!] = c$, and $[\![(S, k)]\!]$ is the `fun` or `fix` node of the closure $k$ with each of its free variables $y$ replaced by $[\![\rho_k(y)]\!]$. Each meaning is a value. For a term $e$ and an environment $\rho$, $e[\![\rho]\!]$ is $e$ with each free variable $y$ replaced by $[\![\rho(y)]\!]$. Fresh names of the specializer do not occur in the program, so these substitutions never capture a name. Lifting a constant and coercing do not change the meaning.

*Lemma.* With a congruent annotation and a good environment $\rho$ for $e$, if the specializer on $e$ returns $r$, then $e[\![\rho]\!] =_v [\![r]\!]$.

*Proof.* By induction on the length of the run, with the cases of Theorem 2.

- *Variable, constant, static `fun` or `fix`.* $e[\![\rho]\!]$ and $[\![r]\!]$ are the same term.
- *Dynamic `fun x -> e1`.* After renaming $x$ to the fresh $x'$, $e[\![\rho]\!]$ is $\texttt{fun } x' \to e_1[\![\rho, x \mapsto x']\!]$. By induction the body is $=_v$ to its residual code, and $=_v$ is a congruence under `fun`. A dynamic `fix` is the same.
- *Dynamic application, `let` with a dynamic variable, `if` with a dynamic test, dynamic operator.* The result is the same construct around the results of the parts. By induction each part is $=_v$ to its residual code, and $=_v$ is a congruence.
- *Static application.* By induction $e_1[\![\rho]\!] =_v [\![k]\!]$ and $e_2[\![\rho]\!] =_v [\![r_2]\!]$. Let $k$ be a closure of $\texttt{fun } x \to b$ with environment $\rho_k$, so $[\![k]\!] = \texttt{fun } x \to b[\![\rho_k]\!]$. If the argument is static or trivial, $[\![r_2]\!]$ is a value $w$, and $\beta_v$ gives $(\texttt{fun } x \to b[\![\rho_k]\!])\ w =_v b[\![\rho_k, x \mapsto w]\!]$, which is $=_v$ to the result by induction. Otherwise the result is $\texttt{let } x_2 = q \texttt{ in } q'$ with $q = [\![r_2]\!]$, and by induction $b[\![\rho_k, x \mapsto x_2]\!] =_v q'$. By the `let` rule and renaming, $(\texttt{fun } x \to b[\![\rho_k]\!])\ q =_v \texttt{let } x_2 = q \texttt{ in } b[\![\rho_k, x \mapsto x_2]\!] =_v \texttt{let } x_2 = q \texttt{ in } q'$. No $\beta_v$ step is used on $q$, which need not be a value. For a `fix` closure, the `fix` rule is used in the same way, with $f$ bound to $k$, whose meaning is the `fix` term itself.
- *Static `let x = e1 in e2`.* The bound value $r_1$ is static, so $w = [\![r_1]\!]$ is a value, and by induction $e_1[\![\rho]\!] =_v w$. Then $\texttt{let } x = w \texttt{ in } e_2[\![\rho]\!] =_v e_2[\![\rho, x \mapsto r_1]\!]$ by the `let` rule and $\beta_v$, and this is $=_v [\![r]\!]$ by induction.
- *Static `if`.* By induction the test is $=_v$ to a constant true or false, the `if` rule picks the branch that the specializer runs, and induction applies to that branch.
- *Static operator.* By induction both operands are $=_v$ to constants, and the operator rule gives the constant the specializer computes. $\square$

*Theorem.* Let the annotation be congruent, $\sigma$ the values of the static inputs, and suppose the specializer stops with residual program $r$. Then $e$ with $\sigma$ substituted and $r$ are operationally equivalent. In particular, for every choice $\delta$ of values of the dynamic inputs, $e[\sigma, \delta]$ and $r[\delta]$ both run forever or both stop, with the same constant when the program has base type.

*Proof.* The root environment $\rho_0$ of Theorem 2 is good, and $e[\![\rho_0]\!]$ is $e$ with $\sigma$ substituted and the dynamic inputs left as variables. The lemma gives $e[\![\rho_0]\!] =_v r$, where $r$ is the root code or the lifted root constant. Plotkin's theorem gives operational equivalence. The context that binds the dynamic inputs to $\delta$, for example $(\texttt{fun } d \to [\,])\ \delta$ for one input $d$, gives the second sentence. $\square$

*Remarks.* The theorem says nothing when the specializer does not stop, and it may not stop on a congruent annotation (the loop example of the page). The let insertion is used in exactly one place, the static call with non-trivial code as argument, and the proof shows why: $\beta_v$ needs a value, so binding the code with a `let` is the only step that is sound there.
