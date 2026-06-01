import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import requests
import time

# 1. Konfiguration af hjemmesiden
st.set_page_config(page_title="Ravnkjærgaard - Jagtbooking", page_icon="🌲", layout="centered")

# --- NY DATABASEFORBINDELSE TIL JERS NYE SHEET ---
SHEETDB_API_URL = "https://sheetdb.io"

def send_til_google_sheet(noegle, jaeger_id, navn, tidspunkt, notat):
    """Skriver en ny booking direkte ind i jeres Google Sheet"""
    payload = {
        "data": [{
            "noegle": str(noegle).strip(),
            "jaeger_id": str(jaeger_id).strip(),
            "navn": str(navn).strip(),
            "tidspunkt": str(tidspunkt).strip(),
            "notat": str(notat).strip()
        }]
    }
    try:
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        res = requests.post(SHEETDB_API_URL, json=payload, headers=headers)
        return res.status_code == 201
    except:
        return False

def aflyst_i_google_sheet(noegle):
    """Sletter en booking live baseret på nøglen"""
    try:
        res = requests.delete(f"{SHEETDB_API_URL}/noegle/{noegle}")
        return res.status_code == 200
    except:
        return False

def hent_aktuelle_bookinger():
    """Henter alle bookinger lynhurtigt og fejlfrit fra det nye sheet"""
    try:
        res = requests.get(f"{SHEETDB_API_URL}?cache_buster={int(time.time())}")
        bookinger_dict = {}
        if res.status_code == 200:
            data = res.json()
            if isinstance(data, dict) and "error" in data:
                return {}
            if isinstance(data, list):
                for række in data:
                    if "noegle" in række and række["noegle"] and str(række["noegle"]).strip() != "":
                        n_noegle = str(række["noegle"]).strip()
                        bookinger_dict[n_noegle] = {
                            "jaeger_id": int(række["jaeger_id"]) if "jaeger_id" in række and række["jaeger_id"] and str(række["jaeger_id"]).isdigit() else 0,
                            "navn": str(række["navn"]) if "navn" in række else "Ukendt",
                            "tidspunkt": str(række["tidspunkt"]) if "tidspunkt" in række else "Morgen",
                            "notat": str(række["notat"]) if "notat" in række and pd.notna(række["notat"]) else "-"
                        }
        return bookinger_dict
    except:
        return {}

# Indlæs altid de allernyeste bookinger live fra skyen ved opdatering
st.session_state.bookinger = hent_aktuelle_bookinger()

# --- STYLING OG BAGGRUND ---
baggrunds_css = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://unsplash.com");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
.stTabs [data-baseweb="tab-panel"] {
    background-color: rgba(255, 255, 255, 0.95);
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
}
h1, h2, h3, p, label {
    color: #1c2e15;
}
</style>
"""
st.markdown(baggrunds_css, unsafe_allow_html=True)

# --- MEDLEMSDATA ---
kontakt_data = [
    {"Nr": 1, "Navn": "Lasse Lichon Hesthaven", "Tlf": "28 57 23 62", "E-mail": "lichon10@hotmail.com"},
    {"Nr": 2, "Navn": "Alexander Knudsen", "Tlf": "31 14 94 08", "E-mail": "alekproscore@hotmail.com"},
    {"Nr": 3, "Navn": "Thomas Jøns", "Tlf": "42 17 78 07", "E-mail": "cuba_joens@hotmail.com"},
    {"Nr": 4, "Navn": "Jørgen Thomsen", "Tlf": "49 40 50 64", "E-mail": "thomsen777@gmail.com"},
    {"Nr": 5, "Navn": "Per Eli Løfqvist", "Tlf": "30 50 32 12", "E-mail": "loefqvist@gmail.com"},
    {"Nr": 6, "Navn": "Peter Aaen", "Tlf": "20 92 34 14", "E-mail": "peter.aaen46@gmail.com"},
    {"Nr": 7, "Navn": "Morten Ransborg", "Tlf": "20 18 95 91", "E-mail": "morten@ransborg.net"},
    {"Nr": 8, "Navn": "Steffen Carlsen", "Tlf": "53 55 49 94", "E-mail": "steffencarlsen86@gmail.com"},
    {"Nr": 9, "Navn": "Morten Mæng Pedersen", "Tlf": "28 91 69 15", "E-mail": "mortenmaeng@hotmail.com"},
    {"Nr": 10, "Navn": "Ole Libak Christensen", "Tlf": "31 50 35 55", "E-mail": "ole.libak@gmail.com"},
    {"Nr": 11, "Navn": "Christian Ringstrøm Andersen", "Tlf": "61 26 17 38", "E-mail": "Christian.ringstroem@gmail.com"},
    {"Nr": 12, "Navn": "Tom Erik Houen", "Tlf": "40 59 10 59", "E-mail": "tomhouen@gmail.com"},
    {"Nr": 13, "Navn": "Jan Carstens", "Tlf": "61 80 60 00", "E-mail": "janc280656@gmail.com"},
    {"Nr": 14, "Navn": "Benjamin Kirkeby G. Carstenskiold", "Tlf": "31 72 43 02", "E-mail": "Hj01bg@gmail.com"},
    {"Nr": 15, "Navn": "Lars Højmose Kristensen", "Tlf": "30 24 51 07", "E-mail": "lakris@proton.me"},
    {"Nr": 16, "Navn": "Peter Hahn Boelt", "Tlf": "60 67 50 19", "E-mail": "peterhbmail@proton.me"},
    {"Nr": 17, "Navn": "Jonathan Brun Sønderbæk", "Tlf": "20 60 89 35", "E-mail": "Jona811k@yahoo.dk"},
    {"Nr": 18, "Navn": "Mathies Boelt", "Tlf": "23 96 83 72", "E-mail": "Mathies-boelt@hotmail.com"},
    {"Nr": 19, "Navn": "Per Behrmann", "Tlf": "50 58 17 41", "E-mail": "perbehrmann@hotmail.com"},
    {"Nr": 20, "Navn": "Tonni Bastrup Pedersen", "Tlf": "23 47 74 02", "E-mail": "tonnibastrup@gmail.com"},
    {"Nr": 21, "Navn": "Peter Michael Nielsen", "Tlf": "23 72 62 25", "E-mail": "pmn@bbnpost.dk"},
    {"Nr": 22, "Navn": "Simon Noer Burkal", "Tlf": "28 74 70 45", "E-mail": "Simon@burkal.dk"},
    {"Nr": 23, "Navn": "Carsten Bjerregaard", "Tlf": "30 13 10 27", "E-mail": "Cbj.bjerregaard@gmail.com"},
    {"Nr": 24, "Navn": "Rene' Andersen", "Tlf": "22 44 62 22", "E-mail": "Rahunter13@gmail.com"},
    {"Nr": 25, "Navn": "Kristian Hæsum Pedersen", "Tlf": "60 19 06 26", "E-mail": "Khaesum@gmail.com"}
]

# --- OMRAADE KONFIGURATION ---
st.session_state.omraader = {
    1: "Stige 1", 2: "Stige 2", 3: "Stige 3", 4: "Stige 4", 5: "Stige 5", 
    6: "Tårn 1", 7: "Tårn 2", 8: "Tårn 3", 9: "Tårn 4", 10: "Tårn 5",
    11: "Område F", 12: "Område G", 13: "Område H", 14: "Område I", 15: "Område J"
}

if "logget_ind" not in st.session_state:
    st.session_state.logget_ind = False
if "bruger_info" not in st.session_state:
    st.session_state.bruger_info = None

# --- ADGANGSKONTROL ---
if not st.session_state.logget_ind:
    st.title("🔒 Ravnkjærgaard - Adgangskontrol")
    st.write("Indtast dit registrerede telefonnummer. Systemet logger dig ind automatisk.")
    indtastet_tlf = st.text_input("Telefonnummer (8 tal):", placeholder="Skriv dit tlf. nr. her", key="login_input")
    renset_indtastet = indtastet_tlf.replace(" ", "").replace("+45", "").strip()
    if len(renset_indtastet) == 8:
        fundet_bruger = None
        for medlem in kontakt_data:
            if renset_indtastet == medlem["Tlf"].replace(" ", "").strip():
                fundet_bruger = medlem
                break
        if fundet_bruger:
            st.session_state.logget_ind = True
            st.session_state.bruger_info = fundet_bruger
            st.rerun()
        else:
            st.error("❌ Telefonnummeret blev ikke fundet på medlemslisten. Tjek indtastningen.")
    st.stop()

# --- SIDEBAR & LOGUD ---
st.sidebar.write(f"Logget ind som:\n**{st.session_state.bruger_info['Navn']}**")
if st.sidebar.button("Log ud"):
    st.session_state.logget_ind = False
    st.session_state.bruger_info = None
    st.rerun()
st.title("🌲 Ravnkjærgaard - Jagt & Hytte")

# --- FANER ---
fane_book, fane_hytte, fane_tjek_dato, fane_fuld_oversigt, fane_regler_info = st.tabs([
    "🆕 Opret Jagtbooking", "🏠 Book Jagthytte", "🔍 Tjek Specifik Dato", "📅 Den Fulde Kalenderoversigt & Aflysning", "📜 Priser, Regler & Info"
])

# --- FANE 1: OPRET JAGTBOOKING ---
with fane_book:
    st.header("Opret ny jagtreservation")
    st.success(f"✍️ Logget ind som: **{st.session_state.bruger_info['Navn']}**")
    
    valgt_omraade_id = st.selectbox("Vælg jagtområde:", options=list(st.session_state.omraader.keys()), format_func=lambda x: st.session_state.omraader[x])
    
    idag = datetime.today().date()
    maks_dato = idag + timedelta(days=14)
    valgt_dato = st.date_input("Vælg dato for jagten (Maks 14 dage frem):", min_value=idag, max_value=maks_dato, value=idag)
    
    valgt_tidspunkt = st.radio("Vælg tidspunkt:", ["Morgen", "Aften"])
    bruger_notat = st.text_input("Evt. notat (f.eks. 'Gæst med', 'Rifeljagt'):", value="-")
    
    genereret_noegle = f"{valgt_dato}_{valgt_omraade_id}_{valgt_tidspunkt}"
    
    if st.button("Bekræft og opret booking", type="primary"):
        if genereret_noegle in st.session_state.bookinger:
            st.error(f"❌ {st.session_state.omraader[valgt_omraade_id]} er allerede booket {valgt_tidspunkt.lower()} d. {valgt_dato}!")
        else:
            med_succes = send_til_google_sheet(
                noegle=genereret_noegle,
                jaeger_id=st.session_state.bruger_info["Nr"],
                navn=st.session_state.bruger_info["Navn"],
                tidspunkt=f"{valgt_dato} ({valgt_tidspunkt})",
                notat=bruger_notat
            )
            if med_succes:
                st.success("🎉 Din booking er gemt i systemet!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Kunne ikke oprette forbindelse til databasen. Prøv igen.")

# --- FANE 2: BOOK JAGTHYTTE ---
with fane_hytte:
    st.header("🏠 Booking af Jagthytten")
    st.info("Denne funktion kan udvides med separat tabel i jeres sheet til overnatninger.")
    st.write("Kontakt formanden eller brug det fælles notatfelt, hvis hytten ønskes reserveret til selskaber.")

# --- FANE 3: TJEK SPECIFIK DATO ---
with fane_tjek_dato:
    st.header("🔍 Se ledige og bookede områder")
    tjek_dato = st.date_input("Vælg den dato du vil undersøge:", value=idag)
    st.write(f"### Oversigt for d. {tjek_dato}")
    
    data_oversigt = []
    for o_id, o_navn in st.session_state.omraader.items():
        noegle_morgen = f"{tjek_dato}_{o_id}_Morgen"
        noegle_aften = f"{tjek_dato}_{o_id}_Aften"
        
        status_morgen = st.session_state.bookinger[noegle_morgen]["navn"] if noegle_morgen in st.session_state.bookinger else "🟢 Ledig"
        status_aften = st.session_state.bookinger[noegle_aften]["navn"] if noegle_aften in st.session_state.bookinger else "🟢 Ledig"
        
        data_oversigt.append({
            "Område": o_navn,
            "Morgen (Solopgang)": status_morgen,
            "Aften (Solnedgang)": status_aften
        })
        
    df_dag = pd.DataFrame(data_oversigt)
    st.dataframe(df_dag, use_container_width=True, hide_index=True)

# --- FANE 4: DEN FULDE KALENDEROVERSIGT & AFLYSNING ---
with fane_fuld_oversigt:
    st.header("📅 Alle aktive reservationer")
    
    if not st.session_state.bookinger:
        st.info("Der er ingen registrerede bookinger i systemet lige nu.")
    else:
        fuld_liste = []
        for noegle, info in st.session_state.bookinger.items():
            fuld_liste.append({
                "Nøgle": noegle,
                "Jæger ID": info["jaeger_id"],
                "Navn": info["navn"],
                "Tidspunkt & Dato": info["tidspunkt"],
                "Notat": info["notat"]
            })
        
        df_alle = pd.DataFrame(fuld_liste)
        st.dataframe(df_alle.drop(columns=["Nøgle"]), use_container_width=True, hide_index=True)
        
        st.write("---")
        st.subheader("❌ Aflys en af dine reservationer")
        
        mine_bookinger = {k: v for k, v in st.session_state.bookinger.items() if v["jaeger_id"] == st.session_state.bruger_info["Nr"]}
        
        if not mine_bookinger:
            st.write("Du har ingen aktive reservationer at aflyse.")
        else:
            valgt_aflys_noegle = st.selectbox(
                "Vælg den reservation du vil slette:",
                options=list(mine_bookinger.keys()),
                format_func=lambda x: f"{mine_bookinger[x]['tidspunkt']} - {mine_bookinger[x]['notat']}"
            )
            
            if st.button("Slet denne booking", type="secondary"):
                if aflyst_i_google_sheet(valgt_aflys_noegle):
                    st.success("🗑️ Reservationen er blevet slettet!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Kunne ikke slette reservationen. Prøv igen.")

# --- FANE 5: REGLER & INFO ---
with fane_regler_info:
    st.header("📜 Priser, Regler & Praktisk Info")
    st.markdown("""
    * **Tidsbegrænsning**: Du kan højst booke et jagtområde **14 dage frem** i tiden.
    * **Kvoter**: Husk at registrere alt nedlagt vildt til bestyrelsen umiddelbart efter jagten.
    * **Gæster**: Hvis du har gæster med, skal det noteres i feltet ved oprettelse.
    * **Aflysning**: Slet din booking i god tid, hvis du bliver forhindret, så en anden kan få pladsen.
    """)
