---
title: The nominal unification rules find a most general solution or fail correctly
proves: [correctness]
status: full
---

We use the definitions of the problem page. A *problem* is a pair $(E, F)$ of equations and freshness problems. A pair $(\nabla', \theta)$ *solves* it if $\nabla' \vdash \theta(t) \approx \theta(u)$ for each $t \approx^? u$ in $E$ and $\nabla' \vdash a \# \theta(t)$ for each $a \#^? t$ in $F$. We write $U(E, F)$ for the set of solutions.

## Facts about nominal terms

The proof uses the following facts, which Urban, Pitts and Gabbay prove by induction on the rules of $\approx$ and $\#$ (Section 2 of their paper).

- **(F1)** Under each $\nabla$, the relation $\approx$ is an equivalence relation, and it is a congruence for $f(\ldots)$ and $[a]\cdot$.
- **(F2)** Permutations preserve the judgments: $\nabla \vdash t \approx u$ iff $\nabla \vdash \pi \cdot t \approx \pi \cdot u$, and $\nabla \vdash a \# t$ iff $\nabla \vdash \pi(a) \# \pi \cdot t$.
- **(F3)** If $\nabla \vdash t \approx u$, then $\nabla \vdash a \# t$ iff $\nabla \vdash a \# u$.
- **(F4)** $\nabla \vdash \pi \cdot t \approx \pi' \cdot t$ iff $\nabla \vdash a \# t$ for each $a \in ds(\pi, \pi')$.
- **(F5)** Substitution commutes with permutations: $\theta(\pi \cdot t) = \pi \cdot \theta(t)$. If $\nabla' \vdash \theta(X) \approx \theta'(X)$ for each variable $X$, then $\nabla' \vdash \theta(t) \approx \theta'(t)$ for each term $t$, and the same freshness facts hold for $\theta(t)$ and $\theta'(t)$.
- **(F6)** The rules of $\approx$ and $\#$ are syntax-directed. So $\nabla \vdash [a]t \approx [a]u$ iff $\nabla \vdash t \approx u$; $\nabla \vdash [a]t \approx [b]u$ with $a \neq b$ iff $\nabla \vdash t \approx (a\ b) \cdot u$ and $\nabla \vdash a \# u$; $\nabla \vdash f(\bar t) \approx f(\bar u)$ iff the arguments are pairwise equivalent; and two terms whose top constructors differ (atom, abstraction, function symbol, or two different atoms or symbols) are never equivalent. Also $\nabla \vdash a \# b$ iff $a \neq b$, $\nabla \vdash a \# [a]t$ always, $\nabla \vdash a \# [b]t$ iff $\nabla \vdash a \# t$ for $b \neq a$, and $\nabla \vdash a \# f(\bar t)$ iff $\nabla \vdash a \# t_i$ for each $i$.
- **(F7)** $\nabla \vdash a \# \pi \cdot X$ iff $\pi^{-1}(a) \# X \in \nabla$.

A permutation does not change the size of a term, and the size of $\theta(t)$ is at least the size of $t$.

## Lemma 1: the steps of the first phase keep the solutions

Let one iteration of lines L3 to L10 turn $(E, F)$ with substitution $\sigma$ into $(E', F')$ with substitution $\sigma'$.

- **Lines L4 to L9.** Here $\sigma' = \sigma$ and $U(E, F) = U(E', F')$. For line L4 this is clear. For lines L6, L7 and L8 it is (F6) applied to $\theta(t)$ and $\theta(u)$, together with (F5) for $\theta((a\ b) \cdot u') = (a\ b) \cdot \theta(u')$. For line L9, $\theta(\pi \cdot X) = \pi \cdot \theta(X)$ and $\theta(\pi' \cdot X) = \pi' \cdot \theta(X)$, so (F4) says that the equation holds iff $\nabla' \vdash a \# \theta(X)$ for each $a \in ds(\pi, \pi')$. These are the new freshness problems.
- **Line L10.** Let the equation be $\pi \cdot X \approx^? s$, with $X$ not in $s$, and $\rho = [X := \pi^{-1} \cdot s]$. If $(\nabla', \theta)$ solves $(E, F)$, then $\nabla' \vdash \pi \cdot \theta(X) \approx \theta(s)$, and by (F2) $\nabla' \vdash \theta(X) \approx \pi^{-1} \cdot \theta(s) = \theta(\rho(X))$. On other variables $\theta$ and $\theta \circ \rho$ agree. So by (F5), $\theta$ and $\theta \circ \rho$ give equivalent terms with the same freshness facts, and $(\nabla', \theta)$ solves $(\rho(E'), \rho(F))$ iff $(\nabla', \theta \circ \rho)$ does. Conversely, if $(\nabla', \theta)$ solves $(\rho(E \setminus \{e\}), \rho(F))$, then $(\nabla', \theta \circ \rho)$ solves $(E, F)$: the equation $e$ holds because $\theta(\rho(\pi \cdot X)) = \pi \cdot \pi^{-1} \cdot \theta(s) \approx \theta(s) = \theta(\rho(s))$, since $X$ is not in $s$.

So in each case, the solutions of the original input are exactly the pairs $(\nabla', \theta)$ such that $(\nabla', \theta)$ solves the current problem and $\nabla' \vdash \theta(\sigma(X)) \approx \theta(X)$ for each variable $X$. We call this the *invariant*. It holds at the start with $\sigma$ the identity, and the cases above show that each step keeps it. Here we use that $\sigma$ is idempotent: its domain variables do not occur in $E$, $F$ or its range, because line L10 applies $\rho$ to all three and $X$ does not occur in $s$.

## Lemma 2: failure is correct

- **Line L5.** Two different atoms are not equivalent, by (F6).
- **Line L11.** The two sides have different top constructors, or different function symbols or arities, and neither is a suspension, so (F6) says that no instance is equivalent. Or one side is $\pi \cdot X$ and $X$ occurs in the other side $s$ but $s$ is not a suspension of $X$. Then $\theta(s)$ contains $\theta(X)$ as a proper subterm, up to a permutation, so it is strictly larger than $\pi \cdot \theta(X)$. Equivalent terms have the same size, so there is no solution.
- **Line L14.** The problem $a \#^? a$ has no solution, by (F6).

Since every step keeps the solutions (Lemma 1, and Lemma 3 below for the second phase), a failure means that the input has no solution.

## Lemma 3: the steps of the second phase keep the solutions

At line L12 the set $E$ is empty. Lines L14 to L17 replace a freshness problem by problems with the same solutions, by (F6). Line L18 replaces $a \#^? \pi \cdot X$ by the constraint $\pi^{-1}(a) \# X$: by (F2), a pair $(\nabla', \theta)$ solves the first iff $\nabla' \vdash \pi^{-1}(a) \# \theta(X)$. At the end, $(\nabla', \theta)$ solves the input iff $\nabla' \vdash b \# \theta(X)$ for each $b \# X \in \nabla$ and $\nabla' \vdash \theta(\sigma(X)) \approx \theta(X)$ for each $X$. We write $\nabla' \vdash \theta(\nabla)$ for the first condition.

## Theorem

The algorithm terminates. If it returns $(\nabla, \sigma)$, then $(\nabla, \sigma)$ is a most general solution. If it fails, there is no solution.

*Proof.* **Termination.** In the first phase, take the pair (number of distinct variables in $E$, total size of $E$), ordered lexicographically. Line L10 removes $X$ from $E$, since $X$ is not in $\pi^{-1} \cdot s$, and adds no variable, so the first number drops. Lines L4 and L9 remove an equation and add none. Lines L6, L7 and L8 replace an equation by equations of smaller total size; in line L8, $(a\ b) \cdot u'$ has the size of $u'$. So the size drops and the variables do not grow. In the second phase each step replaces a problem $a \#^? t$ by problems on proper subterms of $t$, or removes it. So the total size of $F$ drops.

**Failure.** This is Lemma 2.

**Soundness.** Apply Lemma 3 with $\nabla' = \nabla$ and $\theta = \sigma$. First, $\nabla \vdash \sigma(\nabla)$: each constraint in $\nabla$ is $b \# X$ for a variable $X$ that is not in the domain of $\sigma$, because line L10 applied $\sigma$ to $F$ before the constraint was made, so $\sigma(X) = X$ and $b \# X \in \nabla$. Second, $\sigma(\sigma(X)) = \sigma(X)$, since $\sigma$ is idempotent, and $\approx$ is reflexive by (F1). So $(\nabla, \sigma)$ solves the input.

**Most general.** Let $(\nabla', \theta)$ be any solution. By Lemma 3, $\nabla' \vdash \theta(\nabla)$ and $\nabla' \vdash \theta(\sigma(X)) \approx \theta(X)$ for each $X$. So $\tau = \theta$ shows that $(\nabla, \sigma)$ is more general than $(\nabla', \theta)$. $\blacksquare$

The tests check this on random problems: for problems made by instantiating a term $s$ with a ground $\theta$ and renaming the binders, the algorithm must succeed, $\theta$ must satisfy $\nabla$, and $\theta(\sigma(X))$ must be α-equivalent to $\theta(X)$. For one-variable problems, a search over all small ground terms checks that the algorithm never fails when a solution exists. For ground terms, success must agree with α-equivalence computed by de Bruijn indices.
