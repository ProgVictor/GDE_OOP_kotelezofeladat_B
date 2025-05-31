from abc import ABC, abstractmethod
from datetime import datetime
import uuid

class Jarat(ABC):
     def __init__(self, jaratszam, celallomas, jegyar):
         self.jaratszam = jaratszam
         self.celallomas = celallomas
         self.jegyar = jegyar

class BelfoldiJarat(Jarat):

    def __init__(self,jaratszam, celallomas, jegyar):
         super().__init__(jaratszam,celallomas,jegyar)
    def get_info(self):
         return f"Belföldi Járat: {self.jaratszam}-->{self.celallomas}, Ár: {self.jegyar} Ft"

class NemzetkoziJarat(Jarat):

    def __init__(self,jaratszam, celallomas, jegyar):
         super().__init__(jaratszam,celallomas,jegyar)
    def get_info(self):
         return f"Nemzetközi Járat: {self.jaratszam}-->{self.celallomas}, Ár: {self.jegyar} Ft"

class JegyFoglalas:
    def __init__(self,foglalas_id, jarat,datum):
        self.foglalas_id = foglalas_id
        self.jarat = jarat
        self.datum = datum
    def __str__(self):
        return f"Foglalás ID: {self.foglalas_id}, Járat:{self.jarat.jaratszam}, Dátum:{self.datum}, Ár: {self.jarat.jegyar} Ft"

class LegiTarsasag:
        def __init__(self,nev):
             self.nev = nev
             self.jaratok = []
             self.foglalasok = {}
        def jarat_hozzaadas(self,jarat):
             self.jaratok.append(jarat)
        def jarat_kereses(self,jaratszam):
             return next((j for j in self.jaratok if j.jaratszam == jaratszam),None)
        def jegy_foglalas(self,jaratszam,datum_str):
            jarat = self.jarat_kereses(jaratszam)
            if not jarat:
                  return "Hiba: A megadott járat nem létezik."
            try:
             datum = datetime.strptime(datum_str,"%Y-%m-%d")
             if datum < datetime.now():
                  return "Hiba: A dátum nem lehet múltbéli."
            except ValueError:
             return "Hiba: Hibás dátumformátum. Használja ÉÉÉÉ-HH-NN." 
            
            foglalas_id = str(uuid.uuid4())[:8]
            foglalas = JegyFoglalas(foglalas_id,jarat,datum_str)
            self.foglalasok[foglalas_id]=foglalas
            return f"Sikeres foglalás! Foglalás ID: {foglalas_id}, Ár: {jarat.jegyar} Ft"
        
        def foglalas_lemondas(self,foglalas_id):
            if foglalas_id in self.foglalasok:
                del self.foglalasok[foglalas_id]
                return "A foglalás sikeresen törölve lett."
            else:
                return "Hiba: A foglalás nem található."
        
        def foglalasok_listazasa(self):
            if not self.foglalasok:
                return "Nincs aktív foglalás."
            return "\n".join(str(f) for f in self.foglalasok.values())
        
        def elore_betoltott_adatok():
            lt = LegiTarsasag("SkyFly")
            lt.jarat_hozzaadas(BelfoldiJarat("BF101","Budapest",10000))
            lt.jarat_hozzaadas(BelfoldiJarat("BF102","Debrecen",8000))
            lt.jarat_hozzaadas(BelfoldiJarat(NemzetkoziJarat("NZ201","London",30000)))

            lt.jegy_foglalas("BF101","2025-07-10")
            lt.jegy_foglalas("BF102","2025-07-16")
            lt.jegy_foglalas("NZ201","2025-08-05")
            lt.jegy_foglalas("BF101","2025-08-17")
            lt.jegy_foglalas("NZ201","2025-08-22")
            lt.jegy_foglalas("BF102","2025-09-03")
            return lt
        
        def menu(lt):
            while True:
                print("1.Jegy foglalása")
                print("2.Foglalás lemondása")
                print("3.Foglalások listázása")
                valasz = input("Válasszon műveletet: ")
                if valasz == "1":
                    print("Elérhető járatok:")
                    for jarat in lt.jaratok:
                        print(jarat.get_info())
                    jaratszam = input("Adja meg a járatszámot: ")
                    datum = input("Adja meg az utazás dátumát(ÉÉÉÉ-HH-NN): ")
                    print(lt.jegy_foglalas(jaratszam,datum))
                elif valasz == "2":
                    foglalas_id = input("Adja meg a lemondandó foglalás azonosítóját: ")
                    print(lt.foglalas_lemondas(foglalas_id))
                elif valasz == "3":
                    print("\nAktív foglalások:")
                    print(lt.foglalasok_listazasa())
                elif valasz == "4":
                    print("Kilépés...")
                    break
                else:
                    print("Hibás választás. Próbálja újra")
                    break

        if __name__ == "__main__":
            legitarsasag = elore_betoltott_adatok()
            menu(legitarsasag)
