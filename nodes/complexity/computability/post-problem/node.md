---
tag: ANG7BC
kind: problem
slug: post-problem
name: Post's problem
aliases:
- intermediate degree problem
area: complexity/computability
level: research
summary: "Post asked in 1944 whether some c.e. set is undecidable but does not compute the halting problem. Friedberg and Muchnik answered yes in 1956 and 1957 with the priority method."
prereqs: [turing-degrees, turing-jump]
see_also: [turing-degrees, turing-jump, oracle-turing-machine, halting-problem, many-one-reducibility, ladners-theorem, np-intermediate, recursively-enumerable-language]
sources:
  - paper: doi:10.1090/S0002-9904-1944-08111-1
    title: "Emil L. Post, Recursively enumerable sets of positive integers and their decision problems, Bulletin of the American Mathematical Society 50 (1944)"
    locator: "pp. 284 to 316 (the question, simple and hypersimple sets)"
  - paper: doi:10.1073/pnas.43.2.236
    title: "Richard M. Friedberg, Two recursively enumerable sets of incomparable degrees of unsolvability, Proceedings of the National Academy of Sciences 43(2) (1957)"
    locator: pp. 236 to 238
  - title: "Albert A. Muchnik, On the unsolvability of the problem of reducibility in the theory of algorithms (in Russian), Doklady Akademii Nauk SSSR 108 (1956)"
    locator: pp. 194 to 197
  - paper: doi:10.2307/1969708
    title: "Stephen C. Kleene and Emil L. Post, The upper semi-lattice of degrees of recursive unsolvability, Annals of Mathematics 59(3) (1954)"
    locator: pp. 379 to 407
  - book: isbn:9783642319327
    title: "Robert I. Soare, Turing Computability, Theory and Applications, Springer, 2016"
    locator: "Chapter 7, The Finite Injury Method"
---

Post's problem asks whether there is a computably enumerable (c.e.) set that is undecidable and yet does not let an algorithm decide the [halting problem](/halting-problem/). In the language of [Turing degrees](/turing-degrees/), it asks for a c.e. degree strictly between $\mathbf{0}$ and $\mathbf{0}'$. Emil Post asked it in 1944, after he noticed that every undecidable c.e. set known at the time was as hard as the halting problem. Friedberg (1957) in the United States and Muchnik (1956) in the Soviet Union solved it independently: they built two c.e. sets, neither of which is computable from the other, so both are intermediate. Their method, the priority method, became the main tool for constructions of c.e. sets. The analog in complexity theory is [Ladner's theorem](/ladners-theorem/) on [NP-intermediate](/np-intermediate/) problems.

## In plain words

Some yes-or-no problems have a program that confirms every yes answer, by searching until it finds a proof, but no program that always answers. The halting problem is the standard one, and every such problem known in 1944 was as hard as the halting problem: a magic box for it would solve halting.

Post asked whether there is a problem of this kind that is easier than halting but still unsolvable. The answer is yes. The two people who found it built a problem step by step, and at each step they balanced a list of goals by giving earlier goals priority over later ones.

## Definition

Post's problem is a single question about the class of c.e. sets, not a decision problem with instances. In the form of Post (1944), with $K = \{ e : \varphi_e(e) \text{ is defined} \}$ for the diagonal halting set and $\le_T$ for Turing reducibility (see [oracle Turing machine](/oracle-turing-machine/)):

**Instance.** The class of all c.e. sets of natural numbers, with Turing reducibility.

**Question.** Is there a c.e. set $A$ that is not decidable and such that $K \not\le_T A$? Equivalently, is there a c.e. degree $\mathbf{a}$ with $\mathbf{0} < \mathbf{a} < \mathbf{0}'$?

Every c.e. set $A$ satisfies $A \le_m K$ by a many-one reduction, so $\mathbf{a} \le \mathbf{0}'$ always holds, and the question is whether the order between $\mathbf{0}$ and $\mathbf{0}'$ has anything in the middle among the c.e. degrees.

**Friedberg-Muchnik theorem.** There are c.e. sets $A$ and $B$ with $A \not\le_T B$ and $B \not\le_T A$.

Since a decidable set is computable from every set, neither $A$ nor $B$ is decidable. Since $K$ computes every c.e. set, neither computes $K$. So $\mathbf{0} < \deg(A) < \mathbf{0}'$, and the answer to Post's question is yes.

*Proof sketch (finite injury).* Fix a numbering $\Phi_e$ of the oracle programs. Build $A$ and $B$ in stages $s = 0, 1, 2, \ldots$ as unions of finite sets $A_s$ and $B_s$, so that both are c.e. The requirements are
$$R_{2e} : A \ne \Phi_e^B, \qquad R_{2e+1} : B \ne \Phi_e^A,$$
in the priority order $R_0, R_1, R_2, \ldots$, where $R_i$ has higher priority than $R_j$ for $i < j$. To meet $R_{2e}$:

1. choose a *witness* $x$, a number not yet used, not in $A$;
2. wait for a stage $s$ at which $\Phi_{e,s}^{B_s}(x)$ halts within $s$ steps with output $0$;
3. if that happens, put $x$ into $A$, so that $A(x) = 1 \ne 0 = \Phi_e^B(x)$, and *restrain* $B$: no requirement of lower priority may put into $B$ a number below the use of the computation.

$R_{2e+1}$ works in the same way with $A$ and $B$ swapped. A requirement of higher priority may still put a number below the restraint into $B$. This *injures* $R_{2e}$, whose computation may then change, and $R_{2e}$ starts again with a new witness. Each requirement acts at most once between injuries, and only requirements of higher priority can injure it, so by induction each requirement is injured finitely often and is met after its last injury. If the computation of step 2 never appears after the last injury, then $\Phi_e^B(x)$ is undefined or not $0$, because a halting computation with output $0$ on the final $B$ would appear at some stage by the use principle. Since $x \notin A$, $A(x) = 0 \ne \Phi_e^B(x)$, and $R_{2e}$ is met in this case too. Details are in Friedberg (1957) and in Soare, Chapter 7.

## Variants

- **Weaker reducibilities.** For many-one reductions, Post answered his own question: a *simple set* (a c.e. set whose complement is infinite but contains no infinite c.e. set) is undecidable and not many-one complete. For truth-table reductions, a *hypersimple* set is undecidable and not truth-table complete. Both kinds exist, by constructions in Post (1944).
- **Post's program.** Post hoped to find a property of the complement, like simplicity, that forces a set to be incomplete for Turing reductions. Simplicity is not such a property: there are simple sets that are Turing complete. The Friedberg-Muchnik solution builds the sets directly instead.
- **Many intermediate degrees.** The degrees between $\mathbf{0}$ and $\mathbf{0}'$ of c.e. sets are a rich structure: by Sacks's density theorem, between any two c.e. degrees $\mathbf{a} < \mathbf{b}$ there is another one.
- **Without priority.** Kučera gave a solution that uses algorithmic randomness in place of the priority method.
- **Complexity theory.** Under polynomial-time many-one reductions, the question is whether NP has problems that are neither in P nor NP-complete. [Ladner's theorem](/ladners-theorem/) says yes if $\mathrm{P} \ne \mathrm{NP}$.

## Examples

**Post's simple set.** Post built a simple set $S$ as follows: enumerate all the c.e. sets $W_0, W_1, \ldots$ in parallel, and for each $e$ put into $S$ the first number $x > 2e$ that appears in $W_e$. Then $S$ is c.e. Each $W_e$ adds at most one number, and only $W_0, \ldots, W_{n-1}$ can add a number $x \le 2n$, so $S$ has at most $n$ elements in $\{0, 1, \ldots, 2n\}$, and its complement is infinite. Every infinite $W_e$ has a number above $2e$, so it meets $S$ and is not contained in the complement.

A toy run with seven sets in place of all c.e. sets shows the rule:

| $e$ | $W_e$ | threshold | number put into $S$ |
| --- | --- | --- | --- |
| 0 | even numbers | $x > 0$ | 2 |
| 1 | squares | $x > 2$ | 4 |
| 2 | primes | $x > 4$ | 5 |
| 3 | empty set | $x > 6$ | none |
| 4 | multiples of 7 | $x > 8$ | 14 |
| 5 | $\{3\}$ | $x > 10$ | none |
| 6 | numbers from 100 on | $x > 12$ | 100 |

So $S = \{2, 4, 5, 14, 100\}$. The finite sets $W_3$ and $W_5$ do not have to meet $S$; every infinite one does.

**The Friedberg-Muchnik sets.** The sets $A$ and $B$ above can also be made *low*, with $A' \equiv_T \emptyset'$ and $B' \equiv_T \emptyset'$ (see [Turing jump](/turing-jump/)). A low set cannot compute $K$, because $K' = \emptyset''$ is strictly above $\emptyset'$, so lowness gives a second proof that the sets are incomplete.

## Known algorithms

The Friedberg-Muchnik construction is an algorithm: at each stage it runs finitely many oracle programs for finitely many steps and adds finitely many numbers to $A$ or $B$. It is what makes $A$ and $B$ c.e. What no algorithm can do is tell, from the construction, when a requirement has been injured for the last time.

**Number of injuries.** Let $a_n$ be the largest number of times $R_n$ acts. $R_n$ acts at most once at the start and once after each injury, and each injury comes from an action of some $R_i$ with $i < n$, so $a_n \le 1 + \sum_{i<n} a_i$. With $a_0 = 1$ this gives $a_n \le 2^n$, and $R_n$ is injured at most $2^n - 1$ times. The name "finite injury" refers to this: each requirement is injured only finitely often. Later constructions, such as the proof of Sacks's density theorem, need infinite injury.

## Bounds

The intermediate c.e. degrees are not all alike. They include low degrees, whose jump is $\mathbf{0}'$ as for $\mathbf{0}$, and high degrees, whose jump is $\mathbf{0}''$ as for $\mathbf{0}'$. So the jump does not separate them from the two ends. No natural problem, in the sense of a decision problem from outside computability theory, is known to have an intermediate c.e. degree: the undecidable c.e. problems of mathematics that have been classified are all complete.

## Reductions

- **Many-one completeness.** The usual way to show that a c.e. problem is undecidable is a many-one reduction from $K$, which also shows that it has the degree $\mathbf{0}'$. An intermediate set cannot be shown undecidable in this way.
- **Turing completeness of simple sets.** Some simple sets are Turing complete, so Post's construction of a simple set does not answer the question for Turing reductions.

## Applications

- **The priority method.** The method of requirements with priorities, injuries and restraints is used for most constructions of c.e. sets and degrees, including the density theorem, minimal pairs, and splitting theorems.
- **Complexity theory.** [Ladner's theorem](/ladners-theorem/) for NP is a resource-bounded form of the question. The idea that a hard class may contain problems that are neither easy nor complete comes from here.
- **The structure of the c.e. degrees.** Post's problem started the study of the c.e. degrees as an ordered structure, which is a main subject of classical computability theory.

## References
