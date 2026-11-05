---
tag: SVKGXR
kind: problem
slug: dfa-learning
name: DFA learning
aliases:
- automata learning
- regular language inference
area: automata-and-parsing/finite-automata
level: research
summary: Infer an unknown DFA from queries to a teacher or from labelled example strings.
prereqs: [deterministic-finite-automaton, myhill-nerode-relation, dfa-equivalence]
see_also: [lstar-algorithm, dfa-minimization, minimal-dfa-uniqueness, hopcroft-karp-equivalence, mealy-machine, moore-machine]
sources:
  - paper: doi:10.1016/0890-5401(87)90052-6
    title: Dana Angluin, Learning regular sets from queries and counterexamples, Information and Computation 75(2) (1987)
    locator: pp. 87 to 106 (the minimally adequate teacher and the L* algorithm)
  - paper: doi:10.1016/s0019-9958(67)91165-5
    title: E. Mark Gold, Language identification in the limit, Information and Control 10(5) (1967)
    locator: pp. 447 to 474
  - paper: doi:10.1016/s0019-9958(78)90562-4
    title: E. Mark Gold, Complexity of automaton identification from given data, Information and Control 37(3) (1978)
    locator: pp. 302 to 320 (NP-completeness of the minimum consistent DFA)
  - paper: doi:10.1016/s0019-9958(78)90683-6
    title: Dana Angluin, On the complexity of minimum inference of regular sets, Information and Control 39(3) (1978)
    locator: pp. 337 to 350
  - paper: doi:10.1145/138027.138042
    title: Leonard Pitt and Manfred K. Warmuth, The minimum consistent DFA problem cannot be approximated within any polynomial, Journal of the ACM 40(1) (1993)
    locator: pp. 95 to 142
  - paper: doi:10.1007/bf00116034
    title: Dana Angluin, Negative results for equivalence queries, Machine Learning 5(2) (1990)
    locator: pp. 121 to 150
  - paper: doi:10.1145/174644.174647
    title: Michael Kearns and Leslie Valiant, Cryptographic limitations on learning Boolean formulae and finite automata, Journal of the ACM 41(1) (1994)
    locator: pp. 67 to 95
  - paper: doi:10.1006/inco.1993.1021
    title: Ronald L. Rivest and Robert E. Schapire, Inference of finite automata using homing sequences, Information and Computation 103(2) (1993)
    locator: pp. 299 to 347
  - paper: doi:10.1109/tse.1978.231496
    title: Tsun S. Chow, Testing software design modeled by finite-state machines, IEEE Transactions on Software Engineering SE-4(3) (1978)
    locator: pp. 178 to 187 (the W-method)
  - paper: doi:10.1145/2967606
    title: Frits Vaandrager, Model learning, Communications of the ACM 60(2) (2017)
    locator: pp. 86 to 95 (active learning of models of software, and equivalence queries by testing)
---

DFA learning asks for the [DFA](/deterministic-finite-automaton/) of an unknown regular language, from information about the language. In the *active* setting, a learner asks a teacher whether given strings are in the language and whether a proposed DFA is correct; [Angluin's L* algorithm](/lstar-algorithm/) then finds the minimal DFA in polynomial time. In the *passive* setting, the learner only gets a finite set of labelled strings, and finding the smallest DFA that agrees with them is NP-hard, even to approximate. The two settings show how much the power to choose questions matters. Active learning is used to build models of black-box software and protocols.

## In plain words

Someone has a machine that says yes or no to words, and we want a copy of it. We cannot look inside.

If we may ask questions, the task is easy in a precise sense. We may ask "is this word a yes?" as often as we like, and we may also show our current guess and ask "is this right?". The answer to the second question is either "yes" or a word on which the guess is wrong. With these two kinds of question, a careful learner always finds the smallest correct machine, and it needs a number of questions that grows only polynomially with the size of the machine.

If we only get a fixed list of words with their answers, the task is hard. Many machines agree with the list, and finding the smallest one is as hard as the hardest puzzles of its kind.

## Definition

Fix an alphabet $\Sigma$ with $\sigma = |\Sigma|$. The target is a regular language $L \subseteq \Sigma^*$. Let $n$ be the number of states of its minimal complete DFA, which is unique by the [uniqueness of the minimal DFA](/minimal-dfa-uniqueness/). DFAs are complete and have no $\varepsilon$-moves.

**Active learning with a minimally adequate teacher** (Angluin, 1987). The learner may ask two kinds of query:

- a *membership query* $\mathrm{MQ}(w)$ for $w \in \Sigma^*$, answered by whether $w \in L$;
- an *equivalence query* $\mathrm{EQ}(H)$ for a DFA $H$, answered by "yes" if $L(H) = L$, and otherwise by a *counterexample* $c$ in the symmetric difference of $L(H)$ and $L$, chosen by the teacher.

The learner must halt with a DFA $H$ such that $L(H) = L$. It is *efficient* if its running time, and so its number of queries, is bounded by a polynomial in $n$, $\sigma$ and $m$, the length of the longest counterexample returned.

**Passive learning from a sample.** The input is two disjoint finite sets $S_+, S_- \subseteq \Sigma^*$. A DFA $D$ is *consistent* with them if $S_+ \subseteq L(D)$ and $S_- \cap L(D) = \emptyset$. The *minimum consistent DFA* problem asks for a consistent DFA with the fewest states; the decision version asks whether one with at most $k$ states exists.

**Identification in the limit** (Gold, 1967). The learner reads an infinite sequence of labelled examples and outputs a guess after each one. It identifies $L$ in the limit if, from some point on, all guesses are the same DFA for $L$.

## Variants

- **Membership queries only.** The learner may not ask equivalence queries. This needs exponentially many queries (see Bounds). If the learner knows $n$, it can ask all strings of length at most $2n - 2$, since two DFAs with at most $n$ states each that agree on these strings are equivalent; this is also exponential.
- **Equivalence queries only.** No polynomial algorithm exists (Angluin, 1990).
- **PAC learning.** Strings come from an unknown distribution, and the learner must find, with high probability, a DFA that errs on few strings of that distribution. With membership queries, L* gives a PAC learner, since a random sample can stand in for an equivalence query. Without them, PAC learning of DFAs is as hard as breaking some cryptographic assumptions (Kearns and Valiant, 1994).
- **Learning without reset.** The learner controls a machine that it cannot return to the start state, and only sees outputs. Rivest and Schapire (1993) solved it with homing sequences.
- **Machines with output.** For [Mealy machines](/mealy-machine/) and [Moore machines](/moore-machine/), the queries return output words instead of one bit. Learning tools for software use this form (Vaandrager, 2017).
- **Other targets.** Learning of NFAs, of residual automata, of automata over infinite words, and of register automata over data are research topics with their own algorithms.

## Examples

**A passive sample.** Over $\{a, b\}$, let $S_+ = \{b, ab, bb, aab\}$ and $S_- = \{\varepsilon, a, ba, aa\}$. No DFA with 1 state is consistent, because $b$ is accepted and $a$ is rejected. A search over all DFAs with 2 states found exactly one consistent DFA: the DFA for "ends with $b$", whose state is the last symbol read. So here the sample determines the 2-state answer.

**A sample that is too small.** With $S_+ = \{b\}$ and $S_- = \{\varepsilon\}$, the minimum is again 2 states, but a search found 8 different languages of 2-state DFAs consistent with this sample, among them "ends with $b$", "contains $b$" and "has odd length". The smallest consistent DFA is then a guess, and passive methods need samples that are rich enough to rule out the wrong ones.

**An active run.** The [L* page](/lstar-algorithm/) shows a full run on the language "even numbers of $a$s and of $b$s", whose minimal DFA has 4 states. The learner proposes a 2-state DFA, receives the counterexample $ba$, and then finds the 4-state DFA with 19 membership queries and 2 equivalence queries in all.

## Known algorithms

- **L*** (Angluin, 1987). An [observation table](/lstar-algorithm/) of membership answers, indexed by access strings and test suffixes, gives a hypothesis DFA when it is closed and consistent. Each counterexample adds at least one state, so at most $n - 1$ counterexamples are needed before the hypothesis has $n$ states and is correct. The original algorithm asks $O(\sigma m n^2)$ membership queries and runs in time polynomial in $n$, $\sigma$ and $m$.
- **Better handling of counterexamples.** Rivest and Schapire (1993) add one suffix of the counterexample, found by binary search, which brings the membership queries to $O(\sigma n^2 + n \log m)$. Discrimination-tree learners store only the suffixes that are needed to tell states apart.
- **Equivalence by testing.** When the target is a running system, an equivalence query is approximated by a test suite, for example the W-method of Chow (1978), which is complete when an upper bound on the number of states is known.
- **Passive learning by state merging.** Build the prefix tree of $S_+$ and $S_-$, then merge pairs of states as long as no string of $S_+$ and string of $S_-$ end in the same state. RPNI, by Oncina and García (1992), is the standard algorithm of this kind; it identifies the target in the limit and finds it exactly when the sample contains a characteristic set. Heuristic merge orders work well in practice but come with no size guarantee.
- **Exact passive learning.** The minimum consistent DFA can be found by trying $k = 1, 2, \ldots$ and searching for a consistent DFA with $k$ states, by brute force or by an encoding as Boolean satisfiability. The time is exponential in the worst case, as the hardness results require.

## Bounds

**Membership queries alone need exponentially many queries.** For $w \in \{a, b\}^k$, the language $\{w\}$ has a minimal DFA with $k + 2$ states: a path of $k + 1$ states plus a dead state. Consider a learner that only asks membership queries and knows that the target is one of these $2^k$ languages. Answer "no" to every query. Each answer rules out at most one candidate $w$. So after fewer than $2^k - 1$ queries, at least two candidates are consistent with all answers, and the learner's output is wrong for one of them. Hence $2^k - 1$ queries are needed, which is exponential in $n = k + 2$. $\square$

**Equivalence queries alone.** Angluin (1990) proved that no algorithm learns DFAs with polynomially many equivalence queries when the hypotheses are DFAs and the teacher chooses the counterexamples.

**Both kinds of query.** L* is polynomial. At most $n - 1$ equivalence queries are answered with a counterexample, since each one makes the hypothesis grow by at least one state and the hypotheses never have more than $n$ states.

**Passive learning is hard.** Deciding whether some DFA with at most $k$ states is consistent with $S_+$ and $S_-$ is NP-complete (Gold, 1978; Angluin, 1978). Pitt and Warmuth (1993) proved that, unless P = NP, no polynomial-time algorithm can even find a consistent DFA whose size is within any polynomial of the minimum.

**Identification in the limit.** From positive and negative examples that list all of $\Sigma^*$ with labels, the regular languages are identifiable in the limit: guess the first DFA in a fixed enumeration that is consistent with the data seen so far. From positive examples only, no learner identifies all regular languages in the limit, because any class that contains all finite languages and one infinite language is not identifiable in this way (Gold, 1967).

## Reductions

- **Learning to the Myhill-Nerode relation.** The states of the minimal DFA are the classes of the [Myhill-Nerode relation](/myhill-nerode-relation/). Active learners find a set of access strings, one per class, and a set of suffixes that separate them; the hypothesis is the quotient that these give.
- **Equivalence queries to DFA equivalence.** When the target DFA is known, as in tests or teaching tools, the teacher answers an equivalence query with an algorithm for [DFA equivalence](/dfa-equivalence/) such as [Hopcroft-Karp](/hopcroft-karp-equivalence/), which returns a counterexample.
- **From and to SAT.** The NP-hardness results are proved by reductions from satisfiability problems to the minimum consistent DFA problem. In the other direction, practical exact learners encode "a DFA with $k$ states is consistent with the sample" as a SAT instance.
- **PAC learning to equivalence queries.** An equivalence query can be replaced by a test on a random sample of strings; if no counterexample is found among enough samples, the hypothesis is probably approximately correct.

## Applications

- **Model learning of software.** Learning tools infer state machines of network protocol implementations, smart cards and embedded controllers, by running them as the membership oracle and testing as the equivalence oracle; the learned models are then checked or compared with specifications (Vaandrager, 2017).
- **Grammatical inference.** Passive DFA learning is used to infer patterns from example strings, in areas such as natural language processing and bioinformatics.
- **Verification.** Learned automata serve as assumptions in compositional verification and as models for model checking of black-box components.

## References
