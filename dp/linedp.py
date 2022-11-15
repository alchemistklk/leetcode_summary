'''
'''


# 198. 打家劫舍
# https://leetcode.cn/problems/house-robber/?envType=study-plan&id=dong-tai-gui-hua-ji-chu&plan=dynamic-programming&plan_progress=4dfaiy2

from typing import List


class RobSolution:
    def rob(self, nums: List[int]) -> int:
        '''
        f[i]: 第i个房子最大收获
        f[i] = max(f[i - 1](不偷当前房子), f[i - 2] + nums[i](偷当前房子))
        '''
        n = len(nums) + 1
        f = [0] * n
        f[0] = 0
        f[1] = nums[0]

        for i in range(2, n):
            f[i] = max(f[i - 1], f[i - 2] + nums[i - 1])

        return f[n - 1]

# 213. 打家劫舍 II
# https://leetcode.cn/problems/house-robber-ii/


class RobIISolution:
    def rob(self, nums: List[int]) -> int:
        '''
        由于房子环形排列, 根据最后一件房子区分为两种情况
        最后一间房子被选中, 则不能选择第一间房子
        最后一件房子不被选中, 可以选择第一间房子
        '''

        n = len(nums)
        if n <= 2:
            return nums[0] if n == 1 else max(nums[0], nums[1])

        def dynamic(arr: List[int]) -> int:
            f = [0] * n
            f[0] = 0
            f[1] = arr[0]

            for i in range(2, n):
                f[i] = max(f[i - 1], f[i - 2] + arr[i - 1])
            return f[-1]

        # 选择最后的房子
        res1 = dynamic(nums[1::])
        # 不选择最后的房子
        res2 = dynamic(nums[:n - 1])
        return max(res1, res2)


# 256. 粉刷房子
# https://leetcode.cn/problems/paint-house/

class MinCostSolution:
    def minCost(self, costs: List[List[int]]) -> int:
        '''
        计算每一层的花费, 然后遍历最后一层得到最小的花费
        '''
        m = len(costs)

        for i in range(1, m):
            costs[i][0] += min(costs[i - 1][1], costs[i - 1][2])
            costs[i][1] += min(costs[i - 1][0], costs[i - 1][2])
            costs[i][2] += min(costs[i - 1][0], costs[i - 1][1])

        mn = 2001
        for i in range(3):
            if mn > costs[m - 1][i]:
                mn = costs[m - 1][i]
        return mn


# 265. 粉刷房子 II
# https://leetcode.cn/problems/paint-house-ii/
# ?envType=study-plan&id=dong-tai-gui-hua-ji-chu&plan=dynamic-programming&plan_progress=4dfaiy2

class MinCostIISolution:
    def minCostII(self, costs: List[List[int]]) -> int:
        m = len(costs)
        k = len(costs[0])
        for i in range(1, m):
            # 每一列的数据, 然后选择不同的列
            for j in range(k):
                tmp = 40001
                for p in range(k):
                    if j != p:
                        tmp = min(tmp, costs[i - 1][p])

                costs[i][j] += tmp

        mn = 40001

        for i in range(k):
            if mn > costs[m - 1][i]:
                mn = costs[m - 1][i]

        return mn


# 121. 买卖股票的最佳时机
# https://leetcode.cn/problems/best-time-to-buy-and-sell-stock/
# ?envType=study-plan&id=dong-tai-gui-hua-ji-chu&plan=dynamic-programming&plan_progress=4dfaiy2

class MaxProfitSolution:
    def maxProfit(self, prices: List[int]) -> int:
        mn = 10 ** 4 + 1
        ans = 0
        n = len(prices)
        for i in range(n):
            mn = min(mn, prices[i])
            ans = max(prices[i] - mn, ans)
        return ans


# 714. 买卖股票的最佳时机含手续费
# https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/

class MaxProfitSolutioContainFee:
    def maxProfit(self, prices: List[int], fee: int) -> int:
        '''
        转移方程: dp[0][0]当前时间手里没有股票, dp[0][1]当前时间手里有股票
                dp[i][0] = max(dp[i - 1][0], dp[i - 1][1] + prices[i] - fee)
                dp[i][1] = max(dp[i - 1][1], dp[i - 1][0] - prices[i])
        最终返回: dp[n - 1][0]
        '''
        # n = len(prices)
        # dp = [[0, 0] for _ in range(n)]
        # dp[0][0] = 0
        # dp[0][1] = -prices[0]

        # for i in range(1, n):
        #     dp[i][0] = max(dp[i - 1][0], dp[i - 1][1] + prices[i] - fee)
        #     dp[i][1] = max(dp[i - 1][1], dp[i - 1][0] - prices[i])
        # return dp[n - 1][0]

        n = len(prices)

        sell = 0
        buy = -prices[0]

        for i in range(1, n):
            sell = max(sell, buy + prices[i] - fee)
            buy = max(buy, sell - prices[i])

        return sell
