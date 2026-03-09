[Setup]
AppName=Media Export
AppVersion=1.0
DefaultDirName={pf}\MediaExport
DefaultGroupName=Media Export
OutputDir=installer
OutputBaseFilename=MediaExportSetup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "dist\MediaExport\*"; DestDir: "{app}"; Flags: recursesubdirs

[Icons]
Name: "{group}\Media Export"; Filename: "{app}\MediaExport.exe"
Name: "{autodesktop}\Media Export"; Filename: "{app}\MediaExport.exe"

[Run]
Filename: "{app}\MediaExport.exe"; Description: "Launch Media Export"; Flags: nowait postinstall skipifsilent