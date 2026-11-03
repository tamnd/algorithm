// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/merge-sort/. The authors are listed in prov/4MRG7S.jsonl.

using Algorithm;
using Xunit;

public class MergeSortTests
{
    [Fact]
    public void Example()
    {
        long[] a = [38, 27, 43, 3, 9, 82, 10];
        MergeSort.Sort<long>(a);
        Assert.Equal(new long[] { 3, 9, 10, 27, 38, 43, 82 }, a);
    }

    [Fact]
    public void Edges()
    {
        foreach (var a in new[] { new long[] { }, new long[] { 1 }, new long[] { 2, 1 }, new long[] { 1, 1, 1 }, new long[] { 3, 2, 1 } })
        {
            var want = (long[])a.Clone();
            Array.Sort(want);
            MergeSort.Sort<long>(a);
            Assert.Equal(want, a);
        }
    }

    [Fact]
    public void RandomAgainstArraySort()
    {
        var rng = new Random(2150);
        for (int t = 0; t < 500; t++)
        {
            var a = new long[rng.Next(61)];
            for (int i = 0; i < a.Length; i++) a[i] = rng.Next(101) - 50;
            var want = (long[])a.Clone();
            Array.Sort(want);
            MergeSort.Sort<long>(a);
            Assert.Equal(want, a);
        }
    }
}
