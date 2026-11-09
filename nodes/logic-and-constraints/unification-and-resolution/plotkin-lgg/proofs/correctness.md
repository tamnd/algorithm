---
title: Plotkin's algorithm returns a least general generalization, unique up to renaming, in linear time
proves: [correctness]
status: full
---

We use the notation of the page. For terms, $h \le g$ means that $g = h\lambda$ for some substitution $\lambda$: $g$ is an instance of $h$, and $h$ is at least as general. A **generalization** of $s$ and $t$ is a term $h$ with $h\eta_1 = s$ and $h\eta_2 = t$ for some substitutions $\eta_1, \eta_2$. A **least general generalization** (lgg) is a generalization $g$ with $h \le g$ for every generalization $h$. Two terms have the same **head** when both are the same variable, or both have the same function symbol and arity. The variables of $s$ and $t$ are not bound by the algorithm. The new variables $z$ that L6 makes do not occur in $s$ or $t$.

## The function A

In one run, let $A(a, b)$ be the result of the call on the pair $(a, b)$ of subterms. The table $M$ of L1 makes $A$ a function of the pair: if the heads of $a$ and $b$ differ, the first call on $(a, b)$ makes a new variable $z_{a,b}$ (L6), and every later call returns the same $z_{a,b}$ (L5). If the heads agree, $A(a, b) = f(A(a_1, b_1), \ldots, A(a_k, b_k))$ (L3, L4), or the common variable or constant when $k = 0$. By induction on the size of $a$, each pair gets one value. Also $\theta_1(z_{a,b}) = a$ and $\theta_2(z_{a,b}) = b$, and two different pairs get two different variables.

The run visits the pair $(s|_p, t|_p)$ for each position $p$ such that $s$ and $t$ have the same head at every proper prefix of $p$. This follows from L4 by induction on the length of $p$.

## Lemma 1: the output is a generalization

For every visited pair, $A(a, b)\theta_1 = a$ and $A(a, b)\theta_2 = b$.

*Proof.* By induction on the size of $a$. If the heads differ, $A(a, b) = z_{a,b}$ and $z_{a,b}\theta_1 = a$, $z_{a,b}\theta_2 = b$. If $a$ and $b$ are the same variable $x$, then $A(a, b) = x$, and $x\theta_1 = x$ because $\theta_1$ binds only new variables. A common constant is fixed in the same way. If $a = f(a_1, \ldots, a_k)$ and $b = f(b_1, \ldots, b_k)$, then $A(a, b)\theta_1 = f(A(a_1, b_1)\theta_1, \ldots) = f(a_1, \ldots, a_k) = a$ by induction, and the same for $\theta_2$. $\square$

So $g = A(s, t)$ satisfies $g\theta_1 = s$ and $g\theta_2 = t$.

## Lemma 2: the output is least general

Let $h$ be a generalization of $s$ and $t$, with $h\eta_1 = s$ and $h\eta_2 = t$. Then $h\lambda = g$ for the substitution

$$\lambda = \{y \mapsto A(y\eta_1, y\eta_2) : y \in \mathrm{Var}(h)\}.$$

*Proof.* First, $\lambda$ is well defined. Let $y$ occur in $h$ at a position $p$. Every proper prefix of $p$ is a function position of $h$, so $s = h\eta_1$ and $t = h\eta_2$ have the same head there. So the pair $(s|_p, t|_p) = (y\eta_1, y\eta_2)$ is visited, and $A(y\eta_1, y\eta_2)$ is a value of the run. Different positions of $y$ give the same pair, so the same value.

Now show $h'\lambda = A(h'\eta_1, h'\eta_2)$ for each subterm $h'$ of $h$, by induction on $h'$. For a variable $y$, this is the definition of $\lambda$. For $h' = f(h_1, \ldots, h_k)$, the terms $h'\eta_1 = f(h_1\eta_1, \ldots, h_k\eta_1)$ and $h'\eta_2 = f(h_1\eta_2, \ldots, h_k\eta_2)$ have the same head $f$, so

$$A(h'\eta_1, h'\eta_2) = f(A(h_1\eta_1, h_1\eta_2), \ldots, A(h_k\eta_1, h_k\eta_2)) = f(h_1\lambda, \ldots, h_k\lambda) = h'\lambda.$$

For $h' = h$ this gives $h\lambda = A(s, t) = g$, so $h \le g$. $\square$

The memo table is essential here. Without it, two positions with the same pair $(a, b)$ could get two different variables, and a generalization $h$ that uses one variable $y$ at both positions would not be more general than the output.

## Lemma 3: uniqueness up to renaming

If $g$ and $g'$ are both lggs of $s$ and $t$, then $g' = g\rho$ for a substitution $\rho$ that maps the variables of $g$ one to one onto the variables of $g'$.

*Proof.* Both are lggs, so $g' = g\lambda$ and $g = g'\lambda'$. Let $|u|$ be the number of symbol occurrences of $u$. Applying a substitution never makes a term smaller, so $|g| \le |g'| \le |g|$, and both applications keep the size. So $\lambda$ maps each variable of $g$ to a term of size 1, that is, to a variable or a constant. It cannot map a variable $y$ to a constant $c$: then $g'\lambda'$ would have $c$ at a position where $g$ has $y$. So $\lambda$ maps variables of $g$ to variables. If $\lambda$ mapped two variables $y \ne y'$ of $g$ to the same variable, then $g = g'\lambda'$ would have one term at the positions of $y$ and of $y'$, which is false. So $\rho = \lambda$ restricted to $\mathrm{Var}(g)$ is a one-to-one map of variables. $\square$

## Termination and time

Every call on a pair with the same head makes calls only on pairs of proper subterms, so the recursion ends. The visited pairs correspond to a set of positions that are positions of both $s$ and $t$, so there are at most $\min(|s|, |t|)$ of them.

With hash consing, each subterm of $s$ and $t$ gets a node number in $O(|s| + |t|)$ expected time, and two subterms are equal exactly when their numbers are equal. The key of $M$ is then a pair of numbers, so L5 and L6 take $O(1)$ expected time. Each visited pair with arity $k$ costs $O(k)$ to make the $k$ child calls and to build the output node, and the sum of the arities of the visited pairs is less than the number of visited pairs plus one. So the run takes $O(|s| + |t|)$ expected time and space, and the output has at most $\min(|s|, |t|)$ symbols. $\blacksquare$
