# CAP Interview
Joe Herman
Created 8.1.2021
Updated 2.3.2023

## Getting started
Download a [release](https://github.com/Penryn/cap-coding-challenge/releases), or grab a [build from the `main` branch](https://github.com/Penryn/cap-coding-challenge/actions?query=branch%3Amain).

### Prerequisites
* Docker
* Standard make build tools

### Running
After expanding the archive, run one of the following:

```sh
# Run the server (automatically rebuilds images)
make run
```

```sh
# Run built-in tests
make test
```

## Sample API Usage

### Send a string

```bash
curl -id '{"input":"this is the input"}' -H 'Content-Type: application/json' http://localhost:6000/stringinate
```

### Get stats
```bash
curl -i -H 'Content-Type: application/json' http://localhost:6000/stats
```

## Ops Guide

### Updating environment variables
Modify `./python/.env` to update Flask server variables.
Update `./docker-compose.yml` for other container variables.

### Updating package dependencies
1. Obtain a shell in the appropriate container:

```sh
# Jump into a shell on the app
APP=cap-app make shell

# Jump into a shell on the tester app
APP=cap-test make shell
```

2. Install current dependencies

```bash
pip install -r requirements.txt
```

3. Update pip dependencies as needed
```bash
pip install --upgrade
```

4. Update requirements.txt
```bash
pip freeze > requirements.txt
```

## Approach
***tl;dr in bold***

I will use **Python** because why not?

I'll **Dockerize the app** and installation since Python dependencies are particularly annoying to keep portable.

All operational things (build, run, test, etc.) should be contained in a single **`Makefile`**.

Since this is about web services and design decisions, I will add a persistent cache layer (redis), **orchestrated via Docker Compose**.

Basic container orchestration **lays groundwork for sidecar services** (networking [Zero Trust, load balancing], metrics, logging, auth, etc.) and scaling. Admittedly, for a basic app, this may be a wholly unnecessary performance and maintenance drain.

Tests will **integration test** the app's behavior because I don't feel like mocking/stubbing out contract tests right now.

I will use **GitHub Actions to help with CI and to give static builds** that are easily referenced later.

I used **Redis** ~~to overcomplicate things~~ as a memory-based store to allow for theoretical horizontal scaling (benefits debatable).

Documentation should cover at least the following aspects:
* **Developer documentation** (like this!) should clearly indicate _why_ the code does what it does.
* **Operator documentation** should indicate how to run and maintain the app.
* **Product documentation** should specify user-facing features.

## Non-goals

* Kubernetes
* On-call reference and troubleshooting guide
* Opsviz things like APM, metrics, unified logging

## TODO
1. ~~Document approach~~
2. ~~Set up boilerplate and sidecar containers for data persistence and testing~~
3. ~~For the `/stringinate` endpoint, for a given input string we need to find the character that occurs most frequently and add that character, along with its number of occurrences to the API response JSON. You decide how to represent this in the JSON response.  Ignore white space and punctuation.~~
4. ~~For the `stats` endpoint, track which string input has been seen the most times. Return this value as the `most_popular` key in the response JSON.~~
5. ~~For the `stats` endpoint, track which string input is the longest string to be seen by the server and return as the `longest_input_received` key in the response JSON.~~
6. ~~Implement one new feature to improve the application:~~
  * ~~Persistence/caching~~
  * ~~CI with GHA~~
7. Finalize documentation
8. Additional tests

## Version history
* v1.2.0 updates the default port to 6000 to avoid conflicts when running on MacOS Ventura with AirPlay enabled.
* v1.1.0 requires redis. There are performance tradeoffs particularly in the `/stats` endpoint.
* v1.0.0 is an MVP
