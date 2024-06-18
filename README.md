
## About
It is an application to score an audio on grammer correctness.

## Deployment
Deploy into an EC2 instance. Need to install Python3.12, Poetry, NodeJS:

- Install Python:
```
sudo yum groupinstall -y "Development Tools"
sudo yum install -y openssl-devel bzip2-devel libffi-devel zlib-devel wget
wget https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tgz
tar xzf Python-3.12.0.tgz
cd Python-3.12.0
./configure --enable-optimizations
make -j $(nproc)
sudo make altinstall
```
- Install Poetry:
```
curl -sSL https://install.python-poetry.org | python3.12 -
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```
- Install NodeJS:
```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm
nvm install 18.19.0
nvm use 18.19.0
nvm alias default 18.19.0
```

Next clone this project to the instance.

Whispter requires the command-line tool `ffmpeg` to be installed on your system, which is available from most package managers

## Start the App

- `npm start`
- `cd backend/app`
- `uvicorn server:app --reload`

## Reference

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).
Scaffolded by `npx create-react-app my-app --template typescript` (https://create-react-app.dev/docs/adding-typescript/)

## Future Improvements
