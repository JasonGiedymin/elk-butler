# ELK Butler

## Install

At the moment a release is offered on GitHub. We're working on creating a
pip package but there are some subtleties necessary. For now please follow
the instructions within this README.

### Pip Requirements

See the `requirements.txt` file.

Please use a virtual environment.

```shell
$ pip install -r requirements.txt
# OR if your install is borked
$ sudo $(which pip) install -r requirements.txt
```

#### Manual Pip Steps

```shell
pip install -U pytest
pip install -U requests
pip install -U requests-mock
pip install -U elasticsearch

# alternatively if you have a borked system
sudo $(which pip) install -U pip
sudo $(which pip) install -U pytest
sudo $(which pip) install -U requests
sudo $(which pip) install -U requests-mock
sudo $(which pip) install -U elasticsearch
```

## Integration Tests

Requries a running instance of elasticsearch. You may use docker like so:

```shell
docker rm test_elasticsearch
docker run --name test_elasticsearch -dP elasticsearch elasticsearch -Des.node.name="TestNode"
```

## Running

When executing either test or running, you may supply the following environment
variables:

```shell
# the following works against a docker container like the one above in the section labeled "Integration Test"
export ES_HOST=localhost                           # defaults to localhost
export ES_PORT=32769                               # defaults to 9200
export ELK_BUTLER_LOGLEVEL=TRACE                   # defaults to INFO
export ELK_BUTLER_LOGFILE=$(pwd)/logs/process.log  # defaults to /var/log/elk-butler/process.log
export ELK_BUTLER_TIMEOUT=60                       # defaults to 60
export ELK_BUTLER_INTERVAL=60                      # defaults to 60
export ELK_DISK_MOUNT='/mnt/data'                  # defaults to '/'
python app.py

# OR via the env method (recommended)
env ES_PORT=32769 \
ELK_BUTLER_LOGLEVEL=TRACE \
ELK_BUTLER_LOGFILE=$(pwd)/logs/process.log \
ES_HOST=192.168.99.100 \
ELK_BUTLER_TIMEOUT=60 \
ELK_BUTLER_INTERVAL=60 \
ELK_DISK_MOUNT="/mnt/data"
python app.py
```

## Running as a Daemon process

It is completely recommended that you use supervisord at the moment.
Supplied is a sample supervisord script `elk-butler.supervisord.conf`.

To run do the following:

  1. symlink the desired python to the root of `elk-butler`, i.e. (`sudo ln -sf $(which python) /opt/elk-butler/python`)
  1. install package requirements (see above section [Pip Requirements])
  1. run the following shell commands:
  ```shell
  $ sudo $(which supervisorctl) status
  $ sudo $(which supervisorctl) avail
  $ sudo $(which supervisorctl) update
  $ sudo $(which supervisorctl) status
  # you should now see like so:
  # elk-butler                       in use    auto      999:999
  # - Now inspect the log file: `sudo tail -f /var/log/elk-butler/process.log`
  # - sudo tail -f /var/log/elk-butler/elk-butler_stderr.log
  $ sudo $(which supervisorctl) stop elk-butler
  ```

## TODO

TODOs:

  - write `setup.py`, `setup.cfg`...
  - add 'time taken'
  - pip
