@echo off
@tasklist | find "pythonw.exe" /c > NUL

IF %ErrorLevel%==1 goto 2
IF NOT %ErrorLevel%==1 goto 0

:0
taskkill /f /im pythonw.exe
goto 2

:repeat
Timeout 10 > NUL

@tasklist | find "pythonw.exe" /c > NUL
IF %ErrorLevel%==1 goto 2
IF NOT %ErrorLevel%==1 goto 1

:1
goto repeat

:2
pythonw C:\api\server.py
goto repeat