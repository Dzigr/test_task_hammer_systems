### Simple referral system ###

Referral system api-application based on the Django Rest Framework, initialization is carried out by phone number, authorization by JWT token.

[You may try demo here](https://referral-app.onrender.com)


**Stack:**
* Python
* DRF
* PostgreSQL

----

### Start project with Docker ###

----

###### Note: Required Python & Poetry ######
1. Clone the repository
    ```comandline
    git clone git@github.com:Dzigr/test_task_hammer_systems && cd test_task_hammer_systems
    ```
2. Initiate configuration with Makefile command
    ```commandline
    make docker-install
    ```
   This will create .env file with necessary variables and build docker containers


3. Run application by
    ```commandline
    make docker
    ```

----

### API references ###

----

#### Registration and authorization: ####
*POST api/v1/auth/phone/* - sending phone number and receive authentication code
<details><summary>Response example</summary>

```json lines
{
    "Authentication code": "7718"
}
```

</details>

*POST api/v1/auth/verify_code/* - sending authentication code and receive JWT token

<details><summary>Response example</summary>

```json lines
{
    "phone_number": "79940111108",
    "authorization_code": "9043",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwaG9uZV9udW1iZXIiOiI3OTk0MDExMTEwOCIsImV4cCI6MTY5MjQwMzUxNn0.MdQcS4me84iQn1jqhsuOPF2w-_jMhWHFuSWMP-ll29E"
}
```

</details>


###### Note: Further methods require authentication via JWT token ######
#### User profile: ####
*GET api/v1/user/profile/* - receive user profile information

<details><summary>Response example</summary>

```json lines
{
    "user": {
        "phone_number": "79940111108",
        "invite_code": "kkBIEl",
        "referral_activated": true,
        "referred_users": []
    }
}
```

</details>


#### Add referral link: ####
*PATCH api/v1/user/profile/add_referral/* - sending referral invite code
###### Note: Only one invite code could be activated. Not possible to activate own invite code #####

<details><summary>Response example</summary>

```json lines
{
    "message": "Referrer added successfully"
}
```
or error message, like below:

```json lines
{
    "detail": "Referral link has already been activated"
}
```

</details>

----

#### To run the tests: ####

```comandline
    make test
```
