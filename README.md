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
 
### For windows:
* Create Docker Image
 ```
    sudo docker build -t tele-worker .
 ```
 * Create configuration for workers in `config.json` with Api Keys from `https://my.telegram.org/auth`
 * in `python3 workers.py` replace function "create Worker"
 ```
    def createWorker(worker):
    w_path = 'workers/test_' + worker['API_NAME']
    print('mkdir ' + w_path)
    shutil.copytree("working/", w_path, ignore=shutil.ignore_patterns('*.pyc', 'tmp*'))
    with open(w_path + '/config.json', 'w') as outfile:
        json.dump(worker, outfile)
 ```
 * Command `python3 workers.py` will generate workers
 * in `simulator.py` for first start, add import
 ```
 from selenium.webdriver.firefox.webdriver import WebDriver
 ```
 and add 
 ```
  driver = WebDriver(executable_path=r'yourpathtodriver\geckodriver.exe',options=self.opts)
  self.browser = driver
 ```
 * After first start in `simulator.py` replace code on
 ```
 driver = WebDriver(options=self.opts)
 self.browser = driver
 ```
 * In each new worker folder run `python3 main.py` and login
 * If you get errors install dependencies from `requirement.txt`
 * Go to `containers.py` and replace path `/home/botfarm/tele-worker/workers` with your path to workers folder
 * Run `sudo python3 containers.py` and create container for each worker
