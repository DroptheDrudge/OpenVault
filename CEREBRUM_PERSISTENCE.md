# CEREBRUM Persistence — Always-On Brain

Make the CEREBRUM brain restart automatically after crashes and system reboots.

---

## Option 1: Windows Service (Recommended for Production)

### Step 1: Create Service Wrapper

Create `cerebrum_service.py`:

```python
#!/usr/bin/env python3
"""
CEREBRUM Windows Service
Auto-starts on boot, restarts on crash
"""

import win32serviceutil
import win32service
import win32event
import servicemanager
import subprocess
import sys
import os
import time
import signal

class CerebrumService(win32serviceutil.ServiceFramework):
    _svc_name_ = "CerebrumBrain"
    _svc_display_name_ = "CEREBRUM Capital Allocator"
    _svc_description_ = "Meta-cognitive capital allocation brain with consciousness layer"
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.process = None
        
    def SvcStop(self):
        """Called when service is stopped"""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        
        # Graceful shutdown of CEREBRUM
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=10)
            except:
                self.process.kill()
    
    def SvcDoRun(self):
        """Main service loop"""
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        
        self.main()
    
    def main(self):
        """Keep CEREBRUM running forever"""
        cerebrum_path = r"C:\Kimi_EAs\cerebrum.py"
        
        while True:
            # Check if we should stop
            if win32event.WaitForSingleObject(self.stop_event, 1000) == win32event.WAIT_OBJECT_0:
                break
            
            # Start or restart CEREBRUM
            if self.process is None or self.process.poll() is not None:
                servicemanager.LogInfoMsg("CEREBRUM: Starting brain...")
                
                try:
                    self.process = subprocess.Popen(
                        [sys.executable, cerebrum_path, "--continuous"],
                        cwd=r"C:\Kimi_EAs",
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                    )
                    servicemanager.LogInfoMsg(f"CEREBRUM: Brain started (PID {self.process.pid})")
                except Exception as e:
                    servicemanager.LogErrorMsg(f"CEREBRUM: Failed to start: {e}")
                    time.sleep(5)
                    continue
            
            # Monitor health
            time.sleep(5)
            
            # Check if process died
            if self.process.poll() is not None:
                stdout, stderr = self.process.communicate()
                if stderr:
                    servicemanager.LogErrorMsg(f"CEREBRUM crashed: {stderr.decode()[-500:]}")
                servicemanager.LogWarningMsg("CEREBRUM: Brain stopped, restarting...")
                self.process = None
                time.sleep(2)  # Brief delay before restart

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(CerebrumService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(CerebrumService)
```

### Step 2: Install Service

```powershell
# Install pywin32 if not already
pip install pywin32

# Install the service (run as Administrator)
python cerebrum_service.py install

# Configure to auto-start on boot
sc config CerebrumBrain start= auto

# Start the service
python cerebrum_service.py start
# OR
sc start CerebrumBrain

# Check status
sc query CerebrumBrain
```

### Step 3: Service Commands

```powershell
# Stop
python cerebrum_service.py stop
# OR
sc stop CerebrumBrain

# Restart
sc stop CerebrumBrain && sc start CerebrumBrain

# Remove service
python cerebrum_service.py remove
```

---

## Option 2: Task Scheduler (Simpler)

### Create Scheduled Task

```powershell
# Create task that runs on boot and restarts on failure
$action = New-ScheduledTaskAction -Execute "python.exe" -Argument "C:\Kimi_EAs\cerebrum.py --continuous" -WorkingDirectory "C:\Kimi_EAs"

$trigger = New-ScheduledTaskTrigger -AtStartup

$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable:$false -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1)

$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest

Register-ScheduledTask -TaskName "CEREBRUM_Brain" -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description "CEREBRUM Capital Allocator - Always On"

# Start now
Start-ScheduledTask -TaskName "CEREBRUM_Brain"

# Check status
Get-ScheduledTask -TaskName "CEREBRUM_Brain" | Get-ScheduledTaskInfo
```

### Remove Task

```powershell
Unregister-ScheduledTask -TaskName "CEREBRUM_Brain" -Confirm:$false
```

---

## Option 3: Python Process Manager (Cross-Platform)

Create `cerebrum_daemon.py`:

```python
#!/usr/bin/env python3
"""
CEREBRUM Daemon - Process manager that keeps brain alive
Run this: python cerebrum_daemon.py
"""

import subprocess
import sys
import time
import signal
import os
from pathlib import Path

CEREBRUM_PATH = Path("C:/Kimi_EAs/cerebrum.py")
RESTART_DELAY = 5  # seconds
MAX_RESTARTS = 10  # per hour
CHECK_INTERVAL = 5  # seconds

class CerebrumDaemon:
    def __init__(self):
        self.process = None
        self.restart_count = 0
        self.last_restart_hour = time.strftime("%H")
        self.running = True
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)
    
    def handle_signal(self, signum, frame):
        print(f"\n🛑 CEREBRUM Daemon: Received signal {signum}, shutting down...")
        self.running = False
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=10)
            except:
                self.process.kill()
    
    def can_restart(self):
        """Rate limit restarts"""
        current_hour = time.strftime("%H")
        if current_hour != self.last_restart_hour:
            self.restart_count = 0
            self.last_restart_hour = current_hour
        
        return self.restart_count < MAX_RESTARTS
    
    def start_cerebrum(self):
        """Start the CEREBRUM brain"""
        print(f"🧠 CEREBRUM Daemon: Starting brain...")
        
        try:
            self.process = subprocess.Popen(
                [sys.executable, str(CEREBRUM_PATH), "--continuous"],
                cwd=CEREBRUM_PATH.parent,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
            )
            print(f"✅ CEREBRUM Daemon: Brain started (PID {self.process.pid})")
            self.restart_count += 1
            return True
            
        except Exception as e:
            print(f"❌ CEREBRUM Daemon: Failed to start: {e}")
            return False
    
    def monitor_output(self):
        """Stream output from CEREBRUM"""
        if self.process and self.process.stdout:
            try:
                line = self.process.stdout.readline()
                if line:
                    print(f"[CEREBRUM] {line.rstrip()}")
                    return True
            except:
                pass
        return False
    
    def run(self):
        """Main daemon loop"""
        print("🚀 CEREBRUM Daemon: Starting...")
        print(f"   Path: {CEREBRUM_PATH}")
        print(f"   Max restarts/hour: {MAX_RESTARTS}")
        print(f"   Check interval: {CHECK_INTERVAL}s")
        print("   Press Ctrl+C to stop\n")
        
        while self.running:
            # Start CEREBRUM if not running
            if self.process is None or self.process.poll() is not None:
                if not self.can_restart():
                    print(f"⚠️  CEREBRUM Daemon: Too many restarts this hour, waiting...")
                    time.sleep(60)
                    continue
                
                exit_code = self.process.poll() if self.process else None
                if exit_code is not None:
                    print(f"⚠️  CEREBRUM Daemon: Brain exited with code {exit_code}")
                
                time.sleep(RESTART_DELAY)
                
                if not self.start_cerebrum():
                    time.sleep(10)
                    continue
            
            # Monitor output
            self.monitor_output()
            
            # Check if still running
            time.sleep(CHECK_INTERVAL)
        
        print("👋 CEREBRUM Daemon: Shutdown complete")

if __name__ == "__main__":
    daemon = CerebrumDaemon()
    daemon.run()
```

### Run Daemon on Startup

**Method A: Create .bat file in Startup folder**

Create `C:\Users\%USERNAME%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\start_cerebrum.bat`:

```batch
@echo off
cd /d C:\Kimi_EAs
start /min pythonw cerebrum_daemon.py
```

**Method B: Task Scheduler (more reliable)**

```powershell
# Create task
$action = New-ScheduledTaskAction -Execute "pythonw.exe" -Argument "C:\Kimi_EAs\cerebrum_daemon.py" -WorkingDirectory "C:\Kimi_EAs"
$trigger = New-ScheduledTaskTrigger -AtStartup
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -Hidden
Register-ScheduledTask -TaskName "CEREBRUM_Daemon" -Action $action -Trigger $trigger -Settings $settings
```

---

## Option 4: NSSM (Non-Sucking Service Manager)

**Best for: Simple, robust Windows service without code**

```powershell
# Download NSSM from https://nssm.cc/download
# Extract nssm.exe to C:\Windows\System32\ or C:\Kimi_EAs\

# Install CEREBRUM as service
nssm install CerebrumBrain "python.exe" "C:\Kimi_EAs\cerebrum.py --continuous"
nssm set CerebrumBrain AppDirectory C:\Kimi_EAs
nssm set CerebrumBrain DisplayName "CEREBRUM Brain"
nssm set CerebrumBrain Description "Meta-cognitive capital allocator"
nssm set CerebrumBrain Start SERVICE_AUTO_START

# Configure restart
nssm set CerebrumBrain AppRestartDelay 5000  # 5 seconds
nssm set CerebrumBrain AppThrottle 60000       # 1 minute between restarts

# Start service
nssm start CerebrumBrain

# Monitor
nssm status CerebrumBrain

# View logs
nssm logs CerebrumBrain
```

---

## Recommended Setup

| Use Case | Recommended Option |
|----------|-------------------|
| **Production trading** | Option 1 (Windows Service) or Option 4 (NSSM) |
| **Development/testing** | Option 3 (Python Daemon) |
| **Quick setup** | Option 2 (Task Scheduler) |
| **Maximum reliability** | Option 4 (NSSM) + Option 3 (as backup) |

---

## Health Monitoring

Add to CEREBRUM to enable health checks:

```python
# In cerebrum.py

def health_check():
    """Return health status for monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "neurons_connected": len(active_neurons),
        "last_allocation": last_allocation_time,
        "uptime_seconds": uptime,
        "memory_mb": get_memory_usage()
    }

# Write heartbeat file every minute
while running:
    # ... main loop ...
    
    if time.time() - last_heartbeat > 60:
        with open("cerebrum_heartbeat.json", "w") as f:
            json.dump(health_check(), f)
        last_heartbeat = time.time()
```

---

## Quick Start (Copy-Paste)

```powershell
# 1. Create daemon
# Save cerebrum_daemon.py to C:\Kimi_EAs\

# 2. Create startup task
$action = New-ScheduledTaskAction -Execute "pythonw.exe" -Argument "C:\Kimi_EAs\cerebrum_daemon.py" -WorkingDirectory "C:\Kimi_EAs"
$trigger = New-ScheduledTaskTrigger -AtStartup
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -Hidden -RestartCount 5 -RestartInterval (New-TimeSpan -Minutes 1)
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount
Register-ScheduledTask -TaskName "CEREBRUM_Daemon" -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Force

# 3. Start now
Start-ScheduledTask -TaskName "CEREBRUM_Daemon"

# 4. Verify
Get-ScheduledTask -TaskName "CEREBRUM_Daemon"
Get-Process -Name python | Where-Object {$_.Path -like "*Kimi_EAs*"}

# 5. Check logs
Get-Content C:\Kimi_EAs\cerebrum.log -Tail 50
```

---

**The CEREBRUM brain will now:**
- ✅ Start automatically on Windows boot
- ✅ Restart if it crashes
- ✅ Rate-limit restarts (max 10/hour)
- ✅ Log all activity
- ✅ Graceful shutdown on system shutdown

**Immortality achieved!** 🧠⚡🔄
