from collections import defaultdict

import json
import time
import random
import logging
import os
from argparse import ArgumentParser, RawTextHelpFormatter
import logging

import psycopg2
from psycopg2.errors import SerializationFailure

conn = psycopg2.connect(
    "postgresql://chantal:wafflehacks2022@free-tier6.gcp-asia-southeast1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&options=--cluster%3Dwafflehacks-2805")


def initDB() -> None:
    """ Create the user_id and reviews tables if not already made. """
    global conn
    with conn.cursor() as cur:

        # execute sql
        cur.execute(
            "CREATE TABLE IF NOT EXISTS user_info (\
                user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),\
                email VARCHAR(319), password VARCHAR(50))"),
        cur.execute(
            "CREATE TABLE IF NOT EXISTS reviews (\
                rev_id UUID PRIMARY KEY DEFAULT gen_random_uuid(), \
                revText VARCHAR(1000), restaurant VARCHAR(100), \
                dietary_rest VARCHAR(1000), rating FLOAT)"),

        # send logger message for debugging
        logging.debug("initDB(): status message: %s", cur.statusmessage)

    # commit all changes to cockroachDB
    conn.commit()


def addUser(email: str, password: str) -> None:
    """ Add another row to the user_info table. """
    global conn
    with conn.cursor() as cur:

        # execute sql
        cur.execute(
            f"INSERT INTO user_info (email, password) VALUES ('{email}', '{password}')")

        # send logger message for debugging
        logging.debug("addUser(): status message: %s", cur.statusmessage)

    # commit all changes to cockroachDB
    conn.commit()


def createReview(revText: str, restaurant: str, dietary_rest: str, rating: float) -> None:
    """ Insert a row for the given review into the reviews table. """
    global conn
    with conn.cursor() as cur:

        # execute sql
        cur.execute(
            f"INSERT INTO reviews (revText, restaurant, dietary_rest, rating) \
            VALUES ('{revText}', '{restaurant}', '{dietary_rest}', '{rating}')")

        # send logger message for debugging
        logging.debug("createReview(): status message: %s", cur.statusmessage)

    # commit all changes to cockroachDB
    conn.commit()


def getRating(restaurant: str, dietary_rest: str) -> float:
    """ Average rating of a restaurant for the dietary restriction.
        Returns None is there are no ratings. """
    global conn
    with conn.cursor() as cur:

        # execute sql
        cur.execute(
            f"SELECT AVG(rating) FROM reviews \
            WHERE restaurant='{restaurant}' AND dietary_rest='{dietary_rest}'")
        result = cur.fetchone()[0]

        # send logger message for debugging
        logging.debug("getRating(): status message: %s", cur.statusmessage)

    # commit all changes to cockroachDB
    conn.commit()

    # return the restaurant's rating for the dietary restriction
    return result


def getReviews(restaurant: str, dietary_rest: str) -> [str, ...]:
    """ Get all the reviews from a restaurant with a dietary restriction.
        Returns an empty list '[]' if there are no reviews. """
    global conn
    with conn.cursor() as cur:

        # execute sql
        cur.execute(
            f"SELECT revText FROM reviews \
            WHERE restaurant='{restaurant}' AND dietary_rest='{dietary_rest}'")
        result = [i[0] for i in cur.fetchall()]

        # send logger message for debugging
        logging.debug("getReviews(): status message: %s", cur.statusmessage)

    # commit all changes to cockroachDB
    conn.commit()

    # return a list of strings for all the reviews
    return result


def validate_login(email: str, password: str) -> bool:
    """ Return True if the email and password are a valid user,
        otherwise it returns False. """
    global conn
    with conn.cursor() as cur:

        # execute sql
        cur.execute(f"SELECT user_id FROM user_info \
            WHERE email='{email}' AND password='{password}'")
        result = cur.fetchone() != None

        # send logger message for debugging
        logging.debug("validate_login(): status message: %s", cur.statusmessage)

    # commit all changes to cockroachDB
    conn.commit()

    # return is the login is valid
    return result


def resetTables() -> None:
    """ Drop all the tables made: for debugging purposes. """
    global conn
    with conn.cursor() as cur:

        # execute sql
        cur.execute("DROP TABLE user_info"),
        cur.execute("DROP TABLE reviews"),

        # send logger message for debugging
        logging.debug("resetTables(): status message: %s", cur.statusmessage)

    # commit all changes to cockroachDB
    conn.commit()


def testDB() -> None:
    """ Quick check to ensure db.py is working. """
    # resetTables()
    initDB()
    addUser(email='hi@gmail.com', password='pass')
    createReview(revText='This place was good!',
                 restaurant='subway', dietary_rest='vegan', rating=5)
    print(getRating('subway', 'vegan'))
    print(getReviews('subway', 'vegan'))
    print(validate_login(email='hi@gmail.com', password='pass'))
    print(validate_login(email='hi@gmail.com', password='wrongPass'))


testDB()
