---
tag: XZR3YW
kind: technique
slug: algorithmic-method
name: Algorithmic method
aliases:
- Williams' algorithmic method
area: complexity/fine-grained-complexity
level: research
summary: "Williams' method turns a satisfiability algorithm for a circuit class that beats brute force by a superpolynomial factor into a lower bound: NEXP, or NQP, has no such small circuits."
prereqs: [circuit-sat, circuit-complexity, time-hierarchy-theorem, nexptime]
see_also: [ac0, polynomial-method, quasi-polynomial-time, natural-proofs-barrier, strong-exponential-time-hypothesis, p-poly, apsp-conjecture, tc0]
sources:
  - paper: doi:10.1137/10080703X
    title: "R. Ryan Williams, Improving exhaustive search implies superpolynomial lower bounds, SIAM Journal on Computing 42(3), 2013, 1218-1244 (conference version in STOC 2010)"
    locator: the abstract and the main theorem on Circuit SAT in the introduction (a superpolynomial saving over 2^n for Circuit SAT gives NEXP not in P/poly)
  - paper: doi:10.1145/2559903
    title: "R. Ryan Williams, Nonuniform ACC circuit lower bounds, Journal of the ACM 61(1), 2014, 1-32 (conference version in CCC 2011)"
    locator: the abstract (NEXP has no polynomial size ACC circuits; E^NP has no ACC circuits of size 2^(n^o(1)); the SAT algorithm combines properties of ACC with fast rectangular matrix multiplication and dynamic programming) and the ACC SAT algorithm in time 2^(n - n^delta)
  - paper: doi:10.1145/3188745.3188910
    title: "Cody Murray and R. Ryan Williams, Circuit lower bounds for nondeterministic quasi-polytime: an easy witness lemma for NP and NQP, STOC 2018, 890-901"
    locator: the main theorem (NQP is not in ACC0) and the easy witness lemma for NQP
  - paper: doi:10.1016/s0022-0000(02)00024-7
    title: "Russell Impagliazzo, Valentine Kabanets and Avi Wigderson, In search of an easy witness: exponential time vs. probabilistic polynomial time, Journal of Computer and System Sciences 65(4), 2002, 672-694 (conference version in CCC 2001)"
    locator: the easy witness lemma (if NEXP is in P/poly, then NEXP verifiers have witnesses that are truth tables of small circuits)
  - paper: "Amir Abboud, Thomas Dueholm Hansen, Virginia Vassilevska Williams and Ryan Williams, Simulating branching programs with edit distance and friends, or: a polylog shaved is a lower bound made, Proceedings of the 48th ACM Symposium on Theory of Computing (STOC 2016), 375-388"
    locator: the abstract (saving enough polylogarithmic factors for edit distance or LCS gives circuit lower bounds for NEXP)
  - paper: doi:10.1137/15M1024524
    title: "R. Ryan Williams, Faster all-pairs shortest paths via circuit complexity, SIAM Journal on Computing 47(5), 2018, 1965-1985 (conference version in STOC 2014)"
    locator: the main theorem (APSP in n^3 / 2^(Omega(sqrt(log n))) time, through a circuit representation of the min-plus product)
  - paper: arxiv:2610.06783
    title: "Josh Alman and Virginia Vassilevska Williams, Truly subquadratic 3SUM and truly subcubic APSP via triangles in sparse lopsided graphs, arXiv preprint, October 2026"
    locator: the introduction (exact triangle and APSP results, and the statement that SETH and OV are not affected); not yet refereed
---

The algorithmic method, due to Ryan Williams, proves circuit lower bounds from algorithms. It shows that a satisfiability algorithm for a class $\mathcal{C}$ of circuits that beats the brute force time $2^n$ by a superpolynomial factor implies that $\mathsf{NEXP}$ has no polynomial size circuits in $\mathcal{C}$. The proof is by contradiction: if $\mathsf{NEXP}$ had such circuits, the SAT algorithm would let a nondeterministic machine save time on every problem in $\mathsf{NEXP}$, which the nondeterministic time hierarchy forbids.

With this method Williams proved in 2011 that $\mathsf{NEXP}$ is not in $\mathsf{ACC}^0$, the first lower bound for that class after decades of effort. Murray and Williams extended it in 2018 to $\mathsf{NQP}$, nondeterministic quasi-polynomial time. The method links the search for faster algorithms, the subject of fine-grained complexity, to the oldest open problems of circuit complexity.

## In plain words

Suppose you can check whether a small electric circuit ever outputs 1 a little faster than by trying every input. This seems to be only a modest speedup for a search problem.

Williams showed that such a speedup has a large consequence. If some very hard problems could be solved by small circuits of that kind, then the fast checker would let a guessing machine solve those hard problems faster than a known theorem allows. So the hard problems cannot have small circuits of that kind.

In short: a better algorithm proves that something is hard. The speedup must be larger than any polynomial factor, but it may be very small compared with the brute force time.

## When it applies

- You have a circuit class $\mathcal{C}$, such as [ACC0](#the-class-acc0) or [TC0](/tc0/), and you want to show that some explicit problem has no small circuits in $\mathcal{C}$.
- You can design a SAT algorithm for $\mathcal{C}$: given a circuit with $n$ inputs, decide whether some input makes it output 1, in time $2^n / s(n)$ with $s(n)$ larger than every polynomial. A deterministic algorithm is needed for the simplest form.
- The class $\mathcal{C}$ is closed under a few simple operations, such as adding an AND or an OR at the top and putting constants on some inputs, so that the circuits built in the proof stay in $\mathcal{C}$ or in a class with a similar SAT algorithm.
- The target is a nondeterministic class with a time hierarchy, such as $\mathsf{NEXP}$, $\mathsf{NQP}$ or $\mathsf{E}^{\mathsf{NP}}$. The method does not give lower bounds for problems in $\mathsf{NP}$ or $\mathsf{P}$.

### The class ACC0

$\mathsf{ACC}^0$ is the class of circuit families of constant depth and polynomial size with gates AND, OR and NOT of unbounded fan-in and gates $\mathrm{MOD}_m$ for a constant $m$. A $\mathrm{MOD}_m$ gate outputs 1 when the number of its inputs that are 1 is divisible by $m$; conventions differ by a negation. It contains [AC0](/ac0/). For prime $m$, strong lower bounds were known since the 1980s. For composite $m$, such as 6, Williams notes that before his work it was not known whether $\mathsf{EXP}^{\mathsf{NP}}$ has depth-3 polynomial size circuits made only of $\mathrm{MOD}_6$ gates.

## The template

The proof assumes the lower bound is false and builds a nondeterministic algorithm that is too fast.

```pseudo id=template
DECIDE-L(x)                          ▷ L ∈ NTIME[2^n] is hard by HIERARCHY; |x| = n
L1  D ← SUCCINCT-INSTANCE(x)          ▷ a circuit of size poly(n) that describes a 3-CNF
                                      ▷   formula F_x with 2^n poly(n) clauses; x ∈ L iff F_x is satisfiable
L2  guess W, a C-circuit of size poly(n) ▷ WITNESS-LEMMA: if NTIME[2^n] ⊆ C, a satisfying
                                      ▷   assignment of F_x is the truth table of such a W
L3  if C is weaker than general circuits then
L4      guess a C-circuit D' and check D' ≡ D with calls to SAT-ALG
L5  E(i) ← "clause i of F_x, read from D', is false under W"   ▷ a circuit with n + O(log n) inputs
L6  if SAT-ALG(E) reports that E is satisfiable then reject   ▷ time 2^n / s(n)
L7  accept                             ▷ total time 2^n poly(n) / s(n)
```

The holes are:

- **The class $\mathcal{C}$** and its closure properties.
- **SAT-ALG**, a satisfiability algorithm for the circuits $E$ built on line L5, with saving $s(n)$.
- **WITNESS-LEMMA**, a theorem that turns "the class has small circuits" into "the witnesses of the verifier have small circuits". For $\mathsf{NEXP}$ and general circuits this is the easy witness lemma of Impagliazzo, Kabanets and Wigderson (2002).
- **HIERARCHY**, the nondeterministic time hierarchy theorem, which gives a language in $\mathsf{NTIME}[2^n]$ that is not in $\mathsf{NTIME}[2^n / s'(n)]$ for a suitable $s'$; see [time hierarchy theorem](/time-hierarchy-theorem/).

**Why it works.** Every path of the guesses that accepts has checked that $W$ satisfies all clauses of $F_x$, so it accepts only if $x \in L$. If $x \in L$, then under the assumption some guess $W$ is a satisfying assignment, and $D'$ exists, so some path accepts. The time is $\mathrm{poly}(n)$ for the guesses and $2^n \mathrm{poly}(n) / s(n)$ for the calls of SAT-ALG. If $s(n)$ grows faster than every polynomial, this puts $L$ in $\mathsf{NTIME}[2^n / s'(n)]$, against HIERARCHY. So the assumption fails: $\mathsf{NTIME}[2^n]$, and with it $\mathsf{NEXP}$, is not in $\mathcal{C}$.

## Classic examples

### Circuit SAT and P/poly

Williams (STOC 2010, SIAM J. Comput. 2013). Here $\mathcal{C}$ is all circuits of polynomial size, so line L4 is not needed. The result: if [Circuit SAT](/circuit-sat/) for circuits with $n$ inputs and size polynomial in $n$ can be solved in time $2^n / s(n)$ for a superpolynomial $s$, then $\mathsf{NEXP} \not\subseteq$ [P/poly](/p-poly/). This is conditional on the algorithm, which nobody has. The abstract also states that minor algorithmic improvements over the trivial deterministic simulation of some classes would already give lower bounds such as $\mathsf{NEXP} \not\subseteq \mathsf{P/poly}$ and $\mathsf{LOGSPACE} \neq \mathsf{NP}$.

### ACC0 and NEXP

Williams (CCC 2011, J. ACM 2014). For $\mathsf{ACC}^0$ circuits of depth $d$ and size $2^{n^{\varepsilon}}$, Williams gives a deterministic SAT algorithm in time $2^{n - n^{\delta}}$ for some $\delta > 0$ that depends on $d$, $m$ and $\varepsilon$. It writes the circuit as a symmetric function applied to many ANDs of few inputs each, by known structure results for $\mathsf{ACC}^0$, and evaluates it on all inputs at once with fast rectangular matrix multiplication and dynamic programming. The saving $2^{n^{\delta}}$ is superpolynomial, so the template gives an unconditional result: $\mathsf{NEXP}$ has no polynomial size $\mathsf{ACC}^0$ circuits. The same argument shows that $\mathsf{E}^{\mathsf{NP}}$ has no $\mathsf{ACC}^0$ circuits of size $2^{n^{o(1)}}$.

### ACC0 and NQP

Murray and Williams (STOC 2018). They prove an easy witness lemma for $\mathsf{NP}$ and $\mathsf{NQP}$, the class of problems solvable in nondeterministic time $2^{(\log n)^{O(1)}}$, and use it as WITNESS-LEMMA in the template, with the ACC SAT algorithm above. The result is unconditional: $\mathsf{NQP}$ is not in $\mathsf{ACC}^0$. Since $\mathsf{NQP}$ is much smaller than $\mathsf{NEXP}$, this moves the lower bound much closer to $\mathsf{NP}$. See [quasi-polynomial time](/quasi-polynomial-time/).

## Variations

- **Fine-grained algorithms.** Abboud, Hansen, Vassilevska Williams and Williams (STOC 2016) show that saving enough polylogarithmic factors over the quadratic time for edit distance or LCS would give, through this method, new circuit lower bounds for $\mathsf{NEXP}$. So some conditional lower bounds of fine-grained complexity are backed by circuit complexity, not only by SETH.
- **The reverse direction.** Tools from circuit complexity also give algorithms. Williams (STOC 2014) writes the min-plus product as a small circuit of a kind that can be evaluated fast with the [polynomial method](/polynomial-method/), and so solves APSP in time $n^3 / 2^{\Omega(\sqrt{\log n})}$. This is the best bound for APSP before 2026; see [APSP conjecture](/apsp-conjecture/).
- **Other classes.** The same template works for any class with a nontrivial SAT algorithm and the needed closure properties. The lower bound is only as strong as the class.
- **The 2026 preprints.** Alman and Vassilevska Williams (arXiv:2610.06783) and Chan, Itakura, Ma and Yu (arXiv:2610.42012), both not yet refereed, refute the 3SUM conjecture, the APSP conjecture and the weighted k-clique hypotheses. They give no faster SAT algorithm for a circuit class, and Alman and Vassilevska Williams state that SETH and OV are not affected. So the preprints give no new circuit lower bound by this method.

## Pitfalls

- **The saving must be superpolynomial.** A saving of $n^{10}$ is not enough: the proof spends polynomial time on the guesses and on the construction, and the hierarchy theorem needs a gap larger than those factors. A saving of $2^{n^{\delta}}$ is enough.
- **The class must be closed.** The circuit $E$ on line L5 combines $W$, $D'$ and a check of three literals. If $\mathcal{C}$ is not closed under this, SAT-ALG must handle a larger class.
- **The target is nondeterministic and large.** The method gives lower bounds for $\mathsf{NEXP}$, $\mathsf{NQP}$ and similar classes, not for $\mathsf{NP}$. Proving that $\mathsf{NP}$ is not in $\mathsf{ACC}^0$ is still open.
- **Conditional and unconditional.** "A fast Circuit SAT algorithm implies $\mathsf{NEXP} \not\subseteq \mathsf{P/poly}$" is a conditional statement. "$\mathsf{NEXP} \not\subseteq \mathsf{ACC}^0$" is unconditional, because the ACC SAT algorithm exists.
- **Barriers.** The method combines an algorithm with diagonalization. It is not a direct combinatorial argument about circuits, so the [natural proofs barrier](/natural-proofs-barrier/) must be checked for each use, not assumed to apply.

## Exercises

1. Let $s(n) = 2^{n^{\delta}}$ and let the proof lose a factor $n^c$. For $\delta = 0.5$ and $c = 10$, find the least $\log_2 n$ where the saving is larger than the loss. (A run gives about 14.3; for $\delta = 0.1$ it gives about 99.6.)
2. Explain why a SAT algorithm with time $2^n / n^{100}$ for general circuits does not give $\mathsf{NEXP} \not\subseteq \mathsf{P/poly}$ by the template.
3. Show that $\mathsf{AC}^0 \subseteq \mathsf{ACC}^0$, and that the parity of $n$ bits is in $\mathsf{ACC}^0$ with one $\mathrm{MOD}_2$ gate.
4. In the template, why must SAT-ALG be run on $E$ and not on the 3-CNF formula $F_x$ itself? How many clauses does $F_x$ have?
5. Why does the method need a witness lemma? What goes wrong if the guess on line L2 is a full assignment of $2^n$ bits?
6. Williams' APSP algorithm and the ACC SAT algorithm both use fast matrix multiplication. Name the step in each where it is used.

## References
