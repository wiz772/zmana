import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import sys
import time

class Service(win32serviceutil.ServiceFramework):
    _svc_name_ = 'Zmana'
    _svc_display_name_ = 'Zmana Service'
    _svc_start_type_ =  win32service.SERVICE_AUTO_START

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(120)
        self.is_alive = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_alive = False

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        try:
            self.main()
        except Exception as e:
            servicemanager.LogErrorMsg(f"Zmana error: {e}")
            self.SvcStop()

    def main(self):
        # Main service logic goes here
        servicemanager.LogInfoMsg("Zmana: main entered")
        while self.is_alive:
            
            # Perform your service tasks here
            time.sleep(5)  # Example: Sleep for 5 seconds

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(Service)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(Service)