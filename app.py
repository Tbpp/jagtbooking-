import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import requests
import time

# 1. Konfiguration af hjemmesiden
st.set_page_config(page_title="Ravnkjærgaard - Jagtbooking", page_icon="🌲", layout="centered")

# --- OPPDATERET DATABASEFORBINDELSE TIL DIT NYE SHEET ---
SHEETDB_API_URL = "https://sheetdb.io/api/v1/586zzfgt2797k"

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

# --- LIVE DATA MED CACHE (HENTER KUN VED RELEVANTE ÆNDRINGER) ---
@st.cache_data(ttl=600)
def hent_aktuelle_bookinger():
    """Henter alle jagtbookinger lynhurtigt fra det nye sheet (Cachet i op til 10 min)"""
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
    return {}

# --- FUNKTIONER TIL HYTTE-FANEN ---
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

@st.cache_data(ttl=600)
def hent_hytte_bookinger():
    """Henter alle hyttebookinger live fra hytte-fanen (Cachet i op til 10 min)"""
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
    return {}

# Indlæs data fra cache i session state, hvis de ikke allerede er indlæst
if "bookinger" not in st.session_state:
    st.session_state.bookinger = hent_aktuelle_bookinger()
if "hytte_bookinger" not in st.session_state:
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
    else:
        if indtastet_tlf:
            st.warning("⚠️ Telefonnummeret skal være præcis 8 tal.")
        st.stop()
# --- SIDEBAR & MANUEL SYNKRONISERING ---
st.sidebar.write(f"Logget ind som:\n**{st.session_state.bruger_info['Navn']}**")

# Manuel genopfriskningsknap i sidebaren, hvis der laves manuelle rettelser direkte i Google Sheets
if st.sidebar.button("🔄 Synkroniser med Google Sheets"):
    st.cache_data.clear()
    st.session_state.bookinger = hent_aktuelle_bookinger()
    st.session_state.hytte_bookinger = hent_hytte_bookinger()
    st.toast("Data synkroniseret direkte fra regnearket!", icon="📥")
    time.sleep(0.5)
    st.rerun()

if st.sidebar.button("Log ud"):
    st.session_state.logget_ind = False
    st.session_state.bruger_info = None
    st.rerun()

st.title("🌲 Ravnkjærgaard - Jagt & Hytte")

# --- FANER ---
fane_book, fane_hytte, fane_tjek_dato, fane_fuld_oversigt, fane_regler_info = st.tabs([
    "🆕 Opret Jagtbooking", 
    "🏠 Book Jagthytte", 
    "🔍 Tjek Specifik Dato", 
    "📅 Den Fulde Kalenderoversigt & Aflysning", 
    "📜 Priser, Regler & Info"
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
            optaget_af = st.session_state.bookinger[genereret_noegle]["navn"]
            st.error(f"❌ Dette område er allerede booket til {valgt_tidspunkt.lower()} af **{optaget_af}**.")
        else:
            succes = send_til_google_sheet(
                noegle=genereret_noegle,
                jaeger_id=st.session_state.bruger_info.get("ID", 0),
                navn=st.session_state.bruger_info["Navn"],
                tidspunkt=valgt_tidspunkt,
                notat=bruger_notat
            )
            if succes:
                st.success(f"🎉 Booking bekræftet! {st.session_state.omraader[valgt_omraade_id]} den {valgt_dato} ({valgt_tidspunkt}).")
                # Rydder den gamle cache og tvinger en frisk database-opdatering med det samme
                st.cache_data.clear() 
                st.session_state.bookinger = hent_aktuelle_bookinger()
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Fejl under lagring i Google Sheet. Prøv igen.")

# --- FANE 2: BOOK JAGTHYTTE ---
with fane_hytte:
    st.header("Book Jagthytten")
    hytte_dato = st.date_input("Vælg dato for hytteovernatning:", min_value=idag, key="hytte_dato_input")
    hytte_noegle = f"hytte_{hytte_dato}"
    
    if st.button("Book hytten", type="primary"):
        if hytte_noegle in st.session_state.hytte_bookinger:
            hytte_ejer = st.session_state.hytte_bookinger[hytte_noegle]["navn"]
            st.error(f"❌ Hytten er allerede booket denne dag af **{hytte_ejer}**.")
        else:
            succes_hytte = send_hytte_til_google_sheet(
                noegle=hytte_noegle,
                jaeger_id=st.session_state.bruger_info.get("ID", 0),
                navn=st.session_state.bruger_info["Navn"],
                dato=str(hytte_dato)
            )
            if succes_hytte:
                st.success(f"🏡 Jagthytten er nu booket til dig den {hytte_dato}!")
                st.cache_data.clear()
                st.session_state.hytte_bookinger = hent_hytte_bookinger()
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Fejl under lagring af hyttebooking. Prøv igen.")

# --- FANE 3: TJEK SPECIFIK DATO ---
with fane_tjek_dato:
    st.header("Undersøg ledige pladser på en bestemt dag")
    tjek_dato = st.date_input("Vælg den dato du vil undersøge:", value=idag, key="tjek_dato_input")
    
    st.subheader(f"Status for d. {tjek_dato}")
    
    hytte_tjek_noegle = f"hytte_{tjek_dato}"
    if hytte_tjek_noegle in st.session_state.hytte_bookinger:
        st.info(f"🏡 **Jagthytten:** Booket af {st.session_state.hytte_bookinger[hytte_tjek_noegle]['navn']}")
    else:
        st.success("🏡 **Jagthytten:** Ledig")
        
    st.write("---")
    
    tjek_data = []
    for o_id, o_navn in st.session_state.omraader.items():
        morgen_noegle = f"{tjek_dato}_{o_id}_Morgen"
        aften_noegle = f"{tjek_dato}_{o_id}_Aften"
        
        morgen_status = st.session_state.bookinger[morgen_noegle]["navn"] if morgen_noegle in st.session_state.bookinger else "🔴 Ledig"
        aften_status = st.session_state.bookinger[aften_noegle]["navn"] if aften_noegle in st.session_state.bookinger else "🔴 Ledig"
        
        tjek_data.append({
            "Område": o_navn,
            "Morgen": morgen_status,
            "Aften": aften_status
        })
        
    st.table(pd.DataFrame(tjek_data))

# --- FANE 4: FULL OVERSIGT & AFLYSNING ---
with fane_fuld_oversigt:
    st.header("Administrer og se alle reservationer")
    st.subheader("Dine personlige jagt- og hyttebookinger")
    bruger_navn = st.session_state.bruger_info["Navn"]
    
    egne_jagter = {k: v for k, v in st.session_state.bookinger.items() if v["navn"] == bruger_navn}
    if egne_jagter:
        for noegle, info in egne_jagter.items():
            dele = noegle.split("_")
            dato_str = dele[0]
            omr_navn = st.session_state.omraader.get(int(dele[1]), "Ukendt område")
            tid = info["tidspunkt"]
            
            col1, col2 = st.columns([3, 1])
            col1.write(f"🏹 **{omr_navn}** - d. {dato_str} ({tid}) — *Notat: {info['notat']}*")
            if col2.button("Aflys", key=f"aflys_jagt_{noegle}"):
                if aflyst_i_google_sheet(noegle):
                    st.success("Booking aflyst!")
                    st.cache_data.clear()
                    st.session_state.bookinger = hent_aktuelle_bookinger()
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Fejl ved aflysning.")
    else:
        st.write("Du har ingen aktive jagtbookinger.")
        
    egne_hytter = {k: v for k, v in st.session_state.hytte_bookinger.items() if v["navn"] == bruger_navn}
    if egne_hytter:
        st.write("---")
        for noegle, info in egne_hytter.items():
            col1, col2 = st.columns([3, 1])
            col1.write(f"🏡 **Jagthytten** - d. {info['dato']}")
            if col2.button("Aflys", key=f"aflys_hytte_{noegle}"):
                if aflyst_hytte_i_google_sheet(noegle):
                    st.success("Hyttebooking aflyst!")
                    st.cache_data.clear()
                    st.session_state.hytte_bookinger = hent_hytte_bookinger()
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Fejl ved aflysning.")
                    
    st.write("---")
    st.subheader("Alle fremtidige bookinger i systemet")
    
    alle_data = []
    for noegle, info in st.session_state.bookinger.items():
        try:
            dele = noegle.split("_")
            alle_data.append({
                "Type": "Jagt",
                "Dato": dele[0],
                "Område/Hytte": st.session_state.omraader.get(int(dele[1]), "Ukendt"),
                "Tid": info["tidspunkt"],
                "Jæger": info["navn"],
                "Notat": info["notat"]
            })
        except:
            pass
            
    for noegle, info in st.session_state.hytte_bookinger.items():
        alle_data.append({
            "Type": "Jagthytte",
            "Dato": info["dato"],
            "Område/Hytte": "Jagthytten 🏡",
            "Tid": "Hele døgnet",
            "Jæger": info["navn"],
            "Notat": "-"
        })
        
    if alle_data:
        df_alle = pd.DataFrame(alle_data).sort_values(by="Dato")
        st.dataframe(df_alle, use_container_width=True)
    else:
        st.write("Der er ingen registrerede bookinger i systemet lige nu.")

# --- FANE 5: REGLER & INFO ---
with fane_regler_info:
    st.header("Praktisk information & Jagtregler")
    st.markdown("""
    ### 📜 Generelle Bookingregler
    * **Tidsbegrænsning:** Du kan maksimalt booke jagtområder **14 dage frem** i tiden.
    * **Gæster:** Hvis du har en gæst med, bedes dette noteres i feltet 'Notat' ved oprettelse.
    * **Respekt:** Aflys i god tid, hvis du alligevel bliver forhindret, så andre kan få glæde af pladsen.
    
    ### 🏡 Regler for Jagthytten
    * Hytten skal efterlades i rengjort og pæn stand.
    * Husk at slukke for lys og varme, når du forlader hytten.
    
    ### 📞 Support og Kontakt
    Hvis du oplever tekniske problemer med bookingsystemet, bedes du kontakte jagtforeningens administrator.
    """)
