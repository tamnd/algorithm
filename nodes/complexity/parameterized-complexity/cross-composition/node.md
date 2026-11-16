---
tag: SJQJR6
kind: technique
slug: cross-composition
name: Cross-composition
aliases:
- OR-cross-composition
area: complexity/parameterized-complexity
level: research
summary: "Pack many equivalent instances of an NP-hard problem into one instance whose parameter is polynomial in the largest size plus log t. It rules out polynomial kernels unless NP is in coNP/poly."
prereqs: [kernel-lower-bounds]
see_also: [polynomial-compression, polynomial-parameter-transformation, polynomial-kernel, lossy-kernelization, sat, parameterized-longest-path, parameterized-clique, treewidth]
sources:
  - paper: doi:10.1137/120880240
    title: "Hans L. Bodlaender, Bart M. P. Jansen and Stefan Kratsch, Kernelization lower bounds by cross-composition, SIAM Journal on Discrete Mathematics 28(1), 277-305 (2014)"
    locator: the definitions of a polynomial equivalence relation and of cross-composition, and the main theorem
  - paper: doi:10.1016/j.jcss.2009.04.001
    title: "Hans L. Bodlaender, Rodney G. Downey, Michael R. Fellows and Danny Hermelin, On problems without polynomial kernels, Journal of Computer and System Sciences 75(8), 423-434 (2009)"
    locator: OR-composition by disjoint union, the earlier form of the method
  - paper: doi:10.1016/j.jcss.2010.06.007
    title: "Lance Fortnow and Rahul Santhanam, Infeasibility of instance compression and succinct PCPs for NP, Journal of Computer and System Sciences 77(1), 91-106 (2011)"
    locator: the distillation theorem the method rests on
  - paper: doi:10.1137/130927115
    title: "Andrew Drucker, New limits to classical and quantum instance compression, SIAM Journal on Computing 44(5), 1443-1479 (2015)"
    locator: the AND version
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 15, Lower bounds for kernelization
  - book: isbn:9781107057760
    title: Fedor V. Fomin, Daniel Lokshtanov, Saket Saurabh and Meirav Zehavi, Kernelization, Theory of Parameterized Preprocessing, Cambridge University Press, 2019
    locator: Chapter 17, Framework, and Chapter 18, Instance selectors
---

A cross-composition packs $t$ instances of an NP-hard problem $L$ into one instance of a parameterized problem $Q$, so that the result is a yes-instance exactly when at least one input is, and the new parameter is bounded by a polynomial in the largest input size plus $\log t$. Bodlaender, Jansen and Kratsch introduced it in 2011 as the general form of the composition method. If such a map exists, $Q$ has no [polynomial compression](/polynomial-compression/), and so no polynomial kernel, unless $\mathrm{NP} \subseteq \mathrm{coNP/poly}$. It is the main tool of [kernel lower bounds](/kernel-lower-bounds/).

## In plain words

Suppose you can glue a large pile of hard puzzles into a single puzzle that is solvable exactly when at least one puzzle of the pile is solvable. Suppose also that the glued puzzle has a small measure of difficulty, one that grows only with the size of the largest puzzle and very slowly with the size of the pile.

Then a strong shrinking method for the glued puzzle would shrink a whole pile of hard puzzles into one short text that keeps the answer. A known theorem says this is not possible unless a widely believed claim about complexity fails. So no strong shrinking method exists for the glued kind of puzzle.

## When it applies

The target $Q$ must be a parameterized problem that is in NP, or at least decidable, and you want to show that it has no polynomial kernel. Typical signs:

- the problem is FPT, but every known kernel has exponential size;
- the instances can be combined so that one yes-instance makes the whole yes, as for a disjoint union of graphs when the question asks for a connected structure;
- or the instances can share a fixed frame, so that a small *instance selector* gadget picks one of them, at a parameter cost of about $\log t$.

The source $L$ can be any NP-hard language, and it does not have to equal $Q$.

## The template

Two notions come first. A *polynomial equivalence relation* $\mathcal{R}$ on strings is decidable in polynomial time, and for every $n$ it splits the strings of length at most $n$ into at most $\mathrm{poly}(n)$ classes. An *OR-cross-composition* of $L$ into $Q$ with respect to $\mathcal{R}$ is an algorithm that takes $t$ strings $x_1, \ldots, x_t$ in one class, runs in time polynomial in $\sum_i |x_i|$, and outputs $(y, k)$ with

- $(y, k) \in Q$ if and only if $x_i \in L$ for some $i$, and
- $k \le \mathrm{poly}(\max_i |x_i| + \log t)$.

The template has four holes. SAME is the relation $\mathcal{R}$, which usually asks for the same size measures, such as the number of vertices and the target value. EMBED turns one input into a part of the output. SELECT adds a gadget that lets exactly one part be "active". PARAM gives the new parameter.

```pseudo id=main
CROSS-COMPOSE(x_1, ..., x_t)                    ▷ all in one class of SAME
L1  n ← max_i |x_i|
L2  s ← ⌈log₂ t⌉; pad the list to 2^s inputs by repeating x_t
L3  for i ← 0 to 2^s - 1 do
L4      P_i ← EMBED(x_i, i)                       ▷ part i, tagged with the bits of i
L5  y ← SELECT(P_0, ..., P_{2^s - 1}, s)           ▷ a solution must choose one i
L6  k ← PARAM(n, s)                               ▷ must be poly(n + s)
L7  return (y, k)
```

When the inputs can be combined with no gadget, as in a disjoint union, line L5 only joins the parts and $s$ plays no role.

**Main theorem (Bodlaender, Jansen and Kratsch).** If $L$ is NP-hard and has an OR-cross-composition into $Q$, then $Q$ has no polynomial compression, unless $\mathrm{NP} \subseteq \mathrm{coNP/poly}$.

*Proof sketch.* Assume $Q$ has a compression into a language $R'$ of size $k^c$. Take strings $x_1, \ldots, x_t$ of length at most $n$ and remove duplicates, so $t < 2^{n+1}$. Split them into the at most $\mathrm{poly}(n)$ classes of $\mathcal{R}$. Cross-compose each class, which gives parameters $\mathrm{poly}(n + \log t) = \mathrm{poly}(n)$, and compress each result to $\mathrm{poly}(n)$ bits. The list of these $\mathrm{poly}(n)$ short strings has $\mathrm{poly}(n)$ bits, and it is a yes-instance of the language "some entry is in $R'$" exactly when some $x_i \in L$. This is an OR-distillation of an NP-hard language, and by Fortnow and Santhanam it gives $\mathrm{NP} \subseteq \mathrm{coNP/poly}$. $\square$

The class split is what makes the method easier than plain composition: the inputs that EMBED and SELECT see all share their sizes, so the gadgets can be built for one shape.

## Classic examples

**CNF-SAT parameterized by the number of variables.** Let $L$ be CNF-SAT, and let SAME put formulas with the same number $n$ of variables in one class (and all malformed strings in one more class). Brute force decides a formula in time $2^n$ times its size, so the problem is FPT, and a formula has at most $3^n$ distinct clauses, which is a kernel of exponential size. A cross-composition shows there is no polynomial one.

- SELECT adds $s = \lceil \log_2 t \rceil$ new variables $y_1, \ldots, y_s$, and the list is padded to $2^s$ formulas.
- EMBED takes each clause of $\varphi_i$ and adds the $s$ literals that are true when $y$ is not the binary code $b(i)$ of $i$: the literal $y_j$ if bit $j$ of $i$ is 0, and $\neg y_j$ if it is 1.
- If $y = b(i)$, all the added literals of $\varphi_i$ are false, so the clauses of $\varphi_i$ must hold; all other formulas have a true added literal in each clause. So the result is satisfiable if and only if some $\varphi_i$ is.
- PARAM is $n + s \le n + \log_2 t + 1$.

A scratch script checked this on 200 random lists of formulas with $n \in \{2, 3, 4\}$ and $t \le 9$ (seed 11). The satisfiability of the result always matched the OR of the inputs. For a worked case, take four formulas over $x_1, x_2$, each the 4 clauses of all sign patterns on $x_1, x_2$, which is unsatisfiable. The result has 4 variables and is unsatisfiable. Replace the formula with index 2 by $(x_1 \lor x_2)(\neg x_1 \lor x_2)$. The result then has $4 + 4 + 2 + 4 = 14$ clauses and is satisfiable, by $x_1 = 0$, $x_2 = 1$, $y_1 = 0$, $y_2 = 1$: the code of 2 has bit 1 equal to 0 and bit 2 equal to 1, so $y$ selects formula 2.

**k-Path from Hamiltonian path.** Let $L$ be Hamiltonian path and let SAME put graphs with the same number $n$ of vertices together. Output the disjoint union with $k = n$. A path on $n$ vertices cannot leave a component with $n$ vertices, so the union has one if and only if some input graph has a Hamiltonian path. Here SELECT is empty, and $k \le \max_i |x_i|$. So k-path has no polynomial kernel unless $\mathrm{NP} \subseteq \mathrm{coNP/poly}$, though it is FPT with time $2^{O(k)} n^{O(1)}$; see [parameterized longest path](/parameterized-longest-path/).

**Clique parameterized by the maximum degree.** The problem asks for a clique of size $\ell$ in a graph of maximum degree $\Delta$, with parameter $\Delta$. It is FPT: a clique lies in the closed neighborhood of each of its vertices, so trying all subsets of each neighborhood takes time $2^{\Delta}$ times a polynomial. Let $L$ be [clique](/parameterized-clique/), and let SAME put instances with the same $n$ and $\ell$ together. The disjoint union has a clique of size $\ell$ if and only if some input has one, and its maximum degree is less than $n$. So the parameter is at most $n$, and the problem has no polynomial kernel unless $\mathrm{NP} \subseteq \mathrm{coNP/poly}$.

## Variations

- **AND-cross-composition.** Ask for "all $x_i \in L$" instead of "some". Drucker (2012) showed that this also rules out polynomial compression under the same assumption. [Treewidth](/treewidth/) at most $k$ has one by disjoint union, since the treewidth of a union is the largest treewidth of its parts.
- **Composition into a parameterized source.** The first form of Bodlaender, Downey, Fellows and Hermelin composed instances of $Q$ into $Q$ with parameter $\mathrm{poly}(\max_i k_i)$. Cross-composition allows a different source and a relation $\mathcal{R}$, which makes many proofs shorter.
- **Polynomial lower bounds.** If the parameter grows like $t^{1/d}$ times a polynomial instead of $\log t$, a similar argument rules out compressions of size $O(k^{d - \varepsilon})$. This follows the work of Dell and van Melkebeek on vertex cover and d-hitting set.
- **Gap cross-composition.** For [lossy kernels](/lossy-kernelization/), a composition that keeps a gap between yes and no rules out $\alpha$-approximate kernels of polynomial size.
- **Transfer.** A [polynomial parameter transformation](/polynomial-parameter-transformation/) from a problem with a cross-composition carries the lower bound to the next problem.

## Pitfalls

- **The parameter may grow only with $\log t$.** A disjoint union of vertex cover instances needs the sum of the $k_i$ as its parameter, which grows linearly in $t$. That is not a cross-composition, and vertex cover does have a polynomial kernel.
- **The source must be NP-hard as a classical language.** The theorem uses Fortnow and Santhanam, which needs NP-hardness of $L$, not hardness of $Q$.
- **The relation must have few classes.** "Same number of vertices" is fine. "Same graph up to isomorphism" is not polynomial-time and is not allowed.
- **Padding must not add yes-instances.** In the CNF-SAT example the padding repeats a real input. Padding with a satisfiable formula would make every output satisfiable.
- **The result is conditional and only about compression.** It does not rule out kernels of exponential size, Turing kernels, or kernels for a different parameter.

## Exercises

1. Show that the CNF-SAT composition above is correct when $t = 1$, and check what goes wrong if $s = 0$ selector variables are used for $t = 2$.
2. Give an OR-cross-composition from Hamiltonian cycle into "a cycle of length at least $k$", with parameter $k$.
3. Explain why the disjoint union is not a cross-composition for "vertex cover of size at most $k$", and why no cross-composition can exist unless $\mathrm{NP} \subseteq \mathrm{coNP/poly}$.
4. Prove that "is the treewidth at most $k$" has an AND-composition, and state what Drucker's theorem then gives.

## References
