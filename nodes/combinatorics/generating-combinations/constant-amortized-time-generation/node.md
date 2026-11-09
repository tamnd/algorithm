---
tag: TRSSMY
kind: concept
slug: constant-amortized-time-generation
name: Constant amortized time (CAT) generation
aliases:
- CAT algorithm
- CAT generation
- Constant amortized time generation
- constant amortized time enumeration
area: combinatorics/generating-combinations
level: core
summary: Generate each object with O(1) average work over the whole run, even if single steps can be longer.
prereqs: [combinatorial-generation, amortized-cost, k-subset-enumeration]
see_also: [loopless-generation, aggregate-method, binary-counter-increment, lexicographic-combinations, recursive-combination-generation, heaps-algorithm, generating-all-permutations, output-sensitive-generation]
sources:
  - paper: doi:10.1137/S0036144595295272
    title: Carla Savage, A survey of combinatorial Gray codes, SIAM Review 39(4), 1997, 605-629
    locator: Section 1 (the cost measures of generation, constant amortized time and loopless algorithms)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Sections 7.2.1.1 to 7.2.1.3 (the running time analyses of Algorithms M, L and T, and of the permutation generators)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition, MIT Press, 2022
    locator: Chapter 16, Amortized analysis (Section 16.1, the aggregate method and the binary counter)
---

A generation algorithm runs in constant amortized time, or is CAT, when the total time to list all $N$ objects of a class is $O(N)$. So the average time for each object is $O(1)$, even if one step between two objects takes much longer. The usual model keeps the current object in place and does not count the visit, so a CAT bound counts only the changes that the generator makes. Most simple generators are CAT: the [binary counter](/binary-counter-increment/), the [lexicographic successor](/lexicographic-combinations/) for $k \le n/2$, [Heap's algorithm](/heaps-algorithm/) and most recursive generators with no dead branches. A [loopless](/loopless-generation/) generator is CAT, but the converse is false.

## In plain words

A generator makes a long list of objects, one after the other. Some steps are cheap and some are expensive. CAT means that the total work, divided by the number of objects, is at most a fixed number. That number does not grow with the size of the objects.

A binary counter is the standard example. Most of the time it changes only the last digit. Sometimes it changes many digits, for example from $0111$ to $1000$. But such long steps are rare, and on average it changes fewer than two digits for each step.

## The idea

**Definition.** Let $\mathcal{A}_n$ be a class of objects with $N_n = |\mathcal{A}_n|$, and let $T(n)$ be the total time that a generator takes to list $\mathcal{A}_n$, after its initialization. The generator is CAT if there is a constant $c$ such that $T(n) \le c \cdot N_n$ for all $n$. The amortized time for each object is $T(n)/N_n$, see [amortized cost](/amortized-cost/).

**The output model.** In the in-place model, the generator changes one object in memory and calls a visit procedure, whose cost is not counted. Writing each object of size $n$ in full costs $\Theta(n)$, so a CAT bound with full output is impossible when the objects have size $n$. CAT therefore implies that the generator changes $O(1)$ entries of the object for each step on average.

**Why the bound is the best possible.** Each object needs a visit, so $T(n) = \Omega(N_n)$. CAT is this lower bound, up to a constant factor.

**How to prove a CAT bound.** Two methods cover most cases.

1. *Count the work in aggregate.* Sum the work of all steps directly. For the binary counter on $n$ bits, bit $j$ changes $\lfloor (2^n - 1)/2^j \rfloor$ times, so the total is less than $2 \cdot 2^n$. This is the [aggregate method](/aggregate-method/). The [potential method](/potential-method/) gives the same bound with a potential equal to the number of one bits.
2. *Count the nodes of the recursion tree.* Let the leaves of the tree be the visits. If each call does $O(1)$ work besides its calls, and each internal node has at least two children, then the tree has at most $2N - 1$ nodes, and the generator is CAT. Unary nodes and dead calls, which lead to no visit, must be counted on their own. A generator whose recursion tree has long chains of unary nodes, or many dead branches, need not be CAT.

**CAT and loopless.** A [loopless](/loopless-generation/) generator takes $O(1)$ time in the worst case between two visits. Each loopless generator is CAT. A CAT generator can have long steps, so it is not loopless in general. The binary counter is CAT and has a step of $\Theta(n)$ time. The [binary reflected Gray code](/binary-reflected-gray-code/) with focus pointers is loopless.

**CAT for a family, not for one size.** The definition needs one constant for all sizes. A generator can be CAT for some ranges of the parameters and not for others. The lexicographic successor for $k$-subsets takes $k/(n - k + 1)$ scan steps for each subset on average. This is less than $1$ for $k \le n/2$, but it is about $n/2$ for $k = n - 1$.

## Examples

**Binary counter.** To list the $2^n$ subsets of $[n]$, the counter changes $2^{n+1} - n - 2$ bits in its $2^n - 1$ steps. For $n = 10$ this is $2036$ changes for $1023$ steps, so $1.99$ changes for each step. The [binary reflected Gray code](/binary-reflected-gray-code/) changes exactly $1023$ bits, one for each step.

**Lexicographic $k$-subsets.** The [lexicographic successor](/lexicographic-combinations/) scans $C(n, k-1)$ entries in total.

| $n$ | $k$ | $N = C(n, k)$ | scan steps $C(n, k-1)$ | steps for each subset |
| --- | --- | --- | --- | --- |
| 10 | 5 | 252 | 210 | 0.83 |
| 20 | 10 | 184756 | 167960 | 0.91 |
| 10 | 9 | 10 | 45 | 4.5 |
| 20 | 19 | 20 | 190 | 9.5 |
| 40 | 39 | 40 | 780 | 19.5 |

The first two rows stay below $1$. The last three rows grow with $n$, so for $k = n - 1$ the generator is not CAT. Listing the complements, which are $1$-subsets, fixes this.

**The recursion for $k$-subsets.** The [choose or skip recursion](/recursive-combination-generation/) makes $2N - 1 + 2C(n, k-1)$ calls: $923$ calls for $n = 10$ and $k = 5$, that is $3.66$ calls for each subset. Its recursion tree has $N + C(n, k-1)$ leaves and only binary internal nodes, and the dead leaves number $C(n, k-1)$.

**A generator that is not CAT.** To list the $k$-subsets of $[n]$ by a binary counter and a test of the size takes $2^n$ steps for $C(n, k)$ outputs. For $n = 20$ and $k = 2$ this is $1048576$ steps for $190$ subsets.

**Permutations.** [Heap's algorithm](/heaps-algorithm/) makes one swap for each permutation, and its recursion does $O(1)$ work for each call on average, so it is CAT. The [Steinhaus-Johnson-Trotter](/steinhaus-johnson-trotter/) algorithm can be made loopless. See [generating all permutations](/generating-all-permutations/).

## Where it is used

- **The standard target for generation.** A new generation algorithm for a class of objects is usually first shown to be CAT. Savage's survey and Knuth's Section 7.2.1 measure generators this way.
- **Enumeration with a known count.** When the number of objects is known, CAT means that the program runs in time proportional to the count, so the total time is easy to predict.
- **Output-sensitive bounds.** When the number of objects is not known in advance, as in many graph enumeration problems, the analogue is time $O(1)$ or polynomial for each output. See [output-sensitive generation](/output-sensitive-generation/).
- **A step towards loopless.** Many loopless algorithms start from a CAT recursion and remove its loops with extra pointers. See [loopless generation](/loopless-generation/).

## References
