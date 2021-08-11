# CAP Interview
Joe Herman
8.1.2021

## Approach
***tl;dr in bold***

I will use **Python** because why not?

I'll **Dockerize the app** and installation since Python dependencies are particularly annoying to keep portable.

All operational things (build, run, test, etc.) should be contained in a single **`Makefile`**.

Since this is about web services and design decisions, I will add a persistent cache layer (redis), **orchestrated via Docker Compose**.

Basic container orchestration **lays groundwork for sidecar services** (networking [Zero Trust, load balancing], metrics, logging, auth, etc.) and scaling. Admittedly, for a basic app, this may be a wholly unnecessary performance and maintenance drain.

Tests will **integration test** the app's behavior because I don't feel like mocking/stubbing out contract tests right now.

Documentation should cover at least the following aspects:
* **Developer documentation** (like this!) should clearly indicate _why_ the code does what it does.
* **Operator documentation** should indicate how to run and maintain the app.
* **Product documentation** should specify user-facing features.

## Non-goals

* Kubernetes
* On call reference and troubleshooting guide
* Opsviz things like APM, metrics, unified logging

## TODO
1. ~~Document approach~~
2. ~Set up boilerplate and sidecar containers for data persistence and testing~
~3. For the `/stringinate` endpoint, for a given input string we need to find the character that occurs most frequently and add that character, along with its number of occurrences to the API response JSON. You decide how to represent this in the JSON response.  Ignore white space and punctuation.~
4. For the `stats` endpoint, track which string input has been seen the most times. Return this value as the `most_popular` key in the response JSON.
5. For the `stats` endpoint, track which string input is the longest string to be seen by the server and return as the `longest_input_received` key in the response JSON.
6. Implement one new feature to improve the application:
  * authorization?
  * secrets management?
  * HTTPS?
7. Finalize documentation

