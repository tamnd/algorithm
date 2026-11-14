---
tag: HABH4Y
kind: definition
slug: unate-function
name: Unate function
aliases:
- monotone in each variable
area: cad/logic-synthesis
level: core
summary: A Boolean function that is, in each variable, either nondecreasing or nonincreasing. Tautology and complement are easy for unate covers.
prereqs: [boolean-function, cofactor, sum-of-products]
see_also: [unate-recursive-paradigm, shannon-expansion, prime-implicant, espresso, set-cover, binate-covering-problem, petricks-method, zero-suppressed-bdd]
sources:
  - book: isbn:9780898381641
    title: Robert K. Brayton, Gary D. Hachtel, Curtis T. McMullen and Alberto L. Sangiovanni-Vincentelli, Logic Minimization Algorithms for VLSI Synthesis, Kluwer, 1984
    locator: Chapter 3, Decomposition and Unate Functions, Section 3.3, Unate Functions, and Section 3.5, Unate Complementation
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 7, Two-Level Combinational Logic Optimization (unate covers, tautology and complementation)
  - book: isbn:9780792397465
    title: Gary D. Hachtel and Fabio Somenzi, Logic Synthesis and Verification Algorithms, Kluwer, 1996
    locator: Chapter 5, Heuristic Minimization of Two-Level Circuits
---

A Boolean function is unate in a variable $x$ if, as $x$ goes from 0 to 1 with the other inputs fixed, the value only goes up in all cases, or only goes down in all cases. It is positive unate in $x$ in the first case and negative unate in the second. A function is unate if it is unate in every variable. Otherwise it is binate in some variable, like $x_1 \oplus x_2$. A positive unate function, unate in the positive sense in every variable, is what most mathematicians call a monotone function. That is why "monotone in each variable" and "monotone" are not the same: the first allows a different direction for each variable, while many authors use the second only for the positive case. Unate covers are easy: a unate cover is a tautology only if it has the cube with no literal. The [unate recursive paradigm](/unate-recursive-paradigm/) and [Espresso](/espresso/) are built on this fact.

## Definition

Let $f : \{0,1\}^n \to \{0,1\}$ and let $f_{x_i}$ and $f_{\bar{x}_i}$ be its [cofactors](/cofactor/) by $x_i = 1$ and $x_i = 0$. Write $g \le h$ when $g(a) \le h(a)$ for every point $a$.

- $f$ is **positive unate** in $x_i$ if $f_{\bar{x}_i} \le f_{x_i}$.
- $f$ is **negative unate** in $x_i$ if $f_{x_i} \le f_{\bar{x}_i}$.
- $f$ is **unate** in $x_i$ if one of these holds, and **binate** in $x_i$ otherwise.
- $f$ is **unate** if it is unate in each of its variables. It is positive unate if it is positive unate in each variable.

A function that does not depend on $x_i$ is both positive and negative unate in $x_i$.

**Unate cover.** A cover $C$, a set of cubes, is unate in $x_i$ if $x_i$ does not appear in $C$ both as $x_i$ and as $\bar{x}_i$. In positional notation, the column $i$ of $C$ does not hold both a 0 and a 1. The cover is unate if it is unate in every variable.

**Facts.**

1. **A unate cover gives a unate function.** If no cube of $C$ has the literal $\bar{x}_i$, then every cube of the cofactor $C_{\bar{x}_i}$ is also a cube of $C_{x_i}$, so $f_{\bar{x}_i} \le f_{x_i}$.
2. **The converse is false for covers.** The cover $\{x_1, \bar{x}_1 x_2\}$ is binate in $x_1$, but its function $x_1 + x_2$ is positive unate. Every unate function has some unate cover, for example the sum of its primes, by fact 3.
3. **Primes of a unate function.** If $f$ is positive unate in $x_i$, no prime of $f$ has the literal $\bar{x}_i$. Proof: let $p = \bar{x}_i q$ be a prime, where $q$ has no literal of $x_i$. Take a point $a$ of $q$ with $a_i = 1$, and let $a'$ be $a$ with $a_i = 0$. Then $a' \in p$, so $f(a') = 1$, and $f(a) \ge f(a') = 1$ because $f$ is positive unate in $x_i$. So $q$ is an implicant, and it contains $p$ strictly, which is not allowed.
4. **Tautology of a unate cover.** A unate cover $C$ is a tautology (the constant 1) exactly when it holds the cube with no literal. Proof: if it does not, build a point $a$: set $a_i = 0$ when $x_i$ appears in $C$, $a_i = 1$ when $\bar{x}_i$ appears, and $a_i = 0$ when neither does. Each cube of $C$ has a literal, and each literal of $C$ is false at $a$. So $C$ is 0 at $a$.
5. **Every prime is essential.** If $f$ is completely specified and unate, each prime $p$ is essential, so the sum of all primes is the unique minimum [sum of products](/sum-of-products/). Proof for the positive case: by fact 3, $p$ is a product of positive literals. Let $a$ be the point with $a_i = 1$ exactly for the variables of $p$. Any prime $q$ that contains $a$ is also positive, so its variables are among those of $p$, so $q \supseteq p$, and then $q = p$ since $p$ is prime. The negative and mixed cases are the same after renaming $x_i$ to $\bar{x}_i$.
6. **Unate covering.** A product of sums of positive literals, like the Petrick function of a prime table, is a positive unate function. This is why the covering step of two-level minimization is called the unate covering problem. It is the [set cover](/set-cover/) problem. When negative literals also occur, the problem becomes the [binate covering problem](/binate-covering-problem/).

Fact 4 gives a test in $O(nm)$ time for a unate cover of $m$ cubes. For a general cover the test is hard. A cover $C$ is a tautology exactly when the CNF that De Morgan's law gives for $\bar{C}$ is not satisfiable, and every CNF arises this way, so the tautology of a general cover is [co-NP-complete](/co-np-complete/).

## Examples and non-examples

- **Unate.** $f = x_1 + \bar{x}_2 x_3$ is positive unate in $x_1$ and $x_3$ and negative unate in $x_2$. The cover is unate, and by fact 4 it is not a tautology: the point $a = (0, 1, 0)$ makes it 0.
- **Monotone.** The majority $x_1 x_2 + x_1 x_3 + x_2 x_3$ and every threshold function with positive weights are positive unate. A threshold function with mixed signs is unate. The converse fails: $x_1 x_2 + x_3 x_4$ is positive unate but is not a threshold function.
- **Binate.** $x_1 \oplus x_2$ is binate in both variables. The multiplexer $\bar{s} a + s b$ is binate in $s$ and positive unate in $a$ and $b$.
- **A binate cover of a tautology.** $\{x_1, \bar{x}_1\}$ is a tautology with no cube free of literals. Fact 4 needs the cover to be unate.
- **Counts.** Of the 16 functions of two variables, 14 are unate; only $x_1 \oplus x_2$ and its complement are not. For three variables, 104 of the 256 functions are unate, and 20 are positive unate. For four, 2170 of 65536 are unate and 168 are positive unate. The number of positive unate functions is the Dedekind number.
- **Don't-cares break fact 5.** Let $F = \{11\}$ and $D = \{01, 10\}$ over $x_1 x_2$. Both $F$ and $F \cup D$ are positive unate. The primes are $x_1$ and $x_2$, each covers the one on-set point, neither is essential, and there are two minimum covers.
- **A large complement.** The complement of the positive unate function $x_1 y_1 + \cdots + x_k y_k$ is negative unate. Its primes are the $2^k$ cubes $\bar{z}_1 \cdots \bar{z}_k$ with each $z_i \in \{x_i, y_i\}$, and by fact 5 all of them are needed. So a unate cover of $k$ cubes can have a complement with $2^k$ cubes.

## Related definitions

- **[Cofactor](/cofactor/)** and **[Shannon expansion](/shannon-expansion/).** The definition compares the two cofactors. Splitting a binate cover by the Shannon expansion on a binate variable makes the parts closer to unate.
- **[Unate recursive paradigm](/unate-recursive-paradigm/).** Tautology, complement and containment for covers, by splitting until each part is unate.
- **[Espresso](/espresso/).** Uses unate tautology and complement in each of its steps.
- **[Prime implicant](/prime-implicant/).** Fact 5 says that for unate functions the primes are the answer.
- **[Set cover](/set-cover/)** and the **[binate covering problem](/binate-covering-problem/).** The unate and the binate cases of covering with a product of sums.
- **[Zero-suppressed BDD](/zero-suppressed-bdd/).** Stores sets of cubes such as unate covers in a compact way.

## References
