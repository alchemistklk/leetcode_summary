'''
1. 可被三整除的偶数的平均值

2. 最流行的视频创作者
(1) 题目获取歌手总的流行度, 使用map来记录, value 为 不同数据组成的集合
(2) value 为 sum_view, mx_view, id
(3) 更新总的最大播放量

3. 美丽整数的最小增量
(1) 要想让数位和变小则需要"进位"
(2) "进位"之后, 如何计算"进位"变化的数字, m = n + (tail - n % tail)
(3) 对于新的数字 m 则需要重新计算其数位是否符合要求

'''

# 2455. 可被三整除的偶数的平均值
# https://leetcode.cn/problems/average-value-of-even-numbers-that-are-divisible-by-three/


from typing import List


class AverageValueSolution:
    def averageValue(self, nums: List[int]) -> int:
        cnt = 0
        s = 0
        for i in nums:
            if i % 2 == 0 and i % 3 == 0:
                s += 1
                cnt += 1

        return s // cnt if cnt != 0 else 0


# 2456. 最流行的视频创作者
# https://leetcode.cn/problems/most-popular-video-creator/
class MostPopularCreatorSolution:
    def mostPopularCreator(self, creators: List[str], ids: List[str],
                           views: List[int]) -> List[List[str]]:
        '''
        1. 题目中要求返回播放量最高的视频, 如果相同播放量则字典序最小
        2. 记录用户的最大视频量以及最小的id
        '''
        # 使用map记录, key为用户name, value 为 元组 (sum_view, max_view, id)
        memo = {}
        mx_view = 0
        for m, i, v in zip(creators, ids, views):
            if m in memo:
                t = memo[m]
                t[0] += v
                if t[1] < v or t[1] == v and t[2] > i:
                    t[1] = v
                    t[2] = i
            else:
                memo[m] = [v, v, i]

            mx_view = max(mx_view, memo[m][0])

        ans = []
        for name, (sum_view, _, i) in memo.items():
            if sum_view == mx_view:
                ans.append([name, i])

        return ans

# 2457. 美丽整数的最小增量
# https://leetcode.cn/problems/minimum-addition-to-make-integer-beautiful/


class MakeIntegerBeautifulSolution:
    def makeIntegerBeautiful(self, n: int, target: int) -> int:
        '''
        1. 贪心求解时需要主动的模拟
        2. 为了让数位和变小, 则需要进位, 467 -> 470
        3. 如何计算进位需要的差值 10 - 467 % 10 = 3, 100 - 470 % 100 = 30
        4. 每次得到新的数字, 判断是否符合条件
        5. 为了避免最后一位为0, 计算进位所需要的数字需要多球一次mod
        '''

        tail = 1
        while True:
            m = x = n + (tail - n % tail) % tail
            cnt = 0
            while x:
                cnt += x % 10
                x //= 10

            if cnt <= target:
                return m - n

            tail *= 10
