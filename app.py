import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import requests
import time

# 1. Konfiguration af hjemmesiden
st.set_page_config(page_title="Ravnkjærgaard - Jagtbooking", page_icon="🌲", layout="centered")

# --- DATABASEFORBINDELSE TIL SHEETDB ---
# FAST RETTELSE: Dit API-ID er nu sat korrekt på plads igen
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
    """Sletter en booking i jeres Google Sheet live baseret på nøglen"""
    try:
        res = requests.delete(f"{SHEETDB_API_URL}/noegle/{noegle}")
        return res.status_code == 200
    except:
        return False

def hent_aktuelle_bookinger():
    """Henter alle bookinger lynhurtigt fra Google Sheet via SheetDB API'en"""
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
    {"Nr": 8, "Navn": "Steffen Carlsen", "Tlf": "53 55 44 94", "E-mail": "steffencarlsen86@gmail.com"},
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
    {"Nr": 23, "Navn": "Carsten Bjerregaard", "Tlf": "30 13 10 26", "E-mail": "Cbj.bjerregaard@gmail.com"},
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
fane_book, fane_hytte, fane_tjek_dato, fane_fuld_oversigt, fane_regler_info, fane_kontakt = st.tabs([
    "🆕 Opret Jagtbooking", "🏠 Book Jagthytte", "🔍 Tjek Specifik Dato", "📅 Den Fulde Kalenderoversigt & Aflysning", "📜 Priser, Regler & Info", "📞 Medlemsliste & Kontakt"
])

# --- FANE 1: OPRET JAGTBOOKING ---
with fane_book:
    st.header("Opret ny jagtreservation")
    st.success(f"✍️ Logget ind som: **{st.session_state.bruger_info['Navn']}**")
    valgt_omraade_id = st.selectbox("Vælg jagtområde:", options=list(st.session_state.omraader.keys()), format_func=lambda x: st.session_state.omraader[x])
    idag = datetime.today().date()
    # FAST RETTELSE: Færdiggjort linjen, som var afbrudt
    valgt_dato = st.date_input("Vælg dato for jagten (Maks 14 dage frem):", min_value=idag, max_value=idag + timedelta(days=14), key="dato_valg")
    dato_streng = valgt_dato.strftime("%Y-%m-%d")
    
    valgt_tidspunkt_visning = st.radio("Vælg tidspunkt på dagen:", ["Morgen 🌅", "Aften 🌇"])
    valgt_tidspunkt = "Morgen" if "Morgen" in valgt_tidspunkt_visning else "Aften"
    notat_input = st.text_input("Tilføj et notat (valgfrit):", placeholder="F.eks. 'Hund med', 'Riffel'", key="jagt_notat")
    
    if st.button("Bekræft og book jagt", type="primary"):
        omr_navn_tekst = st.session_state.omraader[valgt_omraade_id]
        omr_sammensat = omr_navn_tekst.replace(" ", "")
        booking_noegle = f"{dato_streng}_{omr_sammensat}_{valgt_tidspunkt}"
        
        if booking_noegle in st.session_state.bookinger:
            nuvaerende_booker = st.session_state.bookinger[booking_noegle]["navn"]
            st.error(f"❌ Området er optaget! {omr_navn_tekst} er allerede booket {valgt_tidspunkt.lower()} d. {dato_streng} af {nuvaerende_booker}.")
        else:
            nyt_notat = notat_input.strip() if notat_input.strip() else "-"
            
            if send_til_google_sheet(booking_noegle, st.session_state.bruger_info['Nr'], st.session_state.bruger_info['Navn'], valgt_tidspunkt, nyt_notat):
                st.success(f"✅ Godkendt! Din booking er gemt live i skyen for {omr_navn_tekst} d. {dato_streng}.")
                time.sleep(1.5)
                st.rerun()
            else:
                st.error("❌ Fejl: Kunne ikke gemme i databasen. Sørg for at du har genindlæst din app.")
# --- FANE 2: BOOK JAGTHYTTE ---
with fane_hytte:
    st.header("🏠 Reservation af Jagthytten")
    st.info("Hytten bookes altid for hele døgnet ad gangen.")
    
    hytte_dato = st.date_input("Vælg dato for hytte-booking (Maks 14 dage frem):", min_value=idag, max_value=idag + timedelta(days=14), key="hytte_dato_valg")
    hytte_dato_str = hytte_dato.strftime("%Y-%m-%d")
    hytte_notat = st.text_input("Formål med bookingen (valgfrit):", placeholder="F.eks. 'Overnatning', 'Generalforsamling'", key="hytte_notat")
    
    hytte_noegle = f"{hytte_dato_str}_Jagthytte_HeleDagen"
    
    if hytte_noegle in st.session_state.bookinger:
        hytte_booker = st.session_state.bookinger[hytte_noegle]["navn"]
        st.error(f"❌ Hytten er desværre optaget d. {hytte_dato_str}! Den er reserveret af: **{hytte_booker}**.")
    else:
        if st.button("Reserver hytten nu 🔑", type="primary"):
            nyt_hytte_notat = hytte_notat.strip() if hytte_notat.strip() else "Hytte-booking"
            
            if send_til_google_sheet(hytte_noegle, st.session_state.bruger_info['Nr'], st.session_state.bruger_info['Navn'], "Hele døgnet", nyt_hytte_notat):
                st.success(f"🎉 Godkendt! Jagthytten er nu reserveret til dig d. {hytte_dato_str}.")
                time.sleep(1.5)
                st.rerun()
            else:
                st.error("❌ Kunne ikke oprette forbindelse til databasen. Tjek din SheetDB opsætning.")

# --- FANE 3: TJEK DATO ---
with fane_tjek_dato:
    st.header("Hvem er på reviret eller i hytten denne dag?")
    tjek_dato = st.date_input("Vælg den dato du vil undersøge:", value=datetime.today().date(), key="tjek_dato_valg")
    tjek_dato_streng = tjek_dato.strftime("%Y-%m-%d")
    st.write(f"### Status for d. {tjek_dato_streng}:")
    
    hytte_tjek_noegle = f"{tjek_dato_streng}_Jagthytte_HeleDagen"
    if hytte_tjek_noegle in st.session_state.bookinger:
        st.warning(f"🏠 **Jagthytten:** Reserveret af {st.session_state.bookinger[hytte_tjek_noegle]['navn']} ({st.session_state.bookinger[hytte_tjek_noegle]['notat']})")
    else:
        st.success("🏠 **Jagthytten:** Er ledig i dag")
        
    st.write("---")
    
    data_tjek_liste = []
    for omr_id, omr_navn in st.session_state.omraader.items():
        omr_renset_id = omr_navn.replace(" ", "")
        morgen_noegle = f"{tjek_dato_streng}_{omr_renset_id}_Morgen"
        aften_noegle = f"{tjek_dato_streng}_{omr_renset_id}_Aften"
        morgen_status = "Ledig 🟢"
        aften_status = "Ledig 🟢"
        if morgen_noegle in st.session_state.bookinger:
            morgen_status = f"🔴 {st.session_state.bookinger[morgen_noegle]['navn']} ({st.session_state.bookinger[morgen_noegle]['notat']})"
        if aften_noegle in st.session_state.bookinger:
            aften_status = f"🔴 {st.session_state.bookinger[aften_noegle]['navn']} ({st.session_state.bookinger[aften_noegle]['notat']})"
        data_tjek_liste.append({"Jagtområde": omr_navn, "Morgen 🌅": morgen_status, "Aften 🌇": aften_status})
    df_tjek = pd.DataFrame(data_tjek_liste)
    st.dataframe(df_tjek, use_container_width=True, hide_index=True)

# --- FANE 4: OVERSIGT OG AFBESTILLING ---
with fane_fuld_oversigt:
    st.header("Alle aktive bookinger i skyen")
    if st.session_state.bookinger:
        aktive_bookinger_liste = []
        for noegle, info in st.session_state.bookinger.items():
            dele = noegle.split("_")
            if len(dele) == 3:
                dato_samlet = dele
                type_del = dele
                tidspunkt_del = dele
                
                if type_del == "Jagthytte":
                    visnings_navn = "🏠 Jagthytte"
                    tidspunkt_del = "Hele døgnet"
                else:
                    if "Stige" in type_del:
                        visnings_navn = type_del.replace("Stige", "Stige ")
                    elif "Tårn" in type_del:
                        visnings_navn = type_del.replace("Tårn", "Tårn ")
                    elif "Område" in type_del:
                        visnings_navn = type_del.replace("Område", "Område ")
                    else:
                        visnings_navn = type_del
                
                if tidspunkt_del == "HeleDagen":
                    tidspunkt_del = "Hele døgnet"
                
                aktive_bookinger_liste.append({
                    "Nøgle": noegle, 
                    "Dato": dato_samlet, 
                    "Område/Type": visnings_navn,
                    "Tidspunkt": tidspunkt_del, 
                    "Jæger": info["navn"], 
                    "Jæger_ID": info["jaeger_id"], 
                    "Notat": info["notat"]
                })
        if aktive_bookinger_liste:
            df_alle = pd.DataFrame(aktive_bookinger_liste).sort_values(by=["Dato", "Tidspunkt"])
            st.dataframe(df_alle[["Dato", "Område/Type", "Tidspunkt", "Jæger", "Notat"]], use_container_width=True, hide_index=True)
            st.subheader("❌ Aflys en af dine egne bookinger")
            egne_bookinger = df_alle[df_alle["Jæger_ID"] == st.session_state.bruger_info["Nr"]]
            if not egne_bookinger.empty:
                aflys_valg = st.selectbox(
                    "Vælg den reservation du vil slette:", 
                    options=egne_bookinger["Nøgle"].tolist(), 
                    format_func=lambda x: f"{df_alle[df_alle['Nøgle'] == x]['Dato'].values} - {df_alle[df_alle['Nøgle'] == x]['Område/Type'].values} ({df_alle[df_alle['Nøgle'] == x]['Tidspunkt'].values})"
                )
                if st.button("Slet valgte reservation", type="secondary"):
                    if aflyst_i_google_sheet(aflys_valg):
                        st.success("Aflysningen er registreret i skyen! Opdaterer...")
                        time.sleep(1.5)
                        st.rerun()
            else:
                st.info("Du har ikke nogen aktive bookinger i systemet lige nu.")
        else:
            st.info("Der er ikke oprettet nogen aktive bookinger endnu.")
    else:
        st.info("Der er ikke oprettet nogen bookinger i systemet endnu.")

# --- FANE 5: INFO ---
with fane_regler_info:
    st.header("📜 Praktisk information & Jagtregler")
    st.markdown("""
    * **Sikkerhed først:** Vis altid absolut hensyn to sikkerhedszoner og naboskel.
    * **Én jæger pr. område:** Kun én active jæger ad gangen per område.
    * **🏠 Jagthytte regler:** Ryd altid op efter dig selv, vask op og tag dit affald med hjem efter leje.
    * **Bookingbetingelser:** Du kan maksimalt booke en jagt eller hytten 14 dage frem i tiden.
    """)

# --- FANE 6: LISTE ---
with fane_kontakt:
    st.header("📞 Medlemsliste")
    st.dataframe(pd.DataFrame(kontakt_data)[["Nr", "Navn", "Tlf", "E-mail"]], use_container_width=True, hide_index=True)
