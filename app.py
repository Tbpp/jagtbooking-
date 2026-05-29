import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import requests

# 1. Konfiguration af hjemmesiden
st.set_page_config(page_title="Ravnkjærgaard - Jagtbooking", page_icon="🌲", layout="centered")

# --- FORBINDELSE TIL GOOGLE SHEET & FORM ---
GOOGLE_SHEET_URL = "https://google.com"
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
                    if pd.notna(row[noegle_col[0]]) and noegle != "" and noegle != "nan":
                        if handling == "BOOK" and "|" in data_felt:
                            dele = data_felt.split("|")
                            if len(dele) >= 4:
                                bookinger_dict[noegle] = {
                                    "jaeger_id": int(dele[0]),
                                    "navn": dele[1],
                                    "tidspunkt": dele[2],
                                    "notat": dele[3]
                                }
                        elif handling == "AFBESTIL":
                            if noegle in bookinger_dict:
                                del bookinger_dict[noegle]
        return bookinger_dict
    except Exception as e:
        return {}

st.session_state.bookinger = hent_aktuelle_bookinger()

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

st.session_state.omraader = {
    1: "Område A", 2: "Område B", 3: "Område C", 4: "Område D", 5: "Område E",
    6: "Område F", 7: "Område G", 8: "Område H", 9: "Område I", 10: "Område J"
}
if "logget_ind" not in st.session_state:
    st.session_state.logget_ind = False
if "bruger_info" not in st.session_state:
    st.session_state.bruger_info = None

if not st.session_state.logget_ind:
    st.title("🔒 Ravnkjærgaard - Adgangskontrol")
    st.write("Indtast dit registrerede telefonnummer. Systemet logger dig ind automatisk.")
    indtastet_tlf = st.text_input("Telefonnummer (8 tal):", placeholder="Skriv dit tlf. nr. her", key="login_input")
    renset_indtastet = indtastet_tlf.replace(" ", "").strip()
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

st.sidebar.write(f"Logget ind som:\n**{st.session_state.bruger_info['Navn']}**")
if st.sidebar.button("Log ud"):
    st.session_state.logget_ind = False
    st.session_state.bruger_info = None
    st.rerun()

st.title("🌲 Ravnkjærgaard - Jagt Booking")

fane_book, fane_tjek_dato, fane_fuld_oversigt, fane_regler_info, fane_kontakt = st.tabs([
    "🆕 Opret Booking", "🔍 Tjek Specifik Dato", "📅 Den Fulde Kalenderoversigt & Aflysning", "📜 Priser, Regler & Info", "📞 Medlemsliste & Kontakt"
])

with fane_book:
    st.header("Opret ny jagtreservation")
    st.success(f"✍️ Logget ind som: **{st.session_state.bruger_info['Navn']}**")
    valgt_omraade_id = st.selectbox("Vælg jagtområde:", options=list(st.session_state.omraader.keys()), format_func=lambda x: st.session_state.omraader[x])
    idag = datetime.today().date()
    valgt_dato = st.date_input("Vælg dato for jagten (Maks 14 dage frem):", min_value=idag, max_value=idag + timedelta(days=14), key="dato_valg")
    dato_streng = valgt_dato.strftime("%Y-%m-%d")
    valgt_tidspunkt = st.radio("Vælg tidspunkt på dagen:", ["Morgen 🌅", "Aften 🌇"])
    notat_input = st.text_input("Tilføj et notat (valgfrit):", placeholder="F.eks. 'Hund med', 'Riffel'")
    if st.button("Bekræft og book jagt", type="primary"):
        booking_noegle = f"{dato_streng}_{valgt_omraade_id}_{valgt_tidspunkt}"
        if booking_noegle in st.session_state.bookinger:
            nuvaerende_booker = st.session_state.bookinger[booking_noegle]["navn"]
            st.error(f"❌ Området er optaget! {st.session_state.omraader[valgt_omraade_id]} er allerede booket {valgt_tidspunkt.lower()} d. {dato_streng} af {nuvaerende_booker}.")
        else:
            nyt_notat = notat_input.strip() if notat_input.strip() else "-"
            data_format = f"{st.session_state.bruger_info['Nr']}|{st.session_state.bruger_info['Navn']}|{valgt_tidspunkt}|{nyt_notat}"
            if send_til_google_form(booking_noegle, "BOOK", data_format):
                st.success(f"✅ Godkendt! Din booking er gemt i skyen for {st.session_state.omraader[valgt_omraade_id]} d. {dato_streng}.")
                st.rerun()

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

with fane_fuld_oversigt:
    st.header("Alle aktive bookinger i skyen")
    if st.session_state.bookinger:
        aktive_bookinger_liste = []
        for noegle, info in st.session_state.bookinger.items():
            dele = noegle.split("_")
            if len(dele) >= 3:
                dato_samlet = f"{dele[0]}-{dele[1]}-{dele[2]}"
                aktive_bookinger_liste.append({
                    "Nøgle": noegle, 
                    "Dato": dato_samlet, 
                    "Område": st.session_state.omraader.get(int(dele[1]), "Ukendt"),
                    "Tidspunkt": dele[2], 
                    "Jæger": info["navn"], 
                    "Jæger_ID": info["jaeger_id"], 
                    "Notat": info["notat"]
                })
        if aktive_bookinger_liste:
            df_alle = pd.DataFrame(aktive_bookinger_liste).sort_values(by=["Dato", "Tidspunkt"])
            st.dataframe(df_alle[["Dato", "Område", "Tidspunkt", "Jæger", "Notat"]], use_container_width=True, hide_index=True)
            st.subheader("❌ Aflys en af dine egne bookinger")
            egne_bookinger = df_alle[df_alle["Jæger_ID"] == st.session_state.bruger_info["Nr"]]
            if not egne_bookinger.empty:
                aflys_valg = st.selectbox("Vælg den booking du vil slette:", options=egne_bookinger["Nøgle"].tolist(), format_func=lambda x: f"{df_alle[df_alle['Nøgle'] == x]['Dato'].values[0]} - {df_alle[df_alle['Nøgle'] == x]['Område'].values[0]} ({df_alle[df_alle['Nøgle'] == x]['Tidspunkt'].values[0]})")
                if st.button("Slet valgte booking", type="secondary"):
                    data_afbestil = f"{st.session_state.bruger_info['Nr']}|{st.session_state.bruger_info['Navn']}|-|-"
                    if send_til_google_form(aflys_valg, "AFBESTIL", data_afbestil):
                        st.success("Aflysningen er registreret i skyen! Opdaterer kalenderen...")
                        st.rerun()
            else:
                st.info("Du har ikke nogen aktive bookinger i systemet lige nu.")
    else:
        st.info("Der er ikke oprettet nogen bookinger i systemet endnu.")

with fane_regler_info:
    st.header("📜 Praktisk information & Jagtregler")
    st.markdown("""
    * **Sikkerhed først:** Vis altid absolut hensyn til sikkerhedszoner og naboskel.
    * **Én jæger pr. område:** Kun én aktiv jæger ad gangen per område.
    * **Bookingbetingelser:** Du kan maksimalt booke en jagt 14 dage frem i tiden.
    """)

with fane_kontakt:
    st.header("📞 Medlemsliste")
    st.dataframe(pd.DataFrame(kontakt_data)[["Nr", "Navn", "Tlf", "E-mail"]], use_container_width=True, hide_index=True)
