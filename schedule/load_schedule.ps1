$pythonPath = "D:\DevEnv\Python\python.exe"
$projectPath = "E:\Python\DW_MecKey\load"
$scriptPath = "$projectPath\main.py"


$schedules = @(
    @{Name = "RunAkko_Load"; Param = "--auto -pn akko_load"; Time = "09:55AM" },
    @{Name = "RunCps_Load"; Param = "--auto -pn cps_load"; Time = "10:05AM" }
)

foreach ($schedule in $schedules) {
    try {
        # Create the action
        $action = New-ScheduledTaskAction -Execute "powershell.exe" `
            -Argument "-NoProfile -ExecutionPolicy Bypass -Command `"Set-Location '$projectPath'; & '$pythonPath' '$scriptPath' $($schedule.Param)`""
        
        # Create trigger with repetition
        $trigger = New-ScheduledTaskTrigger -Daily -At $schedule.Time
        
        # Create repetition pattern using CimInstance
        $class = Get-CimClass -ClassName MSFT_TaskRepetitionPattern -Namespace Root/Microsoft/Windows/TaskScheduler
        $repetition = New-CimInstance -CimClass $class -ClientOnly
        $repetition.Interval = "PT30M"  # 30 minutes
        $repetition.Duration = "P1D"    # 1 day
        
        # Apply repetition to trigger
        $trigger.Repetition = $repetition

        # Create settings
        $settings = New-ScheduledTaskSettingsSet `
            -AllowStartIfOnBatteries `
            -DontStopIfGoingOnBatteries `
            -StartWhenAvailable `
            -WakeToRun `
            -MultipleInstances IgnoreNew

        # Register task
        Register-ScheduledTask `
            -TaskName $schedule.Name `
            -Action $action `
            -Trigger $trigger `
            -Settings $settings `
            -User $env:USERNAME `
            -Description "Runs process daily with 30-minute intervals" `
            -Force

        Write-Host "Successfully registered task: $($schedule.Name)"
    }
    catch {
        Write-Error "Failed to create task $($schedule.Name): $_"
    }
}