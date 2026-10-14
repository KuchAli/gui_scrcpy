[Setup]
AppName=GUI Scrcpy
AppVersion=1.0
AppPublisher=Mister K
DefaultDirName={autopf}\GUI Scrcpy
DefaultGroupName=GUI Scrcpy
OutputBaseFilename=GUIScrcpy_Setup_1.0
Compression=lzma2
SolidCompression=yes
SetupIconFile=assets\icons\logos.ico
UninstallDisplayIcon={app}\GUIScrcpy.exe
PrivilegesRequired=lowest

[Files]
Source: "dist\GUIScrcpy\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion

[Icons]
Name: "{group}\GUI Scrcpy"; Filename: "{app}\GUIScrcpy.exe"
Name: "{autodesktop}\GUI Scrcpy"; Filename: "{app}\GUIScrcpy.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Buat shortcut di Desktop"

[Run]
Filename: "{app}\GUIScrcpy.exe"; Description: "Jalankan GUI Scrcpy"; Flags: nowait postinstall skipifsilent