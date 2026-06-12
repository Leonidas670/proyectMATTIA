' MATT — Lanzador con permisos de Administrador
' Auto-eleva vía UAC si no tiene privilegios de admin
Option Explicit

Function IsAdmin()
    On Error Resume Next
    Dim shell
    Set shell = CreateObject("WScript.Shell")
    shell.RegRead "HKEY_USERS\S-1-5-19\Environment\TEMP"
    If Err.Number = 0 Then
        IsAdmin = True
    Else
        IsAdmin = False
    End If
    Err.Clear
    On Error GoTo 0
    Set shell = Nothing
End Function

If Not IsAdmin() Then
    Dim objShell
    Set objShell = CreateObject("Shell.Application")
    objShell.ShellExecute "wscript.exe", Chr(34) & WScript.ScriptFullName & Chr(34), "", "runas", 0
    Set objShell = Nothing
    WScript.Quit 0
End If

Dim ws, fso, d, py, cmd
Set ws  = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
d = Left(WScript.ScriptFullName, InStrRev(WScript.ScriptFullName, "\"))

ws.CurrentDirectory = d

py = d & ".venv\Scripts\pythonw.exe"
If Not fso.FileExists(py) Then
    py = d & ".venv\Scripts\python.exe"
End If
If Not fso.FileExists(py) Then
    MsgBox "MATT: ejecuta el archivo Instalar_MATT.bat primero para configurar el entorno.", 16, "MATT"
    WScript.Quit 1
End If

cmd = Chr(34) & py & Chr(34) & " " & Chr(34) & d & "main.py" & Chr(34)
ws.Run cmd, 1, False
Set ws  = Nothing
Set fso = Nothing
