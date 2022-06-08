# Repo was migrated to AICenter github (ev_db repo)

# Docker Tutorial
Toto je krátký návod pro používání SQL-based databáze pro potřebu spolupráce mezi Škoda Auto a AIC. Databáze běží ve virtuálně v Dockeru. Pro získání dat k databází je nutné napsat Martinovi Schaeferovi (martin.schaefer@fel.cvut.cz), neboť data nemohou být volně k dispozici. Všechny kódy jsou umístěny v mém GIT repozitáři.

Repozitář je rozdělený na dvě složky. Složka PYTHON_CODES obsahuje skripty v Pythonu s SQL dotazy pro získávání dat a jejich následnou vizualizaci.  Složka SETUP obsahuje podklady k Dockeru a SQL databázím. Celá složka SETUP musí mít permission „chmod +x name-of-script“.

## 1. krok
Je nutné mít nainstalovaný Docker z https://hub.docker.com/, zbytek SW si doinstaluje konfigurační soubor našeho Docker Image.


## 2. krok
Pokud již máte vstupní data od Martina, vložte je do SETUP/DIR/IMPORT_DATA. Pro debugovací účely doporučuji používat zmenšený dataset, pár desítek tisíc řádků stačí. Jinak trvá tvorba databáze poměrně velké množství času. Jsou k dispozici exporty dat po jednotlivých měsících nebo celé období rozdělené na 11 menších celků. Je nutné mít stejný název souboru jako ve skriptu ../DIR/populate_database.sh, jinak nedojde k načtení dat.

## 3. krok
Dále už by nemělo nic bránit v cestě vytvoření databáze pomocí příkazu „sh execute.sh populate“,  tento vytvoří databáze a naplní je vstupními daty. Využívá se vícero SQL skriptů pro transformaci dat do správného formátu, vytvoření další tabulek/sloupců, atd.

Každý z těchto skriptů obsahuje krátký popis k čemu slouží. Nicméně se dá celý postup shrnout následovně. Z údajů o zeměpisné šířce, výšce a timestampu vytvoříme GPS souřadnice spojené s timestampem (preprocess_rides.sql). Z GPS souřadnících vytvoříme spojité trajektorie, po kterých vozidla cestovala (trajectories.sql). Tyto trajektorie jsou poté rozděleny na jednotlivé tripy, neboť trajektorie obsahovala jízdy vozidla za celý časový interval, takto je rozdělíme podle stání (create_trips.sql). Cokoliv s dobou stání delší než 5 minut se považuje za další trip (start_end.sql).

Problémem se ukázalo přerušované používání GPS, jelikož pro osobní jízdy si zaměstnanci sledování vypínají, dochází tak k občasným „teleportům“ vozidel.  Dále jsou jednotlivá zastavení v areálu ŠA přiřazena k nejbližší možné nabíječce a zároveň je vyznačeno kdy vozidlo poblíž nabíječky stálo (nn_charger.sql).


## 4. krok
Pokud byla databáze úspěšně vytvořena, tak jí nyní můžeme spustit pomocí příkazu "sh execute alive“, její nastartování trvá přibližně minutu, proto je nutné být trpělivý. Na takto spuštěné databáze lze pak pracovat s kódem PYTHON_CODES/queries1.py a nebo se k ní přímo připojit pomocí příkazu „psql -h localhost -p 35432 -d skoda-postgres -U root“, heslo: sumpr0ject .
