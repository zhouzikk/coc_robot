from dataclasses import dataclass
from 任务流程.基础任务框架 import 基础任务, 任务上下文
from 任务流程.夜世界打鱼.夜世界基础任务 import 夜世界基础任务


@dataclass
class 滑动配置:
    起点: tuple[int, int]
    终点: tuple[int, int]

class 收集圣水车任务(夜世界基础任务):
    def __init__(self ,上下文: '任务上下文'):
        super().__init__(上下文)

    def 执行(self) -> bool:
        try:
            找不到夜世界船的次数=0
            while True:
                是否匹配,( x, y)=self.是否出现图片("夜世界的船1.bmp|夜世界的船2.bmp|夜世界的船3.bmp|夜世界的船4.bmp|夜世界的船6.bmp")
                if 是否匹配:
                    # 点击车
                    self.上下文.点击(x - 118, y + 46)
                    # 点击收集
                    self.上下文.点击(605, 471)
                    self.上下文.脚本延时(1000)
                    # 关闭领取界面
                    self.上下文.点击(699, 103)
                    return True
                else:
                    找不到夜世界船的次数 += 1
                    self.上下文.滑动屏幕((595,182),(135,250))
                    self.上下文.置脚本状态(F"第{找不到夜世界船的次数}次找不到夜世界的船")
                    if 找不到夜世界船的次数 > 10:
                        raise RuntimeError("关闭游戏,原因:一直找不到夜世界的船")
        except RuntimeError as e:
            self.异常处理(e)
            return False


    def 异常处理(self, 异常: Exception,**关键字参数):
        super().异常处理(异常)
        self.上下文.发送重启请求(f"任务[{self.__class__.__name__}] 触发了异常：{异常}")