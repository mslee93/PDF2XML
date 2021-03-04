@echo off
@tasklist | find "nginx.exe" /c > NUL

IF %ErrorLevel%==1 goto 2
IF NOT %ErrorLevel%==1 goto 0

:0
taskkill /f /im nginx.exe
goto 2

:repeat
Timeout 10 > NUL

@tasklist | find "nginx.exe" /c > NUL
IF %ErrorLevel%==1 goto 2
IF NOT %ErrorLevel%==1 goto 1

:1
goto repeat

:2
cd C:\nginx-1.17.10\
start nginx
goto repeat