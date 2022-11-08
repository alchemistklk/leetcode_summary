"""
weekly 314

1. 模拟


2. 位运算
(1) pref[i] = pref[i - 1] ^ arr[i] -> pref[i - 1] ^ pref[i]
    = pref[i - 1] ^ pref[i - 1] ^ arr[i]
    = pref[i - 1] ^ pref[i] = arr[i]

(2) 差分数组 => diff[i] = arr[i] - arr[i - 1] => diff[0] + ... + diff[i] = arr[i]
    前缀和数组 => pre_sum[i] = arr[i] + pre_sum[i - 1]
             => arr[i] = pre_sum[i] - pre_sum[i - 1]


3. 贪心栈
(1) 删除 s 中字符并加到 t 尾部; 弹出 t 尾部字符 -> 存在先进后出的情况，使用栈
(2) 如果后面有较小的字符, 则继续向前遍历; 否则弹出当前的较小的字符
(3) 如何快速判断后面是否存在较小字符, 统计字符出现次数 ?
    通过计算所有字符出现次数, 从0开始遍历作为最小值, 如果当前字符出现次数为 0
    则代表栈里面小于当前字符的数字都可以出栈


4. 记忆化搜索/递归
(1) 记忆化搜索
    注意需要清除缓存, 避免内存溢出
(2) 递推
    刷表法: f[i+1][j+1][(v+grid[i][j])%k] = f[i][j+1][v] + f[i][j+1][v]
    查表法: f[i+1][j+1][v] = f[i][j+1][v-grid[i][j]]+f[i+1][j][v-grid[i][j]]



标签:
    1. pairwise的使用
    2. 差分数组, 异或计算结合律
    3. 快速统计后面字符串中最小数字
"""


from functools import cache
from itertools import pairwise
from string import ascii_lowercase
from typing import Counter, List


# 2432. 处理用时最长的那个任务的员工
# https://leetcode.cn/problems/the-employee-that-worked-on-the-longest-task/
class HardestWorkerSolution:
    def hardestWorker(self, n: int, logs: List[List]) -> int:
        # 使用packing的方式赋值
        ans, maxt = logs[0]
        # 快速计算当前元素与前一个元素的差值
        for (_, t0), (i, t) in pairwise(logs):
            t -= t0
            if t > maxt or (t == maxt and i < ans):
                ans = i
                maxt = t
        return ans


# 2433. 找出前缀异或的原始数组
# https://leetcode.cn/problems/find-the-original-array-of-prefix-xor/
class FindArraySolution:
    def findArray(self, pref: List[int]) -> List[int]:
        ans = [pref[0]]
        n = len(pref)
        for i in range(1, n):
            ans.append(pref[i - 1] ^ pref[i])

        return ans


# 2434. 使用机器人打印字典序最小的字符串
# https://leetcode.cn/problems/using-a-robot-to-print-the-lexicographically-smallest-string/
class RobotWithSolution:
    def robotWithString(self, s: str) -> str:
        cnt = Counter(s)
        # 代表 0 - 25
        mn = 0
        ans = []
        st = []
        for c in s:
            cnt[c] -= 1
            while mn < 25 and cnt[ascii_lowercase[mn]] == 0:
                mn += 1
            st.append(c)
            while st and st[-1] <= ascii_lowercase[mn]:
                ans.append(st.pop())

        return ''.join(ans)


# 2435. 矩阵中和能被 K 整除的路径
# https://leetcode.cn/problems/paths-in-matrix-whose-sum-is-divisible-by-k/

'''
方法一: 记忆化搜索
'''


class NumberOfPathsSolution:
    def numberOfPaths(self, grid: List[List[int]], k: int) -> int:
        m, n = len(grid), len(grid[0])
        mod = 10 ** 9 + 7

        @cache
        def dfs(i: int, j: int, v: int) -> int:
            if i >= m or j >= n:
                return 0
            # 先加入当前数字，之后进行判断，因为是mod运算，所以在任何时候都要计算
            v = (v + grid[i][j]) % k
            if i == m - 1 and j == n - 1 and v == 0:
                return 1

            return (dfs(i + 1, j, v) % mod + dfs(i, j + 1, v) % mod) % mod
        ans = dfs(0, 0, 0)
        dfs.cache_clear()
        return ans


'''
方法二: 递推的搜索方式
        查表法: 是为了得到 从其他节点得到 v
                f[i-1][j][v-grid[i-1][j]]+f[i][j-1][v-grid[i][j-1]]=f[i][j][v]
                # 为了避免出现 -1 < 0 的情况;使用 +1的操作方式
                # 为了避免出现 v-grid[i][j] < 0 的情况, (v-grid[i][j]+k)%k
                f[i][j+1][v+k-grid[i][j]]+f[i+1][j][v+k-grid[i][j]]=f[i+1][j+1][v]

        刷表法: 是为了得到 从 v 推导到下一个节点
                f[i+1][j+1][(v+grid[i][j])%k]+=f[i+1][j][v]+f[i][j+1][v]
'''


class Solution:
    def numberOfPaths(self, grid: List[List[int]], k: int) -> int:
        m, n = len(grid), len(grid[0])
        mod = 10 ** 9 + 7
        # 声明三维数组
        f = [[[0] * k for _ in range(n + 1)] for _ in range(m + 1)]

        # 初始值，因为是从f[1][1][]开始计算要以f[0][1]或者是f[1][0]为基础
        f[0][1][0] = 1
        for i, row in enumerate(grid):
            for j, x in enumerate(row):
                for v in range(k):
                    f[i + 1][j + 1][(v + x) % k] = (f[i + 1][j]
                                                    [v] + f[i][j + 1][v]) % mod

        return f[-1][-1][0]
