$pythonPath = "D:\DevEnv\Python\python.exe"
$projectPath = "E:\Python\DW_MecKey\extract"
$scriptPath = "$projectPath\main.py"

Set-Location $projectPath

$schedules = @(
    @{Name = "RunAkko_Extract"; Param = "--auto -pn akko_extract"; Time = "08:22AM" },
    @{Name = "RunCps_Extract"; Param = "--auto -pn cps_extract"; Time = "08:27AM" }
)

foreach ($schedule in $schedules) {
    try {
        $action = New-ScheduledTaskAction -Execute "powershell.exe" `
            -Argument "-NoProfile -ExecutionPolicy Bypass -Command `"Set-Location '$projectPath'; & '$pythonPath' '$scriptPath' $($schedule.Param)`""
        $trigger = New-ScheduledTaskTrigger -Daily -At $schedule.Time

        $existingTask = Get-ScheduledTask -TaskName $schedule.Name -ErrorAction SilentlyContinue
        if ($existingTask) {
            Unregister-ScheduledTask -TaskName $schedule.Name -Confirm:$false
        }

        $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries

        Register-ScheduledTask -TaskName $schedule.Name -Action $action -Trigger $trigger -Settings $settings
    }
    catch {
        Write-Error "Failed to create task $($schedule.Name): $_"
    }
}