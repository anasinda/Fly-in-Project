class Solution(object):
    def isPalindrome(self, x):
        """
        :type x: int
        :rtype: bool
        """
        if x < 0:
            return False

        temp = x
        res = 0
        while temp:
            res = int(res * 10 + (temp % 10))
            print(res)
            temp = int(temp / 10)

        print("this is res", res)
        return res == x

sol = Solution()
print(sol.isPalindrome(144))
