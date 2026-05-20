import sqlite3
import json
import os
from pathlib import Path
from app.config import DB_PATH

class DatabaseManager:
    def __init__(self):
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        self.path = str(DB_PATH)

    def _conn(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

    def initialize(self):
        with self._conn() as conn:
            conn.executescript("""
            CREATE TABLE IF NOT EXISTS user_profiles (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT NOT NULL,
                age         INTEGER,
                country     TEXT,
                city        TEXT,
                currency    TEXT DEFAULT 'EUR',
                marital_status TEXT,
                education_level TEXT,
                career_field TEXT,
                health_notes TEXT,
                created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS financial_profiles (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id             INTEGER REFERENCES user_profiles(id),
                monthly_income      REAL DEFAULT 0,
                side_income         REAL DEFAULT 0,
                monthly_expenses    REAL DEFAULT 0,
                monthly_savings     REAL DEFAULT 0,
                salary_growth_pct   REAL DEFAULT 0.02,
                current_savings     REAL DEFAULT 0,
                current_investments REAL DEFAULT 0,
                current_debt        REAL DEFAULT 0,
                monthly_debt_payment REAL DEFAULT 0,
                emergency_fund      REAL DEFAULT 0,
                risk_tolerance      TEXT DEFAULT 'Modéré',
                investing_knowledge TEXT DEFAULT 'Débutant',
                crypto_pct          REAL DEFAULT 0,
                stocks_pct          REAL DEFAULT 0,
                etf_pct             REAL DEFAULT 0,
                updated_at          DATETIME DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS lifestyle_profiles (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id             INTEGER REFERENCES user_profiles(id),
                transport_monthly   REAL DEFAULT 0,
                subscriptions_monthly REAL DEFAULT 0,
                leisure_monthly     REAL DEFAULT 0,
                travel_annual       REAL DEFAULT 0,
                luxury_monthly      REAL DEFAULT 0,
                discipline_score    INTEGER DEFAULT 5,
                emotional_spending  INTEGER DEFAULT 5,
                financial_anxiety   INTEGER DEFAULT 5,
                consistency_score   INTEGER DEFAULT 5,
                updated_at          DATETIME DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS family_goals (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id             INTEGER REFERENCES user_profiles(id),
                desired_marriage_age INTEGER,
                desired_first_child_age INTEGER,
                num_children        INTEGER DEFAULT 0,
                family_support_monthly REAL DEFAULT 0,
                parents_dependency  INTEGER DEFAULT 0,
                inheritance_expected REAL DEFAULT 0,
                updated_at          DATETIME DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS real_estate_goals (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id             INTEGER REFERENCES user_profiles(id),
                wants_property      INTEGER DEFAULT 1,
                target_purchase_age INTEGER,
                target_property_value REAL DEFAULT 0,
                rent_vs_buy_pref    TEXT DEFAULT 'Acheter',
                investment_property INTEGER DEFAULT 0,
                current_rent        REAL DEFAULT 0,
                updated_at          DATETIME DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS retirement_goals (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id             INTEGER REFERENCES user_profiles(id),
                target_retirement_age INTEGER DEFAULT 62,
                desired_monthly_pension REAL DEFAULT 0,
                retirement_lifestyle TEXT DEFAULT 'Confortable',
                updated_at          DATETIME DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS saved_scenarios (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER REFERENCES user_profiles(id),
                name        TEXT,
                description TEXT,
                params_json TEXT,
                results_json TEXT,
                created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS monthly_budgets (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id    INTEGER REFERENCES user_profiles(id),
                year       INTEGER,
                month      INTEGER,
                category   TEXT,
                amount     REAL DEFAULT 0,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, year, month, category)
            );

            CREATE TABLE IF NOT EXISTS savings_log (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id       INTEGER REFERENCES user_profiles(id),
                year          INTEGER,
                month         INTEGER,
                target_amount REAL DEFAULT 0,
                actual_amount REAL DEFAULT 0,
                notes         TEXT DEFAULT '',
                updated_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, year, month)
            );
            """)

    # ---- CRUD ----

    def save_profile(self, data: dict) -> int:
        with self._conn() as conn:
            existing = conn.execute("SELECT id FROM user_profiles WHERE name=?", (data.get("name",""),)).fetchone()
            if existing:
                conn.execute("""UPDATE user_profiles SET age=?,country=?,city=?,currency=?,
                marital_status=?,education_level=?,career_field=?,health_notes=?,updated_at=CURRENT_TIMESTAMP
                WHERE id=?""", (
                    data.get("age"), data.get("country"), data.get("city"), data.get("currency"),
                    data.get("marital_status"), data.get("education_level"),
                    data.get("career_field"), data.get("health_notes"), existing["id"]
                ))
                return existing["id"]
            cur = conn.execute("""INSERT INTO user_profiles
                (name,age,country,city,currency,marital_status,education_level,career_field,health_notes)
                VALUES (?,?,?,?,?,?,?,?,?)""", (
                    data.get("name"), data.get("age"), data.get("country"), data.get("city"),
                    data.get("currency"), data.get("marital_status"),
                    data.get("education_level"), data.get("career_field"), data.get("health_notes")
                ))
            return cur.lastrowid

    def save_financial(self, user_id: int, data: dict):
        with self._conn() as conn:
            existing = conn.execute("SELECT id FROM financial_profiles WHERE user_id=?", (user_id,)).fetchone()
            cols = ["monthly_income","side_income","monthly_expenses","monthly_savings",
                    "salary_growth_pct","current_savings","current_investments","current_debt",
                    "monthly_debt_payment","emergency_fund","risk_tolerance","investing_knowledge",
                    "crypto_pct","stocks_pct","etf_pct"]
            vals = [data.get(c, 0) for c in cols]
            if existing:
                set_clause = ", ".join(f"{c}=?" for c in cols)
                conn.execute(f"UPDATE financial_profiles SET {set_clause},updated_at=CURRENT_TIMESTAMP WHERE user_id=?",
                             vals + [user_id])
            else:
                conn.execute(f"INSERT INTO financial_profiles (user_id,{','.join(cols)}) VALUES (?,{','.join('?'*len(cols))})",
                             [user_id] + vals)

    def save_lifestyle(self, user_id: int, data: dict):
        with self._conn() as conn:
            existing = conn.execute("SELECT id FROM lifestyle_profiles WHERE user_id=?", (user_id,)).fetchone()
            cols = ["transport_monthly","subscriptions_monthly","leisure_monthly","travel_annual",
                    "luxury_monthly","discipline_score","emotional_spending","financial_anxiety","consistency_score"]
            vals = [data.get(c, 0) for c in cols]
            if existing:
                set_clause = ", ".join(f"{c}=?" for c in cols)
                conn.execute(f"UPDATE lifestyle_profiles SET {set_clause} WHERE user_id=?", vals + [user_id])
            else:
                conn.execute(f"INSERT INTO lifestyle_profiles (user_id,{','.join(cols)}) VALUES (?,{','.join('?'*len(cols))})",
                             [user_id] + vals)

    def save_family(self, user_id: int, data: dict):
        with self._conn() as conn:
            existing = conn.execute("SELECT id FROM family_goals WHERE user_id=?", (user_id,)).fetchone()
            cols = ["desired_marriage_age","desired_first_child_age","num_children",
                    "family_support_monthly","parents_dependency","inheritance_expected"]
            vals = [data.get(c, 0) for c in cols]
            if existing:
                set_clause = ", ".join(f"{c}=?" for c in cols)
                conn.execute(f"UPDATE family_goals SET {set_clause} WHERE user_id=?", vals + [user_id])
            else:
                conn.execute(f"INSERT INTO family_goals (user_id,{','.join(cols)}) VALUES (?,{','.join('?'*len(cols))})",
                             [user_id] + vals)

    def save_real_estate(self, user_id: int, data: dict):
        with self._conn() as conn:
            existing = conn.execute("SELECT id FROM real_estate_goals WHERE user_id=?", (user_id,)).fetchone()
            cols = ["wants_property","target_purchase_age","target_property_value",
                    "rent_vs_buy_pref","investment_property","current_rent"]
            vals = [data.get(c, 0) for c in cols]
            if existing:
                set_clause = ", ".join(f"{c}=?" for c in cols)
                conn.execute(f"UPDATE real_estate_goals SET {set_clause} WHERE user_id=?", vals + [user_id])
            else:
                conn.execute(f"INSERT INTO real_estate_goals (user_id,{','.join(cols)}) VALUES (?,{','.join('?'*len(cols))})",
                             [user_id] + vals)

    def save_retirement(self, user_id: int, data: dict):
        with self._conn() as conn:
            existing = conn.execute("SELECT id FROM retirement_goals WHERE user_id=?", (user_id,)).fetchone()
            cols = ["target_retirement_age","desired_monthly_pension","retirement_lifestyle"]
            vals = [data.get(c, 0) for c in cols]
            if existing:
                set_clause = ", ".join(f"{c}=?" for c in cols)
                conn.execute(f"UPDATE retirement_goals SET {set_clause} WHERE user_id=?", vals + [user_id])
            else:
                conn.execute(f"INSERT INTO retirement_goals (user_id,{','.join(cols)}) VALUES (?,{','.join('?'*len(cols))})",
                             [user_id] + vals)

    def load_full_profile(self, user_id: int) -> dict:
        with self._conn() as conn:
            up = conn.execute("SELECT * FROM user_profiles WHERE id=?", (user_id,)).fetchone()
            fp = conn.execute("SELECT * FROM financial_profiles WHERE user_id=?", (user_id,)).fetchone()
            lp = conn.execute("SELECT * FROM lifestyle_profiles WHERE user_id=?", (user_id,)).fetchone()
            fg = conn.execute("SELECT * FROM family_goals WHERE user_id=?", (user_id,)).fetchone()
            re = conn.execute("SELECT * FROM real_estate_goals WHERE user_id=?", (user_id,)).fetchone()
            rg = conn.execute("SELECT * FROM retirement_goals WHERE user_id=?", (user_id,)).fetchone()
        result = {}
        for row in [up, fp, lp, fg, re, rg]:
            if row:
                result.update(dict(row))
        return result

    def list_users(self) -> list[dict]:
        with self._conn() as conn:
            rows = conn.execute("SELECT id, name, age, country, updated_at FROM user_profiles ORDER BY updated_at DESC").fetchall()
        return [dict(r) for r in rows]

    def save_scenario(self, user_id: int, name: str, description: str, params: dict, results: dict):
        with self._conn() as conn:
            conn.execute("""INSERT INTO saved_scenarios (user_id,name,description,params_json,results_json)
                            VALUES (?,?,?,?,?)""",
                         (user_id, name, description, json.dumps(params), json.dumps(results)))

    def load_scenarios(self, user_id: int) -> list[dict]:
        with self._conn() as conn:
            rows = conn.execute("SELECT * FROM saved_scenarios WHERE user_id=? ORDER BY created_at DESC", (user_id,)).fetchall()
        return [dict(r) for r in rows]

    # ---- Monthly budget tracking ----

    def save_monthly_budget(self, user_id: int, year: int, month: int, spending: dict):
        with self._conn() as conn:
            for category, amount in spending.items():
                conn.execute("""
                    INSERT INTO monthly_budgets (user_id, year, month, category, amount)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(user_id, year, month, category)
                    DO UPDATE SET amount=excluded.amount, updated_at=CURRENT_TIMESTAMP
                """, (user_id, year, month, category, amount))

    def load_monthly_budget(self, user_id: int, year: int, month: int) -> dict:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT category, amount FROM monthly_budgets WHERE user_id=? AND year=? AND month=?",
                (user_id, year, month)
            ).fetchall()
        return {row["category"]: row["amount"] for row in rows}

    def save_savings_entry(self, user_id: int, year: int, month: int,
                           target: float, actual: float, notes: str = ""):
        with self._conn() as conn:
            conn.execute("""
                INSERT INTO savings_log (user_id, year, month, target_amount, actual_amount, notes)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(user_id, year, month)
                DO UPDATE SET target_amount=excluded.target_amount,
                              actual_amount=excluded.actual_amount,
                              notes=excluded.notes,
                              updated_at=CURRENT_TIMESTAMP
            """, (user_id, year, month, target, actual, notes))

    def load_savings_history(self, user_id: int) -> list:
        with self._conn() as conn:
            rows = conn.execute("""
                SELECT year, month, target_amount, actual_amount, notes
                FROM savings_log WHERE user_id=? ORDER BY year ASC, month ASC
            """, (user_id,)).fetchall()
        return [{"year": r["year"], "month": r["month"],
                 "target": r["target_amount"], "actual": r["actual_amount"],
                 "notes": r["notes"]} for r in rows]
