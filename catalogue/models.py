from django.db import models


class Task(models.Model):
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

    name = models.CharField(choices=TaskName.choices, max_length=5)


class Branch(models.Model):
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
        # FIXME: branchenunabhängig option
        __empty__ = "Bitte Wert auswählen"

    name = models.CharField(choices=BranchName.choices, max_length=3)


class DataAnalysisProcess(models.Model):
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

    name = models.CharField(choices=DAProcessName.choices, max_length=2)


class Component(models.Model):
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

    name = models.CharField(
        "Name", max_length=200, help_text="Bezeichnung der Komponente", blank=False
    )
    task = models.ManyToManyField(
        Task,
        verbose_name="Task",
        help_text=(
            "Art der Aufgabe, der die beschriebene KI-Komponente zugeordnet werden kann"
            " (z.B. Predictive Maintenance, Qualitätsprüfung)"
        ),
    )
    trl = models.IntegerField(
        "TRL",
        help_text=(
            "Status der Komponente in Bezug auf Ihre Einsetzbarkeit durch die Angabe"
            " eines Technischen Reifegrades (Technology Readiness Level)."
        ),
        choices=TRL.choices,
    )
    description = models.TextField(
        "Kurzbeschreibung", help_text="Kurze Beschreibung der Komponente"
    )
    # TODO: ForeignKeys


class ApplicationProfile(models.Model):
    class CorporateDivision(models.TextChoices):
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

    class HierarchyLevel(models.TextChoices):
        IP = "IP", "Intelligentes Produkt (product)"
        FD = "FD", "Feldebene/Sensoren/Aktoren (field device)"
        CD = "CD", "Regelung & Steuerung (control device)"
        ST = "ST", "Station/Maschine oder Maschinengruppe (station)"
        WC = "WC", "Technische Anlage (work center)"
        EP = "EP", "Unternehmen (enterprise)"
        CW = "CW", "Vernetze Welt (Connected World)"
        __empty__ = "Bitte Wert auswählen"

    class Process(models.TextChoices):
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

    component = models.OneToOneField(Component, on_delete=models.CASCADE)

    branch_proven = models.ManyToManyField(
        Branch,
        verbose_name="Branche (erprobt)",
        help_text="Branche(n) für die die Komponente bereits erfolgreich erprobt wurde; belegte Anwendung",
        related_name="branch_proven_for",
    )
    branch_applicable = models.ManyToManyField(
        Branch,
        verbose_name="Branche (anwendbar)",
        help_text="Branche, in denen die Komponenten anwendbar ist",
        related_name="branch_applicable_for",
    )
    corporate_division = models.CharField(
        "Unternehmensbereich",
        choices=CorporateDivision.choices,
        help_text="Bereich des produzierenden Unternehmens, für den die Komponenten entwickelt wurde",
        max_length=2,
    )  # FIXME: Mehrfachauswahl?
    hierarchy_level = models.CharField(
        "Hierarchie-Ebene",
        choices=HierarchyLevel.choices,
        help_text="Automatisierebene, für die die KI-Komponente gedacht ist",
        max_length=2,
    )  # FIXME: Mehrfachauswahl?
    process = models.CharField(
        "Prozess",
        choices=Process.choices,
        help_text="Prozess der durch die KI-Komponente unterstützt wird",
        max_length=5,
    )  # FIXME: Mehrfachauswahl?
    product = models.TextField("Produkt", help_text="Hergestelltes Produkt")


class Use(models.Model):
    component = models.OneToOneField(Component, on_delete=models.CASCADE)

    kpi = models.CharField(
        "KPI",
        help_text=(
            "Key Performance Indikator, der durch die Komponente optimiert werden soll;"
            "es sollte auf jeden Fall eine Kategorie ausgesucht werden (Wert);"
            " dies Auswahl kann über KPI-Verfeinerung noch verfeinert werden;"
        ),
        max_length=1000,
    )  # TODO: Hierarchy
    scenarios = models.TextField(
        "Szenarien / Use cases",
        help_text="Beschreibung von Szenarien, in denen die Komponente bereits erfolgreich eingesetzt wurde",
    )


class Requirements(models.Model):
    component = models.OneToOneField(Component, on_delete=models.CASCADE)

    # FIXME: multiple inputs? max_length?
    protocols = models.CharField(
        "Protokolle/Schnittstellen",
        help_text="Schnittstellen und/oder Protokolle, die von der Kompomente unterstützt werden",
        max_length=1000,
    )
    it_environment = models.CharField(
        "IT Umgebung/Software",
        help_text=(
            "Anforderungen an die IT-Umgebung (inkl. IT Hardware) und an weitere Software/Bibliotheken"
            ", die für den Betrieb der Komponente notwendig sind"
        ),
        max_length=1000,
    )
    hardware_requirements = models.CharField(
        "Spezielle Hardware",
        help_text="Spezielle Hardware, welche für den Betrieb der Komponente notwendig ist (z.B. Kamera, Roboter)",
        max_length=1000,
    )
    devices = models.CharField(
        "Maschinen/Steuerungen",
        help_text="Maschinen und IoT Devices, mit denen die Komponente kompatibel ist",
        max_length=1000,
    )


class TechnicalSpecification(models.Model):
    class Realtime(models.IntegerChoices):
        RT0 = 0, "Keine Echtzeit"
        RT1 = 1, "Weiche Echtzeit"
        RT2 = 2, "Harte Echtzeit"
        RT3 = 3, "Feste Echtzeit"
        __empty__ = "Bitte Wert auswählen"

    component = models.OneToOneField(Component, on_delete=models.CASCADE)

    ai_method = models.CharField(
        "KI-Methode",
        help_text="Angabe der verwendeten KI-Methode (z.B. Deep Learning)",
        max_length=1000,
    )  # FIXME: multivalue? textfield?
    data_analysis_process = models.ManyToManyField(
        DataAnalysisProcess,
        verbose_name="Datenanalyse-Prozess",
        help_text="Unterstützte Phasen des Datenanalyse-Prozesses (z.B. Data Cleaning)",
    )  # FIXME: "einzelne Schritte des Prozesses erklären"?
    realtime_processing = models.IntegerField(
        "Echtzeitverarbeitung",
        help_text="Klassifizierung der Komponente in Bezug auf ihre Echtzeitfähigkeit",
        choices=Realtime.choices,
    )
    data_formats = models.CharField(
        "Datenformate",
        help_text="Datenformate, die von der KI-Komponente verarbeitet werden können und Datenformat der Ergebnisse",
        max_length=1000,
    )
    licenses = models.CharField(
        "Lizenzen",
        help_text="Welche Lizenzen bringt die Komponente mit, insbesondere Open Source Lizenzen",
        max_length=1000,
    )  # FIXME: multivalue? # TODO: choices

    # FIXME: planed for later
    # machine_readable_spec = models.CharField("Maschinenlesbare Spezifikation",
    # help_text="Beschreibung der Schnittstellen in maschinenlesbarer Form, um automatische Integration zu unterstützen")


class Source(models.Model):
    component = models.OneToOneField(Component, on_delete=models.CASCADE)

    developer = models.CharField(
        "Hersteller",
        help_text="Entwickler und/oder Hersteller der Komponente",
        max_length=1000,
    )
    contact = models.TextField(
        "Kontakt", help_text="Möglichkeit zum Hersteller Kontakt aufzunehmen",
    )
    additional_info = models.TextField(
        "Zusatzinformationen", help_text="Zusatzinformation zur Komponente",
    )
