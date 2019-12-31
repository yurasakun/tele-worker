# Docker Tele-worker

## Into
This script has configuration and cant work with `@TGZaraBot` and `Zcash_click_bot`, so you need add thi bots to your telegram account before start.

### Init 
 * Create Docker Image
 ```
    sudo docker build -t tele-worker .
 ```
 * Create configuration for workers in `config.json` with Api Keys from `https://my.telegram.org/auth`
 * Command `python3 workers.py` will generate workers
 * In each new worker folder run `python3 main.py` and login
 * If you get errors install dependencies from `requirement.txt`
 * Go to `containers.py` and replace path `/home/botfarm/tele-worker/workers` with your path to workers folder
 * Run `sudo python3 containers.py` and create container for each worker