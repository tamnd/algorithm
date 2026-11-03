// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/insertion-sort/. The authors are listed in prov/3NS7RT.jsonl.

using Algorithm;
using Xunit;

public class InsertionSortTests
{
    [Fact]
    public void Example()
    {
        long[] a = [5, 2, 4, 6, 1, 3];
        InsertionSort.Sort<long>(a);
        Assert.Equal(new long[] { 1, 2, 3, 4, 5, 6 }, a);
    }

    [Fact]
    public void Edges()
    {
        long[] e = [];
        InsertionSort.Sort<long>(e);
        Assert.Empty(e);
        string[] w = ["pear", "fig", "apple"];
        InsertionSort.Sort<string>(w);
        Assert.Equal(new[] { "apple", "fig", "pear" }, w);
    }

    [Fact]
    public void RandomAgainstArraySort()
    {
        var rng = new Random(2150);
        for (int t = 0; t < 500; t++)
        {
            var a = new long[rng.Next(41)];
            for (int i = 0; i < a.Length; i++) a[i] = rng.Next(101) - 50;
            var want = (long[])a.Clone();
            Array.Sort(want);
            InsertionSort.Sort<long>(a);
            Assert.Equal(want, a);
        }
    }
}
