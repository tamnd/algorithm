---
tag: 314GEV
kind: definition
slug: substitution
name: Substitution
aliases:
- variable binding map
area: logic-and-constraints/unification-and-resolution
level: intro
summary: A map from variables to terms that changes only finitely many variables, applied to a term by replacing each variable at the same time.
prereqs: [term, subterm]
see_also: [idempotent-substitution, unifier, most-general-unifier, unification-problem, term-matching, standardization-apart, answer-substitution, rewrite-rule]
sources:
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Section 3.1 (terms, substitutions and identities; the subsumption order on substitutions) and Section 4.5 (syntactic unification)
  - book: isbn:9780444508133
    title: Franz Baader and Wayne Snyder, Unification Theory, in J. A. Robinson and A. Voronkov (editors), Handbook of Automated Reasoning, Elsevier and MIT Press, 2001
    locator: Volume I, Chapter 8, Section 2 (syntactic unification; substitutions, composition and the instance order)
  - book: isbn:9783540181997
    title: John W. Lloyd, Foundations of Logic Programming, second edition, Springer, 1987
    locator: Chapter 1, Section 4 (substitutions, unifiers and the unification algorithm)
---

A **substitution** is a map $\sigma$ from [variables](/term/) to [terms](/term/) that is different from the identity on only finitely many variables. It acts on a term by replacing every occurrence of each variable $x$ by $\sigma(x)$, all at the same time. Substitutions are the objects that [unification](/unification-problem/) computes, that [term matching](/term-matching/) and [rewrite rules](/rewrite-rule/) use, and that a Prolog query returns as its [answer](/answer-substitution/).

## Definition

Fix a signature $\Sigma$ of function symbols with arities and a countably infinite set $V$ of variables. $T(\Sigma, V)$ is the set of terms. For a term $t$, $\mathrm{Var}(t)$ is the set of variables in $t$, and $|t|$ is the number of symbol occurrences in $t$ (its number of nodes).

A **substitution** is a function $\sigma : V \to T(\Sigma, V)$ whose **domain**

$$\mathrm{dom}(\sigma) = \{\, x \in V : \sigma(x) \ne x \,\}$$

is finite. Its **range** is $\{\sigma(x) : x \in \mathrm{dom}(\sigma)\}$, and its **variable range** is $\mathrm{vran}(\sigma) = \bigcup_{x \in \mathrm{dom}(\sigma)} \mathrm{Var}(\sigma(x))$. When $\mathrm{dom}(\sigma) = \{x_1, \ldots, x_k\}$ and $\sigma(x_i) = t_i$, we write $\sigma = \{x_1 \mapsto t_1, \ldots, x_k \mapsto t_k\}$. The **identity substitution** $\varepsilon$ has empty domain.

**Application.** A substitution extends to all terms by the homomorphic rule, written in postfix notation $t\sigma$:

$$x\sigma = \sigma(x) \text{ for } x \in V, \qquad f(t_1, \ldots, t_k)\sigma = f(t_1\sigma, \ldots, t_k\sigma).$$

The term $t\sigma$ is an **instance** of $t$. All variables are replaced in one step, so the result does not depend on any order of the bindings.

**Composition.** The composition $\sigma\theta$ means "first $\sigma$, then $\theta$": $x(\sigma\theta) = (x\sigma)\theta$. By induction on $t$, $t(\sigma\theta) = (t\sigma)\theta$ for each term $t$, and composition is associative. It is not commutative. As a finite map,

$$\sigma\theta = \{\, x \mapsto (x\sigma)\theta : x \in \mathrm{dom}(\sigma) \,\} \cup \{\, y \mapsto y\theta : y \in \mathrm{dom}(\theta) \setminus \mathrm{dom}(\sigma) \,\},$$

with the pairs $x \mapsto x$ removed.

**Renaming.** A substitution $\rho$ is a **renaming** when it is a bijection from $V$ to $V$, that is, it maps variables to variables one to one. Then $t\rho$ is a **variant** of $t$.

**Instance order.** $\sigma$ is **more general** than $\theta$, written $\sigma \le \theta$, if $\theta = \sigma\lambda$ for some substitution $\lambda$. This relation is reflexive ($\lambda = \varepsilon$) and transitive ($\theta = \sigma\lambda$ and $\eta = \theta\mu$ give $\eta = \sigma(\lambda\mu)$), so it is a preorder. It is not antisymmetric: $\{x \mapsto y\} \le \{y \mapsto x\}$ and back, by composition with $\{y \mapsto x\}$ and $\{x \mapsto y\}$.

**Size.** The size of a substitution is the total size of its range, $\sum_{x \in \mathrm{dom}(\sigma)} |x\sigma|$. A **triangular** form $\{x_1 \mapsto t_1\}\{x_2 \mapsto t_2\} \cdots \{x_k \mapsto t_k\}$, a composition of single bindings, can be exponentially smaller than the same substitution written as one map.

## Examples and non-examples

**Application is simultaneous.** Let $\sigma = \{x \mapsto y,\ y \mapsto a\}$. Then $f(x, y)\sigma = f(y, a)$, not $f(a, a)$. Applying the bindings one after the other gives the different substitution $\{x \mapsto y\}\{y \mapsto a\} = \{x \mapsto a,\ y \mapsto a\}$.

**Composition is not commutative.** Let $\sigma = \{x \mapsto f(y)\}$ and $\theta = \{y \mapsto b\}$. Then $\sigma\theta = \{x \mapsto f(b),\ y \mapsto b\}$, while $\theta\sigma = \{y \mapsto b,\ x \mapsto f(y)\}$. On the term $g(x)$, the first gives $g(f(b))$ and the second gives $g(f(y))$.

**The domain shrinks when a binding cancels.** Let $\sigma = \{x \mapsto y\}$ and $\theta = \{y \mapsto x\}$. Then $x(\sigma\theta) = y\theta = x$, so the pair $x \mapsto x$ is removed, and $\sigma\theta = \{y \mapsto x\}$.

**Triangular form.** Let $\tau_i = \{x_i \mapsto g(x_{i-1}, x_{i-1})\}$ for $i = 1, \ldots, n$. The composition $\tau_n \tau_{n-1} \cdots \tau_1$ maps $x_n$ to the complete binary tree of $g$ nodes of height $n$ with $2^{n+1} - 1$ nodes, and the full map has size $\sum_{i=1}^{n} (2^{i+1} - 1) = 2^{n+2} - n - 4$, while the triangular form has size $3n$. This is the example of [Robinson's algorithm](/robinson-unification/) and the reason for the [term DAG](/term-dag/).

**Non-examples.**

- The map $x_i \mapsto x_{i+1}$ for all $i \in \mathbb{N}$ changes infinitely many variables, so it is not a substitution in this sense. It is still a function on terms, but it has no finite description as a list of bindings.
- A map that replaces a function symbol, such as $f \mapsto g$, is a signature morphism, not a substitution. Substitutions replace only variables. Replacing function variables is the subject of [higher-order unification](/higher-order-unification-problem/).
- Replacing a subterm that is not a variable, such as $f(a) \mapsto b$, is a rewrite step, not a substitution.

## Related definitions

- A [unifier](/unifier/) of $s$ and $t$ is a substitution $\sigma$ with $s\sigma = t\sigma$. A [most general unifier](/most-general-unifier/) is a least element of the set of unifiers in the instance order.
- A substitution is [idempotent](/idempotent-substitution/) when $\sigma\sigma = \sigma$, which holds exactly when $\mathrm{dom}(\sigma) \cap \mathrm{vran}(\sigma) = \emptyset$.
- [Term matching](/term-matching/) asks for $\sigma$ with $s\sigma = t$: only one side is instantiated.
- [Standardization apart](/standardization-apart/) applies a renaming to a clause so that two clauses share no variables.
- A [term DAG](/term-dag/) stores the range of a substitution with shared subterms.

## References
