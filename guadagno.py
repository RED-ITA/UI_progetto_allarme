"""# Dati iniziali
C1 = 20  # Capital initial, will calculate relative to initial investment without specifying amount
C2 = 150
# Metodo 1: Un unico acquisto e vendita
acquisto_1 = 53000
vendita_1 = 90000
guadagno_1 = C2 * (vendita_1 - acquisto_1) / acquisto_1
tuoPer = guadagno_1*100/C2
print("tuo metodo:")
print(f" (capitale iniziale: {C2}) * ({vendita_1} - {acquisto_1}) / {acquisto_1} -> ricavato {guadagno_1} (cioè il {tuoPer}%)")
# Metodo 2: Due acquisti e vendite
# Prima transazione
acquisto_2_1 = 47000
vendita_2_1 = 70000
guadagno_2_1 = C1 * (vendita_2_1 - acquisto_2_1) / acquisto_2_1

# Capitale dopo la prima transazione
capitale_post_1 = C1 * (vendita_2_1 / acquisto_2_1)

# Seconda transazione
acquisto_2_2 = 50000
vendita_2_2 = 90000
guadagno_2_2 = capitale_post_1 * (vendita_2_2 - acquisto_2_2) / acquisto_2_2

# Guadagno totale del secondo metodo
guadagno_2_totale = guadagno_2_1 + guadagno_2_2
mioPer = guadagno_2_totale*100/C1

print("mio metodo:")
print(f" (capitale iniziale: {C1}) * ({vendita_2_1} - {acquisto_2_1}) / {acquisto_2_1} -> ricavato {guadagno_2_1}")
print(f" (capitale iniziale nuovo: {capitale_post_1}) * ({vendita_2_2} - {acquisto_2_2}) / {acquisto_2_2} -> ricavato {guadagno_2_2}")
print(f"mio guadagno = somma dei due -> {guadagno_2_totale} (cioè il {mioPer}%)")
guadagno_1, guadagno_2_totale

print("resto pover, buon natale")"""

