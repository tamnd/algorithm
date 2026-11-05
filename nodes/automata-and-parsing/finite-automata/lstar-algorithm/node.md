---
tag: 2BJ5ME
kind: algorithm
slug: lstar-algorithm
name: L* algorithm
aliases:
- Angluin's L* algorithm
area: automata-and-parsing/finite-automata
level: research
summary: Learns a DFA from membership and equivalence queries using an observation table.
solves: [dfa-learning]
model: word-ram
complexity:
  vars: {n: the number of states of the minimal DFA of the target, σ: the alphabet size, m: the length of the longest counterexample}
  time: {worst: O(σ m n^3 (m + n))}
  space: {extra: O(σ m n^2 (m + n))}
properties: {deterministic: true, recursive: false}
history:
  year: 1987
  people: [Dana Angluin]
  note: Angluin introduced the minimally adequate teacher and showed with L* that it makes the regular languages learnable in polynomial time.
prereqs: [dfa-learning, myhill-nerode-relation, deterministic-finite-automaton]
see_also: [minimal-dfa-uniqueness, dfa-equivalence, hopcroft-karp-equivalence, dfa-minimization, mealy-machine, moore-minimization]
sources:
  - paper: doi:10.1016/0890-5401(87)90052-6
    title: Dana Angluin, Learning regular sets from queries and counterexamples, Information and Computation 75(2) (1987)
    locator: pp. 87 to 106 (the observation table, the algorithm L*, and its analysis)
  - paper: doi:10.1006/inco.1993.1021
    title: Ronald L. Rivest and Robert E. Schapire, Inference of finite automata using homing sequences, Information and Computation 103(2) (1993)
    locator: pp. 299 to 347 (the handling of counterexamples by binary search)
  - paper: doi:10.1006/inco.1995.1070
    title: Oded Maler and Amir Pnueli, On the learnability of infinitary regular sets, Information and Computation 118(2) (1995)
    locator: pp. 316 to 326 (adding the suffixes of a counterexample to the columns)
  - paper: doi:10.1007/978-3-319-11164-3_26
    title: Malte Isberner, Falk Howar and Bernhard Steffen, The TTT algorithm, a redundancy-free approach to active automata learning, Runtime Verification (RV 2014), Lecture Notes in Computer Science 8734
    locator: pp. 307 to 322
  - paper: doi:10.1007/978-3-642-05089-3_14
    title: Muzammil Shahbaz and Roland Groz, Inferring Mealy machines, FM 2009, Lecture Notes in Computer Science 5850
    locator: pp. 207 to 222
  - paper: doi:10.1145/2967606
    title: Frits Vaandrager, Model learning, Communications of the ACM 60(2) (2017)
    locator: pp. 86 to 95
---

The L* algorithm of Angluin (1987) learns the minimal [DFA](/deterministic-finite-automaton/) of an unknown regular language $L$ from a *teacher* who answers two kinds of question: membership queries, "is $w$ in $L$?", and equivalence queries, "does this DFA accept $L$?", answered by "yes" or by a counterexample. L* keeps a table of membership answers. Its rows are indexed by strings that reach states, and its columns by strings that tell states apart. When the table is complete in a precise sense, it defines a DFA, which L* proposes to the teacher. Each counterexample makes the next proposal larger, and no proposal is larger than the minimal DFA, so L* finishes after at most $n$ proposals, where $n$ is the number of states of the minimal DFA. The number of queries and the running time are polynomial in $n$, the alphabet size and the length of the counterexamples. This solves [DFA learning](/dfa-learning/) in the active setting, and L* and its descendants are the basis of model learning of software.

## In plain words

We want to rebuild a hidden machine that says yes or no to words. We may test any word, and we may show a guess and be told a word on which it is wrong.

The learner fills a grid. Each row is a start word, and each column is an ending that we add to it before we test. Two start words with different rows must lead to different places in the machine, because some ending tells them apart.

When every one-letter step from a known place lands on a known row, and equal rows step to equal rows, the grid describes a whole machine, and we show it. If it is wrong on some word, we add that word and its beginnings as rows. Each wrong guess forces at least one new place, and the hidden machine has only so many places.

## The problem

The learner knows the alphabet $\Sigma$, with $\sigma = |\Sigma|$, but not $L$. Let $n$ be the number of states of the minimal complete DFA of $L$. The teacher answers:

- $\mathrm{MQ}(w)$ for $w \in \Sigma^*$: whether $w \in L$;
- $\mathrm{EQ}(H)$ for a complete DFA $H$: "yes" if $L(H) = L$, and otherwise a counterexample $c$ with $c \in L \Leftrightarrow c \notin L(H)$.

The output is a DFA $H = (Q, \Sigma, \delta, q_0, F)$, complete and without $\varepsilon$-moves, with $L(H) = L$. L* returns the minimal one.

**The observation table.** It has a nonempty finite set $S \subseteq \Sigma^*$ of *access strings* that is prefix-closed, a nonempty finite set $E \subseteq \Sigma^*$ of *test suffixes* that is suffix-closed, and the function $T$ that maps each string of $(S \cup S\Sigma) E$ to its membership bit. For $s \in S \cup S\Sigma$, the *row* of $s$ is the function $\mathrm{row}(s) : E \to \{0, 1\}$, $e \mapsto T(se)$. The table is

- *closed* if for every $s \in S$ and $a \in \Sigma$ there is $s' \in S$ with $\mathrm{row}(sa) = \mathrm{row}(s')$;
- *consistent* if for all $s_1, s_2 \in S$ with $\mathrm{row}(s_1) = \mathrm{row}(s_2)$ and all $a \in \Sigma$, $\mathrm{row}(s_1 a) = \mathrm{row}(s_2 a)$.

A closed and consistent table defines the hypothesis $H(S, E, T)$ with the states $\{\mathrm{row}(s) : s \in S\}$, start state $\mathrm{row}(\varepsilon)$, accepting states $\{\mathrm{row}(s) : s \in S, T(s) = 1\}$ and

$$\delta(\mathrm{row}(s), a) = \mathrm{row}(sa).$$

Consistency makes $\delta$ independent of the choice of $s$, closedness puts $\mathrm{row}(sa)$ among the states, and $\varepsilon \in E$ makes the accepting states well defined.

## The algorithm

```pseudo id=main
LSTAR(Σ, MQ, EQ)
L1  S ← {ε}; E ← {ε}; fill T on (S ∪ SΣ)E with membership queries
L2  loop
L3      if s1, s2 ∈ S, a ∈ Σ, e ∈ E exist with row(s1) = row(s2) and T(s1 a e) ≠ T(s2 a e)
L4          add a e to E; fill T
L5      else if s ∈ S, a ∈ Σ exist with row(s a) ≠ row(s') for every s' ∈ S
L6          add s a to S; fill T
L7      else build the hypothesis H = H(S, E, T)
L8          ask EQ(H)
L9          if the answer is "yes": return H
L10         add the counterexample c and all its prefixes to S; fill T
```

Line L1 starts with one row and one column. "Fill $T$" asks a membership query for each string of $(S \cup S\Sigma)E$ that has no entry yet, so no string is asked twice. Lines L3 and L4 repair an inconsistency: the rows of $s_1$ and $s_2$ are equal, but the suffix $ae$ tells $s_1$ and $s_2$ apart, so adding $ae$ as a column splits their rows. Adding $ae$ keeps $E$ suffix-closed, since $e \in E$ and every suffix of $e$ is in $E$. Lines L5 and L6 repair a gap in closedness: the row of $sa$ is new, so $sa$ becomes an access string, which keeps $S$ prefix-closed. When the table is closed and consistent, line L7 builds the hypothesis and line L8 proposes it. If the teacher accepts it, line L9 returns it. Otherwise line L10 adds the counterexample and its prefixes to $S$, which keeps $S$ prefix-closed, and the loop repairs the table again.

The implementation stores $T$ in a hash map from strings to bits. It checks consistency by comparing each $s \in S$ only with the first access string that has the same row, which is enough because equality of rows is an equivalence relation.

## Example

Let $\Sigma = \{a, b\}$ and let $L$ be the set of strings with an even number of $a$s and an even number of $b$s. Its minimal DFA has 4 states, one for each pair of parities. The teacher returns a shortest counterexample, the first one in the order that tries $a$ before $b$.

**First table.** At line L1, $S = E = \{\varepsilon\}$, with $T(\varepsilon) = 1$ and $T(a) = T(b) = 0$. The row of $a$ is new, so lines L5 and L6 add $a$ to $S$. The table is now closed and consistent:

| | $\varepsilon$ |
|---|---|
| $\varepsilon$ | 1 |
| $a$ | 0 |
| $b$ | 0 |
| $aa$ | 1 |
| $ab$ | 0 |

The first two rows are $S$, the others $S\Sigma$. The hypothesis $H_1$ has the states $\mathrm{row}(\varepsilon) = 1$, accepting, and $\mathrm{row}(a) = 0$. Both letters leave state 1 to state 0; from state 0, $a$ returns to state 1 and $b$ stays. $H_1$ accepts $ba$, but $ba$ has one $a$, so the teacher returns $c = ba$.

**Repairs.** Line L10 adds $b$ and $ba$ to $S$. Now $\mathrm{row}(a) = \mathrm{row}(b) = 0$, but $T(aa) = 1$ and $T(ba) = 0$, so lines L3 and L4 add the column $a$. Then $\mathrm{row}(b) = \mathrm{row}(ba) = (0, 0)$ on the columns $\varepsilon, a$, but $T(bb) = 1$ and $T(bab) = 0$, so the column $b$ is added. The final table is closed and consistent:

| | $\varepsilon$ | $a$ | $b$ |
|---|---|---|---|
| $\varepsilon$ | 1 | 0 | 0 |
| $a$ | 0 | 1 | 0 |
| $b$ | 0 | 0 | 1 |
| $ba$ | 0 | 0 | 0 |
| $aa$ | 1 | 0 | 0 |
| $ab$ | 0 | 0 | 0 |
| $bb$ | 1 | 0 | 0 |
| $baa$ | 0 | 0 | 1 |
| $bab$ | 0 | 1 | 0 |

The four rows of $S$ are different, and they are the four parity classes $(0,0)$, $(1,0)$, $(0,1)$ and $(1,1)$. For example, $\mathrm{row}(ab) = \mathrm{row}(ba)$, so $\delta(\mathrm{row}(a), b) = \mathrm{row}(ba)$. The hypothesis $H_2$ is the minimal DFA of $L$, and the teacher says "yes". The run asked 2 equivalence queries and 19 membership queries, one for each distinct string in the table. The test file checks these numbers and the counterexample $ba$.

## Correctness

The full proof is in the correctness file. Its parts are:

1. **The hypothesis agrees with the table.** If the table is closed and consistent, then $H(S, E, T)$ reaches the state $\mathrm{row}(s)$ on each $s \in S \cup S\Sigma$, and it accepts $se$ if and only if $T(se) = 1$, for all $s \in S \cup S\Sigma$ and $e \in E$. The proof is by induction on $|s|$ and then on $|e|$, and uses that $S$ is prefix-closed and $E$ is suffix-closed.
2. **The hypothesis is the smallest such DFA.** Let $k$ be the number of distinct rows of $S$. Every DFA that agrees with the table and has at most $k$ states is isomorphic to $H(S, E, T)$.
3. **Distinct rows are distinct states.** Two strings with different rows are separated by a suffix in $E$, so they lie in different classes of the [Myhill-Nerode relation](/myhill-nerode-relation/) of $L$. So $k \le n$. Adding to $S$ or $E$ never merges rows, lines L4 and L6 each increase $k$, and so they run at most $n - 1$ times in all.
4. **Each counterexample makes the hypothesis larger.** After line L10, $c \in S$, so the next hypothesis $H'$ agrees with the target on $c$ and differs from $H$. $H'$ has at least as many states as $H$, and if it had the same number, part 2 would make it isomorphic to $H$. So $H'$ has more states. Hypotheses have at most $n$ states, so there are at most $n$ equivalence queries.
5. **The output is minimal.** The returned $H$ accepts $L$ and has at most $n$ states, so it has exactly $n$, and it is the minimal DFA by the [uniqueness of the minimal DFA](/minimal-dfa-uniqueness/).

## Complexity

Let $m$ be the length of the longest counterexample.

- **Size of the table.** $|E| \le n$, since $E$ starts with one column and each column added by line L4 increases $k \le n$. $S$ starts with $\varepsilon$, gains at most $n - 1$ strings at line L6, and at most $m$ strings at each of at most $n - 1$ counterexamples. So $|S| \le n + m(n - 1)$, and the table has at most $(\sigma + 1)(n + m(n - 1)) n = O(\sigma m n^2)$ entries.
- **Queries.** At most $n$ equivalence queries, and at most $(\sigma + 1)(n + m(n - 1)) n$ membership queries, since each entry is asked once.
- **Time.** The loop runs at most $3n$ times: at most $n - 1$ times through line L4, $n - 1$ times through line L6, and $n$ times through line L8. Each pass checks consistency and closedness and builds rows, which reads $O(\sigma m n^2)$ entries of the table, each keyed by a string of length $O(m + n)$. So the time is $O(\sigma m n^3 (m + n))$, not counting the time the teacher takes to answer.
- **Space.** The table stores $O(\sigma m n^2)$ strings of length $O(m + n)$, so $O(\sigma m n^2 (m + n))$ space.

With a teacher that returns shortest counterexamples, $m \le 2n - 2$, because two DFAs with at most $n$ states each that differ also differ on a string of length at most $2n - 2$. Then everything is polynomial in $n$ and $\sigma$ alone.

## Properties

- **Exact and minimal.** The output accepts $L$ exactly and is its minimal DFA.
- **Monotone hypotheses.** The hypotheses have strictly increasing numbers of states, $1 \le |H_1| < |H_2| < \cdots \le n$.
- **Teacher-independent correctness.** Any valid counterexample works; the choice only affects $m$ and the number of steps.
- **No repeated membership queries.** The table caches every answer.
- **Not recursive.** The algorithm is one loop over a table.

## Variants and improvements

- **Suffixes as columns** (Maler and Pnueli, 1995). Instead of adding the prefixes of $c$ to $S$, add all suffixes of $c$ to $E$. Then the rows of $S$ stay pairwise distinct, the table is always consistent, and line L3 is not needed.
- **One suffix by binary search** (Rivest and Schapire, 1993). A counterexample contains a single position where the hypothesis's guess of the state goes wrong; binary search finds it with $O(\log m)$ membership queries, and one new suffix is added. The total is $O(\sigma n^2 + n \log m)$ membership queries.
- **Discrimination trees.** Kearns and Vazirani store only the suffixes needed to separate the access strings, in a tree. The TTT algorithm of Isberner, Howar and Steffen (2014) also keeps the suffixes short, which saves queries when the counterexamples are long.
- **Mealy machines.** For systems with outputs, the table holds output strings instead of bits. Shahbaz and Groz (2009) gave a version for [Mealy machines](/mealy-machine/) that adds the suffixes of counterexamples to the columns.
- **PAC learning.** An equivalence query can be replaced by a test on random strings. If the $i$-th query tests enough strings, the result is probably approximately correct (Angluin, 1987).

## When to use it

Use L* or one of its variants when a system can be queried but not inspected: when a black-box component can be reset and run on chosen inputs, and conformance tests can stand in for equivalence queries (Vaandrager, 2017). It also suits teaching tools and tests where the target DFA is known and the teacher can answer with [DFA equivalence](/dfa-equivalence/). With a large alphabet, long counterexamples or expensive queries, prefer a variant with suffix handling by binary search or discrimination trees. For learning from a fixed sample without queries, L* does not apply; see [DFA learning](/dfa-learning/).

## Pitfalls

- **The alphabet must be known.** The table has a row for each $s a$ with $a \in \Sigma$. A symbol that is missing from $\Sigma$ is never tested.
- **Prefixes of the counterexample.** Adding only $c$ to $S$ breaks prefix-closedness, and then the hypothesis can be wrong on the table. Add all prefixes, or use the suffix variants.
- **Checking only closedness.** When counterexample prefixes are added to $S$, two access strings can have equal rows, and skipping the consistency check gives an ill-defined transition function.
- **Approximate equivalence queries.** In practice, equivalence queries are answered by testing, which can miss a difference. The result is then a correct model of the tested behaviour only, and a bound on the number of states is needed for a complete test suite.
- **Nondeterministic or noisy systems.** L* assumes that each membership query has one fixed answer. A system that answers differently on repeated runs breaks the table.
- **Long counterexamples.** A teacher that returns long counterexamples makes $S$ large; the binary search variant avoids this.

## Implementations

## History

Gold (1967) introduced identification in the limit, and Gold (1978) and Angluin (1978) showed that finding a smallest DFA consistent with given examples is NP-hard. Angluin (1987) introduced the minimally adequate teacher with its membership and equivalence queries, and L* showed that this teacher makes the regular languages learnable in polynomial time. Rivest and Schapire (1993) improved the treatment of counterexamples and removed the need for a reset. Maler and Pnueli (1995) introduced the variant that adds suffixes as columns while studying automata on infinite words. Later work brought discrimination trees, the TTT algorithm (2014), and learning of Mealy machines (Shahbaz and Groz, 2009), and turned the method into a tool for building models of software and protocols (Vaandrager, 2017).

## References
