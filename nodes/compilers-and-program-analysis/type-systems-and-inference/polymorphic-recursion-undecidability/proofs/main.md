---
title: Typability with polymorphic recursion is equivalent to semi-unification
proves: [statement]
status: sketch
---

This file gives the two reductions between typability in ML with polymorphic recursion and the [semi-unification problem](/semi-unification-problem/), and derives undecidability from the [undecidability of semi-unification](/semi-unification-undecidability/). The reductions follow Henglein (1993) and Kfoury, Tiuryn and Urzyczyn (1993), who prove them in full and show that both run in logarithmic space. The first reduction below is given with its correctness argument. The second is given for systems whose terms are already types. The papers also code an arbitrary signature of function symbols into types, and that coding is not repeated here. This is why the status is sketch.

## Setting

Terms and rules are those of the [Hindley-Milner page](/hindley-milner-type-system/), in syntax-directed form, with T-FixPoly in place of T-Fix:

```text
Gamma, f : Gen(Gamma, tau1 -> tau2), x : tau1 |- e : tau2
---------------------------------------------------------  T-FixPoly
Gamma |- fix f x -> e : tau1 -> tau2
```

Mycroft (1984) states the rule as $\Gamma, f : \sigma \vdash e : \sigma$ for any scheme $\sigma$. The two forms derive the same judgments: from $\sigma = \forall \vec\alpha.\, \tau$ with $\vec\alpha$ not free in $\Gamma$, the scheme $\mathrm{Gen}(\Gamma, \tau)$ is at least as general, and a more general scheme in the context keeps each judgment true.

A *semi-unifier* of a system $\{s_1 \le t_1, \ldots, s_n \le t_n\}$ is a substitution $\sigma$ such that for each $i$ some $\rho_i$ has $s_i\sigma\rho_i = t_i\sigma$. Equations $s \doteq t$ may also appear in a system. They add nothing, since $s \doteq t$ holds under $\sigma$ exactly when $g(z, z) \le g(s, t)$ does, for a fresh $z$ (see the [semi-unification page](/semi-unification-problem/)). We write $\langle a_1, \ldots, a_k \rangle$ for a tuple, coded with a fresh function symbol.

## Reduction 1: from typability to semi-unification

Let $e$ be a closed term. Rename the bound variables so that they are all different. Give each node $u$ of $e$ a type variable $\alpha_u$, and each `fun`-bound variable and each `fix` argument $y$ a type variable $\alpha_y$. Call `let`-bound and `fix`-bound names *polymorphic*. For each polymorphic name, let $b$ be its binding node and $\gamma_b$ the tuple of $\alpha_y$ for the `fun`-bound variables and `fix` arguments in scope at $b$, outside the definition. Let $\delta_b$ be the type of the definition: $\alpha_{e_1}$ for `let x = e1 in e2`, and $\alpha_b$ for `fix f x -> e`. The system $\Sigma(e)$ has:

| node $u$ | constraint |
|---|---|
| a `fun`-bound variable or `fix` argument $y$ | $\alpha_u \doteq \alpha_y$ |
| a constant, `if`, an operator | the equation of its rule, such as $\alpha_u \doteq \mathsf{int}$ for `1` |
| `fun y -> e1` | $\alpha_u \doteq \alpha_y \to \alpha_{e_1}$ |
| `e1 e2` | $\alpha_{e_1} \doteq \alpha_{e_2} \to \alpha_u$ |
| `let x = e1 in e2` | $\alpha_u \doteq \alpha_{e_2}$ |
| `fix f y -> e1` | $\alpha_u \doteq \alpha_y \to \alpha_{e_1}$ |
| a use of a polymorphic name bound at $b$ | $\langle \delta_b, \gamma_b \rangle \le \langle \alpha_u, \gamma_b \rangle$ |

The system has size linear in $|e|$.

**Lemma 1.** $e$ is typable if and only if $\Sigma(e)$ has a semi-unifier. If $\sigma$ is one, then $\sigma\alpha_u$ is a type of the node $u$ in one derivation.

*Proof.* The equations are those of the simply typed calculus, so they hold exactly when the types $\sigma\alpha_u$ fit the rules other than T-Var' for polymorphic names. Consider such a use $u$ of a name bound at $b$. In a derivation, the context at $b$ maps each `fun`-bound variable and `fix` argument $y$ in scope to $\sigma\alpha_y$, and each outer polymorphic name to a scheme. By induction on the nesting of binders, the free variables of these schemes are free in the types $\sigma\alpha_y$ of the variables in scope at the outer binder, so $\mathrm{ftv}(\sigma\Gamma_b) = \mathrm{ftv}(\sigma\gamma_b)$. The T-Var' step at $u$ asks that $\sigma\alpha_u$ is an instance of $\mathrm{Gen}(\sigma\Gamma_b, \sigma\delta_b)$, that is, $\sigma\alpha_u = \sigma\delta_b\,\rho$ for a $\rho$ that does not move the variables of $\sigma\Gamma_b$. The inequality says that $\sigma\delta_b\,\rho = \sigma\alpha_u$ and $\sigma\gamma_b\,\rho = \sigma\gamma_b$. The second equation holds exactly when $\rho$ fixes each variable of $\sigma\gamma_b$. On the variables of $\sigma\delta_b$, the two conditions on $\rho$ are the same. So a derivation gives a semi-unifier, by reading off the types of the nodes, and a semi-unifier gives a derivation, by building it from the leaves up with the types $\sigma\alpha_u$. $\square$

The tuple $\gamma_b$ is the whole trick. It turns the side condition of generalization, "do not touch the variables of the context", into an equation that the residual substitution must satisfy.

## Reduction 2: from semi-unification to typability

Let $\{s_1 \le t_1, \ldots, s_n \le t_n\}$ be a system whose terms are types, built from type variables $v_1, \ldots, v_k$, the arrow, $\mathsf{int}$ and $\mathsf{bool}$, with $k \ge 1$. Use two helper terms:

```text
eq  = fun a -> fun b -> if true then a else b
bot = (fix g y -> g y) 0
```

The type of `eq` is $\alpha \to \alpha \to \alpha$, so `eq a b` forces $a$ and $b$ to have the same type. The term `bot` has a fresh type variable as its type, so it fits any argument position. Both are written out at each use, or bound once with `let`. For a type $t$ over $v_1, \ldots, v_k$, define a term $\mathrm{B}(t)$ with free variables $x_1, \ldots, x_k$:

$$\mathrm{B}(v_j) = x_j \qquad \mathrm{B}(\mathsf{int}) = \texttt{0} \qquad \mathrm{B}(\mathsf{bool}) = \texttt{true}$$

$$\mathrm{B}(t \to t') = \texttt{fun y -> (fun d -> } \mathrm{B}(t') \texttt{) (eq y } \mathrm{B}(t)\texttt{)}$$

If each $x_j$ has the type $\tau_j$, then $\mathrm{B}(t)$ has exactly the type $[v_j := \tau_j]\,t$: the argument `y` is forced to the type of $\mathrm{B}(t)$. Now let

```text
fix f x1 -> fun x2 -> ... -> fun xk ->
  (fun d1 -> ... -> fun dn ->
     fun w1 -> ... -> fun wn -> (fun c1 -> ... -> fun cn -> 0) (eq w1 B(s1)) ... (eq wn B(sn)))
  (f bot ... bot  B(t1) bot ... bot)
  ...
  (f bot ... bot  bot ... bot B(tn))
```

In the $i$-th argument line, `f` gets $k$ copies of `bot`, then $n$ arguments: $\mathrm{B}(t_i)$ at place $i$ and `bot` elsewhere.

**Lemma 2.** This term is typable if and only if the system has a semi-unifier.

*Proof.* Let the type of `f` be $\tau_1 \to \cdots \to \tau_k \to \beta$, with $x_j : \tau_j$, and put $\sigma = [v_j := \tau_j]$. The last line of the body has type $s_1\sigma \to \cdots \to s_n\sigma \to \mathsf{int}$, because each $w_i$ is forced to the type of $\mathrm{B}(s_i)$. So $\beta = s_1\sigma \to \cdots \to s_n\sigma \to \mathsf{int}$. The context outside the `fix` is empty, so T-FixPoly gives `f` the scheme that quantifies all variables of its type. The $i$-th use of `f` takes an instance under some $\rho_i$. The `bot` arguments fit any types. The argument at place $i$ is typable exactly when $s_i\sigma\rho_i = t_i\sigma$, since $\mathrm{B}(t_i)$ has the type $t_i\sigma$. The other parts of the body always have types. So the term is typable exactly when some $\tau_1, \ldots, \tau_k$ and $\rho_1, \ldots, \rho_n$ satisfy all $n$ equations, that is, when $\sigma$ is a semi-unifier. Conversely, a semi-unifier $\sigma$ gives the types $\tau_j = \sigma v_j$. $\square$

The term has size linear in the size of the system, and it uses one polymorphic recursive function.

## Undecidability

Semi-unification is undecidable (Kfoury, Tiuryn and Urzyczyn 1993, Information and Computation), and Reduction 2, together with the coding of signatures in the papers, maps it to typability. So typability with polymorphic recursion is undecidable. Reduction 1 maps typability to semi-unification, whose positive instances can be listed. So typability is semi-decidable: a program can confirm each typable term, and no program can reject each untypable one. $\square$

## References

- Alan Mycroft, Polymorphic type schemes and recursive definitions, International Symposium on Programming, LNCS 167, 1984, pages 217 to 228. The type system with polymorphic recursion.
- Fritz Henglein, Type inference with polymorphic recursion, ACM TOPLAS 15(2), 1993, pages 253 to 289. Both reductions, in log space.
- A. J. Kfoury, J. Tiuryn and P. Urzyczyn, Type reconstruction in the presence of polymorphic recursion, ACM TOPLAS 15(2), 1993, pages 290 to 311. Both reductions, independently.
- A. J. Kfoury, J. Tiuryn and P. Urzyczyn, The undecidability of the semi-unification problem, Information and Computation 102(1), 1993, pages 83 to 101.
