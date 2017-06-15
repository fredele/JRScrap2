installer python-2.7.13.msi 32 bit
python -m pip install --upgrade pip wheel setuptools
python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew
python -m pip install kivy
python -m pip install kivy_examples
python -m pip install PyInstaller
cd C:\Python27\share\kivy-examples\tutorials\pong
python main.py

cd C:\Users\fredele\Desktop\JR\
python -m PyInstaller JRScrap2.spec

