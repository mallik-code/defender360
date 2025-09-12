# Windows Development Environment Setup

## Prerequisites

- Windows 10 version 2004 or higher, or Windows 11
- Administrator access for software installation
- Stable internet connection

## Step 1: Enable WSL2 and Hyper-V

### Enable WSL2
1. Open PowerShell as Administrator
2. Run the following commands:
```powershell
# Enable WSL and Virtual Machine Platform
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Restart computer
Restart-Computer
```

3. After restart, download and install the WSL2 Linux kernel update:
   - Download from: https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi
   - Run the installer

4. Set WSL2 as default:
```powershell
wsl --set-default-version 2
```

5. Install Ubuntu 22.04 LTS:
```powershell
wsl --install -d Ubuntu-22.04
```

### Enable Hyper-V (if not already enabled)
```powershell
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All
```

## Step 2: Install Package Manager

### Install Chocolatey
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

### Alternative: Install winget (Windows 11 or Windows 10 with App Installer)
```powershell
# winget is pre-installed on Windows 11
# For Windows 10, install from Microsoft Store: "App Installer"
```

## Step 3: Install Core Development Tools

### Using Chocolatey
```powershell
# Git
choco install git -y

# Docker Desktop
choco install docker-desktop -y

# Python 3.12
choco install python312 -y

# OpenJDK 21
choco install openjdk21 -y

# Node.js 18 LTS
choco install nodejs-lts -y

# Visual Studio Code
choco install vscode -y

# Additional tools
choco install 7zip -y
choco install curl -y
choco install jq -y
```

### Using winget (Alternative)
```powershell
# Git
winget install Git.Git

# Docker Desktop
winget install Docker.DockerDesktop

# Python 3.12
winget install Python.Python.3.12

# OpenJDK 21
winget install EclipseAdoptium.Temurin.21.JDK

# Node.js 18 LTS
winget install OpenJS.NodeJS.LTS

# Visual Studio Code
winget install Microsoft.VisualStudioCode

# Additional tools
winget install 7zip.7zip
winget install cURL.cURL
winget install jqlang.jq
```

## Step 4: Configure Development Environment

### Configure Git
```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@company.com"

# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@company.com"

# Add SSH key to ssh-agent
Get-Service ssh-agent | Set-Service -StartupType Automatic
Start-Service ssh-agent
ssh-add ~/.ssh/id_ed25519
```

### Configure Python
```powershell
# Install Poetry
pip install poetry==1.7.1

# Configure Poetry
poetry config virtualenvs.in-project true
```

### Configure Java
```powershell
# Set JAVA_HOME environment variable
[Environment]::SetEnvironmentVariable("JAVA_HOME", "C:\Program Files\Eclipse Adoptium\jdk-21.0.1.12-hotspot", "Machine")

# Install Maven
choco install maven -y
```

### Configure Node.js
```powershell
# Install global packages
npm install -g typescript@5.2.2
npm install -g @types/node@20.8.0
npm install -g prettier@3.0.3
npm install -g eslint@8.51.0
```

## Step 5: Configure Docker Desktop

1. Launch Docker Desktop
2. Go to Settings → General:
   - Enable "Use WSL 2 based engine"
   - Enable "Add the *.docker.internal names to the host's /etc/hosts file"

3. Go to Settings → Resources → WSL Integration:
   - Enable integration with default WSL distro
   - Enable integration with Ubuntu-22.04

4. Go to Settings → Resources → Advanced:
   - Set Memory to 8GB minimum (16GB recommended)
   - Set CPUs to 4 minimum (8 recommended)
   - Set Disk image size to 100GB minimum

5. Apply & Restart Docker Desktop

## Step 6: Install VS Code Extensions

```powershell
# Install VS Code extensions via command line
code --install-extension ms-python.python
code --install-extension vscjava.vscode-java-pack
code --install-extension ms-vscode.vscode-typescript-next
code --install-extension ms-azuretools.vscode-docker
code --install-extension ms-kubernetes-tools.vscode-kubernetes-tools
code --install-extension eamodio.gitlens
code --install-extension esbenp.prettier-vscode
code --install-extension dbaeumer.vscode-eslint
code --install-extension njpwerner.autodocstring
code --install-extension humao.rest-client
```

## Step 7: Verify Installation

### Check Software Versions
```powershell
# Check versions
docker --version
docker-compose --version
git --version
python --version
java -version
node --version
npm --version
code --version

# Check WSL
wsl --list --verbose
```

### Test Docker
```powershell
# Test Docker installation
docker run hello-world

# Test Docker Compose
docker-compose --version
```

## Step 8: Configure Windows-Specific Settings

### Configure Windows Defender Exclusions
```powershell
# Add exclusions for development directories (run as Administrator)
Add-MpPreference -ExclusionPath "C:\Users\$env:USERNAME\dev"
Add-MpPreference -ExclusionPath "C:\Users\$env:USERNAME\.docker"
Add-MpPreference -ExclusionPath "C:\ProgramData\Docker"
```

### Configure PowerShell Execution Policy
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Configure Environment Variables
```powershell
# Add to PATH if not automatically added
$env:PATH += ";C:\Program Files\Docker\Docker\resources\bin"
$env:PATH += ";C:\Program Files\Git\bin"

# Make permanent
[Environment]::SetEnvironmentVariable("PATH", $env:PATH, "User")
```

## Troubleshooting

### Common Issues and Solutions

#### Docker Desktop Won't Start
- Ensure Hyper-V and WSL2 are properly enabled
- Check Windows version compatibility
- Restart Windows after enabling features
- Run Docker Desktop as Administrator

#### WSL2 Integration Issues
```powershell
# Reset WSL2 if needed
wsl --shutdown
wsl --unregister Ubuntu-22.04
wsl --install -d Ubuntu-22.04
```

#### Port Conflicts
```powershell
# Check what's using a port
netstat -ano | findstr :8080

# Kill process by PID
taskkill /PID <PID> /F
```

#### Permission Issues
- Run PowerShell as Administrator for system-level changes
- Ensure user is in "docker-users" group
- Check WSL2 file permissions

#### Performance Issues
- Increase Docker Desktop resource allocation
- Move Docker data to SSD if possible
- Exclude development directories from Windows Defender

### Getting Help
- Docker Desktop: Check Docker Desktop logs in Settings → Troubleshoot
- WSL2: Run `wsl --status` and `wsl --list --verbose`
- Windows Event Viewer: Check for system errors
- PowerShell: Use `Get-Help` for command assistance

## Next Steps

1. Clone the project repository
2. Run the automated setup script
3. Follow the development workflow documentation
4. Set up IDE configurations
5. Run environment validation tests