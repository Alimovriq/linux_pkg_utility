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
Update your system packages:
```bash
sudo apt-get update && sudo apt-get upgrade
```

### 2. Install Python Requests library (if doesn't exist)
```bash
sudo apt-get install python3-requests
```

### 3. Install Required RPM Packages
Download and install these packages manually:

Package	Download URL
1. librpm7	https://git.altlinux.org/tasks/327286/build/4100/x86_64/rpms/librpm7-4.13.0.1-alt40.x86_64.rpm
2. librpmbuild7 https://git.altlinux.org/tasks/327286/build/4100/x86_64/rpms/librpmbuild7-4.13.0.1-alt40.x86_64.rpm
3. python3-module-rpm https://git.altlinux.org/tasks/324286/build/100/x86_64/rpms/python3-module-rpm-4.13.0.1-alt38.x86_64.rpm

Install downloaded packages:
```bash
sudo apt-get install ./package-name.rpm
```

### 4. Usage
```bash
./cli.py [BRANCH1] [BRANCH2] [--output FILE.json]
```

### 5. Arguments
| Argument       | Default      | Description                      |
|---------------|-------------|----------------------------------|
| `BRANCH1`     | `sisyphus`  | First branch to compare          |
| `BRANCH2`     | `p11`       | Second branch to compare         |
| `-o/--output` | `result.json` | Output JSON file path           |

### 6. Examples
1. Compare default branches (sisyphus vs p11):
```bash
./cli.py
```
2. Compare specific branches with custom output:
```bash
./cli.py branch1 branch2 --output comparison.json
```

### 7. Output Format
```json 
{
  "only_in_first_branch": [],
  "only_in_second_branch": [],
  "newer_in_first_branch": []
}
```


