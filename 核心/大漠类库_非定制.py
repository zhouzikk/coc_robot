
import ctypes
import os
from comtypes.client import CreateObject
# 依赖库
# pip install comtypes -i https://mirrors.aliyun.com/pypi/simple

_local_dir = os.path.dirname(__file__)
class DM:

    def __init__(self,注册账号,注册密码):
        self.dm = None
        reg_path = f"{_local_dir}/DmReg.dll"
        dm_path = f"{_local_dir}/dm.dll"
        if not os.path.exists(reg_path):
            raise ValueError("免注册DmReg.dll 路径不存在 %s" % reg_path)
        if not os.path.exists(dm_path):
            raise ValueError("dm.dll 路径不存在 %s" % dm_path)
        print('正在免注册调用')
        dms = ctypes.windll.LoadLibrary(reg_path)
        location_dmreg = dm_path

        dms.SetDllPathW(location_dmreg, 0)
        self.dm = CreateObject("dm.dmsoft")
        print('免注册调用成功 版本号为:', self.Ver())
        self.reg(注册账号,注册密码)

    def reg(self,dm_user,dm_pass):
        res = self.Reg(dm_user, dm_pass)
        dm_res = {
            -1: "大漠无法连接网络",
            -2: "进程没有以管理员方式运行",
            0: "失败 (未知错误)",
            1: "成功",
            2: "余额不足",
            3: "绑定了本机器，但是账户余额不足50元",
            4: "注册码错误",
            5: "你的机器或者IP在黑名单列表中或者不在白名单列表中",
            6: "非法使用插件. 一般出现在定制插件时，使用了和绑定的用户名不同的注册码.  也有可能是系统的语言设置不是中文简体,也可能有这个错误",
            7: "你的帐号因为非法使用被封禁. （如果是在虚拟机中使用插件，必须使用Reg或者RegEx，不能使用RegNoMac或者RegExNoMac,否则可能会造成封号，或者封禁机器）",
            8: "ver_info不在你设置的附加白名单中",
            77: "机器码或者IP因为非法使用，而被封禁. （如果是在虚拟机中使用插件，必须使用Reg或者RegEx，不能使用RegNoMac或者RegExNoMac,否则可能会造成封号，或者封禁机器）",
        }
        print("大漠注册结果:", dm_res[res])
        return self.dm

    def ActiveInputMethod(self, arg0: int, arg1: str):
        return self.dm.ActiveInputMethod(arg0, arg1)

    def AddDict(self, arg0: int, arg1: str):
        return self.dm.AddDict(arg0, arg1)

    def AiEnableFindPicWindow(self, arg0: int):
        return self.dm.AiEnableFindPicWindow(arg0)

    def AiFindPic(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: float, arg6: int):
        return self.dm.AiFindPic(arg0, arg1, arg2, arg3, arg4, arg5, arg6)

    def AiFindPicEx(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: float, arg6: int):
        return self.dm.AiFindPicEx(arg0, arg1, arg2, arg3, arg4, arg5, arg6)

    def AiFindPicMem(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: float, arg6: int):
        return self.dm.AiFindPicMem(arg0, arg1, arg2, arg3, arg4, arg5, arg6)

    def AiFindPicMemEx(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: float, arg6: int):
        return self.dm.AiFindPicMemEx(arg0, arg1, arg2, arg3, arg4, arg5, arg6)

    def AiYoloDetectObjects(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: float, arg5: float):
        return self.dm.AiYoloDetectObjects(arg0, arg1, arg2, arg3, arg4, arg5)

    def AiYoloDetectObjectsToDataBmp(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: float, arg5: float, arg8: int):
        return self.dm.AiYoloDetectObjectsToDataBmp(arg0, arg1, arg2, arg3, arg4, arg5, arg8)

    def AiYoloDetectObjectsToFile(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: float, arg5: float, arg6: str, arg7: int):
        return self.dm.AiYoloDetectObjectsToFile(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7)

    def AiYoloFreeModel(self, arg0: int):
        return self.dm.AiYoloFreeModel(arg0)

    def AiYoloObjectsToString(self, arg0: str):
        return self.dm.AiYoloObjectsToString(arg0)

    def AiYoloSetModel(self, arg0: int, arg1: str, arg2: str):
        return self.dm.AiYoloSetModel(arg0, arg1, arg2)

    def AiYoloSetModelMemory(self, arg0: int, arg1: int, arg2: int, arg3: str):
        return self.dm.AiYoloSetModelMemory(arg0, arg1, arg2, arg3)

    def AiYoloSetVersion(self, arg0: str):
        return self.dm.AiYoloSetVersion(arg0)

    def AiYoloSortsObjects(self, arg0: str, arg1: int):
        return self.dm.AiYoloSortsObjects(arg0, arg1)

    def AiYoloUseModel(self, arg0: int):
        return self.dm.AiYoloUseModel(arg0)

    def AppendPicAddr(self, arg0: str, arg1: int, arg2: int):
        return self.dm.AppendPicAddr(arg0, arg1, arg2)

    def AsmAdd(self, arg0: str):
        return self.dm.AsmAdd(arg0)

    def AsmCall(self, arg0: int, arg1: int):
        return self.dm.AsmCall(arg0, arg1)

    def AsmCallEx(self, arg0: int, arg1: int, arg2: str):
        return self.dm.AsmCallEx(arg0, arg1, arg2)

    def AsmClear(self):
        return self.dm.AsmClear()

    def AsmSetTimeout(self, arg0: int, arg1: int):
        return self.dm.AsmSetTimeout(arg0, arg1)

    def Assemble(self, arg0: int, arg1: int):
        return self.dm.Assemble(arg0, arg1)

    def BGR2RGB(self, arg0: str):
        return self.dm.BGR2RGB(arg0)

    def Beep(self, arg0: int, arg1: int):
        return self.dm.Beep(arg0, arg1)

    def BindWindow(self, arg0: int, arg1: str, arg2: str, arg3: str, arg4: int):
        return self.dm.BindWindow(arg0, arg1, arg2, arg3, arg4)

    def BindWindowEx(self, arg0: int, arg1: str, arg2: str, arg3: str, arg4: str, arg5: int):
        return self.dm.BindWindowEx(arg0, arg1, arg2, arg3, arg4, arg5)

    def Capture(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str):
        return self.dm.Capture(arg0, arg1, arg2, arg3, arg4)

    def CaptureGif(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: int, arg6: int):
        return self.dm.CaptureGif(arg0, arg1, arg2, arg3, arg4, arg5, arg6)

    def CaptureJpg(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: int):
        return self.dm.CaptureJpg(arg0, arg1, arg2, arg3, arg4, arg5)

    def CapturePng(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str):
        return self.dm.CapturePng(arg0, arg1, arg2, arg3, arg4)

    def CapturePre(self, arg0: str):
        return self.dm.CapturePre(arg0)

    def CheckFontSmooth(self):
        return self.dm.CheckFontSmooth()

    def CheckInputMethod(self, arg0: int, arg1: str):
        return self.dm.CheckInputMethod(arg0, arg1)

    def CheckUAC(self):
        return self.dm.CheckUAC()

    def ClearDict(self, arg0: int):
        return self.dm.ClearDict(arg0)

    def CmpColor(self, arg0: int, arg1: int, arg2: str, arg3: float):
        return self.dm.CmpColor(arg0, arg1, arg2, arg3)

    def CopyFile(self, arg0: str, arg1: str, arg2: int):
        return self.dm.CopyFile(arg0, arg1, arg2)

    def CreateFolder(self, arg0: str):
        return self.dm.CreateFolder(arg0)

    def CreateFoobarCustom(self, arg0: int, arg1: int, arg2: int, arg3: str, arg4: str, arg5: float):
        return self.dm.CreateFoobarCustom(arg0, arg1, arg2, arg3, arg4, arg5)

    def CreateFoobarEllipse(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: int):
        return self.dm.CreateFoobarEllipse(arg0, arg1, arg2, arg3, arg4)

    def CreateFoobarRect(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: int):
        return self.dm.CreateFoobarRect(arg0, arg1, arg2, arg3, arg4)

    def CreateFoobarRoundRect(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: int, arg5: int, arg6: int):
        return self.dm.CreateFoobarRoundRect(arg0, arg1, arg2, arg3, arg4, arg5, arg6)

    def DecodeFile(self, arg0: str, arg1: str):
        return self.dm.DecodeFile(arg0, arg1)

    def DelEnv(self, arg0: int, arg1: str):
        return self.dm.DelEnv(arg0, arg1)

    def Delays(self, arg0: int, arg1: int):
        return self.dm.Delays(arg0, arg1)

    def DeleteFile(self, arg0: str):
        return self.dm.DeleteFile(arg0)

    def DeleteFolder(self, arg0: str):
        return self.dm.DeleteFolder(arg0)

    def DeleteIni(self, arg0: str, arg1: str, arg2: str):
        return self.dm.DeleteIni(arg0, arg1, arg2)

    def DeleteIniPwd(self, arg0: str, arg1: str, arg2: str, arg3: str):
        return self.dm.DeleteIniPwd(arg0, arg1, arg2, arg3)

    def DisAssemble(self, arg0: str, arg1: int, arg2: int):
        return self.dm.DisAssemble(arg0, arg1, arg2)

    def DisableCloseDisplayAndSleep(self):
        return self.dm.DisableCloseDisplayAndSleep()

    def DisableFontSmooth(self):
        return self.dm.DisableFontSmooth()

    def DisablePowerSave(self):
        return self.dm.DisablePowerSave()

    def DisableScreenSave(self):
        return self.dm.DisableScreenSave()

    def DmGuard(self, arg0: int, arg1: str):
        return self.dm.DmGuard(arg0, arg1)

    def DmGuardExtract(self, arg0: str, arg1: str):
        return self.dm.DmGuardExtract(arg0, arg1)

    def DmGuardLoadCustom(self, arg0: str, arg1: str):
        return self.dm.DmGuardLoadCustom(arg0, arg1)

    def DmGuardParams(self, arg0: str, arg1: str, arg2: str):
        return self.dm.DmGuardParams(arg0, arg1, arg2)

    def DoubleToData(self, arg0: float):
        return self.dm.DoubleToData(arg0)

    def DownCpu(self, arg0: int, arg1: int):
        return self.dm.DownCpu(arg0, arg1)

    def DownloadFile(self, arg0: str, arg1: str, arg2: int):
        return self.dm.DownloadFile(arg0, arg1, arg2)

    def EnableBind(self, arg0: int):
        return self.dm.EnableBind(arg0)

    def EnableDisplayDebug(self, arg0: int):
        return self.dm.EnableDisplayDebug(arg0)

    def EnableFakeActive(self, arg0: int):
        return self.dm.EnableFakeActive(arg0)

    def EnableFindPicMultithread(self, arg0: int):
        return self.dm.EnableFindPicMultithread(arg0)

    def EnableFontSmooth(self):
        return self.dm.EnableFontSmooth()

    def EnableGetColorByCapture(self, arg0: int):
        return self.dm.EnableGetColorByCapture(arg0)

    def EnableIme(self, arg0: int):
        return self.dm.EnableIme(arg0)

    def EnableKeypadMsg(self, arg0: int):
        return self.dm.EnableKeypadMsg(arg0)

    def EnableKeypadPatch(self, arg0: int):
        return self.dm.EnableKeypadPatch(arg0)

    def EnableKeypadSync(self, arg0: int, arg1: int):
        return self.dm.EnableKeypadSync(arg0, arg1)

    def EnableMouseAccuracy(self, arg0: int):
        return self.dm.EnableMouseAccuracy(arg0)

    def EnableMouseMsg(self, arg0: int):
        return self.dm.EnableMouseMsg(arg0)

    def EnableMouseSync(self, arg0: int, arg1: int):
        return self.dm.EnableMouseSync(arg0, arg1)

    def EnablePicCache(self, arg0: int):
        return self.dm.EnablePicCache(arg0)

    def EnableRealKeypad(self, arg0: int):
        return self.dm.EnableRealKeypad(arg0)

    def EnableRealMouse(self, arg0: int, arg1: int, arg2: int):
        return self.dm.EnableRealMouse(arg0, arg1, arg2)

    def EnableShareDict(self, arg0: int):
        return self.dm.EnableShareDict(arg0)

    def EnableSpeedDx(self, arg0: int):
        return self.dm.EnableSpeedDx(arg0)

    def EncodeFile(self, arg0: str, arg1: str):
        return self.dm.EncodeFile(arg0, arg1)

    def EnterCri(self):
        return self.dm.EnterCri()

    def EnumIniKey(self, arg0: str, arg1: str):
        return self.dm.EnumIniKey(arg0, arg1)

    def EnumIniKeyPwd(self, arg0: str, arg1: str, arg2: str):
        return self.dm.EnumIniKeyPwd(arg0, arg1, arg2)

    def EnumIniSection(self, arg0: str):
        return self.dm.EnumIniSection(arg0)

    def EnumIniSectionPwd(self, arg0: str, arg1: str):
        return self.dm.EnumIniSectionPwd(arg0, arg1)

    def EnumProcess(self, arg0: str):
        return self.dm.EnumProcess(arg0)

    def EnumWindow(self, arg0: int, arg1: str, arg2: str, arg3: int):
        return self.dm.EnumWindow(arg0, arg1, arg2, arg3)

    def EnumWindowByProcess(self, arg0: str, arg1: str, arg2: str, arg3: int):
        return self.dm.EnumWindowByProcess(arg0, arg1, arg2, arg3)

    def EnumWindowByProcessId(self, arg0: int, arg1: str, arg2: str, arg3: int):
        return self.dm.EnumWindowByProcessId(arg0, arg1, arg2, arg3)

    def EnumWindowSuper(self, arg0: str, arg1: int, arg2: int, arg3: str, arg4: int, arg5: int, arg6: int):
        return self.dm.EnumWindowSuper(arg0, arg1, arg2, arg3, arg4, arg5, arg6)

    def ExcludePos(self, arg0: str, arg1: int, arg2: int, arg3: int, arg4: int, arg5: int):
        return self.dm.ExcludePos(arg0, arg1, arg2, arg3, arg4, arg5)

    def ExecuteCmd(self, arg0: str, arg1: str, arg2: int):
        return self.dm.ExecuteCmd(arg0, arg1, arg2)

    def ExitOs(self, arg0: int):
        return self.dm.ExitOs(arg0)

    def FaqCancel(self):
        return self.dm.FaqCancel()

    def FaqCapture(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: int, arg5: int, arg6: int):
        return self.dm.FaqCapture(arg0, arg1, arg2, arg3, arg4, arg5, arg6)

    def FaqCaptureFromFile(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: int):
        return self.dm.FaqCaptureFromFile(arg0, arg1, arg2, arg3, arg4, arg5)

    def FaqCaptureString(self, arg0: str):
        return self.dm.FaqCaptureString(arg0)

    def FaqFetch(self):
        return self.dm.FaqFetch()

    def FaqGetSize(self, arg0: int):
        return self.dm.FaqGetSize(arg0)

    def FaqIsPosted(self):
        return self.dm.FaqIsPosted()

    def FaqPost(self, arg0: str, arg1: int, arg2: int, arg3: int):
        return self.dm.FaqPost(arg0, arg1, arg2, arg3)

    def FaqRelease(self, arg0: int):
        return self.dm.FaqRelease(arg0)

    def FaqSend(self, arg0: str, arg1: int, arg2: int, arg3: int):
        return self.dm.FaqSend(arg0, arg1, arg2, arg3)

    def FetchWord(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: str):
        return self.dm.FetchWord(arg0, arg1, arg2, arg3, arg4, arg5)

    def FindColor(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: float, arg6: int):
        return self.dm.FindColor(arg0, arg1, arg2, arg3, arg4, arg5, arg6)

    def FindColorBlock(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: float, arg6: int, arg7: int, arg8: int):
        return self.dm.FindColorBlock(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8)

    def FindColorBlockEx(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: float, arg6: int, arg7: int, arg8: int):
        return self.dm.FindColorBlockEx(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8)

    def FindColorE(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: float, arg6: int):
        return self.dm.FindColorE(arg0, arg1, arg2, arg3, arg4, arg5, arg6)

    def FindColorEx(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: float, arg6: int):
        return self.dm.FindColorEx(arg0, arg1, arg2, arg3, arg4, arg5, arg6)

    def FindData(self, arg0: int, arg1: str, arg2: str):
        return self.dm.FindData(arg0, arg1, arg2)

    def FindDataEx(self, arg0: int, arg1: str, arg2: str, arg3: int, arg4: int, arg5: int):
        return self.dm.FindDataEx(arg0, arg1, arg2, arg3, arg4, arg5)

    def FindDouble(self, arg0: int, arg1: str, arg2: float, arg3: float):
        return self.dm.FindDouble(arg0, arg1, arg2, arg3)

    def FindDoubleEx(self, arg0: int, arg1: str, arg2: float, arg3: float, arg4: int, arg5: int, arg6: int):
        return self.dm.FindDoubleEx(arg0, arg1, arg2, arg3, arg4, arg5, arg6)

    def FindFloat(self, arg0: int, arg1: str, arg2: str, arg3: str):
        return self.dm.FindFloat(arg0, arg1, arg2, arg3)

    def FindFloatEx(self, arg0: int, arg1: str, arg2: str, arg3: str, arg4: int, arg5: int, arg6: int):
        return self.dm.FindFloatEx(arg0, arg1, arg2, arg3, arg4, arg5, arg6)

    def FindInputMethod(self, arg0: str):
        return self.dm.FindInputMethod(arg0)

    def FindInt(self, arg0: int, arg1: str, arg2: int, arg3: int, arg4: int):
        return self.dm.FindInt(arg0, arg1, arg2, arg3, arg4)

    def FindIntEx(self, arg0: int, arg1: str, arg2: int, arg3: int, arg4: int, arg5: int, arg6: int, arg7: int):
        return self.dm.FindIntEx(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7)

    def FindMulColor(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: float):
        return self.dm.FindMulColor(arg0, arg1, arg2, arg3, arg4, arg5)

    def FindMultiColor(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: str, arg6: float, arg7: int):
        return self.dm.FindMultiColor(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7)

    def FindMultiColorE(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: str, arg6: float, arg7: int):
        return self.dm.FindMultiColorE(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7)

    def FindMultiColorEx(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: str, arg6: float, arg7: int):
        return self.dm.FindMultiColorEx(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7)

    def FindNearestPos(self, arg0: str, arg1: int, arg2: int, arg3: int):
        return self.dm.FindNearestPos(arg0, arg1, arg2, arg3)

    def FindPic(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: str, arg6: float, arg7: int):
        return self.dm.FindPic(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7)

    def FindPicE(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: str, arg6: float, arg7: int):
        return self.dm.FindPicE(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7)

    def FindPicEx(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: str, arg6: float, arg7: int):
        return self.dm.FindPicEx(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7)

    def FindPicExS(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: str, arg6: float, arg7: int):
        return self.dm.FindPicExS(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7)

    def FindPicMem(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: str, arg6: float, arg7: int):
        return self.dm.FindPicMem(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7)

    def FindPicMemE(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: str, arg6: float, arg7: int):
        return self.dm.FindPicMemE(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7)

    def FindPicMemEx(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: str, arg6: float, arg7: int):
        return self.dm.FindPicMemEx(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7)

    def FindPicS(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: str, arg6: float, arg7: int):
        return self.dm.FindPicS(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7)

    def FindPicSim(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: str, arg6: int, arg7: int):
        return self.dm.FindPicSim(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7)

    def FindPicSimE(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: str, arg6: int, arg7: int):
        return self.dm.FindPicSimE(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7)

    def FindPicSimEx(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: str, arg6: int, arg7: int):
        return self.dm.FindPicSimEx(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7)

    def FindPicSimMem(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: str, arg6: int, arg7: int):
        return self.dm.FindPicSimMem(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7)

    def FindPicSimMemE(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: str, arg6: int, arg7: int):
        return self.dm.FindPicSimMemE(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7)

    def FindPicSimMemEx(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: str, arg6: int, arg7: int):
        return self.dm.FindPicSimMemEx(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7)

    def FindShape(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: float, arg6: int):
        return self.dm.FindShape(arg0, arg1, arg2, arg3, arg4, arg5, arg6)

    def FindShapeE(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: float, arg6: int):
        return self.dm.FindShapeE(arg0, arg1, arg2, arg3, arg4, arg5, arg6)

    def FindShapeEx(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: float, arg6: int):
        return self.dm.FindShapeEx(arg0, arg1, arg2, arg3, arg4, arg5, arg6)

    def FindStr(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: str, arg6: float):
        return self.dm.FindStr(arg0, arg1, arg2, arg3, arg4, arg5, arg6)

    def FindStrE(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: str, arg6: float):
        return self.dm.FindStrE(arg0, arg1, arg2, arg3, arg4, arg5, arg6)

    def FindStrEx(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: str, arg6: float):
        return self.dm.FindStrEx(arg0, arg1, arg2, arg3, arg4, arg5, arg6)

    def FindStrExS(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: str, arg6: float):
        return self.dm.FindStrExS(arg0, arg1, arg2, arg3, arg4, arg5, arg6)

    def FindStrFast(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: str, arg6: float):
        return self.dm.FindStrFast(arg0, arg1, arg2, arg3, arg4, arg5, arg6)

    def FindStrFastE(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: str, arg6: float):
        return self.dm.FindStrFastE(arg0, arg1, arg2, arg3, arg4, arg5, arg6)

    def FindStrFastEx(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: str, arg6: float):
        return self.dm.FindStrFastEx(arg0, arg1, arg2, arg3, arg4, arg5, arg6)

    def FindStrFastExS(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: str, arg6: float):
        return self.dm.FindStrFastExS(arg0, arg1, arg2, arg3, arg4, arg5, arg6)

    def FindStrFastS(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: str, arg6: float):
        return self.dm.FindStrFastS(arg0, arg1, arg2, arg3, arg4, arg5, arg6)

    def FindStrS(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: str, arg6: float):
        return self.dm.FindStrS(arg0, arg1, arg2, arg3, arg4, arg5, arg6)

    def FindStrWithFont(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: str, arg6: float, arg7: str, arg8: int, arg9: int):
        return self.dm.FindStrWithFont(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9)

    def FindStrWithFontE(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: str, arg6: float, arg7: str, arg8: int, arg9: int):
        return self.dm.FindStrWithFontE(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9)

    def FindStrWithFontEx(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: str, arg6: float, arg7: str, arg8: int, arg9: int):
        return self.dm.FindStrWithFontEx(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9)

    def FindString(self, arg0: int, arg1: str, arg2: str, arg3: int):
        return self.dm.FindString(arg0, arg1, arg2, arg3)

    def FindStringEx(self, arg0: int, arg1: str, arg2: str, arg3: int, arg4: int, arg5: int, arg6: int):
        return self.dm.FindStringEx(arg0, arg1, arg2, arg3, arg4, arg5, arg6)

    def FindWindow(self, arg0: str, arg1: str):
        return self.dm.FindWindow(arg0, arg1)

    def FindWindowByProcess(self, arg0: str, arg1: str, arg2: str):
        return self.dm.FindWindowByProcess(arg0, arg1, arg2)

    def FindWindowByProcessId(self, arg0: int, arg1: str, arg2: str):
        return self.dm.FindWindowByProcessId(arg0, arg1, arg2)

    def FindWindowEx(self, arg0: int, arg1: str, arg2: str):
        return self.dm.FindWindowEx(arg0, arg1, arg2)

    def FindWindowSuper(self, arg0: str, arg1: int, arg2: int, arg3: str, arg4: int, arg5: int):
        return self.dm.FindWindowSuper(arg0, arg1, arg2, arg3, arg4, arg5)

    def FloatToData(self, arg0: str):
        return self.dm.FloatToData(arg0)

    def FoobarClearText(self, arg0: int):
        return self.dm.FoobarClearText(arg0)

    def FoobarClose(self, arg0: int):
        return self.dm.FoobarClose(arg0)

    def FoobarDrawLine(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: int, arg5: str, arg6: int, arg7: int):
        return self.dm.FoobarDrawLine(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7)

    def FoobarDrawPic(self, arg0: int, arg1: int, arg2: int, arg3: str, arg4: str):
        return self.dm.FoobarDrawPic(arg0, arg1, arg2, arg3, arg4)

    def FoobarDrawText(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: int, arg5: str, arg6: str, arg7: int):
        return self.dm.FoobarDrawText(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7)

    def FoobarFillRect(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: int, arg5: str):
        return self.dm.FoobarFillRect(arg0, arg1, arg2, arg3, arg4, arg5)

    def FoobarLock(self, arg0: int):
        return self.dm.FoobarLock(arg0)

    def FoobarPrintText(self, arg0: int, arg1: str, arg2: str):
        return self.dm.FoobarPrintText(arg0, arg1, arg2)

    def FoobarSetFont(self, arg0: int, arg1: str, arg2: int, arg3: int):
        return self.dm.FoobarSetFont(arg0, arg1, arg2, arg3)

    def FoobarSetSave(self, arg0: int, arg1: str, arg2: int, arg3: str):
        return self.dm.FoobarSetSave(arg0, arg1, arg2, arg3)

    def FoobarSetTrans(self, arg0: int, arg1: int, arg2: str, arg3: float):
        return self.dm.FoobarSetTrans(arg0, arg1, arg2, arg3)

    def FoobarStartGif(self, arg0: int, arg1: int, arg2: int, arg3: str, arg4: int, arg5: int):
        return self.dm.FoobarStartGif(arg0, arg1, arg2, arg3, arg4, arg5)

    def FoobarStopGif(self, arg0: int, arg1: int, arg2: int, arg3: str):
        return self.dm.FoobarStopGif(arg0, arg1, arg2, arg3)

    def FoobarTextLineGap(self, arg0: int, arg1: int):
        return self.dm.FoobarTextLineGap(arg0, arg1)

    def FoobarTextPrintDir(self, arg0: int, arg1: int):
        return self.dm.FoobarTextPrintDir(arg0, arg1)

    def FoobarTextRect(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: int):
        return self.dm.FoobarTextRect(arg0, arg1, arg2, arg3, arg4)

    def FoobarUnlock(self, arg0: int):
        return self.dm.FoobarUnlock(arg0)

    def FoobarUpdate(self, arg0: int):
        return self.dm.FoobarUpdate(arg0)

    def ForceUnBindWindow(self, arg0: int):
        return self.dm.ForceUnBindWindow(arg0)

    def FreePic(self, arg0: str):
        return self.dm.FreePic(arg0)

    def FreeProcessMemory(self, arg0: int):
        return self.dm.FreeProcessMemory(arg0)

    def FreeScreenData(self, arg0: int):
        return self.dm.FreeScreenData(arg0)

    def GetAveHSV(self, arg0: int, arg1: int, arg2: int, arg3: int):
        return self.dm.GetAveHSV(arg0, arg1, arg2, arg3)

    def GetAveRGB(self, arg0: int, arg1: int, arg2: int, arg3: int):
        return self.dm.GetAveRGB(arg0, arg1, arg2, arg3)

    def GetBasePath(self):
        return self.dm.GetBasePath()

    def GetBindWindow(self):
        return self.dm.GetBindWindow()

    def GetClientRect(self, arg0: int):
        return self.dm.GetClientRect(arg0)

    def GetClientSize(self, arg0: int):
        return self.dm.GetClientSize(arg0)

    def GetClipboard(self):
        return self.dm.GetClipboard()

    def GetColor(self, arg0: int, arg1: int):
        return self.dm.GetColor(arg0, arg1)

    def GetColorBGR(self, arg0: int, arg1: int):
        return self.dm.GetColorBGR(arg0, arg1)

    def GetColorHSV(self, arg0: int, arg1: int):
        return self.dm.GetColorHSV(arg0, arg1)

    def GetColorNum(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: float):
        return self.dm.GetColorNum(arg0, arg1, arg2, arg3, arg4, arg5)

    def GetCommandLine(self, arg0: int):
        return self.dm.GetCommandLine(arg0)

    def GetCpuType(self):
        return self.dm.GetCpuType()

    def GetCpuUsage(self):
        return self.dm.GetCpuUsage()

    def GetCursorPos(self):
        return self.dm.GetCursorPos()

    def GetCursorShape(self):
        return self.dm.GetCursorShape()

    def GetCursorShapeEx(self, arg0: int):
        return self.dm.GetCursorShapeEx(arg0)

    def GetCursorSpot(self):
        return self.dm.GetCursorSpot()

    def GetDPI(self):
        return self.dm.GetDPI()

    def GetDict(self, arg0: int, arg1: int):
        return self.dm.GetDict(arg0, arg1)

    def GetDictCount(self, arg0: int):
        return self.dm.GetDictCount(arg0)

    def GetDictInfo(self, arg0: str, arg1: str, arg2: int, arg3: int):
        return self.dm.GetDictInfo(arg0, arg1, arg2, arg3)

    def GetDir(self, arg0: int):
        return self.dm.GetDir(arg0)

    def GetDiskModel(self, arg0: int):
        return self.dm.GetDiskModel(arg0)

    def GetDiskReversion(self, arg0: int):
        return self.dm.GetDiskReversion(arg0)

    def GetDiskSerial(self, arg0: int):
        return self.dm.GetDiskSerial(arg0)

    def GetDisplayInfo(self):
        return self.dm.GetDisplayInfo()

    def GetDmCount(self):
        return self.dm.GetDmCount()

    def GetEnv(self, arg0: int, arg1: str):
        return self.dm.GetEnv(arg0, arg1)

    def GetFileLength(self, arg0: str):
        return self.dm.GetFileLength(arg0)

    def GetForegroundFocus(self):
        return self.dm.GetForegroundFocus()

    def GetForegroundWindow(self):
        return self.dm.GetForegroundWindow()

    def GetFps(self):
        return self.dm.GetFps()

    def GetID(self):
        return self.dm.GetID()

    def GetKeyState(self, arg0: int):
        return self.dm.GetKeyState(arg0)

    def GetLastError(self):
        return self.dm.GetLastError()

    def GetLocale(self):
        return self.dm.GetLocale()

    def GetMac(self):
        return self.dm.GetMac()

    def GetMachineCode(self):
        return self.dm.GetMachineCode()

    def GetMachineCodeNoMac(self):
        return self.dm.GetMachineCodeNoMac()

    def GetMemoryUsage(self):
        return self.dm.GetMemoryUsage()

    def GetModuleBaseAddr(self, arg0: int, arg1: str):
        return self.dm.GetModuleBaseAddr(arg0, arg1)

    def GetModuleSize(self, arg0: int, arg1: str):
        return self.dm.GetModuleSize(arg0, arg1)

    def GetMousePointWindow(self):
        return self.dm.GetMousePointWindow()

    def GetMouseSpeed(self):
        return self.dm.GetMouseSpeed()

    def GetNetTime(self):
        return self.dm.GetNetTime()

    def GetNetTimeByIp(self, arg0: str):
        return self.dm.GetNetTimeByIp(arg0)

    def GetNetTimeSafe(self):
        return self.dm.GetNetTimeSafe()

    def GetNowDict(self):
        return self.dm.GetNowDict()

    def GetOsBuildNumber(self):
        return self.dm.GetOsBuildNumber()

    def GetOsType(self):
        return self.dm.GetOsType()

    def GetPath(self):
        return self.dm.GetPath()

    def GetPicSize(self, arg0: str):
        return self.dm.GetPicSize(arg0)

    def GetPointWindow(self, arg0: int, arg1: int):
        return self.dm.GetPointWindow(arg0, arg1)

    def GetProcessInfo(self, arg0: int):
        return self.dm.GetProcessInfo(arg0)

    def GetRealPath(self, arg0: str):
        return self.dm.GetRealPath(arg0)

    def GetRemoteApiAddress(self, arg0: int, arg1: int, arg2: str):
        return self.dm.GetRemoteApiAddress(arg0, arg1, arg2)

    def GetResultCount(self, arg0: str):
        return self.dm.GetResultCount(arg0)

    def GetResultPos(self, arg0: str, arg1: int):
        return self.dm.GetResultPos(arg0, arg1)

    def GetScreenData(self, arg0: int, arg1: int, arg2: int, arg3: int):
        return self.dm.GetScreenData(arg0, arg1, arg2, arg3)

    def GetScreenDataBmp(self, arg0: int, arg1: int, arg2: int, arg3: int):
        return self.dm.GetScreenDataBmp(arg0, arg1, arg2, arg3)

    def GetScreenDepth(self):
        return self.dm.GetScreenDepth()

    def GetScreenHeight(self):
        return self.dm.GetScreenHeight()

    def GetScreenWidth(self):
        return self.dm.GetScreenWidth()

    def GetSpecialWindow(self, arg0: int):
        return self.dm.GetSpecialWindow(arg0)

    def GetSystemInfo(self, arg0: str, arg1: int):
        return self.dm.GetSystemInfo(arg0, arg1)

    def GetTime(self):
        return self.dm.GetTime()

    def GetTypeInfoCount(self):
        return self.dm.GetTypeInfoCount()

    def GetWindow(self, arg0: int, arg1: int):
        return self.dm.GetWindow(arg0, arg1)

    def GetWindowClass(self, arg0: int):
        return self.dm.GetWindowClass(arg0)

    def GetWindowProcessId(self, arg0: int):
        return self.dm.GetWindowProcessId(arg0)

    def GetWindowProcessPath(self, arg0: int):
        return self.dm.GetWindowProcessPath(arg0)

    def GetWindowRect(self, arg0: int):
        return self.dm.GetWindowRect(arg0)

    def GetWindowState(self, arg0: int, arg1: int):
        return self.dm.GetWindowState(arg0, arg1)

    def GetWindowThreadId(self, arg0: int):
        return self.dm.GetWindowThreadId(arg0)

    def GetWindowTitle(self, arg0: int):
        return self.dm.GetWindowTitle(arg0)

    def GetWordResultCount(self, arg0: str):
        return self.dm.GetWordResultCount(arg0)

    def GetWordResultPos(self, arg0: str, arg1: int):
        return self.dm.GetWordResultPos(arg0, arg1)

    def GetWordResultStr(self, arg0: str, arg1: int):
        return self.dm.GetWordResultStr(arg0, arg1)

    def GetWords(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: float):
        return self.dm.GetWords(arg0, arg1, arg2, arg3, arg4, arg5)

    def GetWordsNoDict(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str):
        return self.dm.GetWordsNoDict(arg0, arg1, arg2, arg3, arg4)

    def HackSpeed(self, arg0: float):
        return self.dm.HackSpeed(arg0)

    def Hex32(self, arg0: int):
        return self.dm.Hex32(arg0)

    def Hex64(self, arg0: int):
        return self.dm.Hex64(arg0)

    def ImageToBmp(self, arg0: str, arg1: str):
        return self.dm.ImageToBmp(arg0, arg1)

    def InitCri(self):
        return self.dm.InitCri()

    def Int64ToInt32(self, arg0: int):
        return self.dm.Int64ToInt32(arg0)

    def IntToData(self, arg0: int, arg1: int):
        return self.dm.IntToData(arg0, arg1)

    def Is64Bit(self):
        return self.dm.Is64Bit()

    def IsBind(self, arg0: int):
        return self.dm.IsBind(arg0)

    def IsDisplayDead(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: int):
        return self.dm.IsDisplayDead(arg0, arg1, arg2, arg3, arg4)

    def IsFileExist(self, arg0: str):
        return self.dm.IsFileExist(arg0)

    def IsFolderExist(self, arg0: str):
        return self.dm.IsFolderExist(arg0)

    def IsSurrpotVt(self):
        return self.dm.IsSurrpotVt()

    def KeyDown(self, arg0: int):
        return self.dm.KeyDown(arg0)

    def KeyDownChar(self, arg0: str):
        return self.dm.KeyDownChar(arg0)

    def KeyPress(self, arg0: int):
        return self.dm.KeyPress(arg0)

    def KeyPressChar(self, arg0: str):
        return self.dm.KeyPressChar(arg0)

    def KeyPressStr(self, arg0: str, arg1: int):
        return self.dm.KeyPressStr(arg0, arg1)

    def KeyUp(self, arg0: int):
        return self.dm.KeyUp(arg0)

    def KeyUpChar(self, arg0: str):
        return self.dm.KeyUpChar(arg0)

    def LeaveCri(self):
        return self.dm.LeaveCri()

    def LeftClick(self):
        return self.dm.LeftClick()

    def LeftDoubleClick(self):
        return self.dm.LeftDoubleClick()

    def LeftDown(self):
        return self.dm.LeftDown()

    def LeftUp(self):
        return self.dm.LeftUp()

    def LoadAi(self, arg0: str):
        return self.dm.LoadAi(arg0)

    def LoadAiMemory(self, arg0: int, arg1: int):
        return self.dm.LoadAiMemory(arg0, arg1)

    def LoadPic(self, arg0: str):
        return self.dm.LoadPic(arg0)

    def LoadPicByte(self, arg0: int, arg1: int, arg2: str):
        return self.dm.LoadPicByte(arg0, arg1, arg2)

    def LockDisplay(self, arg0: int):
        return self.dm.LockDisplay(arg0)

    def LockInput(self, arg0: int):
        return self.dm.LockInput(arg0)

    def LockMouseRect(self, arg0: int, arg1: int, arg2: int, arg3: int):
        return self.dm.LockMouseRect(arg0, arg1, arg2, arg3)

    def Log(self, arg0: str):
        return self.dm.Log(arg0)

    def MatchPicName(self, arg0: str):
        return self.dm.MatchPicName(arg0)

    def Md5(self, arg0: str):
        return self.dm.Md5(arg0)

    def MiddleClick(self):
        return self.dm.MiddleClick()

    def MiddleDown(self):
        return self.dm.MiddleDown()

    def MiddleUp(self):
        return self.dm.MiddleUp()

    def MoveDD(self, arg0: int, arg1: int):
        return self.dm.MoveDD(arg0, arg1)

    def MoveFile(self, arg0: str, arg1: str):
        return self.dm.MoveFile(arg0, arg1)

    def MoveR(self, arg0: int, arg1: int):
        return self.dm.MoveR(arg0, arg1)

    def MoveTo(self, arg0: int, arg1: int):
        return self.dm.MoveTo(arg0, arg1)

    def MoveToEx(self, arg0: int, arg1: int, arg2: int, arg3: int):
        return self.dm.MoveToEx(arg0, arg1, arg2, arg3)

    def MoveWindow(self, arg0: int, arg1: int, arg2: int):
        return self.dm.MoveWindow(arg0, arg1, arg2)

    def Ocr(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: float):
        return self.dm.Ocr(arg0, arg1, arg2, arg3, arg4, arg5)

    def OcrEx(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: float):
        return self.dm.OcrEx(arg0, arg1, arg2, arg3, arg4, arg5)

    def OcrExOne(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: float):
        return self.dm.OcrExOne(arg0, arg1, arg2, arg3, arg4, arg5)

    def OcrInFile(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: str, arg6: float):
        return self.dm.OcrInFile(arg0, arg1, arg2, arg3, arg4, arg5, arg6)

    def OpenProcess(self, arg0: int):
        return self.dm.OpenProcess(arg0)

    def Play(self, arg0: str):
        return self.dm.Play(arg0)

    def RGB2BGR(self, arg0: str):
        return self.dm.RGB2BGR(arg0)

    def ReadData(self, arg0: int, arg1: str, arg2: int):
        return self.dm.ReadData(arg0, arg1, arg2)

    def ReadDataAddr(self, arg0: int, arg1: int, arg2: int):
        return self.dm.ReadDataAddr(arg0, arg1, arg2)

    def ReadDataAddrToBin(self, arg0: int, arg1: int, arg2: int):
        return self.dm.ReadDataAddrToBin(arg0, arg1, arg2)

    def ReadDataToBin(self, arg0: int, arg1: str, arg2: int):
        return self.dm.ReadDataToBin(arg0, arg1, arg2)

    def ReadDouble(self, arg0: int, arg1: str):
        return self.dm.ReadDouble(arg0, arg1)

    def ReadDoubleAddr(self, arg0: int, arg1: int):
        return self.dm.ReadDoubleAddr(arg0, arg1)

    def ReadFile(self, arg0: str):
        return self.dm.ReadFile(arg0)

    def ReadFileData(self, arg0: str, arg1: int, arg2: int):
        return self.dm.ReadFileData(arg0, arg1, arg2)

    def ReadFloat(self, arg0: int, arg1: str):
        return self.dm.ReadFloat(arg0, arg1)

    def ReadFloatAddr(self, arg0: int, arg1: int):
        return self.dm.ReadFloatAddr(arg0, arg1)

    def ReadIni(self, arg0: str, arg1: str, arg2: str):
        return self.dm.ReadIni(arg0, arg1, arg2)

    def ReadIniPwd(self, arg0: str, arg1: str, arg2: str, arg3: str):
        return self.dm.ReadIniPwd(arg0, arg1, arg2, arg3)

    def ReadInt(self, arg0: int, arg1: str, arg2: int):
        return self.dm.ReadInt(arg0, arg1, arg2)

    def ReadIntAddr(self, arg0: int, arg1: int, arg2: int):
        return self.dm.ReadIntAddr(arg0, arg1, arg2)

    def ReadString(self, arg0: int, arg1: str, arg2: int, arg3: int):
        return self.dm.ReadString(arg0, arg1, arg2, arg3)

    def ReadStringAddr(self, arg0: int, arg1: int, arg2: int, arg3: int):
        return self.dm.ReadStringAddr(arg0, arg1, arg2, arg3)

    def Reg(self, arg0: str, arg1: str):
        return self.dm.Reg(arg0, arg1)

    def RegEx(self, arg0: str, arg1: str, arg2: str):
        return self.dm.RegEx(arg0, arg1, arg2)

    def RegExNoMac(self, arg0: str, arg1: str, arg2: str):
        return self.dm.RegExNoMac(arg0, arg1, arg2)

    def RegNoMac(self, arg0: str, arg1: str):
        return self.dm.RegNoMac(arg0, arg1)

    def ReleaseRef(self):
        return self.dm.ReleaseRef()

    def RightClick(self):
        return self.dm.RightClick()

    def RightDown(self):
        return self.dm.RightDown()

    def RightUp(self):
        return self.dm.RightUp()

    def RunApp(self, arg0: str, arg1: int):
        return self.dm.RunApp(arg0, arg1)

    def SaveDict(self, arg0: int, arg1: str):
        return self.dm.SaveDict(arg0, arg1)

    def SelectDirectory(self):
        return self.dm.SelectDirectory()

    def SelectFile(self):
        return self.dm.SelectFile()

    def SendCommand(self, arg0: str):
        return self.dm.SendCommand(arg0)

    def SendPaste(self, arg0: int):
        return self.dm.SendPaste(arg0)

    def SendString(self, arg0: int, arg1: str):
        return self.dm.SendString(arg0, arg1)

    def SendString2(self, arg0: int, arg1: str):
        return self.dm.SendString2(arg0, arg1)

    def SendStringIme(self, arg0: str):
        return self.dm.SendStringIme(arg0)

    def SendStringIme2(self, arg0: int, arg1: str, arg2: int):
        return self.dm.SendStringIme2(arg0, arg1, arg2)

    def SetAero(self, arg0: int):
        return self.dm.SetAero(arg0)

    def SetClientSize(self, arg0: int, arg1: int, arg2: int):
        return self.dm.SetClientSize(arg0, arg1, arg2)

    def SetClipboard(self, arg0: str):
        return self.dm.SetClipboard(arg0)

    def SetColGapNoDict(self, arg0: int):
        return self.dm.SetColGapNoDict(arg0)

    def SetDict(self, arg0: int, arg1: str):
        return self.dm.SetDict(arg0, arg1)

    def SetDictMem(self, arg0: int, arg1: int, arg2: int):
        return self.dm.SetDictMem(arg0, arg1, arg2)

    def SetDictPwd(self, arg0: str):
        return self.dm.SetDictPwd(arg0)

    def SetDisplayAcceler(self, arg0: int):
        return self.dm.SetDisplayAcceler(arg0)

    def SetDisplayDelay(self, arg0: int):
        return self.dm.SetDisplayDelay(arg0)

    def SetDisplayInput(self, arg0: str):
        return self.dm.SetDisplayInput(arg0)

    def SetDisplayRefreshDelay(self, arg0: int):
        return self.dm.SetDisplayRefreshDelay(arg0)

    def SetEnumWindowDelay(self, arg0: int):
        return self.dm.SetEnumWindowDelay(arg0)

    def SetEnv(self, arg0: int, arg1: str, arg2: str):
        return self.dm.SetEnv(arg0, arg1, arg2)

    def SetExactOcr(self, arg0: int):
        return self.dm.SetExactOcr(arg0)

    def SetExcludeRegion(self, arg0: int, arg1: str):
        return self.dm.SetExcludeRegion(arg0, arg1)

    def SetExitThread(self, arg0: int):
        return self.dm.SetExitThread(arg0)

    def SetExportDict(self, arg0: int, arg1: str):
        return self.dm.SetExportDict(arg0, arg1)

    def SetFindPicMultithreadCount(self, arg0: int):
        return self.dm.SetFindPicMultithreadCount(arg0)

    def SetFindPicMultithreadLimit(self, arg0: int):
        return self.dm.SetFindPicMultithreadLimit(arg0)

    def SetInputDm(self, arg0: int, arg1: int, arg2: int):
        return self.dm.SetInputDm(arg0, arg1, arg2)

    def SetKeypadDelay(self, arg0: str, arg1: int):
        return self.dm.SetKeypadDelay(arg0, arg1)

    def SetLocale(self):
        return self.dm.SetLocale()

    def SetMemoryFindResultToFile(self, arg0: str):
        return self.dm.SetMemoryFindResultToFile(arg0)

    def SetMemoryHwndAsProcessId(self, arg0: int):
        return self.dm.SetMemoryHwndAsProcessId(arg0)

    def SetMinColGap(self, arg0: int):
        return self.dm.SetMinColGap(arg0)

    def SetMinRowGap(self, arg0: int):
        return self.dm.SetMinRowGap(arg0)

    def SetMouseDelay(self, arg0: str, arg1: int):
        return self.dm.SetMouseDelay(arg0, arg1)

    def SetMouseSpeed(self, arg0: int):
        return self.dm.SetMouseSpeed(arg0)

    def SetParam64ToPointer(self):
        return self.dm.SetParam64ToPointer()

    def SetPath(self, arg0: str):
        return self.dm.SetPath(arg0)

    def SetPicPwd(self, arg0: str):
        return self.dm.SetPicPwd(arg0)

    def SetRowGapNoDict(self, arg0: int):
        return self.dm.SetRowGapNoDict(arg0)

    def SetScreen(self, arg0: int, arg1: int, arg2: int):
        return self.dm.SetScreen(arg0, arg1, arg2)

    def SetSendStringDelay(self, arg0: int):
        return self.dm.SetSendStringDelay(arg0)

    def SetShowAsmErrorMsg(self, arg0: int):
        return self.dm.SetShowAsmErrorMsg(arg0)

    def SetShowErrorMsg(self, arg0: int):
        return self.dm.SetShowErrorMsg(arg0)

    def SetSimMode(self, arg0: int):
        return self.dm.SetSimMode(arg0)

    def SetUAC(self, arg0: int):
        return self.dm.SetUAC(arg0)

    def SetWindowSize(self, arg0: int, arg1: int, arg2: int):
        return self.dm.SetWindowSize(arg0, arg1, arg2)

    def SetWindowState(self, arg0: int, arg1: int):
        return self.dm.SetWindowState(arg0, arg1)

    def SetWindowText(self, arg0: int, arg1: str):
        return self.dm.SetWindowText(arg0, arg1)

    def SetWindowTransparent(self, arg0: int, arg1: int):
        return self.dm.SetWindowTransparent(arg0, arg1)

    def SetWordGap(self, arg0: int):
        return self.dm.SetWordGap(arg0)

    def SetWordGapNoDict(self, arg0: int):
        return self.dm.SetWordGapNoDict(arg0)

    def SetWordLineHeight(self, arg0: int):
        return self.dm.SetWordLineHeight(arg0)

    def SetWordLineHeightNoDict(self, arg0: int):
        return self.dm.SetWordLineHeightNoDict(arg0)

    def ShowScrMsg(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: str, arg5: str):
        return self.dm.ShowScrMsg(arg0, arg1, arg2, arg3, arg4, arg5)

    def ShowTaskBarIcon(self, arg0: int, arg1: int):
        return self.dm.ShowTaskBarIcon(arg0, arg1)

    def SortPosDistance(self, arg0: str, arg1: int, arg2: int, arg3: int):
        return self.dm.SortPosDistance(arg0, arg1, arg2, arg3)

    def SpeedNormalGraphic(self, arg0: int):
        return self.dm.SpeedNormalGraphic(arg0)

    def Stop(self, arg0: int):
        return self.dm.Stop(arg0)

    def StrStr(self, arg0: str, arg1: str):
        return self.dm.StrStr(arg0, arg1)

    def StringToData(self, arg0: str, arg1: int):
        return self.dm.StringToData(arg0, arg1)

    def SwitchBindWindow(self, arg0: int):
        return self.dm.SwitchBindWindow(arg0)

    def TerminateProcess(self, arg0: int):
        return self.dm.TerminateProcess(arg0)

    def TerminateProcessTree(self, arg0: int):
        return self.dm.TerminateProcessTree(arg0)

    def UnBindWindow(self):
        return self.dm.UnBindWindow()

    def UnLoadDriver(self):
        return self.dm.UnLoadDriver()

    def UseDict(self, arg0: int):
        return self.dm.UseDict(arg0)

    def Ver(self):
        return self.dm.Ver()

    def VirtualAllocEx(self, arg0: int, arg1: int, arg2: int, arg3: int):
        return self.dm.VirtualAllocEx(arg0, arg1, arg2, arg3)

    def VirtualFreeEx(self, arg0: int, arg1: int):
        return self.dm.VirtualFreeEx(arg0, arg1)

    def VirtualProtectEx(self, arg0: int, arg1: int, arg2: int, arg3: int, arg4: int):
        return self.dm.VirtualProtectEx(arg0, arg1, arg2, arg3, arg4)

    def VirtualQueryEx(self, arg0: int, arg1: int, arg2: int):
        return self.dm.VirtualQueryEx(arg0, arg1, arg2)

    def WaitKey(self, arg0: int, arg1: int):
        return self.dm.WaitKey(arg0, arg1)

    def WheelDown(self):
        return self.dm.WheelDown()

    def WheelUp(self):
        return self.dm.WheelUp()

    def WriteData(self, arg0: int, arg1: str, arg2: str):
        return self.dm.WriteData(arg0, arg1, arg2)

    def WriteDataAddr(self, arg0: int, arg1: int, arg2: str):
        return self.dm.WriteDataAddr(arg0, arg1, arg2)

    def WriteDataAddrFromBin(self, arg0: int, arg1: int, arg2: int, arg3: int):
        return self.dm.WriteDataAddrFromBin(arg0, arg1, arg2, arg3)

    def WriteDataFromBin(self, arg0: int, arg1: str, arg2: int, arg3: int):
        return self.dm.WriteDataFromBin(arg0, arg1, arg2, arg3)

    def WriteDouble(self, arg0: int, arg1: str, arg2: float):
        return self.dm.WriteDouble(arg0, arg1, arg2)

    def WriteDoubleAddr(self, arg0: int, arg1: int, arg2: float):
        return self.dm.WriteDoubleAddr(arg0, arg1, arg2)

    def WriteFile(self, arg0: str, arg1: str):
        return self.dm.WriteFile(arg0, arg1)

    def WriteFloat(self, arg0: int, arg1: str, arg2: str):
        return self.dm.WriteFloat(arg0, arg1, arg2)

    def WriteFloatAddr(self, arg0: int, arg1: int, arg2: str):
        return self.dm.WriteFloatAddr(arg0, arg1, arg2)

    def WriteIni(self, arg0: str, arg1: str, arg2: str, arg3: str):
        return self.dm.WriteIni(arg0, arg1, arg2, arg3)

    def WriteIniPwd(self, arg0: str, arg1: str, arg2: str, arg3: str, arg4: str):
        return self.dm.WriteIniPwd(arg0, arg1, arg2, arg3, arg4)

    def WriteInt(self, arg0: int, arg1: str, arg2: int, arg3: int):
        return self.dm.WriteInt(arg0, arg1, arg2, arg3)

    def WriteIntAddr(self, arg0: int, arg1: int, arg2: int, arg3: int):
        return self.dm.WriteIntAddr(arg0, arg1, arg2, arg3)

    def WriteString(self, arg0: int, arg1: str, arg2: int, arg3: str):
        return self.dm.WriteString(arg0, arg1, arg2, arg3)

    def WriteStringAddr(self, arg0: int, arg1: int, arg2: int, arg3: str):
        return self.dm.WriteStringAddr(arg0, arg1, arg2, arg3)

    def delay(self, arg0: int):
        return self.dm.delay(arg0)

# 测试代码
if __name__ == "__main__":
    dm_user = "jv965720b239b8396b1b7df8b768c919e86e10f"
    dm_pass = "jvt7apmy39b8700"
    dm = DM(dm_user, dm_pass)

