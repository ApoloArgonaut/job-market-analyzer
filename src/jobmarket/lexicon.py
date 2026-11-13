"""Léxico de habilidades: término canónico -> alias aceptados.

Cada alias se compara con límites de palabra (ver normalize.py), así que
"sql" no coincide con "mysql". Los alias incluyen las variantes reales que
aparecen en las ofertas: siglas, marcas y formas con guion.
"""
from __future__ import annotations

LEXICON: dict[str, tuple[str, ...]] = {
    # --- datos ---
    "sql": ("sql", "t-sql", "pl/sql", "mysql", "postgresql", "postgres", "mariadb", "sqlite", "mssql"),
    "python": ("python", "python3", "py"),
    "excel": ("excel", "microsoft excel", "ms excel", "spreadsheets", "pivot tables", "vlookup", "xlookup"),
    "power_bi": ("power bi", "powerbi", "dax"),
    "tableau": ("tableau",),
    "looker": ("looker", "lookml"),
    "data_visualization": ("data visualization", "dataviz", "dashboards", "dashboarding", "charts"),
    "etl": ("etl", "elt", "data pipeline", "data pipelines", "airflow", "dbt", "dagster"),
    "pandas": ("pandas", "numpy", "polars"),
    "statistics": ("statistics", "statistical analysis", "hypothesis testing", "regression analysis"),
    "data_quality": ("data quality", "data validation", "data integrity", "data cleansing", "data cleaning"),
    "data_entry": ("data entry", "data capture", "typing speed"),

    # --- QA ---
    "qa": ("qa", "quality assurance", "quality control"),
    "manual_testing": ("manual testing", "manual qa", "exploratory testing", "black box testing"),
    "test_cases": ("test case", "test cases", "test scenario", "test scenarios"),
    "test_plans": ("test plan", "test plans", "test planning", "test strategy"),
    "regression": ("regression testing", "regression test", "regression suite", "smoke testing", "smoke test"),
    "bug_reporting": ("bug report", "bug reporting", "defect report", "defect tracking", "bug tracking", "jira"),
    "testrail": ("testrail", "zephyr", "qtest", "test management"),
    "selenium": ("selenium",),
    "cypress": ("cypress",),
    "playwright": ("playwright",),
    "postman": ("postman", "soapui", "insomnia"),
    "api_testing": ("api testing", "rest api", "restful api", "graphql", "web services testing"),
    "performance_testing": ("performance testing", "load testing", "jmeter", "k6", "gatling"),
    "accessibility": ("accessibility", "wcag", "a11y", "screen reader"),
    "cross_browser": ("cross-browser", "cross browser", "browser compatibility"),

    # --- soporte ---
    "zendesk": ("zendesk",),
    "intercom": ("intercom",),
    "freshdesk": ("freshdesk", "freshservice"),
    "salesforce": ("salesforce", "sales force"),
    "hubspot": ("hubspot",),
    "crm": ("crm", "customer relationship management"),
    "ticketing": ("ticketing", "ticket queue", "tickets", "help desk", "helpdesk"),
    "sla": ("sla", "slas", "service level agreement"),
    "csat": ("csat", "customer satisfaction", "nps", "net promoter score"),
    "escalation": ("escalation", "escalate", "escalations"),
    "troubleshooting": ("troubleshooting", "root cause analysis", "debugging"),
    "knowledge_base": ("knowledge base", "knowledgebase", "kb articles", "help center"),
    "customer_success": ("customer success", "account management", "client success"),
    "onboarding": ("onboarding", "customer onboarding", "user onboarding"),
    "bilingual": ("bilingual", "english and spanish", "spanish and english"),

    # --- UX ---
    "figma": ("figma",),
    "sketch": ("sketch app", "sketch"),
    "adobe_xd": ("adobe xd", "xd"),
    "design_system": ("design system", "design systems", "component library", "storybook"),
    "prototyping": ("prototyping", "prototype", "prototypes", "interactive prototype"),
    "wireframing": ("wireframe", "wireframes", "wireframing", "low-fidelity"),
    "user_research": ("user research", "user interviews", "usability testing", "usability test", "user testing"),
    "user_flows": ("user flow", "user flows", "user journey", "journey map", "journey mapping"),
    "personas": ("persona", "personas", "user personas"),
    "information_architecture": ("information architecture", "ia structure", "sitemap"),
    "handoff": ("developer handoff", "design handoff", "handoff"),
    "ab_testing": ("a/b testing", "ab testing", "split testing", "experimentation"),
    "product_design": ("product design", "product designer", "ux/ui", "ui/ux"),

    # --- operaciones / administración ---
    "sop": ("sop", "sops", "standard operating procedure", "standard operating procedures", "process documentation"),
    "process_improvement": ("process improvement", "process optimization", "continuous improvement", "lean", "six sigma"),
    "inventory": ("inventory", "stock control", "stock management", "warehouse"),
    "logistics": ("logistics", "supply chain", "last mile", "shipping", "fulfillment"),
    "reconciliation": ("reconciliation", "reconcile", "cash handling", "cash management"),
    "vendor_management": ("vendor management", "supplier management", "procurement", "purchasing"),
    "reporting": ("reporting", "reports", "weekly reports", "monthly reports", "analytics reporting"),
    "kpi": ("kpi", "kpis", "metrics", "okrs"),
    "asana": ("asana",),
    "notion": ("notion",),
    "trello": ("trello",),
    "monday": ("monday.com", "monday com"),
    "clickup": ("clickup",),

    # --- gestión ---
    "project_management": ("project management", "project manager", "program management", "pmo"),
    "stakeholder": ("stakeholder", "stakeholders", "stakeholder management"),
    "agile": ("agile", "scrum", "kanban", "sprint", "sprints"),
    "jira": ("jira", "confluence", "atlassian"),
    "roadmap": ("roadmap", "roadmapping", "product roadmap"),
    "requirements": ("requirements gathering", "business requirements", "brd", "user stories", "acceptance criteria"),
    "documentation": ("documentation", "technical writing", "process documentation"),

    # --- IA / evaluación ---
    "llm": ("llm", "llms", "large language model", "large language models", "gpt", "claude", "gemini"),
    "prompt_engineering": ("prompt engineering", "prompting", "prompt design", "prompt writing"),
    "model_evaluation": ("model evaluation", "llm evaluation", "evals", "evaluation framework", "benchmarking"),
    "annotation": ("annotation", "data annotation", "labeling", "labelling", "data labeling"),
    "rlhf": ("rlhf", "reinforcement learning from human feedback", "human feedback"),
    "rubric_design": ("rubric", "rubrics", "rubric design", "grading criteria"),
    "red_teaming": ("red teaming", "red team", "adversarial testing", "jailbreak"),
    "trust_safety": ("trust and safety", "trust & safety", "content moderation", "policy enforcement"),
    "ai_quality": ("ai quality", "model quality", "output quality", "hallucination"),

    # --- turismo ---
    "travel": ("travel", "tourism", "travel agency", "tour operator"),
    "hospitality": ("hospitality", "hotel", "hotels", "resort", "lodging"),
    "booking": ("booking", "reservation", "reservations", "bookings"),
    "itinerary": ("itinerary", "itineraries", "travel planning", "trip planning"),
    "gds": ("gds", "amadeus", "sabre", "galileo", "worldspan"),
    "quotation": ("quotation", "quote", "quotes", "quoting", "price quote"),
    "upselling": ("upselling", "upsell", "cross-selling", "cross selling"),

    # --- herramientas transversales ---
    "git": ("git", "github", "gitlab", "bitbucket", "version control"),
    "docker": ("docker", "containers", "containerization", "kubernetes", "k8s"),
    "ci_cd": ("ci/cd", "cicd", "continuous integration", "continuous delivery", "github actions", "jenkins"),
    "linux": ("linux", "unix", "bash", "shell scripting"),
    "javascript": ("javascript", "js", "typescript", "ts", "node.js", "nodejs", "react", "vue", "angular"),
    "html_css": ("html", "css", "html5", "css3", "tailwind", "sass", "scss"),
    "java": ("java", "spring boot", "spring"),
    "remote_work": ("remote", "remote-first", "work from home", "distributed team", "anywhere"),
}

#: Alias de perfil usados por el clasificador: nombre legible -> patrones de título.
ROLE_PROFILES: dict[str, tuple[str, ...]] = {
    "QA": ("qa", "quality assurance", "tester", "test engineer", "test analyst", "sdet"),
    "SUPPORT": ("customer support", "customer service", "support specialist", "support engineer",
                 "help desk", "helpdesk", "customer success", "technical support", "client support"),
    "UX": ("ux", "ui", "product design", "interaction design", "visual design", "ux research",
           "user experience", "design lead"),
    "OPS": ("operations", "operaciones", "back office", "coordinator", "logistics", "supply chain",
            "inventory", "warehouse"),
    "ADMIN": ("administrative", "administrativo", "assistant", "executive assistant", "data entry",
              "office manager", "secretary"),
    "PM": ("project manager", "program manager", "project coordinator", "delivery manager", "pmo",
           "product manager", "product owner", "scrum master"),
    "IA": ("ai trainer", "ai evaluator", "data annotator", "annotation", "labeling", "labelling",
           "content reviewer", "llm", "prompt", "trust and safety", "ai quality", "data quality"),
    "TURISMO": ("travel", "tourism", "hospitality", "hotel", "booking", "reservation",
                "travel agent", "tour operator", "cruise"),
}

#: Términos que describen el contexto de la bolsa, no una habilidad.
#: Todas las fuentes son bolsas de empleo remoto, así que "remote" aparece en
#: más de la mitad de las ofertas por construcción. Contarlo como demanda
#: sería medir el sesgo de muestreo, no el mercado.
CONTEXT_TERMS: frozenset[str] = frozenset({"remote_work"})
