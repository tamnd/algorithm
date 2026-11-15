---
tag: HSQPF9
kind: model
slug: defeasible-logic-programming
name: Defeasible logic programming
aliases:
- DeLP
area: information-retrieval-and-ai-reasoning/argumentation-and-belief-revision
level: advanced
summary: Logic programs with strict and defeasible rules, where a query is warranted by a dialectical tree of arguments and defeaters.
prereqs: [logic-programming, abstract-argumentation-framework]
see_also: [aspic-plus, assumption-based-argumentation, value-based-argumentation, minimax, alpha-beta-pruning, negation-as-failure, nonmonotonic-reasoning, grounded-extension]
sources:
  - paper: doi:10.1017/S1471068403001674
    title: Alejandro J. García and Guillermo R. Simari, Defeasible logic programming, an argumentative approach, Theory and Practice of Logic Programming 4(1-2), 95 to 138 (2004)
    locator: "Definitions 2.4 to 5.3 (programs, derivations, argument structures, disagreement, counter-arguments, generalized specificity, proper and blocking defeaters, acceptable argumentation lines, dialectical trees, warrant, answers), Procedure 5.1 (marking), Example 2.1 and Section 5.1 (pruning)"
  - paper: "On the complexity of DeLP through game semantics"
    title: Laura A. Cecchi, Pablo R. Fillottrani and Guillermo R. Simari, in Proceedings of the 11th International Workshop on Non-Monotonic Reasoning (NMR 2006), Clausthal University of Technology, Technical Report IfI-06-04, 386 to 394 (2006)
    locator: Theorem 3 (checking an argument is P-complete), Lemma 3 (bound on building all arguments) and Corollary 1 (argument existence is in NP)
  - paper: doi:10.1016/0004-3702(94)00041-X
    title: Phan Minh Dung, On the acceptability of arguments and its fundamental role in nonmonotonic reasoning, logic programming and n-person games, Artificial Intelligence 77(2), 321 to 357 (1995)
    locator: the abstract frameworks with which DeLP is compared
---

Defeasible logic programming (DeLP) joins logic programming and argumentation. A program has strict rules, which always hold, and defeasible rules, which hold unless there is a reason against them. To answer a query, DeLP builds an argument for it from the defeasible rules, finds the arguments that defeat it, then the arguments that defeat those, and so on. The result is a dialectical tree, and the query is warranted when the root of the tree survives. Alejandro García and Guillermo Simari gave the full system in 2004, building on the argument structures of Simari and Loui (1992). An interpreter answers each query with YES, NO, UNDECIDED or UNKNOWN.

## The machine

The definitions follow García and Simari (2004). Literals are atoms $a$ or their strong negations $\sim a$. The complement of $a$ is $\sim a$ and the other way round.

**Program (Definition 2.4).** A program $\mathcal{P} = (\Pi, \Delta)$ has:

- a set $\Pi$ of facts (ground literals) and strict rules `h <- b1, ..., bn`;
- a set $\Delta$ of defeasible rules `h -< b1, ..., bn`, read as "reasons to believe $b_1, \dots, b_n$ are reasons to believe $h$".

Rules with variables stand for all their ground instances. $\Pi$ must be non-contradictory: it must not derive a literal and its complement.

**Derivation (Definitions 2.5 to 2.7).** A defeasible derivation of $h$ from $\mathcal{P}$ is a finite sequence of ground literals that ends in $h$, where each literal is a fact or the head of a rule whose body appears earlier. It is strict if it uses no defeasible rule. A set of rules is contradictory if it derives some literal and its complement.

**Argument structure (Definition 3.1).** $\langle \mathcal{A}, h \rangle$ is an argument for $h$ if $\mathcal{A} \subseteq \Delta$ and:

1. $h$ has a defeasible derivation from $\Pi \cup \mathcal{A}$;
2. $\Pi \cup \mathcal{A}$ is non-contradictory;
3. $\mathcal{A}$ is minimal with these two properties.

A sub-argument is an argument $\langle \mathcal{B}, q \rangle$ with $\mathcal{B} \subseteq \mathcal{A}$. If $h$ has a strict derivation, then $\langle \emptyset, h \rangle$ is its only argument.

**Conflict (Definitions 3.3 and 3.4).** Two literals $h$ and $h_1$ disagree if $\Pi \cup \{h, h_1\}$ is contradictory. $\langle \mathcal{A}_1, h_1 \rangle$ counter-argues $\langle \mathcal{A}_2, h_2 \rangle$ at $h$ if some sub-argument $\langle \mathcal{A}, h \rangle$ of $\langle \mathcal{A}_2, h_2 \rangle$ has a conclusion that disagrees with $h_1$.

**Comparison (Definition 3.5).** The default order is generalized specificity. Let $\Pi_G$ be the strict rules without the facts, and call a set $H$ of literals an activation set of $\langle \mathcal{A}, h \rangle$ when $\Pi_G \cup H \cup \mathcal{A}$ derives $h$ and $\Pi_G \cup H$ alone does not. Then $\langle \mathcal{A}_1, h_1 \rangle$ is strictly more specific than $\langle \mathcal{A}_2, h_2 \rangle$ if every activation set of the first activates the second, and some activation set of the second does not activate the first. In words, the more specific argument uses more information or uses it more directly. Other orders, such as priorities on rules, can replace specificity.

**Defeat (Definitions 4.1 to 4.3).** Let $\langle \mathcal{A}_1, h_1 \rangle$ counter-argue $\langle \mathcal{A}_2, h_2 \rangle$ at the sub-argument $\langle \mathcal{A}, h \rangle$. It is a proper defeater if it is strictly better than $\langle \mathcal{A}, h \rangle$, and a blocking defeater if the two are not comparable. A defeater is proper or blocking.

**Argumentation lines (Definitions 4.4 to 4.7).** A line is a sequence $[\mathcal{A}_0, \mathcal{A}_1, \mathcal{A}_2, \dots]$ in which each argument defeats the one before. The arguments at even positions support the root and those at odd positions interfere with it. A line is acceptable if:

1. it is finite;
2. the supporting arguments together with $\Pi$ are non-contradictory, and so are the interfering arguments;
3. no argument is a sub-argument of an argument that appears earlier in the line;
4. a blocking defeater is followed only by a proper defeater.

**Dialectical tree and warrant (Definitions 5.1 and 5.2, Procedure 5.1).** The tree for $\langle \mathcal{A}_0, h_0 \rangle$ has this argument at the root. The children of a node are all its defeaters that keep the line from the root acceptable. Mark the tree from the leaves:

- every leaf is U (undefeated);
- an inner node is U if all its children are D, and D (defeated) if some child is U.

The literal $h$ is warranted if some argument for $h$ has a tree with a root marked U.

**Answers (Definition 5.3).** For a query $h$ the answer is YES if $h$ is warranted, NO if the complement of $h$ is warranted, UNDECIDED if neither is, and UNKNOWN if $h$ is not in the language of the program.

## What it counts

DeLP counts arguments, defeaters and the nodes of dialectical trees. The costs come from three levels:

- **Checking an argument.** Deciding whether a given $\mathcal{A} \subseteq \Delta$ is an argument for $h$ is P-complete (Cecchi, Fillottrani and Simari 2006, Theorem 3). Derivation and the test for contradiction are both forward chaining over ground Horn rules.
- **Finding arguments.** Deciding whether some argument for $h$ exists is in NP: guess $\mathcal{A}$ and check it (Corollary 1). Building all arguments takes at most $|\mathrm{Lit}| \cdot 2^{|\Delta|}$ such checks (Lemma 3).
- **Marking the tree.** The marking is an AND-OR evaluation: a node is U only if all its children are D, so one child marked U is enough to make it D. As soon as one child is U, the parent is D and the other children need not be built. García and Simari (Section 5.1) use this pruning and compare it with [alpha-beta pruning](/alpha-beta-pruning/) of a [minimax](/minimax/) tree.

**A worked example.** This is Example 2.1 of García and Simari:

| $\Pi$ | $\Delta$ |
|---|---|
| `bird(X) <- chicken(X)` | `flies(X) -< bird(X)` |
| `bird(X) <- penguin(X)` | `~flies(X) -< chicken(X)` |
| `~flies(X) <- penguin(X)` | `flies(X) -< chicken(X), scared(X)` |
| `chicken(tina)`, `scared(tina)`, `penguin(tweety)` | `nests_in_trees(X) -< flies(X)` |

For Tina there are these arguments:

- $B_1 = \langle \{$`flies(tina) -< bird(tina)`$\}, \mathit{flies}(tina) \rangle$;
- $B_2 = \langle \{$`flies(tina) -< chicken(tina), scared(tina)`$\}, \mathit{flies}(tina) \rangle$;
- $C = \langle \{$`~flies(tina) -< chicken(tina)`$\}, \sim\mathit{flies}(tina) \rangle$;
- $N = \langle \{$`nests_in_trees(tina) -< flies(tina)`, `flies(tina) -< bird(tina)`$\}, \mathit{nests\_in\_trees}(tina) \rangle$.

Specificity orders them as follows. Every activation set of $C$ contains `chicken(tina)`, which also activates $B_1$ through the strict rule, but $\{$`bird(tina)`$\}$ activates $B_1$ and not $C$. So $C$ is strictly more specific than $B_1$. In the same way, $B_2$ needs both `chicken(tina)` and `scared(tina)`, so it is strictly more specific than $C$. Hence $C$ is a proper defeater of $B_1$ and of $N$ (at its sub-argument $B_1$), $B_2$ is a proper defeater of $C$, and nothing defeats $B_2$.

| query | dialectical tree | marking | answer |
|---|---|---|---|
| $\mathit{flies}(tina)$ | root $B_2$, no defeaters | $B_2$: U | YES |
| $\sim\mathit{flies}(tina)$ | $C$, child $B_2$ | $B_2$: U, $C$: D | NO |
| $\mathit{nests\_in\_trees}(tina)$ | $N$, child $C$, grandchild $B_2$ | $B_2$: U, $C$: D, $N$: U | YES |
| $\mathit{flies}(tweety)$ | no argument | | NO |

The line $[N, C, B_2]$ is acceptable: the supporting arguments $N$ and $B_2$ agree with $\Pi$, and $B_2$ is not a sub-argument of $N$ or $C$. For Tweety, $\sim\mathit{flies}(tweety)$ has a strict derivation, so it is warranted by $\langle \emptyset, \sim\mathit{flies}(tweety) \rangle$, and `flies(tweety) -< bird(tweety)` gives no argument because it contradicts $\Pi$. These answers match those stated in the paper.

**Blocking defeaters.** In the Nixon diamond, `pacifist(nixon) -< quaker(nixon)` and `~pacifist(nixon) -< republican(nixon)` give two arguments of equal specificity, each a blocking defeater of the other. In the tree of the first, the second is a child. The first cannot follow again, because it is a sub-argument of the root, and condition 4 also forbids a blocking defeater after a blocking defeater. So the child is a leaf marked U, the root is D, and by symmetry the answer to both queries is UNDECIDED.

## Relation to other models

- **Logic programming.** Without defeasible rules, DeLP is an extended logic program with strong negation, and a literal is warranted when it has a strict derivation (Proposition 5.1). An extended version also allows default negation, as [negation as failure](/negation-as-failure/), in the bodies of defeasible rules.
- **Abstract argumentation.** DeLP builds arguments and a defeat relation as in an [abstract framework](/abstract-argumentation-framework/), but it does not take a Dung semantics. Warrant is defined by the tree and by the conditions on acceptable lines. García and Simari note that a change in these conditions changes the behaviour of the system. So warrant need not match the [grounded extension](/grounded-extension/) of the framework of all arguments and defeats.
- **ASPIC+.** [ASPIC+](/aspic-plus/) has the same split into strict and defeasible rules. It adds undercutters and attacks on premises, it uses restricted rebut, and it evaluates the result with extension semantics.
- **ABA.** [Assumption-based argumentation](/assumption-based-argumentation/) uses only strict rules and puts the defeasibility into assumptions. Its dispute derivations are also trees of proponent and opponent moves.
- **Defeasible logic.** Nute's defeasible logic also has strict rules, defeasible rules and defeaters, but it resolves conflicts with priorities on single rules, not by comparing whole arguments.
- **Values and preferences.** Specificity is a syntactic order. [Value-based argumentation](/value-based-argumentation/) and other preference-based frameworks take the order from outside the program.

## Known results in the model

- **Strict facts are warranted (Proposition 5.1).** A literal with a strict derivation has the empty argument, which nothing can counter-argue.
- **No self-conflict.** Because of condition 2 in Definition 3.1, no argument derives a literal and its complement together with $\Pi$.
- **No defeat between equivalent arguments (Proposition 4.1).** A defeater, proper or blocking, is never equi-specific with the sub-argument it attacks.
- **Concordance.** Condition 2 on lines stops one side of a dispute from using two arguments that contradict each other. Without it, a supporting argument could be defended by an argument for the opposite claim.
- **Complexity (Cecchi, Fillottrani and Simari 2006).** Checking that a set of rules is an argument is P-complete. Deciding that some argument for a literal exists is in NP. The authors also study the data complexity of queries, with the rules fixed and the facts as input.
- **Pruning.** The answer does not change if the search stops at the first undefeated child of a node, so the warrant procedure of Section 5.1 never builds the whole tree when it can avoid it.

## References
