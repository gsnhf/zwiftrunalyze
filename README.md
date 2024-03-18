# zwiftrunalyze
This is a fork of [zwiftrunalyze](https://github.com/pnposch/zwiftrunalyze) from [pnposch](https://github.com/pnposch). I fixed some bugs.

The original program was not working for me. 

Download FIT files from [Zwift](www.zwift.com) or [MyWhoosh](www.mywhoosh.com) and upload to runanalyze. Simple as that.

[Zwift](www.zwift.com) and [MyWhoosh](www.mywhoosh.com) are popular virtual reality worlds for cyclists and runners.

[Runalyze](www.runalyze.com) is a privacy-friendly training log with extensive functionality (and its free!)

## Prequisites
Install requirements with:

``` sh
pip install -r requirements.txt
```
to include the few other (standard) packages needed.

## Alternatively use the Docker config below.

or include the few other (standard) packages needed:
``` sh
pip install -r requirements.txt 
```

- add data directory to your folder ``` mkdir data ```

- Rename ```zrconfig.py.example``` to ``` zrconfig.py ``` and proceed to config (no worries only three infos needed)


## Configure
Add your zwift username, zwift password and obtain a token for runanalyze (https://runalyze.com/settings/personal-api) and entere it too in the header of main.py and you are good to go. 

FIT files are downloaded into /data and pushed to runanalyze, once downloaded there are not requested a second time. Furthermore Zwift info is saved in a JSON file.

## Docker
Use Docker Image with local mounts of data/ and zrconfig.py/

``` sh
docker-compose up -d --build
```

To recreate the image 

``` sh
docker-compose up -d --build --force-recreate
```

Then start zwift import with

``` sh
docker exec zwiftrunalyze_app_1 python3 main.py
```

or MyWhoosh import with 

``` sh
docker exec zwiftrunalyze_app_1 python3 mywhoosh.py
```

which can be added to the host system's crontab

``` sh
crontab -e
```

e.g. run every evening at 22:30h:

``` sh
30 22 * * * docker exec zwiftrunalyze_app_1 python3 main.py
```

## Run locally
Simple: 

``` sh
python3 main.py
``` 
or 

``` sh
python3 mywhoosh.py
``` 
Make the file executable: 

``` sh
chmod +x main.py
```
and

``` sh
./main.py
```
.

Optional argument: Download only after date:
``` sh
python3 main.py YYYY.MM.DD
```
will skip any zwift acitivies ended before YYYY-MM-DD
s