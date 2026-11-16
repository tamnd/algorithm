---
tag: VZ3B4A
kind: concept
slug: p-versus-np-problem
name: P versus NP problem
aliases:
- P vs NP
- P=NP question
area: complexity/complexity-classes
level: intro
summary: "The open question whether every problem whose solutions can be checked in polynomial time can also be solved in polynomial time. A Clay Millennium Prize Problem since 2000."
prereqs: [p, np, np-complete]
see_also: [p, np, np-complete, cook-levin-theorem, co-np, ladner-theorem, relativization, natural-proofs-barrier]
sources:
  - book: isbn:9780821836798
    title: James Carlson, Arthur Jaffe and Andrew Wiles (editors), The Millennium Prize Problems, Clay Mathematics Institute and American Mathematical Society, 2006
    locator: Stephen Cook, The P versus NP problem, pp. 87 to 104
  - url: https://www.claymath.org/millennium/p-vs-np/
    title: Clay Mathematics Institute, P vs NP (Millennium Prize Problems)
    locator: problem page and official description
  - paper: doi:10.1145/129712.129771
    title: Michael Sipser, The history and status of the P versus NP question, Proceedings of the 24th Annual ACM Symposium on Theory of Computing (STOC 1992), 603 to 618
    locator: the history, including Gödel's 1956 letter to von Neumann
  - paper: doi:10.1145/1562164.1562186
    title: Lance Fortnow, The status of the P versus NP problem, Communications of the ACM 52(9) (2009), 78 to 86
    locator: consequences, barriers and approaches
  - paper: doi:10.1145/800157.805047
    title: Stephen A. Cook, The complexity of theorem-proving procedures, Proceedings of the 3rd Annual ACM Symposium on Theory of Computing (STOC 1971)
    locator: pp. 151 to 158
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: Richard M. Karp, Reducibility among combinatorial problems, in R. E. Miller and J. W. Thatcher (editors), Complexity of Computer Computations, Plenum Press (1972)
    locator: pp. 85 to 103
  - paper: "Leonid A. Levin, Universal sequential search problems, Problemy Peredachi Informatsii 9(3) (1973)"
    locator: pp. 115 to 116
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach
    locator: Chapter 2 (NP and NP-completeness) and Section 3.4 (oracle machines and the limits of diagonalization)
---

The P versus NP problem asks whether $\mathsf{P} = \mathsf{NP}$: whether every [decision problem](/decision-problem/) whose yes-answers have short certificates that can be checked in polynomial time can also be solved in polynomial time. Cook stated it in 1971, Levin found the same notions independently, and Karp showed in 1972 that many classical combinatorial problems are equivalent to it. It is the central open problem of complexity theory, and in 2000 the Clay Mathematics Institute made it one of its seven Millennium Prize Problems, with a prize of one million US dollars for a solution. Most researchers believe that $\mathsf{P} \ne \mathsf{NP}$.

## In plain words

For many puzzles, checking a proposed answer is easy, but finding an answer seems to need a search through a huge number of possibilities. A filled-in Sudoku grid is quick to check. A set of numbers that adds up to a target is quick to check. A route that visits every city within a given distance is quick to check.

The question is whether this gap is real. Perhaps every puzzle whose answers are quick to check also has a quick method to find them, and we have not found the methods. Or perhaps some of these puzzles need a slow search, whatever method we use.

Thousands of important problems are known to stand or fall together: a quick method for any one of them would give quick methods for all. Nobody has found one, and nobody has proved that none exists.

## The idea

### The statement

[P](/p/) is the class of decision problems that a deterministic Turing machine solves in time polynomial in the input length. [NP](/np/) is the class of decision problems whose yes-instances have certificates of polynomial length that a deterministic polynomial-time verifier checks. Every problem in P is in NP, so the question is whether the inclusion $\mathsf{P} \subseteq \mathsf{NP}$ is strict.

By the [Cook-Levin theorem](/cook-levin-theorem/), [SAT](/sat/) is [NP-complete](/np-complete/): every problem in NP reduces to it by a polynomial-time many-one reduction. Cook (1971) used polynomial-time Turing reductions, and Karp (1972) used many-one reductions, which are the standard now. P is closed under these reductions, so the following statements are equivalent.

1. $\mathsf{P} = \mathsf{NP}$.
2. SAT is in P.
3. Some NP-complete problem is in P.
4. Every NP-complete problem is in P.
5. For every polynomial-time verifier, a polynomial-time algorithm finds a certificate whenever one exists ([search-to-decision reduction](/search-to-decision-reduction/)).

The fifth form uses [self-reducibility](/self-reducibility/). For SAT, set the variables one at a time: set $x_i = 0$ and ask the decision algorithm whether the formula is still satisfiable, and set $x_i = 1$ if not. With $n$ variables this takes at most $n + 1$ calls. For other NP problems, reduce the search to SAT. So the decision question and the search question are the same question.

### What would follow from $\mathsf{P} = \mathsf{NP}$

- Every NP search problem and many optimization problems would be solved in polynomial time. This includes the [traveling salesman problem](/traveling-salesman-problem/), integer programming and the [subset sum problem](/subset-sum-problem/).
- $\mathsf{NP} = \mathsf{coNP}$, and the whole [polynomial hierarchy](/polynomial-hierarchy/) would equal P.
- $\mathsf{EXP} = \mathsf{NEXP}$, by padding ([NEXP](/nexptime/)).
- [One-way functions](/one-way-function/) would not exist, because inverting a function is an NP search problem. Public-key cryptography as it is built today would be insecure.
- For a formal system in which proofs are checked in polynomial time, the question "does this statement have a proof of length at most $n$?", with $n$ written in unary, is in NP. So proofs of polynomial length would be found in polynomial time.

A proof of $\mathsf{P} = \mathsf{NP}$ could be useless in practice: the algorithm might run in time $n^{100}$, or the proof might not give an explicit algorithm. See [computational tractability](/computational-tractability/).

### What would follow from $\mathsf{P} \ne \mathsf{NP}$

- No NP-complete problem has a polynomial-time algorithm in the worst case.
- NP contains problems that are neither in P nor NP-complete ([Ladner's theorem](/ladner-theorem/), [NP-intermediate](/np-intermediate/)).
- It would not show that NP problems are hard on typical inputs, and it would not by itself give secure cryptography. Both need hardness on average, a stronger assumption.

### Why it is hard to prove

The known separations, such as $\mathsf{P} \ne \mathsf{EXP}$ and $\mathsf{NP} \ne \mathsf{NEXP}$, come from diagonalization. Three results show that the standard methods cannot settle the question.

- **Relativization.** Baker, Gill and Solovay (1975) built oracles $A$ and $B$ with $\mathsf{P}^A = \mathsf{NP}^A$ and $\mathsf{P}^B \ne \mathsf{NP}^B$. A proof that stays true for every oracle, as diagonalization by simulation does, cannot settle the question. See [relativization](/relativization/) and the [Baker-Gill-Solovay theorem](/baker-gill-solovay-theorem/).
- **Natural proofs.** Razborov and Rudich (1997) showed that a large class of combinatorial proofs of circuit lower bounds would break pseudorandom functions, if such functions exist. See [natural proofs](/natural-proofs-barrier/).
- **Algebrization.** Aaronson and Wigderson (2009) extended the oracle barrier to proofs that use algebraic extensions of the oracle, such as the proof of $\mathsf{IP} = \mathsf{PSPACE}$. See [algebrization](/algebrization-barrier/).

The main approaches are [circuit complexity](/circuit-complexity/), because $\mathsf{P} \subseteq \mathsf{P/poly}$ and so a superpolynomial circuit lower bound for SAT would prove $\mathsf{P} \ne \mathsf{NP}$, and proof complexity, because superpolynomial lower bounds for every propositional proof system would prove $\mathsf{NP} \ne \mathsf{coNP}$ and hence $\mathsf{P} \ne \mathsf{NP}$. Both are far from the goal. A milestone of the circuit approach is the proof of Williams (2014) that NEXP does not have polynomial-size ACC0 circuits.

### History

In a letter to John von Neumann in 1956, Kurt Gödel asked how fast a machine could decide whether a statement of first-order logic has a proof of length $n$, and whether the number of steps could grow only linearly or quadratically in $n$. Sipser (1992) describes the letter and its rediscovery. In 1965 Cobham and Edmonds proposed polynomial time as the measure of efficient computation. Cook (1971) defined NP in terms of nondeterministic machines, proved that SAT is complete for it, and asked whether $\mathsf{P} = \mathsf{NP}$. Levin (1973) proved the same kind of result for search problems. Karp (1972) gave 21 NP-complete problems ([Karp's 21 problems](/karps-21-np-complete-problems/)), and Garey and Johnson (1979) collected several hundred more ([compendium](/garey-johnson-compendium/)). Cook wrote the official description of the problem for the Clay Mathematics Institute.

## Examples

**Checking against finding.** For the list $3, 34, 4, 12, 5, 2$ and the target $9$, checking the certificate $\{4, 5\}$ takes one addition. Finding a certificate by brute force means looking through up to $2^6 = 64$ sublists, of which exactly two work: $\{4, 5\}$ and $\{3, 4, 2\}$. With 40 numbers there are $2^{40} = 1{,}099{,}511{,}627{,}776$ sublists, about 1100 seconds at $10^9$ sublists per second, and every added number doubles the count. The P versus NP problem asks whether some cleverer method always avoids this growth.

**Search from decision.** Take the formula

$$\varphi = (x_1 \lor x_2) \land (\neg x_1 \lor x_3) \land (\neg x_2 \lor \neg x_3) \land (x_3 \lor x_4) \land (\neg x_4 \lor x_1).$$

It has two satisfying assignments: $(x_1, x_2, x_3, x_4) = (1, 0, 1, 0)$ and $(1, 0, 1, 1)$. A procedure that only answers yes or no finds one of them as follows. The first call confirms that $\varphi$ is satisfiable. With $x_1 = 0$ the answer is no, so $x_1 = 1$. With $x_1 = 1, x_2 = 0$ the answer is yes. With $x_3 = 0$ added the answer is no, so $x_3 = 1$. With $x_4 = 0$ added the answer is yes. The result is $(1, 0, 1, 0)$ after 5 calls, which is $n + 1$ for $n = 4$ variables. If the decision procedure runs in polynomial time, so does the whole search.

## Where it is used

The question shapes the practice of algorithm design. A proof that a problem is NP-complete is read as strong evidence that no polynomial-time algorithm exists, and it turns the work toward [approximation algorithms](/approximation-ratio/), [fixed-parameter algorithms](/fixed-parameter-tractable/), heuristics and special cases. Modern cryptography assumes far more than $\mathsf{P} \ne \mathsf{NP}$, such as the existence of [one-way functions](/one-way-function/), and so a proof of $\mathsf{P} = \mathsf{NP}$ with a practical algorithm would break it. Complexity theory states many results conditionally on $\mathsf{P} \ne \mathsf{NP}$, for example the hardness of approximation results that follow from the [PCP theorem](/pcp-theorem/).

## References
