# Linux Development Environment Setup

## Prerequisites

- Linux distribution: Ubuntu 20.04+, CentOS 8+, Fedora 35+, or Debian 11+
- Sudo access for package installation
- Stable internet connection
- Minimum 4GB RAM, 50GB disk space

## Distribution-Specific Instructions

### Ubuntu/Debian Setup

#### Step 1: Update System
```bash
# Update package lists and system
sudo apt update && sudo apt upgrade -y

# Install essential build tools
sudo apt install -y build-essential curl wget git vim tree htop
```

#### Step 2: Install Docker
```bash
# Remove old Docker versions
sudo apt remove -y docker docker-engine docker.io containerd runc

# Install Docker dependencies
sudo apt install -y apt-transport-https ca-certificates gnupg lsb-release

# Add Docker GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add user to docker group
sudo usermod -aG docker $USER

# Enable Docker service
sudo systemctl enable docker
sudo systemctl start docker
```

#### Step 3: Install Python 3.12
```bash
# Add deadsnakes PPA for Python 3.12
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

# Install Python 3.12 and development packages
sudo apt install -y python3.12 python3.12-dev python3.12-venv python3-pip

# Create symlinks
sudo ln -sf /usr/bin/python3.12 /usr/bin/python3
sudo ln -sf /usr/bin/python3.12 /usr/bin/python

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

#### Step 4: Install Java 21
```bash
# Install OpenJDK 21
sudo apt install -y openjdk-21-jdk

# Set JAVA_HOME
echo 'export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64' >> ~/.bashrc
echo 'export PATH=$JAVA_HOME/bin:$PATH' >> ~/.bashrc

# Install Maven
sudo apt install -y maven
```

#### Step 5: Install Node.js 18
```bash
# Install Node.js 18 LTS via NodeSource repository
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install global packages
sudo npm install -g typescript@5.2.2 @types/node@20.8.0 prettier@3.0.3 eslint@8.51.0
```

### CentOS/RHEL/Fedora Setup

#### Step 1: Update System
```bash
# For CentOS/RHEL 8+
sudo dnf update -y
sudo dnf groupinstall -y "Development Tools"
sudo dnf install -y curl wget git vim tree htop

# For Fedora
sudo dnf update -y
sudo dnf groupinstall -y "Development Tools" "Development Libraries"
sudo dnf install -y curl wget git vim tree htop
```

#### Step 2: Install Docker
```bash
# Remove old Docker versions
sudo dnf remove -y docker docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-logrotate docker-engine

# Install Docker repository
sudo dnf install -y dnf-plugins-core
sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# Install Docker Engine
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add user to docker group and start service
sudo usermod -aG docker $USER
sudo systemctl enable docker
sudo systemctl start docker
```

#### Step 3: Install Python 3.12
```bash
# Install Python 3.12 from source (CentOS/RHEL)
sudo dnf install -y gcc openssl-devel bzip2-devel libffi-devel zlib-devel

# Download and compile Python 3.12
cd /tmp
wget https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tgz
tar xzf Python-3.12.0.tgz
cd Python-3.12.0
./configure --enable-optimizations
make -j $(nproc)
sudo make altinstall

# Create symlinks
sudo ln -sf /usr/local/bin/python3.12 /usr/local/bin/python3
sudo ln -sf /usr/local/bin/python3.12 /usr/local/bin/python

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

#### Step 4: Install Java 21
```bash
# Install OpenJDK 21
sudo dnf install -y java-21-openjdk java-21-openjdk-devel

# Set JAVA_HOME
echo 'export JAVA_HOME=/usr/lib/jvm/java-21-openjdk' >> ~/.bashrc
echo 'export PATH=$JAVA_HOME/bin:$PATH' >> ~/.bashrc

# Install Maven
sudo dnf install -y maven
```

#### Step 5: Install Node.js 18
```bash
# Install Node.js 18 LTS
curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
sudo dnf install -y nodejs

# Install global packages
sudo npm install -g typescript@5.2.2 @types/node@20.8.0 prettier@3.0.3 eslint@8.51.0
```

## Common Configuration (All Distributions)

### Step 6: Configure Git
```bash
# Configure Git
git config --global user.name "Your Name"
git config --global user.email "your.email@company.com"

# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@company.com"

# Add SSH key to ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Display public key
cat ~/.ssh/id_ed25519.pub
echo "Add this SSH key to your Git provider"
```

### Step 7: Install Visual Studio Code
```bash
# Install VS Code (Ubuntu/Debian)
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
sudo apt update
sudo apt install -y code

# Install VS Code (CentOS/RHEL/Fedora)
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
sudo sh -c 'echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/vscode.repo'
sudo dnf check-update
sudo dnf install -y code
```

### Step 8: Install VS Code Extensions
```bash
# Install essential extensions
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

### Step 9: Configure Shell Environment
```bash
# Add environment variables to ~/.bashrc
cat >> ~/.bashrc << 'EOF'

# Development environment
export PATH="$HOME/.local/bin:$PATH"
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64  # Ubuntu/Debian
# export JAVA_HOME=/usr/lib/jvm/java-21-openjdk      # CentOS/RHEL/Fedora
export PATH=$JAVA_HOME/bin:$PATH

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

# Python aliases
alias py='python3'
alias pip='pip3'
EOF

# Reload shell configuration
source ~/.bashrc
```

### Step 10: Install Additional Development Tools
```bash
# Install Kubernetes tools
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Install Helm
curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt update && sudo apt install -y helm  # Ubuntu/Debian

# For CentOS/RHEL/Fedora
# curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
# chmod 700 get_helm.sh && ./get_helm.sh

# Install jq
sudo apt install -y jq  # Ubuntu/Debian
# sudo dnf install -y jq  # CentOS/RHEL/Fedora
```

## Step 11: Configure System Limits and Performance

### Increase File Descriptor Limits
```bash
# Add to /etc/security/limits.conf
echo "* soft nofile 65536" | sudo tee -a /etc/security/limits.conf
echo "* hard nofile 65536" | sudo tee -a /etc/security/limits.conf

# Add to current session
echo 'ulimit -n 65536' >> ~/.bashrc
```

### Configure Docker for Performance
```bash
# Create Docker daemon configuration
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json > /dev/null <<EOF
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "storage-driver": "overlay2",
  "storage-opts": [
    "overlay2.override_kernel_check=true"
  ]
}
EOF

# Restart Docker
sudo systemctl restart docker
```

## Step 12: Verify Installation

### Check Software Versions
```bash
# Core tools
docker --version
docker compose version
git --version
python3 --version
java -version
node --version
npm --version

# Package managers
poetry --version
mvn --version

# System info
uname -a
lsb_release -a  # Ubuntu/Debian
cat /etc/redhat-release  # CentOS/RHEL
cat /etc/fedora-release  # Fedora
```

### Test Docker
```bash
# Test Docker installation (logout and login first to apply group membership)
docker run hello-world

# Test Docker Compose
docker compose version

# Check Docker system info
docker system info
```

### Test Development Tools
```bash
# Test Python
python3 -c "import sys; print(f'Python {sys.version}')"

# Test Java
java -version
javac -version

# Test Node.js
node -e "console.log('Node.js version:', process.version)"

# Test Poetry
poetry --version

# Test Maven
mvn --version
```

## Troubleshooting

### Common Issues and Solutions

#### Docker Permission Issues
```bash
# If docker commands require sudo
sudo usermod -aG docker $USER
# Logout and login again, or run:
newgrp docker
```

#### Python Installation Issues
```bash
# If Python 3.12 is not available
# Use pyenv to install Python 3.12
curl https://pyenv.run | bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc
pyenv install 3.12.0
pyenv global 3.12.0
```

#### Java Version Issues
```bash
# Switch between Java versions
sudo update-alternatives --config java
sudo update-alternatives --config javac

# Or use JAVA_HOME
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
```

#### Network/Firewall Issues
```bash
# Configure firewall for development ports
sudo ufw allow 8000:8100/tcp
sudo ufw allow 5000:5010/tcp
sudo ufw allow 9092/tcp  # Kafka
sudo ufw allow 9200/tcp  # Elasticsearch
sudo ufw allow 6379/tcp  # Redis
sudo ufw allow 5432/tcp  # PostgreSQL
```

#### Performance Issues
```bash
# Check system resources
htop
df -h
free -h

# Clean up Docker
docker system prune -a

# Check Docker resource usage
docker stats
```

### Distribution-Specific Issues

#### Ubuntu/Debian
- Use `apt` instead of `apt-get` for newer features
- Check `/var/log/apt/` for package installation logs
- Use `dpkg -l | grep package_name` to check installed packages

#### CentOS/RHEL/Fedora
- Use `dnf` instead of `yum` on newer versions
- Check `/var/log/dnf.log` for package installation logs
- Use `rpm -qa | grep package_name` to check installed packages

## Next Steps

1. Logout and login to apply group memberships
2. Clone the project repository
3. Run the automated setup script
4. Follow the development workflow documentation
5. Set up IDE configurations
6. Run environment validation tests

## Additional Resources

- [Docker Engine Installation](https://docs.docker.com/engine/install/)
- [Python Installation Guide](https://docs.python.org/3/using/unix.html)
- [OpenJDK Installation](https://openjdk.java.net/install/)
- [Node.js Installation](https://nodejs.org/en/download/package-manager/)
- [VS Code on Linux](https://code.visualstudio.com/docs/setup/linux)