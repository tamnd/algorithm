---
tag: W1V17Z
kind: model
slug: oracle-turing-machine
name: Oracle Turing machine
aliases:
- Turing machine with an oracle
- Turing machine with oracle
- oracle machine
area: complexity/computability
level: advanced
summary: "A Turing machine with a query tape that can ask whether a string is in a fixed set A, the oracle, and gets the answer in one step. It defines Turing reducibility and relativized classes such as P^A."
prereqs: [turing-machine, halting-problem]
see_also: [turing-degrees, turing-jump, turing-reduction, relativization, baker-gill-solovay-theorem, polynomial-hierarchy, query-model, many-one-reducibility]
sources:
  - paper: doi:10.1112/plms/s2-45.1.161
    title: "Alan M. Turing, Systems of logic based on ordinals, Proceedings of the London Mathematical Society (2) 45 (1939)"
    locator: "pp. 161 to 228 (the o-machine)"
  - paper: doi:10.1090/S0002-9904-1944-08111-1
    title: "Emil L. Post, Recursively enumerable sets of positive integers and their decision problems, Bulletin of the American Mathematical Society 50 (1944)"
    locator: "pp. 284 to 316 (Turing reducibility as a reducibility between sets)"
  - paper: doi:10.1007/BF01683260
    title: "Richard E. Ladner and Nancy A. Lynch, Relativization of questions about log space computability, Mathematical Systems Theory 10 (1976)"
    locator: pp. 19 to 32
  - book: isbn:9783642319327
    title: "Robert I. Soare, Turing Computability, Theory and Applications, Springer, 2016"
    locator: "Chapter 3, Turing Reducibility"
  - book: isbn:9780521424264
    title: "Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009"
    locator: "Chapter 3 (oracle machines and the limits of diagonalization)"
---

An oracle Turing machine is a [Turing machine](/turing-machine/) with one extra ability: it can ask whether a string is in a fixed set $A$, called the oracle, and it receives the answer in a single step. The machine does not know how the answers are found; $A$ can be any set, including undecidable sets such as the [halting problem](/halting-problem/). Turing introduced the model in 1939 as the "o-machine". It defines Turing reducibility: $A \le_T B$ if some oracle machine with oracle $B$ decides $A$. In computability the model is the basis of [Turing degrees](/turing-degrees/), the [Turing jump](/turing-jump/) and the [arithmetical hierarchy](/arithmetical-hierarchy/). In complexity theory, the same machine with a time bound defines classes such as $\mathrm{P}^A$ and $\mathrm{NP}^A$, the polynomial-time Turing reductions of the [Turing reduction](/turing-reduction/) page, and the oracle results of [relativization](/relativization/).

## The machine

An oracle Turing machine $M$ is a deterministic Turing machine with these additions:

- a second tape, the *oracle tape* or *query tape*, with its own head, on which $M$ writes the string to ask about;
- three special states: the query state $q_?$ and the two answer states $q_{\mathrm{yes}}$ and $q_{\mathrm{no}}$.

The machine runs with an *oracle* $A \subseteq \Sigma^*$ (or $A \subseteq \mathbb{N}$, with numbers written in binary). It moves as an ordinary machine in every state except $q_?$. When it enters $q_?$ with the string $w$ on the oracle tape, the next state is $q_{\mathrm{yes}}$ if $w \in A$ and $q_{\mathrm{no}}$ if $w \notin A$, in one step. In the complexity convention the oracle tape is then erased and its head returns to the first cell; in computability the convention does not matter.

**What it computes.** $M^A$ denotes $M$ run with oracle $A$. It decides a set, accepts a set or computes a partial function, as an ordinary machine does. The program of $M$ does not depend on $A$: the same text runs with every oracle and can give different results. With a fixed computable numbering of the programs (the encoding is fixed and computable), $\Phi_e^A$ is the partial function that the $e$-th oracle program computes with oracle $A$, and $W_e^A = \mathrm{dom}(\Phi_e^A)$.

**Reductions.** For sets $A$ and $B$:

- $A \le_T B$ (*$A$ is Turing reducible to $B$*, or *$A$ is computable in $B$*) if $A = \{x : M^B \text{ accepts } x\}$ for some oracle machine $M$ that halts on every input with oracle $B$;
- $A$ is *c.e. in $B$* if $A = W_e^B$ for some $e$.

**Use.** A halting computation is finite, so it makes finitely many queries. The *use* of the computation of $\Phi_e^A(x)$ is one more than the largest number queried. If $B$ agrees with $A$ on every number below the use, then $\Phi_e^B(x) = \Phi_e^A(x)$, with the same computation. This is the *use principle*, and it is what makes oracle constructions possible: to keep a computation, a construction only has to protect a finite part of the oracle.

**Worked example.** Let $A$ be the set of primes and let $M$ compute the parity of the number of elements of $A$ below $x$. With $x = 20$, $M$ queries $0, 1, \ldots, 19$, which is 20 queries, and gets yes for $2, 3, 5, 7, 11, 13, 17, 19$. The count is 8, so the output is $0$. The use is 20: every oracle $B$ that agrees with the primes below 20 gives the same output for $x = 20$, whatever $B$ contains above. Here $A$ is decidable, so the oracle saves time but not power. With the oracle $K$, the machine that on input $e$ queries $e$ and outputs the answer decides $K$ with one query, which no ordinary machine can do.

## What it counts

**In computability** the model counts nothing: the question is only whether a function is computable with the oracle. A query is one step, whatever the oracle.

**In complexity** the cost is the number of steps of $M$, with each query counted as one step plus the steps that write the query string. So a machine that runs in time $t$ can ask only strings of length at most $t$. $\mathrm{P}^A$ is the class of languages decided in polynomial time with oracle $A$, and $\mathrm{NP}^A$ uses a nondeterministic oracle machine. For a class $\mathcal{C}$, $\mathrm{P}^{\mathcal{C}}$ is the union of $\mathrm{P}^A$ over $A \in \mathcal{C}$.

**Space.** For space-bounded oracle machines the oracle tape needs a convention, because a query can be longer than the space bound. The usual one, from Ladner and Lynch (1976), makes the oracle tape write-only and does not count it in the space used.

**Queries.** The number of queries, and whether later queries depend on the answers to earlier ones, give finer measures. A machine whose queries are all fixed before it gets any answer makes a *truth-table* (non-adaptive) reduction. A machine that asks one query and outputs the answer as its own makes a [many-one reduction](/many-one-reducibility/). The [query model](/query-model/) counts only queries, to the input itself, and makes all other work free.

## Relation to other models

- **Turing machines.** An ordinary machine is an oracle machine that never queries, or one with a [decidable](/decidable-language/) oracle: if $B$ is decidable, a machine can answer each query itself, so $A \le_T B$ implies that $A$ is decidable.
- **Variants of the machine.** Multitape, nondeterministic and alternating machines all have oracle versions, defined by the same three states. A universal oracle machine $U$ exists: $U^A(e, x) = \Phi_e^A(x)$ for every oracle $A$, by the construction of the [universal Turing machine](/universal-turing-machine/).
- **Reductions.** Turing reducibility is the most general of the standard reducibilities between sets. Many-one and truth-table reductions are oracle machines with limits on the queries. The polynomial-time version, the Cook reduction, is the [Turing reduction](/turing-reduction/) of complexity theory.
- **Relativization.** A proof *relativizes* if it stays true when every machine in it is given the same oracle. Most proofs by simulation and [diagonalization](/diagonalization-argument/), including the time and space hierarchy theorems and the undecidability of the halting problem, relativize. See [relativization](/relativization/).
- **The polynomial hierarchy.** Oracle machines give one definition of the [polynomial hierarchy](/polynomial-hierarchy/): $\Sigma_{k+1}^{\mathrm{P}} = \mathrm{NP}^{\Sigma_k^{\mathrm{P}}}$. The [arithmetical hierarchy](/arithmetical-hierarchy/) has the same shape, with "c.e. in" in place of $\mathrm{NP}$ (see [Post's theorem](/posts-theorem/)).

## Known results in the model

- **Turing reducibility is a preorder.** $A \le_T A$, and if $A \le_T B$ and $B \le_T C$, then $A \le_T C$: replace each query to $B$ by a run of the machine for $B$ with oracle $C$. The equivalence classes are the [Turing degrees](/turing-degrees/).
- **Relativized computability theory.** The enumeration theorem, the [s-m-n theorem](/s-m-n-theorem/) and [Kleene's recursion theorem](/kleene-recursion-theorem/) hold for oracle programs, with the same proofs, for every oracle.
- **The halting problem relative to $A$.** The set $A' = \{ e : \Phi_e^A(e)\!\downarrow \}$ is c.e. in $A$ and not computable in $A$, by the diagonal proof for $K$ run with the oracle. This is the [Turing jump](/turing-jump/). In particular, an oracle for $K$ does not decide the halting problem for oracle machines with oracle $K$.
- **Post's criterion.** $A \le_T B$ if and only if both $A$ and its complement are c.e. in $B$. This is the relativized form of the theorem that a set is decidable exactly when it and its complement are c.e.
- **Oracles for P versus NP.** Baker, Gill and Solovay (1975) gave an oracle $A$ with $\mathrm{P}^A = \mathrm{NP}^A$, for example any PSPACE-complete set, and an oracle $B$ with $\mathrm{P}^B \ne \mathrm{NP}^B$. So no proof that relativizes can settle whether $\mathrm{P} = \mathrm{NP}$ ([Baker-Gill-Solovay theorem](/baker-gill-solovay-theorem/)).
- **Incomparable sets.** Kleene and Post (1954) built, with oracle machines and finite-extension arguments, two sets that are each computable in $K$ and neither computable in the other. The question for c.e. sets is [Post's problem](/post-problem/).

## References
