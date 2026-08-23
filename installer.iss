[Setup]
AppName=FixBug-core
AppVersion=1.0.0
AppPublisher="Bharathikannan R"
DefaultDirName={autopf}\fixbug-core
DisableProgramGroupPage=yes
OutputDir=Output
OutputBaseFilename=FixBug_core_Installer
Compression=lzma
SolidCompression=yes
; Required to immediately refresh the terminal environment variables after installation
ChangesEnvironment=yes
SetupIconFile=assets\fixbug.ico
UninstallDisplayIcon={app}\fbcore.exe

; Ensure installer installs to native Program Files (64-bit) and only runs on 64-bit machines.
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

[Files]
Source: "dist\fbcore\fbcore.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\fbcore\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Registry]
Root: HKLM; Subkey: "System\CurrentControlSet\Control\Session Manager\Environment"; ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{app}"; Check: NeedsAddPath(ExpandConstant('{app}'))

[Code]
function NeedsAddPath(Param: string): boolean;
var
  OrigPath: string;
begin
  if not RegQueryStringValue(HKEY_CURRENT_USER, 'Environment', 'Path', OrigPath)
  then begin
    Result := True;
    exit;
  end;
  { Prevent duplicating the PATH entry if the user reinstalls or updates }
  Result := Pos(';' + Param + ';', ';' + OrigPath + ';') = 0;
end;
