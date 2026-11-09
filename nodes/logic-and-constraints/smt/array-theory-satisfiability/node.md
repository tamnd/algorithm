---
tag: 6QSHKR
kind: problem
slug: array-theory-satisfiability
name: Theory of arrays satisfiability
aliases:
- theory of arrays
- read-over-write axioms
- QF_AX
- array property fragment
area: logic-and-constraints/smt
level: advanced
summary: Decide formulas with select and store operations over array variables.
prereqs: [euf-satisfiability, smt-problem]
see_also: [congruence-closure, ackermannization, bit-vector-satisfiability, presburger-arithmetic, quantifier-instantiation, nelson-oppen, symbolic-execution, loop-invariant]
sources:
  - paper: "John McCarthy, Towards a mathematical science of computation, Information Processing 1962 (Proceedings of IFIP Congress 1962), North-Holland, 1963"
    locator: the functions access and change, and the axioms that relate them
  - paper: doi:10.1007/11609773_28
    title: Aaron R. Bradley, Zohar Manna and Henny B. Sipma, What's decidable about arrays?, Verification, Model Checking, and Abstract Interpretation (VMCAI 2006), Lecture Notes in Computer Science 3855, Springer, 2006, 427 to 442
    locator: Definitions 4 and 5 (array property fragment), Definitions 6 to 9 (index set and the procedure SAT_A), Theorems 1 and 2 (decidability and NP-completeness), Theorems 3 and 4 (undecidable extensions)
  - paper: "Aaron Stump, Clark W. Barrett, David L. Dill and Jeremy Levitt, A decision procedure for an extensional theory of arrays, Proceedings of the 16th IEEE Symposium on Logic in Computer Science (LICS 2001)"
    locator: the decision procedure for quantifier-free formulas with extensionality (to be checked)
  - paper: "Leonardo de Moura and Nikolaj Bjørner, Generalized, efficient array decision procedures, Formal Methods in Computer-Aided Design (FMCAD 2009)"
    locator: lazy instantiation of the array axioms in an SMT solver, and combinatory arrays with map and constant arrays
  - book: isbn:9783662504963
    title: Daniel Kroening and Ofer Strichman, Decision Procedures, An Algorithmic Point of View, second edition, Springer, 2016
    locator: Chapter 7, Arrays (the reduction to uninterpreted functions and the array property fragment)
  - book: isbn:9783540741121
    title: Aaron R. Bradley and Zohar Manna, The Calculus of Computation, Springer, 2007
    locator: Chapter 11, Arrays (the quantifier-free procedure and the array property fragment with proofs)
---

The theory of arrays describes memory as a function from indices to values, with two operations: the read $a[i]$ (select) and the write $a\{i \leftarrow e\}$ (store), which returns a new array equal to $a$ except at $i$. Its axioms, the *read-over-write* axioms of McCarthy, say what a read after a write returns. Satisfiability of quantifier-free formulas in this theory is [NP-complete](/np-complete/) and reduces to [equality with uninterpreted functions](/euf-satisfiability/). With quantifiers, the full theory is undecidable, but the *array property fragment* of Bradley, Manna and Sipma (2006) allows the bounded universal statements that program proofs need, such as "the array is sorted between $\ell$ and $u$", and stays decidable.

## In plain words

An array is a row of boxes, each with a number written on it. Reading a box gives its content. Writing a value into a box gives a new row that is the same as the old one, except for that one box.

The rules are simple: if you write a value into a box and then read the same box, you get that value back; if you read a different box, you get what was there before. Two rows are equal if every box has the same content. Solvers use these rules to decide whether formulas about reads and writes can all be true, for example to check that a program never reads a wrong value from memory. Formulas that say "all boxes in a range have some property" are much harder, and only some kinds can be decided.

## Definition

The theory has three sorts: indices $I$, elements $E$, and arrays $A$, with the functions $\mathrm{read} : A \times I \to E$, written $a[i]$, and $\mathrm{write} : A \times I \times E \to A$, written $a\{i \leftarrow e\}$. Its axioms are:

1. **Read over write, same index.** $\forall a, i, j, e.\; i = j \rightarrow a\{i \leftarrow e\}[j] = e$.
2. **Read over write, other index.** $\forall a, i, j, e.\; i \ne j \rightarrow a\{i \leftarrow e\}[j] = a[j]$.
3. **Extensionality.** $\forall a, b.\; (\forall i.\; a[i] = b[i]) \rightarrow a = b$.

Without axiom 3 the theory is *non-extensional*. The index and element sorts can carry their own theories, for example integers with [linear arithmetic](/linear-integer-arithmetic-satisfiability/) for indices, or [bit-vectors](/bit-vector-satisfiability/) for both (QF_ABV, the memory of a machine). The problem: given a formula over these symbols (quantifier-free in QF_AX), decide whether it has a model of the axioms and the index and element theories.

**Array property fragment (Bradley, Manna and Sipma 2006, Definitions 4 and 5).** Take integer indices. An *array property* is a formula $\forall \bar\imath.\; (\varphi_I(\bar\imath) \rightarrow \varphi_V(\bar\imath))$, where

- the *index guard* $\varphi_I$ is built with $\wedge$ and $\vee$ from atoms $t \le t'$ and $t = t'$, where each $t$ is a universally quantified variable or a linear term over the existential (free) variables, with no arithmetic on the universal variables;
- in the *value constraint* $\varphi_V$, each universal variable occurs only as an array index $a[i]$, and reads are not nested ($a[b[i]]$ is not allowed).

The fragment is the set of existentially closed Boolean combinations of array properties and quantifier-free formulas. It expresses bounded equality $\forall i.\; \ell \le i \le u \rightarrow a[i] = b[i]$, extensionality, and sortedness $\forall i, j.\; \ell \le i \le j \le u \rightarrow a[i] \le a[j]$.

## Variants

- **QF_AX.** Quantifier-free, with uninterpreted index and element sorts.
- **QF_ALIA, QF_ABV, QF_AUFLIA.** Arrays combined with integer or bit-vector indices and elements and with uninterpreted functions, combined by [Nelson-Oppen](/nelson-oppen/) or model-based combination.
- **Extended array theories.** Constant arrays ($\forall i.\; K[i] = c$), pointwise maps of a function over arrays, and the default value, the combinatory array logic of de Moura and Bjørner (2009), still decidable in the quantifier-free case.
- **Array property fragment.** The decidable quantified fragment above.
- **Full first-order theory.** Undecidable, and even small extensions of the array property fragment are undecidable (see Bounds).

## Examples

Each example was checked by brute force over arrays of length 3 with values in $\{0, 1, 2\}$, or over small arrays as stated.

1. **A read-over-write conflict.** $a\{i \leftarrow e\}[j] = e \wedge i \ne j \wedge a[j] \ne e$ is unsatisfiable: by axiom 2 the read equals $a[j]$, which is not $e$.
2. **A valid identity.** $a\{i \leftarrow a[i]\} = a$ holds in each model, by axioms 1, 2 and 3.
3. **Commuting writes.** $a\{i \leftarrow x\}\{j \leftarrow y\} = a\{j \leftarrow y\}\{i \leftarrow x\}$ holds exactly when $i \ne j$ or $x = y$, so its negation together with $i \ne j$ is unsatisfiable.
4. **Sortedness (Bradley, Manna and Sipma 2006, Example 3).** The formula
$$w < x < y < z \wedge 0 < k < \ell < n \wedge \ell - k > 1 \wedge \mathrm{sorted}(0, n - 1, a\{k \leftarrow w\}\{\ell \leftarrow x\}) \wedge \mathrm{sorted}(0, n - 1, a\{k \leftarrow y\}\{\ell \leftarrow z\})$$
is unsatisfiable: an index $m$ with $k < m < \ell$ exists, and the two sorted arrays force $a[m] \le x < y \le a[m]$. A script found no model for $n \le 5$ and values in $[0, 4]$, and 30 models when the condition $\ell - k > 1$ is dropped, for example $n = 3$, $k = 1$, $\ell = 2$, $(w, x, y, z) = (0, 1, 2, 3)$, $a = (0, 0, 0)$. The procedure finds the contradiction only because step 2 below adds the index terms $k \pm 1$ and $\ell \pm 1$.

## Known algorithms

**Read-over-write rewriting.** The two axioms give the equivalence
$$a\{i \leftarrow e\}[j] \;=\; \mathrm{ite}(i = j,\; e,\; a[j]),$$
so each read of a write can be replaced by a case split. After all such rewrites, reads apply only to array variables, and each array variable $a$ can be replaced by an uninterpreted function $f_a$, which gives an [EUF](/euf-satisfiability/) formula, decided with [congruence closure](/congruence-closure/) or [Ackermannization](/ackermannization/). Each disequality $a \ne b$ between arrays becomes $a[k] \ne b[k]$ for a fresh index $k$, by extensionality.

**Procedure SAT_A for the array property fragment (Definition 9 of Bradley, Manna and Sipma).**

1. Expand defined predicates and put the formula in negation normal form.
2. Remove each write $a\{i \leftarrow e\}$: replace it by a fresh array $b$ and add $b[i] = e \wedge \forall j.\; (j \le i - 1 \vee i + 1 \le j) \rightarrow a[j] = b[j]$.
3. Replace each negated array property $\exists \bar\imath.\; \varphi_I \wedge \neg\varphi_V$ by a fresh instance.
4. Replace each array property by the conjunction of its instances over the *index set* $\mathcal{I}$: the terms read at ($t$ in some $a[t]$, other than universal variables) together with the terms in the index guards, or $\{0\}$ if there are none.
5. Replace reads by uninterpreted functions and decide the quantifier-free formula in the combination of EUF, [Presburger arithmetic](/presburger-arithmetic/) and the element theories.

**Lazy instantiation.** SMT solvers do not add all instances at once. They treat reads as fresh terms, and when the model found violates an axiom, they add the instance that is violated (lemmas on demand; de Moura and Bjørner 2009, and Brummayer and Biere in Boolector). General [quantifier instantiation](/quantifier-instantiation/) handles array properties outside the fragment, without a guarantee of termination.

## Bounds

**Theorem.** Satisfiability of quantifier-free formulas over arrays, with index and element theories whose quantifier-free problems are in NP and without equalities between arrays, is NP-complete.

*Proof.* *In NP.* Rewrite each read over a write with the $\mathrm{ite}$ equivalence above, introducing a fresh variable for each new $\mathrm{ite}$ term so that the size grows by a constant for each pair of a read and a write it passes through; this gives an equisatisfiable formula of polynomial size in which only array variables are read. Replacing these reads by uninterpreted functions gives a formula in the combination of EUF and the index and element theories, which is in NP by guessing the equalities between shared terms and checking each theory (the [Nelson-Oppen](/nelson-oppen/) argument for convex or stably infinite theories, or by [Ackermannization](/ackermannization/)). *NP-hard.* The Boolean structure alone encodes [SAT](/sat/). $\square$

Equalities between arrays and extensionality keep the problem in NP (Stump et al. 2001), by the fresh index for each disequality and by treating equal arrays as equal functions; the details need care when equal arrays are written to.

**The array property fragment (quoted from Bradley, Manna and Sipma 2006).**

- *Theorem 1.* If the quantifier-free combination of EUF, Presburger arithmetic and the element theories is decidable, then SAT_A decides the array property fragment: the formula is satisfiable if and only if the instantiated formula of step 5 is.
- *Theorem 2.* If that combination is in NP, then satisfiability of the fragment with a bounded number of universal variables in each property is NP-complete. The instantiation has size polynomial in the formula for a fixed height, since each property with $h$ universal variables gets $|\mathcal{I}|^h$ instances.
- *Theorem 3.* The $\exists^* \forall \exists$ fragment is undecidable, even with the syntactic restrictions of the fragment; the proof encodes the termination of linear loops over the integers.
- *Theorem 4.* Each of these extensions makes the fragment undecidable: nested reads such as $a[b[i]]$, reads indexed by a universal variable inside an index guard, and arithmetic on universal variables, even $a[i] \le a[i + 1]$ written with $i + 1$.

The key idea of the proof of Theorem 1 is that a model of the instantiated formula extends to a model of the array properties: each index that is not the value of a term in $\mathcal{I}$ is mapped to the closest index value below it that is in $\mathcal{I}$, and arrays are made constant between consecutive index values. Index guards are positive combinations of comparisons between universal variables and terms of $\mathcal{I}$, so a guard that holds at a point also holds at its projection; and since universal variables occur in value constraints only as indices of reads, the value constraint has the same truth value at the point and at its projection, where the instance in step 4 makes it true.

## Reductions

- **To EUF.** As above, by read-over-write rewriting; this is the eager method.
- **To SAT.** With bit-vector indices of small width, each array is a table of $2^w$ words and can be [bit-blasted](/bit-blasting/); for wide addresses the EUF reduction is used first.
- **From SAT.** Through the Boolean structure, or with element variables of a two-valued sort.
- **From program semantics.** Each assignment $a[i] := e$ becomes a write, and each loop invariant over a range becomes an array property, so the [verification conditions](/hoare-logic/) of many array programs fall into the fragment.

## Applications

- Modelling memory and the heap in software verification and [symbolic execution](/symbolic-execution/), as QF_ABV with 32 or 64 bit addresses and 8 bit values.
- Checking [loop invariants](/loop-invariant/) of sorting and searching programs, with sortedness, bounded equality and partitioning as array properties.
- Hardware verification of memories, register files and caches.
- Parameterized systems, where an array holds the state of each of $n$ processes.

## References
