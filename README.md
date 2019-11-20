# Super Simple Secret Santa

Secret santa for groups with couples. Put your group's info into `config.yml`.

I used google's smtp server. There's a helpful guide [here](https://realpython.com/python-send-email/#option-2-setting-up-a-local-smtp-server).

### Install

```
git clone git@github.com:chipfranzen/secret_santa.git

cd secret_santa
```

I use [poetry](https://github.com/sdispater/poetry) for dependency management.

```
poetry install
```

### Run the thing

```
make santa
```

### Test it first

Start a local debugging server.
```
make server
```

Send test emails.
```
make test
```


