---
tag: 3S3FFB
kind: problem
slug: monty-hall-problem
name: Monty Hall problem
area: foundations/probabilistic-analysis
level: intro
summary: A probability puzzle about whether to switch doors after the host reveals a goat, whose answer is that switching wins two thirds of the time.
prereqs: [conditional-probability, bayes-theorem, probability-space]
see_also: [birthday-paradox, randomized-algorithm, independent-events, conditional-expectation]
sources:
  - paper: "Steve Selvin, A problem in probability (letter to the editor), The American Statistician 29(1), 1975"
    locator: p. 67, the first statement of the problem with three boxes and the answer two thirds
  - paper: "Steve Selvin, On the Monty Hall problem (letter to the editor), The American Statistician 29(3), 1975"
    locator: p. 134, the name Monty Hall problem and a solution by conditional probability
  - book: isbn:9780195367898
    title: Jason Rosenhouse, The Monty Hall Problem, Oxford University Press, 2009
    locator: the whole book, on the history of the problem, the role of the host's rule, and the variants with more doors and other hosts
  - paper: "Leonard Gillman, The car and the goats, The American Mathematical Monthly 99(1), 1992"
    locator: pp. 3 to 7, the solution by Bayes' theorem and the version with a host who prefers one door
---

The Monty Hall problem is a game with three doors: a car is behind one and goats are behind the other two. The player picks a door, the host, who knows where the car is, opens another door that shows a goat, and the player may then switch to the last closed door. Switching wins with probability $2/3$ and staying wins with probability $1/3$. The answer depends on the exact rule of the host, and it is a standard exercise in [conditional probability](/conditional-probability/) and [Bayes' theorem](/bayes-theorem/).

## In plain words

There are three doors. A car is behind one of them and a goat is behind each of the others. You point at a door. The host knows where the car is. He opens one of the other two doors, and it always shows a goat. Then he asks if you want to change your door.

Many people think it does not matter. But your first door was right only one time in three, and the host cannot change that. In the other two cases out of three, the car is behind one of the two doors you did not pick, and the host has shown you which one it is not. So if you change, you win two times in three.

## Definition

**The game.** Doors $1, 2, 3$. The car is behind a door $C$, uniform on the three doors. The player picks a door $P$. The host opens a door $H$ under these rules:

1. $H \ne P$: the host never opens the player's door.
2. $H \ne C$: the host knows where the car is and always shows a goat.
3. If two doors satisfy rules 1 and 2, which happens when $P = C$, the host picks one of them uniformly at random.

The player then stays with $P$ or switches to the third door.

**The question.** Find the probability of winning the car by staying and by switching, given everything the player has seen, and find the best strategy.

**Formal model.** By symmetry take $P = 1$. The [probability space](/probability-space/) has four outcomes with probabilities: $(C, H) = (1, 2)$ and $(1, 3)$ with $1/6$ each, and $(2, 3)$ and $(3, 2)$ with $1/3$ each.

**Origin.** Selvin stated the problem with three boxes in a letter to The American Statistician in 1975, and gave it the name of Monty Hall, the host of the television show Let's Make a Deal, in a second letter the same year. Rosenhouse's book tells the later history of the problem and its many variants.

## Variants

- **$n$ doors, the host opens $n - 2$.** The host opens all other doors but one, each with a goat. Staying wins with probability $1/n$ and switching with $(n-1)/n$.
- **$n$ doors, the host opens one.** The host opens one goat door, and the player may switch to one of the $n - 2$ other closed doors at random. Switching wins with probability $\frac{n-1}{n}\cdot\frac{1}{n-2} = \frac{n-1}{n(n-2)}$, which is more than $1/n$, so switching still helps a little.
- **The ignorant host.** The host opens one of the other two doors at random, and it happens to show a goat. Then staying and switching both win with probability $1/2$. The fact that a goat appeared is the same, but the rule that produced it is different.
- **A host with a preference.** When $P = C$, the host opens door $h$ with probability $q$ and the other goat door with probability $1 - q$. If the player sees door $h$ opened, switching wins with probability $1/(1 + q)$, which is between $1/2$ and $1$. So switching is never worse, and it is strictly better unless $q = 1$.
- **A host who offers a switch only when the player is right.** If the host may choose whether to open a door, and opens one only when $P = C$, then switching always loses. The rules of the host decide the answer.

## Examples

**Exact values and a simulation.** The simulation plays each game 300000 times (seed 19). For the ignorant host, only the games where a goat was shown are counted.

| game | stay wins (exact) | switch wins (exact) | stay (simulated) | switch (simulated) |
| --- | --- | --- | --- | --- |
| 3 doors, standard host | $1/3$ | $2/3$ | 0.3338 | 0.6662 |
| 10 doors, host opens 8 | $1/10$ | $9/10$ | 0.1006 | 0.8994 |
| 10 doors, host opens 1 | $1/10$ | $9/80 = 0.1125$ | 0.1002 | 0.1134 |
| 3 doors, ignorant host | $1/2$ | $1/2$ | 0.5006 | 0.4994 |
| 3 doors, preference $q = 0.7$ | $0.4118$ | $1/1.7 = 0.5882$ | 0.4104 | 0.5896 |

**The 100-door view.** With 100 doors, the player picks one, and the host opens 98 goat doors and leaves one other door closed. The first pick is right with probability $1/100$. The other closed door holds the car in all other cases, with probability $99/100$.

## Known algorithms

- **Always switch.** Wins with probability $2/3$ in the standard game, and this is optimal (see Bounds).
- **Randomized first pick, then switch.** If the car is placed by an adversary but the host follows rules 1 to 3, a uniformly random first pick followed by a switch wins with probability $2/3$ whatever the placement. This is the same idea as a [randomized algorithm](/randomized-algorithm/) that removes the dependence on the input distribution.
- **Computing the answer for any host rule.** List the outcomes $(C, H)$ with their probabilities, keep those that match what the player saw, and compare the totals for each closed door. This is [Bayes' theorem](/bayes-theorem/) on a finite space.

## Bounds

**Theorem.** In the standard game with $P = 1$ and $H = 3$, $\Pr[C = 1 \mid H = 3] = 1/3$ and $\Pr[C = 2 \mid H = 3] = 2/3$. The same holds for each $P$ and each $H$ that the rules allow.

*Proof.* From the rules, $\Pr[H = 3 \mid C = 1] = 1/2$ (rule 3), $\Pr[H = 3 \mid C = 2] = 1$ (doors 1 and 2 are not allowed), and $\Pr[H = 3 \mid C = 3] = 0$ (rule 2). With the prior $\Pr[C = c] = 1/3$,
$$ \Pr[H = 3] = \tfrac13\cdot\tfrac12 + \tfrac13\cdot 1 + \tfrac13\cdot 0 = \tfrac12, $$
so by Bayes' theorem
$$ \Pr[C = 1 \mid H = 3] = \frac{\frac13\cdot\frac12}{\frac12} = \frac13, \qquad \Pr[C = 2 \mid H = 3] = \frac{\frac13\cdot 1}{\frac12} = \frac23. $$
The other cases follow by renaming the doors. $\square$

**Switching is optimal.** A strategy chooses, for each observed $(P, H)$, to stay or switch. For each observation, switching wins with conditional probability $2/3$ and staying with $1/3$, so always switching maximizes the probability of a win, and the maximum is $2/3$. No strategy, randomized or not, does better.

**A shorter argument for the unconditional value.** The switching player wins if and only if the first pick was wrong, because the host removes the only other goat. The first pick is wrong with probability $2/3$. This gives the overall probability $2/3$ but not the conditional one for a given $H$; the conditional statement needs rule 3, as the host with a preference shows.

**The general formula.** For the host with a preference $q$, when the player sees door $h$ opened, $\Pr[H = h] = \frac13 q + \frac13$, so $\Pr[\text{switch wins} \mid H = h] = \frac{1/3}{(q + 1)/3} = \frac{1}{1 + q}$. For $n$ doors with one door opened, the car is behind one of the $n - 2$ other closed doors with probability $(n-1)/n$, and by symmetry each of them has the car with probability $\frac{n-1}{n(n-2)}$.

## Reductions

- **Bayes' theorem on a finite space.** Each version of the problem is a computation of a posterior from a prior and a likelihood, the likelihood being the rule of the host.
- **Three prisoners problem and Bertrand's box.** Both are older puzzles with the same structure: a choice among three, a piece of information given by a person who knows the truth, and a posterior of $1/3$ against $2/3$.

## Applications

- **Teaching conditional probability.** The problem shows that a conditional probability depends on how the information was produced, not only on what was seen. The ignorant host and the host with a preference make this exact.
- **Testing intuition with simulation.** A short program that plays the game many times settles the question for most people, which makes it a standard first exercise in Monte Carlo simulation.
- **Selection effects in data.** The same error, ignoring the rule that selected the data, appears when one conditions on a filtered sample.

## References
