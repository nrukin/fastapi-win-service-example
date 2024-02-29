import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
from main import Server
import asyncio
import sys


class AppServerSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "uuidGenerator"
    _svc_display_name_ = "UUID generator"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.svc = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        if self.svc is not None:
            self.svc.stop()
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.svc = Server(True)
        self.svc.start()


def init():
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(AppServerSvc)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(AppServerSvc)


if __name__ == '__main__':
    init()
