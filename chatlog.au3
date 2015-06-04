#include <Constants.au3>

;
; AutoIt Version: 3.0
; Language:       English
; Platform:       Win7
; Author:         Kama
;
; Script Function:
;	append steamchat to logfile
;

Local $iAnswer = MsgBox(BitOR($MB_YESNO, $MB_SYSTEMMODAL), "AutoIt Steamlog", "get current steamchat and append to log.  ok?")
If $iAnswer = 7 Then
	MsgBox($MB_SYSTEMMODAL, "AutoIt", "k bye")
	Exit
EndIf

WinActivate("[CLASS:USurface_38134203]")
MouseClickDrag ( "left", 50, 200, 100, 200, 0)
Send('^a')
Send('^c')
$sData = ClipGet()
FileOpen ( "C:\Users\Pascal\Documents\pastes\steamlog.txt", 1 )
FileWrite ( "C:\Users\Pascal\Documents\pastes\steamlog.txt", $sData & @CRLF )
