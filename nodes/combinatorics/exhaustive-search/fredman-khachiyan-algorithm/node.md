---
tag: FEAKXY
kind: algorithm
slug: fredman-khachiyan-algorithm
name: Fredman-Khachiyan algorithm
aliases:
- FK dualization algorithm
- Fredman-Khachiyan duality test
area: combinatorics/exhaustive-search
level: research
summary: Quasi-polynomial-time algorithm for hypergraph dualization, generating all minimal transversals.
solves: [minimal-transversal-enumeration]
model: word-ram
complexity:
  vars: {n: the number of variables, m: the total number of terms of f and g}
  time: {worst: n^O(1) m^O(log^2 m), best: O(n m^2)}
  space: {extra: O(n^2 m)}
properties: {deterministic: true, recursive: true}
history:
  year: 1996
  people: [Michael L. Fredman, Leonid Khachiyan]
  note: Published in the Journal of Algorithms in 1996. It gave the first sub-exponential bound for testing the duality of two monotone DNFs, and so for generating all minimal transversals of a hypergraph.
prereqs: [hypergraph, boolean-function, quasi-polynomial-time]
see_also: [minimal-transversal-enumeration, hitting-set, hypergraph, output-sensitive-enumeration, quasi-polynomial-time, maximal-independent-set-enumeration, enumeration-problem, exact-exponential-algorithms]
sources:
  - paper: doi:10.1006/jagm.1996.0062
    title: Michael L. Fredman and Leonid Khachiyan, On the complexity of dualization of monotone disjunctive normal forms, Journal of Algorithms 21(3), 1996, 618 to 628
    locator: the necessary conditions for duality, the frequent variable, the decomposition into two smaller duality tests, and the bounds for algorithms A and B
  - paper: "Thomas Eiter and Georg Gottlob, Identifying the minimal transversals of a hypergraph and related problems, SIAM Journal on Computing 24(6), 1995, 1278 to 1304"
    locator: the problem of listing all minimal transversals, its equivalence with the duality test, and the many problems that reduce to it
  - paper: "Thomas Eiter, Kazuhisa Makino and Georg Gottlob, Computational aspects of monotone dualization: a brief survey, Discrete Applied Mathematics 156(11), 2008, 2035 to 2049"
    locator: the survey of the Fredman-Khachiyan algorithms, their later analysis and the problems that are equivalent to dualization
---

The Fredman-Khachiyan algorithm tests whether two monotone Boolean functions in disjunctive normal form are *dual* to each other, and finds an assignment that shows they are not when this is the case. With $m$ terms in total it runs in time $m^{O(\log^2 m)}$ times a polynomial in the number of variables, which is [quasi-polynomial](/quasi-polynomial-time/). Since the minimal transversals of a [hypergraph](/hypergraph/) form the dual of the hypergraph, one duality test per new transversal lists all [minimal transversals](/minimal-transversal-enumeration/) in incremental quasi-polynomial time. Fredman and Khachiyan published the method in 1996, and it is still the best known general bound; whether the problem has a polynomial algorithm is open.

## In plain words

Think of a list of committees, and of a second list of groups of people. A group *blocks* the committees if it has at least one member in every committee. The question is whether the second list holds exactly the smallest blocking groups.

The algorithm first makes quick checks: every group must meet every committee, and the two lists must not be too short. If a quick check fails, it can name a set of people that proves the lists are wrong. If all checks pass, it picks a person who is in many of the committees or many of the groups. It then splits the question into two smaller questions, one in which this person is in and one in which this person is out, and answers each of them in the same way.

## The problem

A *monotone DNF* over variables $V$ is a family of *terms*, each a subset of $V$. The function $f$ is true on an assignment $x \subseteq V$ (the set of true variables) when some term of $f$ is a subset of $x$. Two monotone DNFs $f$ and $g$ are *dual* when

$$f(x) \ne g(\bar{x}) \quad \text{for every } x \subseteq V,$$

where $\bar{x} = V \setminus x$. This means $g = f^d$, the function $f^d(x) = \lnot f(\bar{x})$. An $x$ with $f(x) = g(\bar{x})$ is a *witness* that the two are not dual.

**Duality test.** Given $f$ and $g$, decide whether they are dual, and if not, return a witness.

If the terms of $f$ are the edges of a hypergraph $H$ and no term contains another, then $f^d$ has exactly the minimal transversals of $H$ as its minimal terms. So $g$ is dual to $f$ exactly when the minimal terms of $g$ are all minimal transversals of $H$.

## The algorithm

Call the recursive procedure FK-DUAL. The variables of $f$ and $g$ are $V$, and for a variable $v$ the DNFs split as $f = v f_1 \lor f_0$ and $g = v g_1 \lor g_0$: the terms without $v$ form $f_0$, and the terms with $v$, with $v$ removed, form $f_1$.

```pseudo id=main
FK-DUAL(f, g)                    ▷ none if f and g are dual, else a witness x
L1  remove repeated terms and terms that contain another term, in f and in g
L2  if some F ∈ f and G ∈ g have F ∩ G = ∅ then return F
L3  if a variable v is in a term F of f and in no term of g then return F \ {v}
L4  if a variable v is in a term G of g and in no term of f then return V \ (G \ {v})
L5  if Σ_{F ∈ f} 2^{-|F|} + Σ_{G ∈ g} 2^{-|G|} < 1 then return an x with f(x) = g(x̄) = 0
L6  if V = ∅ then return none
L7  v ← a variable that is in the largest fraction of the terms of f or of g
L8  split f = v f1 ∨ f0 and g = v g1 ∨ g0
L9  y ← FK-DUAL(f0 ∨ f1, g0); if y ≠ none then return y ∪ {v}
L10 y ← FK-DUAL(f0, g0 ∨ g1); if y ≠ none then return y
L11 return none
```

Lines L2 to L5 are necessary conditions for duality, and each failure gives a witness at once.

- **L2.** For $x = F$, $f(x) = 1$, and $\bar{x}$ contains $G$, so $g(\bar{x}) = 1$.
- **L3.** No other term of $f$ is inside $F \setminus \{v\}$, by line L1, so $f$ is false there. And $g$ does not use $v$, so $g$ on the complement is $g(\bar{F})$, which is false because every term of $g$ meets $F$.
- **L4.** The same argument with the roles of $f$ and $g$ exchanged.
- **L5.** For a uniform random $x$, the expected number of terms of $f$ true on $x$ plus terms of $g$ true on $\bar{x}$ is the sum, which is below 1. Fixing the variables one by one, each to the value that does not raise this expected number, ends with an $x$ on which it is 0.

Lines L9 and L10 use the identity: $f$ and $g$ are dual if and only if $f_0 \lor f_1$ and $g_0$ are dual (the case $v$ true) and $f_0$ and $g_0 \lor g_1$ are dual (the case $v$ false). Both smaller tests are over $V \setminus \{v\}$.

**Listing minimal transversals.** Start with $g$ empty. Run FK-DUAL$(H, g)$. A witness $x$ cannot have $f(x) = g(\bar{x}) = 1$, since every term of $g$ is a transversal and meets every edge. So $x$ contains no edge and $\bar{x}$ contains no term of $g$: $\bar{x}$ is a transversal of $H$ that is new. Remove its vertices one by one while it stays a transversal, add the resulting minimal transversal to $g$, and repeat until FK-DUAL returns none.

## Example

Let $f = \{ab, cd\}$, the hypergraph with edges $\{a, b\}$ and $\{c, d\}$, and let $g = \{ac, ad, bc\}$. The fourth minimal transversal $bd$ is missing.

1. **Checks.** Every term of $f$ meets every term of $g$. Both use $a, b, c, d$. The sum is $\tfrac14 + \tfrac14 + \tfrac14 + \tfrac14 + \tfrac14 = \tfrac54 \ge 1$. So the checks pass.
2. **Frequent variable.** Each variable is in half of the terms of $f$. In $g$, the variables $a$ and $c$ are in two of the three terms. Take $v = a$. Then $f_0 = \{cd\}$, $f_1 = \{b\}$, $g_0 = \{bc\}$ and $g_1 = \{c, d\}$.
3. **Line L9.** Call FK-DUAL$(\{cd, b\}, \{bc\})$. The pairs meet: $cd \cap bc = \{c\}$ and $b \cap bc = \{b\}$. But $d$ is in the term $cd$ of the first DNF and in no term of the second, so line L3 returns $cd \setminus \{d\} = \{c\}$.
4. **Lift.** The outer call returns $\{c\} \cup \{a\} = \{a, c\}$.

Indeed, $x = \{a, c\}$ contains neither $ab$ nor $cd$, so $f(x) = 0$, and $\bar{x} = \{b, d\}$ contains none of $ac, ad, bc$, so $g(\bar{x}) = 0$. The complement $\{b, d\}$ is the missing transversal. With $bd$ added to $g$, the same run passes every check at every level and returns none.

## Correctness

Line L1 does not change $f$ or $g$ as functions. Each return at lines L2 to L5 is a witness by the arguments above. If the checks pass and $V = \emptyset$, then $f$ and $g$ are each the constant 0 (no terms) or the constant 1 (the empty term). Line L2 removes the case where both are 1, and line L5 removes the case where both are 0, so one is 0 and the other is 1, and these are dual. For lines L9 and L10, fix $v$ and an assignment $y$ of the other variables. If $v$ is true in $x$, then $f(x) = (f_0 \lor f_1)(y)$ and $g(\bar{x}) = g_0(\bar{y})$; if $v$ is false, then $f(x) = f_0(y)$ and $g(\bar{x}) = (g_0 \lor g_1)(\bar{y})$. So a witness of either smaller test, with $v$ set as in that case, is a witness of $f$ and $g$, and if neither smaller test has a witness, then $f$ and $g$ are dual. Each recursive call has one variable fewer, so the recursion ends. The full proof is below.

## Complexity

**The frequent variable.** If lines L2 and L5 pass, some term has at most $\log_2 m$ variables, because otherwise the sum at line L5 would be below $m \cdot 2^{-\log_2 m} = 1$. Say it is a term $F$ of $f$. Every term of $g$ meets $F$, so one of the at most $\log_2 m$ variables of $F$ is in at least a fraction $1 / \log_2 m$ of the terms of $g$. So the variable chosen at line L7 has frequency at least $\varepsilon = 1 / \log_2 m$ in $f$ or in $g$.

**The recurrence.** Measure a test by its volume $|f| \cdot |g|$. Suppose $v$ is frequent in $g$. In the call at line L9, $g_0$ has at most $(1 - \varepsilon)|g|$ terms, so the volume drops by the factor $1 - \varepsilon$. In the call at line L10, $f_0$ has at least one term fewer than $f$, since line L3 ensures that $v$ is in some term of $f$, so the volume drops by at least 1. The case of $v$ frequent in $f$ is symmetric. Along any path from the root, the volume can drop by the factor $1 - \varepsilon$ only $O(\log m / \varepsilon) = O(\log^2 m)$ times before it reaches 1. Fredman and Khachiyan count the paths and get a tree with $m^{O(\log^2 m)}$ nodes. Each node does polynomial work in $n$ and $m$: the minimization and the pair test at lines L1 and L2 take $O(n m^2)$ time, and line L5 takes $O(n^2 m)$ steps of exact arithmetic.

So the duality test runs in time $n^{O(1)} m^{O(\log^2 m)}$. The best case is a witness at line L2 of the first call, in $O(n m^2)$ time. The recursion has depth at most $n$, and each level keeps $O(n m)$ words for its four DNFs, so the extra space is $O(n^2 m)$.

**Listing.** To list the $k$ minimal transversals of a hypergraph with $e$ edges, the method makes $k + 1$ duality tests, each with at most $e + k$ terms. So the $i$-th transversal comes after time quasi-polynomial in $n$, $e$ and $i$. This is *incremental quasi-polynomial time*.

## Properties

- **Gives a witness.** A "no" answer comes with an assignment that proves it, and in the listing this witness is a new transversal.
- **Symmetric.** The roles of $f$ and $g$ are the same, since duality is symmetric.
- **Deterministic.** Line L5 uses the method of conditional expectations instead of random sampling.
- **Quasi-polynomial in the input and output together.** The bound depends on $|f| + |g|$, so it is useful only when the dual is not much larger than the input, which is the case for the listing method above.

## Variants and improvements

- **Algorithm B.** The same paper refines the choice of the frequent variable and the analysis, and gets time $m^{4 \chi(m) + O(1)}$, where $\chi(m)^{\chi(m)} = m$. Since $\chi(m) \sim \log m / \log \log m$, this is $m^{o(\log m)}$.
- **Small space.** Later work gives versions of algorithm A that use polynomial space in total, and versions with a small amount of nondeterminism, which place the problem in classes below co-NP.
- **Joint generation.** Boros, Elbassioni, Gurvich, Khachiyan and Makino used the same test to generate a monotone function and its dual together, for problems such as the minimal integer solutions of monotone linear systems.
- **Practical methods.** Berge's method, which adds one edge at a time and updates the transversals, and search methods with pruning are often faster in practice, though their worst case is exponential in the output.

## When to use it

Use the Fredman-Khachiyan algorithm when a proven bound per output is needed for listing minimal transversals, minimal hitting sets, maximal frequent sets, minimal keys, or any other problem that is equivalent to monotone dualization, or to decide whether a given list of such sets is complete. For data of moderate size, the simpler practical methods are usually faster.

## Pitfalls

- **Merged DNFs need minimization.** $f_0 \lor f_1$ can contain a term that contains another. Without line L1 at each call, line L3 can return a set that is not a witness.
- **The complement depends on $V$.** Take $\bar{x}$ over a variable set that contains every variable of $f$ and $g$. Variables that neither DNF uses do not change any value.
- **Constants.** The DNF with no terms is the constant 0, and the DNF with the empty term is the constant 1. They are dual to each other and to nothing else.
- **Rounding.** The sum at line L5 can be exactly 1, for example for $f = g = \{a\}$, which are dual. Use exact arithmetic, not floating point.
- **The choice of variable.** Any variable gives a correct algorithm, but only a frequent variable gives the quasi-polynomial bound.

## Implementations

## History

Monotone dualization, under many names, was known to be equivalent to a long list of problems in logic, databases, artificial intelligence and graph theory, and Eiter and Gottlob (1995) surveyed these links. Whether it can be solved in polynomial total time was, and still is, open. In 1996 Fredman and Khachiyan gave the first sub-exponential bound, with algorithm A in time $m^{O(\log^2 m)}$ and algorithm B in time $m^{o(\log m)}$. Later work studied their algorithms from the point of view of space, of limited nondeterminism and of parallel time, and used them for joint generation.

## References
