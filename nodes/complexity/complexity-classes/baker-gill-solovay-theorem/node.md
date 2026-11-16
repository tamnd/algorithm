---
tag: PP2RJR
kind: theorem
slug: baker-gill-solovay-theorem
name: Baker-Gill-Solovay theorem
aliases:
- oracles separating P and NP
area: complexity/complexity-classes
level: advanced
summary: "There is an oracle A with P^A = NP^A (any PSPACE-complete set) and an oracle B with P^B != NP^B (built by diagonalization). So no relativizing proof settles P versus NP."
prereqs: [oracle-turing-machine, relativization, pspace, qsat, diagonalization-argument]
see_also: [relativization, oracle-turing-machine, p-versus-np-problem, natural-proofs-barrier, algebrization-barrier, time-hierarchy-theorem, query-complexity, ladner-theorem]
sources:
  - paper: doi:10.1137/0204037
    title: Theodore Baker, John Gill and Robert Solovay, Relativizations of the P =? NP question, SIAM Journal on Computing 4(4) (1975)
    locator: pp. 431 to 442 (the oracle that makes P and NP equal, the oracle that separates them, and oracles for the relations among P, NP and coNP)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Section 3.4, Oracle machines and the limits of diagonalization (the theorem of Baker, Gill and Solovay with both constructions)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 9.2, Relativization (limits of the diagonalization method)
  - book: isbn:9780201530827
    title: Christos H. Papadimitriou, Computational Complexity, Addison-Wesley, 1994
    locator: Section 14.3, Oracles
  - paper: doi:10.1137/0210008
    title: Charles H. Bennett and John Gill, Relative to a random oracle A, P^A != NP^A != co-NP^A with probability 1, SIAM Journal on Computing 10(1) (1981)
    locator: pp. 96 to 113 (separation relative to a random oracle)
---

The Baker-Gill-Solovay theorem says that the [P versus NP problem](/p-versus-np-problem/) goes one way relative to one oracle and the other way relative to another. With an oracle for a PSPACE-complete set, every NP machine can be simulated in polynomial time, so P and NP become equal. With an oracle built by diagonalization, NP can find a single hidden string that no polynomial-time machine can find, so P and NP differ. A proof that stays valid when every machine gets the same oracle would give the same answer in both worlds. So no such proof can settle P versus NP. Baker, Gill and Solovay proved the theorem in 1975, and it is the origin of the [relativization](/relativization/) barrier.

## Statement

All machines are [oracle Turing machines](/oracle-turing-machine/) with multitape work tapes and a query tape. A query costs one step. $\mathsf{P}^X$ and $\mathsf{NP}^X$ are the classes decided in polynomial time by deterministic and by nondeterministic oracle machines with oracle $X$.

**Theorem (Baker, Gill and Solovay, 1975).**

1. If $A$ is PSPACE-complete under polynomial-time many-one reductions, for example $A = \mathrm{TQBF}$, the set of true quantified Boolean formulas, then $\mathsf{P}^A = \mathsf{NP}^A = \mathsf{PSPACE}$.
2. There is a decidable set $B$ with $\mathsf{P}^B \ne \mathsf{NP}^B$. The language $U_B = \{1^n : B \text{ contains a string of length } n\}$ is in $\mathsf{NP}^B \setminus \mathsf{P}^B$.

The two parts concern different oracles. Neither part says anything about P and NP without an oracle.

## In plain words

Give every program a helper that answers one fixed kind of question in one step. If the helper can answer any question about a game of two players with many rounds, then it is so strong that guessing gives no extra power: a program that checks proofs and a program that finds them become equally fast. Now take a different helper, a secret list with at most one word of each length. A guessing program finds out whether a word of a given length is on the list by guessing the word and asking once. A program that does not guess must ask about words one by one, and there are too many. The list is chosen so that each fast program misses the word on some length. The two worlds give opposite answers, so a proof that ignores which helper is present cannot decide the question.

## Proof

**Part 1: a collapsing oracle.** Let $A = \mathrm{TQBF}$. It is PSPACE-complete under polynomial-time many-one reductions, and a recursive evaluation decides it in space polynomial in the length of the formula ([QSAT](/qsat/)).

*$\mathsf{NP}^A \subseteq \mathsf{PSPACE}$.* Let $N$ be a nondeterministic oracle machine with oracle $A$ that runs in time $p(n)$. A deterministic machine goes through all sequences of at most $p(n)$ nondeterministic choices, one after another, and reuses the same space for each. For each sequence it simulates $N$ along that path. When $N$ asks a query, the query has at most $p(n)$ symbols, and the simulator evaluates it in space polynomial in $p(n)$. It accepts if some path accepts. The space is polynomial in $n$.

*$\mathsf{PSPACE} \subseteq \mathsf{P}^A$.* Let $L \in \mathsf{PSPACE}$, and let $f$ be a polynomial-time many-one reduction from $L$ to $A$. The oracle machine computes $f(x)$, asks the query $f(x)$, and accepts if the answer is yes. This takes polynomial time.

*$\mathsf{P}^A \subseteq \mathsf{NP}^A$* holds for every oracle, since a deterministic machine is a nondeterministic one. So $\mathsf{NP}^A \subseteq \mathsf{PSPACE} \subseteq \mathsf{P}^A \subseteq \mathsf{NP}^A$, and the three classes are equal.

The same argument works for every PSPACE-complete set $A$, because $A$ is in PSPACE and so has a decision procedure in polynomial space.

**Part 2: a separating oracle.** For any set $B$, the language $U_B$ is in $\mathsf{NP}^B$. A nondeterministic machine rejects an input that is not of the form $1^n$, guesses a string $w$ of length $n$, asks whether $w \in B$, and accepts if the answer is yes. This takes $O(n)$ steps. It remains to build $B$ so that $U_B \notin \mathsf{P}^B$.

*A list of clocked machines.* Let $M_1, M_2, \ldots$ list all pairs $(M, k)$ of a deterministic oracle machine $M$ and a number $k \ge 1$. The machine $M_i$, for the pair $(M, k_i)$, runs $M$ for at most $n^{k_i} + k_i$ steps on an input of length $n$, and rejects if $M$ has not halted by then. Every language in $\mathsf{P}^B$ is decided by some $M_i$ with oracle $B$. Indeed, if $M$ with oracle $B$ halts within $c n^k + c$ steps, take the pair $(M, k + 2c)$. For $n \ge 2$ we have $c \le 2^c \le n^c$, so $c n^k + c \le n^{k + 2c} + (k + 2c)$, and for $n \le 1$ the left side is at most $2c$. So the clock never stops $M$ early.

*The construction.* $B$ is built in stages. Before stage $i$ there is a finite set $B_{i-1}$ and a number $\ell_{i-1}$ such that membership in $B$ of every string of length at most $\ell_{i-1}$ is already fixed. Start with $B_0 = \emptyset$ and $\ell_0 = 0$.

At stage $i$:

1. Choose $n_i > \ell_{i-1}$ with $n_i^{k_i} + k_i < 2^{n_i}$. Such an $n_i$ exists, because $2^n$ grows faster than every polynomial.
2. Run $M_i$ on $1^{n_i}$, and answer each query $q$ with "yes" if $q \in B_{i-1}$ and "no" otherwise.
3. If $M_i$ accepts, let $B_i = B_{i-1}$. If $M_i$ rejects, it asked at most $n_i^{k_i} + k_i < 2^{n_i}$ queries, so some string $w$ of length $n_i$ was not asked. Let $B_i = B_{i-1} \cup \{w\}$ for the first such $w$.
4. Let $\ell_i = n_i^{k_i} + k_i$. No query of $M_i$ in step 2 is longer than $\ell_i$, since writing a query takes one step per symbol, and $\ell_i \ge n_i$.

Let $B = \bigcup_i B_i$. Every string that stage $j$ adds has length $n_j > \ell_{j-1}$. So for $j > i$, stage $j$ adds only strings longer than $\ell_i$.

*The diagonal argument.* Fix $i$. Compare the run of $M_i$ on $1^{n_i}$ with oracle $B$ to the run in stage $i$. The two oracles $B$ and $B_{i-1}$ differ on at most these strings: the string $w$ added in stage $i$, which $M_i$ did not ask, and strings added in later stages, which are longer than $\ell_i$ and so are not asked either. So both runs get the same answers to the same queries, and they end the same way.

- If $M_i$ accepts $1^{n_i}$, then stage $i$ adds nothing. The strings of $B_{i-1}$ have lengths $n_1, \ldots, n_{i-1}$, all at most $\ell_{i-1} < n_i$, and later strings are longer than $\ell_i \ge n_i$. So $B$ has no string of length $n_i$, and $1^{n_i} \notin U_B$.
- If $M_i$ rejects $1^{n_i}$, then $w \in B$ has length $n_i$, and $1^{n_i} \in U_B$.

In both cases $M_i$ with oracle $B$ gives the wrong answer on $1^{n_i}$. Every language in $\mathsf{P}^B$ is decided by some $M_i$, so $U_B \notin \mathsf{P}^B$.

*$B$ is decidable.* To decide whether a string $x$ is in $B$, run the stages until $\ell_i \ge |x|$. Each stage is a finite computation, and after it the membership of $x$ is fixed. $\blacksquare$

**A worked stage.** The condition $n^k + k < 2^n$ first holds at $n = 5$ for $k = 2$ (since $27 < 32$), at $n = 10$ for $k = 3$, at $n = 17$ for $k = 4$ and at $n = 23$ for $k = 5$. In each case $n \ge 2k$, and then $(n + 1)^k \le e^{k/n} n^k < 2 n^k$, so the left side less than doubles while $2^n$ doubles. The inequality then holds for every larger $n$. Take a toy machine that, on $1^n$, asks about the first $n^2$ strings of length $n$ in lexicographic order and accepts if one of them is in the oracle. At $n = 5$ it asks 25 of the 32 strings, from $00000$ to $11000$. All answers are "no", so it rejects. The stage adds $11001$, the first string it did not ask. With the new oracle the machine asks the same 25 strings, gets the same answers and still rejects, but now $1^5 \in U_B$.

## Consequences

- **No relativizing proof settles P versus NP.** A proof of $\mathsf{P} = \mathsf{NP}$ that relativizes would prove $\mathsf{P}^B = \mathsf{NP}^B$, and a proof of $\mathsf{P} \ne \mathsf{NP}$ that relativizes would prove $\mathsf{P}^A \ne \mathsf{NP}^A$. Both are false. This rules out proofs that only simulate machines and diagonalize against them, such as the proof of the [time hierarchy theorem](/time-hierarchy-theorem/). See [relativization](/relativization/).
- **Other questions have the same status.** Part 1 also gives $\mathsf{NP}^A = \mathsf{coNP}^A$, since both equal PSPACE. If the query tape counts toward the space bound, so that queries have polynomial length, then also $\mathsf{PSPACE}^A = \mathsf{PSPACE} = \mathsf{P}^A$. Part 2 gives $\mathsf{P}^B \ne \mathsf{NP}^B \subseteq \mathsf{PSPACE}^B$, so $\mathsf{P}^B \ne \mathsf{PSPACE}^B$. Baker, Gill and Solovay also built an oracle relative to which NP is not closed under complement. So NP versus coNP and P versus PSPACE need non-relativizing proofs too.
- **The answer is not decided by the theorem.** An oracle world is a different world. The theorem gives no evidence for either answer to P versus NP without oracles.
- **A link to query complexity.** Part 2 rests on a query lower bound. $U_B$ on length $n$ is the OR of the $2^n$ bits "is $w$ in $B$". A nondeterministic machine needs one query to certify a yes answer, and a deterministic machine that asks fewer than $2^n$ queries can be fooled. See [query complexity](/query-complexity/).

## Tightness

- **The time bound in Part 2.** The proof used only that $M_i$ asks fewer than $2^{n_i}$ queries on some input length. So for every time-constructible bound $t(n)$ with $t(n) = o(2^n)$, the same construction gives an oracle $B$ with $U_B \notin \mathsf{DTIME}^B(t(n))$, while $U_B \in \mathsf{NTIME}^B(n)$. The bound cannot go past $2^n$ in this form: a deterministic machine that asks all $2^n$ strings of length $n$ decides $U_B$ for every $B$, in time $O(n 2^n)$.
- **Random oracles.** The separating oracle is not special. Bennett and Gill (1981) proved that for a random oracle $R$, with each string in $R$ independently with probability 1/2, $\mathsf{P}^R \ne \mathsf{NP}^R$ holds with probability 1. So the oracles with $\mathsf{P}^A = \mathsf{NP}^A$, such as the PSPACE-complete sets, form a set of measure 0.
- **Beyond relativization.** Some true statements fail relative to an oracle, for example $\mathsf{IP} = \mathsf{PSPACE}$ (see [IP = PSPACE](/ip-equals-pspace/)). So some theorems have no relativizing proof, and the known proofs of them use arithmetization. The [algebrization barrier](/algebrization-barrier/) shows that P versus NP also resists a stronger family of methods.

## History

Baker, Gill and Solovay published the theorem in SIAM Journal on Computing in 1975, in a paper that also studied oracles for the relations among P, NP and coNP. Bennett and Gill (1981) showed that random oracles separate P and NP, and they proposed the random oracle hypothesis, which was later refuted. Fortnow and Sipser (1988) gave an oracle relative to which coNP has no interactive proof, and the proof of $\mathsf{IP} = \mathsf{PSPACE}$ in 1990 then gave a clear example of a theorem whose proof does not relativize. Razborov and Rudich (1994) and Aaronson and Wigderson (2008) found two further barriers, [natural proofs](/natural-proofs-barrier/) and [algebrization](/algebrization-barrier/).

## References
