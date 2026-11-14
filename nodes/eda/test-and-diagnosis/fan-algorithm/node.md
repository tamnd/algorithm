---
tag: DJVVW8
kind: algorithm
slug: fan-algorithm
name: FAN
aliases:
- fanout-oriented test generation
- Fujiwara-Shimono algorithm
area: eda/test-and-diagnosis
level: core
summary: Fujiwara and Shimono's ATPG that improves PODEM with headlines, backtrace to many objectives at once and unique sensitization, cutting the search a lot.
solves: [automatic-test-pattern-generation]
model: word-ram
complexity:
  vars: {n: the number of primary inputs, h: "the number of head lines, at most n", L: the number of lines, P: the number of gate input pins}
  time: {worst: "O(L (L + P) + 2^h (L + P))", best: "O(L (L + P))"}
  space: {extra: O(L + n)}
properties: {deterministic: true, exact: true, complete: true, recursive: false}
history:
  year: 1983
  people: [Hideo Fujiwara, Takeshi Shimono]
  note: Fujiwara and Shimono published FAN in 1983 as a faster PODEM. SOCRATES (1988) added learning to FAN, and FAN-style rules stayed in structural test generators.
prereqs: [podem, automatic-test-pattern-generation]
see_also: [d-algorithm, sat-based-atpg, static-learning, recursive-learning, scoap, redundant-fault, dominator-tree, dynamic-test-compaction]
sources:
  - paper: doi:10.1109/TC.1983.1676174
    title: H. Fujiwara and T. Shimono, On the acceleration of test generation algorithms, IEEE Transactions on Computers C-32(12), 1137 to 1144, 1983
    locator: head lines, multiple backtrace, unique sensitization, immediate implications, and the comparison with PODEM
  - paper: "Prabhakar Goel, An implicit enumeration algorithm to generate tests for combinational logic circuits, IEEE Transactions on Computers C-30(3), 215 to 222, 1981"
    title: P. Goel, An implicit enumeration algorithm to generate tests for combinational logic circuits, IEEE Transactions on Computers C-30(3), 215 to 222, March 1981
    locator: PODEM, the search that FAN keeps
  - paper: "M. H. Schulz, E. Trischler and T. M. Sarfert, SOCRATES: a highly efficient automatic test pattern generation system, IEEE Transactions on Computer-Aided Design 7(1), 126 to 137, 1988"
    title: M. H. Schulz, E. Trischler and T. M. Sarfert, SOCRATES, a highly efficient automatic test pattern generation system, IEEE Transactions on Computer-Aided Design 7(1), 126 to 137, 1988
    locator: the FAN-based system with improved implication, unique sensitization and multiple backtrace
  - book: isbn:9780792379911
    title: Michael L. Bushnell and Vishwani D. Agrawal, Essentials of Electronic Testing for Digital, Memory and Mixed-Signal VLSI Circuits, Kluwer, 2000
    locator: the chapter Combinational Circuit Test Generation (FAN)
  - book: isbn:9780780310629
    title: Miron Abramovici, Melvin A. Breuer and Arthur D. Friedman, Digital Systems Testing and Testable Design, IEEE Press, 1994
    locator: the chapter on test generation for combinational circuits (FAN)
---

FAN is an algorithm for [automatic test pattern generation](/automatic-test-pattern-generation/) by Fujiwara and Shimono (1983). Like [PODEM](/podem/), it takes a combinational circuit and one [single stuck-at fault](/stuck-at-fault-model/), and it finds an input vector that detects the fault or proves that none exists. It keeps the PODEM search, a depth-first search over decisions with forward simulation, and makes the search tree smaller and the dead ends easier to see. It decides on head lines, which are the roots of the fanout-free parts of the circuit, instead of on primary inputs. It sends all current goals back at once with counts. And it fixes the values that every path of the fault effect needs before it decides anything else.

## In plain words

PODEM sets one circuit input at a time, and it often finds out late that an early choice was wrong. FAN uses three ideas to waste less work.

First, a group of inputs that feeds a tree of gates with no shared signals can give the root of the tree any value, so FAN decides on the root. It works out the inputs only at the end, without any search.

Second, FAN collects all its current goals and walks back from all of them together. Where two goals pull a signal in different directions, it counts the votes and takes the majority.

Third, when the error can only travel through some gates, FAN sets their other inputs to the values that let it through, at once. A wrong earlier choice then shows up immediately.

## The problem

The input is a combinational circuit $C$ with $n$ primary inputs and $L$ lines in topological order, and a fault $(\ell, s)$, line $\ell$ stuck at $s$. The lines are the stems of the primary inputs and gates and the fanout branches, as on the [PODEM](/podem/) page. The output is a vector over $\{0, 1, X\}$ whose every two-valued completion detects the fault, or "untestable" when no vector detects it.

FAN uses Roth's values 0, 1, D, D' and X, the D-frontier and the X-path of the PODEM page. Two new words describe the structure of the circuit.

- A line is **bound** when it is a fanout branch or is reached from a fanout branch. A line that is not bound is **free**. On this page, the fault site and every line that it reaches are also bound, so a free line never carries the fault effect.
- A **head line** is a free line with a bound fanout. The free lines from which a head line $h$ is reached form a tree with $h$ as root and primary inputs as leaves, and the trees of two head lines share no line. When the fault site is a primary input, it is a decision line too, and the page counts it among the head lines $H$.

## The algorithm

```pseudo id=main
FAN(C, (ℓ, s))
L1  mark the bound lines; H ← the head lines
L2  set every line of H to X; stack ← empty
L3  loop
L4      simulate the good and the faulty circuit with three values from the values on H
L5      if some primary output has D or D' then return JUSTIFY()
L6      R ← UNIQUE-SENSITIZATION()
L7      if ℓ is not at s and (ℓ has X or a D-frontier gate has an X-path) and no (j, v) in R has j at ¬v then
L8          O ← {(ℓ, ¬s)} if ℓ has X, plus each (j, v) in R with j at X
L9          if O is empty then O ← {(j, the non-controlling value of G)} for an X input j of a D-frontier gate G with an X-path
L10         (h, u) ← MULTIPLE-BACKTRACE(O)
L11         set h to u; push (h, u, not flipped)
L12     else
L13         pop each entry that is flipped and set its line to X
L14         if the stack is empty then return "untestable"
L15         flip the value of the top entry, set its line to it, and mark it flipped

UNIQUE-SENSITIZATION()
L16 if ℓ has X or more than one D-frontier gate has an X-path then return ∅
L17 R ← ∅; G ← the D-frontier gate with an X-path
L18 for each gate d with a controlling value c that lies on every path from G to a primary output, G included do
L19     for each input j of d outside the fanout cone of ℓ do add (j, ¬c) to R
L20 return R

MULTIPLE-BACKTRACE(O)
L21 n0(k) ← 0 and n1(k) ← 0 for each line k; for each (k, v) in O add 1 to n_v(k)
L22 for each line k not in H with n0(k) + n1(k) > 0, in reverse topological order do
L23     if k is a fanout stem with n0(k) > 0 and n1(k) > 0 then set the smaller count to 0 (n1 on a tie)
L24     for each value v with n_v(k) > 0 do
L25         u ← v xor inversion(k)
L26         if u is the controlling value of k then add n_v(k) to n_u(j) for the first input j of k with X
L27         else add n_v(k) to n_u(j) for every input j of k with X
L28 return (h, v): the line h of H with the largest n0(h) + n1(h), and v the value with the larger count (0 on a tie)

JUSTIFY()
L29 for each line h of H with a value u, set the inputs of the tree of h by one backtrace so that h gets u
L30 return the primary input values, with X for the inputs that are not set
```

Here inversion(k) is 1 for NAND, NOR, NOT and XNOR. For XOR and XNOR, line L26 is used with $u$ corrected by the parity of the known inputs. In line L29, a gate whose inputs need the controlling value gets it on one input, and otherwise every input of the tree gets a value. Line L1 takes $O(L + P)$ time, where $P$ is the number of gate input pins. Line L18 needs the gates through which every path from $G$ to an output passes. These are the post-dominators of $G$, and the code builds their [dominator tree](/dominator-tree/) once, before the loop.

The decisions and the order of the passes are those of PODEM. What changes is the place of the decisions (line L11 sets a head line, not an input), the goals (line L8 can hold many), and the test of line L7, which also fails when a required value of $R$ is contradicted. In the original, a fanout stem that gets both counts at line L23 stops the backtrace and becomes a decision of its own, which is justified later. This page keeps the larger count and goes on, so every decision is on a head line. Both forms are complete.

## Example

**Head lines.** The circuit is the consensus circuit of the PODEM page with $b$ and $c$ widened into small trees: $b = b_1 b_2$, $c = c_1 + c_2$, $na = \lnot a$, $p = ab$, $q = \overline{a}c$, $r = bc$ and $z = p + q + r$. The stems $a$, $b$ and $c$ fan out, so their branches and everything after them are bound. The head lines are $a$, $b$ and $c$, three decision lines for five inputs. The fault $r$ stuck at 0 is redundant, because $bc$ is the consensus of $ab$ and $\overline{a}c$. Each pass takes the first candidate on a tie.

| pass | $a\,b\,c$ | values | action |
|---|---|---|---|
| 1 | X X X | all X | objective $(r, 1)$: the AND $r$ gives a 1-count to $b$ and to $c$; set $b = 1$ |
| 2 | X 1 X | $r$ = X | objective $(r, 1)$; set $c = 1$ |
| 3 | X 1 1 | $r = D$, D-frontier $\{z\}$ | the D-frontier gate is the output $z$ itself, so $R = \{(p, 0), (q, 0)\}$. $p = 0$ gives $a$ a 0-count and $q = 0$ gives $a$ a 1-count through $na$; tie, set $a = 0$ |
| 4 | 0 1 1 | $q = 1$, $z = 1$ | $(q, 0)$ fails and the D-frontier is empty: flip $a$ to 1 |
| 5 | 1 1 1 | $p = 1$, $z = 1$ | $(p, 0)$ fails: pop $a$, flip $c$ to 0 |
| 6 | X 1 0 | $r = 0$ | $r$ is at its stuck value: pop $c$, flip $b$ to 0 |
| 7 | X 0 X | $r = 0$ | the stack is empty: return "untestable" |

FAN proves the fault redundant in 7 passes and 3 flips. PODEM, with the same first-candidate choices, decides on the five inputs. It sets $b_1$, $b_2$, $c_1$ and $a$, then tries both values of $a$ again after it flips $c_1$ and sets $c_2$, and it needs 13 passes and 6 flips. Its tree enumerates the ways to make $b = 1$ and $c = 1$, which FAN never looks at.

**Unique sensitization and multiple backtrace.** The second circuit is $s = e + k$, $g = x s$, $w_1 = \overline{e + f}$, $u = g w_1$, $w_2 = \overline{e + h}$ and $z = u w_2$, with inputs in the order $x, e, k, f, h$. The fault is $x$ stuck at 0, and $x$ is a decision line because it is the fault site.

| pass | $x\,e\,k\,f\,h$ | values | action |
|---|---|---|---|
| 1 | X X X X X | all X | objective $(x, 1)$; set $x = 1$ |
| 2 | 1 X X X X | $x = D$, D-frontier $\{g\}$ | every path from $g$ passes $g$, $u$ and $z$: $R = \{(s, 1), (w_1, 1), (w_2, 1)\}$. Counts: $e$ gets one 1-count from $s$ and two 0-counts from $w_1$ and $w_2$; set $e = 0$ |
| 3 | 1 0 X X X | $s$ = X | objectives $(s,1), (w_1,1), (w_2,1)$; set $k = 1$ |
| 4 | 1 0 1 X X | $g = D$ | set $f = 0$ |
| 5 | 1 0 1 0 X | $u = D$ | set $h = 0$ |
| 6 | 1 0 1 0 0 | $z = D$ | return 10100 |

FAN makes no flip. PODEM first takes the one objective "the X input $s$ of $g$ to 1", backtraces through the OR to $e = 1$, and only then sees that $w_1 = 0$ blocks the path. It needs 7 passes and 1 flip to reach the same vector. Over all 28 faults of this circuit, PODEM makes 13 flips and FAN 9. Over all 36 faults of the first circuit, PODEM makes 24 and FAN 13.

## Correctness

FAN returns a test exactly when the fault is detectable. The new part of the proof is that the head lines cut the circuit. Every input of a bound line is bound or a head line, so the good and the faulty values of every bound line depend only on the values of the head lines. Each head line is the root of a tree with its own primary inputs, so any values on the head lines can be justified at the end without a conflict. The values in $R$ are necessary: every detecting path leaves the single D-frontier gate $G$ and passes every gate $d$ of line L18, and a side input of $d$ outside the fanout cone of $\ell$ has the same value in both circuits, so it must not be controlling. Hence the test of line L7 fails only at nodes below which no test exists. As in PODEM, each pass assigns a new head line, the tree has depth at most $|H| \le n$, and the branch that agrees with a test is never pruned. The [full proof](proofs/correctness.md) gives the details.

## Complexity

Line L1 and the dominator tree are built once, in $O(L (L + P))$ time by the simple meet-walk used here, and in almost linear time with the Lengauer and Tarjan method. Each pass then costs $O(L + P)$ for the simulation, the D-frontier, the X-paths, the list $R$ and the backtrace. The tree has at most $2^{h+1} - 1$ nodes for $h = |H|$ head lines, so the worst case is $O(L (L + P) + 2^h (L + P))$ time. Since $h \le n$, this bound is never above the bound of PODEM apart from the preprocessing, and it is much lower when the circuit has large fanout-free regions. The extra space is $O(L + n)$ for the values, the counts and the stack.

The bound is exponential, and must be, since the decision problem is NP-complete. That FAN needs fewer passes than PODEM on real circuits is a measured result. Fujiwara and Shimono report it on their test circuits, and later tools such as SOCRATES build on it. On small random circuits the gain is not uniform. In a run over 2000 random circuits with 3 to 6 inputs and 4 to 8 gates of the types AND, OR, NAND, NOR and NOT (86 888 faults), the code of this page made 36 359 flips on the 18 779 redundant faults where PODEM made 38 470, but 3 731 flips on the 68 109 detectable faults where PODEM made 3 606. FAN made fewer flips on 2 521 faults and more on 1 115.

## Properties

- **Complete.** FAN returns a test exactly when one exists, so "untestable" proves that the fault is [redundant](/redundant-fault/).
- **Smaller tree.** The depth of the search is the number of head lines, at most the number of inputs. The inputs inside the tree of a head line are set once, at line L29, without search.
- **Same test quality.** The returned vector leaves free all inputs that no justification needed, like PODEM, which helps [dynamic test compaction](/dynamic-test-compaction/).
- **Free choices.** Any rule for ties at lines L23, L26 and L28 keeps the result correct. Testability measures such as [SCOAP](/scoap/) are the usual guide.
- **Heuristic gain.** Head lines and the pruning by $R$ never make the bound on the tree larger, but multiple backtrace can pick a different decision than PODEM, so on a single fault FAN can make more flips.

## Variants and improvements

- **Fanout stems as decisions.** In the paper, when the counts at a fanout stem conflict, the stem becomes the final objective, gets the majority value, and is justified later like a line of the D-algorithm. This avoids walking through the stem with a value that half of the goals did not want.
- **Immediate implications.** The paper also implies values backward. For example, an AND output that must be 1 sets all its inputs to 1 at once. Simulation only goes forward and finds the same conflicts later.
- **Learning.** SOCRATES (Schulz, Trischler and Sarfert, 1988) adds [static learning](/static-learning/), which stores indirect implications found before the search, and an improved unique sensitization. [Recursive learning](/recursive-learning/) by Kunz and Pradhan finds all necessary values with enough depth.
- **Dominator-based sensitization.** Later systems compute the dominator tree of the circuit once and use it for each fault, as this page does.
- **SAT.** [SAT-based ATPG](/sat-based-atpg/) gives the same problem to a CDCL solver. Its clause learning finds many of the implications that FAN finds with its rules.

## When to use it

Use FAN, or a descendant, for test generation on combinational logic or the combinational part of a full [scan design](/scan-design/), together with a [fault simulator](/fault-simulation/) that drops the faults each new test also detects. Its rules pay most on circuits with large fanout-free regions and on redundant faults, where the whole tree must be searched. For the hardest faults, tools often switch to SAT-based ATPG after a backtrack limit.

## Pitfalls

- **The fault inside a fanout-free region.** If the fault site lies in the tree of a head line, a decision on the head line also fixes the faulty value. Treat the fault site and its fanout cone as bound, as on this page, or give the head line a value pair.
- **Unique sensitization through reconvergence.** A side input that the fault reaches by another path can carry the fault effect, and then it need not be non-controlling. Only side inputs outside the fanout cone of the fault site may go into $R$.
- **Dominators of the wrong gate.** Line L18 needs the gates on every path from the D-frontier gate to any output, not to one output. With two D-frontier gates, nothing is required, since the effect can take either.
- **Stopping at a head line that is not free.** A line with a bound fanout and a bound input is bound, not a head line. Its value cannot be justified without search.
- **Aborted is not redundant.** With a backtrack limit, FAN reports some faults as aborted. Only a full search proves redundancy.

## Implementations

## History

Goel's PODEM of 1981 made decisions only on the primary inputs. Hideo Fujiwara and Takeshi Shimono published FAN in 1983, and the name stands for a fanout-oriented method. They kept the search of PODEM and added head lines, multiple backtrace, unique sensitization and immediate implications, and they reported shorter run times than PODEM on their test circuits. Schulz, Trischler and Sarfert built SOCRATES on FAN in 1988 and added learning. From about 1990, SAT-based engines took over the hardest faults, but the FAN rules stayed in structural test generators.

## References
