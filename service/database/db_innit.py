import sqlite3
from pathlib import Path

# Chemins vers la base de données et la configuration Alembic
DATABASE_PATH = Path(__file__).resolve().with_name("time.db")
ALEMBIC_INI_PATH = Path(__file__).resolve().parent.parent / "alembic.ini"


def create_initial_database():
    """Branche 'NON' : Création initiale de la base et de ses tables."""
    print("Base inexistante. Création initiale de la base de données...")
    
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS screen_time (
                user_id INTEGER NOT NULL,
                app_name TEXT NOT NULL,
                total_duration REAL NOT NULL DEFAULT 0.0,
                number_of_sessions INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (user_id, app_name)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                app_name TEXT NOT NULL,
                started_at TEXT NOT NULL,
                ended_at TEXT,
                duration REAL
            )
        """)
        conn.commit()

    print(f"Base et tables créées avec succès dans {DATABASE_PATH}")

    # IMPORTANT pour Alembic :
    # Si alembic est installé et configuré, on marque la base comme étant
    # déjà à jour ('head') pour éviter qu'Alembic n'essaie de recréer ces tables plus tard.
    if ALEMBIC_INI_PATH.exists():
        try:
            from alembic import command
            from alembic.config import Config

            alembic_cfg = Config(str(ALEMBIC_INI_PATH))
            command.stamp(alembic_cfg, "head")
            print("Alembic : version synchronisée sur 'head'.")
        except Exception as e:
            print(f"Note : synchronisation Alembic ignorée ({e})")


def apply_migrations():
    """Branche 'OUI' : Tenter d'appliquer les migrations existantes."""
    print("La base existe déjà. Tentative d'application des migrations...")
    
    if not ALEMBIC_INI_PATH.exists():
        print("Fichier 'alembic.ini' introuvable : aucune migration à appliquer.")
        return

    try:
        from alembic import command
        from alembic.config import Config

        alembic_cfg = Config(str(ALEMBIC_INI_PATH))
        command.upgrade(alembic_cfg, "head")
        print("Migrations appliquées avec succès !")
    except Exception as e:
        print(f"Erreur lors de l'application des migrations : {e}")


def setup_database():
    """Point d'entrée correspondant à votre diagramme."""
    if not DATABASE_PATH.exists():
        # Branche NON
        create_initial_database()
    else:
        # Branche OUI
        apply_migrations()


if __name__ == "__main__":
    setup_database()