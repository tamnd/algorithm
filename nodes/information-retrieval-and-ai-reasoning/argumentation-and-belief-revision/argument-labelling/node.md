---
tag: 1Q8F36
kind: technique
slug: argument-labelling
name: Argument labelling
aliases:
- Caminada labelling
- in-out-undec labelling
area: information-retrieval-and-ai-reasoning/argumentation-and-belief-revision
level: advanced
summary: Describes extensions as labellings that mark each argument in, out or undec under local rules. Each semantics becomes a selection among the complete labellings.
prereqs: [complete-extension]
see_also: [grounded-extension-algorithm, grounded-extension, preferred-extension, stable-extension-argumentation, semi-stable-extension, argumentation-sat-encoding, unit-propagation]
sources:
  - paper: doi:10.1007/11853886_11
    title: Martin Caminada, On the issue of reinstatement in argumentation, JELIA 2006, Lecture Notes in Computer Science 4160, 111 to 123 (2006)
    locator: the whole paper (reinstatement labellings, their link with complete extensions, and the grounded, preferred and stable cases)
  - paper: "Martin Caminada, Semi-stable semantics, in Computational Models of Argument (COMMA 2006), Frontiers in Artificial Intelligence and Applications 144, IOS Press, 121 to 130 (2006)"
    locator: the whole paper (semi-stable semantics as complete labellings with a minimal set of undec arguments)
  - paper: "Martin W. A. Caminada and Dov M. Gabbay, A logical account of formal argumentation, Studia Logica 93(2), 109 to 145 (2009)"
    locator: the whole paper (complete labellings, the maps between labellings and extensions, and the semantics as conditions on labellings)
  - paper: "Sanjay Modgil and Martin Caminada, Proof theories and algorithms for abstract argumentation frameworks, in Guillermo Simari and Iyad Rahwan (eds), Argumentation in Artificial Intelligence, Springer (2009)"
    locator: pp. 105 to 129 (labelling algorithms and argument games)
  - paper: "Yining Wu and Martin Caminada, A labelling-based justification status of arguments, Studies in Logic 3(4), 12 to 29 (2010)"
    locator: the whole paper (the justification status of an argument from its labels in all complete labellings)
  - paper: "Pietro Baroni, Martin Caminada and Massimiliano Giacomin, An introduction to argumentation semantics, The Knowledge Engineering Review 26(4), 365 to 410 (2011)"
    locator: the whole paper (extension-based and labelling-based definitions side by side)
  - book: isbn:9781848902756
    title: Wolfgang Dvořák and Paul E. Dunne, Computational problems in formal argumentation and their complexity, in Pietro Baroni, Dov Gabbay, Massimiliano Giacomin and Leendert van der Torre (eds), Handbook of Formal Argumentation, volume 1, College Publications (2018)
    locator: Section 3.6 (labelling-based semantics and their reasoning problems)
---

A labelling gives each argument of a framework one of three labels: in (accepted), out (rejected) or undec (undecided). A few local rules link the label of an argument to the labels of its attackers. The labellings that obey the rules match the complete extensions one to one, and each standard semantics becomes a simple condition on the labels: the fewest in, the most in, no undec, or the fewest undec. Martin Caminada made this the standard view in 2006. The technique turns the global definitions of Dung into rules that each argument checks against its neighbours, which is what propagation, search and SAT encodings need.

## In plain words

Write in, out or undecided next to each argument. The rules are simple. An argument is in when every argument that attacks it is out. An argument is out when at least one argument that attacks it is in. In all other cases it is undecided. A labelling that follows these rules is a consistent verdict on the whole debate.

Many verdicts can be consistent. The careful judge, who only accepts what is forced, picks the one with the fewest arguments in. A bold judge picks one with as many arguments in as possible. A judge who wants a decision on everything asks that nothing be left undecided. A judge who wants to leave as little open as possible picks one with the fewest undecided arguments. These four choices are the grounded, preferred, stable and semi-stable semantics.

## When it applies

The technique applies to any finite [abstract argumentation framework](/abstract-argumentation-framework/) $(A, R)$ and to any semantics that is defined from complete or admissible sets. It is useful when:

- the task is local by nature: propagation, incremental checks, or explaining why an argument is rejected (it is out because of an in attacker);
- the task needs the rejected arguments as well as the accepted ones, for example the range $S \cup S^+$ in [semi-stable semantics](/semi-stable-extension/);
- the task is to encode a semantics for a solver, where three values per argument give short clauses;
- the task is a dialogue or proof procedure, where one side defends in labels and the other attacks them.

It does not add expressive power: every statement about labellings can be translated back to extensions. The gain is in clarity and in the shape of the algorithms.

## The template

A labelling is a total function $L : A \to \{\mathit{in}, \mathit{out}, \mathit{undec}\}$. Write $\mathit{in}(L)$, $\mathit{out}(L)$ and $\mathit{undec}(L)$ for the three sets of arguments.

**Step 1: the local rules.** $L$ is a *complete labelling* when, for every argument $a$ (Caminada 2006; Caminada and Gabbay 2009):

- $L(a) = \mathit{in}$ if and only if every attacker of $a$ is labelled out;
- $L(a) = \mathit{out}$ if and only if some attacker of $a$ is labelled in.

Then $a$ is undec exactly when some attacker is undec and no attacker is in. An argument with no attacker must be in. A self-attacking argument cannot be in, since it would need to be out.

**Step 2: the link with extensions.** The two maps

$$\mathrm{Ext2Lab}(S) = (S,\ S^+,\ A \setminus (S \cup S^+)), \qquad \mathrm{Lab2Ext}(L) = \mathit{in}(L)$$

are inverse bijections between the [complete extensions](/complete-extension/) and the complete labellings. Under them, $\mathit{out}(L)$ is the set $S^+$ of the arguments that $S$ attacks.

**Step 3: the selection.** Among the complete labellings, pick:

| semantics | condition on the complete labelling $L$ |
|---|---|
| [grounded](/grounded-extension/) | $\mathit{in}(L)$ minimal, which is the same as $\mathit{undec}(L)$ maximal or $\mathit{out}(L)$ minimal |
| [preferred](/preferred-extension/) | $\mathit{in}(L)$ maximal, which is the same as $\mathit{out}(L)$ maximal |
| [stable](/stable-extension-argumentation/) | $\mathit{undec}(L) = \emptyset$ |
| [semi-stable](/semi-stable-extension/) | $\mathit{undec}(L)$ minimal |

All minima and maxima are under $\subseteq$. The equivalences in the first two rows hold because for complete labellings $\mathit{in}(L_1) \subseteq \mathit{in}(L_2)$ exactly when $\mathit{out}(L_1) \subseteq \mathit{out}(L_2)$.

**Step 4: the computation.** Choose how to find the selected labellings: propagate labels from the unattacked arguments (grounded), search over labels with backtracking (preferred, stable), or encode the rules as clauses for a [SAT](/sat/) solver (all of them).

## Classic examples

**A worked case.** Take $a \leftrightarrow b$, $b \to c$, the 3-cycle $c \to d \to e \to c$, and a self-attacking $g$. There are three complete labellings:

| labelling | a | b | c | d | e | g | in | undec |
|---|---|---|---|---|---|---|---|---|
| $L_1$ | undec | undec | undec | undec | undec | undec | $\emptyset$ | all six |
| $L_2$ | in | out | undec | undec | undec | undec | $\{a\}$ | $\{c, d, e, g\}$ |
| $L_3$ | out | in | out | in | out | undec | $\{b, d\}$ | $\{g\}$ |

$L_1$ is grounded, $L_2$ and $L_3$ are preferred, $L_3$ alone is semi-stable, and there is no stable labelling, because $g$ is undec in all three. Check $L_3$ by the rules: $c$ is out because $b$ is in; $d$ is in because its only attacker $c$ is out; $e$ is out because $d$ is in; $g$ is undec because its only attacker, $g$ itself, is undec.

**Grounded labelling by propagation.** Start with all arguments undec. Label in each argument whose attackers are all out, and label out each argument with an in attacker. Repeat until nothing changes. The [grounded extension algorithm](/grounded-extension-algorithm/) does this in linear time with one counter per argument. The process is the same as [unit propagation](/unit-propagation/) on the clauses of the rules.

**Labelling search for preferred and stable extensions.** Modgil and Caminada (2009) give algorithms that start from a labelling and change labels in steps that keep the local rules, with backtracking over the choices. A stable labelling is found when no undec label is left.

**Credulous acceptance under preferred semantics.** An argument is in some preferred extension exactly when it is in some admissible labelling (defined below). So a search only needs to build an admissible labelling with the argument in, which is a witness of polynomial size. This is why the problem is in NP; see [complexity of preferred semantics](/preferred-semantics-complexity/).

**SAT encodings.** With two variables for each argument, one for in and one for out, each rule of step 1 becomes a few clauses over the argument and its attackers. Stable semantics adds a clause that forbids undec. See the [argumentation SAT encoding](/argumentation-sat-encoding/).

## Variations

- **Admissible labellings.** Keep only the "only if" halves: an in argument has all its attackers out, and an out argument has an attacker that is in. Then $\mathit{in}(L)$ is an [admissible set](/admissible-set/), and each admissible set arises. The map is not one to one: in the worked case, the in set $\{b\}$ comes with out set $\{a\}$ or $\{a, c\}$.
- **Conflict-free labellings.** Ask only that no in argument has an in attacker, and that each out argument has an in attacker.
- **Stage labellings.** Among the conflict-free labellings, minimize the undec set. This gives the stage extensions.
- **Justification status.** Wu and Caminada (2010) classify an argument by the set of labels it gets across all complete labellings, which is finer than credulous and sceptical acceptance.
- **Argument games.** In a discussion game, one player claims that an argument is in and the other answers with an attacker that must then be shown out. Modgil and Caminada (2009) give such games for grounded and preferred semantics.

## Pitfalls

- **Out is not "not in".** An argument outside an extension $S$ is either out (attacked by $S$) or undec. Two-valued thinking loses the difference, which is exactly what semi-stable semantics needs.
- **One-way rules.** With only "if" or only "only if" in step 1, one gets admissible labellings or other families, not complete ones, and the bijection with complete extensions fails.
- **Out needs an in attacker.** Being attacked is not enough. An argument whose attackers are all undec is undec, not out.
- **Grounded is not "minimal undec".** Grounded minimizes in and maximizes undec. Semi-stable minimizes undec. Mixing them up gives the wrong semantics.
- **Maximal versus maximum.** The selections use $\subseteq$, not the number of labels. Two preferred labellings can have in sets of different sizes.
- **Self-attacks.** A self-attacking argument is never in. It is out when some other in argument attacks it, and else undec.

## Exercises

1. Show that in a complete labelling, every argument with no attacker is in, and deduce that the unattacked arguments are in the grounded extension.
2. Prove that Ext2Lab and Lab2Ext are inverse maps between complete extensions and complete labellings.
3. Show that for complete labellings, $\mathit{in}(L_1) \subseteq \mathit{in}(L_2)$ holds exactly when $\mathit{out}(L_1) \subseteq \mathit{out}(L_2)$. Deduce that maximal in and maximal out select the same labellings.
4. Find all complete labellings of the 4-cycle $a \to b \to c \to d \to a$, and say which are grounded, preferred, stable and semi-stable.
5. Give a framework with a labelling that is admissible but not complete, and say which rule it breaks.

## References
