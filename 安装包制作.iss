; 脚本由 Inno Setup 脚本向导 生成！
; 有关创建 Inno Setup 脚本文件的详细资料请查阅帮助文档！

#define MyAppName "Screenshot2code"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "翎雨"
#define MyAppExeName "Screenshot2code.exe"

[Setup]
; 注: AppId的值为单独标识该应用程序。
; 不要为其他安装程序使用相同的AppId值。
; (生成新的GUID，点击 工具|在IDE中生成GUID。)
AppId={{B2F9A9D7-D460-4F67-B56C-D4F8812A62E2}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=C:\Users\86188\PycharmProjects\screenshot2code\用户协议.txt
InfoBeforeFile=C:\Users\86188\PycharmProjects\screenshot2code\安装信息.txt
InfoAfterFile=C:\Users\86188\PycharmProjects\screenshot2code\更新日志.txt
OutputDir=C:\Users\86188\PycharmProjects\screenshot2code\packages
OutputBaseFilename=Screenshot2code-setup-1.0.0
SetupIconFile=C:\Users\86188\PycharmProjects\screenshot2code\favicon.ico
Compression=lzma
SolidCompression=yes

[UninstallDelete]
Name: {app}; Type: filesandordirs; Languages:

[Languages]
Name: "chinesesimp"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkablealone; OnlyBelowVersion: 0,6.3

[Files]
Source: "C:\Users\86188\PycharmProjects\screenshot2code\Screenshot2code\Screenshot2code.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\86188\PycharmProjects\screenshot2code\Screenshot2code\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; 注意: 不要在任何共享系统文件上使用“Flags: ignoreversion”

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

