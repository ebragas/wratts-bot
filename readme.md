[![CodeFactor](https://www.codefactor.io/repository/github/ebragas/wratts-bot/badge)](https://www.codefactor.io/repository/github/ebragas/wratts-bot)
[![codecov](https://codecov.io/gh/ebragas/wratts-bot/branch/master/graph/badge.svg?token=K3022QBYDA)](undefined)

## Usage
### Discord Auth
1. Login to Discord developer portal
2. Create application and get OAuth token

### Run Wratt-Bot
1. Clone repository
2. Build Docker image with `docker build -t wratt-bot .`
3. Create `.env` file with your Discord token and channel_id TODO: change to args?
4. Run image (with stdout) `docker run --rm -it wratt-bot`
