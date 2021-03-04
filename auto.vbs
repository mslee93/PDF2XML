Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs1
strArgs1 = "cmd /c nginx.bat"
oShell.Run strArgs1, 0, false
Dim strArgs2
strArgs2 = "cmd /c waitress.bat"
oShell.Run strArgs2, 0, false