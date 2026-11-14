---
tag: M7MW7Q
kind: theorem
slug: ml-typability-dexptime-completeness
name: DEXPTIME-completeness of ML typability
aliases:
- Mairson's theorem on ML typing
area: compilers-and-program-analysis/type-systems-and-inference
level: advanced
summary: Deciding whether an ML program is typable is complete for deterministic exponential time, since nested lets can double type sizes.
prereqs: [hindley-milner-type-system, exptime, type-inference-problem]
see_also: [let-polymorphism, algorithm-w, algorithm-j, principal-type-theorem, polymorphic-recursion-undecidability, time-hierarchy-theorem, turing-machine, polynomial-time-reduction]
sources:
  - paper: doi:10.1145/96709.96748
    title: Harry G. Mairson, Deciding ML typability is complete for deterministic exponential time, Seventeenth ACM Symposium on Principles of Programming Languages (POPL 1990), pages 382 to 401
    locator: the DEXPTIME-hardness proof by simulation of an exponential time Turing machine with nested let
  - paper: doi:10.1007/3-540-52590-4_50
    title: A. J. Kfoury, J. Tiuryn and P. Urzyczyn, ML typability is DEXPTIME-complete, CAAP 1990, Lecture Notes in Computer Science 431, pages 206 to 220
    locator: the main theorem, with ML typability shown log-space equivalent to acyclic semi-unification
  - paper: "A. J. Kfoury, J. Tiuryn and P. Urzyczyn, An analysis of ML typability, Journal of the ACM 41(2), 1994, pages 368 to 398"
    locator: the journal version of the CAAP 1990 paper, with the full proofs
  - book: isbn:9780262162098
    title: Benjamin C. Pierce, Types and Programming Languages, MIT Press, 2002
    locator: Section 22.7 (typing let by substitution, and the remark that nested lets make types exponentially large)
  - paper: doi:10.1007/3-540-44881-0_31
    title: David McAllester, A logical algorithm for ML type inference, Rewriting Techniques and Applications (RTA 2003), Lecture Notes in Computer Science 2706, pages 436 to 451
    locator: the nearly linear time bound for programs whose types have bounded order and arity
---

Deciding whether a program of core ML has a type is complete for DEXPTIME, the class of problems that a deterministic machine solves in time $2^{n^k}$ for some fixed $k$. The upper bound comes from typing each `let` as if its definition were copied at each use. The lower bound simulates any exponential time Turing machine by a short ML term whose type inference does the computation. Mairson (1990) and Kfoury, Tiuryn and Urzyczyn (1990) proved the result independently. It explains why [algorithm W](/algorithm-w/) is exponential in the worst case, and it shows that no faster algorithm exists. In practice the hard terms do not occur, and ML compilers infer types quickly.

## Statement

*ML typability* is the problem: given a closed term $e$ of the [Hindley-Milner type system](/hindley-milner-type-system/), with `fun`, application, `let`, constants, `if` and operators, decide whether $\vdash e : \tau$ for some type $\tau$. Write $n = |e|$ for the number of nodes of $e$. DEXPTIME, also written [EXPTIME](/exptime/), is $\bigcup_k \mathrm{DTIME}(2^{n^k})$.

**Theorem (Mairson 1990; Kfoury, Tiuryn and Urzyczyn 1990).**

1. *Upper bound.* ML typability can be decided in time $2^{O(n)}$.
2. *Lower bound.* For each problem $L$ in DEXPTIME there is a function $f$, computable in polynomial time, such that $w \in L$ if and only if the term $f(w)$ is typable. So ML typability is DEXPTIME-hard under [polynomial-time reductions](/polynomial-time-reduction/), and with part 1 it is DEXPTIME-complete.
3. *Size of types.* The principal type of a typable term has $2^{O(n)}$ nodes when equal subtrees are shared, and $2^{2^{O(n)}}$ nodes when it is written as a tree. Both bounds are reached.

## In plain words

An ML compiler finds the types of a program with no help. This theorem says how hard that job can be in the worst case.

The answer is: exponentially hard. When a helper function is defined with `let` and used twice, the compiler in effect types two copies of it. If each helper is built from two uses of the one before, the copies double at each level. A short program can then stand for an enormous one.

The hard direction shows that this doubling is strong enough to run any computer program that finishes in exponential time. True and false become two shapes of type, gates become small functions, and the compiler's matching of types does the computing. So a fast type checker for ML would give a fast way to run all those programs, and that is known to be impossible.

## Proof

The full argument is in the [proof file](proofs/main.md). Here is its structure.

**Upper bound.** The key fact is that `let` is typed by copying: $\texttt{let } x = e_1 \texttt{ in } e_2$ has the type $\tau$ exactly when $e_1$ has some type and $[x := e_1]\,e_2$ has the type $\tau$ (Pierce, Section 22.7). The proof of the "if" direction uses the [principal type theorem](/principal-type-theorem/): all types of the copies are instances of one scheme of $e_1$. Expanding every `let` in this way, with an extra unused argument so that an unused definition is still checked, gives a term with no `let` and with the same types. Its size is at most $4^n$, by induction on the term. A term with no `let` is typable exactly when a set of $O(N)$ equations has a unifier, and unification on a [term DAG](/term-dag/) solves this in almost linear time. So the total time is $2^{O(n)}$.

**Size bounds.** The expanded term has at most $4^n$ nodes, so the unification DAG and the principal type have $2^{O(n)}$ nodes. A DAG with $D$ nodes unfolds to a tree with at most $2^{D+1}$ nodes. The family $f_0 = $ `fun x -> fun z -> z x x`, $f_i = $ `fun y -> f(i-1) (f(i-1) y)` reaches both bounds: its term has $7k + 9$ nodes, and its principal type has $2^{k+2} + 2$ nodes as a DAG and $6 \cdot 2^{2^k} - 3$ nodes as a tree.

**Lower bound.** Take a deterministic [Turing machine](/turing-machine/) $M$ that runs in time $2^{p(n)}$, and an input $w$.

- *Truth values as types.* `fun x -> fun y -> x` has a type of the form $\alpha \to \beta \to \alpha$, and `fun x -> fun y -> y` one of the form $\alpha \to \beta \to \beta$. The test `(b 1 true) + 1` is typable for the first and not for the second.
- *Gates.* `not = fun p -> p f t`, `and = fun p -> fun q -> p q f` and `or = fun p -> fun q -> p t q` compute the right shape of result type by unification. Because a `fun`-bound variable has one type, each wire is used once, and fan-out goes through `copy = fun p -> p (pair t t) (pair f f)`.
- *Exponential size and time.* A step of $M$ on a tape of $2^{p(n)}$ cells is built level by level with `let`, each level from two uses of the one below. Then `let run_i = fun s -> run_(i-1) (run_(i-1) s)` repeats the step $2^{p(n)}$ times with only $p(n)$ definitions.
- *Correctness.* By the copying property, the term is typable exactly when its expansion is. In the expansion each `fun`-bound variable occurs at most once, and for such terms beta reduction keeps the types in both directions. The expansion reduces to `1 + 1` if $M$ accepts $w$, and to `true + 1` if not.

The proof file gives the upper bound and the size bounds in full, and the lower bound as a sketch. Mairson (1990) gives the complete simulation.

## Consequences

- **W is exponential, not cubic.** No algorithm decides ML typability in polynomial time, because DEXPTIME contains problems outside P by the [time hierarchy theorem](/time-hierarchy-theorem/). Every inference algorithm for HM, [W](/algorithm-w/), [J](/algorithm-j/) and the constraint-based ones, has an exponential worst case.
- **Sharing is needed for the upper bound.** An implementation that copies types as trees takes doubly exponential time on the family $f_k$. Algorithm J with union-find works on a DAG and stays within $2^{O(n)}$.
- **The hardness carries over.** Each language that contains core ML typing with polymorphic `let`, such as Standard ML, OCaml, F# and Haskell, has a DEXPTIME-hard type inference problem. Adding features can only make it harder: [polymorphic recursion](/polymorphic-recursion-undecidability/) makes it undecidable.
- **Error messages can be huge.** A type error in a term like $f_k$ can involve a type with millions of nodes. A compiler that prints types as trees can print output of doubly exponential size.

## Tightness

- **Without `let`.** Typability in the [simply typed lambda calculus](/simply-typed-lambda-calculus/) needs only one unification problem of linear size. It takes linear time with the [Paterson-Wegman algorithm](/paterson-wegman-unification/). So the whole cost comes from `let`-polymorphism.
- **Bounded nesting.** If the nesting depth of `let` is bounded by a constant $d$, the bound of Lemma 3 of the proof file becomes polynomial: each level of nesting at most squares the size, so the expansion has at most about $n^{2^{d}}$ nodes, and typability is in polynomial time. McAllester (2003) gives a nearly linear bound for programs whose types have bounded order and arity. Real programs are close to this case.
- **The size bounds are exact in form.** The family $f_k$ has a principal type of DAG size $2^{\Theta(n)}$ and tree size $2^{2^{\Theta(n)}}$.
- **Checking a given type** is no easier in general: given $e$ and $\tau$, deciding $\vdash e : \tau$ is also DEXPTIME-hard, since the term of the lower bound has type $\mathsf{int}$ when it has a type at all.

## History

Milner (1978) gave algorithm W. It was fast on real programs, and for about ten years its worst case was not known. Kanellakis and Mitchell (1989) showed that ML typability is PSPACE-hard. In 1990, Mairson closed the gap with DEXPTIME-hardness, by a direct simulation of Turing machines, and Kfoury, Tiuryn and Urzyczyn proved the same result independently. Their proof shows that ML typability is equivalent to acyclic semi-unification, a restricted form of the [semi-unification problem](/semi-unification-problem/). The journal version appeared in 1994. McAllester (2003) explained the good behavior in practice by a bound that is nearly linear when the order and arity of types are bounded.

## References
