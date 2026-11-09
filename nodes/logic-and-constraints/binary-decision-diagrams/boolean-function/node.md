---
tag: T52BWB
kind: definition
slug: boolean-function
name: Boolean function
aliases:
- Boolean function of n variables
- switching function
area: logic-and-constraints/binary-decision-diagrams
level: intro
summary: A map from {0,1}^n to {0,1}, the object that BDDs represent.
prereqs: []
see_also: [cofactor, shannon-expansion, binary-decision-diagram, reduced-ordered-bdd, conjunctive-normal-form, boolean-circuit, boolean-function-composition, sat]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms Part 1, 2011
    locator: Section 7.1.1, Boolean basics (truth tables, the 16 functions of two variables, the count of functions of n variables) and Section 7.1.4 (functions as BDDs)
  - paper: doi:10.1109/TC.1986.1676819
    title: Randal E. Bryant, Graph-based algorithms for Boolean function manipulation, IEEE Transactions on Computers C-35(8), 1986, pages 677 to 691
    locator: Section 1.1, Notation (restriction, composition, the dependency set I_f and the satisfying set S_f)
  - book: isbn:9780521847513
    title: Yves Crama and Peter L. Hammer, Boolean Functions, Theory, Algorithms, and Applications, Cambridge University Press, 2011
    locator: Chapter 1, Fundamental concepts and applications
---

A Boolean function of $n$ variables is a map $f : \{0,1\}^n \to \{0,1\}$. There are $2^{2^n}$ of them, so most of them have no short description, but the functions that occur in circuits, constraints and verification often do. A truth table, a formula in [conjunctive normal form](/conjunctive-normal-form/), a [Boolean circuit](/boolean-circuit/) and a [binary decision diagram](/binary-decision-diagram/) are four ways to write one down. This page fixes the terms that the other pages of this area use.

## Definition

Let $n \ge 0$ and let $x_1, \ldots, x_n$ be variables that take the values 0 and 1. A **Boolean function** of $n$ variables is a total map

$$f : \{0,1\}^n \to \{0,1\}.$$

We write $B_n$ for the set of all of them. Two functions $f, g \in B_n$ are **equal** (or **equivalent**) when $f(x) = g(x)$ for each $x \in \{0,1\}^n$. Since a function is a set of $2^n$ input and output pairs, and each output is free,

$$|B_n| = 2^{2^n}.$$

The operations $\wedge$, $\vee$, $\neg$ and $\oplus$ act pointwise: $(f \wedge g)(x) = f(x) \wedge g(x)$, and so on. The constant functions are written $0$ and $1$. The terms below are the ones that BDD pages use.

- **Truth table.** With the inputs listed in a fixed order, $f$ is the string of its $2^n$ output values. On these pages, entry $a$ of the table, for $0 \le a < 2^n$, is $f(x)$ where $x_j$ is bit $j - 1$ of $a$. So $a = \sum_{j=1}^{n} x_j 2^{j-1}$.
- **Satisfying set.** $S_f = \{x \in \{0,1\}^n : f(x) = 1\}$. The map $f \mapsto S_f$ is a one-to-one map from $B_n$ onto the subsets of $\{0,1\}^n$, so a Boolean function is also a set of bit vectors. $|S_f|$ is the number of models; the page [counting satisfying assignments on BDDs](/bdd-satisfy-count/) computes it.
- **Essential variable.** $f$ **depends on** $x_i$ when there is an input $x$ such that changing only $x_i$ changes $f(x)$. In terms of the [cofactors](/cofactor/), $f$ depends on $x_i$ exactly when $f|_{x_i=0} \neq f|_{x_i=1}$. The **support** (Bryant's dependency set $I_f$) is the set of indices $i$ on which $f$ depends.
- **Subfunction.** A subfunction of $f$ is a function that we get from $f$ by fixing some variables to constants. With a fixed variable order, the subfunctions $f|_{x_1=a_1, \ldots, x_{i-1}=a_{i-1}}$ that depend on $x_i$ are exactly the nodes on level $i$ of the [reduced ordered BDD](/reduced-ordered-bdd/) of $f$ (see [canonicity](/bdd-canonicity/)).

## Examples and non-examples

**Two variables.** $|B_2| = 2^4 = 16$. With the table order $(x_1, x_2) = (0,0), (1,0), (0,1), (1,1)$:

| function | truth table | depends on |
|---|---|---|
| $0$ | 0000 | nothing |
| $x_1 \wedge x_2$ | 0001 | $x_1, x_2$ |
| $x_1$ | 0101 | $x_1$ only |
| $x_1 \oplus x_2$ | 0110 | $x_1, x_2$ |
| $x_1 \vee x_2$ | 0111 | $x_1, x_2$ |
| $\neg x_2$ | 1100 | $x_2$ only |

**Three variables.** $|B_3| = 2^8 = 256$. The majority function $\mathrm{MAJ}(x_1, x_2, x_3) = (x_1 \wedge x_2) \vee (x_1 \wedge x_3) \vee (x_2 \wedge x_3)$ has the truth table 00010111 in the order of the definition. It is 1 on the four inputs with $a = 3, 5, 6, 7$, so $|S_{\mathrm{MAJ}}| = 4$. The parity function $x_1 \oplus x_2 \oplus x_3$ has the table 01101001.

**Functions that depend on all their variables.** By inclusion and exclusion over the set of variables that a function may ignore, the number of $f \in B_n$ with support $\{1, \ldots, n\}$ is

$$D(n) = \sum_{k=0}^{n} (-1)^{n-k} \binom{n}{k} 2^{2^k}.$$

This gives $D(1) = 4 - 2 = 2$ (the functions $x_1$ and $\neg x_1$), $D(2) = 16 - 8 + 2 = 10$, and $D(3) = 256 - 48 + 12 - 2 = 218$. To prove it, let $A_i$ be the set of functions that do not depend on $x_i$. A function that does not depend on the variables of a set $T$ of size $t$ is a function of the other $n - t$ variables, so $|\bigcap_{i \in T} A_i| = 2^{2^{n-t}}$. Then $D(n) = \sum_{t=0}^{n} (-1)^t \binom{n}{t} 2^{2^{n-t}}$, which is the sum above with $k = n - t$.

**A function written in two ways.** The formulas $x_1 \vee (x_1 \wedge x_2)$ and $x_1$ are different strings, but they define the same function in $B_2$. That function does not depend on $x_2$. Deciding whether two formulas or circuits define the same function is the problem of [Boolean equivalence checking](/boolean-equivalence-checking/).

**Non-examples.**

- A formula, a circuit or a BDD is not a Boolean function. It is a representation of one, and many representations can give the same function.
- A partial map, defined only on a subset $C \subseteq \{0,1\}^n$, is not in $B_n$. It is an incompletely specified function, and the inputs outside $C$ are don't cares; see [don't-care minimization](/dont-care-minimization/).
- A map $\{0,1\}^n \to \{0, 1, 2, \ldots\}$ is a pseudo-Boolean or integer-valued function, not a Boolean function. An [algebraic decision diagram](/algebraic-decision-diagram/) represents such maps.
- A relation $R \subseteq \{0,1\}^n \times \{0,1\}^m$ is not a function from $n$ bits to $m$ bits unless each input has exactly one output. Its characteristic function $\chi_R \in B_{n+m}$ is a Boolean function, and this is how [symbolic model checking](/symbolic-model-checking/) stores a transition relation.

## Related definitions

- [Cofactor](/cofactor/): the function $f|_{x_i=b}$ that we get by fixing one variable.
- [Shannon expansion](/shannon-expansion/): $f = (\neg x_i \wedge f|_{x_i=0}) \vee (x_i \wedge f|_{x_i=1})$, the identity that every BDD algorithm uses.
- [Boolean function composition](/boolean-function-composition/): put a function $g$ in place of a variable of $f$.
- [Conjunctive normal form](/conjunctive-normal-form/) and [Boolean circuit](/boolean-circuit/): representations whose equality test is [co-NP-complete](/co-np-complete/).
- [Binary decision diagram](/binary-decision-diagram/) and [reduced ordered BDD](/reduced-ordered-bdd/): graph representations; the reduced ordered form is canonical for a fixed variable order.
- [Satisfiability](/sat/) asks whether $S_f \neq \emptyset$ for $f$ given as a formula. [Model counting](/model-counting/) asks for $|S_f|$.

## References
