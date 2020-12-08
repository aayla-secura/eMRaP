# OVERVIEW

There are two demos, `search_email_only.sh` and `server_interact.sh`.

`search_email_only.sh` will take the latest email in the inbox and display the `From` email address and the subject.

`server_interact.sh` will send a `GET` request to `http://localhost:50001`, get the domain part of the `From` address in the latest email and use that as the `Host` header in subsequent requests. Then it will send a `POST` request to `http://localhost:50001` extract a line matching "token:" from the response body, then repeat once again, this time including the token extracted from the response to the last `POST` request in the body. After every response it also extracts the set Cookie and uses that in subsequent requests, updating everytime. `pyserver.py` implements the HTTP server. Run `python3 pyserver.py` from one terminal and run the demo in another.
