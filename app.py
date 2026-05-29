import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import requests
import time

# 1. Konfiguration af hjemmesiden
st.set_page_config(page_title="Ravnkjærgaard - Jagtbooking", page_icon="🌲", layout="centered")

# --- FORBINDELSE TIL GOOGLE SHEET & FORM ---
TOKEN_TID = str(int(time.time()))
GOOGLE_SHEET_URL = f"https://google.com{TOKEN_TID}"
FORM_BASE_URL = "https://google.com"

def send_til_google_form(noegle, handling, data_streng):
    payload = {
        "entry.222097927": noegle,
        "entry.1968838176": handling,
        "entry.937412468": data_streng
    }
    try:
        requests.post(FORM_BASE_URL, data=payload)
        return True
    except Exception as e:
        st.error(f"Kunne ikke oprette forbindelse til skyen: {e}")
        return False

def hent_aktuelle_bookinger():
    try:
        df = pd.read_csv(GOOGLE_SHEET_URL)
        bookinger_dict = {}
        if not df.empty:
            for _, row in df.iterrows():
                noegle_col = [c for c in df.columns if 'noegle' in c.lower()]
                handling_col = [c for c in df.columns if 'handling' in c.lower()]
                data_col = [c for c in df.columns if 'data' in c.lower()]
                
                if noegle_col and handling_col and data_col:
                    noegle = str(row[noegle_col[0]]).strip()
                    handling = str(row[handling_col[0]]).strip().upper()
                    data_felt = str(row[data_col[0]]).strip()
                    
                    if pd.notna(row[noegle_col[0]]) and noegle != "" and noegle != "nan" and noegle.lower() != "noegle":
                        if handling == "BOOK" and "|" in data_felt:
                            dele = data_felt.split("|")
                            if len(dele) >= 4:
                                try:
                                    bookinger_dict[noegle] = {
                                        "jaeger_id": int(str(dele[0]).strip()),
                                        "navn": str(dele[1]).strip(),
                                        "tidspunkt": str(dele[2]).strip(),
                                        "notat": str(dele[3]).strip()
                                    }
                                except:
                                    continue
                        elif handling == "AFBESTIL":
                            if noegle in bookinger_dict:
                                del bookinger_dict[noegle]
        return bookinger_dict
    except Exception as e:
        return {}

# Indlæs altid databasen fra skyen live
st.session_state.bookinger = hent_aktuelle_bookinger()

if "jaegere" not in st.session_state:
    st.session_state.jaegere = {
        1: "Lasse Lichon Hesthaven", 2: "Alexander Knudsen", 3: "Thomas Jøns",
        4: "Jørgen Thomsen", 5: "Per Eli Løfqvist", 6: "Peter Aaen",
        7: "Morten Ransborg", 8: "Steffen Carlsen", 9: "Morten Mæng Pedersen",
        10: "Ole Libak Christensen", 11: "Christian Ringstrøm Andersen",
        12: "Tom Erik Houen", 13: "Jan Carstens", 14: "Benjamin Kirkeby G. Carstenskiold",
        15: "Lars Højmose Kristensen", 16: "Peter Hahn Boelt", 17: "Jonathan Brun Sønderbæk",
        18: "Mathies Boelt", 19: "Per Behrmann", 20: "Tonni Bastrup Pedersen",
        21: "Peter Michael Nielsen", 22: "Simon Noer Burkal", 23: "Carsten Bjerregaard",
        24: "Rene' Andersen", 25: "Kristian Hæsum Pedersen"
    }

st.session_state.omraader = {
    1: "Område A", 2: "Område B", 3: "Område C", 4: "Område D", 5: "Område E",
    6: "Område F", 7: "Område G", 8: "Område H", 9: "Område I", 10: "Område J"
}

# --- WEB OVERFLADE ---
st.title("🌲 Ravnkjærgaard - Jagt Booking")
st.write("Hvert område kan maksimalt bookes 2 gange om dagen (Morgen og Aften), og der må kun være 1 jæger pr. område ad gangen.")

fane_book, fane_tjek_dato, fane_fuld_oversigt, fane_regler_info, fane_kontakt = st.tabs([
    "🆕 Opret Booking", "🔍 Tjek Specifik Dato", "📅 Den Fulde Kalenderoversigt & Aflysning", "📜 Priser, Regler & Info", "📞 Medlemsliste & Kontakt"
])
# --- FANE 1: OPRET BOOKING ---
with fane_book:
    st.header("Opret ny jagtreservation")
    
    valgt_jaeger_id = st.selectbox(
        "Vælg dit navn på listen:", 
        options=list(st.session_state.jaegere.keys()),
        format_func=lambda x: f"Nr. {x} - {st.session_state.jaegere[x]}"
    )
    
    valider_id_input = st.text_input("Bekræft beim indtaste dit medlemsnummer (tal):", type="password", key="opret_pin")
    
    valgt_omraade_id = st.selectbox(
        "Vælg jagtområde:", 
        options=list(st.session_state.omraader.keys()),
        format_func=lambda x: st.session_state.omraader[x]
    )
    
    idag = datetime.today().date()
    fjorten_dage_frem = idag + timedelta(days=14)
    
    valgt_dato = st.date_input(
        "Vælg dato for jagten (Maks 14 dage frem):", 
        min_value=idag,
        max_value=fjorten_dage_frem,
        key="dato_valg"
    )
    dato_streng = valgt_dato.strftime("%Y-%m-%d")
    
    valgt_tidspunkt = st.radio("Vælg tidspunkt på dagen:", ["Morgen 🌅", "Aften 🌇"])
    notat_input = st.text_input("Tilføj et notat (valgfrit):", placeholder="F.eks. 'Hund med', 'Riffel'")

    if st.button("Bekræft og book jagt", type="primary"):
        if valider_id_input.strip() != str(valgt_jaeger_id):
            st.error("❌ Fejl: Det indtastede medlemsnummer matcher ikke det valgte navn på listen!")
        else:
            booking_noegle = f"{dato_streng}_{valgt_omraade_id}_{valgt_tidspunkt}"
            
            if booking_noegle in st.session_state.bookinger:
                nuvaerende_booker = st.session_state.bookinger[booking_noegle]["navn"]
                st.error(f"❌ Området er optaget! {st.session_state.omraader[valgt_omraade_id]} er allerede booket {valgt_tidspunkt.lower()} d. {dato_streng} af {nuvaerende_booker}.")
            else:
                nyt_notat = notat_input.strip() if notat_input.strip() else "-"
                data_format = f"{valgt_jaeger_id}|{st.session_state.jaegere[valgt_jaeger_id]}|{valgt_tidspunkt}|{nyt_notat}"
                
                if send_til_google_form(booking_noegle, "BOOK", data_format):
                    st.success(f"✅ Godkendt! {st.session_state.jaegere[valgt_jaeger_id]} har booket {st.session_state.omraader[valgt_omraade_id]}. Opdaterer skyen...")
                    time.sleep(2.0)
                    st.rerun()

# --- FANE 2: TJEK EN SPECIFIK DATO ---
with fane_tjek_dato:
    st.header("Hvem er på jagt denne dag?")
    tjek_dato = st.date_input("Vælg den dato du vil undersøge:", value=datetime.today().date(), key="tjek_dato_valg")
    tjek_dato_streng = tjek_dato.strftime("%Y-%m-%d")
    
    st.write(f"### Status for d. {tjek_dato_streng}:")
    
    data_tjek_liste = []
    for omr_id, omr_navn in st.session_state.omraader.items():
        morgen_noegle = f"{tjek_dato_streng}_{omr_id}_Morgen 🌅"
        aften_noegle = f"{tjek_dato_streng}_{omr_id}_Aften 🌇"
        
        morgen_status = "Ledig 🟢"
        aften_status = "Ledig 🟢"
        
        if morgen_noegle in st.session_state.bookinger:
            morgen_status = f"🔴 {st.session_state.bookinger[morgen_noegle]['navn']} ({st.session_state.bookinger[morgen_noegle]['notat']})"
        if aften_noegle in st.session_state.bookinger:
            aften_status = f"🔴 {st.session_state.bookinger[aften_noegle]['navn']} ({st.session_state.bookinger[aften_noegle]['notat']})"
            
        data_tjek_liste.append({"Jagtområde": omr_navn, "Morgen 🌅": morgen_status, "Aften 🌇": aften_status})
        
    df_tjek = pd.DataFrame(data_tjek_liste)
    st.dataframe(df_tjek, use_container_width=True, hide_index=True)

# --- FANE 3: DEN FULDE KALENDEROVERSIGT & AFLYSNING ---
with fane_fuld_oversigt:
    st.header("Komplet oversigt over alle reservationer")
    
    if not st.session_state.bookinger:
        st.info("Der er i øjeblikket ingen aktive bookinger i systemet.")
    else:
        tabel_data = []
        for noegle, info in list(st.session_state.bookinger.items()):
            dele = noegle.split("_")
            if len(dele) >= 3:
                dato_del = dele
                omraade_id_del = int(dele)
                tid_del = dele
                
                omraade_navn = st.session_state.omraader.get(omraade_id_del, f"Område {omraade_id_del}")
                tabel_data.append({
                    "Nøgle": noegle,
                    "Dato": dato_del,
                    "Tidspunkt": tid_del,
                    "Jagtområde": omraade_navn,
                    "Jæger": f"Nr. {info['jaeger_id']} - {info['navn']}",
                    "Jæger_ID": info['jaeger_id'],
                    "Notat": info["notat"]
                })
        
        if tabel_data:
            df = pd.DataFrame(tabel_data).sort_values(by=["Dato", "Tidspunkt"])
            st.dataframe(df[["Dato", "Tidspunkt", "Jagtområde", "Jæger", "Notat"]], use_container_width=True, hide_index=True)
            
            st.write("---")
            st.subheader("🗑️ Vil du aflyse en booking?")
            
            slet_valg = st.selectbox(
                "Vælg den booking du vil fjerne:",
                options=tabel_data,
                format_func=lambda x: f"{x['Dato']} ({x['Tidspunkt'].lower()}) - {x['Jagtområde']} [{x['Jæger']}]"
                if isinstance(x, dict) else str(x)
            )
            
            slet_id_validering = st.text_input("Indtast dit medlemsnummer for at godkende aflysning:", type="password", key="slet_pin")
            
            if st.button("Slet valgte booking", type="secondary"):
                if isinstance(slet_valg, dict):
                    korrekt_id = str(slet_valg["Jæger_ID"])
                    if slet_id_validering.strip() == korrekt_id:
                        data_afbestil = f"{slet_valg['Jæger_ID']}|-|--|-"
                        if send_til_google_form(slet_valg["Nøgle"], "AFBESTIL", data_afbestil):
                            st.success("📌 Bookingen er blevet slettet!")
                            time.sleep(2.0)
                            st.rerun()
                    else:
                        st.error("❌ Forkert medlemsnummer. Du kan kun slette dine egne bookinger.")

with fane_regler_info:
    st.header("📜 Praktisk information & Jagtregler")
    st.markdown("""
    * **Sikkerhed først:** Vis altid absolut hensyn til sikkerhedszoner og naboskel.
    * **Én jæger pr. område:** Kun én aktiv jæger ad gangen per område.
    * **Bookingbetingelser:** Du kan maksimalt booke en jagt 14 dage frem i tiden.
    """)

with fane_kontakt:
    st.header("📞 Medlemsliste & Kontakt")
    kontakt_liste_visning = []
    for k, v in st.session_state.jaegere.items():
        kontakt_liste_visning.append({"Nr": k, "Navn": v})
    st.dataframe(pd.DataFrame(kontakt_liste_visning), use_container_width=True, hide_index=True)
