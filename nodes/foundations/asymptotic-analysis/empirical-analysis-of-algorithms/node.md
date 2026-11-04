---
tag: 94SMW4
kind: concept
slug: empirical-analysis-of-algorithms
name: Empirical analysis of algorithms
aliases:
- experimental analysis of algorithms
area: foundations/asymptotic-analysis
level: core
summary: Measures running time on test inputs to check and calibrate the theoretical model.
prereqs: [time-complexity, order-of-growth, tilde-notation]
see_also: [doubling-hypothesis, asymptotic-notation, worst-case-analysis, average-case-analysis, input-size, comparison-model]
sources:
  - url: "https://algs4.cs.princeton.edu/14analysis/"
    locator: Section 1.4, Analysis of Algorithms (booksite)
  - book: isbn:9780521173018
    title: Catherine C. McGeoch, A Guide to Experimental Algorithmics
    locator: Chapter 2 (A plan of attack)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.4, Analysis of Algorithms (observations and the power-law hypothesis)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.1, Elementary Sorts (comparing algorithms by experiment)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.2, Analyzing algorithms (the RAM model of analysis)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.1.1, Inversions
---

Empirical analysis of algorithms is the study of a program by running it on test inputs and measuring its cost, as a time or as a count of operations. It checks a theoretical model of the [time complexity](/time-complexity/) against a real machine, it estimates the constants that the [order of growth](/order-of-growth/) leaves out, and it compares programs of the same order. It can refute a claim about the running time. It cannot prove an asymptotic bound.

## In plain words

A proof about an algorithm says what happens for every input and for every size. An experiment says what happened on the inputs you tried, on one machine, on one day. The two help each other. The proof tells you what to expect, and the experiment tells you whether the program you wrote follows it, how large the hidden constants are, and which of two programs wins at the sizes you care about.

To run a good experiment, you decide what you want to learn first. You choose a cost to measure and the inputs to feed the program. You run each size many times, because the results vary. You skip the first runs, because the machine is still warming up. You look at the whole table of results, and not at one number. Then you say what the experiment showed, and what it did not.

## The idea

**The question.** An experiment answers one question: does the cost follow the formula $\sim a\,n^b$ (see [tilde notation](/tilde-notation/)), what is the constant, which program is faster at a size, where do two programs cross, or where is the time spent. Fix the question before the run.

**The cost measure.** There are two choices.

- *Operation counts.* Count compares, array accesses, swaps, or calls. A count does not depend on the machine, the language or the load, and it can be exact. It matches the cost model of the analysis (for sorting, the [comparison model](/comparison-model/)), so it checks the formula directly. Its weakness is that an operation that is not counted, such as a cache miss, is hidden.
- *Time.* Seconds on a real machine are what a user sees. Time includes the memory hierarchy, the compiler and the runtime. Its weakness is noise, and the dependence on the machine.

Use a count to test the model and a time to test the program. Often both are recorded in the same run.

**The inputs.** The input generator is part of the experiment. State the family and the size $n$ ([input size](/input-size/) in the sense of the analysis). Use families that match the cases of the analysis: random inputs for the average case, a sorted or reversed array, an array with many equal keys, and the worst case when you know one. A [worst case](/worst-case-analysis/) is rarely met by a random generator. Build the input outside the timed region. Fix the seed of the random generator and record it, so that the run can be repeated. Choose the sizes as a geometric series, for example $n_0, 2n_0, 4n_0, \ldots$, so that a log-log plot has evenly spaced points and so that the [doubling hypothesis](/doubling-hypothesis/) applies.

**Repetition and noise.** The cost varies from run to run, for two reasons. First, the input is random: the number of inversions of a random permutation of $n$ items has mean $n(n-1)/4$ and variance $n(n-1)(2n+5)/72$ (Knuth, Volume 3, Section 5.1.1), so for $n = 1000$ the mean is $249\,750$ and the standard deviation is $5\,274$, which is $2.1$ percent of the mean. Second, the machine is noisy. Run many trials for each size. For random inputs, report the mean and its standard error, which is the standard deviation divided by the square root of the number of trials: for $n = 1000$ and $100$ trials it is $527$ inversions. For timings, report the median or the minimum, which are less sensitive to a slow outlier, and the spread. In a managed runtime, a garbage-collection pause can fall inside one timed run. Run enough trials that such a run shows as an outlier. Compare two programs by the ratio of their times on the same inputs.

**Warm-up and the timer.** The first runs of a program can be slower: caches are cold, files are loaded, and a managed runtime compiles code while it runs. Run the work a few times and discard these runs. Use a monotonic clock, and make each timed run last much longer than the resolution of the clock: loop the operation inside the timer and divide by the count. Use the result of the computation, so that an optimizing compiler cannot remove the work. Keep other loads on the machine low, and fix the settings (compiler flags, clock frequency) for the whole experiment.

**Analysis of the data.** Look at the table first. Then use these tools.

- The ratio $T(2n)/T(n)$ and its logarithm, see the [doubling hypothesis](/doubling-hypothesis/).
- A log-log plot of $T$ against $n$: a power law $a n^b$ is a line of slope $b$.
- A plot of $T(n)/f(n)$ against $n$ for a guess $f$: if the guess is right, the points settle at a constant, which estimates the leading constant $a$. If the plot rises or falls without end, the guess is wrong.
- A comparison with the exact formula, when one is known.

**What an experiment can show.** It can refute a hypothesis: a program whose time grows by a factor of about eight at each doubling, over a series of sizes, is not quadratic. It can estimate $a$ and $b$ in the range of sizes tested, and use them to predict a nearby larger size. It can show which of two programs is faster in that range, and where they cross. It can find a part of the program that dominates the time.

**What it cannot show.** It cannot prove that a bound holds for all $n$, because the sizes are finite and a change in behavior can lie beyond the range. It does not show a worst case unless the input is a worst case. It cannot tell $n\lg n$ from $n^{1.07}$ by a short series near $n = 10^6$, where the local exponent of $n\lg n$ is $1 + 1/\ln n \approx 1.07$ (see the pitfalls of the doubling hypothesis). It gives a result for one machine, one compiler and one implementation, and the result may not carry over. It does not replace a proof, and a proof does not replace it: an asymptotic bound says nothing about the constants or the memory behavior of the program that you run.

## Examples

**Checking a formula with a count.** [Randomized quicksort](/randomized-quicksort/) makes $2(n+1)H_n - 4n$ compares on average, when the partition of $m$ keys uses $m-1$ compares, where $H_n$ is the [harmonic number](/harmonic-series/). For $n = 1000$ the value is $10\,985.9$. The leading term alone, $2n\ln n$, is $13\,815.5$, which is $26$ percent too large. A fit of $a\,n\ln n$ on small sizes would estimate a leading constant that is too small, because the term $-4n$ and the other lower terms are still large. This is why one plots $T(n)/f(n)$ for several sizes, and does not rely on one.

**Two programs that cross.** Let program A cost exactly $n^2$ steps and program B cost exactly $100\,n\lg n$ steps. Then A is cheaper for $2 \le n \le 996$, and B is cheaper for each $n \ge 997$. At $n = 1000$ the costs are almost equal ($10^6$ and $996\,578$), at $n = 2000$ the ratio $A/B$ is $1.82$, at $n = 10^4$ it is $7.5$, and at $n = 10^6$ it is $502$. An experiment on sizes up to $500$ would measure the ratio $0.56$ and conclude that A is the better program, and it would be correct for those sizes. It would also be wrong about the order of growth. The crossing point is a fact about the constants, and only an experiment finds it for a real machine.

**Counting versus timing.** [Insertion sort](/insertion-sort/) on a random array does about $n^2/4$ exchanges. This count is the same on every machine. The time of the same program depends on the processor, on the language and on whether the array fits in cache. A report gives both: the count to confirm the $n^2/4$, and the time for the machine at hand.

## Where it is used

- **Validating an analysis.** Sedgewick and Wayne use experiments in Section 1.4 to state a hypothesis for the running time, and in Chapter 2 to compare the sorts on random inputs.
- **Choosing between algorithms of the same order.** Two sorts with the same $\Theta(n \log n)$ time differ by a constant factor, which only a measurement gives for a given machine.
- **Tuning.** The size at which a hybrid algorithm switches from one method to another, for example from a recursive sort to an elementary sort on a small part, is found by experiment.
- **Prediction.** After the exponent and the constant are estimated, the running time on a larger input is predicted. This avoids a run that would take days.
- **Finding bugs in an analysis.** A measured exponent that is higher than the proved one points to a hidden cost, such as a copy of an array in each call.

## References
