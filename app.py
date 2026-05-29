import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 1. Konfiguration af hjemmesiden
st.set_page_config(page_title="Ravnkjærgaard - Jagtbooking", page_icon="🌲", layout="centered")

# --- KODE TIL BAGGRUNDSBILLEDE (NY) ---
# Du kan udskifte linket i 'url(...)' herunder med dit eget billedlink, hvis du vil have et andet billede på.
baggrunds_css = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

/* Gør boksene en lille smule gennemsigtige, så teksten er nemmere at læse oven på billedet */
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
.stTabs [data-baseweb="tab-panel"] {
    background-color: rgba(255, 255, 255, 0.95);
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
}
</style>
"""
st.markdown(baggrunds_css, unsafe_allow_html=True)


# Medlemsliste med Kontaktoplysninger
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

if "jaegere" not in st.session_state:
    st.session_state.jaegere = {item["Nr"]: item["Navn"] for item in kontakt_data}

st.session_state.omraader = {
    1: "Område A", 2: "Område B", 3: "Område C", 4: "Område D", 5: "Område E",
    6: "Område F", 7: "Område G", 8: "Område H", 9: "Område I", 10: "Område J"
}

if "bookinger" not in st.session_state:
    st.session_state.bookinger = {}

if "logget_ind" not in st.session_state:
    st.session_state.logget_ind = False
if "bruger_info" not in st.session_state:
    st.session_state.bruger_info = None


# --- AUTOMATISK LOGIN-KONTROL ---
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


# --- SIDEBAR ---
st.sidebar.write(f"Logget ind som:\n**{st.session_state.bruger_info['Navn']}**")
if st.sidebar.button("Log ud"):
    st.session_state.logget_ind = False
    st.session_state.bruger_info = None
    st.rerun()


# --- HOVEDSIDE (LOGGET IND) ---
st.title("🌲 Ravnkjærgaard - Jagt Booking")
st.write("Hvert område kan maksimalt bookes 2 gange om dagen (Morgen og Aften), og der må kun være 1 jæger pr. område ad gangen.")

fane_book, fane_tjek_dato, fane_fuld_oversigt, fane_regler_info, fane_kontakt = st.tabs([
    "🆕 Opret Booking", 
    "🔍 Tjek Specifik Dato", 
    "📅 Den Fulde Kalenderoversigt & Aflysning",
    "📜 Priser, Regler & Info",
    "📞 Medlemsliste & Kontakt"
])


# --- FANE 1: OPRET BOOKING ---
with fane_book:
    st.header("Opret ny jagtreservation")
    st.success(f"✍️ Du opretter lige nu en booking for: **{st.session_state.bruger_info['Navn']}**")
    
    valgt_omraade_id = st.selectbox(
        "Vælg jagtområde:", 
        options=list(st.session_state.omraader.keys()),
        format_func=lambda x: st.session_state.omraader[x]
    )
    
    idag = datetime.today().date()
    valgt_dato = st.date_input(
        "Vælg dato for jagten (Maks 14 dage frem):", 
        min_value=idag,
        max_value=idag + timedelta(days=14),
        key="dato_valg"
    )
    dato_streng = valgt_dato.strftime("%Y-%m-%d")
    
    valgt_tidspunkt = st.radio("Vælg tidspunkt på dagen:", ["Morgen 🌅", "Aften 🌇"])
    notat_input = st.text_input("Tilføj et notat (valgfrit):", placeholder="F.eks. 'Hund med', 'Riffel'")

    if st.button("Bekræft og book jagt", type="primary"):
        booking_noegle = f"{dato_streng}_{valgt_omraade_id}_{valgt_tidspunkt}"
        
        if booking_noegle in st.session_state.bookinger:
            nuvaerende_booker = st.session_state.bookinger[booking_noegle]["navn"]
            st.error(f"❌ Området er optaget! {st.session_state.omraader[valgt_omraade_id]} er allerede booket {valgt_tidspunkt.lower()} d. {dato_streng} af {nuvaerende_booker}.")
        else:
            st.session_state.bookinger[booking_noegle] = {
                "jaeger_id": st.session_state.bruger_info["Nr"],
                "navn": st.session_state.bruger_info["Navn"],
                "tidspunkt": valgt_tidspunkt,
                "notat": notat_input if notat_input.strip() else "-"
            }
            st.success(f"✅ Godkendt! Du har booket {st.session_state.omraader[valgt_omraade_id]} ({valgt_tidspunkt.lower()}) d. {dato_streng}.")


# --- FANE 2: TJEK EN SPECIFIK DATO ---
with fane_tjek_dato:
    st.header("Hvem er på jagt denne dag?")
    tjek_dato = st.date_input("Vælg den dato du vil undersøge:", value=datetime.today().date(), key="tjek_dato_valg")
    tjek_dato_streng = tjek_dato.strftime("%Y-%m-%d")
    
    st.write(f"### Status for d. {tjek_dato_streng}:")
    
    fundet_booking = False
    for omr_id, omr_navn in st.session_state.omraader.items():
        morgen_noegle = f"{tjek_dato_streng}_{omr_id}_Morgen 🌅"
        aften_noegle = f"{tjek_dato_streng}_{omr_id}_Aften 🌇"
        
        if morgen_noegle in st.session_state.bookinger:
            b = st.session_state.bookinger[morgen_noegle]
            st.info(f"🌅 **Morgen**: {omr_navn} er optaget af Nr. {b['jaeger_id']} - {b['navn']} *(Besked: {b['notat']})*")
            fundet_booking = True
        else:
            st.write(f"🌅 **Morgen**: {omr_navn} er 🟢 **Ledig**")
            
        if aften_noegle in st.session_state.bookinger:
            b = st.session_state.bookinger[aften_noegle]
            st.warning(f"🌇 **Aften**: {omr_navn} er optaget af Nr. {b['jaeger_id']} - {b['navn']} *(Besked: {b['notat']})*")
            fundet_booking = True
        else:
            st.write(f"🌇 **Aften**: {omr_navn} er 🟢 **Ledig**")
            
        st.write("---")
            
    if not fundet_booking:
        st.success("🌲 Alle områder er helt ledige denne dag!")

# --- FANE 3: DEN FULDE KALENDEROVERSIGT & AFLYSNING ---
with fane_fuld_oversigt:
    st.header("Komplet oversigt over alle reservationer")
    
    if not st.session_state.bookinger:
        st.info("Der er i øjeblikket ingen aktive bookinger i systemet.")
    else:
        tabel_data = []
        for noegle, info in list(st.session_state.bookinger.items()):
            dato_del, omraade_id_del, tid_del = noegle.split("_")
            
            omraade_id_int = int(omraade_id_del)
            if omraade_id_int in st.session_state.omraader:
                omraade_navn = st.session_state.omraader[omraade_id_int]
            else:
                omraade_navn = f"Gammelt område (ID: {omraade_id_int})"
                
            tabel_data.append({
                "Nøgle": noegle,
                "Dato": dato_del,
                "Tidspunkt": tid_del,
                "Jagtområde": omraade_navn,
                "Jæger": f"Nr. {info['jaeger_id']} - {info['navn']}",
                "Notat": info["notat"]
            })
        
        if tabel_data:
            df = pd.DataFrame(tabel_data).sort_values(by=["Dato", "Tidspunkt"])
            st.dataframe(df.drop(columns=["Nøgle"]), use_container_width=True, hide_index=True)
            
            st.write("---")
            st.subheader("🗑️ Vil du aflyse en booking?")
            
            slet_valg = st.selectbox(
                "Vælg den booking du vil fjerne:",
                options=tabel_data,
                format_func=lambda x: f"{x['Dato']} ({x['Tidspunkt'].lower()}) - {x['Jagtområde']} [{x['Jæger']}]"
            )
            
            slet_id_validering = st.text_input("Indtast dit medlemsnummer for at godkende aflysning:", type="password", key="slet_pin")
            
            if st.button("Slet valgte booking", type="secondary"):
                korrekt_id = str(st.session_state.bookinger[slet_valg["Nøgle"]]["jaeger_id"])
                
                if slet_id_validering.strip() == korrekt_id:
                    del st.session_state.bookinger[slet_valg["Nøgle"]]
                    st.success("📌 Bookingen er blevet slettet!")
                    st.rerun()
                else:
                    st.error("❌ Forkert medlemsnummer. Du kan kun slette dine egne bookinger.")
        else:
            st.info("Der er i øjeblikket ingen aktive bookinger i systemet.")


# --- FANE 4: PRISER, REGLER & INFO ---
with fane_regler_info:
    st.header("💰 Vildtpriser")
    kol1, kol2 = st.columns(2)
    with kol1:
        st.write("""
        * **Buk:** 500 kr.
        * **Rå:** 400 kr.
        * **Lam:** 300 kr.
        * **Stor hjort:** 3000 kr. *inkl. trofæ*
        * **Spidshjort:** 1200 kr.
        """)
    with kol2:
        st.write("""
        * **Hind:** 1000 kr.
        * **kalv:** 800 kr.
        * **Dåhjort, større end spidshjort:** 2500 kr. *inkl. trofæ*
        * **Spidshjort:** 1000 kr.
        * **Då:** 800 kr.
        * **Kalv:** 600 kr.
        """)
    st.write("**Alt andet vildt:** 0 kr.")
    st.markdown("<span style='color:red; font-weight:bold;'>Alt nedlagt vildt skal rapporteres til formanden.</span>", unsafe_allow_html=True)
    st.markdown("<span style='color:red; font-weight:bold;'>Alle skud skal rapporteres til formanden. Dog ikke haglskud på frijagter</span>", unsafe_allow_html=True)
    
    st.write("---")
    st.header("📅 Arbejdsdage")
    st.write("""
    Da der bliver brug for en ekstra indsats ang. arbejdsdag det første år, er vi blevet enige om nedenstående.
    * Der bliver **5 arbejdsdage** inden udgang af august.
    * **Datoer for arbejdsdage:** 13/6 – 21/6 – 1/8 – 16/8 – 29/8
    """)
    st.caption("*Muligvis kan arbejdsdagene også placeres i september, hvis det besluttes ikke at drive jagt på kronkalv i september, dette bestemmes efter samtale med nabokonsortier.*")
    st.write("""
    * Man skal **min. deltage på 3 ud af 5 dage**.
    * Ved udeblivelse af mere end 2 arbejdsdage betales af medlem **200kr. pr. dag**.
    * Ved udeblivelse af alle 5 arbejdsdage betales af medlem **1200kr.**
    """)
    
    st.write("---")
# --- FANE 5: MEDLEMSLISTE & KONTAKT ---
with fane_kontakt:
    st.header("📞 Anpartsliste & Kontaktoplysninger")
    st.write("Her er den samlede medlemsliste med kontaktinformationer:")
    
    kontakt_data = [
        {"Navn": "Lasse Lichon Hesthaven", "Tlf": "28 57 23 62", "E-mail": "lichon10@hotmail.com"},
        {"Navn": "Alexander Knudsen", "Tlf": "31 14 94 08", "E-mail": "alekproscore@hotmail.com"},
        {"Navn": "Thomas Jøns", "Tlf": "42 17 78 07", "E-mail": "cuba_joens@hotmail.com"},
        {"Navn": "Jørgen Thomsen", "Tlf": "49 40 50 64", "E-mail": "thomsen777@gmail.com"},
        {"Navn": "Per Eli Løfqvist", "Tlf": "30 50 32 12", "E-mail": "loefqvist@gmail.com"},
        {"Navn": "Peter Aaen", "Tlf": "20 92 34 14", "E-mail": "peter.aaen46@gmail.com"},
        {"Navn": "Morten Ransborg", "Tlf": "20 18 95 91", "E-mail": "morten@ransborg.net"},
        {"Navn": "Steffen Carlsen", "Tlf": "53 55 44 94", "E-mail": "steffencarlsen86@gmail.com"},
        {"Navn": "Morten Mæng Pedersen", "Tlf": "28 91 69 15", "E-mail": "mortenmaeng@hotmail.com"},
        {"Navn": "Ole Libak Christensen", "Tlf": "31 50 35 55", "E-mail": "ole.libak@gmail.com"},
        {"Navn": "Christian Ringstrøm Andersen", "Tlf": "61 26 17 38", "E-mail": "Christian.ringstroem@gmail.com"},
        {"Navn": "Tom Erik Houen", "Tlf": "40 59 10 59", "E-mail": "tomhouen@gmail.com"},
        {"Navn": "Jan Carstens", "Tlf": "61 80 60 00", "E-mail": "janc280656@gmail.com"},
        {"Navn": "Benjamin Kirkeby G. Carstenskiold", "Tlf": "31 72 43 02", "E-mail": "Hj01bg@gmail.com"},
        {"Navn": "Lars Højmose Kristensen", "Tlf": "30 24 51 07", "E-mail": "lakris@proton.me"},
        {"Navn": "Peter Hahn Boelt", "Tlf": "60 67 50 19", "E-mail": "peterhbmail@proton.me"},
        {"Navn": "Jonathan Brun Sønderbæk", "Tlf": "20 60 89 35", "E-mail": "Jona811k@yahoo.dk"},
        {"Navn": "Mathies Boelt", "Tlf": "23 96 83 72", "E-mail": "Mathies-boelt@hotmail.com"},
        {"Navn": "Per Behrmann", "Tlf": "50 58 17 41", "E-mail": "perbehrmann@hotmail.com"},
        {"Navn": "Tonni Bastrup Pedersen", "Tlf": "23 47 74 02", "E-mail": "tonnibastrup@gmail.com"},
        {"Navn": "Peter Michael Nielsen", "Tlf": "23 72 62 25", "E-mail": "pmn@bbnpost.dk"},
        {"Navn": "Simon Noer Burkal", "Tlf": "28 74 70 45", "E-mail": "Simon@burkal.dk"},
        {"Navn": "Carsten Bjerregaard", "Tlf": "30 13 10 26", "E-mail": "Cbj.bjerregaard@gmail.com"},
        {"Navn": "Rene' Andersen", "Tlf": "22 44 62 22", "E-mail": "Rahunter13@gmail.com"},
        {"Navn": "Kristian Hæsum Pedersen", "Tlf": "60 19 06 26", "E-mail": "Khaesum@gmail.com"}
    ]
    
    df_kontakt = pd.DataFrame(kontakt_data)
    st.dataframe(df_kontakt, use_container_width=True, hide_index=True)
    
    st.write("---")
    st.caption("Linket til denne app: https://streamlit.app")
