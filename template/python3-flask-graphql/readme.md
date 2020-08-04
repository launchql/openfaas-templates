# testing

pip install -r requirements.txt --target=`pwd`/testpip
export PATH=$PATH:`pwd`/testpip/bin
export PYTHONPATH=$PYTHONPATH:`pwd`/testpip
PORT=10101 python3 index.py