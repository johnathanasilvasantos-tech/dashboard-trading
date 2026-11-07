import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import os

def get_db():
    if not firebase_admin._apps:
        try:
            cred_dict = dict(st.secrets["firebase"])
            cred = credentials.Certificate(cred_dict)
        except Exception:
            if os.path.exists("serviceAccountKey.json"):
                cred = credentials.Certificate("serviceAccountKey.json")
            else:
                raise FileNotFoundError("serviceAccountKey.json não encontrado.")
        firebase_admin.initialize_app(cred)
    return firestore.client()