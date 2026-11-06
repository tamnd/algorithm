---
tag: Q386XT
kind: model
slug: combinatory-logic
name: Combinatory logic
aliases:
- SK combinators
- combinators
area: automata-and-parsing/term-rewriting
level: advanced
summary: A model of computation with combinators S and K as rewrite rules, equivalent to the lambda calculus.
prereqs: [term-rewriting-system, lambda-calculus, orthogonal-rewrite-system]
see_also: [beta-reduction, church-rosser-theorem, orthogonal-confluence-theorem, graph-reduction, outermost-reduction, confluence-decision-problem, turing-machine, markov-algorithm]
sources:
  - paper: doi:10.1007/BF01448013
    title: Moses Schönfinkel, Über die Bausteine der mathematischen Logik, Mathematische Annalen 92(3-4) (1924)
    locator: pp. 305 to 316 (the combinators, among them C and S, that remove bound variables from logic)
  - paper: doi:10.2307/2370619
    title: Haskell B. Curry, Grundlagen der kombinatorischen Logik, American Journal of Mathematics 52(3) (1930)
    locator: pp. 509 to 536 (the first part, with the formal system of combinators and its reduction)
  - book: isbn:9780521898850
    title: J. Roger Hindley and Jonathan P. Seldin, Lambda-Calculus and Combinators, an Introduction, Cambridge University Press, 2008
    locator: Chapter 2, Combinatory logic, pp. 21 to 32 (CL-terms, weak reduction, abstraction and its main property), Chapters 3 to 5 (fixed points, computable functions and undecidability), and Chapter 8 (extensionality in CL)
  - paper: doi:10.1002/spe.4380090105
    title: David A. Turner, A new implementation technique for applicative languages, Software, Practice and Experience 9(1) (1979)
    locator: pp. 31 to 49 (compiling a functional language to combinators S, K, I, B, C and running them by graph reduction)
---

**Combinatory logic** (CL) is a model of computation with no variables in its programs. A program is built from two constants, $S$ and $K$, by application only, and it runs by two rewrite rules: $K\,x\,y \to x$ and $S\,x\,y\,z \to x\,z\,(y\,z)$. Schönfinkel introduced combinators in 1924 to remove bound variables from logic, and Curry developed the system from 1930. CL computes exactly what the [lambda calculus](/lambda-calculus/) and [Turing machines](/turing-machine/) compute, but it does so without substitution under binders: each step is a plain [rewrite step](/rewrite-step/) of a first-order [term rewriting system](/term-rewriting-system/). This makes it a standard example in rewriting, and the basis of an implementation method for lazy functional languages.

## The machine

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, rules $l \to r$, $\to^*$ for the reflexive transitive closure, positions as sequences of positive integers, and substitutions $\sigma$.

**Terms.** The signature has the constants $S$ and $K$ and one binary symbol, application, written as juxtaposition. So the terms are given by $M ::= x \mid S \mid K \mid (M\ M)$ with $x \in V$, and application associates to the left: $S\,x\,y\,z$ means $(((S\,x)\,y)\,z)$. A **combinator** is a term without variables. Variables are needed only to state the rules and to show what a combinator does.

**Rules.** CL is the term rewriting system with two rules:

$$K\,x\,y \to x \qquad\qquad S\,x\,y\,z \to x\,z\,(y\,z).$$

A step rewrites one instance of a left side, anywhere in a term. This is called **weak reduction**. A term with no redex is a [normal form](/normal-form/). The term $I = S\,K\,K$ behaves as the identity: $S\,K\,K\,x \to K\,x\,(K\,x) \to x$. Many presentations add $I$ as a third constant with the rule $I\,x \to x$; this changes the step counts but not what can be computed. The examples below use $I$ as a constant.

**Computing.** A combinator $F$ computes a function on data encoded as normal forms: $F$ applied to the codes of the inputs reduces to the code of the output. For numbers, let $B = S\,(K\,S)\,K$, so that $B\,x\,y\,z \to^4 x\,(y\,z)$, and let the **Church numerals** be $\bar 0 = K\,I$ and $\overline{n+1} = S\,B\,\bar n$. Then $\bar n\,f\,x \to^* f^n(x)$: $K\,I\,f\,x \to I\,x \to x$, and $S\,B\,\bar n\,f\,x \to B\,f\,(\bar n\,f)\,x \to^* f\,(\bar n\,f\,x)$. So $S\,B$ computes the successor. With $f$ and $x$ as variables, $\bar 2\,f\,x$ reaches $f\,(f\,x)$ in 12 leftmost-outermost steps.

A computation **halts** if it reaches a normal form. It may not halt: with $\Omega = S\,I\,I\,(S\,I\,I)$, $\Omega \to I\,(S\,I\,I)\,(I\,(S\,I\,I)) \to S\,I\,I\,(I\,(S\,I\,I)) \to S\,I\,I\,(S\,I\,I) = \Omega$, a cycle of 3 steps.

## What it counts

The cost of a computation is the number of rewrite steps, and its memory is the size of the terms, counted as the number of constant and variable occurrences. Both depend on the **strategy**, the rule that chooses the next redex. Two strategies matter.

- **Leftmost-outermost** (normal order) reduces the redex whose head is leftmost. It is the [outermost reduction](/outermost-reduction/) strategy of this system, and it finds the normal form whenever one exists (see Known results).
- **Innermost** reduces arguments first. It can loop on a term that has a normal form: $K\,I\,\Omega$ reduces to $I$ in one leftmost step, but an innermost strategy keeps rewriting $\Omega$.

The rule for $S$ copies its argument $z$. On a tree representation, the copy costs time proportional to the size of $z$, and repeated copies can make the size grow exponentially in the number of steps. Implementations therefore count steps on graphs, where $z$ is shared and a step costs $O(1)$; this is [graph reduction](/graph-reduction/).

## Relation to other models

**Lambda calculus.** Each combinator is a closed λ-term: $K = \lambda x y.\,x$ and $S = \lambda x y z.\,x\,z\,(y\,z)$, and each CL step becomes one or more [beta steps](/beta-reduction/). In the other direction, **bracket abstraction** removes a variable from a CL term:

- $[x]\,x = I$,
- $[x]\,M = K\,M$ if $x$ does not occur in $M$,
- $[x]\,(M\,N) = S\,([x]\,M)\,([x]\,N)$ otherwise.

A λ-term is translated by replacing each $\lambda x.\,M$, innermost first, by $[x]\,M$. For example, $[x]\,[y]\,(y\,x) = S\,(K\,(S\,I))\,(S\,(K\,K)\,I)$, and this term applied to $a$ and $b$ reaches $b\,a$ in 8 steps. The two systems compute the same functions. But weak reduction is weaker than beta reduction, because it cannot reduce inside an abstraction: $S\,K$ and $K\,I$ are distinct normal forms of CL, but $S\,K\,x\,y \to^2 y$ and $K\,I\,x\,y \to^2 y$, and as λ-terms both are equal to $\lambda x y.\,y$. Adding extensionality axioms to CL makes its equality match $\beta\eta$-equality of the λ-calculus (Hindley and Seldin, Chapter 8).

**Term rewriting.** CL is a first-order term rewriting system in applicative form. Its left sides are [linear](/linearity/) and do not overlap, so it is an [orthogonal system](/orthogonal-rewrite-system/). It is not terminating, as $\Omega$ shows. Many general results about orthogonal systems were first found for CL and the λ-calculus.

**Turing machines and other models.** CL can simulate [Turing machines](/turing-machine/), through the λ-calculus or directly, and a Turing machine can carry out weak reduction, so the two models compute the same partial functions. A [Markov algorithm](/markov-algorithm/) is the string rewriting counterpart: also a rewriting model of general computation, but on strings, with a fixed order of rules.

**Implementations.** Turner (1979) compiled a lazy functional language to combinators, with the extra constants $B$ and $C$ to keep the code small, and ran the result by graph reduction. The idea led to special machines for combinator reduction and to later abstract machines for lazy languages.

## Known results in the model

**Confluence.** If $M \to^* N_1$ and $M \to^* N_2$, then $N_1$ and $N_2$ have a common reduct. So a term has at most one normal form, and the result of a halting computation does not depend on the order of steps. This follows from the [orthogonal confluence theorem](/orthogonal-confluence-theorem/), because CL is orthogonal; it is the CL form of the [Church-Rosser theorem](/church-rosser-theorem/).

**Combinatory completeness.** For every term $M$ and variable $x$, the term $[x]\,M$ does not contain $x$, and for every term $N$,

$$([x]\,M)\,N \to^* M[x := N].$$

*Proof.* By induction on $M$. That $x$ does not occur in $[x]\,M$ is clear from the three cases. If $M = x$, then $I\,N \to N = M[x := N]$. If $x$ does not occur in $M$, then $K\,M\,N \to M = M[x := N]$. Otherwise $M = M_1\,M_2$, and $S\,([x]\,M_1)\,([x]\,M_2)\,N \to ([x]\,M_1)\,N\,(([x]\,M_2)\,N) \to^* M_1[x := N]\,M_2[x := N]$ by the induction hypothesis applied to both parts, and this is $M[x := N]$. $\blacksquare$

So every function that can be written with variables can be written without them, using only $S$ and $K$ (and $I = S\,K\,K$).

**Fixed points.** For every term $F$ there is a term $X$ with $X \to^* F\,X$.

*Proof.* Let $W = S\,(K\,F)\,(S\,I\,I)$ and $X = W\,W$. Then

$$W\,W \to K\,F\,W\,(S\,I\,I\,W) \to F\,(S\,I\,I\,W) \to F\,(I\,W\,(I\,W)) \to F\,(W\,(I\,W)) \to F\,(W\,W),$$

five steps, the last two inside the argument of $F$. $\blacksquare$

With bracket abstraction, $Y = [f]\,(W_f\,W_f)$, where $W_f = S\,(K\,f)\,(S\,I\,I)$, is a single combinator. By combinatory completeness $Y\,F \to^* W_F\,W_F$, and $W_F\,W_F \to^* F\,(W_F\,W_F)$ as above, so $Y$ finds a fixed point of any $F$. Fixed points give recursion, as in the λ-calculus.

**Normalizing strategy.** Leftmost-outermost reduction reaches the normal form of every term that has one. For CL this is a case of the result for orthogonal systems whose left sides have all variables to the right of the constants (left-normal systems).

**Turing completeness and undecidability.** Every partial recursive function is computed by a combinator on Church numerals (Hindley and Seldin, Chapters 4 and 5). So the questions "does $M$ have a normal form?" and "do $M$ and $N$ have a common reduct?" are undecidable, by a reduction from the [halting problem](/halting-problem/). The [confluence decision problem](/confluence-decision-problem/) page uses CL to show that confluence of finite rewrite systems is undecidable.

**One basis is enough.** $\{S, K\}$ is a basis: every closed λ-term has a translation into it. Other bases exist, such as Curry's $\{B, C, K, W\}$, and there are single combinators from which $S$ and $K$ can be built.

**Typed CL.** If types are assigned with $K : A \to B \to A$ and $S : (A \to B \to C) \to (A \to B) \to A \to C$, the typable terms are strongly normalizing, and the types of $S$ and $K$ are exactly the axioms of the implicational fragment of intuitionistic logic, with application as modus ponens. This is the first instance of the correspondence between proofs and programs that Curry noted.

## References
