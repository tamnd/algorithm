---
tag: BAMJ4Y
kind: theorem
slug: second-order-unification-undecidability
name: Undecidability of second-order unification
aliases:
- Goldfarb's theorem
area: logic-and-constraints/unification-and-resolution
level: research
summary: No algorithm decides second-order unification, even over one constant and one binary function symbol. Goldfarb proved it in 1981 by encoding Hilbert's tenth problem.
prereqs: [second-order-unification-problem, hilberts-tenth-problem, undecidability, higher-order-unification-problem]
see_also: [higher-order-unification-undecidability, huet-pre-unification, semi-unification-undecidability, undecidability-of-unification-modulo-theories, pattern-unification-problem]
sources:
  - paper: doi:10.1016/0304-3975(81)90040-2
    title: Warren D. Goldfarb, The undecidability of the second-order unification problem, Theoretical Computer Science 13(2), 225 to 230 (1981)
    locator: the whole paper (numerals over g and a, and the encoding of addition and multiplication)
  - paper: doi:10.1145/3372885.3373832
    title: Simon Spies and Yannick Forster, Undecidability of higher-order unification formalised in Coq, Proceedings of the 9th ACM SIGPLAN International Conference on Certified Programs and Proofs (CPP 2020), 143 to 157
    locator: Section 5 (Goldfarb numerals and the single equation for multiplication, which this page follows)
  - paper: "Jordi Levy and Margus Veanes, On the undecidability of second-order unification, Information and Computation 159(1-2), 125 to 150 (2000)"
    locator: the list of known results in the concluding section, and the undecidability with one unary second-order variable
---

Goldfarb's theorem says that second-order unification is undecidable: no algorithm decides whether a set of equations between first-order terms with second-order variables has a solution. Warren Goldfarb proved it in 1981 by a reduction from [Hilbert's tenth problem](/hilberts-tenth-problem/). It strengthens the earlier result of Huet and Lucchesi, which needed [third-order variables](/higher-order-unification-undecidability/). It is the reason why the decidable cases of [second-order unification](/second-order-unification-problem/), such as the monadic case, need strong restrictions.

## Statement

The signature has a base type $\iota$, a constant $a : \iota$ and a function symbol $g : \iota \to \iota \to \iota$. The free variables have types $\iota^k \to \iota$, so they have order at most 2.

**Theorem (Goldfarb 1981).** The second-order unification problem is undecidable, already over the signature $\{a, g\}$.

## In plain words

Numbers can be written as terms: the number $n$ is the function that wraps its input $n$ times in $g(a, \cdot)$. One equation forces an unknown to be such a number and nothing else. Adding numbers is then just doing one after the other. Multiplying is harder, but one equation can force an unknown to list all the steps of the sum $n + n + \cdots + n$, and the last step gives the product. So each polynomial equation over the natural numbers turns into a set of unification equations with the same solutions. No program can decide polynomial equations, so no program can decide second-order unification.

## Proof

We reduce from Hilbert's tenth problem over the natural numbers. Each system of polynomial equations can be rewritten, with new variables for its subterms, into a system with the same solvability in which each equation has one of the forms $x = 1$, $x + y = z$ or $x \cdot y = z$. Such systems are undecidable by the theorem of Matiyasevich, Robinson, Davis and Putnam.

Write $S(t)$ for $g(a, t)$, so $S^n(t) = g(a, g(a, \ldots g(a, t)))$ with $n$ copies of $g$. The *numeral* of $n$ is the term $\lambda z.\, S^n(z) : \iota \to \iota$. In the equations below, $u$ and $v$ are bound variables, so a solution cannot mention them. All terms of type $\iota$ are first-order trees over $a$, $g$, bound variables and free variables applied to arguments, and two such terms are equal only when they are the same tree.

**Lemma 1 (numerals).** A substitution solves $\lambda u.\, X(g(a, u)) \doteq \lambda u.\, g(a, X(u))$ if and only if it maps $X$ to a numeral.

*Proof.* A numeral $\lambda z.\, S^n(z)$ gives $S^n(S(u)) = S^{n+1}(u) = S(S^n(u))$ on both sides. Conversely let $X \mapsto \lambda z.\, t$, so that $t[S(u)/z] = S(t[u/z])$. We show by induction on $t$ that $t = S^n(z)$ for some $n$. If $t = z$, take $n = 0$. If $t = a$, or if the head of $t$ is a free variable, the left side does not start with $g$ but the right side does, so this is impossible. If $t = g(t_1, t_2)$, the equation gives $t_1[S(u)/z] = a$ and $t_2[S(u)/z] = S(t_2[u/z])$. The first forces $t_1 = a$, because $z$ would become $S(u)$ and any other head differs from $a$. The second gives $t_2 = S^m(z)$ by induction, so $t = S^{m+1}(z)$. $\square$

**Constants and addition.** If $X$ is a numeral, then $\lambda u.\, X(u) \doteq \lambda u.\, g(a, u)$ holds exactly when $X$ is the numeral of 1. If $X$, $Y$ and $Z$ are the numerals of $x$, $y$ and $z$, then $\lambda u.\, X(Y(u)) \doteq \lambda u.\, Z(u)$ holds exactly when $S^{x + y}(u) = S^z(u)$, that is, when $x + y = z$.

**Multiplication.** Use $g$ also to build pairs $\langle s, t \rangle = g(s, t)$ and lists $s :: t = g(s, t)$, with $a$ as the empty list. For numerals $M$, $N$, $P$ of $m$, $n$, $p$ and a new variable $G : \iota \to \iota \to \iota \to \iota$, take the pair

$$\lambda u v.\, G(\langle P(u), M(v) \rangle :: a,\ u,\ v) \;\doteq\; \lambda u v.\, \langle u, v \rangle :: G(a,\ N(u),\ S(v)).$$

The idea follows the computation of $m \cdot n$ by repeated addition. The list of pairs $\langle k n, k \rangle$ for $k = 0, 1, \ldots, m$ is the same as the list that starts with $\langle 0, 0 \rangle$ and then adds $\langle n, 1 \rangle$ to each pair of the list. The left side ends the list with $\langle p, m \rangle$. The right side shifts each pair by $\langle n, 1 \rangle$ and puts $\langle 0, 0 \rangle$ in front. Here $u$ and $v$ play the role of 0.

**Lemma 2.** The pair has a solution for $G$ if and only if $p = m n$.

*Proof.* If $p = m n$, let $G \mapsto \lambda r x y.\, \langle x, y \rangle :: \langle S^n x, S y \rangle :: \cdots :: \langle S^{(m-1) n} x, S^{m-1} y \rangle :: r$, a list of $m$ pairs followed by $r$. The left side becomes the list of $\langle S^{k n} u, S^k v \rangle$ for $k = 0, \ldots, m - 1$, followed by $\langle S^p u, S^m v \rangle$. The right side becomes $\langle u, v \rangle$ followed by $\langle S^{k n} u, S^k v \rangle$ for $k = 1, \ldots, m$. Since $p = m n$, the two lists are equal.

Conversely let $G \mapsto \lambda r x y.\, t$, and write $t = h_1 :: h_2 :: \cdots :: h_k :: e$, where $e$ does not start with $g$. So $e$ is $a$, $r$, $x$, $y$, or a term whose head is a free variable. Let $\alpha$ substitute $\langle S^p u, S^m v \rangle :: a$, $u$, $v$ for $r$, $x$, $y$ (the left side), and let $\beta$ substitute $a$, $S^n u$, $S v$ (the right side). The equation says $t\alpha = \langle u, v \rangle :: t\beta$. Compare the two lists, that is, the chains of $g$ along the right edge of the trees.

- If $e = r$, both sides are lists of $k + 1$ elements that end in $a$.
- If $e = a$, the left list has $k$ elements and the right list has $k + 1$.
- If $e = x$, the left side ends in $u$ after $k$ elements, and the right side ends in $u$ after $k + 1 + n$ elements, since $S^n u$ adds $n$ more.
- If $e = y$, the left side ends in $v$ after $k$ elements, the right side after $k + 2$.
- If $e$ has a free variable as head, the two lists end at that head after $k$ and $k + 1$ elements.

So $e = r$, and the elements must match one by one: $h_1 \alpha = \langle u, v \rangle$, $h_{i+1} \alpha = h_i \beta$ for $1 \le i < k$, and $\langle S^p u, S^m v \rangle = h_k \beta$ (if $k = 0$, the last equation is $\langle S^p u, S^m v \rangle = \langle u, v \rangle$).

A sub-claim: if $w\alpha = S^j(u)$, then $w = S^j(x)$; and if $w\alpha = S^j(v)$, then $w = S^j(y)$. For $j = 0$, only $x$ becomes $u$ under $\alpha$: the term $r$ becomes a list whose first element is a pair, not $a$, and the other atoms keep their heads. For $j > 0$, the term $w$ must be $g(w_1, w_2)$ with $w_1 \alpha = a$, so $w_1 = a$, and $w_2 \alpha = S^{j-1}(u)$, so $w_2 = S^{j-1}(x)$ by induction. The case of $v$ is the same.

Now induction on $i$ gives $h_i = \langle S^{(i-1) n} x, S^{i-1} y \rangle$. For $i = 1$ this follows from $h_1\alpha = \langle u, v \rangle$ and the sub-claim. If it holds for $i$, then $h_i \beta = \langle S^{i n} u, S^i v \rangle = h_{i+1} \alpha$, and the sub-claim gives the form of $h_{i+1}$. Finally $h_k \beta = \langle S^{k n} u, S^k v \rangle = \langle S^p u, S^m v \rangle$, so $m = k$ and $p = k n = m n$. This also covers $k = 0$, where $m = p = 0$. $\square$

**The reduction.** Given a system of equations of the three forms in the variables $x_1, \ldots, x_q$, make a free variable $X_i : \iota \to \iota$ for each $x_i$, add the pair of Lemma 1 for each $X_i$, and add the pair for each equation, with a new $G$ for each product. By Lemmas 1 and 2, a unifier gives a solution in the natural numbers (read $x_i$ off the numeral $X_i$), and a solution gives a unifier (take the numerals, and the terms for $G$ from the proof of Lemma 2). All free variables have types $\iota^k \to \iota$, and the only symbols are $a$ and $g$. The pairs can be joined into one pair $\lambda u v.\, g(s_1, g(s_2, \ldots)) \doteq \lambda u v.\, g(t_1, g(t_2, \ldots))$, since $g$ decomposes uniquely. So a decision procedure for second-order unification would decide Hilbert's tenth problem. $\blacksquare$

## Consequences

- **Order 2 is the border.** First-order unification is decidable in linear time, so Goldfarb's theorem places the border of decidability exactly between first and second order.
- **Higher-order unification.** Since second-order problems are higher-order problems, this gives a second proof that [higher-order unification](/higher-order-unification-problem/) is undecidable.
- **Semi-decision only.** Procedures such as [Huet's pre-unification](/huet-pre-unification/), restricted to second order, cannot always stop.
- **Small signatures.** The proof needs only one constant and one binary function symbol. With function symbols of arity at most one (the monadic case), the problem becomes decidable, so the binary symbol is needed.

## Tightness

The theorem is sharp in the order. Many further restrictions keep it undecidable. Levy and Veanes (2000) showed that it stays undecidable with a single second-order variable, which is unary. Farmer (1991) had shown undecidability when all second-order variables are unary. On the other side, monadic second-order unification is decidable (Zhezherun 1979, and Farmer 1988 by reduction to word equations), second-order matching is decidable (Huet and Lang 1978), and second-order unification becomes decidable when the number of occurrences of each bound variable in the solutions is bounded (Schmidt-Schauß). Goldfarb used two equations for multiplication; Spies and Forster (2020) found the single equation used above and checked the proof in Coq.

## History

After the third-order result of Huet and Lucchesi, the second-order case, which is the case used most in practice, stayed open. Goldfarb settled it in 1981 with a short paper in Theoretical Computer Science. His numerals over $g$ and $a$ replace the Church numerals that a third-order proof can use, because second-order variables cannot take functions as arguments. Levy and Veanes (2000) and others then studied how far the problem can be restricted before it becomes decidable.

## References
