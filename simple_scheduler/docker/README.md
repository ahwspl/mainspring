# Dockerize simple scheduler

## Build docker image
```bash
    docker build -t mainspring .
```

## Run a container

```bash
    docker run -it -p 8888:8888 \
	  -e "SIMPLE_SCHEDULER_SLACK_URL=$SLACK_API_URL" \
	  mainspring
```

You can now access the localhost:8888 for the web ui.
