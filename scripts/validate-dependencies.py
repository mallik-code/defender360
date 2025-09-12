#!/usr/bin/env python3
"""
Dependency Validation Script for Agentic SOC Framework
Validates system dependencies and requirements for local development.
"""

import os
import sys
import subprocess
import platform
import shutil
import json
import socket
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class ValidationStatus(Enum):
    PASS = "✅"
    FAIL = "❌"
    WARNING = "⚠️"
    INFO = "ℹ️"

@dataclass
class ValidationResult:
    name: str
    status: ValidationStatus
    message: str
    details: Optional[str] = None
    required: bool = True

class SystemValidator:
    """Validates system requirements and dependencies."""
    
    def __init__(self):
        self.results: List[ValidationResult] = []
        self.system = platform.system().lower()
        self.architecture = platform.machine().lower()
        
    def run_command(self, command: str, shell: bool = True) -> Tuple[int, str, str]:
        """Run a system command and return exit code, stdout, stderr."""
        try:
            result = subprocess.run(
                command,
                shell=shell,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode, result.stdout.strip(), result.stderr.strip()
        except subprocess.TimeoutExpired:
            return 1, "", "Command timed out"
        except Exception as e:
            return 1, "", str(e)
    
    def check_version(self, command: str, min_version: str, version_pattern: str = None) -> ValidationResult:
        """Check if a command exists and meets minimum version requirements."""
        # Check if command exists
        if not shutil.which(command.split()[0]):
            return ValidationResult(
                name=command.split()[0],
                status=ValidationStatus.FAIL,
                message=f"{command.split()[0]} not found in PATH"
            )
        
        # Get version
        exit_code, stdout, stderr = self.run_command(command)
        if exit_code != 0:
            return ValidationResult(
                name=command.split()[0],
                status=ValidationStatus.FAIL,
                message=f"Failed to get version: {stderr}"
            )
        
        # Extract version from output
        version_output = stdout + stderr
        if version_pattern:
            import re
            match = re.search(version_pattern, version_output)
            if match:
                current_version = match.group(1)
            else:
                return ValidationResult(
                    name=command.split()[0],
                    status=ValidationStatus.WARNING,
                    message=f"Could not parse version from: {version_output[:100]}"
                )
        else:
            # Simple version extraction
            import re
            version_match = re.search(r'(\d+\.\d+(?:\.\d+)?)', version_output)
            if version_match:
                current_version = version_match.group(1)
            else:
                return ValidationResult(
                    name=command.split()[0],
                    status=ValidationStatus.WARNING,
                    message=f"Could not parse version from: {version_output[:100]}"
                )
        
        # Compare versions
        try:
            from packaging import version
            if version.parse(current_version) >= version.parse(min_version):
                return ValidationResult(
                    name=command.split()[0],
                    status=ValidationStatus.PASS,
                    message=f"Version {current_version} (>= {min_version})"
                )
            else:
                return ValidationResult(
                    name=command.split()[0],
                    status=ValidationStatus.FAIL,
                    message=f"Version {current_version} < {min_version}"
                )
        except ImportError:
            # Fallback to simple string comparison if packaging not available
            if current_version >= min_version:
                return ValidationResult(
                    name=command.split()[0],
                    status=ValidationStatus.PASS,
                    message=f"Version {current_version} (>= {min_version})"
                )
            else:
                return ValidationResult(
                    name=command.split()[0],
                    status=ValidationStatus.WARNING,
                    message=f"Version {current_version}, expected >= {min_version} (simple comparison)"
                )
    
    def check_system_requirements(self) -> List[ValidationResult]:
        """Check basic system requirements."""
        results = []
        
        # Operating System
        if self.system in ['windows', 'darwin', 'linux']:
            results.append(ValidationResult(
                name="Operating System",
                status=ValidationStatus.PASS,
                message=f"{platform.system()} {platform.release()}"
            ))
        else:
            results.append(ValidationResult(
                name="Operating System",
                status=ValidationStatus.WARNING,
                message=f"Unsupported OS: {platform.system()}"
            ))
        
        # Architecture
        if self.architecture in ['x86_64', 'amd64', 'arm64', 'aarch64']:
            results.append(ValidationResult(
                name="Architecture",
                status=ValidationStatus.PASS,
                message=f"{self.architecture}"
            ))
        else:
            results.append(ValidationResult(
                name="Architecture",
                status=ValidationStatus.WARNING,
                message=f"Untested architecture: {self.architecture}"
            ))
        
        # Memory
        try:
            import psutil
            memory_gb = psutil.virtual_memory().total / (1024**3)
            if memory_gb >= 16:
                results.append(ValidationResult(
                    name="System Memory",
                    status=ValidationStatus.PASS,
                    message=f"{memory_gb:.1f} GB (>= 16 GB)"
                ))
            elif memory_gb >= 8:
                results.append(ValidationResult(
                    name="System Memory",
                    status=ValidationStatus.WARNING,
                    message=f"{memory_gb:.1f} GB (minimum 16 GB recommended)"
                ))
            else:
                results.append(ValidationResult(
                    name="System Memory",
                    status=ValidationStatus.FAIL,
                    message=f"{memory_gb:.1f} GB (< 8 GB minimum)"
                ))
        except ImportError:
            results.append(ValidationResult(
                name="System Memory",
                status=ValidationStatus.INFO,
                message="Could not check (psutil not available)",
                required=False
            ))
        
        # Disk Space
        try:
            disk_usage = shutil.disk_usage('.')
            free_gb = disk_usage.free / (1024**3)
            if free_gb >= 100:
                results.append(ValidationResult(
                    name="Disk Space",
                    status=ValidationStatus.PASS,
                    message=f"{free_gb:.1f} GB free (>= 100 GB)"
                ))
            elif free_gb >= 50:
                results.append(ValidationResult(
                    name="Disk Space",
                    status=ValidationStatus.WARNING,
                    message=f"{free_gb:.1f} GB free (minimum 100 GB recommended)"
                ))
            else:
                results.append(ValidationResult(
                    name="Disk Space",
                    status=ValidationStatus.FAIL,
                    message=f"{free_gb:.1f} GB free (< 50 GB minimum)"
                ))
        except Exception as e:
            results.append(ValidationResult(
                name="Disk Space",
                status=ValidationStatus.WARNING,
                message=f"Could not check disk space: {e}",
                required=False
            ))
        
        return results
    
    def check_core_tools(self) -> List[ValidationResult]:
        """Check core development tools."""
        results = []
        
        # Git
        results.append(self.check_version("git --version", "2.40"))
        
        # Docker
        results.append(self.check_version("docker --version", "24.0"))
        
        # Docker Compose
        docker_compose_result = self.check_version("docker compose version", "2.20")
        if docker_compose_result.status == ValidationStatus.FAIL:
            # Try legacy docker-compose
            docker_compose_result = self.check_version("docker-compose --version", "2.20")
        results.append(docker_compose_result)
        
        return results
    
    def check_programming_languages(self) -> List[ValidationResult]:
        """Check programming language runtimes."""
        results = []
        
        # Python
        results.append(self.check_version("python3 --version", "3.12"))
        
        # Alternative Python check
        python_result = self.check_version("python --version", "3.12")
        if python_result.status == ValidationStatus.PASS:
            results.append(ValidationResult(
                name="python (alias)",
                status=ValidationStatus.PASS,
                message=python_result.message,
                required=False
            ))
        
        # Java
        results.append(self.check_version("java -version", "21", r'version "(\d+)'))
        
        # Node.js
        results.append(self.check_version("node --version", "18.0"))
        
        return results
    
    def check_package_managers(self) -> List[ValidationResult]:
        """Check package managers."""
        results = []
        
        # Poetry
        results.append(self.check_version("poetry --version", "1.7"))
        
        # Maven
        results.append(self.check_version("mvn --version", "3.9"))
        
        # npm
        results.append(self.check_version("npm --version", "9.0"))
        
        return results
    
    def check_docker_configuration(self) -> List[ValidationResult]:
        """Check Docker configuration and resources."""
        results = []
        
        # Docker daemon running
        exit_code, stdout, stderr = self.run_command("docker info")
        if exit_code == 0:
            results.append(ValidationResult(
                name="Docker Daemon",
                status=ValidationStatus.PASS,
                message="Running"
            ))
            
            # Parse Docker info for resource allocation
            try:
                # Check memory allocation
                if "Total Memory:" in stdout:
                    import re
                    memory_match = re.search(r'Total Memory:\s*([0-9.]+)\s*([A-Za-z]+)', stdout)
                    if memory_match:
                        memory_value = float(memory_match.group(1))
                        memory_unit = memory_match.group(2).lower()
                        
                        if memory_unit.startswith('g'):
                            memory_gb = memory_value
                        elif memory_unit.startswith('m'):
                            memory_gb = memory_value / 1024
                        else:
                            memory_gb = 0
                        
                        if memory_gb >= 8:
                            results.append(ValidationResult(
                                name="Docker Memory",
                                status=ValidationStatus.PASS,
                                message=f"{memory_gb:.1f} GB allocated (>= 8 GB)"
                            ))
                        else:
                            results.append(ValidationResult(
                                name="Docker Memory",
                                status=ValidationStatus.WARNING,
                                message=f"{memory_gb:.1f} GB allocated (< 8 GB recommended)"
                            ))
            except Exception as e:
                results.append(ValidationResult(
                    name="Docker Memory",
                    status=ValidationStatus.INFO,
                    message="Could not parse memory allocation",
                    required=False
                ))
        else:
            results.append(ValidationResult(
                name="Docker Daemon",
                status=ValidationStatus.FAIL,
                message=f"Not running: {stderr}"
            ))
        
        return results
    
    def check_network_ports(self) -> List[ValidationResult]:
        """Check if required ports are available."""
        results = []
        
        required_ports = [8000, 8080, 5432, 6379, 9092, 9200]
        
        for port in required_ports:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    result = s.connect_ex(('localhost', port))
                    if result == 0:
                        results.append(ValidationResult(
                            name=f"Port {port}",
                            status=ValidationStatus.WARNING,
                            message="In use (may conflict)",
                            required=False
                        ))
                    else:
                        results.append(ValidationResult(
                            name=f"Port {port}",
                            status=ValidationStatus.PASS,
                            message="Available",
                            required=False
                        ))
            except Exception as e:
                results.append(ValidationResult(
                    name=f"Port {port}",
                    status=ValidationStatus.INFO,
                    message=f"Could not check: {e}",
                    required=False
                ))
        
        return results
    
    def check_ide_tools(self) -> List[ValidationResult]:
        """Check IDE and development tools."""
        results = []
        
        # VS Code
        vscode_result = self.check_version("code --version", "1.80")
        vscode_result.required = False
        results.append(vscode_result)
        
        return results
    
    def run_all_checks(self) -> Dict[str, List[ValidationResult]]:
        """Run all validation checks."""
        checks = {
            "System Requirements": self.check_system_requirements(),
            "Core Tools": self.check_core_tools(),
            "Programming Languages": self.check_programming_languages(),
            "Package Managers": self.check_package_managers(),
            "Docker Configuration": self.check_docker_configuration(),
            "Network Ports": self.check_network_ports(),
            "IDE Tools": self.check_ide_tools(),
        }
        
        # Flatten results for summary
        self.results = []
        for category_results in checks.values():
            self.results.extend(category_results)
        
        return checks
    
    def print_results(self, checks: Dict[str, List[ValidationResult]]):
        """Print validation results in a formatted way."""
        print("🔍 Agentic SOC Framework - Dependency Validation")
        print("=" * 60)
        print()
        
        for category, results in checks.items():
            print(f"📋 {category}")
            print("-" * 40)
            
            for result in results:
                status_icon = result.status.value
                required_marker = "" if result.required else " (optional)"
                print(f"{status_icon} {result.name}{required_marker}: {result.message}")
                if result.details:
                    print(f"   {result.details}")
            print()
        
        # Summary
        total_checks = len([r for r in self.results if r.required])
        passed_checks = len([r for r in self.results if r.required and r.status == ValidationStatus.PASS])
        failed_checks = len([r for r in self.results if r.required and r.status == ValidationStatus.FAIL])
        warning_checks = len([r for r in self.results if r.required and r.status == ValidationStatus.WARNING])
        
        print("📊 Summary")
        print("-" * 40)
        print(f"✅ Passed: {passed_checks}/{total_checks}")
        print(f"❌ Failed: {failed_checks}/{total_checks}")
        print(f"⚠️  Warnings: {warning_checks}/{total_checks}")
        print()
        
        if failed_checks > 0:
            print("❌ Critical issues found. Please resolve before proceeding.")
            print("📖 See installation guides in docs/development/installation-guides/")
            return False
        elif warning_checks > 0:
            print("⚠️  Some warnings found. Development may work but performance could be impacted.")
            return True
        else:
            print("✅ All checks passed! Your system is ready for development.")
            return True
    
    def generate_report(self, output_file: str = "validation-report.json"):
        """Generate a JSON report of validation results."""
        report = {
            "timestamp": subprocess.run(["date", "-Iseconds"], capture_output=True, text=True).stdout.strip(),
            "system": {
                "os": platform.system(),
                "release": platform.release(),
                "architecture": platform.machine(),
                "python_version": platform.python_version()
            },
            "results": []
        }
        
        for result in self.results:
            report["results"].append({
                "name": result.name,
                "status": result.status.name,
                "message": result.message,
                "details": result.details,
                "required": result.required
            })
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📄 Detailed report saved to: {output_file}")

def main():
    """Main validation function."""
    validator = SystemValidator()
    
    print("Starting dependency validation...")
    print()
    
    try:
        checks = validator.run_all_checks()
        success = validator.print_results(checks)
        
        # Generate report
        validator.generate_report()
        
        # Exit with appropriate code
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n❌ Validation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Validation failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()