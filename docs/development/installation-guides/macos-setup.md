# macOS Development Environment Setup

## Prerequisites

- macOS 12 (Monterey) or higher
- Administrator access for software installation
- Stable internet connection
- Apple ID for App Store downloads (optional)

## Step 1: Install Xcode Command Line Tools

```bash
# Install Xcode Command Line Tools
xcode-select --install

# Verify installation
xcode-select -p
gcc --version
```

## Step 2: Install Homebrew Package Manager

```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Add Homebrew to PATH (for Apple Silicon Macs)
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"

# For Intel Macs, Homebrew installs to /usr/local/bin (usually already in PATH)

# Verify installation
brew --version
```

## Step 3: Install Core Development Tools

### Essential Tools
```bash
# Git (latest version)
brew install git

# Docker Desktop
brew install --cask docker

# Python 3.12
brew install python@3.12

# OpenJDK 21
brew install openjdk@21

# Node.js 18 LTS
brew install node@18

# Visual Studio Code
brew install --cask visual-studio-code

# Additional utilities
brew install curl
brew install jq
brew install wget
brew install tree
```

### Optional but Recommended Tools
```bash
# Database tools
brew install postgresql@15
brew install redis

# Development utilities
brew install htop
brew install watch
brew install gnu-sed
brew install gnu-tar

# Container tools
brew install kubectl
brew install helm
```

## Step 4: Configure Development Environment

### Configure Git
```bash
# Set global Git configuration
git config --global user.name "Your Name"
git config --global user.email "your.email@company.com"

# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@company.com"

# Add SSH key to ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Copy public key to clipboard
pbcopy < ~/.ssh/id_ed25519.pub
echo "SSH public key copied to clipboard. Add it to your Git provider."
```

### Configure Python
```bash
# Create symlink for python3.12 (if needed)
ln -sf /opt/homebrew/bin/python3.12 /opt/homebrew/bin/python3
ln -sf /opt/homebrew/bin/python3.12 /opt/homebrew/bin/python

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zprofile
source ~/.zprofile

# Configure Poetry
poetry config virtualenvs.in-project true

# Verify Python installation
python3 --version
poetry --version
```

### Configure Java
```bash
# Set JAVA_HOME for OpenJDK 21
echo 'export JAVA_HOME="/opt/homebrew/opt/openjdk@21"' >> ~/.zprofile
echo 'export PATH="/opt/homebrew/opt/openjdk@21/bin:$PATH"' >> ~/.zprofile
source ~/.zprofile

# Install Maven
brew install maven

# Verify Java installation
java -version
javac -version
mvn -version
```

### Configure Node.js
```bash
# Use Node.js 18 LTS
echo 'export PATH="/opt/homebrew/opt/node@18/bin:$PATH"' >> ~/.zprofile
source ~/.zprofile

# Install global packages
npm install -g typescript@5.2.2
npm install -g @types/node@20.8.0
npm install -g prettier@3.0.3
npm install -g eslint@8.51.0
npm install -g create-react-app@5.0.1

# Verify Node.js installation
node --version
npm --version
```

## Step 5: Configure Docker Desktop

1. Launch Docker Desktop from Applications
2. Complete the initial setup wizard
3. Go to Docker Desktop → Preferences:

### General Settings
- Enable "Use Docker Compose V2"
- Enable "Send usage statistics" (optional)

### Resources Settings
- **CPUs**: 4 minimum (8 recommended)
- **Memory**: 8GB minimum (16GB recommended)
- **Swap**: 2GB
- **Disk image size**: 100GB minimum

### Advanced Settings
- Enable "Use Rosetta for x86/amd64 emulation on Apple Silicon" (Apple Silicon Macs only)

4. Apply & Restart Docker Desktop

## Step 6: Install VS Code Extensions

```bash
# Install VS Code extensions
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

## Step 7: Configure Shell Environment

### For Zsh (default on macOS Monterey+)
```bash
# Create or update ~/.zshrc
cat >> ~/.zshrc << 'EOF'
# Homebrew
eval "$(/opt/homebrew/bin/brew shellenv)"

# Python
export PATH="$HOME/.local/bin:$PATH"

# Java
export JAVA_HOME="/opt/homebrew/opt/openjdk@21"
export PATH="/opt/homebrew/opt/openjdk@21/bin:$PATH"

# Node.js
export PATH="/opt/homebrew/opt/node@18/bin:$PATH"

# Development aliases
alias ll='ls -la'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'

# Docker aliases
alias dps='docker ps'
alias dpa='docker ps -a'
alias di='docker images'
alias dcu='docker-compose up'
alias dcd='docker-compose down'

# Git aliases
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git log --oneline'
EOF

# Reload shell configuration
source ~/.zshrc
```

### For Bash (if using bash)
```bash
# Create or update ~/.bash_profile
cat >> ~/.bash_profile << 'EOF'
# Homebrew
eval "$(/opt/homebrew/bin/brew shellenv)"

# Python
export PATH="$HOME/.local/bin:$PATH"

# Java
export JAVA_HOME="/opt/homebrew/opt/openjdk@21"
export PATH="/opt/homebrew/opt/openjdk@21/bin:$PATH"

# Node.js
export PATH="/opt/homebrew/opt/node@18/bin:$PATH"
EOF

source ~/.bash_profile
```

## Step 8: Verify Installation

### Check Software Versions
```bash
# Core tools
docker --version
docker-compose --version
git --version
python3 --version
java -version
node --version
npm --version
code --version

# Package managers
brew --version
poetry --version
mvn --version

# System info
uname -a
sw_vers
```

### Test Docker
```bash
# Test Docker installation
docker run hello-world

# Test Docker Compose
docker-compose --version

# Check Docker system info
docker system info
```

### Test Development Tools
```bash
# Test Python
python3 -c "import sys; print(f'Python {sys.version}')"

# Test Java
java -version

# Test Node.js
node -e "console.log('Node.js version:', process.version)"

# Test Git
git --version
```

## Step 9: macOS-Specific Optimizations

### Configure System Preferences

#### Security & Privacy
- Allow Docker Desktop in "Privacy & Security" → "Full Disk Access"
- Allow Terminal/iTerm2 in "Privacy & Security" → "Developer Tools"

#### Performance Optimizations
```bash
# Increase file descriptor limits
echo 'ulimit -n 65536' >> ~/.zshrc

# Disable Spotlight indexing for development directories (optional)
sudo mdutil -i off ~/dev
```

### Configure Finder
```bash
# Show hidden files
defaults write com.apple.finder AppleShowAllFiles YES
killall Finder

# Show file extensions
defaults write NSGlobalDomain AppleShowAllExtensions -bool true
killall Finder
```

## Troubleshooting

### Common Issues and Solutions

#### Homebrew Installation Issues
```bash
# Fix Homebrew permissions
sudo chown -R $(whoami) /opt/homebrew/*

# Update Homebrew
brew update
brew doctor
```

#### Docker Desktop Issues
- Ensure sufficient disk space (100GB+ recommended)
- Reset Docker Desktop: Docker → Troubleshoot → Reset to factory defaults
- Check Activity Monitor for resource usage

#### Python Path Issues
```bash
# Check Python installation
which python3
python3 --version

# Fix Poetry PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zprofile
source ~/.zprofile
```

#### Java Version Issues
```bash
# List installed Java versions
/usr/libexec/java_home -V

# Switch Java versions
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
```

#### Permission Issues
```bash
# Fix npm permissions
sudo chown -R $(whoami) ~/.npm

# Fix Docker permissions
sudo dscl . append /Groups/staff GroupMembership $(whoami)
```

#### Apple Silicon Compatibility
- Use Rosetta 2 for x86 Docker images: `docker run --platform linux/amd64 image_name`
- Install x86 versions of tools if needed: `arch -x86_64 brew install package_name`

### Performance Tips
- Use SSD for Docker data directory
- Increase Docker resource allocation based on available system resources
- Close unnecessary applications during development
- Use `brew cleanup` regularly to free disk space

## Next Steps

1. Clone the project repository
2. Run the automated setup script
3. Follow the development workflow documentation
4. Set up IDE configurations
5. Run environment validation tests

## Additional Resources

- [Homebrew Documentation](https://docs.brew.sh/)
- [Docker Desktop for Mac](https://docs.docker.com/desktop/mac/)
- [macOS Development Setup Guide](https://sourabhbajaj.com/mac-setup/)
- [Oh My Zsh](https://ohmyz.sh/) for enhanced shell experience