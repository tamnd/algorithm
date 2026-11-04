---
tag: 3F82GZ
kind: concept
slug: separation-logic
name: Separation logic
aliases:
- Concurrent separation logic
area: foundations/correctness-and-invariants
level: research
summary: An extension of Hoare logic for reasoning about heap-manipulating programs with disjoint memory regions.
prereqs: [hoare-triple, hoare-logic, partial-correctness]
see_also: [program-verification, linked-list, singly-linked-list, loop-invariant, refinement-calculus, weakest-precondition]
sources:
  - paper: "R. M. Burstall, Some techniques for proving correctness of programs which alter data structures, Machine Intelligence 7, Edinburgh University Press (1972)"
    locator: pp. 23 to 50 (distinct nonrepeating list systems, an early form of disjointness)
  - paper: "John C. Reynolds, Intuitionistic reasoning about shared mutable data structure, in Millennial Perspectives in Computer Science, Palgrave (2000)"
    locator: pp. 303 to 321 (the first form of the separating conjunction, in an intuitionistic logic)
  - paper: doi:10.1145/360204.375719
    title: Samin Ishtiaq and Peter W. O'Hearn, BI as an assertion language for mutable data structures, POPL 2001
    locator: pp. 14 to 26 (the logic of bunched implications as the assertion language, the magic wand, the classical model)
  - paper: doi:10.1007/3-540-44802-0_1
    title: Peter W. O'Hearn, John C. Reynolds and Hongseok Yang, Local reasoning about programs that alter data structures, CSL 2001, LNCS 2142, Springer
    locator: pp. 1 to 19 (the small axioms, the frame rule and its soundness)
  - paper: doi:10.1109/LICS.2002.1029817
    title: John C. Reynolds, Separation logic, a logic for shared mutable data structures, LICS 2002, IEEE
    locator: pp. 55 to 74 (the model, the assertions, the rules, list segments, the reversal of a list)
  - paper: doi:10.1007/3-540-45931-6_28
    title: Hongseok Yang and Peter W. O'Hearn, A semantic basis for local reasoning, FoSSaCS 2002, LNCS 2303, Springer
    locator: pp. 402 to 416 (safety monotonicity and the frame property)
  - paper: doi:10.1016/j.tcs.2006.12.035
    title: Peter W. O'Hearn, Resources, concurrency, and local reasoning, Theoretical Computer Science 375(1-3) (2007)
    locator: pp. 271 to 307 (concurrent separation logic, the parallel rule, resource invariants, precision)
  - paper: doi:10.1016/j.tcs.2006.12.034
    title: Stephen Brookes, A semantics for concurrent separation logic, Theoretical Computer Science 375(1-3) (2007)
    locator: pp. 227 to 270 (the soundness of concurrent separation logic with precise resource invariants)
  - paper: doi:10.1145/1480881.1480917
    title: Cristiano Calcagno, Dino Distefano, Peter W. O'Hearn and Hongseok Yang, Compositional shape analysis by means of bi-abduction, POPL 2009
    locator: pp. 289 to 300 (bi-abduction, the analysis behind Infer)
  - paper: doi:10.1007/978-3-319-17524-9_1
    title: Cristiano Calcagno and others, Moving fast with software verification, NFM 2015, LNCS 9058, Springer
    locator: pp. 3 to 11 (Infer at Facebook)
  - paper: doi:10.1007/978-3-642-20398-5_4
    title: Bart Jacobs, Jan Smans, Pieter Philippaerts, Frederic Vogels, Willem Penninckx and Frank Piessens, VeriFast, a powerful, sound, predictable, fast verifier for C and Java, NFM 2011, LNCS 6617, Springer
    locator: pp. 41 to 55
  - paper: doi:10.1017/S0956796818000151
    title: Ralf Jung, Robbert Krebbers, Jacques-Henri Jourdan, Ales Bizjak, Lars Birkedal and Derek Dreyer, Iris from the ground up, a modular foundation for higher-order concurrent separation logic, Journal of Functional Programming 28 (2018)
    locator: article e20
  - paper: doi:10.1145/3211968
    title: Peter W. O'Hearn, Separation logic, Communications of the ACM 62(2) (2019)
    locator: pp. 86 to 95 (a survey of the logic, its history and its tools)
---

Separation logic is an extension of [Hoare logic](/hoare-logic/) for programs that read and write a heap through pointers. Its new assertion $P * Q$ says that the heap splits into two parts with no common cell, one for $P$ and one for $Q$. A rule called the frame rule then lets a proof about a small part of the heap carry over to every larger heap. Reynolds (2000), Ishtiaq and O'Hearn (2001), O'Hearn, Reynolds and Yang (2001) and Reynolds (2002) set out the logic. O'Hearn (2007) extended it to concurrent programs.

## In plain words

A program with pointers can have two names for one cell. When it writes through one name, a fact about the other name may become false. In plain Hoare logic you must then say, for each pair of pointers, that they are different. These side facts grow fast, and they hide the main idea of the proof.

Separation logic uses another way. A fact about memory also says which cells it owns. Two facts joined by the new connective own cells that do not overlap. So a program that works only on its own cells cannot break a fact about other cells.

This gives local reasoning. You prove a small specification for the cells that a piece of code touches. The frame rule then adds the rest of memory, and you know that the rest stays as it was. You still must prove that the code touches no other cell: the logic makes this part of what a triple means.

## The idea

**History.** Burstall (1972) already reasoned about lists whose nodes are distinct. Reynolds (2000) gave a first form of the separating conjunction in an intuitionistic logic. Ishtiaq and O'Hearn (2001) took the assertion language from the logic of bunched implications and gave the classical model used on this page. O'Hearn, Reynolds and Yang (2001) gave the small axioms and the frame rule, and Reynolds (2002) gave the survey that fixed the name.

**The model.** A *store* $s$ gives a value to each variable. A *heap* $h$ is a finite partial function from addresses (positive integers) to values. The value $\mathit{nil}$ is $0$, and it is not an address. Write $h_1 \perp h_2$ when the domains of $h_1$ and $h_2$ are disjoint, and $h_1 \uplus h_2$ for the union of such heaps. A state is a pair $(s, h)$.

**Assertions.** The assertions are first-order formulas plus these forms. Here $e$, $f$ and $g$ are expressions over the store. A formula without these forms, such as $x = 1$, is *pure*: it says nothing about the heap, and it holds in a state for each heap.

- $\mathit{emp}$ holds in $(s, h)$ when $h$ is the empty heap.
- $e \mapsto f$ holds when the domain of $h$ is exactly one address, the value of $e$, and $h$ maps it to the value of $f$. This is the *points-to* assertion.
- $e \mapsto f, g$ abbreviates $e \mapsto f * e + 1 \mapsto g$. It describes two adjacent cells.
- $e \mapsto -$ abbreviates $\exists v \cdot e \mapsto v$.
- $P * Q$, the *separating conjunction*, holds in $(s, h)$ when there are $h_1, h_2$ with $h_1 \perp h_2$, $h = h_1 \uplus h_2$, $(s, h_1) \models P$ and $(s, h_2) \models Q$.
- $P \mathrel{-\!\!*} Q$, the *separating implication* or magic wand, holds in $(s, h)$ when for each $h'$ with $h' \perp h$ and $(s, h') \models P$ we have $(s, h \uplus h') \models Q$. It is used for weakest preconditions; the proofs on this page do not need it.

The assertion $x \mapsto 1 * y \mapsto 2$ implies $x \ne y$, since the two cells are different. The assertion $x \mapsto 1 \wedge y \mapsto 2$ is false in each state: a heap that satisfies both has the one cell $x$ and the one cell $y$, so $x = y$, and this cell would hold both $1$ and $2$. The operator $*$ is commutative and associative, and $\mathit{emp}$ is its unit. The formula $P * P$ does not follow from $P$: $x \mapsto 1 * x \mapsto 1$ is false, because one cell cannot be split into two.

**Triples.** The triple $\{P\}\ C\ \{Q\}$ has a stronger meaning than in Hoare logic. It holds when, for each state $(s, h)$ that satisfies $P$, the command $C$ does not fault, and each state in which it stops satisfies $Q$. A command faults when it reads, writes or frees an address that is not in the current heap. So $P$ must describe all the memory that $C$ touches. Termination is not part of the meaning, as in [partial correctness](/partial-correctness/).

**Small axioms.** Each axiom names only the cells that the command uses. Write $[e]$ for the cell at address $e$. In the load and allocation axioms, the variable $x$ does not occur in $e$, $f$, $g$ or $v$.

$$ \{e \mapsto -\}\ [e] \leftarrow f\ \{e \mapsto f\} \qquad \{e \mapsto v\}\ x \leftarrow [e]\ \{e \mapsto v \wedge x = v\} $$

$$ \{\mathit{emp}\}\ x \leftarrow \mathbf{cons}(f, g)\ \{x \mapsto f, g\} \qquad \{e \mapsto -\}\ \mathbf{dispose}(e)\ \{\mathit{emp}\} $$

The command $\mathbf{cons}$ takes two adjacent fresh cells, and $\mathbf{dispose}$ gives one cell back. The precondition $e \mapsto -$ of the store is needed: if $e$ is not in the heap, the store faults, so no triple with a weaker precondition such as $\mathit{emp}$ can hold. The rules for assignment, sequence, conditional, loop and consequence are the rules of Hoare logic.

**The frame rule.**

$$ \frac{\{P\}\ C\ \{Q\}}{\{P * R\}\ C\ \{Q * R\}} \qquad \text{when } C \text{ changes no variable that is free in } R. $$

The condition on variables is needed because $R$ talks about the store as well as the heap. The rule is sound because of two facts about each command $C$ of the language, which Yang and O'Hearn (2002) state as *safety monotonicity* and the *frame property*. First, if $C$ does not fault from $(s, h)$, it does not fault from $(s, h \uplus h')$ for each $h' \perp h$. Second, each run from $(s, h \uplus h')$ that stops is a run from $(s, h)$ with the cells of $h'$ added unchanged. So the cells that $R$ describes are not read, written or freed, and $R$ still holds at the end. The fault-avoiding meaning of triples is what makes this work: if a triple allowed $C$ to touch cells outside $P$, the first fact would fail.

**Linked lists.** Let a node at address $x$ use two cells: $x$ holds the data and $x + 1$ holds the pointer to the next node. For a sequence $\alpha$ of values define, by recursion on $\alpha$, the assertions

$$ \mathit{list}([\,], x) \equiv x = \mathit{nil} \wedge \mathit{emp}, \qquad \mathit{list}(a :: \alpha, x) \equiv \exists n \cdot x \mapsto a, n * \mathit{list}(\alpha, n). $$

The list segment from $x$ to $y$ has the same definition with $\mathit{lseg}([\,], x, y) \equiv x = y \wedge \mathit{emp}$ and $\mathit{lseg}(a :: \alpha, x, y) \equiv \exists n \cdot x \mapsto a, n * \mathit{lseg}(\alpha, n, y)$. So $\mathit{list}(\alpha, x)$ is $\mathit{lseg}(\alpha, x, \mathit{nil})$. The segments join: $\mathit{lseg}(\alpha, x, y) * \mathit{lseg}(\beta, y, z) \implies \mathit{lseg}(\alpha \mathbin{+\!\!+} \beta, x, z)$. The proof is by induction on $\alpha$. For $\alpha = [\,]$ the left side is $(x = y \wedge \mathit{emp}) * \mathit{lseg}(\beta, y, z)$, which is $\mathit{lseg}(\beta, x, z)$. For $\alpha = a :: \alpha'$ unfold the first segment to $x \mapsto a, n * \mathit{lseg}(\alpha', n, y)$, join the inner part by the induction hypothesis, and fold again.

Because $\mathit{nil}$ is not an address, $\mathit{list}(a :: \alpha, \mathit{nil})$ is false, and $\mathit{list}(\alpha, x)$ with $x \ne \mathit{nil}$ forces $\alpha$ to be non-empty. The nodes of $\mathit{list}(\alpha, x)$ are pairwise distinct, because each one owns its own cells, and the last one points to $\mathit{nil}$. So the list has no cycle. The assertion $\mathit{list}(\alpha, x) * \mathit{list}(\beta, y)$ says that the two lists do not share a node.

**Concurrency.** In concurrent separation logic (O'Hearn 2007) the rule for parallel composition is

$$ \frac{\{P_1\}\ C_1\ \{Q_1\} \qquad \{P_2\}\ C_2\ \{Q_2\}}{\{P_1 * P_2\}\ C_1 \parallel C_2\ \{Q_1 * Q_2\}} $$

when no variable that $C_1$ changes is free in $P_2$, $C_2$ or $Q_2$, and the same with 1 and 2 swapped. The two threads own disjoint heaps, so they cannot disturb each other. Shared data sits in a *resource* with an invariant. A thread that enters a critical region takes the cells of the invariant into its own heap, and it must give back cells that satisfy the invariant when it leaves. So ownership of cells can move from one thread to another. Brookes (2007) proved the logic sound when each resource invariant is *precise*: in each state at most one part of the heap satisfies it.

**Pitfalls.**

- *$\wedge$ in place of $*$.* The formula $P \wedge Q$ makes both assertions talk about the same heap. For two cells, $x \mapsto 1 \wedge y \mapsto 2$ is false. The formula $(x \mapsto 1 * \mathit{true}) \wedge (y \mapsto 1 * \mathit{true})$ holds in a heap with one cell when $x = y$, while $x \mapsto 1 * y \mapsto 1 * \mathit{true}$ forces $x \ne y$. Use $*$ when the parts must be disjoint.
- *A frame that mentions a changed variable.* From $\{\mathit{emp}\}\ x \leftarrow 1\ \{\mathit{emp} \wedge x = 1\}$ the frame $R = (x = 0)$ would give $\{\mathit{emp} \wedge x = 0\}\ x \leftarrow 1\ \{\mathit{emp} \wedge x = 1 \wedge x = 0\}$, whose postcondition is false. The side condition of the frame rule forbids this frame.
- *A precondition that is too small.* A triple about $[e] \leftarrow f$ must own the cell $e$. A specification that leaves out a cell the code touches does not hold, because the code faults.
- *Segments may be cycles.* $\mathit{lseg}(\alpha, x, y)$ does not say that $y$ lies outside the segment. For example, $\mathit{lseg}([a], x, x)$ holds for the one node $x \mapsto a, x$, a cycle of length 1. Only $\mathit{list}$, which ends in $\mathit{nil}$, rules out cycles.
- *Imprecise resource invariants.* Reynolds found that with an invariant that is not precise, concurrent separation logic plus the usual conjunction rule proves a false triple. O'Hearn (2007) discusses the example, and Brookes's proof needs precision.
- *Termination.* As in Hoare logic, a triple does not say that the program stops. Absence of faults is proved, termination is not; it needs a [variant function](/variant-function/).

## Examples

**In-place reversal of a list.** The program reverses the list at $i$ by changing the next pointers of its nodes. It uses the variables $i$, $j$, $k$.

$$ j \leftarrow \mathit{nil}\ ;\ \mathbf{while}\ i \ne \mathit{nil}\ \mathbf{do}\ (k \leftarrow [i + 1]\ ;\ [i + 1] \leftarrow j\ ;\ j \leftarrow i\ ;\ i \leftarrow k) $$

Let $\alpha_0$ be a logical variable for the initial sequence, and write $\mathrm{rev}(\alpha)$ for the reversed sequence. The specification is

$$ \{\mathit{list}(\alpha_0, i)\}\ \text{reverse}\ \{\mathit{list}(\mathrm{rev}(\alpha_0), j)\}. $$

The loop invariant $I$ is

$$ \exists \alpha, \beta \cdot \bigl(\mathit{list}(\alpha, i) * \mathit{list}(\beta, j)\bigr) \wedge \mathrm{rev}(\alpha_0) = \mathrm{rev}(\alpha) \mathbin{+\!\!+} \beta. $$

The list at $i$ is the part not yet moved, and the list at $j$ is the reversed part. The proof has three parts.

- *Entry.* After $j \leftarrow \mathit{nil}$ the heap satisfies $\mathit{list}(\alpha_0, i) * \mathit{list}([\,], j)$, since $\mathit{list}([\,], \mathit{nil})$ is $\mathit{emp}$. Take $\alpha = \alpha_0$ and $\beta = [\,]$. Then $\mathrm{rev}(\alpha_0) = \mathrm{rev}(\alpha_0) \mathbin{+\!\!+} [\,]$.
- *Body.* Assume $I$ and $i \ne \mathit{nil}$. Then $\alpha$ is not empty, so $\alpha = a :: \alpha'$ for some $a$ and $\alpha'$. The assertions after each command are:

1. $\exists n \cdot \bigl(i \mapsto a, n * \mathit{list}(\alpha', n) * \mathit{list}(\beta, j)\bigr) \wedge \mathrm{rev}(\alpha_0) = \mathrm{rev}(\alpha') \mathbin{+\!\!+} [a] \mathbin{+\!\!+} \beta$ (unfolding the first list).
2. After $k \leftarrow [i + 1]$: the same, with $k = n$. The load axiom is used on the cell $i + 1$, and the frame rule carries the rest. Here $k$ is not free in the frame.
3. After $[i + 1] \leftarrow j$: $i \mapsto a, j * \mathit{list}(\alpha', k) * \mathit{list}(\beta, j)$. The store axiom is used on the cell $i + 1$, and the frame rule carries the rest.
4. By the definition of $\mathit{list}$, $i \mapsto a, j * \mathit{list}(\beta, j)$ implies $\mathit{list}(a :: \beta, i)$, with $j$ as the witness for $n$. So the state satisfies $\mathit{list}(\alpha', k) * \mathit{list}(a :: \beta, i)$.
5. After $j \leftarrow i$ and $i \leftarrow k$: $\mathit{list}(\alpha', i) * \mathit{list}(a :: \beta, j)$, and $\mathrm{rev}(\alpha_0) = \mathrm{rev}(\alpha') \mathbin{+\!\!+} (a :: \beta)$. This is $I$ with $\alpha'$ for $\alpha$ and $a :: \beta$ for $\beta$.

- *Exit.* From $I$ and $i = \mathit{nil}$: the formula $\mathit{list}(\alpha, \mathit{nil})$ forces $\alpha = [\,]$ and an empty heap for that part. So $\mathrm{rev}(\alpha_0) = \beta$ and the heap satisfies $\mathit{list}(\mathrm{rev}(\alpha_0), j)$.

Each pass takes one node off the list at $i$. The length of $\alpha$ is a [variant function](/variant-function/): it drops by 1 at each pass, so the loop stops.

**A trace.** Let the list at $i = 10$ hold $1, 2, 3$ in the nodes $10 \to 20 \to 30$, so the cells are $10{:}1,\ 11{:}20,\ 20{:}2,\ 21{:}30,\ 30{:}3,\ 31{:}\mathit{nil}$. The values at the start of each pass and at the end are:

| pass | $i$ | $j$ | $\alpha$ | $\beta$ | next cells $11, 21, 31$ |
|---|---|---|---|---|---|
| start | 10 | nil | $[1, 2, 3]$ | $[\,]$ | $20, 30, \mathit{nil}$ |
| after 1 | 20 | 10 | $[2, 3]$ | $[1]$ | $\mathit{nil}, 30, \mathit{nil}$ |
| after 2 | 30 | 20 | $[3]$ | $[2, 1]$ | $\mathit{nil}, 10, \mathit{nil}$ |
| after 3 | nil | 30 | $[\,]$ | $[3, 2, 1]$ | $\mathit{nil}, 10, 20$ |

At each row $\mathrm{rev}(\alpha) \mathbin{+\!\!+} \beta = [3, 2, 1]$, and the list at $j = 30$ is $30 \to 20 \to 10$ with data $3, 2, 1$.

**Local reasoning by the frame rule.** Let $p$ be a variable that the program does not change. The frame rule with $R = \mathit{list}(\gamma, p)$ gives

$$ \{\mathit{list}(\alpha_0, i) * \mathit{list}(\gamma, p)\}\ \text{reverse}\ \{\mathit{list}(\mathrm{rev}(\alpha_0), j) * \mathit{list}(\gamma, p)\}. $$

So a second list stays as it was, and it stays disjoint from the first. No proof about the second list is needed.

**A non-example: lists that share a node.** Let two lists have the nodes $100 \to 200$ and $110 \to 200$, with data $1, 3$ and $2, 3$. They share the node at $200$, so $\mathit{list}(\alpha, 100) * \mathit{list}(\beta, 110)$ is false, because no split of the heap gives each list its own cells. The reversal of the list at $100$ sets the next pointer of the node $100$ to $\mathit{nil}$ and that of the node $200$ to $100$. Afterwards the list at $110$ is $110 \to 200 \to 100$, with three nodes instead of two. The precondition with $*$ excludes this case, so the frame rule cannot be applied to it.

## Where it is used

- Automatic bug finding: the Infer analyzer uses separation logic with bi-abduction (Calcagno, Distefano, O'Hearn and Yang 2009) to find null dereferences and memory leaks, and it ran on Facebook code (Calcagno and others 2015).
- Verifiers for heap programs: VeriFast (Jacobs and others 2011) checks C and Java programs annotated with separation logic assertions. Iris (Jung and others 2018) is a framework for higher-order concurrent separation logic, built in Rocq.
- The proofs of code that manipulates pointers: lists, trees, allocators.
- Concurrent programs, where disjoint ownership of memory replaces global reasoning about all interleavings.
- It is one of the logics under [program verification](/program-verification/) tools for programs with pointers.

## References
