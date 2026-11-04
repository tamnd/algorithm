---
tag: JDFXXG
kind: definition
slug: invariant
name: Invariant
aliases:
- Program invariant
- Invariant property
area: foundations/correctness-and-invariants
level: intro
summary: A property that holds at a given point in every execution, such as at each step of a loop or after each operation.
prereqs: []
see_also: [loop-invariant, inductive-invariant, representation-invariant, assertion, variant-function, hoare-logic, invariant-checking]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.1 (loop invariants)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.1, Mathematical induction (proofs of algorithms by assertions)
  - paper: doi:10.1145/363235.363259
    title: C. A. R. Hoare, An axiomatic basis for computer programming, Communications of the ACM 12(10), 1969
    locator: the rule of iteration for the while statement
  - paper: "Robert W. Floyd, Assigning meanings to programs, Proceedings of Symposia in Applied Mathematics 19 (1967)"
    locator: pages 19 to 32 (assertions attached to the points of a flowchart, checked one step at a time)
  - url: https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/mit6_042js15_textbook2.pdf
    title: Eric Lehman, F. Thomson Leighton and Albert R. Meyer, Mathematics for Computer Science (2015 version)
    locator: Chapter 6, State Machines (preserved invariants and the invariant principle)
---

An invariant is a property of a program, a data structure or a system that is true at a given point in every execution. The point can be the test of a loop, the state between two operations, or every reachable state. Invariants let you reason about a whole family of executions with one statement. The best known kind is the [loop invariant](/loop-invariant/).

## Definition

A *transition system* is a triple $(S, S_0, \to)$ where $S$ is a set of states, $S_0 \subseteq S$ is the set of initial states, and $\to \subseteq S \times S$ is the step relation. The set of *reachable* states is

$$\mathrm{Reach} = \{ s \in S : \exists s_0 \in S_0,\ s_0 \to^* s \},$$

where $\to^*$ is the reflexive and transitive closure of $\to$.

**Invariant.** A predicate $P$ on $S$ is an *invariant* of the system when $P(s)$ holds for each $s \in \mathrm{Reach}$.

**Inductive invariant.** A predicate $P$ is an *inductive* invariant when both conditions hold:

1. **Initiation.** $P(s_0)$ for each $s_0 \in S_0$.
2. **Consecution.** For all $s, s' \in S$: if $P(s)$ and $s \to s'$, then $P(s')$.

**Proposition 1.** Each inductive invariant is an invariant.

*Proof.* Let $P$ be inductive, and let $s \in \mathrm{Reach}$. Then there is a path $s_0 \to s_1 \to \cdots \to s_k = s$ with $s_0 \in S_0$. We show $P(s_j)$ by [induction](/induction/) on $j$. For $j = 0$, initiation gives $P(s_0)$. If $P(s_j)$ and $j < k$, then $s_j \to s_{j+1}$ and consecution give $P(s_{j+1})$. So $P(s_k)$ holds. $\square$

The converse is false, as the example below shows. But each invariant has an inductive strengthening.

**Proposition 2.** The predicate $R(s) = (s \in \mathrm{Reach})$ is an inductive invariant, and it implies every invariant. So $P$ is an invariant if and only if some inductive invariant $J$ satisfies $J \Rightarrow P$.

*Proof.* Initiation: each $s_0 \in S_0$ is reachable by the path of length 0. Consecution: if $s$ is reachable and $s \to s'$, then the path to $s$ followed by this step reaches $s'$. If $P$ is an invariant, then $P(s)$ holds for each reachable $s$, so $R \Rightarrow P$. For the second claim, take $J = R$ in one direction. In the other, $J$ is an invariant by Proposition 1, and so is any $P$ that it implies. $\square$

Proposition 2 does not give an algorithm. $R$ is often not expressible in the language of the proof, and for programs over the integers it is undecidable whether a given predicate is an invariant: the predicate "control never reaches the end" is an invariant exactly when the program does not halt, so a decision procedure would solve the [halting problem](/halting-problem/). The work of a proof is to find an inductive $J$ that is simple enough to check. Two more facts help. The conjunction of two invariants is an invariant, and the conjunction of two inductive invariants is inductive. Each predicate implied by an invariant is an invariant, but a predicate implied by an inductive invariant need not be inductive.

**Invariant at a program point.** Let a program have control points. A predicate $P$ on the program variables is an invariant at a point $p$ when $P$ holds each time that control reaches $p$, in each execution that starts from a state that satisfies the precondition. Write the states as pairs $(p, v)$ of a control point and the variable values, and this is the definition above for the predicate $Q(p', v) = (p' \neq p) \vee P(v)$.

**Loop invariant.** A *loop invariant* is an invariant at the test of the loop condition.

## Examples and non-examples

**An invariant that is inductive.** Let $S = \mathbb{N}$, $S_0 = \{0\}$ and $x \to x + 2$. The reachable states are the even numbers. The predicate "$x$ is even" is an inductive invariant: $0$ is even, and if $x$ is even then $x + 2$ is even.

**An invariant that is not inductive.** In the same system, the predicate $Q(x) = (x \neq 3)$ is an invariant, because 3 is not even and so not reachable. But $Q$ is not inductive. The state $1$ satisfies $Q$ and $1 \to 3$, and $3$ does not satisfy $Q$. Consecution fails at an unreachable state. To prove $Q$, you strengthen it to the inductive invariant "$x$ is even". This is the usual way to prove an invariant: find an inductive one that implies it.

**Loop invariant.** In insertion sort, "the first $i$ items are the original first $i$ items, in order" is an invariant at the test of the outer loop. See [loop invariant](/loop-invariant/) for the proof.

**Data structure invariant.** In a binary min-heap stored in an array $A[1 \ldots n]$, the property $A[\lfloor k/2 \rfloor] \le A[k]$ for each $2 \le k \le n$ is true between the operations. Each operation may break it for a short time inside, and then restores it. See [representation invariant](/representation-invariant/).

**Conservation law.** In a system that moves money between accounts, a transfer of $t$ from account $a$ to account $b$ lowers $a$ by $t$ and raises $b$ by $t$. So the sum of all balances is the same after each step, and "the sum equals its initial value" is an inductive invariant. With balances $(100, 50, 0)$, the transfers of 30 from the first to the third account and of 50 from the second to the first give $(120, 0, 30)$, and the sum stays 150.

**An invariant that proves impossibility.** Remove two opposite corners from an $8 \times 8$ chessboard. Can 31 dominoes, each covering two adjacent squares, cover the other 62 squares? Color the board as usual. The two removed corners have the same color, so 30 squares of one color and 32 of the other remain. Take the state to be the set of squares covered so far, and the step to be placing one domino. The predicate "the covered squares have as many of one color as of the other" is an inductive invariant: it holds for the empty set, and each domino covers two adjacent squares, which have different colors. A full cover would have to cover 30 and 32 squares of the two colors, which breaks the invariant. So no cover exists. This is the usual use of an invariant in puzzles and in lower bounds: a reachable state must satisfy it, and the goal does not.

**Not an invariant: a quantity that changes.** The value of a loop counter $i$ is not an invariant. It is a different value at each test. A property that depends on $i$, such as "$s = i(i+1)/2$", can be an invariant. A quantity that must decrease at each pass is a [variant function](/variant-function/). It is the opposite of an invariant: it is useful because it changes.

**Not an invariant: true only on some executions.** The predicate "$x > 10$" for the system $x \to x + 2$ from $0$ is true in the reachable state 12 and false in the reachable state 4, so it is not an invariant. An invariant must hold in all reachable states, at the stated point.

## Related definitions

- [Loop invariant](/loop-invariant/): an invariant at the test of a loop, used with induction on the number of passes to prove that the loop is correct.
- [Inductive invariant](/inductive-invariant/): an invariant that is closed under the step. It is the form that a proof can check one step at a time.
- [Representation invariant](/representation-invariant/): an invariant of the fields of a data structure, true between operations.
- [Assertion](/assertion/): a statement written in a program that is checked, or proved, at a point. A program point invariant is an assertion that is always true.
- [Variant function](/variant-function/): a quantity that decreases at each step. A variant proves termination, and an invariant proves that the state is correct.
- [Hoare logic](/hoare-logic/): a proof system in which a loop invariant is the key input of the rule for a loop.

## References
