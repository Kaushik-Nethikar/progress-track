from supabase import create_client
import streamlit as st

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)


def save_entry(person, entry_date, status, note):
    data = {
        "person": person,
        "entry_date": str(entry_date),
        "status": status,
        "note": note
    }

    response = (
        supabase
        .table("progress_entries")
        .upsert(
            data,
            on_conflict="person,entry_date"
        )
        .execute()
    )

    return response


def get_person_entries(person):
    response = (
        supabase
        .table("progress_entries")
        .select("*")
        .eq("person", person)
        .execute()
    )

    return response.data


def get_month_entries(person, year, month):

    month_str = f"{year}-{month:02d}"

    response = (
        supabase
        .table("progress_entries")
        .select("*")
        .eq("person", person)
        .gte("entry_date", f"{month_str}-01")
        .lte("entry_date", f"{month_str}-31")
        .execute()
    )

    return response.data


def get_entry(person, entry_date):

    response = (
        supabase
        .table("progress_entries")
        .select("*")
        .eq("person", person)
        .eq("entry_date", str(entry_date))
        .execute()
    )

    if response.data:
        return response.data[0]

    return None