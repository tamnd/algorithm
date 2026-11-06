---
tag: N93W99
kind: technique
slug: matrix-interpretation
name: Matrix interpretation
aliases:
- matrix orderings
area: automata-and-parsing/term-rewriting
level: research
summary: A termination method interpreting function symbols as linear maps on vectors.
prereqs: [polynomial-interpretation, well-founded-reduction-ordering, termination]
see_also: [dependency-pairs, string-rewriting-system, recursive-path-ordering, knuth-bendix-ordering, termination-proof, matrix-power, spectral-radius, min-plus-matrix-multiplication]
sources:
  - paper: doi:10.1007/s10817-007-9087-9
    title: Jörg Endrullis, Johannes Waldmann and Hans Zantema, Matrix interpretations for proving termination of term rewriting, Journal of Automated Reasoning 40(2-3) (2008)
    locator: pp. 195 to 220 (the interpretation over vectors of naturals, the order on the first coordinate, the monotone and the weakly monotone variants, and the SAT encoding)
  - paper: doi:10.1007/11805618_25
    title: Dieter Hofbauer and Johannes Waldmann, Termination of string rewriting with matrix interpretations, Term Rewriting and Applications (RTA 2006), Lecture Notes in Computer Science 4098
    locator: pp. 328 to 342 (the method for string rewriting, as weighted automata)
  - paper: doi:10.1007/978-3-540-70590-1_14
    title: Adam Koprowski and Johannes Waldmann, Arctic termination ...below zero, Rewriting Techniques and Applications (RTA 2008), Lecture Notes in Computer Science 5117
    locator: pp. 202 to 216 (matrices over the max-plus semiring)
  - paper: doi:10.1007/978-3-642-21493-6_1
    title: Aart Middeldorp, Georg Moser, Friedrich Neurauter, Johannes Waldmann and Harald Zankl, Joint spectral radius theory for automated complexity analysis of rewrite systems, Algebraic Informatics (CAI 2011), Lecture Notes in Computer Science 6742
    locator: pp. 1 to 20 (polynomial bounds on derivation length from the growth of matrix products)
---

A **matrix interpretation** proves that a [term rewriting system](/term-rewriting-system/) terminates by mapping each term to a vector of natural numbers. Each function symbol becomes an affine map, $\vec v_1, \ldots, \vec v_n \mapsto F_1 \vec v_1 + \cdots + F_n \vec v_n + \vec f$, with square matrices $F_i$ and a vector $\vec f$ of natural numbers. Vectors are compared on the first coordinate, strictly, and on the others, weakly. If every rule makes the vector smaller for all values of its variables, every [rewrite step](/rewrite-step/) does, and no infinite reduction exists. The method extends linear [polynomial interpretations](/polynomial-interpretation/), which are the case of dimension 1. Hofbauer and Waldmann introduced it for string rewriting in 2006, and Endrullis, Waldmann and Zantema extended it to terms. The test for a given interpretation is exact and cheap, and a search for the matrices can be encoded into SAT.

## In plain words

A polynomial interpretation gives each expression one number that drops at each step. Sometimes no single number works. A matrix interpretation gives each expression a short list of numbers, computed from the lists of its parts by multiplying with fixed tables of numbers and adding fixed numbers.

The first number in the list must drop at each step. The other numbers only must not grow. The extra numbers can count things that one number cannot, for example how many letters of one kind stand to the right of the current place, and how often a part has been copied.

As before, a whole number that always drops cannot drop forever, so the rewriting stops.

## When it applies

- The aim is a proof of [termination](/termination/) of a finite system. A matrix interpretation proves termination; when the search fails, nothing follows, because termination is undecidable.
- The derivation lengths are at most exponential. The first coordinate of the vector of a ground term bounds the number of steps from it, and products of fixed matrices grow at most exponentially in the length of the product. So the method cannot prove termination of systems with longer derivations, such as one that computes the Ackermann function.
- The interpretation is linear in each variable. So, unlike a polynomial interpretation, it cannot multiply two arguments. Its strength is in the dimension: matrices can let several coordinates count different things and move weight between them.
- It is most useful for [string rewriting](/string-rewriting-system/), where each letter is a unary symbol and the interpretation is one matrix and one vector per letter, and inside the [dependency pair](/dependency-pairs/) framework, where weakly monotone matrices give reduction pairs.

## The template

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, rules $l \to r$, substitutions $\sigma$, and $\to^*$ for the reflexive transitive closure.

Fix a dimension $d \ge 1$. For vectors $\vec u, \vec v \in \mathbb{N}^d$, write $\vec u \ge \vec v$ if $u_i \ge v_i$ for all $i$, and $\vec u > \vec v$ if $u_1 > v_1$ and $u_i \ge v_i$ for $i \ge 2$. For matrices, $M \ge N$ means $M_{ij} \ge N_{ij}$ for all $i, j$.

An **interpretation** gives each $f \in \Sigma$ of arity $n$ matrices $F_1, \ldots, F_n \in \mathbb{N}^{d \times d}$ and a vector $\vec f \in \mathbb{N}^d$, with the top-left entry $(F_i)_{11} \ge 1$ for each $i$. Under an assignment $\alpha : V \to \mathbb{N}^d$, the value of a term is $[x]_\alpha = \alpha(x)$ and $[f(t_1, \ldots, t_n)]_\alpha = F_1 [t_1]_\alpha + \cdots + F_n [t_n]_\alpha + \vec f$. By induction on $t$, the value is affine in the variables:

$$[t]_\alpha = \sum_{x \in V} T_x\, \alpha(x) + \vec t,$$

where $T_x$ is a sum of products of the matrices along the paths from the root of $t$ to the occurrences of $x$ (the zero matrix if $x$ does not occur), and $\vec t$ is $[t]_\alpha$ at $\alpha = \vec 0$.

```pseudo id=main
MATRIX-TERMINATION(R, d)
L1  choose matrices F_1 .. F_n and a vector f for each symbol, with (F_i)_11 ≥ 1          ▷ hole: the search
L2  for each rule l → r in R do
L3      compute the coefficients (L_x)_x, l⃗ of [l] and (R_x)_x, r⃗ of [r] by composition
L4      if L_x ≥ R_x fails for some variable x then return "unknown"
L5      if l⃗ > r⃗ fails then return "unknown"
L6  return "R terminates"
```

The one hole is line L1. Lines L3 to L5 are an exact test, as the lemma below shows, and they take time polynomial in $d$ and in the sizes of the rules.

**Lemma (the test is exact).** Let $[l]_\alpha = \sum_x L_x \alpha(x) + \vec l$ and $[r]_\alpha = \sum_x R_x \alpha(x) + \vec r$. Then $[l]_\alpha > [r]_\alpha$ for all $\alpha$ if and only if $L_x \ge R_x$ for all $x$ and $\vec l > \vec r$.

*Proof.* If the conditions hold, then $[l]_\alpha - [r]_\alpha = \sum_x (L_x - R_x)\alpha(x) + (\vec l - \vec r)$, where the sum has no negative entries, because $\alpha(x) \ge \vec 0$, and $\vec l - \vec r$ has a positive first entry and no negative entries. So $[l]_\alpha > [r]_\alpha$. Conversely, $\alpha = \vec 0$ gives $\vec l > \vec r$. If $(L_x)_{ij} < (R_x)_{ij}$ for some $x, i, j$, let $\alpha(x) = m\, \vec e_j$ and $\alpha(y) = \vec 0$ for $y \ne x$. Entry $i$ of $[l]_\alpha - [r]_\alpha$ is $m\,((L_x)_{ij} - (R_x)_{ij}) + (l_i - r_i)$, which is negative for large $m$, so $[l]_\alpha > [r]_\alpha$ fails. $\blacksquare$

This is the main practical difference from polynomial interpretations, where the corresponding test is undecidable.

**Why it works.** Define $s \succ t$ if $[s]_\alpha > [t]_\alpha$ for all $\alpha$. This is a [reduction ordering](/well-founded-reduction-ordering/):

- It is well-founded: a chain $t_1 \succ t_2 \succ \cdots$ gives, at $\alpha = \vec 0$, a strictly decreasing chain of the first coordinates, which are natural numbers.
- It is closed under substitutions: $[t\sigma]_\alpha = [t]_\beta$ with $\beta(x) = [x\sigma]_\alpha$, so a comparison that holds for all assignments holds for $s\sigma$ and $t\sigma$.
- It is closed under contexts: if $\vec u > \vec v$, then $F\vec u + \vec w > F\vec v + \vec w$ for every $F$ with $F_{11} \ge 1$. Entry $i$ of $F(\vec u - \vec v)$ is $\sum_j F_{ij}(u_j - v_j) \ge 0$, and for $i = 1$ it is at least $F_{11}(u_1 - v_1) \ge 1$.

If lines L4 and L5 succeed for every rule, then $l \succ r$ for every rule by the lemma, so $R$ is compatible with a reduction ordering and terminates. For a ground term $t$, each step lowers the first coordinate of $[t]$ by at least 1, so the derivation height of $t$ is at most $[t]_1$.

**Searching for the matrices.** Tools fix $d$ (often 1 to 5) and a bound on the entries, write each entry as a few Boolean variables, and encode the conditions of lines L4 and L5 as a propositional formula. A SAT solver then finds the matrices or reports that none exist within the bounds (Endrullis, Waldmann and Zantema).

## Classic examples

All matrices below were found by an exhaustive search over small entries, and the comparisons, the decreases along random derivations, and the derivation heights were checked by a program.

**A rule with no polynomial interpretation.** Take the string rewriting rule $ab \to baa$, read on terms with unary symbols: $a(b(x)) \to b(a(a(x)))$. Each $a$ moves right past a $b$ and doubles. No polynomial interpretation over the naturals proves it. A monotone polynomial has degree at least 1, and the degrees multiply under composition, so $\deg[a] \cdot \deg[b] \ge \deg[b] \cdot \deg[a]^2$ forces $\deg[a] = 1$. The same comparison of leading coefficients forces $[a](x) = x + c$. Then $[l] = [b](x) + c$ and $[r] = [b](x + 2c) \ge [b](x) + 2c$, so $[l] > [r]$ fails.

In dimension 2, take

$$[a](\vec x) = \begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix} \vec x, \qquad [b](\vec x) = \begin{pmatrix} 1 & 0 \\ 0 & 2 \end{pmatrix} \vec x + \begin{pmatrix} 0 \\ 1 \end{pmatrix}.$$

Then

$$[ab](\vec x) = \begin{pmatrix} 1 & 2 \\ 0 & 2 \end{pmatrix} \vec x + \begin{pmatrix} 1 \\ 1 \end{pmatrix}, \qquad [baa](\vec x) = \begin{pmatrix} 1 & 2 \\ 0 & 2 \end{pmatrix} \vec x + \begin{pmatrix} 0 \\ 1 \end{pmatrix}.$$

The matrices are equal and $(1, 1) > (0, 1)$, so the rule terminates. At $\vec x = \vec 0$, the second coordinate of the vector of a word with $k$ letters $b$ is $2^k - 1$, the number of extra copies that an $a$ makes when it passes all of them. Each $a$ adds the second coordinate of the word to its right to the first coordinate, so the first coordinate counts the copies that all the letters $a$ will make.

**The bound is exact here.** For the word $a b^n$, the first coordinate of $[ab^n](\vec 0)$ is $2^n - 1$, and the longest derivation from $a b^n$ has exactly $2^n - 1$ steps, for $n = 1, \ldots, 5$. The matrix $\begin{pmatrix} 1 & 0 \\ 0 & 2 \end{pmatrix}$ has the eigenvalue 2, and this growth is needed: no interpretation by matrices whose products grow polynomially can prove a system with exponential derivations.

**Dimension 1.** With $d = 1$ a matrix interpretation is a linear polynomial interpretation, such as $[0] = 1$, $[s](x) = x + 1$, $[+](x, y) = 2x + y$ for the rules $0 + y \to y$ and $s(x) + y \to s(x + y)$: the differences are $2$ and $1$.

## Variations

- **Weakly monotone matrices in reduction pairs.** In the [dependency pair](/dependency-pairs/) framework, the condition $(F_i)_{11} \ge 1$ is dropped for the tuple symbols and the matrices may be zero. Rules need only $L_x \ge R_x$ and $\vec l \ge \vec r$, and pairs that also satisfy $\vec l > \vec r$ are removed. This is how matrix interpretations are used in most termination tools.
- **Arctic interpretations.** Replace $(+, \times)$ by $(\max, +)$ over the naturals with $-\infty$ (Koprowski and Waldmann). The value of a word is then the largest weight of a path in a weighted automaton, not a sum over the paths. Products of such matrices are computed as [min-plus matrix products](/min-plus-matrix-multiplication/), with the maximum in place of the minimum.
- **Polynomial bounds.** If all matrices are upper triangular with diagonal entries at most 1, the entries of a product of $m$ matrices grow at most like $m^{d-1}$, and the derivational complexity is polynomial. More generally, the growth of products is governed by the joint [spectral radius](/spectral-radius/) of the matrices (Middeldorp and others, 2011).
- **Rational and real entries.** Interpretations with non-negative rational or real entries, with a decrease by a fixed $\delta > 0$, prove more systems in some cases.
- **Weighted automata.** For string rewriting, the matrices of the letters are the transition matrices of a weighted automaton, and the value of a word is a sum over the paths of the automaton (Hofbauer and Waldmann).

## Pitfalls

- **Strictness in the wrong coordinate.** The order needs strict decrease in a fixed coordinate. Requiring "decrease in some coordinate" for each rule separately does not give a well-founded order on terms.
- **A zero top-left entry.** If $(F_i)_{11} = 0$, a step inside argument $i$ need not lower the first coordinate of the result, and closure under contexts fails. Such matrices are allowed only in reduction pairs.
- **Forgetting repeated variables.** In a rule such as $f(x) \to g(x, x)$, the coefficient $R_x$ is the sum $G_1 + G_2$, and the test must compare $L_x$ with that sum.
- **Testing on sample points.** Checking the vectors only at $\alpha = \vec 0$, or on a small grid, is not enough. A comparison can fail only for large values, so use the coefficient test.
- **Treating failure as non-termination.** A failed search shows only that no interpretation with the chosen dimension and entry bound exists.

## Exercises

1. Show that $[a] = \begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}$ with $\vec a = \vec 0$ and $[b] = \begin{pmatrix} 1 & 1 \\ 0 & 2 \end{pmatrix}$ with $\vec b = (0, 1)$ also proves termination of $ab \to baa$.
2. Prove that $a^n b \to^* b a^{2^n}$ in exactly $n$ steps, and compute $[a^n b](\vec 0)$ for the interpretation of the example.
3. Prove that for upper triangular matrices with diagonal entries in $\{0, 1\}$, the entries of a product of $m$ such $d \times d$ matrices are $O(m^{d-1})$.
4. Show that a matrix interpretation of dimension $d$ with all matrices diagonal is equivalent to $d$ linear polynomial interpretations, of which the first is strictly monotone and the others weakly monotone.

## References
