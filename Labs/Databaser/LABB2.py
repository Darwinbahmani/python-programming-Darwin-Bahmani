 
from sqlalchemy import create_engine, text

# Anslutning
server = "DARWIN"
database = "BOKHANDEL"
driver = "ODBC Driver 17 for SQL Server"

engine = create_engine(
    f"mssql+pyodbc://{server}/{database}?trusted_connection=yes&driver={driver}"
)

# SQL-fråga
query = text("""
    SELECT Böcker.Titel, Butiker.Namn AS Butik, LagerSaldo.Antal
    FROM Böcker
    JOIN LagerSaldo ON Böcker.ISBN13 = LagerSaldo.ISBN
    JOIN Butiker ON LagerSaldo.ButikID = Butiker.ID
    WHERE Böcker.Titel LIKE :sökterm
    ORDER BY Böcker.Titel, Butik
""")

# Funktion för sökning
def sök_böcker(titel_del):
    with engine.connect() as conn:
        resultat = conn.execute(query, {"sökterm": f"%{titel_del}%"})
        rader = resultat.fetchall()
        if not rader:
            print("Inga träffar på titeln.")
        else:
            print("\nTräffar:")
            for rad in rader:
                print(f"{rad.Titel} – {rad.Butik}: {rad.Antal} st")

# Programkörning
if __name__ == "__main__":
    print("Boktitel-sökning i BOKHANDEL\n")
    while True:
        sök = input("Skriv del av titel (eller 'q' för att avsluta): ")
        if sök.lower() == 'q':
            print("Avslutar...")
            break
        sök_böcker(sök)



