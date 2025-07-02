# linux_pkg_utility

A Python CLI tool for comparing packages between ALT Linux branches via the public API.

## Features
- Compares package versions between two ALT Linux branches
- Identifies packages present in only the first branch
- Identifies packages present in only the second branch
- Detects version differences using RPM comparison rules only newest in the first branch
- Generates JSON report file

## Requirements
- ALT Linux 11
- Python 3.11+
- RPM system libraries

## Installation

### 1. System Preparation

Enter the root user 
```bash
su -
```

Update your system packages:
```bash
apt-get update && apt-get upgrade --enable-upgrade
```

Download Git (if doesn't exist)
```bash
apt-get install git
```

*The system will ask to continue because it will download files. Press Y*

### 2. Сlone the repository:
```bash
git clone git@github.com:Alimovriq/linux_pkg_utility.git
```

### 3. Install Required RPM Packages

Download and install these packages manually:

Package	Download URL
1. librpm7	https://git.altlinux.org/tasks/327286/build/4100/x86_64/rpms/librpm7-4.13.0.1-alt40.x86_64.rpm
2. librpmbuild7 https://git.altlinux.org/tasks/327286/build/4100/x86_64/rpms/librpmbuild7-4.13.0.1-alt40.x86_64.rpm
3. python3-module-rpm https://git.altlinux.org/tasks/324286/build/100/x86_64/rpms/python3-module-rpm-4.13.0.1-alt38.x86_64.rpm

go to the download directory by root user, for example, "/Загрузки"
```bash
cd /home/<username>/Загрузки
```

Install downloaded packages:
```bash
apt-get install ./package-name.rpm
```

type "exit" to exit the root user for safety
```bash
exit
```

### 4. Install Python Requests library (if doesn't exist)

Check the pip package manager
```bash
python3 -m ensurepip --upgrade
```

download and install Requests library
```bash
pip3 install requests
```

### 5. Usage
go to the linux_pkg_utility directory
```bash
cd linux_pkg_utility
```

Launch
```bash
./cli_main.py [BRANCH1] [BRANCH2] [--output FILE.json]
```

### 6. Arguments
| Argument       | Default      | Description                      |
|---------------|-------------|----------------------------------|
| `BRANCH1`     | `sisyphus`  | First branch to compare          |
| `BRANCH2`     | `p11`       | Second branch to compare         |
| `-o/--output` | `result.json` | Output JSON file path           |

### 7. Examples
1. Compare default branches (sisyphus vs p11):
```bash
./cli_main.py
```
2. Compare specific branches with custom output:
```bash
./cli_main.py branch1 branch2 --output comparison.json
```

### 8. Output Format
```json 
{
  "only_in_first_branch": [],
  "only_in_second_branch": [],
  "newest_in_first_branch": []
}
```
