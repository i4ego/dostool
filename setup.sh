python3 -m venv .venv
source ./.venv/bin/activate

python3 -m pip install -r req.txt
python3 -m pip install pyinstaller

pyinstaller --onefile --console --clean --noconfirm \
 --distpath ./ --name dostool dostool.py
rm dostool.spec
rm -rf build
./dostool