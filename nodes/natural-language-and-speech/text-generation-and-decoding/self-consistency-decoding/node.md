---
tag: 417M7S
kind: technique
slug: self-consistency-decoding
name: Self-consistency
aliases:
- self-consistency decoding
- majority voting over reasoning paths
area: natural-language-and-speech/text-generation-and-decoding
level: research
summary: Sample many chain-of-thought answers and return the final answer that occurs most often among them.
prereqs: [chain-of-thought-prompting, temperature-sampling, plurality-voting]
see_also: [chain-of-thought-prompting, minimum-bayes-risk-decoding, plurality-voting, temperature-sampling, top-k-sampling, greedy-decoding, in-context-learning, law-of-large-numbers]
sources:
  - url: https://arxiv.org/abs/2203.11171
    title: "Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang, Aakanksha Chowdhery and Denny Zhou, Self-consistency improves chain of thought reasoning in language models, ICLR 2023"
    locator: "Section 2 (the method: sample reasoning paths, marginalize them out by a vote over the final answers), the comparison of the plain vote with votes weighted by the probability of each path, Section 3 (the gains over chain-of-thought prompting with greedy decoding on GSM8K, SVAMP, AQuA, StrategyQA and ARC-challenge), and the study of the number of sampled paths"
---

Self-consistency is a decoding method for questions with a short final answer, such as arithmetic word problems, that a [language model](/language-model/) answers by writing out its reasoning first ([chain-of-thought prompting](/chain-of-thought-prompting/)). In place of one greedy answer, it samples many reasoning paths from the model, for example with [temperature sampling](/temperature-sampling/) and [top-k sampling](/top-k-sampling/), reads the final answer at the end of each path, and returns the answer that occurs most often. Wang et al. 2023 describe it as marginalizing out the reasoning: the vote estimates which answer has the most probability summed over all paths that lead to it, $\sum_r p(a, r \mid x)$, and returns that answer, while greedy decoding follows one path. It is a heuristic. Its gains are measurements: on GSM8K, Wang et al. reported 17.9 percentage points more accuracy than chain-of-thought prompting with greedy decoding, at the price of many samples per question.

## In plain words

Ask a model the same hard question many times and let it think out loud each time, with a bit of randomness so the thinking differs. Each run ends with an answer. Different lines of thought that reach the same answer are good evidence for that answer, because errors tend to scatter while correct reasoning tends to agree. So count the answers and keep the most common one. It costs one run per vote, and it only works when the answers can be compared, such as numbers or choices.

## When it applies

Self-consistency needs three things. The task must have a final answer that can be extracted and compared exactly, such as a number, a multiple-choice letter, or yes or no. The model must reason in a way that differs from sample to sample, which needs sampling with a temperature above 0. And the budget must allow $m$ full generations per question, since the cost grows linearly with $m$. It does not apply directly to open-ended text such as summaries or stories, where no two samples are equal; there a similarity-based choice such as [minimum Bayes risk decoding](/minimum-bayes-risk-decoding/) plays the same role.

## The template

The function extract maps a generated text to its final answer, for example the number after "The answer is".

```pseudo id=main
SELF-CONSISTENCY(model, x, m, extract)    ▷ x = the prompt with chain-of-thought examples
L1  count ← an empty map from answers to integers
L2  for i ← 1 to m do
L3      r ← sample a full output for x from the model   ▷ temperature T > 0, often with top-k
L4      a ← extract(r);  if a is none then skip this sample
L5      count[a] ← count[a] + 1
L6  return an answer with the largest count  ▷ ties: the first answer to reach that count
```

The samples are independent, so they can run in parallel as one batch. The vote is a [plurality vote](/plurality-voting/): the winner needs the most votes, not a majority.

## Classic examples

**A vote.** Five samples for a word problem end with the answers 18, 18, 26, 18 and 14. The vote returns 18, with 3 of 5 votes, even if the greedy path happened to end with 26.

**When more samples help.** Suppose each sample is correct with probability 0.4, and the wrong samples spread over three other answers with probability 0.2 each. With ties split at random, the vote is correct with probability 0.4 for $m = 1$, 0.5094 for $m = 5$, 0.6945 for $m = 15$ and 0.89 for $m = 40$. By the [law of large numbers](/law-of-large-numbers/) it tends to 1, because the correct answer is the most probable single answer.

**When more samples hurt.** Suppose instead that one wrong answer has probability 0.45, the correct one 0.4 and a third 0.15. The vote is correct with probability 0.4 for $m = 1$, 0.4146 for $m = 5$, 0.4096 for $m = 15$ and 0.3655 for $m = 40$, and it tends to 0. The vote returns the mode of the answer distribution of the model; it helps exactly when that mode is correct.

**The published results.** Wang et al. 2023 sampled up to 40 paths per question from several large models, using a temperature with top-k truncation. Against chain-of-thought prompting with greedy decoding, they reported absolute gains in accuracy of 17.9 points on GSM8K, 11.0 on SVAMP, 12.2 on AQuA, 6.4 on StrategyQA and 3.9 on ARC-challenge. Accuracy rose quickly over the first few paths and leveled off toward 40. They also compared the plain vote with votes weighted by the probability of each path under the model, and found that the plain vote did well, which they attribute to the poor calibration of those probabilities.

## Variations

- **Weighted votes.** Weight each answer by the probability of its path, or by the probability normalized by the length. The plain vote is the published default.
- **Early stopping.** Stop sampling once one answer has a lead that the remaining samples cannot overturn, or that is unlikely to be overturned, to save calls.
- **Similarity votes.** For free-form answers, choose the sample most similar to the others, which is [minimum Bayes risk decoding](/minimum-bayes-risk-decoding/) with a similarity as the utility. With the 0-1 utility on exact answers, minimum Bayes risk decoding over the samples is the plurality vote.
- **Verifiers.** Score each path with a separate trained model and pick the best one, or weight the vote by the scores. This needs extra training and data.
- **Diverse prompts.** Vary the chain-of-thought examples in the prompt across samples, in addition to the sampling noise.

## Pitfalls

- **Answer extraction.** "18", "18.0" and "$18" must count as one answer. Normalize the answers before the vote, and decide what to do with samples that have no answer.
- **Cost.** Forty samples cost forty times as much as one. Measure the gain per sample on your task; it often levels off well before 40.
- **A wrong mode.** If the model makes the same mistake most of the time, the vote makes it more confident, not more correct (the second example).
- **Temperature.** At $T = 0$ every sample is the greedy path and the vote is useless. Too high a temperature spreads the samples over nonsense. The paper used moderate temperatures with top-k truncation.
- **Not a probability of correctness.** The share of votes for the winner is a useful signal of confidence, but it is not a calibrated probability that the answer is right.

## Exercises

1. Show that with the 0-1 utility on extracted answers, minimum Bayes risk decoding over the $m$ samples returns the plurality winner.
2. For a sample distribution over answers with a unique most probable answer, prove that the plurality vote returns it with probability tending to 1 as $m$ grows. (Use a [Hoeffding bound](/hoeffding-inequality/) on each pair of answers.)
3. Compute the probability that a vote of 3 samples is correct when each sample is correct with probability 0.4 and wrong with probability 0.3 on each of two other answers, with ties split at random.
4. Design an early stopping rule that stops as soon as the leader cannot be overtaken by the remaining samples of a budget of $m$.

## References
