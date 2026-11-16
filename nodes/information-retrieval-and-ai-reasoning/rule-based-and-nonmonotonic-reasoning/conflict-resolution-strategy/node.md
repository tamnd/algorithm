---
tag: X8YCF7
kind: concept
slug: conflict-resolution-strategy
name: Conflict resolution strategy
aliases:
- rule selection strategy
- agenda ordering
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: core
summary: The rule that picks one instantiation to fire from the conflict set, by refractoriness, recency, specificity or priority.
prereqs: [production-system, forward-chaining]
see_also: [rete-algorithm, treat-algorithm, backward-chaining, priority-queue, markov-algorithm, depth-first-search, breadth-first-search]
sources:
  - paper: "Charles L. Forgy, OPS5 user's manual, technical report CMU-CS-81-135, Carnegie Mellon University (1981)"
    locator: "the description of the LEX and MEA strategies and of refraction"
  - book: isbn:9780201106473
    title: "Lee Brownston, Robert Farrell, Elaine Kant and Nancy Martin, Programming Expert Systems in OPS5, Addison-Wesley (1985)"
    locator: "the treatment of conflict resolution in OPS5 and its use to control a program"
  - paper: "John McDermott and Charles Forgy, Production system conflict resolution strategies, in D. A. Waterman and F. Hayes-Roth (eds.), Pattern-Directed Inference Systems, Academic Press, 177 to 199 (1978)"
    locator: "the criteria of refraction, recency and specificity, and their effect on the sensitivity and stability of a system"
  - title: "CLIPS Reference Manual, Volume I, Basic Programming Guide, version 6.31 (2019)"
    locator: "Section 5.3, the seven conflict resolution strategies and salience"
---

A [production system](/production-system/) finds, in each cycle, every instance of a rule whose conditions hold in the working memory. This set of instantiations is the *conflict set*. A conflict resolution strategy is the rule that picks the one instantiation that fires next. The usual criteria are *refraction* (do not fire the same instantiation twice), *recency* (prefer the instantiations that match newer facts), *specificity* (prefer rules with more conditions or tests) and *priority* (a number the programmer gives to each rule). OPS5 combined the first three in its LEX and MEA strategies, and CLIPS orders by priority and then by one of seven strategies. When the rules only add facts, the strategy changes the cost of a run but not its result; when rules remove facts or test that a fact is absent, the strategy is part of what the program means.

## In plain words

A rule engine often finds several rules that are ready to run at the same time, but it runs only one of them before it looks again. It needs a fixed way to choose. A common way is to never run the same rule on the same facts twice, to prefer the rule that uses the newest facts, and, between equal candidates, to prefer the rule that asks more of the facts. The choice can make the engine work like a person who follows the latest idea first, or like a careful queue that serves the oldest request first. If the rules only add facts, every choice leads to the same final facts. If the rules can delete facts, different choices can lead to different results.

## The idea

**The conflict set.** An instantiation is a pair of a rule and the list of working memory elements (WMEs) that match its conditions, in the order of the conditions. Each WME has a *time tag*, a counter value that it gets when it enters the memory; a *modify* action removes a WME and makes it again with a new time tag. The conflict set changes by small steps from one cycle to the next, and the [Rete](/rete-algorithm/) and [TREAT](/treat-algorithm/) algorithms keep it up to date. A strategy is a total or partial order on the conflict set; the interpreter fires a maximal element.

**The criteria.** McDermott and Forgy (1978) studied these criteria:

- **Refraction.** An instantiation fires at most once. Without it, a rule whose action does not change its own conditions fires forever. Since an instantiation is identified by its WMEs, a new time tag makes a new instantiation, so a rule can fire again on a modified WME.
- **Recency.** Prefer instantiations whose WMEs have larger time tags. This keeps the system *sensitive*: it reacts to what has just changed, and it follows one line of reasoning at a time, as in a [depth-first search](/depth-first-search/).
- **Specificity.** Prefer the instantiation of the rule with more conditions or more tests. A rule for a special case then overrides the general rule, which is a simple form of default reasoning.
- **Priority.** The programmer gives each rule a number, called *salience* in CLIPS, and the highest number wins. A strict priority on rules is the control of a [Markov algorithm](/markov-algorithm/).
- **Order.** Prefer the rule that comes first in the program text, or choose at random.

**LEX.** The LEX strategy of OPS5 applies refraction first. Then it sorts the time tags of each instantiation in decreasing order and compares the sorted lists element by element; the first larger tag wins, and if one list is a prefix of the other, the longer list wins. If the lists are equal, the rule with more tests in its conditions wins. If the tie remains, the choice is arbitrary.

**MEA.** The MEA strategy, named after means-ends analysis, applies refraction and then compares the time tag of the WME that matches the first condition of each rule; the larger one wins. Ties go to LEX. A program that puts a goal WME in the first condition of each rule thus works on its most recent goal first.

**CLIPS.** CLIPS first orders the activations by salience. Among activations of equal salience it uses one of seven strategies: *depth* (the default: new activations go above the old ones), *breadth* (new activations go below the old ones, as in a [breadth-first search](/breadth-first-search/)), *simplicity* and *complexity* (by the number of comparisons in the conditions), *lex*, *mea* and *random*. The agenda is a [priority queue](/priority-queue/) on these keys.

**When the strategy matters.** If the rules have no negated conditions and only add facts, the final memory is the least model of the rules, the same for every strategy, as the [forward chaining](/forward-chaining/) page proves. A good strategy can still reach a goal fact sooner. With *remove* actions or negated conditions this fails, and a program depends on the strategy for its result. Programmers then use the strategy as a control structure, for example with goal WMEs and MEA, or with salience levels for the phases of a task.

## Examples

**LEX and MEA disagree.** Take three instantiations, with the time tags of their WMEs in the order of the conditions:

| instantiation | tags by condition | sorted for LEX | first-condition tag for MEA |
|---|---|---|---|
| $I_1$ | 7, 3 | 7, 3 | 7 |
| $I_2$ | 5, 7, 2 | 7, 5, 2 | 5 |
| $I_3$ | 2, 8 | 8, 2 | 2 |

LEX compares the first sorted tags: $I_3$ has 8, so it fires first. Between $I_1$ and $I_2$ the first tags tie at 7, and the second tags are 3 and 5, so $I_2$ comes next. The LEX order is $I_3, I_2, I_1$. MEA compares the first-condition tags 7, 5 and 2, so its order is $I_1, I_2, I_3$, the reverse.

**Specificity.** The rule *fly* has the one condition $(\mathit{bird}\ {?x})$ and says that $x$ flies. The rule *walk* has the one condition $(\mathit{bird}\ {?x}\ \mathit{penguin})$, with a test on the kind of bird, and says that $x$ walks. For the WME $(\mathit{bird}\ \mathit{tweety}\ \mathit{penguin})$ both rules have an instantiation on the same WME, so the time tags tie, and LEX prefers *walk*, which has more tests. If *walk* then modifies the WME so that the bird is marked as handled, and *fly* tests for that mark being absent, *fly* never fires.

**The strategy changes the result.** With the memory $\{a\}$ and the rules $a \Rightarrow \mathit{make}\ b$ and $a, \neg b \Rightarrow \mathit{make}\ c$, a strategy that fires the first rule first ends with $\{a, b\}$; one that fires the second rule first ends with $\{a, b, c\}$.

**Refraction.** The rule $(\mathit{light}\ \mathit{on}) \Rightarrow \mathit{write}$ "on" fires once on a given WME. If its action were *modify* the light WME without a change in value, the WME would get a new time tag, the rule would get a new instantiation, and the system would loop.

## Where it is used

- **OPS5 and its successors.** LEX and MEA were the two strategies of OPS5, and later systems such as CLIPS kept them for compatibility; the CLIPS manual advises the default *depth* strategy for most programs.
- **Business rule engines.** Rule engines in the Rete family use salience and groups of rules to order activations.
- **Expert system design.** Specificity lets a programmer write general rules with special-case exceptions, and goal WMEs with MEA give goal-directed control inside a forward-chaining engine.
- **Planning and search.** Recency gives depth-first behaviour and a FIFO agenda gives breadth-first behaviour; a [backward chaining](/backward-chaining/) prover makes the same kind of choice when it picks the next rule for a goal.

## References
