[Setup]
AppName=Eemsik
AppVersion=1.0.0
DefaultDirName={localappdata}\Programs\Eemsik
DefaultGroupName=Eemsik
OutputDir=.
OutputBaseFilename=Eemsik_Instalador
Compression=lzma
SolidCompression=yes
SetupIconFile=assets\Logo.ico
PrivilegesRequired=lowest

[Files]
Source: "dist\Eemsik\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion

[Icons]
Name: "{group}\Eemsik"; Filename: "{app}\Eemsik.exe"
Name: "{userdesktop}\Eemsik"; Filename: "{app}\Eemsik.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Crear acceso directo en el escritorio"; GroupDescription: "Accesos directos:"

[Run]
Filename: "{app}\Eemsik.exe"; Description: "Abrir Eemsik"; Flags: nowait postinstall skipifsilent