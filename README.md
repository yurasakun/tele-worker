# Docker Tele-worker

## Into
This script has configuration and cant work with `@TGZaraBot` and `@Zcash_click_bot`, so you need add thi bots to your telegram account before start.

### Init 
 * Create configuration for workers in `config.json` with Api Keys from `https://my.telegram.org/auth`
 * Create login session for each bot with single command `python3 login`
 * Create Docker Image
 ```
    sudo docker build -t tele-farm .
 ```

 * Run Tele farm container
 ```
   sudo docker run -d --name army_1 -v /home/ubuntu/army_1:/usr/src/app  --restart always tele-farm:latest
 ```