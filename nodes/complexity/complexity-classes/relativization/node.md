---
tag: PN2BH4
kind: concept
slug: relativization
name: Relativization
aliases:
- oracle results
- relativized computation
- relativizing proofs
area: complexity/complexity-classes
level: advanced
summary: "A proof relativizes if it stays true when every machine gets the same oracle. P versus NP has oracles that go both ways, so no relativizing proof can settle it."
prereqs: [oracle-turing-machine, p-versus-np-problem, diagonalization-argument]
see_also: [baker-gill-solovay-theorem, oracle-turing-machine, natural-proofs-barrier, algebrization-barrier, time-hierarchy-theorem, ip-equals-pspace, p-versus-np-problem, query-complexity]
sources:
  - paper: doi:10.1137/0204037
    title: Theodore Baker, John Gill and Robert Solovay, Relativizations of the P =? NP question, SIAM Journal on Computing 4(4) (1975)
    locator: pp. 431 to 442 (oracles A with P^A = NP^A and B with P^B different from NP^B, and oracles for other relations among P, NP and coNP)
  - paper: doi:10.1137/0210008
    title: Charles H. Bennett and John Gill, Relative to a random oracle A, P^A != NP^A != co-NP^A with probability 1, SIAM Journal on Computing 10(1) (1981)
    locator: pp. 96 to 113 (the random oracle results and the random oracle hypothesis)
  - paper: doi:10.1016/0020-0190(88)90199-8
    title: Lance Fortnow and Michael Sipser, Are there interactive protocols for co-NP languages?, Information Processing Letters 28(5) (1988)
    locator: pp. 249 to 251 (an oracle relative to which coNP has no interactive proof)
  - paper: doi:10.1016/S0022-0000(05)80084-4
    title: Richard Chang, Benny Chor, Oded Goldreich, Juris Hartmanis, Johan Håstad, Desh Ranjan and Pankaj Rohatgi, The random oracle hypothesis is false, Journal of Computer and System Sciences 49(1) (1994)
    locator: pp. 24 to 39 (IP^A different from PSPACE^A for a random oracle A)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Section 3.4, Oracle machines and the limits of diagonalization
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 9.2, Relativization
  - paper: doi:10.1145/2559903
    title: Ryan Williams, Nonuniform ACC circuit lower bounds, Journal of the ACM 61(1) (2014), Article 2
    locator: the section "How do we avoid the barriers?" (oracles relative to which NEXP has ACC circuits)
---

Relativization is the method of asking a question about complexity classes in a world where every machine can call the same oracle. A statement relativizes if it stays true for every oracle. A proof relativizes if it goes through unchanged when an oracle is added to every machine in it. Most proofs by simulation and by diagonalization relativize. Baker, Gill and Solovay (1975) found one oracle that makes P equal to NP and another that makes them differ. So no proof that relativizes can settle the [P versus NP problem](/p-versus-np-problem/). This was the first of three known barriers, with [natural proofs](/natural-proofs-barrier/) and [algebrization](/algebrization-barrier/).

## In plain words

Imagine that every program, fast or slow, gets a magic helper that answers one fixed kind of question at no cost. Many proofs in complexity theory only use programs as black boxes: they run one program inside another, or they build a program that does the opposite of each program on a list. These proofs still work when every program has the same helper. Now suppose that, with one helper, finding a solution is as easy as checking it, and with another helper, it is not. A black-box proof cannot tell the two worlds apart, so it cannot prove either answer for the real world. To settle the question, a proof must use some fact about real programs that a magic helper can break.

## The idea

**Relativized classes.** An [oracle Turing machine](/oracle-turing-machine/) has a query tape. When it enters a query state, it receives in one step the answer to "is the string on the query tape in $A$?". For a class $\mathsf{C}$ defined by machines with a resource bound, $\mathsf{C}^A$ is the class defined by oracle machines of the same kind and bound with oracle $A$. So $\mathsf{P}^A$ uses deterministic oracle machines in polynomial time, and $\mathsf{NP}^A$ uses nondeterministic ones. For space-bounded classes the oracle tape needs a convention. The usual one, from Ladner and Lynch, makes it write-only and does not count it toward the space bound (see the [oracle Turing machine](/oracle-turing-machine/) page). The definition is for machine classes. A class that is defined in another way, such as $\mathsf{IP}$ by protocols, is relativized by giving the oracle to the verifier.

**Relativizing statements and proofs.** A statement such as $\mathsf{C} \subseteq \mathsf{D}$ or $\mathsf{C} \ne \mathsf{D}$ *relativizes* if $\mathsf{C}^A \subseteq \mathsf{D}^A$, or $\mathsf{C}^A \ne \mathsf{D}^A$, holds for every oracle $A$. A proof relativizes when every step remains valid for oracle machines. This is an informal notion, but it is easy to apply in practice. A proof that only simulates machines, counts their steps and diagonalizes against a list of them relativizes, because a universal oracle machine can simulate another oracle machine and pass each of its queries to the same oracle.

**The barrier.** Suppose that $\mathsf{C}^A = \mathsf{D}^A$ for one oracle $A$ and $\mathsf{C}^B \ne \mathsf{D}^B$ for another oracle $B$. A relativizing proof of $\mathsf{C} = \mathsf{D}$ would also prove $\mathsf{C}^B = \mathsf{D}^B$, which is false. A relativizing proof of $\mathsf{C} \ne \mathsf{D}$ would also prove $\mathsf{C}^A \ne \mathsf{D}^A$, which is false. So neither answer has a relativizing proof. The [Baker-Gill-Solovay theorem](/baker-gill-solovay-theorem/) gives such a pair of oracles for P and NP.

**What the barrier does not say.** An oracle result does not settle the question without oracles. The world with oracle $A$ is a different world. The statement $\mathsf{P}^A = \mathsf{NP}^A$ for a PSPACE-complete $A$ says nothing about whether $\mathsf{P} = \mathsf{NP}$. The barrier is a statement about methods. It rules out a family of proofs and leaves the question open.

**Random oracles.** Bennett and Gill (1981) showed that for an oracle $A$ chosen at random, with each string in $A$ independently with probability 1/2, $\mathsf{P}^A \ne \mathsf{NP}^A \ne \mathsf{coNP}^A$ holds with probability 1. They proposed the *random oracle hypothesis*: a statement that holds relative to a random oracle with probability 1 also holds without an oracle, at least for a natural family of statements. The hypothesis failed. Chang, Chor, Goldreich, Hartmanis, Håstad, Ranjan and Rohatgi (1994) proved that $\mathsf{IP}^A \ne \mathsf{PSPACE}^A$ with probability 1, while $\mathsf{IP} = \mathsf{PSPACE}$ holds. So random oracles do not predict the real answer either.

**Non-relativizing proofs.** Some known theorems are false relative to some oracle, so their proofs must use something that oracles break.

- $\mathsf{IP} = \mathsf{PSPACE}$ ([IP = PSPACE](/ip-equals-pspace/)). Fortnow and Sipser (1988) gave an oracle relative to which coNP has no interactive proof. Since $\mathsf{coNP} \subseteq \mathsf{PSPACE}$ holds for every oracle, the inclusion $\mathsf{PSPACE} \subseteq \mathsf{IP}$ fails relative to that oracle. The proof of $\mathsf{IP} = \mathsf{PSPACE}$ does not relativize. Its key step, arithmetization, turns a formula into a polynomial, and this uses the gates of the formula, which a black-box oracle does not have.
- $\mathsf{MIP} = \mathsf{NEXP}$ ([MIP = NEXP](/mip-equals-nexp/)) and the PCP theorem use the same kind of arithmetization. These results do not relativize, but they do *algebrize*, which is the subject of the [algebrization barrier](/algebrization-barrier/).
- Williams (2014) proved that NEXP does not have polynomial-size ACC circuits. He states that the proof avoids relativization, because there are oracles $A$ with $\mathsf{NEXP}^A \subseteq \mathsf{ACC}^A$.

## Examples

**The time hierarchy relativizes.** The proof of the [time hierarchy theorem](/time-hierarchy-theorem/) builds a machine $D$ that, on input $\langle M \rangle$, simulates $M$ for a fixed number of steps and does the opposite. Give $D$ and every $M$ the same oracle $A$, and let $D$ answer each query of $M$ by asking $A$ itself. Each query costs one step for both machines, so the simulation has the same overhead as before. The proof gives $\mathsf{DTIME}^A(f(n)) \subsetneq \mathsf{DTIME}^A(g(n))$ under the same conditions on $f$ and $g$, for every $A$. In particular $\mathsf{P}^A \ne \mathsf{EXP}^A$ for every oracle $A$.

**An oracle that collapses P and NP.** Let $A$ be TQBF, the set of true quantified Boolean formulas, which is PSPACE-complete under polynomial-time many-one reductions. Then $\mathsf{P}^A = \mathsf{NP}^A = \mathsf{PSPACE}$. A nondeterministic machine with oracle TQBF runs in polynomial space, because it can evaluate each query itself in polynomial space, and $\mathsf{NPSPACE} = \mathsf{PSPACE}$ by [Savitch's theorem](/savitch-theorem/). In the other direction, a polynomial-time machine with oracle TQBF decides any PSPACE language with one query after a reduction.

**An oracle that separates them.** The test language $U_B = \{1^n : B \text{ contains a string of length } n\}$ is in $\mathsf{NP}^B$ for every $B$: guess a string of length $n$ and ask $B$. A deterministic machine that runs in time $n^k$ can ask at most $n^k$ of the $2^n$ strings of length $n$. Baker, Gill and Solovay choose $B$ so that every such machine misses the one string that matters on some length. The full construction is on the [Baker-Gill-Solovay theorem](/baker-gill-solovay-theorem/) page.

**The oracle that changes nothing.** With $A = \emptyset$ every query answers "no", and a machine can skip its queries. So $\mathsf{C}^{\emptyset} = \mathsf{C}$ for the classes above. A statement that relativizes is in particular true without an oracle.

**Space-bounded classes.** With the Ladner and Lynch convention, $\mathsf{L}^A \subseteq \mathsf{P}^A$ holds for every oracle $A$, with the same proof as without an oracle: count the configurations of the work tapes, since the oracle tape is write-only. If the oracle tape were not counted and could also be read back, it would serve as extra work space, and this proof would no longer apply. So a relativized statement about space must name its convention.

## Where it is used

- **Testing proof ideas.** Before working on a separation such as P versus NP, a researcher checks whether the method relativizes. If it does, the method cannot work. This test, together with [natural proofs](/natural-proofs-barrier/) and [algebrization](/algebrization-barrier/), explains why simulation and diagonalization alone cannot resolve P versus NP. The page on the [P versus NP problem](/p-versus-np-problem/) summarizes the three barriers.
- **Structural complexity.** Oracle constructions show which relations among classes are consistent with relativizing methods. Baker, Gill and Solovay also built oracles for other relations among P, NP and coNP, such as an oracle relative to which NP is not closed under complement.
- **Query complexity.** An oracle separation is often a lower bound on the number of queries in disguise. The separating oracle for P and NP rests on the fact that a deterministic search for one marked string among $2^n$ strings needs many queries. See [query complexity](/query-complexity/) and, for quantum algorithms, the [quantum oracle](/quantum-oracle/).
- **Non-relativizing techniques.** Arithmetization in [interactive proofs](/interactive-proofs/) and the algorithmic method behind the ACC lower bound of Williams are the known ways past this barrier. See [algorithmic method](/algorithmic-method/).

## References
