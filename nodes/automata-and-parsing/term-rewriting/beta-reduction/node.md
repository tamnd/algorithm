---
tag: 3ZQV0W
kind: definition
slug: beta-reduction
name: Beta-reduction
aliases:
- beta reduction
- lambda reduction
area: automata-and-parsing/term-rewriting
level: core
summary: The rewrite rule (lambda x. M) N -> M[x := N] of the lambda calculus.
prereqs: [lambda-calculus, abstract-reduction-system]
see_also: [church-rosser-theorem, normal-form, outermost-reduction, combinatory-logic, graph-reduction, confluence, standardization-theorem]
sources:
  - book: isbn:9780444875082
    title: Henk P. Barendregt, The Lambda Calculus, Its Syntax and Semantics, revised edition, North-Holland, 1984
    locator: Chapter 2, Conversion (substitution and the beta rule); Chapter 3, Reduction (beta-reduction as the compatible closure of the beta rule, and its confluence)
  - book: isbn:9780521898850
    title: J. Roger Hindley and Jonathan P. Seldin, Lambda-Calculus and Combinators, an Introduction, Cambridge University Press, 2008
    locator: Chapter 1, The lambda-calculus (Sections on substitution, beta-contraction and beta-normal forms)
  - book: isbn:9780521391153
    title: Terese (Marc Bezem, Jan Willem Klop and Roel de Vrijer, editors), Term Rewriting Systems, Cambridge University Press, 2003
    locator: Chapter 10, Lambda calculus
  - paper: "Alonzo Church, An unsolvable problem of elementary number theory, American Journal of Mathematics 58(2) (1936)"
    locator: pp. 345 to 363 (the undecidability of having a normal form)
---

**Beta-reduction** is the single computation rule of the [lambda calculus](/lambda-calculus/): a function $\lambda x.\, M$ applied to an argument $N$ rewrites to the body $M$ with $N$ substituted for $x$. Applied anywhere inside a term, it makes the lambda terms an [abstract reduction system](/abstract-reduction-system/), and running a functional program is reducing a term by beta steps until it reaches a [normal form](/normal-form/). Beta-reduction is [confluent](/confluence/) by the [Church-Rosser theorem](/church-rosser-theorem/) but not terminating, and whether a term has a normal form is undecidable.

## Definition

**Terms.** Let $V$ be a countable set of variables. The lambda terms $\Lambda$ are given by the grammar

$$M, N ::= x \mid (\lambda x.\, M) \mid (M\, N), \qquad x \in V.$$

Application associates to the left, $M\,N\,P = ((M\,N)\,P)$, and the body of $\lambda$ extends as far right as possible. An occurrence of $x$ in $M$ is bound if it lies inside some $\lambda x.\,\ldots$, and free otherwise; $\mathrm{FV}(M)$ is the set of free variables. Terms that differ only in the names of bound variables are identified ($\alpha$-conversion): $\lambda x.\, x = \lambda y.\, y$.

**Substitution.** $M[x := N]$ replaces the free occurrences of $x$ in $M$ by $N$, renaming bound variables of $M$ where needed so that no free variable of $N$ becomes bound:

- $x[x := N] = N$, and $y[x := N] = y$ for $y \ne x$;
- $(P\,Q)[x := N] = (P[x := N])\,(Q[x := N])$;
- $(\lambda x.\, P)[x := N] = \lambda x.\, P$;
- $(\lambda y.\, P)[x := N] = \lambda z.\, P[y := z][x := N]$ for $y \ne x$, where $z = y$ if $y \notin \mathrm{FV}(N)$, and otherwise $z$ is a fresh variable not in $\mathrm{FV}(N) \cup \mathrm{FV}(P)$.

**The rule.** A **beta-redex** is a term of the form $(\lambda x.\, M)\, N$, and its **contractum** is $M[x := N]$. **One-step beta-reduction** $\to_\beta$ is the least relation on $\Lambda$ such that

$$(\lambda x.\, M)\, N \to_\beta M[x := N],$$

and, whenever $M \to_\beta M'$: $\ M\,N \to_\beta M'\,N$, $\ N\,M \to_\beta N\,M'$ and $\lambda x.\, M \to_\beta \lambda x.\, M'$. So a step contracts one redex at any position, including under a $\lambda$. $\twoheadrightarrow_\beta$ (also written $\to_\beta^*$) is its reflexive transitive closure, and $=_\beta$ is beta-conversion, the least equivalence containing $\to_\beta$.

A term is in **beta-normal form** if it has no beta-redex. Then it has the shape $\lambda x_1 \ldots x_n.\, y\, N_1 \cdots N_k$ with each $N_i$ in normal form. A term **has a normal form** if it reduces to one. By the [Church-Rosser theorem](/church-rosser-theorem/), this normal form is unique up to $\alpha$-conversion, and $M =_\beta N$ iff $M$ and $N$ have a common reduct.

**Related rules.** Eta-reduction is $\lambda x.\, M\,x \to_\eta M$ when $x \notin \mathrm{FV}(M)$; $\beta\eta$-reduction uses both. A term is in **weak head normal form** if it is a $\lambda$-abstraction or has the form $x\,N_1 \cdots N_k$; lazy functional languages stop there and do not reduce under $\lambda$.

**As rewriting.** Beta-reduction is not a first-order [term rewriting system](/term-rewriting-system/), because the rule binds variables and its right-hand side uses substitution. [Combinatory logic](/combinatory-logic/) is a first-order system with the same computing power, and higher-order rewriting systems generalize beta-reduction.

## Examples and non-examples

**Church numerals.** Let $\underline{n} = \lambda f.\, \lambda x.\, f^n\, x$, so $\underline{1} = \lambda f.\, \lambda x.\, f\,x$ and $\underline{2} = \lambda f.\, \lambda x.\, f\,(f\,x)$, and let $\mathit{add} = \lambda m.\, \lambda n.\, \lambda f.\, \lambda x.\, m\,f\,(n\,f\,x)$. Always contracting the leftmost outermost redex:

$$
\begin{aligned}
\mathit{add}\ \underline{1}\ \underline{1}
&\to_\beta (\lambda n.\, \lambda f.\, \lambda x.\, \underline{1}\,f\,(n\,f\,x))\ \underline{1}
\to_\beta \lambda f.\, \lambda x.\, \underline{1}\,f\,(\underline{1}\,f\,x) \\
&\to_\beta \lambda f.\, \lambda x.\, (\lambda x'.\, f\,x')\,(\underline{1}\,f\,x)
\to_\beta \lambda f.\, \lambda x.\, f\,(\underline{1}\,f\,x) \\
&\to_\beta \lambda f.\, \lambda x.\, f\,((\lambda x'.\, f\,x')\,x)
\to_\beta \lambda f.\, \lambda x.\, f\,(f\,x) = \underline{2}.
\end{aligned}
$$

That is six steps to the normal form $\underline{2}$. The third step renames the bound $x$ of $\underline{1}$ to $x'$ only for readability; here no capture can happen.

**Duplication.** $(\lambda x.\, x\,x)\,(\lambda y.\, y) \to_\beta (\lambda y.\, y)\,(\lambda y.\, y) \to_\beta \lambda y.\, y$. The argument is copied before it is used, which is the reason why [graph reduction](/graph-reduction/) shares it instead.

**No normal form.** $\Omega = (\lambda x.\, x\,x)\,(\lambda x.\, x\,x)$ reduces in one step to itself, and to nothing else. So beta-reduction is not terminating.

**The strategy matters.** Let $K = \lambda x.\, \lambda y.\, x$ and $I = \lambda z.\, z$. The term $K\,I\,\Omega$ reduces to $I$ in two steps by contracting the leftmost outermost redex: $K\,I\,\Omega \to_\beta (\lambda y.\, I)\,\Omega \to_\beta I$. Contracting the redex $\Omega$ inside the argument instead loops forever. So $K\,I\,\Omega$ has a normal form, but not every reduction reaches it; [outermost reduction](/outermost-reduction/) (normal order) always does when a normal form exists, by the [standardization theorem](/standardization-theorem/).

**Capture.** $(\lambda x.\, \lambda y.\, x)\, y \to_\beta \lambda y'.\, y$, a constant function that returns the free $y$. The naive result $\lambda y.\, y$, the identity, would be wrong: the free $y$ of the argument would be captured. This is the main pitfall of implementing beta-reduction by textual replacement, and de Bruijn indices avoid it by replacing names with binder distances.

**Non-example: a term that is not a redex.** $x\,(\lambda y.\, y)$ is an application, but its function part is a variable, so it is not a beta-redex, and it is in normal form. $(\lambda x.\, x)$ alone is an abstraction, not a redex.

**Non-example: eta is not beta.** $\lambda x.\, f\,x$ is in beta-normal form; only the eta rule reduces it to $f$.

## Related definitions

- The [Church-Rosser theorem](/church-rosser-theorem/) states that $\to_\beta$ is [confluent](/confluence/), so normal forms are unique.
- [Outermost reduction](/outermost-reduction/) (normal order) finds the normal form whenever there is one, and [innermost reduction](/innermost-reduction/) corresponds to call-by-value; the [standardization theorem](/standardization-theorem/) is behind the first claim.
- [Combinatory logic](/combinatory-logic/) replaces $\lambda$ and substitution by the two first-order rules of $S$ and $K$.
- [Graph reduction](/graph-reduction/) implements beta-reduction with sharing, so an argument copied by a redex is reduced at most once.
- In the simply typed lambda calculus, beta-reduction terminates; in the untyped calculus, having a normal form is undecidable, as Church showed in 1936.

## References
