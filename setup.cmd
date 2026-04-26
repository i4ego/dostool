python3 -m venv .venv
.venv/Scripts/activate.bat

pip3 install -r req.txt
pip3 install pyinstaller

pyinstaller --onefile --console --clean --noconfirm --distpath ./ --name dostool dostool.py
remove dostool.spec
rmdir build /s /q
dostool