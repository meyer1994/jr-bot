set -ev

mkdir -p /tmp/app
cd /tmp/app

# Ubuntu deps
apt update
apt install -yq git python3.8 ffmpeg python3-pip
python3.8 -m pip install --upgrade pip virtualenv

# Venv
python3.8 -m virtualenv venv --clear
source venv/bin/activate

# Clone git
git clone https://github.com/meyer1994/jr-bot.git
cd jr-bot
git checkout algolia

# Python deps
pip install -r requirements.txt

# Environment (I could not find a better way to do it)
export ALGOLIA_USER="" && \
export ALGOLIA_TOKEN="" && \
export TELEGRAM_TOKEN="" && \
export GOOGLE_STORAGE_BUCKET="" && \

# Run
python3.8 local.py
