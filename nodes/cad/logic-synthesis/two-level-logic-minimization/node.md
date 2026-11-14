---
tag: 0D4QNX
kind: problem
slug: two-level-logic-minimization
name: Two-level logic minimization
aliases:
- SOP minimization
- two-level minimization
area: cad/logic-synthesis
level: core
summary: Given a Boolean function with don't-cares, find a sum of products for it with the fewest product terms, then the fewest literals. NP-hard from a truth table, Sigma_2^p-complete from a DNF.
prereqs: [sum-of-products, prime-implicant, dont-care-condition]
see_also: [quine-mccluskey, petricks-method, espresso, karnaugh-map, set-cover, greedy-set-cover, polynomial-hierarchy, multi-level-logic-synthesis]
sources:
  - paper: doi:10.1006/jcss.2001.1775
    title: Christopher Umans, The minimum equivalent DNF problem and shortest implicants, Journal of Computer and System Sciences 63(4), 597 to 611, 2001
    locator: the Sigma_2^p-completeness of MIN DNF (an equivalent DNF with at most k literals) and of the shortest implicant problem
  - paper: "Marcus Schaefer and Christopher Umans, Completeness in the polynomial-time hierarchy, a compendium, SIGACT News 33(3), 2002"
    title: Completeness in the polynomial-time hierarchy, a compendium
    locator: the entries for MIN DNF and for IRREDUNDANT (the term count version and the hardness of approximation)
  - paper: doi:10.1137/060664537
    title: Eric Allender, Lisa Hellerstein, Paul McCabe, Toniann Pitassi and Michael Saks, Minimizing disjunctive normal form formulas and AC0 circuits given a truth table, SIAM Journal on Computing 38(1), 63 to 84, 2008
    locator: the NP-completeness of Min-DNF for a function given by its truth table, with the history of the earlier proofs of Masek and Czort
  - paper: "William J. Masek, Some NP-complete set covering problems, unpublished manuscript, 1979"
    title: Some NP-complete set covering problems
    locator: the first proof of NP-completeness for a truth table input (known through later citations)
  - paper: doi:10.1109/TCAD.1987.1270318
    title: Richard L. Rudell and Alberto L. Sangiovanni-Vincentelli, Multiple-valued minimization for PLA optimization, IEEE Transactions on Computer-Aided Design 6(5), 727 to 750, 1987
    locator: the exact minimizer Espresso-EXACT and the heuristic Espresso-MV, with measurements on PLA benchmarks
  - paper: doi:10.1016/0167-9260(94)00007-7
    title: Olivier Coudert, Two-level logic minimization, an overview, Integration, the VLSI Journal 17(2), 97 to 140, 1994
    locator: the survey of exact and heuristic methods, the cyclic core and implicit prime generation
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 7, Two-Level Combinational Logic Optimization
---

Two-level logic minimization asks for a cheapest [sum of products](/sum-of-products/) of a Boolean function, where the function may have [don't-care conditions](/dont-care-condition/). The cost is the number of product terms first and the number of literals second. A sum of products is a circuit with one level of AND gates and one OR gate, or a programmable logic array (PLA), so the cost is the gate count, or the number of PLA rows. The problem was the first big problem of logic synthesis, from Quine and McCluskey in the 1950s to Espresso in the 1980s. Its hardness depends on how the function is given. From a truth table, the decision version is NP-complete (Masek 1979, unpublished; later proofs by Czort 1999 and by Allender and coauthors 2008). From a DNF formula, it is $\Sigma_2^p$-complete (Umans 2001), one level above NP in the [polynomial hierarchy](/polynomial-hierarchy/).

## In plain words

A light must turn on for some settings of a few switches and stay off for others. For a few settings you do not care. You want to build the rule with AND gates feeding one OR gate. Each AND gate looks at some switches and fires when each one is in the position it wants. The light is on when any gate fires. A gate that checks fewer switches fires for more settings, so it does more work. The task is to use as few gates as you can, and then as few gate inputs as you can. A gate must never fire for a setting where the light must stay off. For a setting you do not care about, a gate may fire or not.

## Definition

**Input.** A function $f$ of $n$ variables, given by its on-set $F \subseteq \{0,1\}^n$ and its don't-care set $D \subseteq \{0,1\}^n \setminus F$. The off-set is $R = \{0,1\}^n \setminus (F \cup D)$. The input form is part of the problem; the common forms are below under Variants.

**Feasible solutions.** A set $C$ of cubes, each a product of literals, such that
$$F \;\subseteq\; \bigcup_{c \in C} c \;\subseteq\; F \cup D.$$
Such a $C$ is a cover of $f$. Each cube of a cover is an [implicant](/implicant/).

**Objective.** Minimize the cost
$$\mathrm{cost}(C) = \Big(|C|,\ \sum_{c \in C} |c|\Big)$$
in lexicographic order, where $|c|$ is the number of literals of $c$.

**Decision version.** Given $f$ and an integer $k$, is there a cover with at most $k$ cubes? The literal version asks for at most $k$ literals in total.

By Quine's theorem on the [prime implicant](/prime-implicant/) page, every minimum cover for this cost consists of prime implicants. So the problem is the same as: choose a cheapest set of primes whose union contains $F$. This second form is a weighted [set cover](/set-cover/) problem with the minterms of $F$ as the elements and the primes as the sets.

## Variants

- **By the input form.**
  - *Truth table.* $F$ and $D$ are given as lists of minterms, or as a table of $2^n$ entries. The input size is $N = 2^n$ up to a factor $n$.
  - *Cover, or DNF.* $F$ and $D$ are given as sums of products. The input can be exponentially smaller than the truth table. This is the form of PLA files and of Espresso.
  - *BDD or circuit.* $f$ is given by a binary decision diagram or by a circuit. Exact methods that work on BDDs of the primes use this form.
- **By the cost.** The number of cubes only; the number of literals only; the pair above; or weighted literals. For the number of cubes only, some minimum cover is prime, but not every one is.
- **Minimal instead of minimum.** A cover is minimal, or prime and irredundant, when each cube is prime and no cube can be dropped. Many minimal covers are not minimum. The heuristic tools find a minimal cover.
- **Irredundant subcover.** Given a cover and $k$, is there a subset of at most $k$ of its cubes that is still a cover? Schaefer and Umans list this problem, IRREDUNDANT, as $\Sigma_2^p$-complete for a DNF input.
- **Multiple outputs.** $m$ functions share one AND plane, so a cube used by several outputs is paid for once. The cost is the number of distinct cubes. Each output has its own don't-cares.
- **Output phase.** For each output, the PLA may build $f_j$ or $\bar{f}_j$ and invert it. Choosing the phases is part of the problem.
- **Multiple-valued inputs.** Variables with more than two values, as in the input decoders of PLAs. Espresso-MV handles this form.
- **Product of sums.** A cheapest CNF of $f$ is the dual problem: a cheapest SOP of $\bar{f}$, with the roles of $F$ and $R$ swapped.

## Examples

- **BCD digit at least 5.** $F = \{5, \ldots, 9\}$ and $D = \{10, \ldots, 15\}$ over $a b c d$. The minimum is $a + b d + b c$: 3 cubes and 5 literals. Without $D$ it is $a \bar{b} \bar{c} + \bar{a} b d + \bar{a} b c$, with 3 cubes and 9 literals.
- **Essential primes and one choice.** $F = \{4, 8, 10, 11, 12, 15\}$ and $D = \{9, 14\}$ over $x_1 x_2 x_3 x_4$. The primes ${-}100$ and $1{-}1{-}$ are essential. The minterm 8 is left, and the primes $10{-}{-}$ and $1{-}{-}0$ cover it at the same cost. Both covers have 3 cubes and 7 literals.
- **A cyclic instance.** $F = \{1, 2, 3, 4, 5, 6\}$ over $x_1 x_2 x_3$, the function "not all three equal". It has six primes, none essential, and each minterm lies in two of them. The minimum covers have 3 cubes and 6 literals, for example $\bar{x}_1 x_3 + x_2 \bar{x}_3 + x_1 \bar{x}_2$. The cover $\bar{x}_1 x_3 + x_1 \bar{x}_3 + \bar{x}_2 x_3 + x_2 \bar{x}_3$ is minimal (prime and irredundant) but has 4 cubes.
- **Parity.** $x_1 \oplus \cdots \oplus x_n$ has a unique cover, its $2^{n-1}$ minterms, with $n 2^{n-1}$ literals.

## Known algorithms

- [Karnaugh map](/karnaugh-map/). By hand, for up to four or five variables. The primes are the largest rectangles. The usual reading takes the essential groups and then picks groups by eye, which is not always minimum.
- [Quine-McCluskey](/quine-mccluskey/). Exact. Lists all primes by merging cubes, then solves the prime table. The table step is exponential in the worst case.
- [Petrick's method](/petricks-method/). Exact for the prime table. Lists every irredundant set of primes by multiplying out a product of sums, and can take exponential time and space.
- [Greedy set cover](/greedy-set-cover/) on the prime table. A cover within a factor $1 + \ln |F| \le 1 + n \ln 2$ of the fewest cubes, after the primes are listed.
- [Espresso](/espresso/). Heuristic. Works on covers without listing all primes, and returns a prime and irredundant cover. It has no proved bound on the gap to the minimum.
- Espresso-EXACT (Rudell and Sangiovanni-Vincentelli 1987) and the implicit methods surveyed by Coudert (1994). Exact, with the primes and the table stored as BDDs or ZDDs, and with branch and bound on the cyclic core.
- A [pseudo-Boolean](/pseudo-boolean-sat/) or [MaxSAT](/max-sat/) solver on the covering step. Exact, with one 0-1 variable for each prime.

## Bounds

**Upper bounds (proved).**

- Every $n$-variable function has a cover with at most $2^{n-1}$ cubes, for $n \ge 1$. By the Shannon expansion $f = \bar{x}_1 f_0 + x_1 f_1$, a cover of $f$ is $\bar{x}_1 C_0 \cup x_1 C_1$, so the bound doubles with each variable, from 1 cube for $n = 1$. Parity needs exactly $2^{n-1}$, so the bound is tight.
- For a truth table input, the decision version is in NP: a cover with at most $k \le 2^n$ cubes is a certificate of size polynomial in $N = 2^n$, and checking it takes time polynomial in $N$. The primes number at most $3^n = N^{\log_2 3}$, and they can be listed in time polynomial in $N$.
- For a DNF input, the decision version is in $\Sigma_2^p$: guess a cover with at most $k$ cubes, then check for all points $x$ that it agrees with $f$ on the care set, which is a co-NP check.

**Lower bounds (proved, as hardness).**

- Truth table input: the decision version with at most $k$ cubes is NP-complete. Masek (1979, unpublished) gave the first proof; Czort (1999, a master's thesis) and Allender, Hellerstein, McCabe, Pitassi and Saks (2008) give full proofs. So no algorithm runs in time polynomial in $2^n$ unless P = NP.
- DNF input: MIN DNF, an equivalent DNF with at most $k$ literals, is $\Sigma_2^p$-complete (Umans 2001). The compendium of Schaefer and Umans lists the version with $k$ terms as $\Sigma_2^p$-complete too, and lists hardness of approximation results for it. So the problem is not in NP unless the polynomial hierarchy collapses to NP.
- Even the case $k = 1$ with no literal is hard for a DNF input: a DNF has a cover with one cube and no literal exactly when it is a tautology, which is co-NP-complete.

**Measured.** Brayton, Hachtel, McMullen and Sangiovanni-Vincentelli (1984) ran Espresso-II on a set of 56 PLAs and compared it with the minimizers MINI, PRESTO and POP. Rudell and Sangiovanni-Vincentelli (1987) ran Espresso-EXACT and Espresso-MV on a set of benchmark PLAs and compared the heuristic results with the exact minima on that set. These are measurements on those sets, not proved bounds.

## Reductions

- **To set cover.** After the primes are listed, the problem is weighted set cover with $|F|$ elements and at most $3^n$ sets. For a truth table input this reduction takes time polynomial in $2^n$.
- **From tautology.** A DNF $G$ is a tautology exactly when its minimum cover is the one cube with no literal. So the DNF version is co-NP-hard by a reduction that only copies the input.
- **CNF and SOP.** A cheapest CNF of $f$ is the De Morgan dual of a cheapest SOP of $\bar{f}$. For a truth table input the two problems are the same up to swapping $F$ and $R$. For a DNF input, the complement can be exponentially larger, as the example $x_1 y_1 + \cdots + x_k y_k$ on the [unate function](/unate-function/) page shows.
- **Multiple outputs to one output.** A function with $m$ outputs becomes one function of the inputs and one extra variable with $m$ values, the output number. A cube of the new function names a cube of the inputs and the set of outputs that use it. Rudell and Sangiovanni-Vincentelli (1987) treat outputs this way in Espresso-MV.

## Applications

- **PLAs and PLDs.** The AND and OR planes of a PLA, and the product terms of a PAL or GAL device, are a sum of products, and their area is close to the number of distinct cubes.
- **Nodes of multi-level circuits.** In [multi-level logic synthesis](/multi-level-logic-synthesis/), each node of a [Boolean network](/boolean-network/) holds a small SOP, and a two-level minimizer simplifies it with the [observability don't-cares](/observability-dont-care/) of the node.
- **State machines and control logic.** The next-state and output functions of a controller, with the unused state codes as don't-cares.
- **Rule sets.** A DNF is a set of if-then rules, so the same minimization makes a rule set shorter.

## References
