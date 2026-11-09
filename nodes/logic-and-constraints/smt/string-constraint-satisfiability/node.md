---
tag: 0R2H6A
kind: problem
slug: string-constraint-satisfiability
name: String constraint satisfiability
aliases:
- string solving
- theory of strings
- word equations with constraints
- QF_S
area: logic-and-constraints/smt
level: research
summary: Decide constraints over string concatenation, length and regular-language membership.
prereqs: [regular-language, smt-problem, linear-integer-arithmetic-satisfiability]
see_also: [regular-expression, nondeterministic-finite-automaton, finite-state-transducer, parikh-theorem, hilberts-tenth-problem, presburger-arithmetic, symbolic-execution, lyndon-word]
sources:
  - paper: "G. S. Makanin, The problem of solvability of equations in a free semigroup, Matematicheskii Sbornik 103(145) (1977); English translation in Mathematics of the USSR Sbornik 32 (1977)"
    locator: the decidability of word equations
  - paper: "Wojciech Plandowski, Satisfiability of word equations with constants is in PSPACE, Journal of the ACM 51(3) (2004)"
    locator: the PSPACE upper bound for word equations
  - paper: "Artur Jeż, Recompression, a simple and powerful technique for word equations, Journal of the ACM 63(1) (2016)"
    locator: a simpler decision procedure for word equations, also with regular constraints
  - paper: "Klaus U. Schulz, Makanin's algorithm for word equations, two improvements and a generalization, Word Equations and Related Topics (IWWERT 1990), Lecture Notes in Computer Science 572, Springer, 1992"
    locator: the extension of decidability to word equations with regular constraints
  - paper: doi:10.1145/3158091
    title: Taolue Chen, Yan Chen, Matthew Hague, Anthony W. Lin and Zhilin Wu, What is decidable about string constraints with the ReplaceAll function, Proceedings of the ACM on Programming Languages 2(POPL), 2018, article 3
    locator: decidability of the straight-line fragment with replaceAll and regular constraints, and undecidability when length constraints are added
  - paper: "Anthony W. Lin and Pablo Barceló, String solving with word equations and transducers, towards a logic for analysing mutation XSS, Principles of Programming Languages (POPL 2016)"
    locator: the straight-line restriction, and undecidability of replace outside it (to be checked)
  - paper: "Vijay Ganesh, Mia Minnes, Armando Solar-Lezama and Martin Rinard, Word equations with length constraints, what's decidable?, Haifa Verification Conference (HVC 2012), Lecture Notes in Computer Science 7857, Springer, 2013"
    locator: the open status of word equations with length constraints, and decidable special cases
  - paper: "Tianyi Liang, Andrew Reynolds, Cesare Tinelli, Clark Barrett and Morgan Deters, A DPLL(T) theory solver for a theory of strings and regular expressions, Computer Aided Verification (CAV 2014), Lecture Notes in Computer Science 8559, Springer, 2014"
    locator: the string solver of CVC4 (now cvc5), with length reasoning and the normal form procedure
---

String constraint satisfiability is the problem of deciding whether a formula over string variables has a model, where the formula uses concatenation, equations between strings, the length function, membership in [regular languages](/regular-language/), and functions such as replace, substring and conversion to integers. String solvers are used to analyse programs that build queries, paths and web pages from user input. The problem is decidable for several fragments, such as word equations, but undecidable in general: with replace-all and length constraints together, it can express [Hilbert's tenth problem](/hilberts-tenth-problem/). Whether word equations with length constraints are decidable is a well-known open problem.

## In plain words

The unknowns are pieces of text. The rules can glue pieces together, compare them, ask for their length, ask whether a piece matches a pattern such as "only digits", or replace each occurrence of one text by another. The question is whether some texts make all rules true.

Some kinds of rules can always be decided by a computer, for example equations that only glue pieces together. But when "replace each occurrence" is mixed with rules about lengths, the rules become strong enough to describe any equation about whole numbers with plus and times, and no computer can decide those. Practical solvers handle the cases met in programs well, and they may answer "unknown".

## Definition

Fix a finite alphabet $\Sigma$. Terms of string sort are string variables, constants in $\Sigma^*$, concatenation $s \cdot t$, and functions such as $\mathrm{substr}(s, i, n)$, $\mathrm{replace}(s, p, r)$ (the first occurrence of $p$) and $\mathrm{replace\_all}(s, p, r)$ (all occurrences, from left to right, without overlaps). Integer terms include $|s|$ (the length), $\mathrm{indexof}(s, t, i)$ and $\mathrm{to\_int}(s)$. The atoms are:

- **word equations** $s = t$ between string terms, and their negations;
- **regular constraints** $s \in L(R)$ for a [regular expression](/regular-expression/) $R$;
- **arithmetic constraints** over lengths and other integer terms, usually [linear](/linear-integer-arithmetic-satisfiability/).

A formula is a Boolean combination of atoms (SMT-LIB logic QF_S, or QF_SLIA with linear integer arithmetic). The problem asks whether some assignment of strings and integers makes it true.

**Straight-line formulas.** A formula is *straight-line* if its equations have the form $x_1 = t_1, \ldots, x_k = t_k$, where each $x_j$ occurs once on a left side and $t_j$ uses only input variables and earlier $x_i$, plus constraints such as regular membership on any variable. Programs in static single assignment form give such formulas.

## Variants

- **Word equations only.** Equations between concatenations of variables and constants.
- **Word equations with regular constraints.**
- **Word equations with length constraints.** The status is open (see Bounds).
- **Regular constraints with length constraints, no equations.**
- **Straight-line formulas** with concatenation, replace-all, [transducers](/finite-state-transducer/) and regular constraints.
- **Bounded length.** If all lengths are bounded by a constant, the problem is finite, and solvers encode it into [bit-vectors](/bit-vector-satisfiability/) or SAT.
- **With string-integer conversion** ($\mathrm{to\_int}$, $\mathrm{from\_int}$), common in web code and hard for solvers.

## Examples

Each example was checked by brute force over the strings on $\{a, b\}$ of length at most 6 or 7.

1. **Commuting words.** $x \cdot y = y \cdot x \wedge x \ne y$ is satisfiable, for example $x = a$, $y = aa$. All solutions with $x, y$ nonempty are powers of a common word, as the classic theorem of Lyndon and Schützenberger says; the script found no other kind.
2. **First and last letters.** $x \cdot a = b \cdot x$ is unsatisfiable. If $x$ is empty, the two sides are $a$ and $b$. Otherwise, comparing the two sides letter by letter from the left gives $x_1 = b$ and $x_{i+1} = x_i$, so each letter of $x$ is $b$; but then the left side ends with $a$ and the right side ends with $b$.
3. **Regular and length.** $x \in (ab)^* \wedge |x| = 5$ is unsatisfiable, since the words of $(ab)^*$ have even length.
4. **Square.** $y = x \cdot x \wedge |y| = 7$ is unsatisfiable, since $|y| = 2|x|$.
5. **Counting with replace-all.** For $x \in \{a, b\}^*$, $y = \mathrm{replace\_all}(x, a, bb) \wedge |y| = |x| + 3$ holds exactly when $x$ has three letters $a$.
6. **Squaring with replace-all.** For $x = a^n$, $\mathrm{replace\_all}(x, a, x) = a^{n^2}$. This is the core of the undecidability proof below; the script checked the product gadget below for all $s, t \le 6$.

## Known algorithms

| method | fragment | notes |
|---|---|---|
| Makanin's algorithm; Plandowski's method; recompression (Jeż 2016) | word equations, also with regular constraints | complete; of theoretical interest, too slow in practice |
| Nielsen transformation | quadratic word equations (each variable at most twice) | complete for that case; a search on the first letters |
| automata constructions | regular constraints, straight-line formulas with transducers and replace-all (Chen et al. 2018) | complete; uses [NFA](/nondeterministic-finite-automaton/) products and pre-images |
| DPLL(T) string solvers (cvc5; Liang et al. 2014; Z3; Z3str3) | full QF_SLIA | normal forms of concatenations, length lemmas, lazy unfolding of regular expressions and functions; incomplete or nonterminating on some inputs |
| length abstraction | all | solve the [LIA](/linear-integer-arithmetic-satisfiability/) abstraction of the lengths first; an unsatisfiable abstraction proves unsatisfiability |
| bounded encoding | lengths bounded by a constant | encode each string as an array of characters in [bit-vectors](/bit-vector-satisfiability/) or SAT; complete only up to the bound |

## Bounds

**Decidable fragments.**

- **Word equations** are decidable (Makanin 1977) and in PSPACE (Plandowski 2004); they are NP-hard, and the exact complexity is open. Decidability extends to word equations with regular constraints (Schulz 1990).
- **Regular constraints with linear length constraints** are decidable: the set of lengths of a regular language is ultimately periodic, by [Parikh's theorem](/parikh-theorem/) on a one-letter image, so the formula reduces to a [Presburger](/presburger-arithmetic/) formula. Intersections of regular constraints on the same variable are handled by the [product of automata](/regular-language-intersection/).
- **Straight-line formulas with replace-all** whose patterns are constant regular expressions, together with concatenation and regular constraints, are decidable, in EXPSPACE (Chen et al. 2018). Replacement strings may be variables.
- **Word equations with length constraints**: decidability is open (Ganesh et al. 2012 discuss it and give decidable special cases).

**Theorem.** Satisfiability of straight-line string formulas with concatenation, $\mathrm{replace\_all}$ with a constant one-letter pattern and a variable replacement, the regular constraint $x \in a^*$, and linear constraints on lengths is undecidable.

*Proof.* Reduce Hilbert's tenth problem over the natural numbers, which is undecidable (Matiyasevich 1970): given a polynomial $p$ with integer coefficients, does $p(n_1, \ldots, n_k) = 0$ have a solution in $\mathbb{N}^k$? Represent a number $n$ by a string $a^n$.

- For each unknown $n_i$, take an input variable $x_i$ with $x_i \in a^*$.
- *Square.* If $u = a^s$, then $\mathrm{replace\_all}(u, a, u)$ replaces each of the $s$ letters by $u$ and equals $a^{s^2}$.
- *Product gadget.* Given $u = a^s$ and $v = a^t$, add the assignments $z = u \cdot v$, $Z = \mathrm{replace\_all}(z, a, z)$, $U = \mathrm{replace\_all}(u, a, u)$, $V = \mathrm{replace\_all}(v, a, v)$, a fresh input variable $w \in a^*$, and the linear constraint $2|w| = |Z| - |U| - |V|$. Then $|w| = ((s + t)^2 - s^2 - t^2)/2 = s t$, so $w = a^{st}$.
- Applying the gadget repeatedly gives, for each monomial of $p$, a variable $w_m = a^{\mathrm{value}}$. Write $p = p^+ - p^-$ with nonnegative coefficients, and add the single linear constraint $\sum_m c_m |w_m| = \sum_{m'} c'_{m'} |w_{m'}|$.

Each assignment uses only earlier variables, so the formula is straight-line, and its size is polynomial in the size of $p$. A solution of $p = 0$ gives a model with $x_i = a^{n_i}$, and each model gives the solution $n_i = |x_i|$. $\square$

Chen et al. (2018) show this undecidability for straight-line replace-all with length constraints, and also when variables may occur in the pattern. Outside the straight-line restriction, even $\mathrm{replace}$ with constant arguments leads to undecidability (Lin and Barceló 2016). With quantifiers, the first-order theory of concatenation alone is undecidable (Quine 1946).

## Reductions

- **To LIA, partially.** Each string constraint implies constraints on lengths; unsatisfiable length constraints refute the formula.
- **To SAT or bit-vectors with bounded length.** Complete up to the bound, used by early tools for web security.
- **From Hilbert's tenth problem.** As in the theorem, for replace-all with lengths.
- **From regular-expression problems.** Emptiness of the [intersection](/regular-language-intersection/) of several regular languages is the satisfiability of $x \in L_1 \wedge \cdots \wedge x \in L_k$, which is PSPACE-complete for $k$ given as part of the input.

## Applications

- Detecting injection attacks and cross-site scripting: can user input reach a database query or a web page in a dangerous form after the sanitizers of the program?
- [Symbolic execution](/symbolic-execution/) of programs in JavaScript, Python and Java, where strings are everywhere.
- Checking access-control policies and configuration files written with patterns, for example in cloud policy languages.
- Test generation for parsers and input validators.

## References
