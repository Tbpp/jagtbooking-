import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import requests
import time

# 1. Konfiguration af hjemmesiden
st.set_page_config(page_title="Ravnkjærgaard - Jagtbooking", page_icon="🌲", layout="centered")

# --- DATABASEFORBINDELSE TIL SHEETDB ---
SHEETDB_API_URL = "https://sheetdb.io"

def send_til_google_sheet(noegle, jaeger_id, navn, tidspunkt, notat):
    """Skriver en ny jagtbooking ind i jeres Google Sheet (Ark1)"""
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
    """Sletter en jagtbooking live baseret på nøglen"""
    try:
        res = requests.delete(f"{SHEETDB_API_URL}/noegle/{noegle}")
        return res.status_code == 200
    except:
        return False

def hent_aktuelle_bookinger():
    """Henter alle jagtbookinger lynhurtigt fra det nye sheet"""
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

# --- FUNKTIONER TIL HYTTE-FANEN (LØSNING B) ---
def send_hytte_til_google_sheet(noegle, jaeger_id, navn, dato):
    """Skriver en ny hyttebooking ind i fanebladet hytte"""
    payload = {
        "data": [{
            "noegle": str(noegle).strip(),
            "jaeger_id": str(jaeger_id).strip(),
            "navn": str(navn).strip(),
            "dato": str(dato).strip()
        }]
    }
    try:
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        res = requests.post(f"{SHEETDB_API_URL}?sheet=hytte", json=payload, headers=headers)
        return res.status_code == 201
    except:
        return False

def aflyst_hytte_i_google_sheet(noegle):
    """Sletter en hyttebooking live fra hytte-fanen"""
    try:
        res = requests.delete(f"{SHEETDB_API_URL}/noegle/{noegle}?sheet=hytte")
        return res.status_code == 200
    except:
        return False

def hent_hytte_bookinger():
    """Henter alle hyttebookinger live fra hytte-fanen"""
    try:
        res = requests.get(f"{SHEETDB_API_URL}?sheet=hytte&cache_buster={int(time.time())}")
        hytte_dict = {}
        if res.status_code == 200:
            data = res.json()
            if isinstance(data, list):
                for række in data:
                    if "noegle" in række and række["noegle"]:
                        hytte_dict[str(række["noegle"]).strip()] = {
                            "jaeger_id": int(række["jaeger_id"]) if "jaeger_id" in række and str(række["jaeger_id"]).isdigit() else 0,
                            "navn": str(række["navn"]) if "navn" in række else "Ukendt",
                            "dato": str(række["dato"]) if "dato" in række else ""
                        }
        return hytte_dict
    except:
        return {}

# Indlæs data live fra skyen ved opdatering
st.session_state.bookinger = hent_aktuelle_bookinger()
st.session_state.hytte_bookinger = hent_hytte_bookinger()

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

# --- SIKKER MEDLEMSDATA FRA STREAMLIT SECRETS ---
try:
    kontakt_data = st.secrets["medlemmer"]
except:
    st.error("❌ Fejl: Medlemslisten kunne ikke hentes fra appens Secrets indstillinger.")
    st.stop()

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
            if renset_indtastet == str(medlem["Tlf"]).replace(" ", "").strip():
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
    st.header("🏠 Reserver Jagthytten til overnatning")
    st.write("Her kan du booke hele hytten til overnatning eller arrangementer.")
    
    maks_hytte_dato = idag + timedelta(days=60)
    valgt_hytte_dato = st.date_input("Vælg dato for hytte-reservation:", min_value=idag, max_value=maks_hytte_dato, value=idag, key="hytte_dato_input")
    hytte_noegle = f"hytte_{valgt_hytte_dato}"
    
    if st.button("Book hytten på denne dato", type="primary", key="hytte_book_knap"):
        if hytte_noegle in st.session_state.hytte_bookinger:
            st.error(f"❌ Jagthytten er allerede reserveret d. {valgt_hytte_dato} af {st.session_state.hytte_bookinger[hytte_noegle]['navn']}.")
        else:
            med_succes = send_hytte_til_google_sheet(
                noegle=hytte_noegle,
                jaeger_id=st.session_state.bruger_info["Nr"],
                navn=st.session_state.bruger_info["Navn"],
                dato=str(valgt_hytte_dato)
            )
            if med_succes:
                st.success(f"🎉 Jagthytten er nu reserveret til dig d. {valgt_hytte_dato}!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Kunne ikke oprette hyttebooking. Prøv igen.")
                
    st.write("---")
    st.subheader("📅 Aktuelle reservationer af hytten")
    
    if not st.session_state.hytte_bookinger:
        st.info("Der er i øjeblikket ingen reservationer af jagthytten.")
    else:
        hytte_liste = []
        for noegle, info in st.session_state.hytte_bookinger.items():
            hytte_liste.append({
                "Nøgle": noegle,
                "Navn": info["navn"],
                "Reserveret dato": info["dato"],
                "jaeger_id": info["jaeger_id"]
            })
        
        df_hytte = pd.DataFrame(hytte_liste)
        df_hytte = df_hytte.sort_values(by="Reserveret dato")
        st.dataframe(df_hytte.drop(columns=["Nøgle", "jaeger_id"]), use_container_width=True, hide_index=True)
        
        st.write("---")
        st.subheader("🗑️ Aflys din hytte-reservation")
        mine_hytte_bookinger = {k: v for k, v in st.session_state.hytte_bookinger.items() if v["jaeger_id"] == st.session_state.bruger_info["Nr"]}
        
        if not mine_hytte_bookinger:
            st.write("Du har ingen aktive hytte-reservationer.")
        else:
            valgt_aflys_hytte = st.selectbox(
                "Vælg den hytte-dato du vil aflyse:",
                options=list(mine_hytte_bookinger.keys()),
                format_func=lambda x: f"Dato: {mine_hytte_bookinger[x]['dato']}"
            )
            if st.button("Annuller hytte-reservation", type="secondary"):
                if aflyst_hytte_i_google_sheet(valgt_aflys_hytte):
                    st.success("🗑️ Din hytte-reservation er blevet slettet!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Kunne ikke slette reservationen. Prøv igen.")

# --- FANE 3: TJEK SPECIFIK DATO ---
with fane_tjek_dato:
    st.header("🔍 Se ledige og bookede områder")
    tjek_dato = st.date_input("Vælg den dato du vil undersøge:", value=idag, key="tjek_dato_input")
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
    * **Hyttebooking**: Jagthytten kan reserveres helt op til **60 dage frem** i tiden.
    * **Kvoter**: Husk at registrere alt nedlagt vildt til bestyrelsen umiddelbart efter jagten.
    * **Gæster**: Hvis du har gæster med, skal det noteres i feltet ved oprettelse.
    * **Aflysning**: Slet din booking i god tid, hvis du bliver forhindret, så en anden kan få pladsen.
    """)
