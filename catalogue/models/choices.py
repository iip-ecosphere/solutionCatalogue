from django.db import models


class TaskName(models.TextChoices):
    PMCM = "PMCM", "Predictive Maintenance/Condition Monitoring"
    QCM = (
        "QCM",
        "Qualitätskontrolle und –management",
    )  # Quality control and management
    OPP = "OPP", "Optimierte Prozessplanung"  # Optimized process planning
    OPC = "OPC", "Optimierte Prozesssteuerung"  # Optimized process control
    RAS = "RAS", "Robotik & autonome Systeme"  # Robotics & autonomous systems
    IST = "IST", "Intelligente Sensorik"  # Intelligent sensor technology
    KM = "KM", "Wissensmanagement"  # Knowledge Management
    FPA = (
        "FPA",
        "Vorhersagen und Predictive Analytics",
    )  # Forecasting and Predictive Analytics
    ORS = "ORS", "Optimiertes Ressourcenmanagement"  # Optimized resource management
    IA = "IA", "Intelligente Automatisierung"  # Intelligent automation
    IAS = "IAS", "Intelligente Assistenzsysteme"  # Intelligent assistance systems
    DA = "DA", "Datenanalyse"  # Data analysis
    DM = "DM", "Data Management"
    VAR = (
        "VAR",
        "Virtuelle und erweiterte Realität",
    )  # Virtual and augmented reality
    OTHER = "OTHER", "Sonstiges?"
    __empty__ = "Bitte Wert auswählen"


class BranchName(models.TextChoices):
    C10 = "C10", "Herstellung von Nahrungs- und Futtermitteln (C.10)"
    C11 = "C11", "Getränkeherstellung (C.11)"
    C12 = "C12", "Tabakverarbeitung (C.12)"
    C13 = "C13", "Herstellung von Textilien (C.13)"
    C14 = "C14", "Herstellung von Bekleidung (C.14)"
    C15 = "C15", "Herstellung von Leder, Lederwaren und Schuhen (C.15)"
    C16 = (
        "C16",
        "Herstellung von Holz-, Flecht-, Korb- und Korkwaren (ohne Möbel) (C.16)",
    )
    C17 = "C17", "Herstellung von Papier, Pappe und Waren daraus (C.17)"
    C18 = (
        "C18",
        "Herstellung von Druckerzeugnissen; Vervielfältigung von bespielten Ton-, Bild und Datenträgern (C.18)",
    )
    C19 = "C19", "Kokerei und Mineralölverarbeitung (C.19)"
    C20 = "C20", "Herstellung von chemischen Erzeugnissen (C.20)"
    C21 = "C21", "Herstellung von pharmazeutischen Erzeugnissen (C.21)"
    C22 = "C22", "Herstellung von Gummi- und Kunststoffwaren (C.22)"
    C23 = (
        "C23",
        "Herstellung von Glas und Glaswaren, Keramik, Verarbeitung von Steinen und Erden (C.23)",
    )
    C24 = "C24", "Metallerzeugung und –bearbeitung (C.24)"
    C25 = "C25", "Herstellung von Metallerzeugnissen (C.25)"
    C26 = (
        "C26",
        "Herstellung von Datenverarbeitungsgeräten, elektronischen und optischen Erzeugnissen (C.26)",
    )
    C27 = "C27", "Herstellung von elektrischen Ausrüstungen (C.27)"
    C28 = "C28", "Maschinenbau (C.28)"
    C29 = "C29", "Herstellung von Kraftwagen und Kraftwagenteilen (C.29)"
    C30 = "C30", "Sonstiger Fahrzeugbau (C.30)"
    C31 = "C31", "Herstellung von Möbeln (C.31)"
    C32 = "C32", "Herstellung von sonstigen Waren (C.32)"

    ALL = "ALL", "Keine / Branchenunabhängig"

    __empty__ = "Bitte Wert auswählen"


class DAProcessName(models.TextChoices):
    DA = "DA", "Datenerfassung"  # Data acquisition
    DC = "DC", "Data-Cleaning/Pre-processing"
    DI = "DI", "Datenintegration"  # Data integration
    MS = "MS", "Modellauswahl"  # Model selection
    MT = "MT", "Modellbildung & Training"  # Modeling & Training
    MA = "MA", "Modellanalyse/erklärung"  # Model analysis/explanation
    MU = "MU", "Modellanwendung"  # Model use
    VI = "VI", "Visualisierung"  # Visualization
    PC = "PC", "KI-basierte Prozesssteuerung"  # AI-based process control
    __empty__ = "Bitte Wert auswählen"


class TRL(models.IntegerChoices):
    TRL1 = 1, "TRL 1 - Grundprinzipien beobachtet"
    TRL2 = 2, "TRL 2 - Technologiekonzept formuliert"
    TRL3 = 3, "TRL 3 - Experimenteller Nachweis des Konzepts"
    TRL4 = 4, "TRL 4 - Technologie im Labor überprüft"
    TRL5 = 5, "TRL 5 - Technologie in relevanter Umgebung überprüft"
    TRL6 = 6, "TRL 6 - Technologie in relevanter Umgebung getestet"
    TRL7 = 7, "TRL 7 - Test eines System-Prototyps im realen Einsatz"
    TRL8 = 8, "TRL 8 - System ist komplett und qualifiziert"
    TRL9 = 9, "TRL 9 - System funktioniert in operationeller Umgebung"
    __empty__ = "Bitte Wert auswählen"


class CorporateDivisionName(models.TextChoices):
    CS = "CS", "Kundendienst / Inbetriebnahme"  # Customer Service / Commissioning
    CD = "DD", "Konstruktion / Entwicklung"  # Construction / Development
    PA = "PA", "Produktion / Montage"  # Production/assembly
    MA = "MA", "Instandhaltung"  # Maintenance
    LO = "LO", "Logistik / Supply Chain Management"
    MC = "MC", "Marketing / Kommunikation"  # Marketing / Communication
    MM = "MM", "Materialwirtschaft / Einkauf"  # Materials Management / Purchasing
    AC = "AC", "Rechnungswesen / Controlling"  # Accounting / Controlling
    CG = "CG", "Management / Unternehmensführung"  # Management/Corporate Governance
    SP = "SP", "Sales / Preisgestaltung"  # Sales / Pricing
    __empty__ = "Bitte Wert auswählen"


class HierarchyLevelName(models.TextChoices):
    IP = "IP", "Intelligentes Produkt (product)"
    FD = "FD", "Feldebene/Sensoren/Aktoren (field device)"
    CD = "CD", "Regelung & Steuerung (control device)"
    ST = "ST", "Station/Maschine oder Maschinengruppe (station)"
    WC = "WC", "Technische Anlage (work center)"
    EP = "EP", "Unternehmen (enterprise)"
    CW = "CW", "Vernetze Welt (Connected World)"
    __empty__ = "Bitte Wert auswählen"


class ProcessName(models.TextChoices):
    PD = "PD", "Produktionsentwicklung"  # Production development
    PA = (
        "PA",
        "Fertigungs- und Montagevorbereitung",
    )  # Production and assembly preparation
    PP = (
        "PP",
        "Produktionsplanung und –steuerung",
    )  # Production planning and control
    PM = "PM", "Teilefertigung"  # Parts manufacturing
    PMPP = (
        "PMPP",
        "Teilefertigung - Produktionsprozess (Prozesskette)",
    )  # Parts manufacturing - production process (process chain)
    PMSP = (
        "PMSP",
        "Teilefertigung - Einzelfertigungsprozess",
    )  # Parts manufacturing - single-part production process
    AS = "AS", "Montage, (VDI 2860)"  # Assembly, (VDI 2860)
    QA = "QA", "Qualitätssicherung"  # Quality assurance
    MFL = "MFL", "Materialfluss, Logistik"  # Material flow, logistics
    CP = "CP", "Änderungsprozesse"  # Change processes
    PRODM = "PRODM", "Produktionsinstandhaltung"  # Production maintenance
    __empty__ = "Bitte Wert auswählen"


class Realtime(models.IntegerChoices):
    RT0 = 0, "Keine Echtzeit"
    RT1 = 1, "Weiche Echtzeit"
    RT2 = 2, "Harte Echtzeit"
    RT3 = 3, "Feste Echtzeit"
    __empty__ = "Bitte Wert auswählen"
