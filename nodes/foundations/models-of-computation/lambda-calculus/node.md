---
tag: QPGDRA
kind: model
slug: lambda-calculus
name: Lambda calculus
aliases:
- lambda calculus model
- untyped lambda calculus
area: foundations/models-of-computation
level: core
summary: Formal system of function abstraction and application, equivalent in power to Turing machines.
prereqs: []
see_also: [turing-machine, church-turing-thesis, beta-reduction, church-rosser-theorem, turing-completeness, halting-problem]
sources:
  - book: isbn:9780444875082
    title: "Henk P. Barendregt, The Lambda Calculus: Its Syntax and Semantics, revised edition"
    locator: Chapters 2, 3, 6 and 13
  - paper: "Beniamino Accattoli, Ugo Dal Lago and Gabriele Vanoni, Reasonable space for the lambda-calculus, logarithmically, 37th Annual ACM/IEEE Symposium on Logic in Computer Science (LICS 2022)"
  - paper: "Stephen C. Kleene and J. Barkley Rosser, The inconsistency of certain formal logics, Annals of Mathematics 36(3) (1935), 630 to 636"
  - paper: "Yannick Forster, Fabian Kunze and Marc Roth, The weak call-by-value lambda-calculus is reasonable for both time and space, Proceedings of the ACM on Programming Languages 4 (POPL 2020), article 27"
  - paper: "Ugo Dal Lago and Simone Martini, The weak lambda calculus as a reasonable machine, Theoretical Computer Science 398 (2008), 32 to 50"
  - paper: "William W. Tait, Intensional interpretations of functionals of finite type I, Journal of Symbolic Logic 32(2) (1967), 198 to 212"
  - paper: "Helmut Schwichtenberg, Definierbare Funktionen im Lambda-Kalkul mit Typen, Archiv fur mathematische Logik und Grundlagenforschung 17 (1976), 113 to 114"
  - paper: "Moses Schonfinkel, Uber die Bausteine der mathematischen Logik, Mathematische Annalen 92 (1924), 305 to 316"
  - paper: "Haskell B. Curry, Grundlagen der kombinatorischen Logik, American Journal of Mathematics 52 (1930), 509 to 536 and 789 to 834"
  - paper: "Alonzo Church, A set of postulates for the foundation of logic, Annals of Mathematics 33(2) (1932), 346 to 366"
  - paper: "Stephen C. Kleene, Lambda-definability and recursiveness, Duke Mathematical Journal 2(2) (1936), 340 to 353"
  - paper: "Alonzo Church, An unsolvable problem of elementary number theory, American Journal of Mathematics 58(2) (1936), 345 to 363"
  - paper: "Alan M. Turing, Computability and lambda-definability, Journal of Symbolic Logic 2(4) (1937), 153 to 163"
  - paper: "Beniamino Accattoli and Ugo Dal Lago, (Leftmost-outermost) beta reduction is invariant, indeed, Logical Methods in Computer Science 12(1:4) (2016), doi 10.2168/LMCS-12(1:4)2016"
---

The lambda calculus is a formal system in which every object is a function. A term is a variable, a function written $\lambda x.M$, or the application $MN$ of one term to another, and the only rule of computation is [beta reduction](/beta-reduction/). Church introduced it in the early 1930s as part of a system of logic. Kleene and Rosser (1935) showed that the full logic was inconsistent, and the pure calculus of functions given here is the part that survived. It computes exactly the functions on the natural numbers that a [Turing machine](/turing-machine/) computes, and it is the base of functional programming languages. The number of beta steps depends on the reduction strategy, and terms can grow exponentially. With leftmost-outermost reduction and terms that share subterms, the count is a fair measure of time (Accattoli and Dal Lago 2016).

## The machine

### Terms

Fix an infinite set of variables. The set $\Lambda$ of *terms* is the smallest set with these rules.

- A variable $x$ is a term.
- If $M$ is a term and $x$ is a variable, then the *abstraction* $\lambda x.M$ is a term. It is the function with parameter $x$ and body $M$.
- If $M$ and $N$ are terms, then the *application* $(MN)$ is a term. It applies $M$ to $N$.

Two conventions drop parentheses: application associates to the left, so $MNP$ means $((MN)P)$, and the body of an abstraction extends as far to the right as possible. The notation $\lambda xy.M$ means $\lambda x.\lambda y.M$.

The *free variables* $\mathrm{FV}(M)$ are defined by $\mathrm{FV}(x) = \{x\}$, $\mathrm{FV}(MN) = \mathrm{FV}(M) \cup \mathrm{FV}(N)$ and $\mathrm{FV}(\lambda x.M) = \mathrm{FV}(M) \setminus \{x\}$. A term with no free variable is *closed*. Terms that differ only in the names of bound variables are identified ($\alpha$-equivalence), so $\lambda x.x$ and $\lambda y.y$ are the same term.

### Substitution and beta reduction

The term $M[x := N]$ is $M$ with $N$ in place of each free occurrence of $x$. It is defined by recursion on $M$.

- $x[x := N] = N$, and $y[x := N] = y$ for a variable $y \ne x$.
- $(PQ)[x := N] = P[x := N]\,Q[x := N]$.
- $(\lambda x.P)[x := N] = \lambda x.P$.
- $(\lambda y.P)[x := N] = \lambda y.(P[x := N])$ for $y \ne x$ and $y \notin \mathrm{FV}(N)$. If $y \in \mathrm{FV}(N)$, rename $y$ in $\lambda y.P$ first, so that no free variable of $N$ is captured.

A *beta step* replaces a *redex* $(\lambda x.M)N$ by $M[x := N]$. This step is written $(\lambda x.M)N \to_\beta M[x := N]$, and the relation $\to_\beta$ applies it to any subterm. The *eta rule* $\lambda x.Mx \to_\eta M$, for $x \notin \mathrm{FV}(M)$, is often added to beta. It makes equality extensional (the theory $\lambda\eta$). The pure system uses only beta, and this page does the same. A term with no redex is in *normal form*. The relation $\to_\beta^*$ is the reflexive and transitive closure of $\to_\beta$. Beta-equality $=_\beta$ is the least equivalence relation that contains $\to_\beta$. By the Church-Rosser theorem below, $M =_\beta N$ if and only if $M$ and $N$ reduce to a common term.

A term can have several redexes, and the choice of redex is a *reduction strategy*. The *leftmost-outermost* strategy always contracts the redex that starts leftmost in the written term. This redex is outermost. The [Church-Rosser theorem](/church-rosser-theorem/) says that if $M \to_\beta^* N_1$ and $M \to_\beta^* N_2$, then some $L$ satisfies $N_1 \to_\beta^* L$ and $N_2 \to_\beta^* L$. So a term has at most one normal form, up to $\alpha$-equivalence. Not every term has one: for $\Omega = (\lambda x.xx)(\lambda x.xx)$ we have $\Omega \to_\beta \Omega$, and $\Omega$ has no normal form.

### Church numerals

The *Church numeral* of a natural number $n$ is the closed term
$$c_n = \lambda f.\lambda x.\,f^n x,$$
where $f^n x$ means $f(f(\cdots(f\,x)\cdots))$ with $n$ copies of $f$. So $c_0 = \lambda fx.x$, $c_1 = \lambda fx.fx$ and $c_2 = \lambda fx.f(fx)$. The numeral $c_n$ takes a function $f$ and returns the $n$-fold composition of $f$. Two terms compute arithmetic:
$$\mathrm{SUCC} = \lambda n f x.\,f(n f x), \qquad \mathrm{ADD} = \lambda m n f x.\,m f (n f x).$$

Worked example: $\mathrm{SUCC}\, c_1$ reduces to $c_2$. The term $c_1$ is closed, so no variable is captured.
$$\begin{aligned}
\mathrm{SUCC}\, c_1 &= (\lambda n f x.\,f(n f x))\,(\lambda f x.\,f x) \\
&\to_\beta \lambda f x.\,f\big((\lambda f x.\,f x)\,f\,x\big) \\
&\to_\beta \lambda f x.\,f\big((\lambda x.\,f x)\,x\big) \\
&\to_\beta \lambda f x.\,f(f x) = c_2.
\end{aligned}$$
The first step replaces $n$ by $c_1$. The second applies $\lambda f x.\,fx$ to $f$, and the third applies $\lambda x.\,fx$ to $x$. The result is in normal form.

In general, two steps give $\mathrm{ADD}\,c_m\,c_n \to_\beta^* \lambda f x.\,c_m f (c_n f x)$. Inside the body, $c_n f x \to_\beta^* f^n x$ and then $c_m f (f^n x) \to_\beta^* f^m(f^n x) = f^{m+n} x$. So $\mathrm{ADD}\,c_m\,c_n \to_\beta^* c_{m+n}$.

### Recursion

The term $Y = \lambda g.\,(\lambda x.\,g(xx))(\lambda x.\,g(xx))$ satisfies $Y g =_\beta g(Yg)$ for each term $g$. To show it, let $A = \lambda x.\,g(xx)$. Then $Yg \to_\beta AA$, and $AA \to_\beta g(AA)$. Also $g(Yg) \to_\beta g(AA)$. So $Yg$ and $g(Yg)$ reduce to terms that both reduce to $g(AA)$, and the two are beta-equal. The term $Y$ is Curry's fixed-point combinator. The term $Yg$ is only beta-equal to $g(Yg)$: it does not reduce to it. Turing's combinator $\Theta = (\lambda xy.\,y(xxy))(\lambda xy.\,y(xxy))$ satisfies $\Theta g \to_\beta^* g(\Theta g)$. With such a combinator, a term can call itself, which gives recursion without a name for the function.

### State and unit of time

The whole state of a computation is the current term. There is no separate memory. One beta step is the unit of time. The next section explains when this count is a fair measure, for example under leftmost-outermost reduction with shared subterms.

## What it counts

The natural measure of time is the number of beta steps from a term to its normal form. The measure depends on the strategy. It also fails to count the work of one step: a step copies the argument $N$ into each occurrence of $x$, and $N$ can be large.

The natural measure of space is the largest size of a term during the reduction. Space depends on the strategy too. Forster, Kunze and Roth (2020) proved that for weak call-by-value reduction, which does not reduce under an abstraction, the largest term size is a reasonable space measure, at the same time as the step count is a reasonable time measure. Sublinear space, such as logarithmic space, cannot be measured by term size, since the term itself is at least as large as the input. It needs an abstract machine with pointers (Accattoli, Dal Lago and Vanoni 2022).

Here is an example. Let $f$ and $a$ be free variables, and define $u_0 = a$ and $u_{k+1} = (\lambda x.\,f x x)\,u_k$. The term $u_k$ has size $O(k)$. Its normal form is $n_k$, where $n_0 = a$ and $n_{k+1} = f\, n_k\, n_k$. So $n_k$ contains $2^k$ copies of $a$, and its size is exponential in the size of $u_k$.

- The leftmost-outermost strategy contracts the outer redex of $u_{k+1}$ first. This gives $f\,u_k\,u_k$, and then each copy of $u_k$ needs its own reduction. The number of steps $T(k)$ satisfies $T(0) = 0$ and $T(k+1) = 1 + 2T(k)$, so $T(k) = 2^k - 1$.
- A strategy that reduces the argument $u_k$ first needs $k$ steps in total: one for each $\lambda x.\,f x x$ redex.

The number of steps goes from $2^k - 1$ to $k$ by a change of strategy. This is the first problem with counting beta steps. The second problem is size explosion: under the second strategy, $k$ unit-cost steps produce a term with $2^k$ copies of $a$, so no machine can write out the result of those $k$ steps as an ordinary term in time polynomial in $k$. A machine that shares subterms can still do the $k$ steps in polynomial time. Other families show the same size explosion under leftmost-outermost reduction. A cost that counts each beta step as one unit is therefore not a fair measure of the time of a machine. Accattoli and Dal Lago (2016) proved that the number of leftmost-outermost beta steps is a *reasonable* cost: a Turing machine can compute a shared representation of the normal form, which is a graph with explicit substitutions, in time polynomial in this number and in the size of the term. The normal form written out in full can be exponentially larger, even under leftmost-outermost reduction. In the other direction, a Turing machine that runs in time $t$ can be simulated in the lambda calculus with a number of leftmost-outermost steps polynomial in $t$. This direction is older (see Dal Lago and Martini 2008 for weak reduction, and the discussion in Accattoli and Dal Lago 2016).

## Relation to other models

- Lambda calculus and [Turing machines](/turing-machine/) compute the same functions on the natural numbers. A total function $f : \mathbb{N}^k \to \mathbb{N}$ is *lambda-definable* when some closed term $F$ satisfies $F\,c_{n_1} \cdots c_{n_k} =_\beta c_{f(n_1,\dots,n_k)}$ for all $n_1,\dots,n_k \in \mathbb{N}$. A total function is lambda-definable if and only if it is computable by a Turing machine. Kleene (1936) proved that the lambda-definable functions are exactly the general recursive functions, and Turing (1937) proved that they are exactly the Turing computable functions. Barendregt, Chapter 6, treats the representation of recursive functions. This fact is evidence for the [Church-Turing thesis](/church-turing-thesis/), which says that these functions are the ones that an algorithm can compute.
- A programming language that can express the lambda calculus is [Turing complete](/turing-completeness/).
- Combinatory logic (Schonfinkel 1924, Curry 1930) has the combinators $S$ and $K$ with $Kxy \to x$ and $Sxyz \to xz(yz)$, and no bound variables. It computes the same functions. Bracket abstraction translates a lambda term into an $S$-$K$ term: $[x]x = SKK$, $[x]M = KM$ when $x \notin \mathrm{FV}(M)$, and $[x](MN) = S([x]M)([x]N)$. These rules apply only to terms that contain no $\lambda$, and the $K$ rule is tried before the $S$ rule. The translation $T$ of a lambda term is $T(x) = x$, $T(MN) = T(M)\,T(N)$ and $T(\lambda x.M) = [x]\,T(M)$.
- The lambda calculus has no memory cell and no sequence of instructions. A Turing machine and a [random access machine](/random-access-machine/) count steps on a store that changes in place. A beta step substitutes a term, which can cost time in proportion to the size of the term unless the terms share subterms.

## Known results in the model

- Confluence: the Church-Rosser theorem holds, so normal forms are unique up to $\alpha$-equivalence.
- Normalization theorem: leftmost-outermost reduction reaches the normal form whenever one exists (Barendregt, Chapter 13).
- Whether a term has a normal form is undecidable (Church 1936). This is the lambda-calculus form of the [halting problem](/halting-problem/).
- Whether two terms are beta-equal is undecidable too (Barendregt, Chapter 6).
- The simply typed lambda calculus, which gives each term a type, is strongly normalizing: every reduction sequence ends (Tait 1967). So every typable term halts, and it is not Turing complete. On Church numerals it defines only the extended polynomials (Schwichtenberg 1976).
- Call-by-name contracts the leftmost-outermost redex but never reduces inside an abstraction. Call-by-value contracts a redex only when its argument is a value (a variable or an abstraction), as in most programming languages.
- De Bruijn indices name each variable by a number, which removes the need for $\alpha$-renaming.

## References
