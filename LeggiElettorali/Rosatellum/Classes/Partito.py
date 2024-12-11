import pandas as pd
import numpy as np
import yaml

from src import cleanup

# inizializzo questa classe usando una configurazione yaml
# creo una metaclasse metas_p che eredita da loger, PolEnt e party ed è subclass di PolEnt
conf = 'metaclasses:\n  - logger\n  - PolEnt\n  - party\n\nsubclass:\n  - PolEnt'

conf = yaml.safe_load(conf)

metas_p = list(map(eval, conf.pop("metaclasses")))
metas_p.append(cleanup)

# istanzio la metaclasse, ottenendo la classe comb_p
comb_p = type("combPol", tuple(metas_p), {})


class Partito(metaclass=comb_p, **conf):
    SOGLIA_PARTITO = 0.03
    SOGLIA_COALIZIONE = 0.10
    def filter(self, district, *, total, row, dataframe, sbarramenti, **kwargs):
        if sbarramenti[0] == 'soglia' and district.type == 'Nazione':
            tot_voti = dataframe['Voti'].sum()
            p_voti = row['Voti']
            # Verifica se il partito è parte di una coalizione
            coalizione = row.get('Coalizione')
            if coalizione:
                # Somma i voti dei partiti appartenenti alla stessa coalizione
                voti_coalizione = dataframe[dataframe['Coalizione'] == coalizione]['Voti'].sum()
                print(f"Verifica soglia per coalizione {coalizione}: {voti_coalizione}/{tot_voti * self.SOGLIA_COALIZIONE}")
                return voti_coalizione >= tot_voti * self.SOGLIA_COALIZIONE
            else:
                print(f"Verifica soglia per partito {row['Partito']}: {p_voti}/{tot_voti * self.SOGLIA_PARTITO}")
                return p_voti >= tot_voti * self.SOGLIA_PARTITO
        return True
