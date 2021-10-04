from django.db import models


class TaskChoices(models.TextChoices):
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
    OTHER = "OTHER", "Sonstiges"
    __empty__ = "Bitte Wert auswählen"


class BranchChoices(models.TextChoices):
    C10 = "C10", "Nahrungs- und Futtermittel"
    C11 = "C11", "Getränke"
    C12 = "C12", "Tabakverarbeitung"
    C13 = "C13", "Textilien"
    C14 = "C14", "Bekleidung"
    C15 = "C15", "Leder, Lederwaren und Schuhe"
    C16 = (
        "C16",
        "Holz-, Flecht-, Korb- und Korkwaren (ohne Möbel)",
    )
    C17 = "C17", "Papier, Pappe und Waren daraus"
    C18 = (
        "C18",
        "Druckerzeugnisse; Vervielfältigung von bespielten Ton-, Bild und Datenträgern",
    )
    C19 = "C19", "Kokerei und Mineralölverarbeitung"
    C20 = "C20", "Chemische Erzeugnisse"
    C21 = "C21", "Pharmazeutischen Erzeugnisse"
    C22 = "C22", "Gummi- und Kunststoffwaren"
    C23 = (
        "C23",
        "Glas und Glaswaren, Keramik, Verarbeitung von Steinen und Erden",
    )
    C24 = "C24", "Metallerzeugung und –bearbeitung"
    C25 = "C25", "Metallerzeugnisse"
    C26 = (
        "C26",
        "Datenverarbeitungsgeräte, elektronische und optische Erzeugnisse",
    )
    C27 = "C27", "Elektrische Ausrüstungen"
    C28 = "C28", "Maschinenbau"
    C29 = "C29", "Kraftwagen und Kraftwagenteile"
    C30 = "C30", "Sonstiger Fahrzeugbau"
    C31 = "C31", "Möbel"
    C32 = "C32", "Herstellung von sonstigen Waren"

    ALL = "ALL", "Keine / Branchenunabhängig"

    __empty__ = "Bitte Wert auswählen"


class DAProcessChoices(models.TextChoices):
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


class TRLChoices(models.IntegerChoices):
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


class CorporateDivisionChoices(models.TextChoices):
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


class HierarchyLevelChoices(models.TextChoices):
    IP = "IP", "Intelligentes Produkt (product)"
    FD = "FD", "Feldebene/Sensoren/Aktoren (field device)"
    CD = "CD", "Regelung & Steuerung (control device)"
    ST = "ST", "Station/Maschine oder Maschinengruppe (station)"
    WC = "WC", "Technische Anlage (work center)"
    EP = "EP", "Unternehmen (enterprise)"
    CW = "CW", "Vernetze Welt (Connected World)"
    __empty__ = "Bitte Wert auswählen"


class ProcessChoices(models.TextChoices):
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


class RealtimeChoices(models.IntegerChoices):
    RT0 = 0, "Keine Echtzeit"
    RT1 = 1, "Weiche Echtzeit"
    RT2 = 2, "Harte Echtzeit"
    RT3 = 3, "Feste Echtzeit"
    __empty__ = "Bitte Wert auswählen"


class LicenseChoices(models.TextChoices):
    FW = "FW", "Freeware"
    OSCL = "OSCL", "Open Source / copy left"
    OS = "OS", "Open Source / no copy left"
    PRO = "PRO", "Proprietär"
    __empty__ = "Bitte Wert auswählen"


class KPIChoices(models.TextChoices):
    E1 = "E1", "Effizienz - Bearbeitungszeit pro Anfrage (h)"
    E2 = "E2", "Effizienz - Termintreue (%)"
    E3 = "E3", "Effizienz - Rüstzeitanteil (%)"
    E4 = "E4", "Effizienz - Automatisierungsgrad (%)"
    E5 = "E5", "Effizienz - Durchlaufzeit (Tage)"
    E6 = "E6", "Effizienz - Durchsatz (VDMA)"
    E7 = "E7", "Effizienz - Produktionsvolumen/Zählwert"
    E8 = (
        "E8",
        "Effizienz - Stillstandzeit/Anzahl und Dauer ungeplanter Produktionsausfälle",
    )
    E9 = "E9", "Effizienz - Taktrate"
    E10 = "E10", "Effizienz - Taktzeit"
    Q1 = "Q1", "Qualität - Qualitätsmängel"
    Q2 = "Q2", "Qualität - Rückgabequote"
    Q3 = (
        "Q3",
        "Qualität - Right first Time/ Nacharbeitsquote / First Pass Yield (FPY, VDMA)",
    )
    Q4 = "Q4", "Qualität - Fall-off-rate (VDMA)"
    Q5 = "Q5", "Qualität - Reklamationsquote (%)"
    Q6 = "Q6", "Qualität - Ausschussquote (%) / Ausschussgrad (VDMA)"
    Q7 = "Q7", "Qualität - Qualitätsgrad (%)"
    Q8 = "Q8", "Qualität - Fehlproduktionsquote (%)"
    Q9 = "Q9", "Qualität - Qualitätsrate (VDMA)"
    Q10 = "Q10", "Qualität - [kritischer] Maschinenfähigkeitssindex (VDMA)"
    Q11 = "Q11", "Qualität - [kritischer] Prozessfähigkeitsindex (VDMA)"
    K1 = "K1", "Kosten/Nutzen - Wertschöpfungsquote (%)"
    K2 = "K2", "Kosten/Nutzen - Fehlproduktionsquote (%)"
    K3 = "K3", "Kosten/Nutzen - Abfallquote (%)"
    K4 = "K4", "Kosten/Nutzen - Instandhaltungsquote (%)"
    K5 = "K5", "Kosten/Nutzen - Return on Assets"
    K6 = "K6", "Kosten/Nutzen - Overall Equipment Effectiveness (OEE)"
    K7 = "K7", "Kosten/Nutzen - Net Equipment Effectiveness (NEE)"
    K8 = "K8", "Kosten/Nutzen - Qualitätsrate (VDMA)"
    K9 = "K9", "Kosten/Nutzen - Nutzgrad/Nutzungsgrad (VDMA)"
    K10 = "K10", "Kosten/Nutzen - Technischer Nutzgrad (VDMA)"
    K11 = "K11", "Kosten/Nutzen - Prozessgrad (VDMA)"
    A1 = "A1", "Auslastung/Verfügbarkeit - Maschinenauslastung (%)"
    A2 = "A2", "Auslastung/Verfügbarkeit - Stillstandszeit (h)"
    A3 = "A3", "Auslastung/Verfügbarkeit - Maschinenausfallquote (%)"
    A4 = "A4", "Auslastung/Verfügbarkeit - Mean Time between Failure (Tage)"
    A5 = "A5", "Auslastung/Verfügbarkeit - Mean Time to Repair (Tage)"
    A6 = "A6", "Auslastung/Verfügbarkeit - Anlagenverfügbarkeit (%)"
    A7 = "A7", "Auslastung/Verfügbarkeit - Kapazitätauslastungsgrad (%)"
    A8 = "A8", "Auslastung/Verfügbarkeit - Beleggrad (VDMA)"
    A9 = "A9", "Auslastung/Verfügbarkeit - Belegnutzgrad (VDMA)"
    F1 = "F1", "Flexibilität - Reaktionsfähigkeit auf Kundenwünsche"
    F2 = "F2", "Flexibilität - Mindestlosgröße (Stk.)"
    F3 = "F3", "Flexibilität - Lieferfähigkeit (%)"
    F4 = "F4", "Flexibilität - Every Part Every Interval (Tage)"
    F5 = "F5", "Mitarbeiter - Fehlzeiten (%)"
    F6 = "F6", "Mitarbeiter - Mitarbeiterverfügbarkeit (%)"
    F7 = "F7", "Mitarbeiter - Mitarbeitereffektivität (%)"
    F8 = "F8", "Mitarbeiter - Beschäftigungsgrad (%)"
    F9 = "F9", "Mitarbeiter - Mitarbeiterproduktivität"
    L1 = "L1", "Logistik - Lagerdauer (Tage)"
    L2 = "L2", "Logistik - Lieferzeit (Tage)"
    L3 = "L3", "Logistik - Lagerumschlag (-)"
    L4 = "L4", "Logistik - Bearbeitungszeit pro Anfrage (h)"
    L5 = "L5", "Logistik - Lieferfähigkeit (%)"
    __empty__ = "Bitte Wert auswählen"
