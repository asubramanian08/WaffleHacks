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


def initDB(conn):
    with conn.cursor() as cur:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS user_info (\
                user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),\
                email VARCHAR(319), password VARCHAR(50))"),

        cur.execute(
            "CREATE TABLE IF NOT EXISTS reviews (\
                rev_id UUID PRIMARY KEY DEFAULT gen_random_uuid(), \
                revText VARCHAR(1000), restaurant VARCHAR(100), \
                dietary_rest VARCHAR(1000), rating FLOAT)"),

        logging.debug("initDB(): status message: %s",
                      cur.statusmessage)

    conn.commit()


def addUser(conn, email, password):
    with conn.cursor() as cur:

        cur.execute(
            f"INSERT INTO user_info (email, password) VALUES ('{email}', '{password}')")

        logging.debug("addUser(): status message: %s", cur.statusmessage)

    conn.commit()


def createReview(revText, restaurant, dietary_rest, rating):
    with conn.cursor() as cur:

        cur.execute(
            f"INSERT INTO reviews (revText, restaurant, dietary_rest, rating) \
            VALUES ('{revText}', '{restaurant}', '{dietary_rest}', '{rating}')")

        logging.debug("createReview(): status message: %s", cur.statusmessage)

    conn.commit()


def getRating(restaurant, dietary_rest):
    with conn.cursor() as cur:

        cur.execute(
            f"SELECT AVG(rating) FROM reviews \
            WHERE restaurant='{restaurant}' AND dietary_rest='{dietary_rest}'")
        result = cur.fetchone()
        logging.debug("getRating(): status message: %s", cur.statusmessage)

    conn.commit()

    return result[0]


def getReviews(restaurant, dietary_rest):
    with conn.cursor() as cur:

        cur.execute(
            f"SELECT revText FROM reviews \
            WHERE restaurant='{restaurant}' AND dietary_rest='{dietary_rest}'")
        result = [i[0] for i in cur.fetchall()]
        logging.debug("getReviews(): status message: %s", cur.statusmessage)

    conn.commit()

    return result


def validate_login(conn, email, password):

    with conn.cursor() as cur:

        cur.execute(
            f"SELECT user_id FROM user_info WHERE email='{email}' AND password='{password}'"
        )
        result = cur.fetchone()
        conn.commit()
        print(result)


def resetTables(conn):
    # """ Debugging purposes """
    with conn.cursor() as cur:
        cur.execute("DROP TABLE user_info"),

        cur.execute("DROP TABLE reviews"),

        logging.debug("resetTables(): status message: %s", cur.statusmessage)

    conn.commit()


# initDB(conn)
# addUser(conn, email='hi@gmail.com', password='pass')
# # resetTables(conn)
# createReview(revText='This place was good!',
#              restaurant='subway', dietary_rest='vegan', rating=5)
# print(getRating('subway', 'vegan'))
# print(getReviews('subway', 'vegan'))
# validate_login(conn, email='hi@gmail.com', password='pass')
