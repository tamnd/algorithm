---
tag: 66DY7C
kind: theorem
slug: ladners-theorem
name: Ladner's theorem (general form)
aliases:
- Ladner's density theorem
area: complexity/np-completeness
level: research
summary: If a computable nontrivial set reduces to another but not back, a third set lies strictly between them under Karp reductions. So if P is not NP, NP has problems neither in P nor NP-complete.
prereqs: [np-complete, polynomial-time-reduction, diagonalization-argument]
see_also: [ladner-theorem, np-intermediate, mahaneys-theorem, graph-isomorphism-problem, relativization, turing-degrees, time-hierarchy-theorem, turing-reduction]
sources:
  - paper: doi:10.1145/321864.321877
    title: Richard E. Ladner, On the structure of polynomial time reducibility, Journal of the ACM 22(1), 155 to 171 (1975)
    locator: the density theorem for polynomial-time reducibilities on computable sets, its corollary for NP, and the results on incomparable sets and minimal pairs
  - paper: doi:10.1016/0304-3975(82)90114-1
    title: Uwe Schoning, A uniform approach to obtain diagonal sets in complexity classes, Theoretical Computer Science 18, 95 to 103 (1982)
    locator: the uniform diagonalization theorem and its application to Ladner's theorem
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach
    locator: Section 3.3 (Ladner's theorem, Theorem 3.3, proved with the padded language SAT_H)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness
    locator: Section 7.1 (the structure of NP)
---

Ladner's theorem in its general form says that the polynomial-time many-one ([Karp](/polynomial-time-reduction/)) reduction order on computable sets is dense: if a nontrivial set $A$ reduces to $B$ and $B$ does not reduce to $A$, then some set $C$ lies strictly between them. The best-known case takes $A$ in P and $B$ = [SAT](/sat/). If P is not equal to NP, it gives a problem in NP that is neither in P nor [NP-complete](/np-complete/), an [NP-intermediate](/np-intermediate/) problem. That case alone is on the page [Ladner's theorem](/ladner-theorem/). This page states and proves the general form, from which that case follows in a few lines.

## Statement

Here $\le$ is $\le_m^p$, Karp reduction computed by a deterministic multitape Turing machine, and $A < B$ means $A \le B$ and $B \not\le A$. A language is nontrivial when it is neither $\emptyset$ nor $\{0,1\}^*$.

**Theorem (Ladner 1975).** Let $A$ and $B$ be computable nontrivial languages with $A < B$. Then there is a computable language $C$ with $A < C < B$.

**Corollary.** If $\mathsf{P} \ne \mathsf{NP}$, there is a language $C \in \mathsf{NP}$ that is not in P and not NP-complete. Moreover there is an infinite chain $C_1 < C_2 < \cdots$ of such languages.

Ladner proved the same density result for polynomial-time Turing (Cook) reductions. The proof below is for Karp reductions; the proof for Cook reductions is the same with oracle machines in place of transducers.

## In plain words

Rank problems by how hard they are, where one problem is at most as hard as another if a fast translation turns the first into the second. Take two problems, the second strictly harder. Ladner showed that there is always a third problem strictly between them. He builds it by gluing the easy problem to the hard one and switching the hard part on and off at different input sizes. Each time the third problem threatens to be as easy as the easy one, or as hard as the hard one, the switch flips, and it flips slowly enough that the result is still easy to compute. If the problems that are easy to check are not all easy to solve, this gives problems that are easy to check, not easy to solve, and not among the hardest.

## Proof

The full proof is on [the proof page](proofs/main.md). Here is the plan.

**The set.** Fix computable $A < B$. Let $C$ consist of the strings $0y$ with $y \in A$ and the strings $1y$ with $y \in B$ and $g(|y|)$ even, for a function $g$ to be built. So $C$ looks like $A$ joined with $B$ at input lengths where $g$ is even, and like $A$ joined with $\emptyset$ at lengths where $g$ is odd.

**The requirements.** List all polynomial-time reductions as clocked transducers $M_1, M_2, \ldots$. Requirement $R_{2j}$ asks that $M_j$ is not a reduction from $C$ to $A$, and $R_{2j+1}$ asks that $M_j$ is not a reduction from $B$ to $C$.

**Delayed diagonalization.** $g$ starts at 2 and moves from $s$ to $s + 1$ only when a search with a budget of $n$ steps at input length $n$ finds a string that shows $R_s$ is met. The search uses only values of $g$ at smaller lengths, so $g$ is well defined, and computing $g(n)$ takes time polynomial in $n$. This makes $C \le B$ and keeps $C$ computable.

**Why $g$ moves.** If $g$ stopped at an even value $2j$ forever, then $C$ would equal $A \oplus B$ up to finitely many strings, and the search would never find a string that refutes $M_j$; so $M_j$ would reduce $C$, and with it $B$, to $A$. If $g$ stopped at an odd value, then $C$ would equal $A \oplus \emptyset$ up to finitely many strings, so $C \le A$, and $M_j$ would reduce $B$ to $C$; so $B \le A$ again. Both contradict $A < B$. So $g$ passes every value, every requirement is met, and $A < C < B$.

**The corollary.** Take $A$ to be any nontrivial set in P and $B$ = SAT. If P is not NP, then SAT does not reduce to $A$, so the theorem applies. The resulting $C$ is in NP because $C \le \mathrm{SAT}$; it is not in P because $C \not\le A$, while every set in P reduces to the nontrivial set $A$; and it is not NP-complete because SAT does not reduce to $C$.

## Consequences

- **Three kinds of problems in NP.** If P is not NP, NP splits into P, the NP-complete problems, and a nonempty rest. The intermediate problems are not one class: there are infinite chains of them, and Ladner also showed that there are pairs of them that do not reduce to each other either way.
- **What a proof of intermediacy would need.** A proof that some problem in NP is NP-intermediate would prove P ≠ NP. So no natural problem is known to be intermediate. [Graph isomorphism](/graph-isomorphism-problem/) and the decision version of [integer factorization](/integer-factorization/) are the usual candidates, because they are in NP, no polynomial-time algorithm is known, and there is evidence that they are not NP-complete.
- **Structure without separation.** The theorem shows that P ≠ NP has consequences for the fine structure of NP, as [Mahaney's theorem](/mahaneys-theorem/) does for sparse sets. It gives no tool to prove P ≠ NP.
- **Other classes.** The same proof works for many pairs of classes. Schöning's uniform approach (1982) makes this precise: roughly, it applies to classes that have a computable list of machines for their members and are closed under finite changes.

## Tightness

- **The hypothesis P ≠ NP is needed.** If P = NP, then every nontrivial language $L$ in NP is NP-complete: SAT is in P, so SAT reduces to $L$ by deciding SAT and mapping to a fixed member or non-member of $L$. So every language in NP is in P, and every nontrivial one is also NP-complete; no language is in NP but outside both P and the NP-complete languages.
- **Nontriviality is needed.** $\{0,1\}^*$ reduces to every nonempty set, and no nontrivial set reduces to $\{0,1\}^*$, because a reduction must send non-members to non-members. So $\{0,1\}^* < B$ for every nontrivial $B$ in P. A set $C$ with $\{0,1\}^* < C \le B$ is nontrivial and in P, and then $B \le C$. So nothing lies strictly between $\{0,1\}^*$ and a nontrivial set in P; the same holds for $\emptyset$.
- **The set is artificial.** $C$ is SAT with holes cut out at input lengths chosen by a diagonalization; it is not a natural problem. The proof of Arora and Barak gives another artificial set, SAT padded to a length that grows slowly. No proof of the theorem gives a natural problem.
- **Relativization.** The proof relativizes: the theorem holds relative to every oracle. So it does not touch the barriers to P versus NP ([relativization](/relativization/)).

## History

Ladner presented the results at STOC 1973 and published them in the Journal of the ACM in 1975, under the title "On the structure of polynomial time reducibility". The method, delayed diagonalization, mirrors the priority constructions of computability theory, where the Friedberg-Muchnik theorem gives intermediate [Turing degrees](/turing-degrees/) between the computable sets and the halting problem. The paper also proved density for Cook reductions and the existence of minimal pairs. Schöning (1982) gave a uniform form of the construction that covers many classes at once. Textbook proofs, such as that of Arora and Barak, often use a padded version of SAT, in which the padding length is chosen by the same kind of slow diagonalization.

## References
