---
tag: CBPE10
kind: concept
slug: class-inclusions-chain
name: Known inclusions among classes
aliases:
- L ⊆ NL ⊆ P ⊆ NP ⊆ PSPACE ⊆ EXP
area: complexity/complexity-classes
level: intro
summary: "The chain L, NL, P, NP, PSPACE, EXP, each class inside the next. NL differs from PSPACE and P from EXP, so some steps are strict, but no single step is known to be strict."
prereqs: [p, np, exptime, complexity-class]
see_also: [logspace, nondeterministic-logspace, pspace, savitch-theorem, space-hierarchy-theorem, time-hierarchy-theorem, nexptime, ac0]
sources:
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Chapter 8 (space complexity, Savitch's theorem, the classes L and NL) and Section 9.1 (hierarchy theorems)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach
    locator: Section 2.6 (coNP, EXP and NEXP) and Chapter 4 (space complexity and configuration graphs)
  - book: isbn:9780201530827
    title: Christos H. Papadimitriou, Computational Complexity, Addison-Wesley, 1994
    locator: Chapter 7, Relations between complexity classes
  - paper: doi:10.1016/S0022-0000(70)80006-X
    title: Walter J. Savitch, Relationships between nondeterministic and deterministic tape complexities, Journal of Computer and System Sciences 4(2) (1970), 177 to 192
    locator: the main theorem
  - paper: doi:10.1090/S0002-9947-1965-0170805-7
    title: Juris Hartmanis and Richard E. Stearns, On the computational complexity of algorithms, Transactions of the American Mathematical Society 117 (1965), 285 to 306
    locator: the time hierarchy
---

The standard complexity classes form the chain $\mathsf{L} \subseteq \mathsf{NL} \subseteq \mathsf{P} \subseteq \mathsf{NP} \subseteq \mathsf{PSPACE} \subseteq \mathsf{EXP}$. Each inclusion has a short proof. The hierarchy theorems show that $\mathsf{NL} \ne \mathsf{PSPACE}$ and $\mathsf{P} \ne \mathsf{EXP}$, so some of the inclusions are strict, but for no single step of the chain is it known whether it is strict. This gap between what is proved and what is believed is the shape of most open questions in complexity theory.

## In plain words

Complexity classes sort problems by how much time or memory they need. The six classes in the chain go from very small memory, through reasonable time, to huge amounts of time. Each class sits inside the next one, because a machine with more resources can do everything that a machine with fewer resources can do.

Theory can prove that the chain does not collapse completely: the first classes are strictly smaller than the last ones. But it cannot yet say where the gaps are. Each single step could be an equality, as far as anyone has proved. Most researchers believe that every step is a real gap.

## The idea

### The classes

All classes are defined with multitape Turing machines on inputs of length $n$. For the space classes, the input is on a read-only tape and only the cells of the work tapes count.

| Class | Machine | Resource |
|---|---|---|
| [L](/logspace/) | deterministic | space $O(\log n)$ |
| [NL](/nondeterministic-logspace/) | nondeterministic | space $O(\log n)$ |
| [P](/p/) | deterministic | time $n^{O(1)}$ |
| [NP](/np/) | nondeterministic | time $n^{O(1)}$ |
| [PSPACE](/pspace/) | deterministic | space $n^{O(1)}$ |
| [EXP](/exptime/) | deterministic | time $2^{n^{O(1)}}$ |

### Why each inclusion holds

- $\mathsf{L} \subseteq \mathsf{NL}$ and $\mathsf{P} \subseteq \mathsf{NP}$: a deterministic machine is a nondeterministic machine with one choice at each step.
- $\mathsf{NL} \subseteq \mathsf{P}$: a *configuration* of a machine with space $s(n)$ is its state, the position of the input head, the positions of the work heads and the contents of the work tapes. For a machine with $q$ states, one work tape over $g$ symbols and space $s(n)$, there are at most $q \cdot (n + 2) \cdot s(n) \cdot g^{s(n)}$ configurations. For $s(n) = c \log n$ this number is a polynomial in $n$. The machine accepts $x$ exactly when the accepting configuration is reachable from the start configuration in the configuration graph, and breadth-first search decides [reachability](/graph-reachability/) in time polynomial in the size of the graph.
- $\mathsf{NP} \subseteq \mathsf{PSPACE}$: take a [verifier](/polynomial-time-verifier/) with certificates of length $p(n)$. A deterministic machine writes the certificates one after the other on the same $p(n)$ cells and runs the verifier on each, reusing its space. The verifier runs in polynomial time and so uses polynomial space.
- $\mathsf{PSPACE} \subseteq \mathsf{EXP}$: the same count of configurations gives $2^{O(s(n))}$ configurations for space $s(n) \ge \log n$. A machine that halts on every input never repeats a configuration, so it halts within $2^{O(n^k)}$ steps when $s(n) = n^k$.

The same arguments extend the chain: $\mathsf{EXP} \subseteq \mathsf{NEXP} \subseteq \mathsf{EXPSPACE}$. They also place the classes of complements: $\mathsf{P} \subseteq \mathsf{coNP} \subseteq \mathsf{PSPACE}$, see [coNP](/co-np/).

### What is known to be strict

- $\mathsf{NL} \ne \mathsf{PSPACE}$. By [Savitch's theorem](/savitch-theorem/), $\mathsf{NL} \subseteq \mathsf{DSPACE}(\log^2 n)$. By the [space hierarchy theorem](/space-hierarchy-theorem/), $\mathsf{DSPACE}(\log^2 n) \subsetneq \mathsf{DSPACE}(n) \subseteq \mathsf{PSPACE}$. So $\mathsf{L} \ne \mathsf{PSPACE}$ too.
- $\mathsf{P} \ne \mathsf{EXP}$. By the [time hierarchy theorem](/time-hierarchy-theorem/), $\mathsf{P} \subseteq \mathsf{DTIME}(2^n) \subsetneq \mathsf{DTIME}(2^{2n}) \subseteq \mathsf{EXP}$.
- Beyond the chain, $\mathsf{NP} \ne \mathsf{NEXP}$ by the nondeterministic time hierarchy ([NEXP](/nexptime/)), and $\mathsf{PSPACE} \ne \mathsf{EXPSPACE}$ by the space hierarchy theorem.
- Below the chain, $\mathsf{AC^0} \ne \mathsf{NC^1}$: the parity function is in $\mathsf{NC^1}$ and not in [AC0](/ac0/). Since $\mathsf{NC^1} \subseteq \mathsf{L}$, this is a separation inside L.

### What follows, and what is open

From $\mathsf{NL} \ne \mathsf{PSPACE}$, at least one of the steps $\mathsf{NL} \subseteq \mathsf{P}$, $\mathsf{P} \subseteq \mathsf{NP}$, $\mathsf{NP} \subseteq \mathsf{PSPACE}$ is strict. From $\mathsf{P} \ne \mathsf{EXP}$, at least one of the steps $\mathsf{P} \subseteq \mathsf{NP}$, $\mathsf{NP} \subseteq \mathsf{PSPACE}$, $\mathsf{PSPACE} \subseteq \mathsf{EXP}$ is strict. Every single step is open:

| Step | Status | Equality would mean |
|---|---|---|
| $\mathsf{L} \subseteq \mathsf{NL}$ | open | nondeterminism does not help logarithmic space |
| $\mathsf{NL} \subseteq \mathsf{P}$ | open | every polynomial-time problem fits in logarithmic nondeterministic space |
| $\mathsf{P} \subseteq \mathsf{NP}$ | open | the [P versus NP problem](/p-versus-np-problem/) has the answer yes |
| $\mathsf{NP} \subseteq \mathsf{PSPACE}$ | open | the [polynomial hierarchy](/polynomial-hierarchy/) equals NP, and NP = coNP |
| $\mathsf{PSPACE} \subseteq \mathsf{EXP}$ | open | every exponential-time problem fits in polynomial space |

The known separations rule out some combinations of equalities. For example, $\mathsf{P} = \mathsf{NP}$ and $\mathsf{NP} = \mathsf{PSPACE}$ and $\mathsf{PSPACE} = \mathsf{EXP}$ cannot all hold. Equalities also travel upward by padding: if $\mathsf{P} = \mathsf{NP}$, then $\mathsf{EXP} = \mathsf{NEXP}$.

Space is better understood than time. Nondeterministic space is closed under complement, $\mathsf{NL} = \mathsf{coNL}$ ([Immerman-Szelepcsényi theorem](/immerman-szelepcsenyi-theorem/)), and nondeterminism costs at most a square in space ([Savitch's theorem](/savitch-theorem/)), so $\mathsf{NPSPACE} = \mathsf{PSPACE}$. For time, no such result is known.

## Examples

**A complete problem at each level.** Each class has problems that are complete for it under reductions of the right strength. Directed [graph reachability](/graph-reachability/) is NL-complete under logspace reductions. The [circuit value problem](/circuit-value-problem/) is P-complete. [SAT](/sat/) is NP-complete. [QSAT](/qsat/) and [generalized geography](/generalized-geography/) are PSPACE-complete. Bounded halting with a clock written in binary is EXP-complete ([EXP](/exptime/)). If two neighboring classes are different, the complete problem of the larger class is not in the smaller one.

**Counting configurations.** Take a logspace machine with $q = 10$ states, a work tape over 4 symbols and space $s = 2 \lg n$. Its number of configurations is at most $10 \cdot (n + 2) \cdot s \cdot 4^{s}$. For $n = 1024$, $s = 20$ and the bound is $225{,}619{,}786{,}019{,}635{,}200 \approx 2^{57.65}$. For $n = 2^{20}$, $s = 40$ and the bound is about $2^{108.64}$. Both numbers are large, but the bound is $10 (n + 2) \cdot 2 \lg n \cdot n^4 = O(n^5 \log n)$, a polynomial. This is the reason why $\mathsf{NL} \subseteq \mathsf{P}$. For space $s = n$ the same count is $2^{\Theta(n)}$, which is the reason why $\mathsf{PSPACE} \subseteq \mathsf{EXP}$ and no better bound is known.

**A trap.** "$\mathsf{P} \ne \mathsf{EXP}$, so $\mathsf{P} \ne \mathsf{PSPACE}$" is wrong. The separation shows only that one of three steps is strict, and it may be the last one, $\mathsf{PSPACE} \subsetneq \mathsf{EXP}$. Whether $\mathsf{P} = \mathsf{PSPACE}$ is open.

## Where it is used

The chain is the frame for placing a new problem. An upper bound puts the problem into a class of the chain, and a completeness proof shows that it is as hard as anything in that class. A problem that is complete for EXP is provably not in P. A problem that is complete for PSPACE is not in P unless $\mathsf{P} = \mathsf{PSPACE}$, which would also give $\mathsf{P} = \mathsf{NP}$. Results on other classes are stated relative to the chain: for example $\mathsf{BPP} \subseteq \mathsf{PSPACE}$, $\mathsf{PH} \subseteq \mathsf{PSPACE}$ and $\mathsf{IP} = \mathsf{PSPACE}$.

## References
